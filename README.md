# Resume Modifier App

- This project is a full-stack, serverless web application that allows users to upload a resume and job description, and get a semantically improved version of their resume tailored to the job. It leverages **AWS SageMaker**, **Lambda**, **S3**, and **React**

# Features

- Upload `.txt` resume file
- Paste job description
- Automatically improve the resume using a **T5-based model**
- Full ML pipeline using **SageMaker + Serverless**
- Real-time inference via **API Gateway + Lambda**
- Secure S3 storage for uploads and outputs

# Architecture Overview

 text
Frontend (React)
    ↓
API Gateway
    ↓
Lambda (app.py)
    ↓
SageMaker Inference Endpoint (T5 Model)
    ↓
S3 Buckets (Raw + Improved Resumes)