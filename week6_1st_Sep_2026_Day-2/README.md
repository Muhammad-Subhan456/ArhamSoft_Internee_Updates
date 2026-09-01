# EDA Peer Review Lab

## Overview

This project is a peer-review exercise focused on identifying and correcting
common problems in Exploratory Data Analysis (EDA).

The notebook reviews an original analysis created by a fictional trainee,
Alex, and then rebuilds the analysis from the same underlying `learners`
DataFrame. The goal is not only to produce correct charts, but also to evaluate
whether the visualizations, statistical calculations, written findings, and
conclusions are properly supported by the data.

The review follows an eight-point EDA checklist covering chart classification,
correlation reporting, null findings, causal language, visualization choices,
visual QA, numerical accuracy, and statistical support for group comparisons.

---

## Objectives

The main objectives of this exercise are to:

- Review an existing EDA notebook from a peer-review perspective.
- Distinguish relationship charts from categorical comparison charts.
- Compute and report Pearson correlations.
- Explicitly report null or near-zero relationships.
- Identify unsupported causal claims.
- Identify plausible confounding variables.
- Use deliberate category ordering and color choices.
- Perform visual QA on saved chart files.
- Independently verify numerical claims.
- Use bootstrap confidence intervals to support group comparisons.
- Produce a corrected, reproducible analysis.
- Verify that the notebook works successfully after restarting the kernel.

---

## Dataset

The notebook generates a synthetic online-course learner dataset using a fixed
random seed.

The dataset contains the following variables:

- `learner_id` — unique learner identifier
- `course_track` — learner's course track
- `weekly_login_hours` — weekly platform login hours
- `forum_posts` — number of forum posts
- `completion_pct` — course completion percentage

The same `learners` DataFrame is used for both the original analysis and the
corrected analysis.

---

## Project Structure

```text
EDA_Peer_Review_Lab/
│
├── EDA_Peer_Review_Lab.ipynb
├── requirements.txt
├── README.md
│
└── eda_outputs/
    ├── chart_distribution.png
    ├── chart_relationship_track.png
    ├── chart_login_vs_completion.png
    ├── chart_forum_vs_completion.png
    └── corrected_*.png
```

The `eda_outputs` directory contains the saved visualizations generated during
the analysis and corrected notebook.

---

## Notebook Structure

The notebook is organized into three major sections.

### Part A — Alex's Original Analysis

Alex's original setup, charts, findings, and conclusion are reproduced before
any corrections are introduced.

The original analysis includes:

1. Distribution of weekly login hours
2. Course track vs. completion
3. Weekly login hours vs. completion
4. Forum posts vs. completion

This reproduction allows the original work to be reviewed independently from
the corrected version.

---

### Part A — Written Peer Review

The original analysis is evaluated using an eight-point review checklist.

The review covers:

1. Relationship vs. comparison chart classification
2. Numerical correlation reporting
3. Reporting every chart result, including null results
4. Correlation vs. causation
5. Deliberate colors and category ordering
6. Saved-chart visual QA
7. Independent numerical verification
8. Statistical backing for group differences

Each identified issue includes the specific chart or finding, supporting
evidence, the relevant checklist item, and the required correction.

---

### Part B — Corrected Analysis

The identified issues are corrected using the same `learners` DataFrame.

The corrections include:

* Reclassifying course track as a categorical comparison.
* Using a consistent course-track order.
* Using deliberate visualization choices.
* Computing and reporting Pearson correlation for login hours and completion.
* Explicitly reporting the forum-posts relationship.
* Removing unsupported causal language.
* Naming learner motivation as a plausible confound.
* Correcting the reported overall mean completion percentage.
* Fixing the histogram annotation/title layout collision.
* Saving and inspecting corrected chart files.
* Independently recomputing numerical claims.
* Computing a bootstrap 95% confidence interval for the Data Science vs.
  Web Dev completion gap.

---

### Part C — Reviewer's Note

The notebook concludes with a short reviewer's note summarizing:

* What Alex did well.
* The most important analytical issue.
* The highest-priority corrections required to make the analysis reliable.

---

## Statistical Methods

The corrected notebook uses:

### Pearson Correlation

Pearson correlation is used to quantify linear associations between continuous
variables.

### Bootstrap Confidence Interval

A bootstrap 95% confidence interval is used to quantify uncertainty around the
difference in mean completion percentage between Data Science and Web Dev
learners.

### Correlation vs. Causation

The notebook explicitly distinguishes observational association from causal
claims and identifies learner motivation as a plausible confounding variable.

---

## Visual QA

The notebook performs visual quality checks on saved PNG files rather than
relying only on inline notebook previews.

The histogram layout issue from the original analysis is deliberately identified
and corrected by repositioning the annotation and applying:

```python
fig.tight_layout()
```

The corrected chart is then saved and inspected as an actual PNG.

---

## Numerical Audit

Numerical claims in the corrected findings are generated dynamically using
Python variables and f-strings rather than manually entered values.

Key numerical results are independently recomputed and compared against the
reported values to ensure consistency with the underlying dataset.

---

## Reproducibility

The notebook was tested using:

**Restart Kernel → Run All**

The complete notebook successfully executes from a fresh kernel without relying
on variables left over from previous interactive execution.

---

## Technologies Used

* Python
* NumPy
* Pandas
* Matplotlib
* SciPy
* Jupyter Notebook
* IPython

---

## Installation

Create and activate a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Then open the notebook and select the project's virtual environment as the
Jupyter kernel.

---

## Key Learning Outcomes

This exercise demonstrates that a high-quality EDA is not only about producing
charts. A reliable analytical report should also:

* Ask the correct analytical question.
* Use an appropriate visualization for that question.
* Quantify relationships instead of relying only on visual impressions.
* Report null findings honestly.
* Avoid unsupported causal conclusions.
* Make visual design choices deliberately.
* Verify saved charts visually.
* Independently audit numerical claims.
* Quantify uncertainty when making group-comparison claims.
* Remain reproducible from a clean kernel.
