import re
from .base_llm import BaseLLM
import time

# could be dynamically imported similar to other models
from openai import OpenAI

import openai

from pyopenagi.utils.chat_template import Response
import json


class GPTLLM(BaseLLM):

    def __init__(
        self,
        llm_name: str,
        max_gpu_memory: dict = None,
        eval_device: str = None,
        max_new_tokens: int = 1024,
        log_mode: str = "console",
    ):
        super().__init__(
            llm_name, max_gpu_memory, eval_device, max_new_tokens, log_mode
        )

    def load_llm_and_tokenizer(self) -> None:
        self.model = OpenAI()
        self.tokenizer = None

    def parse_tool_calls(self, tool_calls):
        if tool_calls:
            parsed_tool_calls = []
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                parsed_tool_calls.append(
                    {
                        "name": function_name,
                        "parameters": function_args,
                        "type": tool_call.type,
                        "id": tool_call.id,
                    }
                )
            return parsed_tool_calls
        return None

    def process(self, agent_request, temperature=0.0):
        # ensures the model is the current one
        assert re.search(r"gpt", self.model_name, re.IGNORECASE)

        """ wrapper around openai api """
        agent_request.set_status("executing")
        agent_request.set_start_time(time.time())
        messages = agent_request.query.messages

        try:
            response = self.model.chat.completions.create(
                model=self.model_name,
                messages=messages,
                tools=agent_request.query.tools,
                # tool_choice = "required" if agent_request.query.tools else None,
                max_tokens=self.max_new_tokens,
            )
            response_message = response.choices[0].message.content
            # print(f"[Response] {response}")
            tool_calls = self.parse_tool_calls(response.choices[0].message.tool_calls)
            # print(tool_calls)
            # print(response.choices[0].message)
            response = Response(
                response_message=response_message, tool_calls=tool_calls
            )

        except openai.APIConnectionError as e:

            response = Response(
                response_message=f"Server connection error: {e.__cause__}"
            )

        except openai.RateLimitError as e:

            response = Response(
                response_message=f"OpenAI RATE LIMIT error {e.status_code}: (e.response)"
            )

        except openai.APIStatusError as e:
            response = Response(
                response_message=f"OpenAI STATUS error {e.status_code}: (e.response)"
            )

        except openai.BadRequestError as e:

            response = Response(
                response_message=f"OpenAI BAD REQUEST error {e.status_code}: (e.response)"
            )

        except Exception as e:
            response = Response(response_message=f"An unexpected error occurred: {e}")

        return response
        