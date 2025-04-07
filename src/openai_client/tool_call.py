import json
from typing import Callable, Dict, Any
import inspect
from openai.types.chat.parsed_chat_completion import ParsedFunctionToolCall

class OpenAITool:
    def __init__(self, name: str, description: str, function: Callable):
        self.name = name
        self.description = description
        self.function = function

    def _get_parameters(self) -> Dict[str, Any]:
        sig = inspect.signature(self.function)
        parameters = {}
        required = []
        
        for name, param in sig.parameters.items():
            if param.default == inspect.Parameter.empty:
                required.append(name)
            
            param_type = str(param.annotation).lower()
            if param_type == 'str':
                param_type = 'string'
            elif param_type == 'int':
                param_type = 'integer'
            elif param_type == 'float':
                param_type = 'number'
            elif param_type == 'bool':
                param_type = 'boolean'
            else:
                param_type = 'string'
            
            parameters[name] = {
                'type': param_type,
                'description': f'Parameter {name}'
            }
        
        return {
            'type': 'object',
            'properties': parameters,
            'required': required,
            'additionalProperties': False
        }
    def _get_function(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self._get_parameters(),
            "strict": True
        }

    def get_tool(self) -> dict:
        return {
            "type": "function",
            "function": self._get_function()
        }

class OpenAIToolCall:
    tool_name: str
    arguments: dict
    real_function: Callable
    def __init__(self, tool_call: ParsedFunctionToolCall, tools: list[OpenAITool]):
        self.tool_name = tool_call.function.name
        self.arguments = json.loads(tool_call.function.arguments)
        self.real_function = next((tool.function for tool in tools if tool.name == self.tool_name), None)
    def dump(self) -> dict:
        return {
            "tool_name": self.tool_name,
            "arguments": self.arguments,
            "real_function": self.real_function.__name__
        }
    def call(self) -> Any:
        return self.real_function(**self.arguments)