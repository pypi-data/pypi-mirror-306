import json
import logging
from typing import Dict, Any, List
import asyncio 
from e2b import Sandbox

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SetVariableNode:
    def __init__(self):
        self.sandbox = None
        self.execution_manager = None
        self.variables: Dict[str, Any] = {}

    def set_execution_manager(self, execution_manager):
        self.execution_manager = execution_manager

    async def initialize(self):
        logger.info("Initializing SetVariableNode")
        self.sandbox = Sandbox()
        # No need to start the sandbox as it's started automatically

    async def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Executing SetVariableNode with data: {json.dumps(node_data, indent=2)}")
        operation = node_data.get('operation', 'set')
        variable_name = node_data.get('variable_name')
        variable_value = node_data.get('variable_value')

        if not variable_name:
            return {"status": "error", "message": "Missing variable_name"}

        try:
            if operation == 'set':
                result = await self.set_variable(variable_name, variable_value)
            elif operation == 'get':
                result = await self.get_variable(variable_name)
            elif operation == 'increment':
                result = await self.increment_variable(variable_name, variable_value)
            elif operation == 'decrement':
                result = await self.decrement_variable(variable_name, variable_value)
            elif operation == 'append':
                result = await self.append_to_variable(variable_name, variable_value)
            elif operation == 'delete':
                result = await self.delete_variable(variable_name)
            else:
                return {"status": "error", "message": f"Unknown operation: {operation}"}

            return {"status": "success", "result": result}
        except Exception as e:
            error_msg = f"Error in SetVariableNode: {str(e)}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}

    async def set_variable(self, name: str, value: Any) -> Dict[str, Any]:
        resolved_value = await self.resolve_value(value)
        self.variables[name] = resolved_value
        return {"variable_name": name, "value": resolved_value}

    async def get_variable(self, name: str) -> Dict[str, Any]:
        value = self.variables.get(name, None)
        return {"variable_name": name, "value": value}

    async def increment_variable(self, name: str, increment_by: Any = 1) -> Dict[str, Any]:
        current_value = self.variables.get(name, 0)
        if not isinstance(current_value, (int, float)):
            raise ValueError(f"Variable '{name}' is not a number")
        increment_by = await self.resolve_value(increment_by)
        new_value = current_value + increment_by
        self.variables[name] = new_value
        return {"variable_name": name, "old_value": current_value, "new_value": new_value}

    async def decrement_variable(self, name: str, decrement_by: Any = 1) -> Dict[str, Any]:
        current_value = self.variables.get(name, 0)
        if not isinstance(current_value, (int, float)):
            raise ValueError(f"Variable '{name}' is not a number")
        decrement_by = await self.resolve_value(decrement_by)
        new_value = current_value - decrement_by
        self.variables[name] = new_value
        return {"variable_name": name, "old_value": current_value, "new_value": new_value}

    async def append_to_variable(self, name: str, value: Any) -> Dict[str, Any]:
        current_value = self.variables.get(name, [])
        if not isinstance(current_value, list):
            raise ValueError(f"Variable '{name}' is not a list")
        resolved_value = await self.resolve_value(value)
        current_value.append(resolved_value)
        self.variables[name] = current_value
        return {"variable_name": name, "appended_value": resolved_value, "new_list": current_value}

    async def delete_variable(self, name: str) -> Dict[str, Any]:
        deleted_value = self.variables.pop(name, None)
        return {"variable_name": name, "deleted_value": deleted_value}

    async def resolve_value(self, value: Any) -> Any:
        if isinstance(value, str) and value.startswith('{{') and value.endswith('}}'):
            # This is a reference to another variable or node output
            reference = value[2:-2].strip()
            if '.' in reference:
                node_name, output_key = reference.split('.', 1)
                return self.execution_manager.get_node_output(node_name, output_key)
            else:
                return self.variables.get(reference)
        return value

    async def close(self):
        # The sandbox doesn't need to be closed explicitly
        self.sandbox = None
        logger.info("SetVariableNode shutdown completed")

SetVariableNodeNode = SetVariableNode

# Example usage
async def run_example():
    set_variable_node = SetVariableNode()
    await set_variable_node.initialize()

    try:
        # Set a variable
        set_result = await set_variable_node.execute({
            "operation": "set",
            "variable_name": "my_var",
            "variable_value": 42
        })
        print("Set variable result:", json.dumps(set_result, indent=2))

        # Get the variable
        get_result = await set_variable_node.execute({
            "operation": "get",
            "variable_name": "my_var"
        })
        print("Get variable result:", json.dumps(get_result, indent=2))

        # Increment the variable
        increment_result = await set_variable_node.execute({
            "operation": "increment",
            "variable_name": "my_var",
            "variable_value": 8
        })
        print("Increment variable result:", json.dumps(increment_result, indent=2))

        # Append to a list variable
        append_result = await set_variable_node.execute({
            "operation": "append",
            "variable_name": "my_list",
            "variable_value": "new item"
        })
        print("Append to variable result:", json.dumps(append_result, indent=2))

        # Delete a variable
        delete_result = await set_variable_node.execute({
            "operation": "delete",
            "variable_name": "my_var"
        })
        print("Delete variable result:", json.dumps(delete_result, indent=2))

    except Exception as e:
        print(f"An error occurred during the example run: {str(e)}")
    finally:
        await set_variable_node.close()

if __name__ == "__main__":
    asyncio.run(run_example())