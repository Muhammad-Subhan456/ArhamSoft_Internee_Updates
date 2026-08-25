# Week 06 — Monday — EDA Precision Lab

## Real Relationships vs. Real Comparisons, and Verified Findings

### Overview

Today's work focused on improving precision in Exploratory Data Analysis (EDA), particularly in distinguishing genuine numerical relationships from categorical comparisons.

The lab also emphasized visualization correctness, Pearson correlation, visual quality assurance, and the discipline of verifying every numerical finding before reporting it.

A major focus was moving beyond simply producing working code toward being able to explain and defend every analytical and visualization decision.

---

## Learning Objectives

- Distinguishing genuine numerical relationships from categorical comparisons.
- Understanding when to use scatter plots, bar charts, and line charts.
- Calculating and interpreting Pearson correlation.
- Understanding that correlation does not imply causation.
- Recognizing a near-zero correlation as a valid analytical finding.
- Using the shuffle test to identify misleading categorical line charts.
- Understanding when color communicates meaningful information.
- Preserving intentional category ordering.
- Performing visual QA on the actual saved PNG rather than relying only on successful code execution.
- Verifying numerical findings independently before writing them into the report.
- Building a final self-audit to catch mismatches before submission.
- Ensuring the complete notebook runs successfully from a fresh kernel.

---

## Environment Setup

A dedicated Python virtual environment was created for the project.

### Packages Used

- NumPy
- Pandas
- Matplotlib
- SciPy
- JupyterLab
- IPykernel
- Tabulate

### Project Structure

```text
week6-Day1/
│
├── venv/
├── eda_precision_lab.ipynb
├── README.md
└── requirements.txt
```

---

# Dataset

The dataset contains 600 student records and six variables:

| Column | Description |
|---|---|
| `student_id` | Unique student identifier |
| `class_section` | Student's class section: A, B, or C |
| `study_hours_per_week` | Weekly study hours |
| `sleep_hours_per_night` | Average nightly sleep hours |
| `attendance_pct` | Attendance percentage |
| `exam_score` | Student examination score |

Dataset shape:

```text
(600, 6)
```

The dataset was generated using the exact specification provided for the lab. No cleaning or modification of the original dataset was performed.

---

# Kata 1 — Genuine Relationship

## Study Hours vs. Exam Score

### Analytical Question

Do students who study more hours per week tend to achieve higher exam scores?

Both variables are numerical, so this is a genuine relationship question.

### Visualization

A scatter plot was selected because it allows the relationship between two numerical variables to be examined directly. A fitted linear trend line was added to make the overall direction easier to assess visually.

### Pearson Correlation

```text
r = 0.689476
```

This indicates a moderately strong positive linear association between weekly study hours and exam score in the observed dataset.

### Verification

The correlation was independently recalculated using `scipy.stats.pearsonr()`.

```text
Primary correlation:       0.689476
Independent verification:  0.689476
Absolute difference:       0.000000000000
```

The matching calculations confirm that the reported correlation is reproducible.

### Interpretation

The results indicate an association between study hours and exam score. However, correlation does not establish causation.

---

# Kata 2 — Null Relationship

## Sleep Hours vs. Exam Score

### Analytical Question

Is nightly sleep duration linearly associated with exam score?

Both variables are numerical, making this a genuine relationship question.

### Visualization

A scatter plot with a fitted linear trend line was used.

### Pearson Correlation

```text
r = -0.021658
```

This value is extremely close to zero, indicating essentially no linear relationship between nightly sleep duration and exam score in this dataset.

### Independent Verification

```text
Primary correlation:       -0.021658
Independent verification: -0.021658
Absolute difference:       0.000000000000
P-value:                   0.596489
```

### Interpretation

The near-zero correlation is a valid analytical finding rather than a failed result.

The analysis provides no evidence of a meaningful linear association between nightly sleep duration and exam score in the observed dataset.

This should not be interpreted as proof that sleep has no effect on academic performance. Pearson correlation measures linear association and does not rule out non-linear relationships or other factors.

---

# Kata 3 — Categorical Comparison

## Exam Score by Class Section

### Analytical Question

How does average exam score differ across class sections A, B, and C?

`class_section` is categorical while `exam_score` is numerical. Therefore, this is a categorical comparison rather than a genuine numerical relationship.

### Visualization

A bar chart was selected because it directly compares a numerical summary across discrete categories.

The natural category order was preserved:

```text
A → B → C
```

### Average Exam Scores

```text
Section A: 87.608491
Section B: 87.025758
Section C: 91.362632
```

Section C had the highest observed average exam score, while Section B had the lowest.

### Verification

The group means were independently recomputed. All absolute differences were zero:

```text
Section A: 0.0
Section B: 0.0
Section C: 0.0
```

### Interpretation

The results describe differences between the observed groups. They do not establish that class section membership causes differences in exam performance.

---

# Kata 4 — The Line-Chart Trap

## Why a Line Chart Is Misleading for Categories

A line chart was deliberately created using the class-section averages.

The chart connected:

```text
A → B → C
```

However, A, B, and C are categorical labels rather than continuous numerical values.

Connecting them with a line can incorrectly imply a continuous progression between the categories.

### Shuffle Test

The category order was changed from:

```text
A → B → C
```

to:

```text
C → A → B
```

The underlying group averages remained unchanged, but the apparent direction of the line changed.

