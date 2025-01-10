
import os
import base64
from openai import AzureOpenAI
import json

endpoint = os.getenv("ENDPOINT_URL", "https://ai-obicherechinasa6198ai384624680927.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o-mini")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "FGDHTXVOemvrf3z4IFo9Vw61cypLFCoJW7zV8mkyiEISeoYaY5VPJQQJ99ALACHYHv6XJ3w3AAAAACOG2xWB")

# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2024-05-01-preview",
)


# IMAGE_PATH = "YOUR_IMAGE_PATH"
# encoded_image = base64.b64encode(open(IMAGE_PATH, 'rb').read()).decode('ascii')


#Prepare the chat prompt

def ai_compare_answer(userInput, correctAnswer):

    #Prepare the chat prompt
    chat_prompt = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": "You are an AI assistant that determines whether two inputs match and refer to the same context. Begin every response with 'Yes' or 'No,' followed by a brief explanation."
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"Does {userInput} match {correctAnswer}"
                }
            ]
        },

    ]

    # Include speech result if speech is enabled
    messages = chat_prompt

    # Generate the completion
    completion = client.chat.completions.create(
        model=deployment,
        messages=messages,
        max_tokens=800,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False
    )

    api_response =  json.loads(completion.to_json())
    return api_response["choices"][0]["message"]["content"]

