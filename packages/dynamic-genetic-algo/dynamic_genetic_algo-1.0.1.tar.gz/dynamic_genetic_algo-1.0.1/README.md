# Genetic Algorithm for Flexible Data Handling

A Python library that leverages genetic algorithms to generate optimized queries for handling data flexibly without dropping rows. This approach enables selective row exclusion per query, bypassing the need for imputation or deletion, and supports high-volume data processing through parallelism.

## Features

- Generates custom queries to ignore specific rows based on query-specific criteria.
- Supports high-volume data processing with parallel computation.
- Dynamically calculates feature-specific min/max values for optimized filtering.
- Enables binary classification filtering and calculates the percentage of 1s.

## Workflow

1. **Load and Clean Data**:

   - Load data and apply minimal cleaning (e.g., drop `inf` values or other outliers that could disrupt quintile calculations).

2. **Set Parameters**:

   - Define parameters that control the algorithm's behavior and query generation.

3. **Dynamic Feature Computation**:

   - Compute min/max values and deltas dynamically for each feature to enhance query specificity.

4. **Generate Feature-Specific Combinations**:

   - Produce min/max combinations for each feature based on unique criteria.

5. **Filter Data**:

   - Filter CSVs using generated criteria, calculating the percentage of 1s for binary classification tasks (if applicable).

6. **Genetic Algorithm Optimization**:
   - Carry over the fittest combinations to the next generation, introducing new entries at a defined rate for continuous improvement.

## Installation

Install the package via pip:

```bash
pip install dynamic_genetic_algo

from dynamic_genetic_algo import GeneticAlgorithm, GeneticParams

# Define the genetic parameters
genetic_params = GeneticParams(
    population_size=200,
    elite_size=0.1,
    mutation_rate=0.6,
    generations=1000,
    min_size_ratio=0.005,  # Percent of dataset that must be retained to avoid anomalies
    average_column="Example Target",
    categorical_columns=id_dict,  # Dictionary where key is column name and value is list of possible categories
    super_elite=20  # Extra privileges for the top elite
)

# Initialize and run the genetic algorithm
if __name__ == "__main__":
    genetic_algo = GeneticAlgorithm(
        training_data=combined_df,
        target="Target Over 5",
        columns_to_drop=[
            "Sample Column 1",
            "Sample Column 2",
            "Target"  # Exclude target column from queries
        ],
        genetic_params=genetic_params,
    )
    genetic_algo.run()
```
