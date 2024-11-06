# EasyEventStudies

This package makes it easy to run event studies on financial assets. In contrast to other packages, it is easy to use, correct and allows for three different models of normal returns estimation. All calculations are based on the standard reference in the literature: *The Econometrics of Financial Markets; John Y. Campbell, Andrew W. Lo and Craig MacKinlay (1998)*

<p align="center">
<a href="https://www.youtube.com/watch?v=H0Ga8uutQgY">🎥 **Watch the Video Tutorial**</a>
</p>

<p align="center">
  <a href="https://www.youtube.com/watch?v=H0Ga8uutQgY">
    <img src="https://img.youtube.com/vi/H0Ga8uutQgY/maxresdefault.jpg" alt="Video Tutorial" width="600"/>
  </a>
</p>




## Quick Start Guide

Install the package using `pip`:

```bash
pip install EasyEventStudies
```

Then import the package:

```python
from EasyEventStudies import *
```

The `run_event_study` function runs a complete event study analysis for a financial asset and an event date. The package takes financial data from Yahoo Finance, so search for the ticker symbol of the asset you are interested on their website [here](https://finance.yahoo.com/). 
As an example, we will run an event study on British Petroleum (ticker: BP) on 15th of April, 2010. At this time, the Deepwater Horizon oil rig exploded. 

```python

results = run_event_study(
    ticker='BP',
    event_date='2010-04-20',
    estimation_window=[-100, -1],
    event_window=[0, 20],
    model_type="constant_model"
)
plot_CAR_over_time(results)
```
<p align="center">
  <img src="https://github.com/NicolasRoever/EasyEventStudies/blob/fbb7adefe2ac26adb6e2d3e319eb455361eccf29/images/BP-example.png" width="70%"/>
</p>

The event study shows that the explosion of the Deepwater Horizon oil rig was associated with a drop in the stock price of about 20 Percent in the first 20 days after the event.


## More Detailed Documentation

The detailed documentation is available as a [PDF](https://github.com/NicolasRoever/EasyEventStudies/blob/main/Documentation_EasyEventStudies.pdf). The package is based on the following two functions:

1. The main function is `run_event_study`. It returns a pandas DataFrame with the results of the event study. Remember to specify the model you want to use to estimate normal returns. 

```python
def run_event_study(
    ticker: str,
    event_date: str,
    estimation_window: Tuple[int, int],
    event_window: Tuple[int, int],
    historical_days: int = 10,
    model_type: str = "market_model"
):
```
- **ticker**: The ticker symbol from Yahoo Finance as a string (e.g., 'BA' for Boeing)
- **event_date**: The date of the event in 'YYYY-MM-DD' format (e.g., '2019-03-08')
- **estimation_window**: A tuple of two integers defining the time period used to estimate normal returns. The first number is the start of the window, the second is the end. For example, [-250, -1] uses the previous year's data.
- **event_window**: A tuple of two integers defining the period for calculating cumulative abnormal returns. The first number is the start, the second is the end. For example, [0, 10] analyzes the 10 days following the event.
- **historical_days**: Number of days before the event window to include in the output. This allows for plotting pre-event stock returns. Defaults to 10.
- **model_type**: The model to use for estimating normal returns. Options are:
  - "market_model": Estimates returns as a function of market returns
  - "constant_model": Assumes constant normal returns
  - "three_factor_model": Uses the Fama-French three-factor model




2. The `plot_CAR_over_time` function plots the cumulative abnormal returns over time. It takes the results of the `run_event_study` function as an input and plots the cumulative abnormal returns over time.

```python
def plot_CAR_over_time(event_study_results,
                       days_before_event: int = 10, 
                       days_after_event: int = 10
                       ):
```

- **event_study_results**: The results of the `run_event_study` function.
- **days_before_event**: Number of days before the event window to include in the plot. Defaults to 10.
- **days_after_event**: Number of days after the event window to include in the plot. Defaults to 10.


# Citation
If you use this package in your work, please cite it as:

```
Roever, Nicolas (2024). EasyEventStudies: A Python Package for Event Studies. https://github.com/NicolasRoever/EasyEventStudies

```

# Notes for Developer

Publishing the package: 
1. Delete the dist folder
2. Update the version number in pyproject.toml
3. Run `python -m build`
4. Run `python -m twine upload dist/*`


