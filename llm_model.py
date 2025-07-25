import traceback
from flask import Flask, request, jsonify, render_template
from groq import Groq
import json
app = Flask(__name__)

def llm_model(text):
    try:
        client = Groq(
            api_key="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",
        )
        
        prompt_content = """############################################
        
        Instruction:
        You are presented with the content of an email. Your task is to predict whether the given email is "HAM" or "SPAM" along with a justification for both classes. Your output should only be a structured JSON of the following format:
        ```json
        {
            "prediction": "SPAM or HAM",
            "justification": "Text message"
        }
        ```
        Your output should only contain properly formatted JSON and nothing else. You will be penalized for not adhering to this instruction.
        #############################################
        
        Email content:\n\n""" + text

   
        
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt_content}
            ],
            model="llama3-70b-8192",
        )
        
            # Retrieve the message content from Groq response
        message = chat_completion.choices[0].message.content
        print("message", message, "\n------------")
        with open('log.txt', 'a') as fl:
            fl.write(message)
            
    
        try:
            # Attempt to parse the message content as JSON
            message_dict = json.loads(message)
            with open('llm_response.json', 'w') as fj:
                json.dump(message_dict, fj)
            print("Justification:", message_dict['justification'])
            prediction = message_dict['prediction']
            justification = message_dict['justification']
            return {'message': prediction, 'justification': justification}
        
        except json.JSONDecodeError:
            # If JSON parsing fails, check for SPAM or HAM keywords
            if "SPAM" in message and "HAM" not in message:
                reason = "Contains suspicious keywords or patterns."
                return {'message': "SPAM", 'justification': message}
            else:
                return {'message': "HAM", 'justification': ""}
    


        
    except Exception as e:
        print("llmerror: ", traceback.format_exc())
        return {'message': f"API error: {str(e)}", "justification": ""}

@app.route('/detect-spam', methods=['POST'])
def detect_spam():
    data = request.get_json()
    text = data['text']
    method = data['method']
    
    if method == 'LLM':
        result = llm_model(text)
        return jsonify(result)
    else:
        return jsonify({'message': 'Unsupported method'}), 400

