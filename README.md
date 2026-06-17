# Credit Risk Modeling Classification App

This project is a machine learning credit risk assessment application. It trains a binary default-risk model in a Jupyter notebook, saves the production inference artifact, and exposes the model through a Streamlit web interface branded as **Kredix Finance**.

The app estimates:

- Default probability
- Credit score on a 300 to 900 scale
- Rating category: Poor, Average, Good, or Excellent
- Lending recommendation based on the rating

## Project Structure

```text
.
|-- README.md
|-- main.py
|-- prediction_helper.py
|-- credit_risk_model_codebasics.ipynb
|-- requirements.txt
`-- artifacts/
    `-- model_data.joblib
```

## Files

| File | Purpose |
| --- | --- |
| `main.py` | Streamlit application with the credit risk form, custom dark UI, score gauge, and recommendation display. |
| `prediction_helper.py` | Loads the saved model artifact, prepares user input, applies scaling, and returns prediction outputs. |
| `credit_risk_model_codebasics.ipynb` | End-to-end notebook for data loading, cleaning, EDA, feature engineering, model training, evaluation, and artifact export. |
| `artifacts/model_data.joblib` | Serialized model bundle used by the app. It contains the trained Logistic Regression model, scaler, selected feature list, and columns to scale. |
| `requirements.txt` | Python package dependencies for running the project. |

## Model Summary

The production artifact uses a **Logistic Regression** classifier. The notebook also experiments with Random Forest and XGBoost, but Logistic Regression is selected for the deployed artifact because it provides strong performance with better interpretability.

The saved model bundle contains:

- `model`: trained `LogisticRegression`
- `scaler`: fitted `MinMaxScaler`
- `features`: final 13 model input columns
- `cols_to_scale`: numeric columns required by the scaler

## Final Model Features

```text
age
loan_tenure_months
number_of_open_accounts
credit_utilization_ratio
loan_to_income
delinquency_ratio
avg_dpd_per_delinquency
residence_type_Owned
residence_type_Rented
loan_purpose_Education
loan_purpose_Home
loan_purpose_Personal
loan_type_Unsecured
```

## Training Workflow

The notebook follows this workflow:

1. Load customer, loan, and bureau datasets.
2. Merge datasets on `cust_id`.
3. Split into train and test sets before EDA to reduce leakage risk.
4. Clean missing values and duplicate records.
5. Remove invalid outliers using business rules.
6. Fix categorical value errors such as `Personaal` to `Personal`.
7. Perform EDA on numerical and categorical predictors.
8. Engineer risk features:
   - Loan to income ratio
   - Delinquency ratio
   - Average DPD per delinquency
9. Remove identifier, date, and business-excluded fields.
10. Scale numeric columns with `MinMaxScaler`.
11. Check multicollinearity using VIF.
12. Select features using Information Value.
13. Encode categorical features with one-hot encoding.
14. Train and compare Logistic Regression, Random Forest, and XGBoost.
15. Handle class imbalance using undersampling and SMOTE Tomek.
16. Tune models using RandomizedSearchCV and Optuna.
17. Evaluate using classification metrics, ROC-AUC, rank ordering, KS statistic, and Gini coefficient.
18. Save the final model bundle to `artifacts/model_data.joblib`.

Notebook evaluation for the selected Logistic Regression model reports:

- Accuracy: `0.93`
- Default-class precision: `0.57`
- Default-class recall: `0.94`
- Default-class F1-score: `0.71`
- ROC-AUC: `0.9837`
- Gini coefficient: `0.9673`

## App Inputs

The Streamlit app collects the following values:

| Input | Description |
| --- | --- |
| Age | Applicant age. |
| Income | Applicant income in rupees. |
| Loan Amount | Requested loan amount in rupees. |
| Loan Tenure | Loan duration in months. |
| Avg DPD | Average days past due per delinquency event. |
| Delinquency Ratio | Percentage of delinquent months. |
| Credit Utilization | Credit utilization percentage. |
| Open Loan Accounts | Number of open loan accounts. |
| Residence Type | Owned, Rented, or Mortgage. |
| Loan Purpose | Education, Home, Auto, or Personal. |
| Loan Type | Secured or Unsecured. |

`loan_to_income` is calculated automatically as:

```text
loan_amount / income
```

## App Outputs

After clicking **Calculate Credit Risk**, the app displays:

- **Default Probability**: predicted probability of default.
- **Credit Score**: score derived from non-default probability and scaled from 300 to 900.
- **Rating**:
  - `Poor`: 300 to 499
  - `Average`: 500 to 649
  - `Good`: 650 to 749
  - `Excellent`: 750 to 900
- **Recommendation**:
  - Good or Excellent: recommended for approval
  - Average: manual review required
  - Poor: not recommended

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit app:

```bash
streamlit run main.py
```

Then open the local URL shown by Streamlit, usually:

```text
http://localhost:8501
```

## Programmatic Prediction

You can call the prediction helper directly:

```python
from prediction_helper import predict

probability, credit_score, rating = predict(
    age=28,
    income=1200000,
    loan_amount=2560000,
    loan_tenure_months=36,
    avg_dpd_per_delinquency=20,
    delinquency_ratio=30,
    credit_utilization_ratio=30,
    num_open_accounts=2,
    residence_type="Owned",
    loan_purpose="Home",
    loan_type="Unsecured",
)

print(probability, credit_score, rating)
```

## Notes and Limitations

- The raw training datasets referenced by the notebook are expected at:
  - `dataset/customers.csv`
  - `dataset/loans.csv`
  - `dataset/bureau_data.csv`
- The `dataset/` directory is not present in the current repository snapshot, so the notebook cannot be fully rerun unless those files are added.
- The saved artifact was created with an older scikit-learn version than the currently pinned dependency. If you see an `InconsistentVersionWarning` while loading `model_data.joblib`, either use the original training version or regenerate the artifact with the installed dependency versions.
- Some fields required by the scaler but not exposed in the app are filled with dummy values in `prediction_helper.py`. The deployed prediction surface is therefore limited to the 13 final model features shown above.
- This project is for educational and prototyping use. A production credit decisioning system should include validation, monitoring, explainability, fairness checks, policy controls, and compliance review.
