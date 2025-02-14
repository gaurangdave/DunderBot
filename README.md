# DunderBot 🤖 – The Office RAG Application

![alt text](frontend/images/a299unbywmgz.jpg)

## 🎯 Project Goal
The goal of this project is to build an end-to-end application leveraging LLM-based RAG (Retrieval-Augmented Generation) techniques to create a chatbot that interacts with The Office dataset. Users can search for episodes, retrieve quotes, and ask contextual questions about the show.

This project involves:
1.	Retrieval Pipeline: Implement a pipeline to retrieve dialogs and metadata from a vector database based on user queries.
2.	Interactive Web Application:
*	Users can input a phrase or mood to retrieve relevant quotes from The Office.
*	Users can search for episodes or ask metadata-based questions (e.g., “Who directed the episode where Dwight started a fire?”).
3.	LLM Comparison: Incorporate a dropdown for users to compare responses generated by OpenAI, Ollama, Gemini, and DeepSeek.

## ✅ Solution Details

### 🧮 Performance Measure

### 🚧 Data Transformation

### 📂 Dataset

### 📒  Notebooks

### 🧠 Model Insights

## 💻 Tech Stack
![Python](https://img.shields.io/badge/Python-3.12.2-FFD43B?logo=Python&logoColor=blue&style=for-the-badge)  
![Pandas](https://img.shields.io/badge/Pandas-2.2.2-2C2D72?logo=Pandas&logoColor=2C2D72&style=for-the-badge)  
![Plotly](https://img.shields.io/badge/Plotly-5.24.1-239120?logo=Plotly&logoColor=239120&style=for-the-badge)  
![Scikit Learn](https://img.shields.io/badge/scikit_learn-1.5.1-F7931E?logo=scikit-learn&logoColor=F7931E&style=for-the-badge)  
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.12.0-FF6F00?logo=TensorFlow&logoColor=FF6F00&style=for-the-badge)  
![Google Colab](https://img.shields.io/badge/Notebook-Google_Colab-FCC624?logo=googlecolab&style=for-the-badge)  
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-109989?logo=Fastapi&logoColor=109989&style=for-the-badge)  

### 🛠️ Tools and Platforms:
1. **Python**: Used for preprocessing, pipeline development, and embedding generation.
2.	**FAISS**: For storing and retrieving dialog and metadata embeddings.
3.	**OpenAI, Ollama, Gemini, DeepSeek APIs**: For generating responses to user queries.
4.	**FastAPI**: Backend API for the application.
5.	**Next.js**: Frontend UI for user interaction.

## 💻 Running Locally

### Install Dependencies

- Create conda environment with `Python 3.12`

```bash
  conda create -n ml python=3.12
```

- Activate the environment

```bash
  conda activate ml
```

- Install ML Libraries

```bash
conda install numpy pandas scikit-learn matplotlib seaborn plotly jupyter ipykernel -y
```

```bash
conda install -c conda-forge python-kaleido
```

- Install GDown
```bash
conda install conda-forge::gdown
```

- Install DotEnv
```bash
conda install conda-forge::python-dotenv
```

- Install FastAPI

```bash
conda install -c conda-forge fastapi uvicorn -y
```
### Training Model for API

* Run the following command to train model(s) for production use

```bash
python -m scripts.training
```

### Running the API
* Run the following command to start the API server

```bash
uvicorn api.main:app --reload
```

* Go to the following URL to access API Docs
```URL
http://localhost:8000/docs
```

### Running API Test Cases
* Run the following command to run all the test cases
```bash
pytest
```

* Run the following command to run a specific test case
  * Here `TBD` is the name of test case in `tests/test_api.py` file.
```bash
pytest -k TBD
```

### API Reference

| Action                                           | HTTP Method | Endpoint                                 |
|--------------------------------------------------|-------------|------------------------------------------|
| TBD                            | **`POST`**  | `/TBD`                               |

### Accessing UI

* To access the UI application, simply go to `http://localhost:8000` after starting the server and you should be able to access the webapp. 

### App Screenshots

#### Default Home Page

#### Prediction

## 📈 Visualizations

## 📊 Project Insights

### 👣 Next Steps

## 🏫 Lessons Learnt
    
## 🌟 Project Highlights

## 🚀 About Me

A jack of all trades in software engineering, with 15 years of crafting full-stack solutions, scalable architectures, and pixel-perfect designs. Now expanding my horizons into AI/ML, blending experience with curiosity to build the future of tech—one model at a time.

## 🔗 Links

[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://gaurangdave.me/)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/gaurangvdave/)

## 🛠 Skills

`Python`, `Jupyter Notebook`, `scikit-learn`, `FastAPI`, `Plotly`, `Conda`
