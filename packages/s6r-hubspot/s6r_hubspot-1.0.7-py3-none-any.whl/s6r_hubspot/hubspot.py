import json
import logging
import time
import requests
from .custom_object import CustomObject
from .hub_db import HubDb


class ExpiredToken(Exception):
    pass


def split(list_a, chunk_size):
    for i in range(0, len(list_a), chunk_size):
        yield list_a[i:i + chunk_size]


class HubspotConnection(HubDb, CustomObject):
    models_properties = {
        'contact': ['firstname', 'lastname', 'email', 'phone', 'mobilephone', 'jobtitle'],
        'company': ['name', 'address', 'address2', 'zip', 'city', 'country', 'phone'],
    }

    def __init__(self, token=False, get_token=False, set_token=False, debug=False):
        """
        init Hubspot connection with token
        :param token: Hubspot token to connect to api
        :param debug: is run in debug mode
        """
        super().__init__(debug=debug)
        self.logger = logging.getLogger()
        if debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
        self._token = token
        self._refresh_token = False
        self._get_token = get_token
        self._set_token = set_token
        self._init_token()
        self._url = "https://api.hubapi.com"
        self._prepare_headers()

    def _init_token(self):
        if self._get_token:
            token = self._get_token()
            self._token = token['access_token']
            self._refresh_token = token['refresh_token']
            self._client_id = token['client_id']
            self._client_secret = token['client_secret']

    def _renew_token(self):
        if self._refresh_token:
            r = requests.post('https://api.hubapi.com/oauth/v1/token',
                              headers={
                                  'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
                              },
                              data={
                                  'grant_type': 'refresh_token',
                                  'client_id': self._client_id,
                                  'client_secret': self._client_secret,
                                  'refresh_token': self._refresh_token,
                              })
            res = r.json()
            if not 'access_token' in res:
                self.logger.error(r.json())
            self._token = res['access_token']
            self._refresh_token = res['refresh_token']
            self._prepare_headers()
            self._set_token(res['access_token'], res['refresh_token'], self._client_id, self._client_secret)

    def _prepare_headers(self):
        """
        set header to connect to Hubspot api
        """
        self._headers = {
            "Authorization": "Bearer %s" % (self._token,),
            "content-type": "application/json"
        }
        self._headers_import = {
            "Authorization": "Bearer %s" % (self._token,),
            # "content-type": "multipart/form-data",
        }

    def get_limit_error(self, data):
        condition = (
            'errorType' in data and
            data['errorType'] == 'RATE_LIMIT' and
            data['message'] != 'You have reached your daily limit.'
        )
        if condition:
            return True
        return False

    def retrieve(self, model, params=None, limit=100, after=0, cc=0):
        params = params or {}
        url = '%s/crm/v3/objects/%s' % (self._url, model)
        params['limit'] = limit
        if after != '{}':
            params['after'] = after
        data = requests.get(url, params=params, headers=self._headers).json()
        after = data.get('paging', {}).get('next', {}).get('after', {})
        results = data['results'] if data.get('results') else []

        if after and cc < 20:
            return results + self.retrieve(model, params=params, limit=100, after=after, cc=cc + 1)[0], after

        return results, after

    def send_request_response_with_status(self, url, params, max_retries, retry_delay):
        retries = 0
        while retries < max_retries:
            response = requests.post(url, data=params, headers=self._headers)
            data = response.json()
            if data['status'] == 'COMPLETE':
                return data['results']
            else:
                retries = self.check_error(data, response, retries, retry_delay)
        return []

    def send_request_response_with_paging(self, model, url, params, function_name, max_retries, retry_delay, **kwargs):
        results = kwargs.get('results', [])
        retries = 0
        while retries < max_retries:
            response = requests.post(url, data=params, headers=self._headers)
            data = response.json()
            if ('status' in data and data['status'] == 'COMPLETE') or ('total' in data):
                results += data['results']
                after = data.get('paging', {}).get('next', {}).get('after', {})
                if after and int(after) < 9900:
                    return getattr(self, function_name)(model, after=after, **kwargs)
                elif after:
                    self.logger.error('Try to search something with more than 10000 results, use get_all instead')
                    return results
                else:
                    return results
            else:
                retries = self.check_error(data, response, retries, retry_delay)
        return []

    def check_error(self, data, response, retries, retry_delay=1):
        if 'category' in data and data['category'] == 'EXPIRED_AUTHENTICATION':
            self.logger.info("Renew token")
            self._renew_token()
            retries += 1
        if response.status_code == 429:  # 429 Too Many Requests
            self.logger.info("Rate limit reached, retrying.")
            time.sleep(retry_delay)
            retries += 1
        else:
            raise Exception(data['message'])
        return retries

    def create(self, model, vals_list, chunk_size=95, max_retries=3, retry_delay=1):
        """
        method call to create new objets in model hubspot
        :param model: string model hubspot
        :param vals_list: list of object to create
        :param chunk_size: size of batch send to hubspot
        """
        result = []
        url = "%s/crm/v3/objects/%s/batch/create" % (self._url, model)
        for split_val_list in list(split(vals_list, chunk_size)):
            params = {
                "inputs": split_val_list
            }
            result.extend(self.send_request_response_with_status(url, json.dumps(params), max_retries, retry_delay))
        return result

    def update(self, model, vals_list, max_retries=3, retry_delay=1):
        """
        method call to update objects in hubspot
        :param model: string model hubspot
        :param vals_list: list of object to update
        :param max_retries: maximum number of retries
        :param retry_delay: delay between retries in seconds
        """
        result = []
        url = "%s/crm/v3/objects/%s/batch/update" % (self._url, model)
        for split_val_list in list(split(vals_list, 95)):
            params = {
                "inputs": split_val_list
            }
            result.extend(self.send_request_response_with_status(url, json.dumps(params), max_retries, retry_delay))
        return result

    def search(self, model, after=0, max_retries=3, retry_delay=1, **kwargs):
        """
        method call to search objects in hubspot
        :param model: string model hubspot
        :param after:
        :param max_retries: maximum number of retries
        :param retry_delay: delay between retries in seconds
        :param kwargs:
                filters,
                filter_groups,
                properties,
                associations,
                results,
                load_associations,
                limit
                sorts
        """
        results = kwargs.get('results', [])
        properties = kwargs.get('properties', [])
        filters = kwargs.get('filters', [])
        filter_groups = kwargs.get('filterGroups', [])
        associations = kwargs.get('associations', [])
        load_associations = kwargs.get('load_associations', False)
        sorts = kwargs.get('sorts', [])
        limit = kwargs.get('limit', 95)
        params = {
            "filterGroups": [
                {
                    "filters": filters
                }
            ],
            "limit": limit,
            "after": after,
            "sorts": sorts
        }
        if filter_groups:
            params['filterGroups'] = filter_groups
        if properties:
            params["properties"] = properties
        url = "%s/crm/v3/objects/%s/search" % (self._url, model)
        self.send_request_response_with_paging(model, url, json.dumps(params), 'search', max_retries,
                                                              retry_delay, filters=filters, results=results,
                                                              associations=associations,
                                                              load_associations=load_associations,
                                                              properties=properties)
        association_result = {}
        for association in associations:
            association_result[association] = {
                i['from']['id']: i for i in self.get_association(model, association, [i['id'] for i in results])
            }
        for result in results:
            for association in associations:
                if result['id'] in association_result[association]:
                    result["_%s" % association] = [{
                        'id': i['toObjectId'],
                        'label': [i['associationTypes'][j]['label'] for j in range(len(i['associationTypes']))]
                    } for i in association_result[association][result['id']]['to']]
        if load_associations:
            results = self._load_associations_properties(associations, results)
        return results

    def _load_associations_properties(self, associations, results):
        for association in associations:
            ids = []
            for r in results:
                ids.extend([rec['id'] for rec in r['_%s' % association]])
            if not ids:
                continue
            ids = set(ids)
            association_cache = {str(rec_id): None for rec_id in ids}
            properties = self.models_properties.get(association, [])
            association_datas = self.read(association, list(ids), properties)
            for association_data in association_datas:
                association_cache[association_data['id']] = association_data

            for result in results:
                for rec in result['_%s' % association]:
                    rec_id = rec['id']
                    res_values = association_cache[str(rec_id)]
                    properties = res_values.pop('properties')
                    rec.update(res_values)
                    rec['properties'] = properties
        return results

    def get_association(self, model_from, model_to, ids, after=0, cc=0, results=None):
        """
        get associate objects identify by model_from and their ids, to objects from model_to
        :param model_from: string hubspot model
        :param model_to: string hubspot model
        :param ids: list of ids
        :param after: int page number to begin request
        :param cc: int number of page return
        :param results: previous result list from recurtion
        :return: result from get request
        """
        results = results or []
        params = {
            "inputs": [{
                "id": id,
            } for id in ids]
        }
        url = "%s/crm/v4/associations/%s/%s/batch/read" % (self._url, model_from, model_to)
        data = requests.post(url, data=json.dumps(params), headers=self._headers).json()
        if data['status'] == 'COMPLETE':
            results += data['results']
            after = data.get('paging', {}).get('next', {}).get('after', {})
            if after:
                return self.get_association(model_from, model_to, ids, after=after, cc=cc + 1, results=results)
        else:
            self.logger.error(data['message'])
            if 'category' in data and data['category'] == 'EXPIRED_AUTHENTICATION':
                self._renew_token()
                return self.get_association(model_from, model_to, ids, after=after, cc=cc, results=results)
            elif self.get_limit_error(data):
                time.sleep(1.5)
                return self.get_association(model_from, model_to, ids, after=after, cc=cc, results=results)
            else:
                raise Exception(data['message'])
        return results

    def read(self, model, ids, properties, associations=[], propertiesWithHistory=[], property_name="id", retry_delay=1, max_retries=3):
        results = []
        for ids_split in list(split(ids, 95)):
            params = {
                "properties": properties,
                "propertiesWithHistory": propertiesWithHistory,
                "inputs": [
                    {
                        "id": id
                    } for id in ids_split
                ]
            }
            if property_name != 'id':
                params['idProperty'] = property_name
            url = "%s/crm/v3/objects/%s/batch/read" % (self._url, model)
            results.extend(self.send_request_response_with_status(url, json.dumps(params), retry_delay, max_retries))
        association_result = {}
        for association in associations:
            association_result[association] = {i['from']['id']: i for i in
                                               self.get_association(model, association, [i['id'] for i in results])}
        for result in results:
            for association in associations:
                if result['id'] in association_result[association]:
                    result["_%s" % (association)] = [{
                        'id': i['toObjectId'],
                        'label': [i['associationTypes'][j]['label'] for j in range(len(i['associationTypes']))]
                    } for i in association_result[association][result['id']]['to']]
        return results

    def get_all(self, model, properties, associations=None, after=0, cc=0, results=None):
        associations = associations or []
        results = results or []
        url = "%s/crm/v3/objects/%s?limit=100&after=%s&properties=%s" % (
            self._url, model, after, ','.join(properties))
        data = requests.get(url, headers=self._headers).json()
        if 'results' in data:
            results += data['results']
            association_result = {}
            for association in associations:
                association_result[association] = {
                    i['from']['id']: i for i in
                    self.get_association(model, association, [i['id'] for i in results])
                }
            for result in results:
                for association in associations:
                    if result['id'] in association_result[association]:
                        result["_%s" % (association)] = [{
                            'id': i['toObjectId'],
                            'label': [i['associationTypes'][j]['label'] for j in range(len(i['associationTypes']))]
                        } for i in association_result[association][result['id']]['to']]
            after = data.get('paging', {}).get('next', {}).get('after', {})
            if after:
                return self.get_all(
                    model,
                    properties,
                    associations=associations,
                    after=after,
                    cc=cc + 1,
                    results=results
                )
        else:
            self.logger.error(data['message'])
            if 'category' in data and data['category'] == 'EXPIRED_AUTHENTICATION':
                self._renew_token()
                return results + self.get_all(
                    model=model,
                    properties=properties,
                    associations=associations,
                    after=after,
                    cc=cc,
                    results=results
                )
            elif self.get_limit_error(data):
                time.sleep(1.5)
                return self.get_all(
                    model=model,
                    properties=properties,
                    associations=associations,
                    after=after,
                    cc=cc,
                    results=results
                )
            else:
                raise Exception(data['message'])
        return results

    def archive(self, model, ids):
        """
        archive object in hubspot identify by model and ids
        :param model: string hubspot model
        :param ids: list of ids
        :return: data archived in hubspot
        """
        for ids_split in list(split(ids, 95)):
            params = {
                "inputs": [{'id': id} for id in ids_split]
            }
            url = "%s/crm/v3/objects/%s/batch/archive" % (self._url, model)
            res = requests.post(url, data=json.dumps(params), headers=self._headers)
            self.logger.info('archive %s' % res)
        return res

    def _get_properties(self, model):
        """
        :param model: string hubspot model
        :return: all properties from hubspot model
        """
        url = "%s/crm/v3/properties/%s" % (self._url, model)
        data = requests.get(url, headers=self._headers).json()
        results = data['results'] if data.get('results') else []
        return results

    def _search_properties(self, model, keyword):
        """
        :param model: string hubspot model
        :param keyword: string keyword to search in property name and description
        :return: properties found with the keyword
        """
        results = self._get_properties(model)
        keyword = keyword.lower()
        return [f for f in results if keyword in f['name'] or keyword in f['description'].lower()]

    def _create_properties(self, model, params):
        """
        :param model: string hubspot model
        :return:
        """
        url = "%s/crm/v3/properties/%s/batch/create" % (self._url, model)
        data = requests.post(url, data=json.dumps(params), headers=self._headers).json()
        if 'errors' in data and 'category' in data['errors'] and data['errors']['category'] == 'OBJECT_ALREADY_EXISTS':
            return data
        elif not 'results' in data:
            raise Exception(data['message'])
        return data

    def _update_properties(self, model, name, params):
        url = "%s/crm/v3/properties/%s/%s" % (self._url, model, name)
        data = requests.patch(url, data=json.dumps(params), headers=self._headers).json()
        return data

    def _archive_properties(self, model, name):
        url = "%s/crm/v3/properties/%s/%s" % (self._url, model, name)
        requests.delete(url, headers=self._headers)

    def get_owner(self, owner_id):
        """
        method call to get owner with id from hubspot crm api
        """
        url = "%s/crm/v3/owners/%s" % (self._url, owner_id)
        result = requests.get(url, headers=self._headers).json()
        if 'status' not in result:
            return result
        else:
            self.logger.error(result['message'])
            if result['category'] == 'EXPIRED_AUTHENTICATION':
                self._renew_token()
                return self.get_owner(owner_id)
            elif ('errorType' in result and
                  result['errorType'] == 'RATE_LIMIT' and
                  result['message'] != 'You have reached your daily limit.'):
                time.sleep(1.5)
                return self.get_owner(owner_id)
            else:
                raise Exception(result['message'])

    def get_owners(self):
        """
        method call to get all owners from hubspot crm api
        """
        url = "%s/crm/v3/owners" % (self._url)
        data = requests.get(url, headers=self._headers).json()
        if 'status' not in data:
            return data['results']
        else:
            self.logger.error(data['message'])
            if 'category' in data and data['category'] == 'EXPIRED_AUTHENTICATION':
                self._renew_token()
                return self.get_owners()
            elif self.get_limit_error(data):
                time.sleep(1.5)
                return self.get_owners()
            else:
                raise Exception(data['message'])

    def create_association(self, model_from, model_to, vals):
        """
        :param model_from: string hubspot model to associate
        :param model_to: string hubspot model to associate
        :param vals: list of dictionary with from id, to id and type of association
        example:
        [
            {
                "from": {
                    "id": "53628"
                },
                "to": {
                    "id": "12726"
                },
                "type": "contact_to_company"
            }
        ]
        :return: request result
        """
        result = []
        for split_val_list in list(split(vals, 75)):
            params = {
                "inputs": split_val_list
            }
            url = "%s/crm/v4/associations/%s/%s/batch/create" % (self._url, model_from, model_to)
            data = requests.post(url, data=json.dumps(params), headers=self._headers).json()
            if data['status'] == 'COMPLETE':
                result.append(data)
            else:
                self.logger.error(data['message'])
                if 'category' in data and data['category'] == 'EXPIRED_AUTHENTICATION':
                    self._renew_token()
                    return self.create_association(model_from, model_to, split_val_list)
                elif self.get_limit_error(data):
                    time.sleep(1.5)
                    data = requests.post(url, data=json.dumps(params), headers=self._headers).json()
                    if data['status'] == 'COMPLETE':
                        result.append(data)
                else:
                    raise Exception(data['message'])
        return result

    def get_stage(self, model, pipeline_id, stage_id):
        """
        :param model: string hubspot model
        :param pipeline_id: hubspot pipeline id
        :param stage_id: hubspot stage id
        :return: stage informations from pipeline and hubspot model
        """
        url = "%s/crm/v3/pipelines/%s/%s/stages/%s" % (self._url, model, pipeline_id, stage_id)
        data = requests.get(url, headers=self._headers).json()
        if 'status' in data:
            self.logger.error(data['message'])
            if 'category' in data and data['category'] == 'EXPIRED_AUTHENTICATION':
                self._renew_token()
                return self.get_stage(model, pipeline_id, stage_id)
            elif self.get_limit_error(data):
                time.sleep(1.5)
                return self.get_stage(model, pipeline_id, stage_id)
            else:
                raise Exception(data['message'])
        else:
            return data

    def get_pipeline(self, model, pipeline_id):
        """
        :param model: string hubspot model
        :param pipeline_id: hubspot pipeline id
        :return: pipeline information from hubspot model
        """
        url = "%s/crm/v3/pipelines/%s/%s" % (self._url, model, pipeline_id)
        data = requests.get(url, headers=self._headers).json()
        if 'status' in data:
            self.logger.error(data['message'])
            if 'category' in data and data['category'] == 'EXPIRED_AUTHENTICATION':
                self._renew_token()
                return self.get_stage(model, pipeline_id)
            elif self.get_limit_error(data):
                time.sleep(1.5)
                return self.get_stage(model, pipeline_id)
            else:
                raise Exception(data['message'])
        else:
            return data

    def get_association_label(self, model_from, model_to):
        """
        method call to get label from association hubspot crm api
        """
        url = "%s/crm/v4/associations/%s/%s/labels" % (self._url, model_from, model_to)
        data = requests.get(url, headers=self._headers).json()
        if 'status' not in data:
            return data
        else:
            self.logger.error(data['message'])
            if data['category'] == 'EXPIRED_AUTHENTICATION':
                self._renew_token()
                return self.get_association_label()
            elif self.get_limit_error(data):
                time.sleep(1.5)
                return self.get_association_label()
            else:
                raise Exception(data['message'])

    def delete_notes(self, note_id):
        url = "%s/crm/v3/objects/notes/%s" % (self._url, note_id)
        requests.delete(url, headers=self._headers)

    def delete_associations(self, model_from, model_to, vals):
        for split_val_list in list(split(vals, 100)):
            params = {"inputs": split_val_list}
            url = "%s/crm/v4/associations/%s/%s/batch/archive" % (self._url, model_from, model_to)
            requests.post(url, data=json.dumps(params), headers=self._headers)

    def get_pipelines(self, model):
        """
        :param model: string hubspot model
        :return: pipelines and stages from hubspot model
        """

        url = "%s/crm/v3/pipelines/%s" % (self._url, model)
        data = requests.get(url, headers=self._headers).json()
        results = data['results']
        return results

    def create_folder(self, name, parent_folder_id=''):
        url = '%s/files/v3/folders' % (self._url,)
        params = {
            'name': name,
        }
        if parent_folder_id:
            params['parentFolderId'] = parent_folder_id
        hubspot_data = requests.post(url, data=json.dumps(params), headers=self._headers).json()

        return hubspot_data

    def search_folder(self):
        url = '%s/files/v3/folders/search' % (self._url,)
        hubspot_data = requests.get(url, headers=self._headers).json()
        return hubspot_data

    def update_folder_name(self, new_name, folder_id):
        url = '%s/files/v3/folders/update/async' % (self._url,)
        params = {
            'name': new_name,
            'id': folder_id,
        }
        hubspot_data = requests.post(url, data=json.dumps(params), headers=self._headers).json()

        return hubspot_data

    def delete_folder(self, folder_id):
        url = '%s/files/v3/folders' % (self._url,)
        params = {
            'folder_id': folder_id
        }
        hubspot_data = requests.delete(url, data=json.dumps(params), headers=self._headers)
        return hubspot_data

    def upload_file(self, file, name, folder_id):
        url = '%s/files/v3/files' % (self._url,)
        options = json.dumps({
            'access': 'PUBLIC_INDEXABLE',
            'overwrite': True,
        })
        files = {
            'file': file,
        }
        params = {
            'folderId': folder_id,
            'options': options,
            'fileName': name,
        }
        headers = {
            "authorization": "Bearer %s" % (self._token,)
        }

        hubspot_data = requests.post(url, files=files, data=params, headers=headers)
        return json.loads(hubspot_data.text)

    def retrieve_owner(self, user_id):
        url = "%s/crm/v3/owners/%s" % (self._url, user_id)
        params = {}
        data = requests.get(url, params=params, headers=self._headers).json()
        return data

    def import_file(self, model, datas, keys):
        """
        Method call to import a csv file into an object
        :param model: string, hubspot object ID
        :param datas: list of dict that contains the lines of the csv file
        :param keys: list of tuple that contains the (variable_name, variable label)
        :return:
        """
        name = "%s_%s" % (model, datetime.datetime.now().strftime('%Y%m%d_%H%M'))
        filename = "%s.csv" % (name)
        params = {
            "name": name,
            "files": [{
                "fileName": filename,
                "importOperations": {
                    "0-1": "UPDATE"
                },
                "fileFormat": "CSV",
                "fileImportPage": {
                    "hasHeader": True,
                    "columnMappings": [{
                        "ignored": False,
                        "columnName": j,
                        "idColumnType": 'HUBSPOT_ALTERNATE_ID' if i == 'id_odoo' else None,
                        "propertyName": i,
                        "foreignKeyType": None,
                        "columnObjectTypeId": model,
                        "associationIdentifiedColumn": False
                        } for i,j in keys
                    ]
                }
            }]
        }

        with open('/tmp/%s'%(filename),'w', newline='') as csvfile:
            fieldnames = [i for i,j in keys]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for data in datas:
                writer.writerow(data)

        files = {
            'importRequest': (None, json.dumps(params), 'application/json'),
            'files': open('/tmp/%s'%(filename), 'rb')
        }
        url = "%s/crm/v3/imports" % (self._url)
        response = requests.post(url, headers=self._headers_import, files=files)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            self.logger.info(f"Failed to fetch rows. Response: %s", response.text)
            return []