This demonstrates why a categorical line chart is misleading.

### Conclusion

The appropriate visualization for comparing average exam scores across class sections is a bar chart or another categorical comparison visualization.

---

# Kata 5 — Visual Quality Assurance

## Inspecting the Actual Saved PNG

A chart was deliberately created with a constrained figure size and long labels to demonstrate a potential layout problem.

The initial visualization was saved as:

```text
chart_qa_before.png
```

The actual PNG file was inspected rather than relying only on the inline notebook output.

The chart was then corrected using `fig.tight_layout()` and an appropriate figure size.

The corrected visualization was saved as:

```text
chart_qa_after.png
```

### Visual QA Workflow

```text
Create
  ↓
Save
  ↓
Inspect actual PNG
  ↓
Identify problem
  ↓
Fix
  ↓
Save again
  ↓
Reinspect
```

### Key Lesson

Successful execution of plotting code does not guarantee that the final visualization is readable. The actual saved artifact must be inspected before considering a visualization complete.

---

# Kata 6 — Color + Category Order

## Meaningful Color

An arbitrary-color version of the class-section comparison was deliberately created. The colors did not represent an additional variable.

Therefore, using different colors could introduce unnecessary visual meaning. A cleaner version was then created using a consistent visual treatment.

### Category Order

The class sections were intentionally preserved in their natural order:

```text
A → B → C
```

The categories were not reordered according to their observed exam-score averages.

### Verification

Expected:

```text
['A', 'B', 'C']
```

Actual:

```text
['A', 'B', 'C']
```

Verification result:

```text
True
```

### Key Lesson

Color should communicate meaningful information when used. Category order should also be intentional and should not be changed simply to emphasize observed results.

---

# Kata 7 — Final Self-Audit

## Purpose

The final self-audit independently recomputed key numerical findings from the dataset.

This was done to ensure that no reported number was based on memory, an earlier output, or an intended result.

### Audit Findings

| Finding | Claimed Value | Freshly Recomputed | Absolute Difference | Verified |
|---|---:|---:|---:|:---:|
| Study hours vs exam score Pearson r | 0.689476 | 0.689476 | 0.000000 | True |
| Sleep hours vs exam score Pearson r | -0.021658 | -0.021658 | 0.000000 | True |
| Section A average exam score | 87.608491 | 87.608491 | 0.000000 | True |
| Section B average exam score | 87.025758 | 87.025758 | 0.000000 | True |
| Section C average exam score | 91.362632 | 91.362632 | 0.000000 | True |

All numerical findings matched their freshly recomputed values.

```text
SELF-AUDIT PASSED
```

---

# Verification Discipline

A key improvement implemented throughout today's notebook was:

```text
Calculate
   ↓
Store result in variable
   ↓
Independently verify
   ↓
Generate report text using f-strings
   ↓
Freshly recompute during self-audit
   ↓
Compare values
```

Computed numbers used in findings were generated from Python variables rather than manually typed from memory.

---

# Final Conclusion

Today's lab demonstrated the distinction between genuine numerical relationships and categorical comparisons.

The relationship between study hours and exam score produced a Pearson correlation of approximately `0.689476`, indicating a positive linear association in the observed data.

The relationship between sleep hours and exam score produced a correlation of approximately `-0.021658`, indicating essentially no linear association.

Average exam scores were compared across class sections using a bar chart because class section is categorical rather than continuous.

The shuffle test demonstrated why connecting categorical groups with a line can create a misleading visual interpretation.

The visual QA exercise demonstrated that successful plotting code does not guarantee a correct final image and that saved visualization artifacts should be inspected directly.

Finally, the self-audit independently recomputed the key numerical findings and confirmed that all reported values matched their fresh calculations.

---

# Final Checklist

## Environment

- [x] Virtual environment created
- [x] Required packages installed
- [x] Jupyter kernel configured
- [x] `tabulate` installed for Markdown table rendering

## Analysis

- [x] Dataset generated
- [x] Dataset structure verified
- [x] Genuine numerical relationship analyzed
- [x] Pearson correlation calculated
- [x] Near-zero correlation analyzed
- [x] Categorical comparison performed
- [x] Group means independently verified

## Visualization

- [x] Scatter plot used for numerical relationships
- [x] Fitted trend lines added
- [x] Bar chart used for categorical comparison
- [x] Misleading line chart demonstrated
- [x] Shuffle test performed
- [x] Visual QA performed on saved PNGs
- [x] Color usage evaluated
- [x] Category order verified

## Verification

- [x] Numerical findings generated from variables
- [x] Independent calculations performed
- [x] Final self-audit completed
- [x] All self-audit differences equal zero
- [x] Self-audit assertion passed
- [x] Restart Kernel → Run All completed successfully

---

## Key Takeaways

1. Use scatter plots for relationships between numerical variables.
2. Use bar charts or boxplots for comparisons across categories.
3. A near-zero correlation is a valid finding.
4. Correlation indicates association, not causation.
5. Categorical line charts can imply relationships that do not exist.
6. The shuffle test helps identify misleading categorical trends.
7. Color should communicate meaningful information rather than decoration.
8. Category order should be intentional.
9. A chart must be visually inspected after saving.
10. Every reported number should be verified before submission.
11. A self-audit catches discrepancies before a reviewer does.
12. A notebook should survive Restart Kernel → Run All.
