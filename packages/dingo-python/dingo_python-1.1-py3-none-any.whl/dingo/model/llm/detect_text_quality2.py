import json
import time

from dingo.config.config import DynamicLLMConfig
from dingo.io import MetaData
from dingo.model import Model
from dingo.model.llm.base import BaseLLM
from dingo.model.llm.prompts.manager import get_prompt
from dingo.model.modelres import ModelRes
from dingo.utils import log


@Model.llm_register('lmdeploy_openai')
class LmdeployOpenai(BaseLLM):
    client = None

    dynamic_config = DynamicLLMConfig(prompt_id="CONTEXT_QUALITY_PROMPT")

    @classmethod
    def create_client(cls):
        from lmdeploy.serve.openai.api_client import APIClient
        cls.client = APIClient(cls.dynamic_config.api_url)

    @classmethod
    def call_api(cls, input_data: MetaData) -> ModelRes:
        if cls.client is None:
            cls.create_client()
        messages = [
            # {"role": "system",
            # "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
            # {"role": "user", "content": "你好，我叫李雷，1+1等于多少？"},
            {"role": "user", "content": get_prompt(cls.dynamic_config) + input_data.content}
        ]

        attempts = 0
        except_msg = ''
        model_name = cls.client.available_models[0]
        while attempts < 3:
            try:
                response = None
                for item in cls.client.chat_completions_v1(model=model_name, messages=messages):
                    response = item['choices'][0]['message']['content']
                log.info(response)

                if response.startswith('```json'):
                    response = response[7:]
                if response.startswith('```'):
                    response = response[3:]
                if response.endswith('```'):
                    response = response[:-3]

                response_json = json.loads(response)

                return ModelRes(
                    error_status=True if response_json['score'] == 0 else False,
                    type=response_json['type'],
                    name=response_json.get('name', 'data'),
                    reason=response
                )
            except Exception as e:
                attempts += 1
                time.sleep(1)
                except_msg = str(e)

        return ModelRes(
            error_status=True,
            type='quality_bad',
            name="api_loss",
            reason=except_msg
        )
