import wolframalpha
from dotenv import load_dotenv
import os
import google.generativeai as genai


load_dotenv()

appID = os.getenv("appID")
geminiKey = os.getenv("geminiKey")
client = wolframalpha.Client(appID)
genai.configure(api_key=geminiKey)
model = genai.GenerativeModel("gemini-2.5-flash")

#problem parsing tests 
#short answers problem
input = input("Enter your question: ") #right now this is console input but we somehow have to change this to the drawn input
try:
    result = client.query(input)
    wolframAnswer = next(result.results).text
except Exception as e:
    print("Error from WolframAlpha:", e)
    wolframAnswer = "Could not receive an answer"

prompt = f"""The User asked: {input}
WolframAlpha returned the answer: {wolframAnswer}

Please explain how to solve this step-by-step in simple terms, like a tutor helping a student.
"""


try:
    response = model.generate_content(prompt)
    print("\n Explanation:\n")
    print(response.text)
except Exception as e:
    print("Error from Gemini:", e)


#send the input to the wolframalpha api to solve. 







#what do we want to acheive? 

