import os
from litellm import completion
# python -m spacy download en_core_web_sm
import spacy

class CloudflareAgent:
    def __init__(self, text):
        self.text = text

    def execute_task(self, text):
        llm_response = completion(
            model="cloudflare/@cf/meta/llama-2-7b-chat-int8",
            messages=[
                {"role": "user", "content": "Hello you will be a ethical cybersecurity engineer certified in ISO/IEC "
                                            "27001/24 certifications, with given data you will indentify any potential "
                                            "threats that may occur because of provided data:" + text}
            ],
        )
        return llm_response
