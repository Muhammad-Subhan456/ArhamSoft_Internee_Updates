# Week 5 — EDA & Matplotlib Foundations

This project contains the Exploratory Data Analysis (EDA) and Matplotlib practical work completed during Week 5.

The notebook builds on the previous Pandas data-cleaning work and uses the cleaned customer sales dataset to practice visualization, analytical interpretation, and reproducible reporting.

## Project Structure

```text
week5_19th_august_2026_Wednesday/
│
├── venv/                       # Local virtual environment (not committed)
├── eda_visualization.ipynb     # Final EDA notebook
├── category_totals.png         # Saved visualization
├── technical_summary.md        # Key findings and limitation
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```

## Prerequisites

Make sure Python 3 is installed.

Check:

```powershell
python --version
```

## 1. Create the Virtual Environment

Open PowerShell in the project directory:

Create the virtual environment:

```powershell
python -m venv venv
```

Project files and notebooks should remain outside `venv`.

## 2. Activate the Virtual Environment

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Verify the Python executable:

```powershell
python -c "import sys; print(sys.executable)"
```

## 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

Today's dependencies are:

- NumPy
- Pandas
- Matplotlib
- JupyterLab
- IPykernel

## 4. Register the Virtual Environment with Jupyter

```powershell
python -m ipykernel install --user --name week5-eda-venv --display-name "Python (Week 5 EDA)"
```

## 5. Launch JupyterLab

```powershell
jupyter lab
```

Open `eda_visualization.ipynb` and select:

```text
Python (Week 5 EDA)
```

## 6. Verify the Environment

Run:

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

The Python executable should point to this project's `venv`.

## 7. Notebook Contents

The notebook covers:

1. Recreating and cleaning the customer sales dataset
2. Understanding Matplotlib Figure and Axes
3. Selecting charts based on analytical questions
4. Histogram for transaction amount distribution
5. Bar chart for category-level sales
6. Scatter plot for customer age vs transaction amount
7. Multiple visualizations using subplots
8. Honest vs misleading visualization
9. Saving a Matplotlib figure as a PNG
10. Overall EDA findings and limitations

## 8. Reproducibility Check

Run the notebook from a fresh kernel:

```text
Kernel → Restart Kernel and Run All
```

The notebook should execute from beginning to end without errors.

## 9. Generated Output

The notebook generates:

```text
category_totals.png
```

This is a standalone visualization that can be opened outside Jupyter and reused in reports or documentation.

## 10. Git

Do not commit the virtual environment.

Commit:

```text
eda_visualization.ipynb
category_totals.png
technical_summary.md
requirements.txt
README.md
```

Ignore:

```text
venv/
```

## 11. Recreate the Environment

On another machine:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m ipykernel install --user --name week5-eda-venv --display-name "Python (Week 5 EDA)"
jupyter lab
```

## 12. Deactivate the Environment

```powershell
deactivate
```
