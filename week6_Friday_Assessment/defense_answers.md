# Defense Answers — ML Pipeline Assessment

## 1. Random Forest vs Logistic Regression

My Random Forest achieved an accuracy of **0.7708**
compared with **0.7458** for Logistic Regression.

This does not mean Logistic Regression should always be the answer.
Model selection should depend on the evaluation criteria and the
behavior of the particular problem. In my experiment, Random Forest
also achieved higher precision (**0.7834**
vs **0.7677**), recall
(**0.8542** vs
**0.8264**), F1
(**0.8173** vs
**0.7960**), and ROC-AUC
(**0.8541** vs
**0.8454**).

Therefore, I selected Random Forest because it had stronger overall
held-out test performance in this experiment. The choice is based on
the actual evidence from this dataset, not on the assumption that
Random Forest is always superior.

---

## 2. Why Must Imputation Use Only the Training Data?

The credit-score imputation value was calculated using only the
training portion of the data.

My train-only median was **649.00**, while
the median calculated from the full dataset was
**650.00**.

Using the full dataset before splitting would allow information from
the future held-out test set to influence preprocessing of the training
data. Even though the median is not a trained predictive model, it is
still a statistic calculated from the data.

That means the test set would indirectly influence the training
pipeline. This is a form of data leakage and can make the evaluation
less representative of how the pipeline would behave on genuinely
unseen data.

The correct procedure is therefore to calculate the imputation value
from `X_train` only and then apply that fixed value to both `X_train`
and `X_test`.

---

## 3. Accuracy vs Recall for Loan Default

For a loan-default problem, recall on the **default class (`default=1`)**
is particularly important because a false negative means the model
fails to identify an applicant who actually defaults.

My Random Forest achieved a default-class recall of
**0.8542**.

If I optimized only for overall accuracy, I could potentially favor a
model that performs well by predicting the majority class while
missing many actual defaulters. The baseline demonstrates this issue:
it achieved recall of **1.0000**, but this
came from predicting the majority class for every applicant, while its
ROC-AUC was only **0.5000**.

In practice, optimizing the wrong metric could result in approving
too many risky loans and therefore increasing financial losses.

However, recall should not automatically be maximized without
considering precision and the business cost of false positives.
Rejecting every applicant would produce very high default recall but
would also incorrectly reject many applicants who would repay their
loans.

---

## 4. Calibration and Risk-Based Interest Rates

The calibration curve compares the model's predicted probability of
default with the actual observed default rate within probability bins.

For my final Random Forest, the mean absolute calibration gap was
**0.0517**, and the maximum calibration
gap was **0.1705**.

I would **not directly trust these predicted probabilities to set
risk-based interest rates** without additional validation.

A model can have strong discrimination — my Random Forest achieved a
ROC-AUC of **0.8541** — while still
having imperfect probability calibration.

For a real lending system, I would validate calibration on
representative out-of-time data and consider recalibration methods
such as Platt scaling or isotonic regression if necessary.

Therefore, a predicted probability such as 0.70 should not
automatically be interpreted as exactly 70% real-world default risk
without calibration and production validation.

---

## 5. Important Real-World Factor Missing From the Pipeline

One important missing factor is the applicant's **existing debt
obligations or debt-to-income ratio (DTI)**.

The current pipeline has applicant income and the new loan amount, but
it does not tell us how much debt the applicant is already responsible
for.

Two applicants could have the same income, credit score, and requested
loan amount but have very different repayment capacities because one
may already have substantial outstanding debt.

Without this information, the model has an incomplete view of the
applicant's financial risk. Therefore, even strong performance on this
synthetic test set would not justify using the model directly for real
lending decisions.
