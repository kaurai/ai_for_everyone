
from abc import ABC, abstractmethod
import os
from openai import OpenAI
from ollama import Client
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

class Solution(ABC):
    SOLUTION = "Solution"
    def __init__(
        self,
        llm_client: str = "sambanova", 
        model_name: str = None,
        solution: str = "Solution",
    ): 
        """
        This Python function initializes different configurations based on the specified LLM client.
        
        :param llm_client: The `llm_client` parameter in the `__init__` method is used to specify the
        client for which the object is being initialized. The client can be one of the following
        options: "sambanova", "openai", or "ollama", defaults to sambanova
        :type llm_client: str (optional)
        """

        if llm_client == "sambanova":
            api_key = os.getenv('SAMBANOVA_API_KEY')
            base_url = os.getenv('SAMBANOVA_BASE_URL')
            if model_name == "llama_3.1_8b":
                self.model_name = os.getenv('SAMBANOVA_LLAMA_3.1_8B')
            elif model_name == "llama_3.1_70b":
                self.model_name = os.getenv('SAMBANOVA_LLAMA_3.1_70B') 
            elif model_name == "llama_3.1_405b":
                self.model_name = os.getenv('SAMBANOVA_LLAMA_3.1_405B')
            elif model_name == "llama_3.2_1b":
                self.model_name = os.getenv('SAMBANOVA_LLAMA_3.2_1B')
            elif model_name == "llama_3.2_3b":
                self.model_name = os.getenv('SAMBANOVA_LLAMA_3.2_3B')
            elif model_name == "llama_3.3_70b":
                self.model_name = os.getenv('SAMBANOVA_LLAMA_33_70B')
            elif model_name == "llamaguard_3_8b":
                self.model_name = os.getenv('SAMBANOVA_LLAMAGUARD_3_8B')
            elif model_name == "qwen_25_32b":
                self.model_name = os.getenv('SAMBANOVA_QWEN_25_32B')
            elif model_name == "qwen_25_72b":
                self.model_name = os.getenv('SAMBANOVA_QWEN_25_72B')
            elif model_name == "llama_3.2_11b_vision":
                self.model_name = os.getenv('SAMBANOVA_LLAMA_3.2_11B_VISION')
            elif model_name == "llama_3.2_90b_vision":
                self.model_name = os.getenv('SAMBANOVA_LLAMA_3.2_90B_VISION')
            else:
                raise ValueError("Invalid SambaNova model name")

        elif llm_client == "openai":
            api_key = os.getenv('OPENAI_API_KEY')
            base_url = os.getenv('OPENAI_BASE_URL')
            if model_name == "gpt4o_mini":
                self.model_name = os.getenv('GPT4o_MINI')
            elif model_name == "gpt4o":
                self.model_name = os.getenv('GPT4o')
            else:
                raise ValueError("Invalid OpenAI model name")
        
        elif llm_client == "ollama":
            api_key = None
            base_url = os.getenv('OLLAMA_BASE_URL')
            if model_name == "llama3.3:latest":
                self.model_name = os.getenv('OLLAMA_LLAMA33_70B')
            elif model_name == "llama3:latest":
                self.model_name = os.getenv('OLLAMA_LLAMA3_8B')
            elif model_name == "qwen2.5:0.5b":
                self.model_name = os.getenv('OLLAMA_QWEN25_05B')
            elif model_name == "qwen2.5:latest": 
                self.model_name = os.getenv('OLLAMA_QWEN25_7B')
            elif model_name == "qwq:latest":
                self.model_name = os.getenv('OLLAMA_QWQ_32B')
            elif model_name == "mixtral_latest":
                self.model_name = os.getenv('OLLAMA_MIXTRAL8_7B')
            else:
                raise ValueError("Invalid ollama model name")
            
        elif llm_client == "gemini":
            api_key = os.getenv('GEMINI_API_KEY')
            base_url = None
            if model_name == "gemini-1.0-pro-latest":
                self.model_name = os.getenv('GEMINI_10_PRO')
            elif model_name == "gemini-1.5-flash":
                self.model_name = os.getenv('GEMINI_15_FLASH')
            elif model_name == "gemini-1.5-flash-8b":
                self.model_name = os.getenv('GEMINI_15_FLASH_8b')
            elif model_name == "gemini-1.5-pro-latest":
                self.model_name = os.getenv('GEMINI_15_PRO')
            elif model_name == "gemini-2.0-flash-exp":
                self.model_name = os.getenv('GEMINI_20_FLASH')
            elif model_name == "gemini-2.0-flash-thinking-exp":
                self.model_name = os.getenv('GEMINI_20_FLASH_THINKING')
            else:
                raise ValueError("Invalid Gemini model name")

        else:
            raise ValueError("Invalid LLM client")
        
        self.llm_client = llm_client
        print(f"Initializing {self.llm_client} client with model: {self.model_name} ... ")
        self.client = self._init_endpoint(api_key=api_key, base_url=base_url)
        self.default_encoder = "o200k_base"
        self.solution = solution if solution else self.SOLUTION

    def _init_endpoint(
        self, 
        api_key: str, 
        base_url: str
    ):  
        """
        The function `_init_endpoint` initializes and returns a client object based on the specified API
        key and base URL for different LLM clients.
        
        :param api_key: The `api_key` parameter is a string that represents the API key needed for
        authentication with the API service being used. This key is typically provided by the API
        provider to authorize access to their services
        :type api_key: str
        :param base_url: The `base_url` parameter typically refers to the base URL of the API endpoint
        that the client will be interacting with. It is the common part of the URL shared by all API
        endpoints provided by the service. For example, if the API base URL is
        `https://api.example.com/v1/
        :type base_url: str
        :return: The function `_init_endpoint` returns the `client` object based on the conditions
        specified in the code snippet. The `client` object is created either as an instance of the
        `OpenAI` class with the provided `api_key` and `base_url` if `self.llm_client` is either
        "sambanova" or "openai", or as an instance of the `Client`
        """
        if self.llm_client in ["sambanova", "openai"]:
            client = OpenAI(api_key=api_key, base_url=base_url)
        elif self.llm_client == "ollama":
            client = Client(
              host=base_url,
              headers={'x-some-header': 'some-value'}
            )
        elif self.llm_client == "gemini":
            genai.configure(api_key=api_key)
            client = genai.GenerativeModel(self.model_name)
        return client
    
    def enrich_prompt(self, prompt: str, args: dict):
        """
        The function `enrich_prompt` takes a prompt string and two game strings as input, and returns
        the prompt with placeholders replaced by the game strings.
        
        :param prompt: The `enrich_prompt` function takes in a `prompt` string along with optional
        `previous_games` and `current_game` strings. It then uses the `format` method to replace
        placeholders in the `prompt` string with the values of `previous_games` and `current_game`. This
        function
        :type prompt: str
        :param previous_games: The `enrich_prompt` function takes in a prompt string along with two
        optional parameters: `previous_games` and `current_game`. The function then uses the `format`
        method to replace placeholders in the prompt string with the values of `previous_games` and
        `current_game`
        :type previous_games: str
        :param current_game: The `enrich_prompt` method takes in a prompt string along with optional
        parameters `previous_games` and `current_game`. It then uses the `format` method to replace
        placeholders in the prompt string with the values of `previous_games` and `current_game`
        :type current_game: str
        :return: The `enrich_prompt` method returns a formatted string using the provided `prompt`
        template and the `previous_games` and `current_game` values passed as arguments.
        """
        return prompt.format(
            **args
        )
    