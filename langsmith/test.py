
import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)

# Models returned by your API
models = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite"
]

successful_model = None

for model in models:

    print("\nTesting:", model)

    try:

        response = client.models.generate_content(
            model=model,
            contents="Hello! Introduce yourself in one sentence."
        )

        if response.text:

            print("SUCCESS!")
            print("Working Model:", model)
            print("Response:", response.text)

            successful_model = model
            break

    except Exception as e:

        print("FAILED:", str(e)[:250])

        time.sleep(2)

if successful_model:

    print("\n================================")
    print("WORKING MODEL:", successful_model)
    print("================================")

else:

    print("\nNo model generated a response.")
    print("Please check API availability and try again.")

