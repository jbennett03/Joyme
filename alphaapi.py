import wolframalpha
from dotenv import load_dotenv
import os
import google.generativeai as genai
from PIL import Image
load_dotenv()

appID = os.getenv("appID")
geminiKey = os.getenv("geminiKey")
client = wolframalpha.Client(appID)
genai.configure(api_key=geminiKey)
model = genai.GenerativeModel("gemini-2.5-flash")
image_prompt = Image.open('capture.png')
#problem parsing tests 
#short answers problem
def solver(question_text):
    try:
        result = client.query(question_text)
        wolframAnswer = next(result.results).text
    except Exception as e:
        print("Error from WolframAlpha:", e)
        wolframAnswer = "Could not receive an answer"

    prompt = [f"""The User asked: {question_text}

Explain how to solve the student's problem step-by-step strictly from a math perspective. Do not include other subjects in this explanation
""", image_prompt]
    print("Wolframalpha: ", wolframAnswer)

    try:
        response = model.generate_content(prompt)
        print("Gemini: ", response.text)
        return response.text
    except Exception as e:
        print("Error from Gemini:", e)
        return "There was an error generating the explanation."





#what do we want to acheive? 


