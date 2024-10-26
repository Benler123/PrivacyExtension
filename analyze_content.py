import anthropic
import os
import json
from prompt import system_prompt_generate_analysis
import pyperclip

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
)
    
def call_anthropic(system_prompt, messages):
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=8192,
        messages=messages, 
        system=system_prompt
    )
    content = response.content
    return content

def prepare_prompt(tc): 
    # numbered_questions = "\n".join(f"{i+1}. {q}" for i, q in enumerate(questions))
        
    system_prompt = system_prompt_generate_analysis

    messages = [
        {
            "role": "user",
            "content": f"Return a JSON analysis for this T&C. Please make sure it is serializable: {tc}"
        }
    ]

    return system_prompt, messages

def parse_response(response):
    response = response[0].text
    pyperclip.copy(response)
    analysis = json.loads(response)
    return analysis



def generate_analysis(tc): 
    system_prompt, messages = prepare_prompt(tc)
    response = call_anthropic(system_prompt, messages)
    analysis = parse_response(response)

    return analysis



if __name__ == "__main__":
    url = "https://press.hulu.com/privacy-policy/"
    analysis = generate_analysis(url)
