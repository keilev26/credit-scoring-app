# Credit Scoring App 🏦

A full-stack machine learning application that predicts loan default risk. Given a borrower's financial profile, the model outputs a binary prediction (default / no default) along with a probability score.

> 📓 **Google Colab Notebook:** [View the full ML experimentation here](https://colab.research.google.com/drive/1oKnkHgDUqf8-FFy9wd7WSSDROIIb7hId?usp=sharing)

---

## What this project does

Banks and lenders need to assess whether a borrower is likely to repay a loan. This app automates that assessment: you submit loan details and borrower information through a web form or API call, and the system returns a credit risk prediction in real time.

---

## Results ✅

| Metric | Score |
|--------|-------|
| ROC-AUC | **0.7346** |

A ROC-AUC of 0.7346 is a strong result for credit scoring datasets, which are notoriously difficult due to class imbalance (most borrowers do repay), noisy financial features, and the inherent unpredictability of human behavior.

---

## Tech stack

| Layer | Technology |
|-------|------------|
| ML model | LightGBM + scikit-learn StandardScaler |
| Data processing | pandas, numpy |
| API | FastAPI (Python) |
| Frontend | HTML, CSS, JavaScript |
| Experimentation | Google Colab |
| Model serving | pickle (.pkl) |

---

## Machine learning pipeline

### 1. Data analysis and preprocessing
Applied pandas with analytical criteria to clean, explore, and engineer features from the **LendingClub dataset** (500,000 records, 2007–2018). This included handling missing values, encoding categorical variables (loan grade, home ownership, verification status, purpose), and scaling numeric features.

### 2. Feature engineering
The final model consumes 29 features. Categorical fields are one-hot encoded; the loan sub-grade (A1–G5) is mapped to an ordered numeric scale (1–35) to preserve its ordinal meaning.

### 3. Model comparison 🔬
Four models were trained and evaluated on the same train/test split. All used class imbalance handling strategies given the skewed target distribution (most borrowers repay):

| Model | ROC-AUC | Notes |
|-------|---------|-------|
| Logistic Regression | 0.7284 | Baseline |
| Logistic Regression (balanced weights) | 0.7286 | `class_weight="balanced"` |
| Random Forest | 0.7309 | 200 trees, max depth 10 |
| XGBoost | 0.7256 | `scale_pos_weight` for imbalance |
| **LightGBM** ✅ | **0.7346** | **Selected — best ROC-AUC** |

**LightGBM** was selected as the final model for its superior ROC-AUC and efficient handling of the imbalanced dataset (`is_unbalance=True`, 300 estimators, learning rate 0.05).

### 4. Model serialization
Both the fitted scaler and classifier are saved as `.pkl` files and loaded once at API startup.

---

## Project structure

```
backend/
├── main.py                    # FastAPI app, model loading, routes
├── models/
│   ├── request_models.py      # Pydantic input schema (ClienteIn)
│   └── response_models.py     # Pydantic output schema (ResponseOut)
├── services/
│   └── preprocess.py          # Builds the 29-feature vector
├── utils/
│   └── subgrade_mapper.py     # Sub-grade string → numeric encoding
├── feature_names.json         # Raw input field names
├── modelo_credit_scoring.pkl  # Trained classifier
└── scaler_credit_scoring.pkl  # Fitted StandardScaler
```

---

## Running the app

```bash
source ~/proyects/fastAPI/fastapi-env/bin/activate
cd backend
uvicorn main:app --reload
```

Then open `http://localhost:8000` in your browser, or send a `POST /predict/` request with a JSON body matching the `ClienteIn` schema.

---

## Input fields

| Field | Type | Description |
|-------|------|-------------|
| `loan_amnt` | float | Requested loan amount |
| `term` | int | Loan term in months |
| `int_rate` | float | Interest rate (%) |
| `installment` | float | Monthly payment amount |
| `sub_grade` | string | Loan sub-grade (A1–G5) |
| `emp_length` | float | Employment length in years |
| `home_ownership` | string | OWN / RENT / OTHER |
| `annual_inc` | float | Annual income |
| `verification_status` | string | Source Verified / Verified / Not Verified |
| `purpose` | string | Loan purpose (e.g. debt_consolidation) |
| `dti` | float | Debt-to-income ratio |
| `open_acc` | float | Number of open credit lines |
| `pub_rec` | float | Number of derogatory public records |
| `revol_bal` | float | Total revolving balance |
| `revol_util` | float | Revolving utilization rate (%) |
| `total_acc` | float | Total credit lines |
| `mort_acc` | float | Number of mortgage accounts |
| `pub_rec_bankruptcies` | float | Number of public record bankruptcies |
