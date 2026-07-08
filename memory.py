"""
Conversation Memory
"""

from database import save_chat, load_chat, clear_chat


class ConversationMemory:

    def __init__(self):
        self.history = []

    # ==============================
    # Save Chat
    # ==============================

    def save(self, user, question, answer):

        save_chat(user, question, answer)

        self.history.append(
            {
                "question": question,
                "answer": answer
            }
        )

    # ==============================
    # Load Chat
    # ==============================

    def load(self, user):

        chats = load_chat(user)

        self.history = []

        for question, answer in chats:

            self.history.append(
                {
                    "question": question,
                    "answer": answer
                }
            )

        return chats

    # ==============================
    # Clear Chat
    # ==============================

    def clear(self, user=None):

        self.history = []

        if user:
            clear_chat(user)

    # ==============================
    # Context
    # ==============================

    def get_context(self, limit=5):

        if not self.history:
            return ""

        context = []

        for item in self.history[-limit:]:

            context.append(f"User: {item['question']}")
            context.append(f"Assistant: {item['answer']}")

        return "\n".join(context)

    # ==============================
    # Last Question
    # ==============================

    def last_question(self):

        if not self.history:
            return ""

        return self.history[-1]["question"]

    # ==============================
    # Last Answer
    # ==============================

    def last_answer(self):

        if not self.history:
            return ""

        return self.history[-1]["answer"]


# Singleton instance
memory = ConversationMemory()