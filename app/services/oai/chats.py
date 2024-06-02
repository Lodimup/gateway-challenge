"""
OpenAI's chat completions related services
"""

from openai import OpenAI


class ChatBot:
    """
    Simple chatbot class that uses OpenAI's Chat API.
    Chat history is not handled by OpenAI, so we need to keep track of it,
    for context to be maintained.
    WARN: Longer chat history results in more tokens, and higher costs.
    - instantiate the class
    - set a system message if needed using .set_system_message()
    - add user messages using .add_message() if needed
    - or, just chat using .chat()
    TODO: Not in current scope. Persists the chat history in a database, across API calls.
    Args:
        model (str): model name
        max_hist (int): maximum history length
    """

    def __init__(self, model="gpt-3.5-turbo", max_hist=15):
        self.client = OpenAI()
        self.model = model
        self.messages = []
        self.max_hist = max_hist

    def _handle_max_hist(self) -> None:
        """
        Check if the message list is longer than the max history.
        If it is, remove the oldest message. that is not a system message.
        """
        if len(self.messages) > self.max_hist:
            self.messages.pop(1)
            self.messages.pop(1)

    def _is_system_exists(self) -> bool:
        """
        Check if there is a system message in the messages list.
        Returns:
            bool: True if there is a system message, False otherwise.
        """
        for i in self.messages:
            if i.get("role") == "system":
                return True

        return False

    def set_system_message(self, content: str) -> None:
        """
        Set the system message.
        if there is already a system message, it will be replaced,
        and the message list will be cleared.
        Args:
            content (str): content of the system message
        """
        if self._is_system_exists():
            self.messages = []

        self.messages.append({"role": "system", "content": content})

    def add_message(self, content: str, role: str) -> None:
        """
        Add a message to the message list.
        Args:
            content (str): content of the message
            role (str): role of the message
        """
        self.messages.append({"role": role, "content": content})
        self._handle_max_hist()

    def chat(self, content: str) -> str:
        """
        Send a message to the chatbot and get a response.
        Args:
            content (str): content of the message
        Returns:
            str: response from the chat completion
        """
        self.messages.append({"role": "user", "content": content})
        r = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
        )
        message = r.choices[0].message
        self.messages.append({"role": message.role, "content": message.content})
        self._handle_max_hist()

        return message.content
