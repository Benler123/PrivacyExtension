from typing import List, Optional
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
import os
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

class TOSChunker:
    def __init__(self, openai_api_key: Optional[str] = None):
        """
        Initialize the Terms of Service chunker.
        
        Args:
            openai_api_key: OpenAI API key. If not provided, will look for OPENAI_API_KEY in environment variables.
        """
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Set API key
        if openai_api_key:
            os.environ["OPENAI_API_KEY"] = openai_api_key
        elif not os.getenv("OPENAI_API_KEY"):
            raise ValueError(
                "OpenAI API key must be provided either as an argument or "
                "through OPENAI_API_KEY environment variable"
            )
            
        try:
            # Initialize the embeddings model
            self.embeddings = OpenAIEmbeddings()
            
            # Initialize the semantic chunker with configuration
            self.text_splitter = SemanticChunker(
                embeddings=self.embeddings,
                chunk_size=500,        # Target chunk size
                chunk_overlap=50,      # Overlap between chunks
                breakpoint_threshold=0.3  # Threshold for creating breaks
            )
        except Exception as e:
            self.logger.error(f"Failed to initialize chunker: {str(e)}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def split_documents(self, text: str) -> List[str]:
        """
        Split the document into semantic chunks.
        
        Args:
            text: The text to split into chunks
            
        Returns:
            List of text chunks
            
        Raises:
            ValueError: If the input text is empty or invalid
            Exception: If chunking fails
        """
        # Input validation
        if not text or not isinstance(text, str):
            raise ValueError("Input must be a non-empty string")
            
        try:
            # Clean the text
            cleaned_text = self._clean_text(text)
            
            # Split the text
            chunks = self.text_splitter.split_text(cleaned_text)
            
            # Post-process chunks
            processed_chunks = self._post_process_chunks(chunks)
            
            self.logger.info(f"Successfully split text into {len(processed_chunks)} chunks")
            return processed_chunks
            
        except Exception as e:
            self.logger.error(f"Error splitting text: {str(e)}")
            raise

    def _clean_text(self, text: str) -> str:
        """Clean and normalize the input text."""
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Remove special characters but keep essential punctuation
        text = re.sub(r'[^\w\s.,;:!?()-]', '', text)
        
        return text

    def _post_process_chunks(self, chunks: List[str]) -> List[str]:
        """Post-process chunks to ensure quality."""
        processed_chunks = []
        
        for chunk in chunks:
            # Remove very short chunks
            if len(chunk.split()) < 5:
                continue
                
            # Ensure chunks end at sentence boundaries where possible
            chunk = self._fix_chunk_boundaries(chunk)
            
            processed_chunks.append(chunk)
            
        return processed_chunks

    def _fix_chunk_boundaries(self, chunk: str) -> str:
        """Ensure chunks end at proper sentence boundaries."""
        # If chunk doesn't end with sentence-ending punctuation,
        # try to find the last sentence boundary
        if not chunk[-1] in '.!?':
            last_period = max(chunk.rfind('.'), chunk.rfind('!'), chunk.rfind('?'))
            if last_period != -1:
                chunk = chunk[:last_period + 1]
        return chunk.strip()

# Example usage
def main():
    # Example text
    sample_text = """
    These Terms of Service govern your use of our platform. 
    By accessing our services, you agree to these terms.
    We reserve the right to modify these terms at any time.
    Users must be at least 18 years old to use our services.
    """
    
    try:
        # Initialize chunker
        chunker = TOSChunker()
        
        # Split the text
        chunks = chunker.split_documents(sample_text)
        
        # Print results
        print("\nChunks generated:")
        for i, chunk in enumerate(chunks, 1):
            print(f"\nChunk {i}:")
            print(chunk)
            print("-" * 50)
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()