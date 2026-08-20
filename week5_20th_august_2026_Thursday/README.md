# Week 5 — EDA Integration Assignment

This project contains the Week 5 EDA integration assignment. The objective was to perform a complete exploratory data analysis pipeline on a new, intentionally imperfect orders dataset.

The workflow follows:

**Generate → Diagnose → Clean → Verify → Visualize → Summarize → Review**

The assignment was completed using a feature branch and submitted through a Pull Request.

---

## Project Structure

```text
week5_20th_august_2026_Thursday/
│
├── venv/                       # Local virtual environment (not committed)
├── week5_thursday_eda.ipynb    # Complete EDA notebook
├── technical_summary.md        # Standalone technical summary
├── self_review.md              # Final self-review checklist
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```

## Prerequisites

Make sure Python 3 is installed.

```powershell
python --version
```

## 1. Create the Virtual Environment

```powershell
python -m venv venv
```

Project files remain outside `venv`.

## 2. Activate the Virtual Environment

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Verify the Python executable:

```powershell
python -c "import sys; print(sys.executable)"
```

It should point to the project's `venv`.

## 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

Dependencies:

- NumPy — numerical operations and dataset generation
- Pandas — data manipulation, cleaning, aggregation, and analysis
- Matplotlib — data visualization
- JupyterLab — notebook environment
- IPykernel — Jupyter kernel integration

## 4. Register the Virtual Environment with Jupyter

```powershell
python -m ipykernel install --user --name week5-thursday-eda --display-name "Python (Week 5 Thursday EDA)"
```

## 5. Launch JupyterLab

```powershell
jupyter lab
```

Open `week5_thursday_eda.ipynb` and select the **Python (Week 5 Thursday EDA)** kernel.

## 6. Verify the Environment

```python
import sys
import numpy as np
import pandas as pd
import matplotlib

print("Python:", sys.executable)
print("NumPy:", np.__version__)
print("Pandas:", pd.__version__)
print("Matplotlib:", matplotlib.__version__)
```

---

# Assignment Overview

The assignment required a complete EDA pipeline on a dataset generated from the exact provided specification.

The dataset contains:

- Order ID
- Order date
- Customer ID
- Product category
- Quantity
- Unit price
- Region

The original dataset contains **5,015 rows and 7 columns**. The additional 15 rows are intentionally introduced duplicate records.

# EDA Pipeline

## 1. Dataset Generation

The dataset was generated using the exact specification provided by the assignment and verified with:

```python
orders.shape
orders.head()
```

Expected shape:

```text
(5015, 7)
```

No cleaning was performed during generation.

## 2. Diagnosis

The raw dataset was diagnosed before applying any cleaning operation.

Diagnostics included:

```python
orders.head()
orders.info()
orders.describe()
orders.isna().sum()
orders["product_category"].value_counts(dropna=False)
orders["region"].value_counts(dropna=False)
```

Additional checks covered negative quantities, extreme unit prices, duplicate rows, duplicate order IDs, and the order-date range.

The following data-quality issues were identified:

1. Missing `customer_id`
2. Missing `region`
3. Inconsistent capitalization in `product_category`
4. Negative `quantity` values
5. Extreme `unit_price` values
6. Duplicate records

## 3. Cleaning Decisions

Each issue was handled independently rather than applying a blanket cleaning operation.

### Missing `customer_id`

Records with missing customer identifiers were removed because a customer ID cannot be reliably inferred without creating an incorrect identity.

### Missing `region`

Missing regions were replaced with `Unknown`. This preserves otherwise useful order information without making an unsupported geographical assumption.

### Inconsistent Product Categories

Product category values were standardized to lowercase so that `Electronics` and `electronics` are treated as the same category.

### Negative Quantities

Negative quantities represented returns. A separate `is_return` indicator was created to preserve this information, and the quantity was converted to its absolute value.

### Extreme Unit Prices

The intentionally introduced extreme unit-price values were treated as data-entry outliers and removed rather than replaced with fabricated mean or median values.

### Duplicate Records

Exact duplicate rows were removed because they do not represent additional orders and could distort aggregate analysis.

# Visualization

The cleaned dataset was analyzed using deliberately selected visualizations.

## 1. Unit Price Distribution

A histogram was used to examine how unit prices are distributed across the cleaned orders.

## 2. Product Category Comparison

A bar chart was used to compare total quantity across product categories.

```python
cleaned_orders.groupby("product_category")["quantity"].sum()
```

## 3. Quantity vs Unit Price

A scatter plot was used to investigate the relationship between quantity and unit price.

The Pearson correlation calculated for the cleaned dataset was approximately:

```text
-0.009
```

This indicates a negligible linear association and should not be interpreted as evidence of causation.

## 4. Regional Comparison

A bar chart was also used to compare order counts across regions. The `Unknown` category was retained for records with missing original region information.

# Findings

The final notebook contains evidence-backed findings based on the generated charts and numerical analysis.

The main analytical observations include:

- The cleaned unit-price distribution is more representative after removing the intentionally introduced extreme price values.
- Product categories can be compared using their aggregated total quantities.
- Quantity and unit price show a negligible linear association, with a Pearson correlation of approximately `-0.009`.
- Missing regional information is retained explicitly as `Unknown` rather than being silently discarded.

# Technical Summary

A separate technical summary is provided in `technical_summary.md` and contains the dataset overview, data-quality handling, key findings, limitations, and conclusion.

# Reproducibility

The notebook was tested from a completely fresh Jupyter kernel using:

```text
Kernel → Restart Kernel → Run All
```

The notebook successfully executes in top-to-bottom order without relying on hidden Jupyter state.

# Git Workflow

The assignment was completed using the feature branch:

```text
feature/week5-eda
```

Work was committed incrementally rather than as one large commit. The feature branch was pushed to GitHub and a Pull Request was opened for review.

# Self Review

The final self-review is documented in `self_review.md`. It confirms that the dataset generation, diagnosis, cleaning, visualization, findings, technical summary, reproducibility test, feature branch, incremental commits, and Pull Request requirements were completed.

# Git and Virtual Environment

The virtual environment should **not** be committed to Git. The repository uses:

```gitignore
venv/
```

to exclude it.

To recreate the environment on another machine:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m ipykernel install --user --name week5-thursday-eda --display-name "Python (Week 5 Thursday EDA)"
jupyter lab
```

## Deactivate the Environment

```powershell
deactivate
```

# Assignment Status

**Completed**

The Week 5 EDA integration assignment has been completed, self-reviewed, pushed through a feature branch, and submitted through a Pull Request for review.
