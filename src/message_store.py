import json
from datetime import datetime
from typing import Dict, List, Optional


class MessageStore:
    def __init__(self, storage_path: str = "data/conversations.json"):
        self.storage_path = storage_path
        self.conversations: Dict[str, List[Dict]] = self._load_conversations()

    def _load_conversations(self) -> Dict[str, List[Dict]]:
        """Load conversations from storage"""
        try:
            with open(self.storage_path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_conversations(self):
        """Save conversations to storage"""
        with open(self.storage_path, "w") as f:
            json.dump(self.conversations, f, indent=2)

    def add_message(
        self,
        conversation_id: str,
        sender: str,
        content: str,
        message_type: str = "text",
    ):
        """Add a message to a conversation"""
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []

        message = {
            "sender": sender,
            "content": content,
            "type": message_type,
            "timestamp": datetime.now().isoformat(),
        }

        self.conversations[conversation_id].append(message)
        self._save_conversations()

    def get_conversation_history(
        self, conversation_id: str, limit: Optional[int] = None
    ) -> List[Dict]:
        """Get messages from a conversation"""
        messages = self.conversations.get(conversation_id, [])
        if limit:
            return messages[-limit:]
        return messages

    def format_history(self, conversation_id: str, limit: Optional[int] = None) -> str:
        """Format conversation history for prompt context"""
        messages = self.get_conversation_history(conversation_id, limit)
        formatted = []

        for msg in messages:
            formatted.append(f"{msg['sender']}: {msg['content']}")

        return "\n".join(formatted)
