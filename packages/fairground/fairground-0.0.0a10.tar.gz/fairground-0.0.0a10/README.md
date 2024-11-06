# fairground

[![CI](https://github.com/CoefficientSystems/clara/actions/workflows/main.yaml/badge.svg)](https://github.com/CoefficientSystems/clara/actions/workflows/main.yaml)

"There is nothing that surpasses the joy of creation, if only because through it one wins hours of self-forgetfulness, when one lives in a world of sound." – Clara Schuman

Compliance Tools for statistical analysis and debiasing for LLM powered applicant tracking systems.

## Project cheatsheet

  - **pre-commit:** `pre-commit run --all-files`
  - **pytest:** `pytest` or `pytest -s`
  - **coverage:** `coverage run -m pytest` or `coverage html`
  - **poetry sync:** `poetry install --sync`
  - **updating requirements:** see [docs/updating_requirements.md](docs/updating_requirements.md)



## Initial project setup

1. See [docs/getting_started.md](docs/getting_started.md) or [docs/quickstart.md](docs/quickstart.md)
   for how to get up & running.
2. Check [docs/project_specific_setup.md](docs/project_specific_setup.md) for project specific setup.
3. See [docs/using_poetry.md](docs/using_poetry.md) for how to update Python requirements using
   [Poetry](https://python-poetry.org/).
4. See [docs/detect_secrets.md](docs/detect_secrets.md) for more on creating a `.secrets.baseline`
   file using [detect-secrets](https://github.com/Yelp/detect-secrets).

## fairground Statistical Analysis Utils

fairground provides a comprehensive suite of visuaisation and statistical analysis tools for assessing fairness and bias in selection processes, particularly useful for applicant tracking systems and hiring decisions.

## Core Features

### Selection Rate Analysis

The selection rate analysis tools help visualise and analyse how different groups are selected within your process:
- `plot_selection_rate()`: Creates a horizontal bar plot showing selection rates across selected protected characteristics groups
- `plot_job_selection_rate()`: Generates faceted plots to compare selection rates across different job roles

### Parity Analysis
The parity analysis functions help identify and visualize disparities between groups:
- `parity_difference()`: Calculates the arithmetic difference in selection rates between groups
- `plot_parity_difference()`: Creates a multi-panel visualisation showing parity differences using each group as a baseline
- `plot_parity_difference_scatter()`: Generates a scatter plot heatmap showing parity differences between all group combinations

### Disparate Impact Analysis

Tools for analysing disparate impact and selection rate deviations:
- `disparate_impact_ratio()`: Calculates the ratio of selection rates between groups (also known as the adverse impact ratio)
- `plot_selection_rate_deviation_with_disparate_impact_ratio_value()`: Creates a comprehensive visualisation showing selection rate deviations from equal treatment and disparate impact ratio thresholds

## Key Features
- Flexible Group Analysis: Support for both single and multiple demographic group analysis
- Regulatory Compliance: Built-in support for standard fairness metrics like the 4/5ths rule (disparate impact ratio)
- Visual Insights: Rich visualizations with detailed annotations including:
-- Group sizes (n values)
-- Statistical significance indicators
-- Disparate impact ratio values
-- Equal treatment thresholds

## Example Usage
```
import pandas as pd
from fairground.utils import plot_selection_rate, plot_parity_difference

# Load your data
df = pd.read_csv("hiring_data.csv")

# Plot selection rates by gender
plot_selection_rate(df, "Gender", "Selected")

# Analyze parity differences across multiple demographics
plot_parity_difference(df, ["Gender", "Race", "Age"], "Selected")
```
