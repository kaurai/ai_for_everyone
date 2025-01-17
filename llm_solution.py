import json
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

from solution import Solution

load_dotenv()


class LLMSolution(Solution):
    SYSTEM_PROMPT = "You are a helpful assistant"
    SOLUTION = "LLMSolution"
    def __init__(self, llm_client: str = "sambanova", model_name: str = None, solution: str = "LLMSolution"):  
        """
        This Python function initializes an object with a default value for the llm_client parameter.
        
        :param llm_client: The `__init__` method is a constructor in Python classes that is called when
        a new object is created. In this case, the `__init__` method takes in a parameter `llm_client`
        with a default value of "sambanova". When an object of this class is, defaults to sambanova
        :type llm_client: str (optional)
        """
        super().__init__(llm_client=llm_client, model_name=model_name, solution=self.SOLUTION)


    def create_response(self, system_prompt: str ="", user_prompt: str ="", response_format: BaseModel=None):
        """
        The function `create_response` generates a response based on system and user prompts using
        different client APIs and response formats.
        
        :param system_prompt: The `system_prompt` parameter is a string that represents the prompt or
        message that will be shown to the system or AI model before it generates a response. This prompt
        helps provide context or guidance to the model on what kind of response is expected
        :type system_prompt: str
        :param user_prompt: The `user_prompt` parameter in the `create_response` method is a string that
        represents the prompt or input provided by the user in a conversation with the system. This
        prompt is used along with the system prompt to generate a response from the AI model being used
        (e.g., Sambanova,
        :type user_prompt: str
        :param response_format: The `response_format` parameter in the `create_response` method is used
        to specify the format in which the response should be returned. It is an optional parameter and
        can be of type `BaseModel`. Depending on the value of `response_format`, the method will handle
        the response generation differently for different
        :type response_format: BaseModel
        :return: The `create_response` method returns the response generated based on the system prompt,
        user prompt, and response format provided. The response can vary based on the conditions and the
        type of language model client being used (e.g., "sambanova", "openai", "ollama"). The final
        response is the generated text based on the input prompts and the language model's completion or
        chat functionality.
        """
        if system_prompt:
            self.SYSTEM_PROMPT = system_prompt

        if response_format:
            if self.llm_client in ["sambanova", "openai"]:
                response = self.client.beta.chat.completions.parse(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": self.SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt},
                    ],
                    response_format=response_format,
                )
                response = response.choices[0].message.parsed

            elif self.llm_client == "ollama":
                response = self.client.chat(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": self.SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt},
                    ],
                    format=response_format.model_json_schema()
                )
                response = response_format.model_validate_json(response.message.content)
            
            elif self.llm_client == "gemini":
                response = self.client.generate_content(
                    user_prompt, 
                    generation_config=genai.GenerationConfig(
                        response_mime_type="application/json", 
                        response_schema=list[response_format]
                    ),
                )
                response = json.loads(response.candidates[0].content.parts[0].text)

        else:
            if self.llm_client in ["sambanova", "openai"]:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": self.SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt},
                    ]
                )
                response = response.choices[0].message.content
            
            elif self.llm_client == "ollama":
                response = self.client.chat(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": self.SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt},
                    ]
                )
                response = response.message.content
            
            elif self.llm_client == "gemini":
                response = self.client.generate_content(user_prompt)
                response = response.text

        return response
    