from typing import Literal

from chromadb import PersistentClient

from config import config
from logger import logger
from utils.path import path


memory_path = config.path.memory
chat_history_length = config.general.chat_history_length
ENTRY_TYPE = Literal["chatHistory"]

class Memory:
    def __init__(self) -> None:
        self.name = "smallYauyu"
        self.client = PersistentClient(path(memory_path))
        self.collection = self.client.get_or_create_collection("memory")
        self.chat_history = []
        self.context = []
        
    def entry_exist(self, type: ENTRY_TYPE, identifier: str) -> bool:
        if self.collection.get(
                where={"$and" : [
                        {"type" : {"$eq" : type}},
                        {"identifier" : {"$eq" : identifier}}
                    ]
                })['documents']:
            return True
        logger.warning(f"No entry of type '{type}' with identifier '{identifier}' was found in the database.")
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
            logger.warning(f"Could not update entry with type '{type}' and identifier '{identifier}' as none was found.")
            return False
        self.collection.update(ids=self.get_id(type=type, identifier=identifier), documents=content)
        logger.info(f"Update entry with type '{type}' and identifier '{identifier}' success.")
        return True
    
    def create_entry(self, type: ENTRY_TYPE, identifier: str, content: str) -> bool:
        # if self.entry_exist(type, identifier):
        #     logger.warning(f"Entry of type '{type}' with identifier '{identifier}' already exists in database.")
        #     return False
        self.collection.add(
            ids=[str(self.collection.count()+1)],
            metadatas=[{"type" : type, "identifier" : identifier}],
            documents=content
        )
        logger.info(f"New entry with id '{self.collection.count()}' has been created.")
        return True
    
    def update_or_create_entry(self, type: ENTRY_TYPE, identifier: str, content: str) -> None:
        if self.entry_exist(type, identifier):
            self.update_entry(type, identifier, content)
        else:
            self.create_entry(type, identifier, content)
    
    def query_memory(
            self,
            queries: list[str],
            type: ENTRY_TYPE|None = None,
            identifier: str|None = None,
            n_results: int = 10,
            max_distance: float = 0.6):
        result = None
        if type is None:
            result = self.collection.query(query_texts=queries, n_results=n_results)
        else:
            if identifier is None:
                result = self.collection.query(
                    query_texts=queries,
                    where={"type": {"$eq": type}},
                    n_results=n_results
                )
            else:
                result = self.collection.query(
                    query_texts=queries,
                    where={"$and" : [
                            {"type" : {"$eq" : type}},
                            {"identifier" : {"$eq" : identifier}}
                        ]
                    },
                    n_results=n_results
                )
        if result is not None:
            filtered_documents = []
            for i, distance in enumerate(result["distances"][0]):
                if distance > max_distance: continue
                filtered_documents.append(result["documents"][0][i])
            logger.info(f"query result: {result}")
            return filtered_documents
        logger.warning("No result")
        return result
    
    def save_chat(self, role, content):
        if len(self.chat_history) > chat_history_length:
            self.chat_history.pop(0)
        self.chat_history.append({
            "role": role,
            "content": content
        })