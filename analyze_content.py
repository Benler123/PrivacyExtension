import anthropic
import os
import json
from prompt import system_prompt_generate_analysis
import google.generativeai as genai


def call_anthropic(system_prompt, user_prompt):
    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
    )

    messages = [
        {
            "role": "user",
            "content": user_prompt
        }
    ]
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=8192,
        messages=messages, 
        system=system_prompt
    )
    text = response.content[0].text
    return text

def call_gemini(system_prompt, user_prompt): 
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_prompt
    )
    response = model.generate_content(user_prompt)
    return response.text

def prepare_prompt(tc):         
    system_prompt = system_prompt_generate_analysis
    user_prompt =  f"Return only a JSON analysis for these T&C: {tc}"
    return system_prompt, user_prompt

def parse_response(response):
    try:
        analysis = json.loads(response)
    except:
        return None
    return analysis



def generate_analysis(tc): 
    system_prompt, user_prompt = prepare_prompt(tc)
    response = call_gemini(system_prompt, user_prompt)
    analysis = parse_response(response)
    if analysis is None:
        response = call_anthropic(system_prompt, user_prompt)
        analysis = parse_response(response)

    return analysis


if __name__ == "__main__":
    url = "https://press.hulu.com/privacy-policy/"
    analysis = generate_analysis(url)
