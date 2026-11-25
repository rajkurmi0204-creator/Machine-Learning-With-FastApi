from fastapi import FastAPI
import joblib
import pandas as pd
from fastapi.responses import FileResponse
from pydantic import BaseModel

app= FastAPI()
model =joblib.load('model.pkl') # Load the untrained model

class job(BaseModel):
    title : str
    company_profile : str =""
    description : str =""
    requirements : str =""

    employment_type : str = 'unknown'
    required_experience : str = 'unknown'
    required_education : str = 'unknown'

    telecommuting : int 
    has_company_logo : int 
    has_questions : int 

@app.get("/")
def home():
    return FileResponse("index.html")

@app.post("/predict")
def predict(job: job):
    text = f"{job.title} {job.company_profile} {job.description} {job.requirements}"

    row = pd.DataFrame([{
        'text': text,
        'employment_type': job.employment_type,
        'required_experience': job.required_experience,
        'required_education': job.required_education,
        'telecommuting': job.telecommuting,
        'has_company_logo': job.has_company_logo,
        'has_questions': job.has_questions
    }])
    prob = float(model.predict_proba(row)[0][1])
    return {'fraudulent': int(prob > 0.5), 'probability': round(prob, 2)}