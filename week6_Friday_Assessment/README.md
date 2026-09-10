# Week 06 Assessment — ML Pipeline Practical

A complete machine-learning classification pipeline for predicting loan defaults using a synthetic dataset.

## Overview

This project demonstrates an end-to-end machine-learning workflow covering:

- Dataset generation and validation
- Data diagnosis and visualization
- Feature construction
- Train/test splitting
- Train-only missing-value imputation
- Baseline modeling
- Logistic Regression
- Decision Tree
- Random Forest
- Hyperparameter tuning
- Model evaluation
- Error analysis
- Probability calibration
- Evaluation reporting
- Written defense preparation

The assessment focuses on model performance, data-leakage prevention, and the ability to justify modeling decisions.

## Problem Statement

The goal is to predict whether a loan applicant will default.

- `default = 1` → Applicant defaults
- `default = 0` → Applicant does not default

The synthetic dataset contains 1,200 loan applications.

| Feature | Description |
|---|---|
| `applicant_id` | Unique applicant identifier |
| `employment_type` | Employment category |
| `credit_score` | Applicant credit score |
| `applicant_income` | Applicant income |
| `loan_amount` | Requested loan amount |
| `default` | Target variable |

There are exactly 90 missing `credit_score` values.

## Machine Learning Pipeline

```text
Dataset Generation
        ↓
Dataset Validation
        ↓
Data Diagnosis
        ↓
Feature Construction
        ↓
Train/Test Split
        ↓
Train-only Imputation
        ↓
Baseline
        ↓
Model Training
        ↓
Hyperparameter Tuning
        ↓
Test-set Evaluation
        ↓
Model Comparison
        ↓
Final Model Selection
        ↓
Error Analysis
        ↓
Calibration Analysis
        ↓
Required Artifacts
```

## Feature Construction

The predictors are:

```text
credit_score
applicant_income
loan_amount
employment_type
```

`employment_type` is one-hot encoded using:

```python
pd.get_dummies(
    X,
    columns=["employment_type"],
    drop_first=True
)
```

## Train/Test Split

The data is split before missing-value imputation:

```python
train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)
```

This produces an 80/20 stratified train/test split.

## Missing-Value Handling

The `credit_score` imputation value is calculated using only the training set:

```python
credit_score_imputation_value = X_train["credit_score"].median()
```

The same training-derived value is then applied to both `X_train` and `X_test`.

Using the full dataset before splitting would allow information from the held-out test set to influence preprocessing and would constitute data leakage.

## Models

Four models are evaluated:

1. **Baseline** — `DummyClassifier(strategy="most_frequent")`
2. **Logistic Regression** — scaled linear classifier
3. **Decision Tree** — non-linear tree-based classifier
4. **Random Forest** — ensemble of decision trees

## Hyperparameter Tuning

The machine-learning models are tuned using `GridSearchCV` with 5-fold cross-validation.

The tuning objective is **F1 score**.

The held-out test set is not used for hyperparameter selection. After tuning, each best estimator is evaluated on the untouched test set.

## Evaluation Metrics

Every model, including the baseline, is evaluated using:

- **Accuracy** — overall proportion of correct predictions.
- **Precision** — proportion of predicted defaults that were actually defaults.
- **Recall** — proportion of actual defaults correctly identified.
- **F1** — harmonic mean of precision and recall.
- **ROC-AUC** — ability to distinguish and rank default versus non-default cases across thresholds.

## Final Model

The selected final model is:

```text
Random Forest
```

Final held-out test-set performance:

| Metric | Score |
|---|---:|
| Accuracy | 0.7708 |
| Precision | 0.7834 |
| Recall | 0.8542 |
| F1 | 0.8173 |
| ROC-AUC | 0.8541 |

Random Forest was selected because it achieved the strongest overall held-out test performance among the trained machine-learning models. The selection was not based on accuracy alone.

## Model Comparison

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Baseline | 0.6000 | 0.6000 | 1.0000 | 0.7500 | 0.5000 |
| Logistic Regression | 0.7458 | 0.7677 | 0.8264 | 0.7960 | 0.8454 |
| Decision Tree | 0.7292 | 0.7651 | 0.7917 | 0.7782 | 0.8258 |
| Random Forest | **0.7708** | **0.7834** | **0.8542** | **0.8173** | **0.8541** |

