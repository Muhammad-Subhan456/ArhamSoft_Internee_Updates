# Week 05 Assessment — EDA Practical

## Overview

This project contains the Week 05 EDA assessment based on an intentionally imperfect support-ticket dataset.

The assessment demonstrates a complete Exploratory Data Analysis (EDA) workflow:

**Dataset Generation → Diagnosis → Cleaning → Verification → Visualization → Findings → Technical Summary**

The dataset contains intentionally introduced data-quality issues such as missing values, inconsistent categories, invalid values, outliers, and duplicate records.

---

## Project Structure

week5_assessment/
│
├── venv/                         # Local virtual environment (not committed)
├── assessment.ipynb              # Main EDA notebook
├── technical_summary.md          # Technical summary
├── test_friday_sample.py         # Sample validation tests
├── tickets_clean.csv             # Cleaned dataset
├── findings.json                 # Raw diagnosis results
├── chart_distribution.png        # Resolution-time distribution
├── chart_category_comparison.png # Average resolution by priority
└── chart_relationship.png        # Ticket ID vs resolution time

---

## Dataset

The dataset contains support-ticket information with the following columns:

| Column             | Description                                  |
| ------------------ | -------------------------------------------- |
| `ticket_id`        | Unique support-ticket identifier             |
| `created_at`       | Ticket creation timestamp                    |
| `agent_id`         | Assigned support-agent identifier            |
| `priority`         | Ticket priority                              |
| `resolution_hours` | Ticket resolution duration                   |
| `channel`          | Channel through which the ticket was created |

The raw dataset contains **4,012 rows and 6 columns**.

---

## Data-Quality Issues Identified

The diagnosis was performed before any cleaning.

The following issues were identified:

* **121** missing `agent_id` values
* **193** missing `channel` values
* **12** duplicate rows
* **25** negative `resolution_hours` values
* **15** extreme `resolution_hours` values of `999.0`
* Inconsistent priority capitalization: `High` and `high`

---

## Cleaning Decisions

Each data-quality issue was handled separately.

### Missing `agent_id`

Rows with missing `agent_id` values were removed because the responsible agent could not be reliably inferred from the available data.

### Missing `channel`

Missing channel values were replaced with `Unknown` because the ticket remains useful for analysis even when its communication channel is unavailable.

### Inconsistent `priority`

Priority values were standardized using consistent capitalization so that `High` and `high` represent the same category.

### Negative `resolution_hours`

Negative resolution durations were removed because a standard ticket resolution time cannot be negative and the correct value cannot be reliably reconstructed from the available data.

### Extreme `resolution_hours`

The `999.0` values were treated as data-entry outliers.

Instead of removing the affected tickets, the outlier values were replaced with the **median of the valid resolution times**. The median was selected because resolution times are right-skewed and the median is less sensitive to extreme values than the mean.

### Duplicate Rows

Exact duplicate records were removed to prevent the same ticket observation from being counted more than once.

---

## Final Cleaned Dataset

After cleaning, the resulting dataset contains:

3856 rows × 6 columns

The cleaned dataset contains:

* No missing values
* No duplicate rows
* No negative resolution times
* No remaining `999.0` outliers
* Standardized priority categories

---

## Visualizations

Three required visualizations were created:

1. `chart_distribution.png` — Resolution-time distribution
2. `chart_category_comparison.png` — Average resolution time by priority
3. `chart_relationship.png` — Ticket ID vs resolution time

---

## Key Findings

### Overall Resolution Time

The cleaned dataset has an average resolution time of approximately **12.04 hours**, while the median is **10.24 hours**.

The difference between the mean and median indicates that the resolution-time distribution is somewhat right-skewed.

### Resolution Time by Priority

Average resolution time varies moderately across priority levels:

| Priority | Average Resolution Time |
| -------- | ----------------------: |
| Low      |             12.19 hours |
| High     |             12.13 hours |
| Medium   |             11.70 hours |

Low-priority tickets have the highest average resolution time among the three categories.

### Resolution-Time Range

After cleaning, resolution times range from approximately **0.10 to 62.03 hours**.

---

## Output Files

The assessment produces the following required files:

tickets_clean.csv
findings.json
chart_distribution.png
chart_category_comparison.png
chart_relationship.png

The `findings.json` file contains diagnosis results calculated from the raw dataset before cleaning:

{
"missing_agent_id": 121,
"missing_channel": 193,
"duplicate_rows": 12,
"negative_resolution_hours": 25,
"outlier_resolution_hours": 15
}

---

## Requirements

The project uses:

* Python
* NumPy
* Pandas
* Matplotlib
* JupyterLab
* IPykernel
* Pytest

Install dependencies with:

pip install -r requirements.txt

---

## Setup

### 1. Create a Virtual Environment

python -m venv venv

### 2. Activate the Virtual Environment

#### Windows PowerShell

.\venv\Scripts\Activate.ps1

#### Windows Command Prompt

venv\Scripts\activate

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Register the Jupyter Kernel

python -m ipykernel install --user --name week5-assessment --display-name "Python (Week 5 Assessment)"

### 5. Launch JupyterLab

jupyter lab

Open `assessment.ipynb` and select the **Python (Week 5 Assessment)** kernel.

---

## Running the Assessment

The notebook should be executed from top to bottom.

Recommended workflow:

1. Generate the exact dataset.
2. Confirm the dataset structure.
3. Diagnose the raw dataset.
4. Document the diagnosis.
5. Create a copy of the raw dataset.
6. Apply the documented cleaning decisions.
7. Verify the cleaned dataset.
8. Export `tickets_clean.csv`.
9. Export `findings.json`.
10. Generate and save the three required charts.
11. Review the findings.
12. Review the technical summary.
13. Run the provided sample tests.
14. Restart the kernel and run all cells again.

---

## Validation

The provided sample tests can be executed using:

pytest test_friday_sample.py

The tests verify that:

* `tickets_clean.csv` contains the required columns.
* `findings.json` contains the required keys with integer values.
* All three required chart files exist and are non-empty.

The sample tests verify the structure of the submission but do not replace manual review of the data-cleaning decisions and analytical findings.

---

## Reproducibility

The notebook should successfully execute using:

**Restart Kernel → Run All**

The virtual environment is intentionally excluded from version control.

The environment can be recreated from:

requirements.txt

This allows another person to clone the repository and reproduce the analysis without needing the original local Python environment.

---

## Limitation

The dataset is artificially generated for assessment purposes and may not represent real-world support-ticket behavior.

Additionally, variables such as issue complexity, agent experience, ticket subject, and customer characteristics are not available. Therefore, the analysis can describe patterns in resolution time but cannot determine the underlying causes of those patterns.

---

## Conclusion

This assessment demonstrates a complete exploratory data analysis workflow on an intentionally imperfect support-ticket dataset.

The analysis began with diagnosis of the raw data, followed by issue-specific cleaning decisions, verification of the cleaned dataset, targeted visualization, and evidence-based interpretation.

The workflow also demonstrates the importance of preserving raw data, documenting cleaning decisions, exporting reproducible outputs, and validating the final notebook before submission.
