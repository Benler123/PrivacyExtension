import anthropic
import os

def call_anthropic(system_prompt, messages):
    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
    )
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=messages, 
        system=system_prompt
    )
    content = response.content
    return content

def prepare_prompt(tc, questions): 
    numbered_questions = "\n".join(f"{i+1}. {q}" for i, q in enumerate(questions))
        
    system_prompt = tc + """
    You must analyze questions about the T&C and respond ONLY with a list of numbers:
    - 1 if the answer is yes/allowed/permitted
    - 0 if the answer is no/not allowed/not permitted

    Return ONLY the list of numbers separated by commas, in the same order as the questions without any explanation or additional text."""

    messages = [
        {
            "role": "user",
            "content": f"Based on the T&C, answer with return only comma-separated list of 0, 1 for these questions:\n{numbered_questions}"
        }
    ]

    return system_prompt, messages

def parse_response(response): 
    str_array = response[0].text
    int_array = [int(x.strip()) for x in str_array.split(',')]
    return int_array

def generate_analysis(tc): 
    questions = [
        "Do they collect data they don't need for the service?",
        "Are they collecting data from your other devices or accounts?",
        "Do they track your activity across other websites?",
        "Can they access your contacts or address book?"
    ]

    system_prompt, messages = prepare_prompt(tc, questions)
    response = call_anthropic(system_prompt, messages)
    bool_answers = parse_response(response)

    return bool_answers





