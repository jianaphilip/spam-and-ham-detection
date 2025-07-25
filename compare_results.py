# def tab(text):
    
    
#     data = {
#             "text": f"{}",
#             "method": ""
#         }
    
#     headers = {
#         "Content-type": "application/json"
#         }
    
#     url = "http://localhost:5000/detect-spam"
    
#     import requests
#     response = requests.post(url, headers=headers, json=data)
#     if response.status_code == 200:
#         response_dict = response.json()
        # print(response_dict["message"])
import requests
import pandas as pd

def get_spam_detection_result(text, model_type):
    
    api_url = "http://localhost:5000/detect-spam"
    
   
    data = {
        "text": text,
        "method": model_type
    }
    
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        
        response = requests.post(api_url, json=data, headers=headers)
        
        
        if response.status_code == 200:
            return response.json()
        else:
            print("Error:", response.text)
            return None
    except Exception as e:
        print("Error occurred:", e)
        return None

def compare_results(text):
    models = ['Naive Bayes', 'Random Forest', 'LSTM', 'LLM']
    results = {}
    
    for model in models:
        result = get_spam_detection_result(text, model)
        if result:
            results[model] = result['spam_probability']
    
    return results

def main():
    text = ""
    comparison_results = compare_results(text)
    
    if comparison_results:
        df = pd.DataFrame.from_dict(comparison_results, orient='index', columns=['Spam Probability'])
        print(df)

if __name__ == "__main__":
    main()
