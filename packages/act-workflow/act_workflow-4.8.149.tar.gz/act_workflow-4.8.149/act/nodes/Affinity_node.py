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

AFFINITY_API_BASE_URL = "https://api.affinity.co/"

class AffinityNode:
    def __init__(self):
        logger.info("Initializing AffinityNode")
        self.session = requests.Session()
        retry = Retry(total=3, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        self.session.mount('http://', HTTPAdapter(max_retries=retry))
        self.session.mount('https://', HTTPAdapter(max_retries=retry))

    def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Starting execution of AffinityNode")
        logger.debug(f"Received node_data: {json.dumps(node_data, indent=2)}")

        form_data = node_data.get('formData', {})
        access_token = form_data.get('accessToken') or os.getenv('AFFINITY_ACCESS_TOKEN')

        if not access_token:
            logger.error("Missing Access Token")
            return {"status": "error", "message": "Missing Access Token. Please provide it in the formData or set AFFINITY_ACCESS_TOKEN environment variable."}

        try:
            resource = form_data.get('resource', '')
            operation = form_data.get('operation', '')

            resolved_form_data = self.resolve_path_placeholders(form_data, node_data)

            if resource == 'list':
                result = self.handle_list(operation, resolved_form_data, access_token)
            elif resource == 'listEntry':
                result = self.handle_list_entry(operation, resolved_form_data, access_token)
            elif resource == 'organization':
                result = self.handle_organization(operation, resolved_form_data, access_token)
            elif resource == 'person':
                result = self.handle_person(operation, resolved_form_data, access_token)
            else:
                logger.error(f"Invalid resource: {resource}")
                raise ValueError(f"Invalid resource: {resource}")

            logger.info("Operation completed successfully")
            return {"status": "success", "result": result}
        except Exception as e:
            error_msg = f"Error during execution: {str(e)}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}

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

    def handle_list(self, operation: str, form_data: Dict[str, Any], access_token: str) -> Dict[str, Any]:
        if operation == 'get':
            list_id = form_data.get('listId')
            return self.api_request(f'lists/{list_id}', 'GET', access_token)
        elif operation == 'getAll':
            limit = form_data.get('limit', 100)
            return self.api_request(f'lists?limit={limit}', 'GET', access_token)
        else:
            raise ValueError(f"Invalid list operation: {operation}")

    def handle_list_entry(self, operation: str, form_data: Dict[str, Any], access_token: str) -> Dict[str, Any]:
        list_id = form_data.get('listId')
        if operation == 'create':
            entity_id = form_data.get('entityId')
            additional_fields = form_data.get('additionalFields', {})
            params = {'entity_id': entity_id}
            self.add_additional_fields(params, additional_fields)
            return self.api_request(f'lists/{list_id}/entries', 'POST', access_token, params)
        elif operation == 'get':
            list_entry_id = form_data.get('listEntryId')
            return self.api_request(f'lists/{list_id}/entries/{list_entry_id}', 'GET', access_token)
        elif operation == 'getAll':
            limit = form_data.get('limit', 100)
            return self.api_request(f'lists/{list_id}/entries?limit={limit}', 'GET', access_token)
        elif operation == 'delete':
            list_entry_id = form_data.get('listEntryId')
            return self.api_request(f'lists/{list_id}/entries/{list_entry_id}', 'DELETE', access_token)
        else:
            raise ValueError(f"Invalid list entry operation: {operation}")

    def handle_organization(self, operation: str, form_data: Dict[str, Any], access_token: str) -> Dict[str, Any]:
        if operation == 'create':
            name = form_data.get('name')
            domain = form_data.get('domain')
            additional_fields = form_data.get('additionalFields', {})
            params = {'name': name, 'domain': domain}
            self.add_additional_fields(params, additional_fields)
            return self.api_request('organizations', 'POST', access_token, params)
        elif operation == 'update':
            organization_id = form_data.get('organizationId')
            update_fields = form_data.get('updateFields', {})
            return self.api_request(f'organizations/{organization_id}', 'PUT', access_token, update_fields)
        elif operation == 'get':
            organization_id = form_data.get('organizationId')
            return self.api_request(f'organizations/{organization_id}', 'GET', access_token)
        elif operation == 'getAll':
            limit = form_data.get('limit', 100)
            return self.api_request(f'organizations?limit={limit}', 'GET', access_token)
        elif operation == 'delete':
            organization_id = form_data.get('organizationId')
            return self.api_request(f'organizations/{organization_id}', 'DELETE', access_token)
        else:
            raise ValueError(f"Invalid organization operation: {operation}")

    def handle_person(self, operation: str, form_data: Dict[str, Any], access_token: str) -> Dict[str, Any]:
        if operation == 'create':
            first_name = form_data.get('firstName')
            last_name = form_data.get('lastName')
            emails = form_data.get('emails')
            additional_fields = form_data.get('additionalFields', {})
            params = {'first_name': first_name, 'last_name': last_name, 'emails': emails}
            self.add_additional_fields(params, additional_fields)
            return self.api_request('persons', 'POST', access_token, params)
        elif operation == 'update':
            person_id = form_data.get('personId')
            update_fields = form_data.get('updateFields', {})
            return self.api_request(f'persons/{person_id}', 'PUT', access_token, update_fields)
        elif operation == 'get':
            person_id = form_data.get('personId')
            return self.api_request(f'persons/{person_id}', 'GET', access_token)
        elif operation == 'getAll':
            limit = form_data.get('limit', 100)
            return self.api_request(f'persons?limit={limit}', 'GET', access_token)
        elif operation == 'delete':
            person_id = form_data.get('personId')
            return self.api_request(f'persons/{person_id}', 'DELETE', access_token)
        else:
            raise ValueError(f"Invalid person operation: {operation}")

    def api_request(self, endpoint: str, method: str, access_token: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        url = f"{AFFINITY_API_BASE_URL}{endpoint}"
        headers = {'Authorization': f"Bearer {access_token}"}
        try:
            if method == 'GET':
                response = self.session.get(url, headers=headers, params=params)
            elif method == 'POST':
                response = self.session.post(url, headers=headers, json=params)
            elif method == 'PUT':
                response = self.session.put(url, headers=headers, json=params)
            elif method == 'DELETE':
                response = self.session.delete(url, headers=headers)
            else:
                raise ValueError(f"Invalid HTTP method: {method}")

            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            raise Exception(f"Affinity API request failed: {str(e)}")

    def add_additional_fields(self, params: Dict[str, Any], additional_fields: Dict[str, Any]) -> None:
        for key, value in additional_fields.items():
            if value is not None:
                params[key] = value

# Alias the class name for compatibility
AffinityNodeNode = AffinityNode

if __name__ == "__main__":
    test_data = {
        "formData": {
            "accessToken": "your_access_token",
            "resource": "list",
            "operation": "getAll",
            "limit": 10
        },
        "results": {}
    }

    node = AffinityNode()
    result = node.execute(test_data)
    print(json.dumps(result, indent=2))