# Anduril – Take Home

Quantitative Analyst position at Anduril Industries

## Context

Take-Home Quantitative Analysis 
 
Objective: Your task is to analyze the attached randomized dataset, which represents a forecasted revenue pipeline over the next 5 years. You will need to assess the probability of our forecast meeting certain revenue targets under uncertainty by applying statistical techniques, including Monte Carlo simulations, to estimate outcomes. To help you structure your answers, consider the audience for this deliverable as our Head of Revenue and Corporate Planning, SVP of Corporate Operations, and Chief Revenue Officer.
 
 
Instructions:
 
Monte Carlo Simulations: Using the provided dataset, conduct a Monte Carlo simulation to estimate the probability that our forecast will meet or exceed the below revenue targets in each of the next 5 years. The definition of forecast is included in the “Variable Definitions” section.  Please run at least 10,000 simulations and summarize the distribution of outcomes. 
2025 target – $11,755,000,000
2026 target – $13,860,000,000
2027 target – $15,355,000,000
2028 target – $16,256,000,000
2029 target – $20,700,000,000
 
Uncertainty Analysis: 
Identify and outline the key sources of uncertainty in the dataset and model 
Describe how you would adjust your Monte Carlo model to account for longer-term, macro-level shifts in government defense budgets 
Describe how you would incorporate shorter-term, operational risks 
Propose an alternative method to quantify uncertainty in this dataset beyond a Monte Carlo simulation
 
Deliverables:
 
A short write-up (preferably PowerPoint) explaining your methodology, assumptions, key takeaways, and answering the questions in the “Uncertainty Analysis” section. Include any visualizations (histograms, probability distributions, etc.) that help illustrate your findings
A Python, R, or Excel-based implementation of your Monte Carlo simulations and summary of outcomes
 
Variable Definitions: 
We define the forecast based on the “Forecast Category”. 
Forecast = the sum of all weighted revenue (as determined by “Probability of Award”) for opportunities with a “Base Case” or “Closed Won” Forecast Category. 
Upside = Forecast + the sum of all weighted revenue for opportunities with a “Upside” Forecast Category
“Stage” determines where in the sales cycle the opportunity is (Identification -> Qualification -> Shaping -> Planning -> Negotiation -> Contracting -> Closed, Won)
“Type” indicates whether the opportunity is new business, a follow-on to a previous contract, or an option on an existing contract 
“Revenue Type” outlines whether the opportunity is a development contract, a direct product sale, cost plus fixed fee, annual subscription, or operations and maintenance (O&M)

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