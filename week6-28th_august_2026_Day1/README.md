# EDA Precision Report — Student Performance Analysis

## Overview

This project presents a complete Exploratory Data Analysis (EDA) of a synthetic student-performance dataset.

The analysis investigates relationships between study habits and exam performance, compares exam scores across class sections, evaluates the consistency of observed relationships, and applies statistical techniques to quantify uncertainty.

The notebook is structured as a standalone analytical report rather than a collection of independent exercises. Each analysis is accompanied by written reasoning explaining what the result means and why it matters.

## Objectives

The analysis focuses on:

* Diagnosing the dataset using standard data-quality checks.
* Examining the relationship between weekly study hours and exam score.
* Examining whether nightly sleep hours have a meaningful relationship with exam score.
* Comparing exam performance across class sections.
* Demonstrating how an inappropriate line chart can create a misleading impression for categorical data.
* Evaluating the effect of arbitrary versus deliberate color choices.
* Comparing Pearson and Spearman correlations.
* Using bootstrap resampling to construct a 95% confidence interval for the Section A versus Section C mean-score difference.
* Examining whether the study-hours relationship remains consistent across class sections using small multiples.
* Performing visual QA on saved chart files.
* Independently auditing reported numerical results for reproducibility.

## Dataset

The dataset is generated programmatically using NumPy and Pandas with a fixed random seed.

It contains the following variables:

| Column                  | Description               |
| ----------------------- | ------------------------- |
| `student_id`            | Unique student identifier |
| `class_section`         | Student's class section   |
| `study_hours_per_week`  | Weekly study hours        |
| `sleep_hours_per_night` | Nightly sleep hours       |
| `attendance_pct`        | Attendance percentage     |
| `exam_score`            | Exam score                |

The dataset is intentionally generated with known relationships so that the analytical workflow can be checked against expected patterns.

## Analysis Performed

### 1. Dataset Diagnosis

Standard data-quality checks are performed before analysis, including:

* Dataset structure and dimensions
* Data types
* Missing values
* Duplicate records
* Numerical ranges
* Categorical values
* Basic descriptive statistics

The purpose is to establish confidence in the data before drawing conclusions.

### 2. Study Hours vs. Exam Score

A scatter plot with a fitted trend line is used to examine the relationship between weekly study hours and exam score.

Pearson correlation is calculated to quantify the strength and direction of the linear association.

The result shows a positive association between study hours and exam performance. The analysis explicitly treats this as a correlation rather than a causal relationship.

### 3. Sleep Hours vs. Exam Score

A second scatter plot examines nightly sleep hours against exam score.

The resulting Pearson correlation is close to zero, and the visual pattern does not show a meaningful linear relationship.

This null relationship is treated as a genuine analytical finding rather than being dismissed because it does not show a strong association.

### 4. Exam Score by Class Section

Mean exam scores are compared across Sections A, B, and C using a categorical comparison chart.

The sections are maintained in their natural A → B → C order rather than being sorted by their observed scores.

A bootstrap confidence interval is later used to evaluate the difference between Sections A and C.

### 5. Categorical Trend Trap

The section means are also displayed as a connected line chart.

This visualization demonstrates how connecting categorical groups can create a misleading impression of a continuous progression from one category to another. The underlying values remain unchanged; only the visualization changes.

### 6. Visual QA

Charts are deliberately tested for common visualization problems.

One scatter plot is intentionally given an overlapping annotation to demonstrate a layout failure. The broken version is retained, then corrected using layout adjustment and saved as a separate version.

All charts are saved as PNG files and visually inspected rather than relying only on inline notebook previews.

### 7. Pearson vs. Spearman

Pearson and Spearman correlations are calculated side by side for weekly study hours and exam score.

The comparison helps determine whether the observed association is represented similarly by a linear correlation and a rank-based monotonic correlation.

### 8. Bootstrap Confidence Interval

A bootstrap procedure using `scipy.stats.bootstrap` is used to estimate a 95% confidence interval for the difference in mean exam score between Section A and Section C.

The interval is interpreted in relation to zero to assess whether the observed difference is compatible with a no-difference value at the selected confidence level.

### 9. Small Multiples

The study-hours relationship is visualized separately for Sections A, B, and C using a three-panel small-multiples figure.

Shared axes make the relationships directly comparable across sections and help determine whether the overall relationship is consistent or driven primarily by one group.

## Statistical Interpretation

The analysis demonstrates an important distinction between **association and causation**.

Although weekly study hours show a positive relationship with exam score, the analysis does not establish that additional study directly causes higher scores.

For example, student motivation could influence both study time and exam performance. Because this is observational data rather than a controlled experiment, potential confounding factors cannot be ruled out.

## Reproducibility and Quality Assurance

The notebook includes two explicit verification stages.

### Visual QA

Every saved chart is opened and inspected for:

* Clear titles
* Correct axis labels
* Readable layout
* Appropriate category ordering
* Visual collisions
* Clipping or excessive whitespace
* Appropriate use of color

The deliberately broken layout example is retained alongside its corrected version.

### Numerical Self-Audit

Reported numerical findings are independently recalculated from the underlying dataset.

The final audit checks the reported correlations, section means, Pearson/Spearman comparison, bootstrap results, and section-specific correlations.

All audited numerical claims matched their independently recomputed values, resulting in a successful numerical audit.

## Project Structure

```text
EDA-Precision-Report/
│
├── EDA_Precision_Report.ipynb
├── README.md
├── requirements.txt
│
└── eda_outputs/
    ├── study_hours_vs_exam_score.png
    ├── sleep_hours_vs_exam_score.png
    ├── exam_score_by_class_section.png
    ├── connected_section_means_line_chart.png
    ├── kata6_study_hours_broken.png
    ├── kata6_study_hours_fixed.png
    ├── section_comparison_arbitrary_colors.png
    ├── section_comparison_deliberate_color.png
    └── study_hours_exam_score_small_multiples.png
```

## Installation

Create and activate a Python virtual environment:

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Notebook

Start Jupyter Notebook or JupyterLab:

```bash
jupyter notebook
```

Open:

```text
EDA_Precision_Report.ipynb
```

The notebook is designed to run from a clean kernel.

For the final reproducibility check, restart the kernel and use **Run All**. The notebook was verified to execute successfully from a restarted kernel without execution errors.

## Key Limitation

The dataset is synthetic and observational. Therefore, the findings demonstrate an analytical workflow and statistical reasoning rather than providing evidence about real-world student populations.

In particular, observed correlations should not be interpreted as causal effects because potential confounding variables cannot be fully controlled in this analysis.

## Tools and Technologies

* Python
* NumPy
* Pandas
* Matplotlib
* SciPy
* IPython
* Jupyter Notebook

## Conclusion

This project demonstrates a complete EDA workflow that combines data diagnosis, visualization, statistical analysis, interpretation, visual quality assurance, and numerical reproducibility checks.

The emphasis is not only on producing charts and statistics, but on explaining what the results mean, recognizing misleading visual representations, distinguishing correlation from causation, quantifying uncertainty, and independently verifying reported numerical claims.
