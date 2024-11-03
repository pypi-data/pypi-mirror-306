import json
import logging
import requests


class HubDb:

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

    def get_hub_db(self):
        """
        method call to get all hubdb tables
        """
        url = "%s/hubdb/api/v2/tables" % (self._url)
        response = requests.get(url, headers=self._headers)
        if response.status_code in [200, 201]:
            data = response.json()
            return data.get('objects', [])
        return response

    def delete_hub_db(self, table_id, row_id):
        """
        :param table_id: HubDB table ID
        :param row_id: Row ID
        :return: Delete the row in the hubdb table
        """
        url = "%s/cms/v3/hubdb/tables/%s/rows/%s/draft" % (self._url, table_id, row_id)
        response = requests.delete(url, headers=self._headers)
        if response.status_code == 204:
            return 'The row ID %s has been deleted successfully from the table %s' % (row_id, table_id)
        return response

    def update_hub_db(self, table_id, row_id, params):
        """
        Method calls to update a specific row in the HubDB table
        :param table_id: HubDB table ID
        :param row_id: Row ID
        :param params: dict of values to update
        """
        url = "%s/cms/v3/hubdb/tables/%s/rows/%s/draft" % (self._url, table_id, row_id)
        response = requests.patch(url, data=json.dumps(params), headers=self._headers)

        if response.status_code in [200, 201]:
            data = response.json()
            return 'The data has been updated successfully \n %s' % (data,)
        else:
            self.logger.info("Failed to Update row: {} on table: {}. Status code: {}, Response: {}".format(
                row_id,
                table_id,
                response.status_code,
                response.content
            ))
        return True

    def publish_hub_db(self, table_id):
        """
        Method calls to publish hubdb data after update/create
        :param table_id: The Id of table to publish
        :return: Hubdb table data published
        """
        url = "%s/cms/v3/hubdb/tables/%s/draft/publish" % (self._url, table_id)
        response = requests.post(url, data=json.dumps({}), headers=self._headers)
        if response.status_code in [200, 201]:
            self.logger.info("Draft table {} published successfully.".format(table_id))
        else:
            self.logger.info("Failed to publish draft table. Status code: {}, Response: {}".format(
                response.status_code,
                response.text
            ))
        return True

    def create_hub_db(self, table_id, params):
        """
        Method call to create new row in the HubDB table on Hubspot
        :param table_id: string Id of table pn hubspot
        :param params: Dict of values
        """
        url = "%s/cms/v3/hubdb/tables/%s/rows" % (self._url, table_id)
        response = requests.post(url, data=json.dumps(params), headers=self._headers)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            self.logger.info("Failed to Create product on table: {}. Status code: {}, Response: {}".format(
                table_id,
                response.status_code,
                response.json()
            ))

        return False

    def create_table_hub_db(self, label, name):
        """
        Method calls to create a new HubDB table
        :param label: string table label
        :param name: string table name
        :return:
        """
        params = {
            "name": name,
            "label": label,
        }
        url = "%s/hubdb/api/v2/tables" % (self._url)
        response = requests.post(url, data=json.dumps(params), headers=self._headers)
        if response.status_code in [200, 201]:
            return response.json()
        return False

    def update_table_hub_db(self, table_id, label, name, columns):
        """
        Method calls to add new columns to the HubDB table
        :param table_id: string id of table
        :param label: string table label
        :param name: string the table name
        :param columns: list of columns names
        :return:
        """
        params = {
            "name": name,
            "label": label,
        }
        if columns:
            params['columns'] = columns
        url = "%s/hubdb/api/v2/tables/%s" % (self._url, table_id)
        response = requests.put(url, data=json.dumps(params), headers=self._headers)
        if response.status_code in [200, 201]:
            return response.json()
        return False

    def delete_all_draft_rows(self, table_id):
        """
        Delete all rows a HubDB table.
        :param table_id: string ID of the HubDB table.
        """
        row_ids = self.fetch_all_draft_rows(table_id)
        for row_id in row_ids:
            self.delete_hub_db(table_id, row_id)
        return True

    def search_hub_db(self, table_id, key, value):
        """
        :param table_id: HubDB table ID
        :param key: Search Key
        :param value: Search Value
        :return:
        """
        url = "%s/cms/v3/hubdb/tables/%s/rows?%s=%s" % (self._url, table_id, key, value)
        response = requests.get(url, headers=self._headers)
        if response.status_code in [200, 201]:
            data = response.json()
            return data
        else:
            self.logger.info("Failed to get row: {}={} on table: {}. Status code: {}, Response: {}".format(
                key,
                value,
                table_id,
                response.status_code,
                response.content
            ))
        return False
