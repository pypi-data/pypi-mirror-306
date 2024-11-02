import os
import json
import logging
from typing import Dict, Any, Union, List
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

ADALO_API_BASE_URL = "https://api.adalo.com/v0/apps"

class AdaloNode:
    def __init__(self):
        logger.info("Initializing AdaloNode")
        self.session = requests.Session()
        retry = Retry(total=3, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        self.session.mount('http://', HTTPAdapter(max_retries=retry))
        self.session.mount('https://', HTTPAdapter(max_retries=retry))
        self.app_id = os.environ.get('ADALO_APP_ID')

    def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Starting execution of AdaloNode")
        logger.debug(f"Received node_data: {json.dumps(node_data, indent=2)}")

        form_data = node_data.get('formData', {})
        access_token = form_data.get('accessToken') or os.getenv('ADALO_API_TOKEN')
        resource = form_data.get('resource', '')
        operation = form_data.get('operation', '')
        collection_id = form_data.get('collectionId', '')

        if not access_token:
            logger.error("Missing Access Token")
            return {
                "status": "error",
                "message": "Missing Access Token. Please provide it in the formData or set ADALO_API_TOKEN environment variable."
            }

        resolved_form_data = self.resolve_path_placeholders(form_data, node_data)

        try:
            if resource == 'Collection':
                if operation == 'Create':
                    result = self.create_collection_record(collection_id, resolved_form_data, access_token)
                elif operation == 'Delete':
                    result = self.delete_collection_record(collection_id, resolved_form_data, access_token)
                elif operation == 'Get':
                    result = self.get_collection_record(collection_id, resolved_form_data, access_token)
                elif operation == 'Get Many':
                    result = self.get_many_collection_records(collection_id, resolved_form_data, access_token)
                elif operation == 'Update':
                    result = self.update_collection_record(collection_id, resolved_form_data, access_token)
                else:
                    raise ValueError(f"Invalid operation: {operation}")
            else:
                raise ValueError(f"Invalid resource: {resource}")

            logger.info("Operation completed successfully")
            return {
                "status": "success",
                "result": result
            }
        except Exception as e:
            logger.error(f"Error in executing operation: {str(e)}")
            return {"status": "error", "message": str(e)}

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

    def create_collection_record(self, collection_id: str, form_data: Dict[str, Any], access_token: str) -> Dict[str, Any]:
        url = f"{ADALO_API_BASE_URL}/{self.app_id}/collections/{collection_id}"
        data = form_data.get('fields', {})
        return self.api_request('POST', url, access_token, json=data)

    def delete_collection_record(self, collection_id: str, form_data: Dict[str, Any], access_token: str) -> Dict[str, Any]:
        row_id = form_data.get('rowId')
        url = f"{ADALO_API_BASE_URL}/{self.app_id}/collections/{collection_id}/{row_id}"
        return self.api_request('DELETE', url, access_token)

    def get_collection_record(self, collection_id: str, form_data: Dict[str, Any], access_token: str) -> Dict[str, Any]:
        row_id = form_data.get('rowId')
        url = f"{ADALO_API_BASE_URL}/{self.app_id}/collections/{collection_id}/{row_id}"
        return self.api_request('GET', url, access_token)

    def get_many_collection_records(self, collection_id: str, form_data: Dict[str, Any], access_token: str) -> Dict[str, Any]:
        url = f"{ADALO_API_BASE_URL}/{self.app_id}/collections/{collection_id}"
        params = {
            'limit': form_data.get('limit', 100),
            'offset': form_data.get('offset', 0)
        }
        return self.api_request('GET', url, access_token, params=params)

    def update_collection_record(self, collection_id: str, form_data: Dict[str, Any], access_token: str) -> Dict[str, Any]:
        row_id = form_data.get('rowId')
        url = f"{ADALO_API_BASE_URL}/{self.app_id}/collections/{collection_id}/{row_id}"
        data = form_data.get('fields', {})
        return self.api_request('PUT', url, access_token, json=data)

    def api_request(self, method: str, url: str, access_token: str, params: Dict[str, Any] = None, json: Dict[str, Any] = None) -> Dict[str, Any]:
        headers = {
            'Authorization': f"Bearer {access_token}",
            'Content-Type': 'application/json'
        }
        try:
            if method == 'GET':
                response = self.session.get(url, headers=headers, params=params)
            elif method == 'POST':
                response = self.session.post(url, headers=headers, json=json)
            elif method == 'PUT':
                response = self.session.put(url, headers=headers, json=json)
            elif method == 'DELETE':
                response = self.session.delete(url, headers=headers)
            else:
                raise ValueError(f"Invalid HTTP method: {method}")

            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            raise Exception(f"Adalo API request failed: {str(e)}")

# Alias the class name for compatibility, if needed
AdaloNodeNode = AdaloNode

if __name__ == "__main__":
    test_data = {
        "formData": {
            "accessToken": "your_access_token",
            "resource": "Collection",
            "operation": "Get",
            "collectionId": "123456789",
            "rowId": "987654321"
        },
        "results": {}
    }

    node = AdaloNode()
    result = node.execute(test_data)
    print(json.dumps(result, indent=2))