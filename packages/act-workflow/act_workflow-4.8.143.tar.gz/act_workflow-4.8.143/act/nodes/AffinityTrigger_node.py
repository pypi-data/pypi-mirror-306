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

AFFINITY_API_BASE_URL = "https://api.affinity.co/"

class AffinityTriggerNode:
    def __init__(self):
        logger.info("Initializing AffinityTriggerNode")
        self.session = requests.Session()
        retry = Retry(total=3, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        self.session.mount('http://', HTTPAdapter(max_retries=retry))
        self.session.mount('https://', HTTPAdapter(max_retries=retry))

    def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Starting execution of AffinityTriggerNode")
        logger.debug(f"Received node_data: {json.dumps(node_data, indent=2)}")

        form_data = node_data.get('formData', {})
        access_token = form_data.get('accessToken') or os.getenv('AFFINITY_API_TOKEN')
        operation = form_data.get('operation', '')

        if not access_token:
            logger.error("Missing Access Token")
            return {"status": "error", "message": "Missing Access Token. Please provide it in the formData or set AFFINITY_API_TOKEN environment variable."}

        resolved_form_data = self.resolve_path_placeholders(form_data, node_data)

        try:
            if operation == 'checkExists':
                result = self.check_webhook_exists(resolved_form_data, access_token)
            elif operation == 'create':
                result = self.create_webhook(resolved_form_data, access_token)
            elif operation == 'delete':
                result = self.delete_webhook(resolved_form_data, access_token)
            else:
                logger.error(f"Invalid operation: {operation}")
                return {"status": "error", "message": f"Invalid operation: {operation}"}

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

    def check_webhook_exists(self, form_data: Dict[str, Any], access_token: str) -> Dict[str, Any]:
        url = f"{AFFINITY_API_BASE_URL}webhooks"
        response = self.api_request('GET', url, access_token)
        webhook_url = form_data.get('webhookUrl')

        for webhook in response.get('webhooks', []):
            if webhook.get('url') == webhook_url:
                return {"exists": True, "webhook_id": webhook.get('id')}
        return {"exists": False}

    def create_webhook(self, form_data: Dict[str, Any], access_token: str) -> Dict[str, Any]:
        webhook_url = form_data.get('webhookUrl')
        events = form_data.get('events', [])

        if ' ' in webhook_url:
            raise ValueError("Webhook URL cannot contain spaces")

        url = f"{AFFINITY_API_BASE_URL}webhooks"
        payload = {
            "url": webhook_url,
            "events": events
        }
        response = self.api_request('POST', url, access_token, json=payload)
        return response

    def delete_webhook(self, form_data: Dict[str, Any], access_token: str) -> Dict[str, Any]:
        webhook_id = form_data.get('webhookId')
        url = f"{AFFINITY_API_BASE_URL}webhooks/{webhook_id}"
        response = self.api_request('DELETE', url, access_token)
        return response

    def api_request(self, method: str, url: str, access_token: str, json: Dict[str, Any] = None) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        try:
            if method == 'GET':
                response = self.session.get(url, headers=headers)
            elif method == 'POST':
                response = self.session.post(url, headers=headers, json=json)
            elif method == 'DELETE':
                response = self.session.delete(url, headers=headers)
            else:
                raise ValueError(f"Invalid HTTP method: {method}")

            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            raise Exception(f"Affinity API request failed: {str(e)}")

# Alias the class name for compatibility
AffinityTriggerNodeNode = AffinityTriggerNode

if __name__ == "__main__":
    test_data = {
        "formData": {
            "accessToken": "your_access_token",
            "operation": "checkExists",
            "webhookUrl": "https://example.com/webhook"
        },
        "results": {}
    }

    node = AffinityTriggerNode()
    result = node.execute(test_data)
    print(json.dumps(result, indent=2))