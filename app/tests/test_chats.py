"""
Test ChatBot Class
"""

import pytest

from services.oai.chats import ChatBot


@pytest.mark.skip(reason="Expensive test.")
def test_chat():
    """
    There should not be raised exceptions
    """
    chatbot = ChatBot()
    chatbot.set_system_message("You are a bot")
    chatbot.chat("Hello")
