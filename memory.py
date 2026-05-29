class Memory:
    def __init__(self, max_history=5):
        self.history = []
        self.max_history = max_history

    # -------------------------------
    # ADD INTERACTION
    # -------------------------------
    def add(self, user_query, agent_response):
        self.history.append({
            "user": user_query,
            "agent": str(agent_response)
        })

        # Keep only last N interactions
        if len(self.history) > self.max_history:
            self.history.pop(0)

    # -------------------------------
    # GET CONTEXT
    # -------------------------------
    def get_context(self):
        context = ""
        for chat in self.history:
            context += f"User: {chat['user']}\n"
            context += f"Agent: {chat['agent']}\n"
        return context.strip()