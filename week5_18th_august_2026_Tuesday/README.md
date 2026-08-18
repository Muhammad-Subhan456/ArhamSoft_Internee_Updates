# Week 5 — Pandas Foundations

This project contains today's Pandas learning and Kata Set work.

## Project Structure

```text
week5_18th_august_2026_Tuesday/
├── venv/                         # Local virtual environment (not committed)
├── pandas_foundations_final.ipynb
├── requirements.txt
└── README.md
```

## Prerequisites

Python 3 must be installed.

Check:

```powershell
python --version
```

## 1. Create the Virtual Environment

Open PowerShell in the project directory:

```powershell
cd "D:\Subhan Folder\ArhamSoft_Internship\week5_18th_august_2026_Tuesday"
```

Create the environment:

```powershell
python -m venv venv
```

Project files and notebooks should remain outside `venv`.

## 2. Activate the Environment

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Verify the interpreter:

```powershell
python -c "import sys; print(sys.executable)"
```

It should point to:

```text
week5_18th_august_2026_Tuesday\venv\Scripts\python.exe
```

## 3. Install Today's Packages

Only today's installed packages are included in `requirements.txt`:

- Pandas
- NumPy
- JupyterLab
- IPykernel

Install them with:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Register the Virtual Environment with Jupyter

```powershell
python -m ipykernel install --user --name week5-pandas-venv --display-name "Python (Week 5 Pandas)"
```

## 5. Launch JupyterLab

```powershell
jupyter lab
```

Open `pandas_foundations_final.ipynb` and select:

```text
Python (Week 5 Pandas)
```

as the kernel.

## 6. Verify the Environment

Run:

```python
import sys
import numpy as np
import pandas as pd

print("Python:", sys.executable)
print("NumPy:", np.__version__)
print("Pandas:", pd.__version__)
```

The Python path should point to this project's `venv`.

## 7. Run the Final Notebook

The notebook covers:

1. Building a deliberately messy dataset
2. Diagnosing the raw dataset
3. Missing-data strategies
4. `.loc` vs `.iloc`
5. Boolean filtering
6. Cleaning inconsistent categories
7. `groupby()` analysis
8. Vectorization vs `.apply()`
9. Final interpretation

For the final reproducibility check:

```text
Kernel → Restart Kernel and Run All
```

The notebook should complete without errors from a fresh kernel.

## 8. Deactivate

```powershell
deactivate
```
