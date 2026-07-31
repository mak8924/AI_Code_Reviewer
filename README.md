# 🛡️ AI Code Reviewer | Automated Software Defect Prediction & Code Analysis

An intelligent Decision Support System (DSS) built with **Streamlit**, **Machine Learning** (Gradient Boosting), and **Generative AI** (Google Gemini). The system predicts potential software defects based on Software Metrics from NASA's **JM1 dataset** and provides real-time automated code reviews, bug fixes, and technical explanations.

---

## 📌 Table of Contents
- [About The Project](#-about-the-project)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Model Performance](#-model-performance)
- [Local Setup & Installation](#-local-setup--installation)
- [Secrets Configuration](#-secrets-configuration)
- [Cloud Deployment (Streamlit Cloud)](#-cloud-deployment-streamlit-cloud)

---

## 📝 About The Project
This project provides an end-to-end technical solution combining **Classical Machine Learning** to estimate software defect probabilities from software metrics (such as McCabe complexity and Halstead measures) and **Generative AI (Gemini AI)** to deliver context-aware code analysis, vulnerability checks, and automated fixes.

---

## ✨ Key Features
* **Software Defect Prediction:** Predicts whether a code module is defective based on statistical software metrics.
* **AI Code Reviewer (Gemini Helper):** Real-time code analysis, vulnerability scanning, and fix recommendations with streaming AI responses.
* **Inspection History Tracker:** Saves and manages full analysis logs locally (`history.json`) for easy lookup.
* **Model Performance Dashboard:** Interactive evaluation metrics including Confusion Matrix, ROC-AUC Curve, and Class Distribution visualizations.
* **Custom Dark Mode UI:** Modern, responsive interface styled with custom CSS stylesheets built on Streamlit.

---

## 🛠️ Tech Stack

### 1. Frameworks & Programming Languages
* **Python 3.10+**: Core programming language.
* **Streamlit**: Web application framework for multi-page UI development.

### 2. Machine Learning & Data Processing
* **Scikit-Learn**: Model building, hyperparameter tuning, and evaluation metrics.
* **Pandas & NumPy**: Data processing, transformation, and matrix computations.
* **Joblib**: Model serialization and loading (`.pkl`).

### 3. Generative AI
* **Google Generative AI (`google-generativeai`)**: Integration with Gemini AI for code review and explanation generation.

### 4. Data Visualization
* **Plotly**: Interactive dashboards (Confusion Matrix, ROC Curve, Class Distribution).
* **Matplotlib & Seaborn**: Static plots and EDA reporting.

---

## 📐 Project Structure

```text
AI_Code_Reviewer/
│
├── assets/
│   └── style.css                        # Custom UI stylesheet
│
├── data/
│   ├── about JM1 Dataset.txt            # JM1 dataset documentation
│   ├── archive.zip                      # Zipped raw data archive
│   ├── history.json                     # Local storage for review history logs
│   ├── jm1.arff                         # ARFF dataset file
│   └── jm1.csv                          # CSV dataset file
│
├── models/
│   └── gradient_boosting_model.pkl      # Trained Gradient Boosting model artifact
│
├── notebooks/
│   └── describe_dataset.ipynb          # Exploratory Data Analysis (EDA) notebook
│
├── pages/
│   ├── 1_Model_Performance.py           # Performance dashboard page
│   └── 2_History.py                     # Historical inspection logs page
│
├── reports/                             # Generated training plots and evaluation figures
│   ├── comprehensive_pairplot.png
│   ├── ConfusionMatrix_Gradient Boosting (Tuned).png
│   ├── ConfusionMatrix_Random Forest (Tuned).png
│   ├── ConfusionMatrix_TF.png
│   ├── correlation_heatmap.png
│   ├── defects_distribution.png
│   ├── gb_tuned_metrics.png
│   ├── loc_distribution_histogram.png
│   ├── loc_vs_complexity_scatter.png
│   ├── metrics_boxplots.png
│   └── uniq_operators_violin.png
│
├── src/                                 # Source modules
│   ├── gemini_helper.py                 # Gemini AI integration service
│   ├── history_helper.py                # History storage and logging logic
│   ├── model_helper.py                  # Model loading and prediction pipeline
│   └── utils.py                         # Helper utilities
│
├── .gitignore                           # Git ignore rules
├── app.py                               # Main Streamlit application entry point
├── README.md                            # Project documentation
├── requirements.txt                     # Project dependencies
└── runtime.txt                          # Python runtime version configuration
```

---

## 📊 Model Performance

The **Gradient Boosting (Tuned)** model was selected after dataset balancing and hyperparameter optimization on the **JM1 dataset**:

| Algorithm | Accuracy | F1_Score | Recall | Precision | ROC_AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Gradient Boosting (Tuned)** | `0.698070` | `0.457473` | `0.657957` | `0.350633` | **`0.738307`** |

---

## 🚀 Local Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/mak8924/AI_Code_Reviewer.git
cd AI_Code_Reviewer
```

### 2. Create and Activate Virtual Environment

* **On Windows:**
```bash
python -m venv my_venv_ACR
my_venv_ACR\Scripts\activate
```

* **On Linux / macOS:**
```bash
python3 -m venv my_venv_ACR
source my_venv_ACR/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🔑 Secrets Configuration

Create a folder named `.streamlit` in the project root directory, and add a `secrets.toml` file containing your Gemini API key:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
```

### 4. Run the Streamlit Application
```bash
streamlit run app.py
```

---

## ☁️ Cloud Deployment (Streamlit Cloud)

To deploy the application on **Streamlit Community Cloud**:

1. **Push Code to GitHub:**
   * Push all project files to a GitHub repository.
   * **Security Notice:** Ensure `.streamlit/secrets.toml` is listed in your `.gitignore` to prevent API key leaks.

2. **Configure `runtime.txt`:**
   * Ensure `runtime.txt` specifies the correct Python environment:
     ```text
     python-3.10
     ```

3. **Deploy on Streamlit Cloud:**
   * Sign in to [Streamlit Community Cloud](https://share.streamlit.io/).
   * Click **Create app** and select your repository and `main` branch.
   * Set the **Main file path** to `app.py`.

4. **Add Environment Secrets:**
   * Before deploying, open **Advanced settings**.
   * Under **Secrets**, paste your API key configuration:
     ```toml
     GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
     ```
   * Click **Save** and then **Deploy**.