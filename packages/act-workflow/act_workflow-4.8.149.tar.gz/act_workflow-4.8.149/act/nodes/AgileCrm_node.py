import os
import json
import logging
from typing import Dict, Any, Optional
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

AGILECRM_API_BASE_URL = "https://{subdomain}.agilecrm.com/dev/api"

class AgileCrmNode:
    def __init__(self):
        logger.info("Initializing AgileCrmNode")
        self.session = requests.Session()
        retry = Retry(total=3, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
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
        logger.info("Starting execution of AgileCrmNode")
        logger.debug(f"Received node_data: {json.dumps(node_data, indent=2)}")

        form_data = node_data.get('formData', {})
        access_token = form_data.get('accessToken') or os.getenv('AGILECRM_ACCESS_TOKEN')

        if not access_token:
            logger.error("Missing Access Token")
            return {
                "status": "error",
                "message": "Missing Access Token. Please provide it in the formData or set AGILECRM_ACCESS_TOKEN environment variable."
            }

        try:
            resolved_form_data = self.resolve_path_placeholders(form_data, node_data)
            logger.info(f"Resolved form_data: {json.dumps(resolved_form_data, indent=2)}")

            resource = resolved_form_data['resource']
            operation = resolved_form_data['operation']
            subdomain = resolved_form_data['subdomain']

            if resource == 'contact':
                result = self.handle_contact(operation, resolved_form_data, access_token, subdomain)
            elif resource == 'company':
                result = self.handle_company(operation, resolved_form_data, access_token, subdomain)
            elif resource == 'deal':
                result = self.handle_deal(operation, resolved_form_data, access_token, subdomain)
            else:
                logger.error(f"Invalid resource: {resource}")
                return {"status": "error", "message": f"Invalid resource: {resource}"}

            logger.info("Operation completed successfully")
            return {
                "status": "success",
                "result": result
            }
        except Exception as e:
            error_msg = f"Error during execution: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {"status": "error", "message": error_msg}

    def handle_contact(self, operation: str, form_data: Dict[str, Any], access_token: str, subdomain: str) -> Dict[str, Any]:
        if operation == 'get':
            contact_id = form_data.get('contactId')
            return self.api_request(f'contacts/{contact_id}', method='GET', access_token=access_token, subdomain=subdomain)
        elif operation == 'delete':
            contact_id = form_data.get('contactId')
            return self.api_request(f'contacts/{contact_id}', method='DELETE', access_token=access_token, subdomain=subdomain)
        elif operation == 'getAll':
            return self.api_request('contacts', method='GET', params=form_data, access_token=access_token, subdomain=subdomain)
        elif operation == 'create':
            return self.api_request('contacts', method='POST', json=form_data, access_token=access_token, subdomain=subdomain)
        elif operation == 'update':
            contact_id = form_data.get('contactId')
            return self.api_request(f'contacts/{contact_id}', method='PUT', json=form_data, access_token=access_token, subdomain=subdomain)
        else:
            raise ValueError(f"Invalid contact operation: {operation}")

    def handle_company(self, operation: str, form_data: Dict[str, Any], access_token: str, subdomain: str) -> Dict[str, Any]:
        if operation == 'get':
            company_id = form_data.get('companyId')
            return self.api_request(f'companies/{company_id}', method='GET', access_token=access_token, subdomain=subdomain)
        elif operation == 'delete':
            company_id = form_data.get('companyId')
            return self.api_request(f'companies/{company_id}', method='DELETE', access_token=access_token, subdomain=subdomain)
        elif operation == 'getAll':
            return self.api_request('companies', method='GET', params=form_data, access_token=access_token, subdomain=subdomain)
        elif operation == 'create':
            return self.api_request('companies', method='POST', json=form_data, access_token=access_token, subdomain=subdomain)
        elif operation == 'update':
            company_id = form_data.get('companyId')
            return self.api_request(f'companies/{company_id}', method='PUT', json=form_data, access_token=access_token, subdomain=subdomain)
        else:
            raise ValueError(f"Invalid company operation: {operation}")

    def handle_deal(self, operation: str, form_data: Dict[str, Any], access_token: str, subdomain: str) -> Dict[str, Any]:
        if operation == 'get':
            deal_id = form_data.get('dealId')
            return self.api_request(f'deals/{deal_id}', method='GET', access_token=access_token, subdomain=subdomain)
        elif operation == 'delete':
            deal_id = form_data.get('dealId')
            return self.api_request(f'deals/{deal_id}', method='DELETE', access_token=access_token, subdomain=subdomain)
        elif operation == 'getAll':
            return self.api_request('deals', method='GET', params=form_data, access_token=access_token, subdomain=subdomain)
        elif operation == 'create':
            return self.api_request('deals', method='POST', json=form_data, access_token=access_token, subdomain=subdomain)
        elif operation == 'update':
            deal_id = form_data.get('dealId')
            return self.api_request(f'deals/{deal_id}', method='PUT', json=form_data, access_token=access_token, subdomain=subdomain)
        else:
            raise ValueError(f"Invalid deal operation: {operation}")

    def api_request(self, endpoint: str, method: str = 'GET', params: Dict[str, Any] = None, json: Dict[str, Any] = None, access_token: str = None, subdomain: str = None) -> Dict[str, Any]:
        url = f"{AGILECRM_API_BASE_URL.format(subdomain=subdomain)}/{endpoint}"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        try:
            response = self.session.request(method, url, headers=headers, params=params, json=json)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Agile CRM API request failed: {str(e)}")
            raise Exception(f"Agile CRM API request failed: {str(e)}")

AgileCrmNodeNode = AgileCrmNode

if __name__ == "__main__":
    test_data = {
        "formData": {
            "accessToken": "your_access_token",
            "subdomain": "your_subdomain",
            "resource": "contact",
            "operation": "get",
            "contactId": "123456789"
        },
        "results": {}
    }

    node = AgileCrmNode()
    result = node.execute(test_data)
    print(json.dumps(result, indent=2))