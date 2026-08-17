# Week 5 — NumPy Foundations

This project contains the Jupyter notebooks and practical exercises completed during the Week 5 NumPy training tasks.

## Project Structure

```text
week5_17th_august_2027_Monday/
├── venv/                       # Local virtual environment (not tracked by Git)
├── images/                     # Supporting images
├── boolean-masking.ipynb
├── hidden-state.ipynb
├── kataSets.ipynb
├── notebook.ipynb
├── requirements.txt
└── README.md
```

## Prerequisites

Make sure Python 3 is installed.

Check the installed Python version:

```powershell
python --version
```

## Setup with Virtual Environment

### 1. Clone the repository

If you have not already cloned the repository:

```powershell
git clone <repository-url>
cd week5_17th_august_2027_Monday
```

### 2. Create the virtual environment

Create a dedicated virtual environment for this project:

```powershell
python -m venv venv
```

### 3. Activate the virtual environment

On Windows PowerShell:

```powershell
.env\Scripts\Activate.ps1
```

After activation, your terminal should show:

```text
(venv)
```

If PowerShell blocks activation because of the execution policy, run the following command in PowerShell and then activate the environment again:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Install the required packages

Install the packages listed in `requirements.txt`:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The project uses:

- NumPy
- JupyterLab
- IPykernel

## Launch JupyterLab

After activating the virtual environment, run:

```powershell
jupyter lab
```

JupyterLab should open in your browser.

Open the required `.ipynb` notebook from the project directory.

## Select the Python Environment

If JupyterLab does not automatically use the project's virtual environment, register the environment as a Jupyter kernel:

```powershell
python -m ipykernel install --user --name week5-venv --display-name "Python (Week 5)"
```

Then select:

```text
Python (Week 5)
```

as the notebook kernel.

## Verify the Environment

Inside a notebook, run:

```python
import sys
import numpy as np

print(sys.executable)
print(np.__version__)
```

The Python executable should point to:

```text
...\week5_17th_august_2027_Mondayenv\Scripts\python.exe
```

## Running the Notebooks

The main notebooks include:

- `kataSets.ipynb` — practical NumPy Kata Set work
- `hidden-state.ipynb` — Jupyter hidden-state experiment
- `boolean-masking.ipynb` — Boolean masking practice
- `notebook.ipynb` — notebook/NumPy practice

Open the required notebook in JupyterLab and execute the cells from top to bottom.

For the final assembled notebook, use:

```text
Restart Kernel → Run All
```

This verifies that the notebook works correctly from a completely fresh kernel without relying on hidden state or previously executed cells.

## Git and Virtual Environment

The `venv/` directory should **not** be committed to Git.

It is ignored because the virtual environment contains locally installed and platform-specific files.

Instead, the project provides:

```text
requirements.txt
```

to recreate the environment.

To recreate the environment on another machine:

```powershell
python -m venv venv
.env\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Deactivate the Environment

When finished working, deactivate the virtual environment with:

```powershell
deactivate
```
