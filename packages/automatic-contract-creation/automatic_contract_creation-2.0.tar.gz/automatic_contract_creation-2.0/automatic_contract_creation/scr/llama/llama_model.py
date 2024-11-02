import os

from openai import OpenAI


class LlamaModel:
    def __init__(self, context):
        self.context = context
        self.client=OpenAI(
                        api_key="a",
                        base_url=os.getenv('llama_api_url'),
                    )


    def get_response(self, prompt_messages):
        chat_completion = self.client.chat.completions.create(
            messages=prompt_messages,
            model="Meta-Llama-3-70B-Instruct-GPTQ",
            temperature=0.7,
            # stream=True
        )


        # for chunk in chat_completion:
        #     print(chunk.choices[0].delta.content or "", end="")

        response_text = chat_completion.choices[0].message.content

        return response_text