The baseline's recall of 1.0 is not evidence of strong predictive performance because it predicts the majority class for every applicant. Its ROC-AUC of 0.5 indicates no useful ranking ability.

## Error Analysis

The final Random Forest is analyzed on the held-out test set.

Errors are separated into:

- **False Positive** — predicted default, but actual outcome was no default.
- **False Negative** — predicted no default, but actual outcome was default.

The analysis examines:

- Misclassified applicants
- Numerical feature characteristics
- Employment type
- Predicted default probabilities
- Overall error patterns

False negatives are particularly important because they represent actual defaulters that the model failed to identify.

Observed patterns are treated as characteristics of the test sample, not causal conclusions.

## Calibration Analysis

A calibration curve is generated for the final Random Forest.

Calibration evaluates whether predicted probabilities correspond to observed default frequencies.

```text
ROC-AUC
→ How well can the model rank/separate cases?

Calibration
→ Can predicted probabilities be interpreted as actual risk?
```

Strong ROC-AUC does not automatically imply well-calibrated probabilities.

The model's probabilities should therefore not automatically be used for real-world risk-based interest-rate decisions without additional calibration and production validation.

## Required Output Files

The assessment produces:

```text
model_metrics.json
chart_model_comparison.png
chart_calibration.png
evaluation_report.md
defense_answers.md
```

### `model_metrics.json`

Contains `accuracy`, `precision`, `recall`, `f1`, and `roc_auc` as plain floats for all four models, plus:

- `credit_score_imputation_value`
- `final_model`

### `chart_model_comparison.png`

Compares the four models using the selected evaluation metrics.

### `chart_calibration.png`

Shows the calibration curve for the final Random Forest.

### `evaluation_report.md`

A standalone report covering the task, baseline, model comparison, final model selection and justification, error analysis, calibration, and one honest limitation.

### `defense_answers.md`

Contains answers to the five assessment defense questions using the actual experiment results.

## Installation

Create and activate a virtual environment.

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Notebook

Start Jupyter Lab:

```bash
jupyter lab
```

Open the assessment notebook and run the cells from top to bottom.

The notebook should be executed in order because later sections depend on variables and models created earlier.

## Requirements

The project uses:

- NumPy
- Pandas
- Matplotlib
- Scikit-learn
- IPython
- JupyterLab
- IPyKernel

See `requirements.txt` for the complete dependency list.

## Reproducibility

Fixed random states are used throughout the assessment.

Dataset generation:

```python
seed=55
```

Train/test split:

```python
random_state=42
```

Model random states are also fixed where applicable.

## Data Leakage Prevention

The pipeline follows these principles:

1. Construct features.
2. Split into training and test sets.
3. Calculate the credit-score imputation value from training data only.
4. Apply that fixed value to both training and test data.
5. Perform hyperparameter tuning using training data only.
6. Evaluate final models on the held-out test set.

The test set is therefore kept separate from preprocessing-statistic calculation, model fitting, and hyperparameter selection.

## Limitations

This project uses a synthetic dataset with a limited number of applicant features.

Important real-world lending information is missing, such as existing debt obligations and debt-to-income ratio. Without this information, the model has an incomplete view of an applicant's repayment capacity.

Strong performance on this synthetic test set does not guarantee similar performance on real-world lending data.

Therefore, the model should be treated as an assessment pipeline rather than a production-ready lending decision system.

## Assessment Defense

The written defense addresses:

1. Why Random Forest was selected instead of automatically choosing Logistic Regression.
2. Why imputation must use training data only.
3. Why recall on the default class is important.
4. Why calibration matters when interpreting predicted probabilities.
5. Which important real-world factor is missing from the pipeline.

## Self-Check

Run the provided structural test with:

```bash
pytest test_friday_sample.py
```

A passing self-check confirms that the required files and their basic structure are present.

It does not guarantee that:

- Data leakage was avoided
- Models genuinely outperform the baseline
- The final model choice is justified
- Error analysis is meaningful
- Calibration analysis is correct
- The written defense is strong

These aspects require inspection of the notebook and the reasoning behind the implementation.

## Conclusion

This assessment demonstrates a complete supervised machine-learning workflow for loan-default prediction, from dataset generation and preprocessing through model tuning, evaluation, error analysis, calibration, and final reporting.

The final selected model is a tuned Random Forest based on its strongest overall held-out test-set performance.
