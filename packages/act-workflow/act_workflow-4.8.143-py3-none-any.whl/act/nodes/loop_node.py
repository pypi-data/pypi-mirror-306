import json
import logging
from typing import Dict, Any, List, Union
import asyncio 
from e2b import Sandbox

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LoopNode:
    def __init__(self):
        self.sandbox = None
        self.execution_manager = None

    def set_execution_manager(self, execution_manager):
        self.execution_manager = execution_manager

    async def initialize(self):
        logger.info("Initializing LoopNode")
        self.sandbox = Sandbox()
        # No need to start the sandbox as it's started automatically

    async def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Executing LoopNode with data: {json.dumps(node_data, indent=2)}")
        loop_type = node_data.get('loop_type', 'count')
        nodes = node_data.get('nodes', [])
        initial_input = node_data.get('input', {})

        if not nodes:
            return {"status": "error", "message": "No nodes provided for loop execution"}

        if loop_type == 'count':
            return await self.execute_count_loop(node_data, nodes, initial_input)
        elif loop_type == 'condition':
            return await self.execute_condition_loop(node_data, nodes, initial_input)
        else:
            return {"status": "error", "message": f"Unknown loop type: {loop_type}"}

    async def execute_count_loop(self, node_data: Dict[str, Any], nodes: List[str], initial_input: Dict[str, Any]) -> Dict[str, Any]:
        count = node_data.get('count', 1)
        if count < 1:
            return {"status": "error", "message": "Loop count must be at least 1"}

        results = []
        current_input = initial_input

        for iteration in range(count):
            logger.info(f"Starting iteration {iteration + 1} of {count}")
            iteration_result = await self.execute_nodes(nodes, current_input)
            
            if iteration_result['status'] == 'error':
                return {
                    "status": "error",
                    "message": f"Error in iteration {iteration + 1}: {iteration_result['message']}",
                    "partial_results": results
                }
            
            results.append({
                "iteration": iteration + 1,
                "result": iteration_result['result']
            })
            current_input = iteration_result['result']

        return {
            "status": "success",
            "message": f"Loop completed successfully with {count} iterations",
            "results": results
        }

    async def execute_condition_loop(self, node_data: Dict[str, Any], nodes: List[str], initial_input: Dict[str, Any]) -> Dict[str, Any]:
        condition = node_data.get('condition')
        max_iterations = node_data.get('max_iterations', 100)  # Safeguard against infinite loops

        if not condition:
            return {"status": "error", "message": "No condition provided for conditional loop"}

        results = []
        current_input = initial_input
        iteration = 0

        while iteration < max_iterations:
            iteration += 1
            logger.info(f"Starting iteration {iteration}")

            # Evaluate the condition
            try:
                condition_result = self.evaluate_condition(condition, current_input)
            except Exception as e:
                return {"status": "error", "message": f"Error evaluating condition: {str(e)}"}

            if not condition_result:
                logger.info(f"Loop condition no longer met. Stopping after {iteration - 1} iterations.")
                break

            iteration_result = await self.execute_nodes(nodes, current_input)
            
            if iteration_result['status'] == 'error':
                return {
                    "status": "error",
                    "message": f"Error in iteration {iteration}: {iteration_result['message']}",
                    "partial_results": results
                }
            
            results.append({
                "iteration": iteration,
                "result": iteration_result['result']
            })
            current_input = iteration_result['result']

        if iteration == max_iterations:
            logger.warning(f"Loop reached maximum iterations ({max_iterations})")

        return {
            "status": "success",
            "message": f"Loop completed with {iteration} iterations",
            "results": results
        }

    async def execute_nodes(self, nodes: List[str], input_data: Dict[str, Any]) -> Dict[str, Any]:
        current_input = input_data
        for node_name in nodes:
            logger.info(f"Executing node: {node_name}")
            node_result = await self.execution_manager.execute_node(node_name, current_input)
            
            if node_result.get('status') == 'error':
                return {
                    "status": "error",
                    "message": f"Error in node {node_name}: {node_result.get('message')}"
                }
            
            current_input = node_result.get('result', {})

        return {"status": "success", "result": current_input}

    def evaluate_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        try:
            return eval(condition, {"__builtins__": {}}, context)
        except Exception as e:
            raise ValueError(f"Error evaluating condition '{condition}': {str(e)}")

    async def close(self):
        # The sandbox doesn't need to be closed explicitly
        self.sandbox = None
        logger.info("LoopNode shutdown completed")

LoopNodeNode = LoopNode

# Example usage
class MockExecutionManager:
    async def execute_node(self, node_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # This is a mock implementation. In a real scenario, this would execute actual nodes.
        logger.info(f"Mock executing node: {node_name} with input: {json.dumps(input_data, indent=2)}")
        return {
            "status": "success",
            "result": {
                "output": f"Result from {node_name}",
                "input_received": input_data,
                "counter": input_data.get('counter', 0) + 1  # Increment counter for demonstration
            }
        }

async def run_example():
    loop_node = LoopNode()
    loop_node.set_execution_manager(MockExecutionManager())
    await loop_node.initialize()

    try:
        # Example count-based loop execution
        count_loop_result = await loop_node.execute({
            "loop_type": "count",
            "count": 3,
            "nodes": ["NodeA", "NodeB"],
            "input": {"initial_data": "Start of loop", "counter": 0}
        })
        print("Count-based loop execution result:", json.dumps(count_loop_result, indent=2))

        # Example condition-based loop execution
        condition_loop_result = await loop_node.execute({
            "loop_type": "condition",
            "condition": "counter < 5",
            "nodes": ["NodeC"],
            "input": {"initial_data": "Start of conditional loop", "counter": 0}
        })
        print("Condition-based loop execution result:", json.dumps(condition_loop_result, indent=2))

    except Exception as e:
        print(f"An error occurred during the example run: {str(e)}")
    finally:
        await loop_node.close()

if __name__ == "__main__":
    asyncio.run(run_example())