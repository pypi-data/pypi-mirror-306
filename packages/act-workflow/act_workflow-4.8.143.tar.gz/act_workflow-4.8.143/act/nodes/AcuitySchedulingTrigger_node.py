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

ACUITY_API_BASE_URL = "https://acuityscheduling.com/api/v1"

class AcuitySchedulingTriggerNode:
    def __init__(self):
        logger.info("Initializing AcuitySchedulingTriggerNode")
        self.session = requests.Session()
        retry = Retry(total=3, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        self.session.mount('http://', HTTPAdapter(max_retries=retry))
        self.session.mount('https://', HTTPAdapter(max_retries=retry))

    def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Starting execution of AcuitySchedulingTriggerNode")
        logger.debug(f"Received node_data: {json.dumps(node_data, indent=2)}")

        form_data = node_data.get('formData', {})
        access_token = form_data.get('accessToken') or os.getenv('ACUITY_ACCESS_TOKEN')
        event = form_data.get('event', '')
        resolve_data = form_data.get('resolveData', True)

        if not access_token:
            logger.error("Missing Access Token")
            return {"status": "error", "message": "Missing Access Token. Please provide it in formData or set ACUITY_ACCESS_TOKEN environment variable."}

        try:
            if event in ['appointment.scheduled', 'appointment.canceled', 'appointment.changed', 'appointment.rescheduled', 'order.completed']:
                result = self.handle_webhook_event(event, resolve_data, access_token)
            else:
                logger.error(f"Invalid event: {event}")
                raise ValueError(f"Invalid event: {event}")

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

    def handle_webhook_event(self, event: str, resolve_data: bool, access_token: str) -> Dict[str, Any]:
        if resolve_data:
            return self.api_request('GET', '/appointments', {'event': event}, access_token)
        else:
            return {"event": event, "message": "Raw webhook data received"}

    def api_request(self, method: str, endpoint: str, params: Dict[str, Any], access_token: str) -> Dict[str, Any]:
        url = f"{ACUITY_API_BASE_URL}{endpoint}"
        headers = {"Authorization": f"Bearer {access_token}"}

        try:
            if method == 'GET':
                response = self.session.get(url, headers=headers, params=params)
            elif method == 'POST':
                response = self.session.post(url, headers=headers, json=params)
            elif method == 'DELETE':
                response = self.session.delete(url, headers=headers, json=params)
            else:
                raise ValueError(f"Invalid HTTP method: {method}")

            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            raise Exception(f"Acuity API request failed: {str(e)}")

# Alias the class name for compatibility
AcuitySchedulingTriggerNodeNode = AcuitySchedulingTriggerNode

if __name__ == "__main__":
    test_data = {
        "formData": {
            "accessToken": "your_access_token",
            "event": "appointment.scheduled",
            "resolveData": True
        },
        "results": {}
    }

    node = AcuitySchedulingTriggerNode()
    result = node.execute(test_data)
    print(json.dumps(result, indent=2))