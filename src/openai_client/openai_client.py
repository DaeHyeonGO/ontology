from typing import Callable, Type
import dotenv
from pydantic import BaseModel
from openai import OpenAI
from mcp import Tool
from openai.types.chat.parsed_chat_completion import ParsedFunctionToolCall
from src.openai_client.tool_call import OpenAITool, OpenAIToolCall
dotenv.load_dotenv()

class TextContentOpenAI(BaseModel):
    role: str
    content: str

class OpenAIClient:
    def __init__(self, system_prompt: str, model: str = "gpt-4o-mini-2024-07-18"):
        import os
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.system_prompt = system_prompt

    def _prompt_message_to_dict(self, prompt_message: TextContentOpenAI) -> dict:
        return {    
            "role": prompt_message.role,
            "content": prompt_message.content
        }
    
    def _prompt_messages_to_dict(self, prompt_messages: list[TextContentOpenAI]) -> list[dict]: 
        return [self._prompt_message_to_dict(prompt_message) for prompt_message in prompt_messages]

    def create_completion(self, messages: list[TextContentOpenAI]) -> str:
        response = self.client.chat.completions.create(
            model=self.model, 
            messages= [{"role": "system", "content": self.system_prompt}] + self._prompt_messages_to_dict(messages)
        )
        return response.choices[0].message.content

    def create_completion_structured_output(
            self, 
            messages: list[TextContentOpenAI], 
            response_format: Type[BaseModel]
        ) -> BaseModel:
        completion = self.client.beta.chat.completions.parse(
            model=self.model,
            messages= [{"role": "system", "content": self.system_prompt}] + self._prompt_messages_to_dict(messages),
            response_format=response_format,
        )
        return completion.choices[0].message.parsed
        
    def create_completion_tool_calls(
                self, 
                messages: list[TextContentOpenAI], 
                tools : list[OpenAITool],
                tool_choice: str = "auto"
            ) -> ParsedFunctionToolCall:
            completion = self.client.beta.chat.completions.parse(
                model=self.model,
                messages= [{"role": "system", "content": self.system_prompt}] + self._prompt_messages_to_dict(messages),
                tools=[tool.get_tool() for tool in tools],
                tool_choice=tool_choice
            )
            
            return [OpenAIToolCall(tool_call, tools) for tool_call in completion.choices[0].message.tool_calls]

if __name__ == "__main__":
    # run srcipt : PYTHONPATH=. python openai_client/openai_client.py
    class Step(BaseModel):
        explanation: str
        output: str

    class MathReasoning(BaseModel):
        steps: list[Step]
        final_answer: str

    client = OpenAIClient(system_prompt="You are a helpful math tutor. Guide the user through the solution step by step.")
    result = client.create_completion_structured_output(
        messages=[
            TextContentOpenAI(role="user", content="how can I solve 8x + 7 = -23")
        ], response_format=MathReasoning)
    print(result)

    def add_one(x: str) -> int:
        return int(x) + 1
    def subtract_one(x: str) -> int:
        return int(x) - 1
    tool_add_one = OpenAITool(
        name="add_one",
        description="A tool to add one to a number",
        function=add_one # type: (str) -> int
    )
    tool_subtract_one = OpenAITool(
        name="subtract_one", 
        description="A tool to subtract one from a number",
        function=subtract_one # type: (str) -> int
    )
    
    client = OpenAIClient(
        system_prompt="You are a helpful math tutor. Guide the user through the solution step by step.",
        model="gpt-4o-mini-2024-07-18"
    )
    result = client.create_completion_tool_calls(
        messages=[
            TextContentOpenAI(role="user", content="add one to 10")
        ],
        tools=[tool_add_one, tool_subtract_one], 
        tool_choice="required"
    )
    print(result[0].dump())
    print(result[0].call())

