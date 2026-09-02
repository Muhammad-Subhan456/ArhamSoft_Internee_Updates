# Week 06 — First ML Pipeline

## Overview

This project builds a complete and reproducible machine learning pipeline using a synthetic student performance dataset.

The notebook moves from exploratory analysis into predictive modeling by establishing simple baselines first and then comparing them with **Linear Regression** for continuous prediction and **Logistic Regression** for binary classification.

The main goal is to evaluate models on unseen test data and use appropriate metrics to understand whether the trained models actually provide value beyond simple baseline predictions.

---

## Learning Objectives

By completing this project, the following concepts were practiced:

* Train/test splitting and evaluation on unseen data
* Reproducible machine learning workflows using fixed random seeds
* Regression and classification baselines
* One-hot encoding of categorical variables
* Linear Regression
* Logistic Regression
* RMSE and R² for regression
* Accuracy, Precision, Recall, and F1 score for classification
* Interpreting Linear Regression coefficients
* Understanding class imbalance and misleading accuracy
* Comparing real models against simple baselines

---

## Dataset

The notebook uses a synthetic `students` dataset containing **600 student observations**.

The dataset includes:

* `student_id`
* `class_section`
* `study_hours_per_week`
* `sleep_hours_per_night`
* `attendance_pct`
* `exam_score`

A binary `distinction` target is later created:

```python
students["distinction"] = (students["exam_score"] >= 85).astype(int)
```

The dataset is generated deterministically using a fixed random seed of `21`.

---

## Feature Engineering

The categorical `class_section` variable contains three categories:

* Section A
* Section B
* Section C

It is converted into numerical features using one-hot encoding with `drop_first=True`.

The final feature matrix contains:

* `study_hours_per_week`
* `sleep_hours_per_night`
* `attendance_pct`
* `class_section_B`
* `class_section_C`

Section A acts as the reference category.

---

## Machine Learning Pipeline

The notebook follows this workflow:

```text
Dataset Generation
       ↓
Feature Engineering
       ↓
Train/Test Split
       ↓
Regression Baseline
       ↓
Linear Regression
       ↓
Coefficient Interpretation
       ↓
Classification Target
       ↓
Stratified Train/Test Split
       ↓
Classification Baseline
       ↓
Logistic Regression
       ↓
Metric Comparison
       ↓
Reproducibility Check
```

---

## Regression

### Baseline

The regression baseline uses:

```python
DummyRegressor(strategy="mean")
```

The baseline predicts the mean training exam score for every test observation.

### Linear Regression

The real regression model uses:

```python
LinearRegression()
```

Performance is evaluated using:

* **RMSE** — measures prediction error in the same units as `exam_score`
* **R²** — measures how much variation in the target is explained relative to the mean-prediction baseline

### Results

| Model             |      RMSE |        R² |
| ----------------- | --------: | --------: |
| Mean Baseline     | 10.297789 | -0.009560 |
| Linear Regression |  7.058469 |  0.525687 |

Linear Regression reduced RMSE by **3.239320** and increased R² by **0.535247** compared with the baseline.

---

## Classification

A `distinction` target is created using an exam score threshold of 85:

```python
students["distinction"] = (students["exam_score"] >= 85).astype(int)
```

A fresh stratified train/test split is used to preserve the class proportions in both sets.

### Baseline

The classification baseline uses:

```python
DummyClassifier(strategy="most_frequent")
```

This model always predicts the majority class.

### Logistic Regression

The real classification model uses:

```python
LogisticRegression(
    random_state=42,
    max_iter=1000
)
```

Performance is evaluated using:

* **Accuracy**
* **Precision**
* **Recall**
* **F1 Score**

### Results

| Model                   | Accuracy | Precision |   Recall |       F1 |
| ----------------------- | -------: | --------: | -------: | -------: |
| Majority-Class Baseline | 0.650000 |  0.650000 | 1.000000 | 0.787879 |
| Logistic Regression     | 0.766667 |  0.812500 | 0.833333 | 0.822785 |

Logistic Regression improved accuracy by **0.116667**, precision by **0.162500**, and F1 by **0.034906**, while recall decreased by **0.166667**.

This demonstrates why accuracy should not be interpreted alone. The majority-class baseline can achieve reasonable accuracy simply by predicting the most common class, without learning meaningful distinctions between students.

---

## Coefficient Interpretation

The Linear Regression coefficients were examined alongside their corresponding feature names.

The analysis showed that `study_hours_per_week` had the strongest effect among the continuous predictors, consistent with the earlier correlation analysis against `exam_score`.

The section coefficients also capture differences relative to the omitted Section A reference category.

---

## Reproducibility

The notebook is designed to produce consistent results when executed from a fresh kernel.

Fixed seeds include:

```python
np.random.default_rng(seed=21)
```

and:

```python
train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)
```

The classification split additionally uses:

```python
stratify=y_classification
```

The final verification is performed by restarting the Jupyter kernel and running the notebook from top to bottom without manually reordering or rerunning cells.

---

## Project Structure

```text
Week-06/
│
├── ml_pipeline.ipynb
├── requirements.txt
└── README.md
```

---

## Requirements

Install the required Python packages with:

```bash
python -m pip install -r requirements.txt
```

Main libraries used:

* NumPy
* Pandas
* Scikit-learn
* Seaborn
* Matplotlib
* Jupyter
* IPython Kernel

---

## Key Takeaways

1. Models must be evaluated on **unseen test data**, not the training data.
2. A simple baseline provides the minimum performance a real model should beat.
3. Categorical variables can be converted into numerical features using **one-hot encoding**.
4. **Linear Regression** can model continuous outcomes and is evaluated using RMSE and R².
5. **Logistic Regression** can classify binary outcomes despite its name.
6. Accuracy can be misleading when the classes are imbalanced.
7. Precision, recall, and F1 provide additional information about classification performance.
8. Model coefficients can help interpret how features influence predictions.
9. Fixed random seeds and a top-to-bottom execution order make an ML notebook reproducible.
