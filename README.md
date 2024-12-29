# Medicine Information Retrieval System using LLMs (OpenAI <GPT4o & GPT4o-mini>)

## Project Aim  
This project leverages FDA's(US Food & Drug Administration) open-source APIs to provide answers to medicine-related questions. The API responses act as the knowledge base for this system, ensuring accurate and up-to-date information.  

In addition, the chatbot periodically scrapes data from drugs.com and provides links where users can find more detailed information about the medicine directly on the website.
</br></br></br>
![image](https://github.com/user-attachments/assets/b959fa41-cc7a-4e19-a96d-fa269efedcaa)
</br></br>

## Important API rules:
* You cannot directly give some information and request a medicine name.
* You'll need to give me the name of the medicine and ask questions about that medicine. (ex → When should I use Ibuprofen)

## Frameworks:
* Langchain
* FastAPI
* Uvicorn

## Running Steps:
* python run.py (the app must be in this address: http://127.0.0.1:8000/chat)
* streamlit run frontend. 

## Requirements  
- **Python Version**: 3.11.7  
- **Dependencies**: All required libraries and their respective versions are listed in the `requirements.txt` file. To install them, run the following command:  

  pip install -r requirements.txt

## Performance
GPT 4o-mini was faster but in terms of accuracy, GPT 4o was better. You can adjust the model from app/app.py line 10


## Special Thanks 🙏
Thank you to **FDA** for providing such a wonderful open-source API, and to **drugs.com** for gathering and sharing all of this valuable information💊
