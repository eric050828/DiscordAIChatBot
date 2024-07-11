from typing import NewType, Literal

from chromadb import PersistentClient

from utils.config import get_config
from utils.logger import logger
from utils.path import path


memory_path = get_config("default", "memory_path")
chat_history_length = get_config("default", "chat_history_length")
ENTRY_TYPE = NewType("ENTRY_TYPE", Literal["chatHistory"])

class Memory:
    def __init__(self) -> None:
        self.client = PersistentClient(path(memory_path))
        self.collection = self.client.get_or_create_collection("memory")
        self.chat_history = []
        
    def entry_exist(self, type: ENTRY_TYPE, identifier: str) -> bool:
        if self.collection.get(
                where={"$and" : [
                        {"type" : {"$eq" : type}},
                        {"identifier" : {"$eq" : identifier}}
                    ]
                })['documents']:
            return True
        logger.error(f"No entry of type '{type}' with identifier '{identifier}' was found in the database.")
        return False
    
    def get_id(self, type: ENTRY_TYPE, identifier: str):
        result = self.collection.get(
            where={"$and" : [
                    {"type" : {"$eq" : type}},
                    {"identifier" : {"$eq" : identifier}}
                ]
            }
        )
        return result["ids"][0]
    
    def update_entry(self, type: ENTRY_TYPE, identifier: str, content: str) -> bool:
        if not self.entry_exist(type, identifier):
            logger.error(f"Could not update entry with type '{type}' and identifier '{identifier}' as none was found.")
            return False
        self.collection.update(ids=self.get_id(type=type, identifier=identifier), documents=content)
        logger.log(f"Update entry with type '{type}' and identifier '{identifier}' success.")
        return True
    
    def create_entry(self, type: ENTRY_TYPE, identifier: str, content: str) -> bool:
        if self.entry_exist(type, identifier):
            logger.error(f"Entry of type '{type}' with identifier '{identifier}' already exists in database.")
            return False
        self.collection.add(
            ids=[str(self.collection.count()+1)],
            metadatas=[{"type" : type, "identifier" : identifier}],
            documents=content
        )
        logger.log(f"New entry with id '{self.collection.count()}' has been created.")
        return True
    
    def update_or_create_entry(self, type: ENTRY_TYPE, identifier: str, content: str) -> None:
        if self.entry_exist(type, identifier):
            self.update_entry(type, identifier, content)
        else:
            self.create_entry(type, identifier, content)
    
    def query_context():  # TODO: get long-term memory
        pass
    
    def save_chat(self, role, content):
        if len(self.chat_history) > chat_history_length:
            self.chat_history.pop(0)
        self.chat_history.append({
            "role": role,
            "content": content
        })