import json
import logging
import requests


class CustomObject:

    def __init__(self, debug=False):
        """
        init Hubspot connection with token
        :param debug: is run in debug mode
        """
        self.logger = logging.getLogger()
        if debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

    def get_custom_object(self):
        """
        method call to get all customobject
        """
        url = "%s/crm/v3/schemas" % (self._url)
        response = requests.get(url, headers=self._headers)
        self.logger.info('================= %s', response.json())
        if response.status_code in [200, 201]:
            data = response.json()
            return data.get('results', [])
        return False

    def create_custom_object(self, name, label):
        """
        """
        params = {
            "name": name,
            "label": label,
            "labels": {
                "plural": label,
                "singular": label,
            },
            "primaryDisplayProperty": "id_odoo",
            "properties": [
                {
                    "name": "id_odoo",
                    "label": "Odoo ID",
                    "isPrimaryDisplayLabel": True,
                    "hasUniqueValue": True,
                }
            ],
        }
        url = "%s//crm/v3/schemas" % (self._url)
        response = requests.post(url, data=json.dumps(params), headers=self._headers)
        self.logger.info('================= %s', response.json())
        if response.status_code in [200, 201]:
            return response.json()
        return False

    def update_custom_object(self, co_id, name, properties):
        """
        """
        params = {
            "name": name,
        }
        if properties:
            params['properties'] = properties
        url = "%s/crm/v3/schemas/%s" % (self._url, co_id)
        response = requests.patch(url, data=json.dumps(params), headers=self._headers)
        self.logger.info('================= %s', response.json())
        if response.status_code in [200, 201]:
            return response.json()
        return False

    def list_on_custom_object(self, object_type):
        url = "%s/crm/v3/properties/%s" % (self._url, object_type)
        data = requests.get(url, headers=self._headers).json()
        return data

    def create_on_custom_object(self, object_type, vals):
        params = {
            "properties": vals
        }
        url = "%s/crm/v3/objects/%s" % (self._url, object_type)
        data = requests.post(url, data=json.dumps(params), headers=self._headers).json()
        return data
