import json
import logging
from typing import Dict, Any, List
import asyncio 
from e2b import Sandbox

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SequenceNode:
    def __init__(self):
        self.sandbox = None
        self.execution_manager = None

    def set_execution_manager(self, execution_manager):
        self.execution_manager = execution_manager

    async def initialize(self):
        logger.info("Initializing SequenceNode")
        self.sandbox = Sandbox()
        # No need to start the sandbox as it's started automatically

    async def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Executing SequenceNode with data: {json.dumps(node_data, indent=2)}")
        sequence = node_data.get('sequence', [])
        initial_input = node_data.get('input', {})

        if not sequence:
            return {"status": "error", "message": "No sequence provided"}

        try:
            results = []
            current_input = initial_input

            for node_name in sequence:
                logger.info(f"Executing node: {node_name}")
                node_result = await self.execution_manager.execute_node(node_name, current_input)
                
                if node_result.get('status') == 'error':
                    logger.error(f"Error in node {node_name}: {node_result.get('message')}")
                    return {
                        "status": "error",
                        "message": f"Error in node {node_name}: {node_result.get('message')}",
                        "partial_results": results
                    }
                
                results.append({
                    "node": node_name,
                    "result": node_result
                })
                
                # Use the output of this node as input for the next node
                current_input = node_result.get('result', {})

            return {
                "status": "success",
                "message": "Sequence executed successfully",
                "results": results
            }

        except Exception as e:
            error_msg = f"Error in SequenceNode: {str(e)}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg, "partial_results": results}

    async def close(self):
        # The sandbox doesn't need to be closed explicitly
        self.sandbox = None
        logger.info("SequenceNode shutdown completed")

SequenceNodeNode = SequenceNode

# Example usage
class MockExecutionManager:
    async def execute_node(self, node_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # This is a mock implementation. In a real scenario, this would execute actual nodes.
        logger.info(f"Mock executing node: {node_name} with input: {json.dumps(input_data, indent=2)}")
        return {
            "status": "success",
            "result": {
                "output": f"Result from {node_name}",
                "input_received": input_data
            }
        }

async def run_example():
    sequence_node = SequenceNode()
    sequence_node.set_execution_manager(MockExecutionManager())
    await sequence_node.initialize()

    try:
        # Example sequence execution
        sequence_result = await sequence_node.execute({
            "sequence": ["NodeA", "NodeB", "NodeC"],
            "input": {"initial_data": "Start of sequence"}
        })
        print("Sequence execution result:", json.dumps(sequence_result, indent=2))

    except Exception as e:
        print(f"An error occurred during the example run: {str(e)}")
    finally:
        await sequence_node.close()

if __name__ == "__main__":
    asyncio.run(run_example())