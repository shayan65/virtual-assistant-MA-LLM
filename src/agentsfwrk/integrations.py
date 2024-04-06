import json
import os
import time
from typing import Union

import openai
from openai.error import APIConnectionError, APIError, RateLimitError

import agentsfwrk.logger as logger

log = logger.get_logger(__name__)

openai.api_key = os.getenv('OPENAI_API_KEY')

class OpenAIIntegrationService:
    def __init__(self, context: Union[str, dict], instruction: Union[str, dict]) -> None:
        self.context = context if isinstance(context, dict) else {"text": context, "role": "system"}
        self.instructions = instruction
        self.messages = [self.context] if isinstance(self.context, dict) else [{"text": self.context + self.instructions, "role": "user"}]

    def get_models(self):
        try:
            return openai.Model.list()
        except Exception as e:
            log.error(f"Error fetching model list: {e}")
            return None

    def add_chat_history(self, messages: list):
        self.messages.extend(messages)

    def answer_to_prompt(self, model: str, prompt: str, **kwargs):
        self.messages.append({'role': 'user', 'content': prompt})
        retry_exceptions = (APIError, APIConnectionError, RateLimitError)

        for attempt in range(3):
            try:
                response = openai.ChatCompletion.create(model=model, messages=self.messages, **kwargs)
                response_message = response.choices[0].message["content"]
                self.messages.append({'role': 'assistant', 'content': response_message})
                return {"answer": response_message}
            except retry_exceptions as e:
                log.error(f"Attempt {attempt + 1}: Exception occurred: {e}")
                if attempt == 2:  # Last attempt
                    log.error("Last attempt failed.")
                    return {"answer": "Sorry, I'm having technical issues."}
                time.sleep(getattr(e, 'retry_after', 3))

    def answer_to_simple_prompt(self, model: str, prompt: str, **kwargs):
        messages = "\n".join([msg["content"] for msg in self.messages]) + f"\n<Client>: {prompt} \n"
        retry_exceptions = (APIError, APIConnectionError, RateLimitError)

        for attempt in range(3):
            try:
                response = openai.Completion.create(model=model, prompt=messages, **kwargs)
                response_message = response.choices[0].text
                self.messages.append({'role': 'assistant', 'content': response_message})
                return self.parse_response(response_message, prompt)
            except retry_exceptions as e:
                log.error(f"Attempt {attempt + 1}: Exception occurred: {e}")
                if attempt == 2:  # Last attempt
                    log.error("Last attempt failed.")
                    return {"intent": False, "answer": "Sorry, I'm having technical issues."}
                time.sleep(getattr(e, 'retry_after', 3))
    def verify_end_conversation(self):
        """
        Verify if the conversation has ended by checking the last message from the user
        and the last message from the assistant.
        """
        pass

    def verify_goal_conversation(self, model: str, **kwargs):
        """
        Verify if the conversation has reached the goal by checking the conversation history.
        Format the response as specified in the instructions.
        """
        messages = self.messages.copy()
        messages.append(self.instructions)

        retry_exceptions = (APIError, APIConnectionError, RateLimitError)
        for _ in range(3):
            try:
                response = openai.ChatCompletion.create(
                    model       = model,
                    messages    = messages,
                    **kwargs
                )
                break
            except retry_exceptions as e:
                if _ == 2:
                    log.error(f"Last attempt failed, Exception occurred: {e}.")
                    raise
                retry_time = getattr(e, 'retry_after', 3)
                log.error(f"Exception occurred: {e}. Retrying in {retry_time} seconds...")
                time.sleep(retry_time)

        response_message = response.choices[0].message["content"]
        try:
            response_data = json.loads(response_message)
            if response_data.get('summary') is None:
                raise ValueError("The response from the model is not valid. Missing summary.")
        except ValueError as e:
            log.error(f"Error occurred while parsing response: {e}")
            log.error(f"Response from the model: {response_message}")
            log.info("Returning a safe response to the user.")
            raise

        return response_data
