from parse_content import HTMLTextExtractor
# from tos_chunker import MLTextChunker
import pyperclip
from analyze_content import generate_analysis

if __name__ == "__main__":
    text_extractor = HTMLTextExtractor()
    # chunker = MLTextChunker()
    text, stats = text_extractor.process_url('https://disneytermsofuse.com/english/')
    text = ' '.join(text)
    pyperclip.copy(text)
    anal = generate_analysis(text)
    print(anal)
    
    
    
