import os
import json
import logging
from typing import Dict, Any, Union
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

AIRTABLE_API_BASE_URL = "https://api.airtable.com/v0"

class AirtableNode:
    def __init__(self):
        logger.info("Initializing AirtableNode")
        self.session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=0.1,
            status_forcelist=[500, 502, 503, 504]
        )
        self.session.mount('http://', HTTPAdapter(max_retries=retry))
        self.session.mount('https://', HTTPAdapter(max_retries=retry))

    def resolve_path_placeholders(self, data: Any, node_data: Dict[str, Any]) -> Any:
        if isinstance(data, str):
            pattern = re.compile(r"\{\{(.*?)\}\}")
            matches = pattern.findall(data)

            for match in matches:
                parts = match.split('.')
                node_id = parts[0]
                path = '.'.join(parts[1:])
                value = self.fetch_value(node_id, path, node_data)
                if value is not None:
                    data = data.replace(f"{{{{{match}}}}}", str(value))

            return data
        elif isinstance(data, dict):
            return {k: self.resolve_path_placeholders(v, node_data) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.resolve_path_placeholders(item, node_data) for item in data]
        else:
            return data

    def fetch_value(self, node_id: str, path: str, node_data: Dict[str, Any]) -> Any:
        try:
            node_result = node_data.get('results', {}).get(node_id, {})
            for part in path.split('.'):
                node_result = node_result.get(part, None)
                if node_result is None:
                    break
            return node_result
        except Exception as e:
            logger.error(f"Failed to fetch value for {node_id}.{path}: {str(e)}")
            return None

    def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Starting execution of AirtableNode")
        logger.info(f"Received node_data: {json.dumps(node_data, indent=2)}")

        form_data = node_data.get('formData', {})
        access_token = form_data.get('accessToken') or os.getenv('AIRTABLE_ACCESS_TOKEN')
        base_id = form_data.get('baseId')
        table_name = form_data.get('tableName')
        operation = form_data.get('operation')

        if not access_token:
            logger.error("Missing Access Token")
            return {
                "status": "error",
                "message": "Missing Access Token. Please provide it in the formData or set AIRTABLE_ACCESS_TOKEN environment variable."
            }

        if not base_id or not table_name:
            logger.error("Missing baseId or tableName")
            return {
                "status": "error",
                "message": "Missing baseId or tableName in formData"
            }

        if not operation:
            logger.error("Missing operation")
            return {"status": "error", "message": "Missing operation in formData"}

        try:
            resolved_form_data = self.resolve_path_placeholders(form_data, node_data)
            logger.info(f"Resolved form_data: {json.dumps(resolved_form_data, indent=2)}")

            if operation == 'read':
                result = self.read_records(base_id, table_name, resolved_form_data, access_token)
            elif operation == 'write':
                result = self.create_record(base_id, table_name, resolved_form_data, access_token)
            elif operation == 'update':
                result = self.update_record(base_id, table_name, resolved_form_data, access_token)
            elif operation == 'delete':
                result = self.delete_record(base_id, table_name, resolved_form_data, access_token)
            else:
                logger.error(f"Invalid operation: {operation}")
                return {"status": "error", "message": f"Invalid operation: {operation}"}

            logger.info("Operation completed successfully")
            return {
                "status": "success",
                "result": result
            }

        except Exception as e:
            error_msg = f"Error during execution: {str(e)}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}

    def read_records(self, base_id: str, table_name: str, form_data: Dict[str, Any], access_token: str) -> Any:
        params = {}
        if 'filterByFormula' in form_data:
            params['filterByFormula'] = form_data['filterByFormula']
        if 'maxRecords' in form_data:
            params['maxRecords'] = form_data['maxRecords']
        if 'view' in form_data:
            params['view'] = form_data['view']

        return self.make_request('GET', f"{base_id}/{table_name}", access_token, params=params)

    def create_record(self, base_id: str, table_name: str, form_data: Dict[str, Any], access_token: str) -> Any:
        data_payload = form_data.get('dataPayload', {})
        return self.make_request('POST', f"{base_id}/{table_name}", access_token, json={"fields": data_payload})

    def update_record(self, base_id: str, table_name: str, form_data: Dict[str, Any], access_token: str) -> Any:
        record_id = form_data.get('recordId')
        if not record_id:
            raise ValueError("Missing recordId for update operation")
        data_payload = form_data.get('dataPayload', {})
        return self.make_request('PATCH', f"{base_id}/{table_name}/{record_id}", access_token, json={"fields": data_payload})

    def delete_record(self, base_id: str, table_name: str, form_data: Dict[str, Any], access_token: str) -> Any:
        record_id = form_data.get('recordId')
        if not record_id:
            raise ValueError("Missing recordId for delete operation")
        return self.make_request('DELETE', f"{base_id}/{table_name}/{record_id}", access_token)

    def make_request(self, method: str, endpoint: str, access_token: str, params: Dict[str, Any] = None, json: Dict[str, Any] = None) -> Dict[str, Any]:
        url = f"{AIRTABLE_API_BASE_URL}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        try:
            if method == 'GET':
                response = self.session.get(url, headers=headers, params=params)
            elif method == 'POST':
                response = self.session.post(url, headers=headers, json=json)
            elif method == 'PATCH':
                response = self.session.patch(url, headers=headers, json=json)
            elif method == 'DELETE':
                response = self.session.delete(url, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Airtable API request failed: {str(e)}")
            raise Exception(f"Airtable API request failed: {str(e)}")

AirtableNodeNode = AirtableNode

if __name__ == "__main__":
    test_data = {
        "formData": {
            "accessToken": "your_access_token",
            "baseId": "appXXXXXXXXXXXXXX",
            "tableName": "Table 1",
            "operation": "read",
            "filterByFormula": "{Status} = 'Open'",
            "maxRecords": 10,
            "view": "Grid view"
        },
        "results": {}
    }

    node = AirtableNode()
    result = node.execute(test_data)
    print(json.dumps(result, indent=2))