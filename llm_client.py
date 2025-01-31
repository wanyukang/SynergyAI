import os
import time
from typing import Optional
from openai import OpenAI


class LLMClient:
    _instance: Optional['LLMClient'] = None
    
    def __init__(self):
        # OpenAI
        # self._endpoint = "https://models.inference.ai.azure.com"
        # self._token = os.environ.get("GITHUB_TOKEN")
        # self._default_model = "o1-mini"

        # deepseek
        # self._endpoint = "https://api.deepseek.com"
        # self._token = os.environ.get("DEEPSEEK_TOKEN")
        # self._default_model = "deepseek-chat"

        # Qwen/Qwen2.5-32B-Instruct from siliconflow
        self._endpoint = "https://api.siliconflow.cn"
        self._token = os.environ.get("SILICONFLOW_TOKEN")
        self._default_model = "Qwen/Qwen2.5-32B-Instruct"
    
        self._client = None
        self._init_client()

        
    
    def _init_client(self) -> None:
        """Initialize OpenAI client"""
        if not self._token:
            raise ValueError("请设置 GITHUB_TOKEN 环境变量")
            
        self._client = OpenAI(
            base_url=self._endpoint,
            api_key=self._token
        )
    
    @classmethod
    def get_instance(cls) -> 'LLMClient':
        """Get singleton instance of LLMClient"""
        if cls._instance is None:
            cls._instance = LLMClient()
        return cls._instance
    
    # def ask(self, 
    #         prompt: str, 
    #         history: list[dict] = None, 
    #         model_name: str = None,
    #         temperature: float = 1) -> str:
    #     """
    #     Send a prompt to the LLM model and get response
        
    #     Args:
    #         prompt: The input text prompt
    #         history: List of previous messages in [{"role": "user/assistant", "content": "msg"}] format
    #         model_name: Name of the model to use, defaults to o1-mini
    #         temperature: Controls randomness in the response (0.0-1.0)
        
    #     Returns:
    #         The model's response text
            
    #     Raises:
    #         ValueError: If prompt is empty
    #         Exception: If LLM call fails
    #     """
    #     if not prompt.strip():
    #         raise ValueError("Prompt cannot be empty")
            
    #     try:
    #         messages = []
    #         if history:
    #             messages.extend(history)
    #         messages.append({"role": "user", "content": prompt})
            
    #         response = self._client.chat.completions.create(
    #             messages=messages,
    #             model=model_name or self._default_model,
    #             temperature=temperature,
    #             # stream=True
    #         )
    #         print(f"LLM Response:")
    #         print(f"ID: {response.id}")
    #         print(f"Model: {response.model}")
    #         print(f"Created: {response.created}")
    #         # print(f"Content: {response.choices[0].message.content}")
    #         print(f"Role: {response.choices[0].message.role}")
    #         print(f"Finish Reason: {response.choices[0].finish_reason}")
    #         print(f"Usage - Prompt Tokens: {response.usage.prompt_tokens}")
    #         print(f"Usage - Completion Tokens: {response.usage.completion_tokens}")
    #         print(f"Usage - Total Tokens: {response.usage.total_tokens}")
    #         return response.choices[0].message.content
            
    #     except Exception as e:
    #         raise Exception(f"LLM call failed: {str(e)}")

    
    # 老ask使用示例:
    # client = LLMClient.get_instance()
    # response = client.ask("What is the capital of France?")



    def ask(self, 
        prompt: str, 
        history: list[dict] = None, 
        model_name: str = None,
        temperature: float = 1,
        max_retries: int = 3,
        retry_delay: float = 1.0) -> Optional[str]:
        """
        Send a prompt to the LLM model with retry mechanism
        
        Args:
            prompt: The input text prompt
            history: List of previous messages
            model_name: Name of the model to use
            temperature: Controls randomness (0.0-1.0)
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds
        """
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty")
            
        attempt = 0
        last_error = None
        
        while attempt < max_retries:
            try:
                messages = []
                if history:
                    messages.extend(history)
                messages.append({"role": "user", "content": prompt})
                
                response = self._client.chat.completions.create(
                    messages=messages,
                    model=model_name or self._default_model,
                    temperature=temperature
                )
                
                # Validate response
                if not response or not response.choices:
                    raise ValueError("Empty response from API")
                    
                # Log response details
                # print(f"LLM Response:")
                # print(f"ID: {response.id}")
                # print(f"Model: {response.model}")
                # print(f"Created: {response.created}")
                # print(f"Role: {response.choices[0].message.role}")
                # print(f"Finish Reason: {response.choices[0].finish_reason}")
                # print(f"Usage - Total Tokens: {response.usage.total_tokens}")
                
                return response.choices[0].message.content
                
            except Exception as e:
                last_error = str(e)
                attempt += 1
                if attempt < max_retries:
                    print(f"Attempt {attempt} failed: {last_error}")
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    continue
                
        raise Exception(f"LLM call failed after {max_retries} attempts. Last error: {last_error}")


# 新ask使用示例，带重试机制:
# response = client.ask(prompt, max_retries=3, retry_delay=1.0)