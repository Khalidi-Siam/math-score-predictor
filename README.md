# Math Score Predictor

> An end-to-end machine learning project that predicts a student's math score based on demographic and academic features, served through a Django web interface.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Online-brightgreen)](https://math-score-predictor-f9xc.onrender.com/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-Web%20Framework-darkgreen)](https://www.djangoproject.com/)

---

## Table of Contents

- [Overview](#overview)
- [Live Demo](#live-demo)
- [Repository](#repository)
- [Project Structure](#project-structure)
- [ML Pipeline](#ml-pipeline)
- [Web Application](#web-application)
- [Getting Started](#getting-started)
- [Training the Model](#training-the-model)
- [Running the App](#running-the-app)
- [Troubleshooting](#troubleshooting)
- [Roadmap](#roadmap)

---

## Overview

This project covers the full lifecycle of a machine learning application — from exploratory data analysis and model training to deployment via a web interface. It trains and evaluates multiple regression algorithms on a student performance dataset, selects the best-performing model, and exposes it through a simple Django form for interactive inference.

**Key highlights:**

- Trains and tunes 8 regression models with GridSearchCV
- Automatically selects the best model by test R² score
- Persists the model and preprocessor as reusable `.pkl` artifacts
- Provides a clean web form for real-time math score prediction

---

## Live Demo

🔗 [https://math-score-predictor-f9xc.onrender.com/](https://math-score-predictor-f9xc.onrender.com/)

---

## Repository

🔗 [https://github.com/Khalidi-Siam/math-score-predictor](https://github.com/Khalidi-Siam/math-score-predictor)

---

## Project Structure

```
math-score-predictor/
├── ml_prediction_website/           # Django project root
│   ├── manage.py
│   ├── ml_prediction_website/       # Settings, URLs, WSGI config
│   ├── prediction/                  # App views and URL routes
│   └── templates/                   # HTML templates (index + result)
│
├── notebook/
│   ├── 1. EDA STUDENT PERFORMANCE.ipynb
│   ├── 2. MODEL TRAINING.ipynb
│   └── data/stud.csv                # Source dataset
│
├── src/
│   ├── components/
│   │   ├── data_ingestion.py        # Data loading and train/test split
│   │   ├── data_transformation.py  # Feature preprocessing pipeline
│   │   └── model_trainer.py        # Model training and evaluation
│   ├── pipeline/
│   │   ├── predict_pipeline.py      # Inference pipeline
│   │   └── train_pipeline.py        # End-to-end training pipeline entry point
│   ├── exception.py
│   ├── logger.py
│   └── utils.py
│
├── requirements.txt
├── setup.py
└── README.md
```

---

## ML Pipeline

### 1. Data Ingestion

- Reads `notebook/data/stud.csv`
- Splits into train and test sets
- Writes to `artifacts/train.csv`, `artifacts/test.csv`, `artifacts/data.csv`

### 2. Data Transformation

| Type | Features |
|------|----------|
| **Target** | `math_score` |
| **Numerical** | `writing_score`, `reading_score` |
| **Categorical** | `gender`, `race_ethnicity`, `parental_level_of_education`, `lunch`, `test_preparation_course` |

**Preprocessing steps:**

- **Numerical pipeline:** Median imputation → Standard scaling
- **Categorical pipeline:** Most-frequent imputation → One-hot encoding → Standard scaling
- Output: `artifacts/preprocessor.pkl`

### 3. Model Training

The following models are trained and tuned with GridSearchCV:

| Model |
|-------|
| Linear Regression |
| Decision Tree |
| Random Forest |
| Gradient Boosting |
| AdaBoost |
| K-Neighbors Regressor |
| XGBoost Regressor |
| CatBoost Regressor |

The model with the highest test R² score is saved to `artifacts/model.pkl`.

### 4. Inference

At prediction time, the pipeline loads `model.pkl` and `preprocessor.pkl`, transforms the incoming input, and returns the predicted math score.

- Artifacts are loaded once when the Django app imports the view module
- Artifact directory is configurable through environment variable `ML_ARTIFACT_DIR`
- Default artifact directory: `<project_root>/artifacts`

---

## Web Application

### Routes

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Renders the student input form |
| `POST` | `/result/` | Returns the predicted math score |

### Form Fields

| Field | Type | Values |
|-------|------|--------|
| `gender` | Select | `male`, `female` |
| `race_ethnicity` | Select | `group A` – `group E` |
| `parental_level_of_education` | Select | 6 education levels |
| `lunch` | Select | `standard`, `free/reduced` |
| `test_preparation_course` | Select | `none`, `completed` |
| `reading_score` | Integer | 0 – 100 |
| `writing_score` | Integer | 0 – 100 |

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/Khalidi-Siam/math-score-predictor.git
cd math-score-predictor
```

**2. Create and activate a virtual environment**

```bash
# macOS / Linux
python -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**3. Install dependencies**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Optionally, install the package in editable mode:

```bash
pip install -e .
```

---

## Training the Model

Run the following from the repository root to generate all artifacts:

```bash
python src/pipeline/train_pipeline.py
```

**Expected outputs:**

```
artifacts/
├── data.csv
├── train.csv
├── test.csv
├── preprocessor.pkl
└── model.pkl
```

---

## Running the App

Before starting the app, make sure training artifacts already exist (`model.pkl` and `preprocessor.pkl`).

**1. Navigate to the Django project directory**

```bash
cd ml_prediction_website
```

**2. Start the development server**

```bash
python manage.py runserver
```

**3. Open in your browser**

```
http://127.0.0.1:8000/
```

**Optional: override artifact directory**

If your artifacts are stored outside the default location, set `ML_ARTIFACT_DIR` before running the server.

```powershell
# Windows (PowerShell)
$env:ML_ARTIFACT_DIR = "D:\path\to\artifacts"
python manage.py runserver
```

```bash
# macOS / Linux
export ML_ARTIFACT_DIR="/path/to/artifacts"
python manage.py runserver
```

> **Note:** `ALLOWED_HOSTS` is set to `["*"]` for local/development use. Restrict this in production.

---

## Troubleshooting

**Prediction fails in the web app**
- Confirm that `artifacts/model.pkl` and `artifacts/preprocessor.pkl` exist
- Re-run training: `python src/pipeline/train_pipeline.py`

**Import errors on startup**
- Ensure you're running commands from the correct directory
- Verify the virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

**XGBoost or CatBoost installation fails**
- Upgrade pip and wheel first: `pip install --upgrade pip wheel`
- Retry: `pip install xgboost catboost`

---

## Roadmap

- [ ] Add unit and integration tests for the pipeline and Django views
- [ ] Expose a REST API endpoint for JSON-based prediction
- [ ] Integrate experiment tracking and model versioning (e.g., MLflow)
- [ ] Set up CI/CD pipeline (lint, test, build)
- [ ] Harden deployment configuration (restrict `ALLOWED_HOSTS`, use environment variables)

---

## Author

**Khalidi Siam**
- GitHub: [@Khalidi-Siam](https://github.com/Khalidi-Siam)
