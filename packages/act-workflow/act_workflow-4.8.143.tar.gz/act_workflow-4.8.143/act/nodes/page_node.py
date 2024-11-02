import logging
from typing import Dict, Any
import json

logger = logging.getLogger(__name__)

class PageNode:
    def __init__(self):
        self.e2b_sandbox_node = None
        self.page_name = None
        self.page_path = None
        self.api_path = None

    def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Starting execution of PageNode")
        logger.info(f"Received page_name: {node_data.get('page_name')}")
        logger.info(f"Received operation: {node_data.get('operation')}")

        try:
            self.e2b_sandbox_node = node_data.get('e2b_sandbox_node')
            if not self.e2b_sandbox_node:
                raise ValueError("Missing E2BSandboxNode instance")

            self.page_name = node_data.get('page_name')
            if self.page_name is None:
                raise ValueError("Missing page name")

            self.page_path = f"{self.e2b_sandbox_node.app_dir}/pages/{self.page_name or 'index'}.tsx"
            self.api_path = f"{self.e2b_sandbox_node.app_dir}/pages/api/{self.page_name or 'index'}.ts"

            operation = node_data.get('operation', 'create')
            content = node_data.get('content', '')
            variable_mappings = node_data.get('variable_mappings', {})

            if operation == 'create':
                self.create(content, variable_mappings)
            elif operation == 'update':
                self.update(content, variable_mappings)
            elif operation == 'delete':
                self.delete()
            else:
                raise ValueError(f"Invalid operation: {operation}")

            result = {
                "status": "success",
                "result": {
                    "page_name": self.page_name,
                    "operation": operation,
                    "page_url": f"{self.e2b_sandbox_node.public_url}/{self.page_name}"
                }
            }
            logger.info(f"Execution completed successfully. Result: {json.dumps(result, indent=2)}")
            return result

        except Exception as e:
            error_msg = f"Unexpected error during execution: {str(e)}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}

    def create(self, content: str, variable_mappings: Dict[str, str]):
        logger.info(f"Creating page '{self.page_name or 'index'}'")
        page_content = self.generate_page_content(content, variable_mappings)
        api_content = self.generate_api_content(variable_mappings)
        self.e2b_sandbox_node.write_file(self.page_path, page_content)
        self.e2b_sandbox_node.write_file(self.api_path, api_content)

    def update(self, content: str, variable_mappings: Dict[str, str]):
        logger.info(f"Updating page '{self.page_name or 'index'}'")
        page_content = self.generate_page_content(content, variable_mappings)
        api_content = self.generate_api_content(variable_mappings)
        self.e2b_sandbox_node.write_file(self.page_path, page_content)
        self.e2b_sandbox_node.write_file(self.api_path, api_content)

    def delete(self):
        logger.info(f"Deleting page '{self.page_name or 'index'}'")
        self.e2b_sandbox_node.sandbox.commands.run(f"rm -f {self.page_path}")
        self.e2b_sandbox_node.sandbox.commands.run(f"rm -f {self.api_path}")

    def generate_page_content(self, content: str, variable_mappings: Dict[str, str]) -> str:
        return f"""
import React from 'react';
import useSWR from 'swr'

const fetcher = (url) => fetch(url).then((res) => res.json());

export default function {self.page_name.capitalize() if self.page_name else 'Home'}Page() {{
    const {{ data, error }} = useSWR('/api/{self.page_name or "index"}', fetcher)

    if (error) return <div>Failed to load</div>
    if (!data) return <div>Loading...</div>

    return (
        <div>
            {content}
            <pre>{{JSON.stringify(data, null, 2)}}</pre>
        </div>
    )
}}
"""

    def generate_api_content(self, variable_mappings: Dict[str, str]) -> str:
        return f"""
import {{ NextApiRequest, NextApiResponse }} from 'next'

export default function handler(req: NextApiRequest, res: NextApiResponse) {{
    const variableMappings = {json.dumps(variable_mappings)};
    const resolvedVariables = {{}};

    for (const [key, value] of Object.entries(variableMappings)) {{
        resolvedVariables[key] = `Resolved value for ${{value}}`;
    }}

    res.status(200).json(resolvedVariables);
}}
"""

PageNodeNode = PageNode

if __name__ == "__main__":
    # This block is for testing the PageNode class independently
    from act_workflow.act.nodes.e2bsandboxnode_node import E2BSandboxNode
    import time

    # Initialize E2BSandboxNode
    e2b_sandbox = E2BSandboxNode()
    e2b_sandbox_result = e2b_sandbox.execute({})

    if e2b_sandbox_result['status'] == 'success':
        # Test PageNode
        test_data = {
            "e2b_sandbox_node": e2b_sandbox,
            "page_name": "test_page",
            "operation": "create",
            "content": "<h1>Test Page</h1><p>This is a test page.</p>",
            "variable_mappings": {"testVar": "testValue"}
        }

        page_node = PageNode()
        result = page_node.execute(test_data)
        print(json.dumps(result, indent=2))

        # Keep the server running for a while
        print("The app will run for 5 minutes. You can open it in your browser.")
        time.sleep(300)

        e2b_sandbox.close()
    else:
        print("Failed to initialize E2BSandboxNode")