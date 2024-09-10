import logging
from groq import Groq

client = Groq(api_key="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")
logging.debug(f"Groq: {client}")

def summarize_text(text_to_summarize):
    template = "Summarize the following text: " + text_to_summarize
    
    # Create a request to Groq API to generate completion with a model
    response = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": template
        }],
        model="llama-3.1-8b-instant"
    )

    choice = response.choices[0]
    message = choice.message.content

    return message
