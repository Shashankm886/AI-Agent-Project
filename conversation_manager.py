class ConversationManager:
    def __init__(self):
        self.history = []

    def add_user_message(self, message):
        self.history.append({'role': 'user', 'content': message})

    def add_agent_message(self, message):
        self.history.append({'role': 'assistant', 'content': message})

    def get_messages(self):
        """
        Returns the conversation history as a list of messages in the format required by the API.
        """
        return self.history
