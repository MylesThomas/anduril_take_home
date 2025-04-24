# Anduril – Take Home

Quantitative Analyst position at Anduril Industries

## 0. Setup

Create a virtual environment, for example using `venv`:

```bash
python -m venv venv_anduril
source venv_anduril/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

## 1. Pipeline

Steps:
- `00_data_cleaning.ipynb`
- `01_modeling.ipynb`

### Assumptions Made

1. One can derive the month from `Award Date`
2. It's OK to remove the 1 row of data where `Award Date` is NA
3. 