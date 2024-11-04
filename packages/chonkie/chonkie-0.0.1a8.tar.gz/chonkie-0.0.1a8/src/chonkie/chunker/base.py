from typing import List
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class Chunk:
    """Dataclass representing a text chunk with metadata."""
    text: str
    start_index: int
    end_index: int
    token_count: int

class BaseChunker(ABC):
    """Abstract base class for all chunker implementations.
    
    All chunker implementations should inherit from this class and implement
    the chunk() method according to their specific chunking strategy.
    """
    
    @abstractmethod
    def chunk(self, text: str) -> List[Chunk]:
        """Split text into chunks according to the implementation strategy.
        
        Args:
            text: Input text to be chunked
            
        Returns:
            List of Chunk objects containing the chunked text and metadata
        """
        pass

    def __call__(self, text: str) -> List[Chunk]:
        """Make the chunker callable directly.
        
        Args:
            text: Input text to be chunked
            
        Returns:
            List of Chunk objects containing the chunked text and metadata
        """
        return self.chunk(text)
    
    def __repr__(self) -> str:
        """Return string representation of the chunker."""
        return f"{self.__class__.__name__}()"