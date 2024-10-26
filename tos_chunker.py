import numpy as np
from typing import List, Tuple
from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering
import re

class MLTextChunker:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize the ML-based text chunker.
        
        Args:
            model_name: Name of the sentence-transformer model to use
        """
        self.model = SentenceTransformer(model_name)
        
    def split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences using regex patterns."""
        # Clean the text
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Split on sentence boundaries
        sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
        
        # Filter out empty or very short sentences
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        return sentences
    
    def get_embeddings(self, sentences: List[str]) -> np.ndarray:
        """Generate embeddings for sentences using the transformer model."""
        return self.model.encode(sentences, show_progress_bar=False)
    
    def cluster_sentences(self, 
                         embeddings: np.ndarray, 
                         threshold: float = 1.0) -> List[int]:
        """
        Cluster sentences based on their semantic similarity.
        
        Args:
            embeddings: Sentence embeddings
            threshold: Distance threshold for clustering (lower = more clusters)
        
        Returns:
            List of cluster labels for each sentence
        """
        clustering = AgglomerativeClustering(
            n_clusters=None,
            distance_threshold=threshold,
            metric='cosine',
            linkage='average'
        )
        return clustering.fit_predict(embeddings)
    
    def chunk_text(self, 
                  text: str, 
                  threshold: float = 1.0,
                  min_chunk_size: int = 2) -> List[Tuple[str, List[str]]]:
        """
        Break text into semantic chunks using ML.
        
        Args:
            text: Input text to chunk
            threshold: Clustering threshold
            min_chunk_size: Minimum number of sentences per chunk
        
        Returns:
            List of tuples containing (topic sentence, chunk sentences)
        """
        # Split into sentences
        sentences = self.split_into_sentences(text)
        if not sentences:
            return []
            
        # Get embeddings
        embeddings = self.get_embeddings(sentences)
        
        # Cluster sentences
        labels = self.cluster_sentences(embeddings, threshold)
        
        # Group sentences by cluster
        chunks = []
        for label in sorted(set(labels)):
            chunk_sentences = [s for i, s in enumerate(sentences) if labels[i] == label]
            
            # Only keep chunks with enough sentences
            if len(chunk_sentences) >= min_chunk_size:
                # Use the first sentence as the topic sentence
                topic = chunk_sentences[0]
                chunks.append((topic, chunk_sentences))
        
        return chunks

    def print_chunks(self, chunks: List[Tuple[str, List[str]]]) -> None:
        """Print chunks in a readable format."""
        for i, (topic, sentences) in enumerate(chunks, 1):
            print(f"\nChunk {i}")
            print(f"Topic: {topic}")
            print("Content:")
            for s in sentences:
                print(f"  - {s}")
            print("-" * 80)

# Example usage
def process_document(text: str) -> None:
    """Process a document and print the semantic chunks."""
    chunker = MLTextChunker()
    chunks = chunker.chunk_text(
        text,
        threshold=0.8,  # Adjust for more/fewer chunks
        min_chunk_size=2
    )
    chunker.print_chunks(chunks)