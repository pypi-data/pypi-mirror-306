import concurrent.futures
import logging
import os
import random
from typing import Dict, List, Tuple

import pandas as pd
from prettytable import PrettyTable

logging.basicConfig(level=logging.INFO)

# Genetic algorithm for flexible data handling without dropping rows:
# Generates queries to selectively ignore rows per query instead of imputing or deleting them.
# Supports high-volume processing through parallelism.

# Workflow:
# 1. Load and clean data minimally (drop infs or other disruptors for quintile calculations).
# 2. Set parameters to control algorithm behavior.
# 3. Dynamically compute min/max values and deltas for each feature.
# 4. Generate feature-specific min/max combinations that meet unique criteria.
# 5. Filter CSVs using criteria, calculating % of 1s for binary classification (if applicable).
# 6. Carry over the fittest combinations to the next generation, adding new entries at a set rate.


class GeneticParams:
    def __init__(
        self,
        population_size: int,
        elite_size: float,
        mutation_rate: float,
        generations: int,
        min_size_ratio: float,
        average_column: str,
        categorical_columns: Dict[str, List[int]],
        super_elite: int = 20,
    ):
        self.population_size = population_size
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.min_size_ratio = min_size_ratio
        self.average_column = average_column
        self.categorical_columns = categorical_columns
        self.super_elite = super_elite


class GeneticAlgorithm:
    """
    A class to implement a genetic algorithm for optimizing query conditions based on training data.

    Parameters:
        training_data (pd.DataFrame): The training dataset.
        target (str): The target column name.
        columns_to_drop (List[str]): List of columns to drop from the training data.
    """

    MAX_COLUMNS = 5
    MIN_COLUMNS = 1

    def __init__(
        self,
        training_data: pd.DataFrame,
        target: str,
        columns_to_drop: List[str],
        genetic_params: GeneticParams,
    ):
        self.training_data = training_data
        self.target = target
        self.columns_to_drop = columns_to_drop
        self.genetic_params = genetic_params
        self.cat_criteria = list(self.genetic_params.categorical_columns.keys())
        self.criteria = self.generate_criteria()
        self.MIN_ROWS = int(
            len(self.training_data) * self.genetic_params.min_size_ratio
        )

    def clean_training_data(self) -> pd.DataFrame:
        """
        Clean the training data by dropping specified columns.

        Returns:
            pd.DataFrame: The cleaned training data.
        """
        return self.training_data.drop(columns=self.columns_to_drop, errors="ignore")

    def generate_criteria(self) -> Dict[str, Dict[str, float]]:
        """
        Generate criteria for each numeric column in the cleaned data.

        Returns:
            dict: A dictionary containing criteria for each column.
        """
        cleaned_data = self.clean_training_data()
        criteria = {}
        numeric_columns = cleaned_data.select_dtypes(include="number").columns

        for column in numeric_columns:
            if column in self.genetic_params.categorical_columns:
                continue  # Skip categorical columns

            non_na_col = cleaned_data[column].dropna()
            if non_na_col.empty:
                continue  # Skip empty columns

            min_value = non_na_col.quantile(0.05).round(2)
            max_value = non_na_col.quantile(0.95).round(2)
            iqr = non_na_col.quantile(0.75) - non_na_col.quantile(0.25)
            std_dev = non_na_col.std()

            min_delta = max(iqr / 10, std_dev / 10)
            max_delta = min(iqr / 2, std_dev / 2)

            # Ensure that min_delta doesn't exceed max_delta and both are non-negative
            min_delta = min(max(min_delta, 0), max_delta)
            max_delta = max(max_delta, 0)

            criteria[column] = {
                "Name": column,
                "Min": min_value,
                "Max": max_value,
                "Min Delta": round(min_delta, 2),
                "Max Delta": round(max_delta, 2),
            }
        return criteria

    def generate_random_query(
        self, allowed_features
    ) -> List[Tuple[str, float, float, str]]:
        """
        Generate a random query with 2 to MAX_COLUMNS columns from both numeric and categorical criteria.
        """
        numeric_columns = [col for col in allowed_features if col in self.criteria]
        categorical_columns = [
            col for col in allowed_features if col in self.cat_criteria
        ]
        all_columns = numeric_columns + categorical_columns

        num_columns = random.randint(self.MIN_COLUMNS, self.MAX_COLUMNS)
        selected_columns = random.sample(
            all_columns, min(num_columns, len(all_columns))
        )

        query_conditions = []
        for column in selected_columns:
            if column in self.cat_criteria:
                # Categorical column
                categories = self.genetic_params.categorical_columns[column]
                value = random.choice(categories)
                query_conditions.append((column, value, value, "categorical"))
            else:
                # Numeric column
                criteria = self.criteria[column]
                min_limit = criteria["Min"]
                max_limit = criteria["Max"]
                min_delta = criteria["Min Delta"]
                max_delta = criteria["Max Delta"]

                if max_limit - min_limit < min_delta:
                    continue  # Skip if the range is too small

                min_value = round(random.uniform(min_limit, max_limit - min_delta), 2)
                max_value = round(
                    random.uniform(
                        min_value + min_delta, min(min_value + max_delta, max_limit)
                    ),
                    2,
                )
                query_conditions.append((column, min_value, max_value, "numeric"))

        return query_conditions

    @staticmethod
    def apply_query(query_conditions, training_data):
        """Filter the dataframe based on query conditions."""
        filtered_df = training_data

        for condition in query_conditions:
            column, min_value, max_value, column_type = condition
            if column_type == "numeric":
                filtered_df = filtered_df[
                    (filtered_df[column] >= min_value)
                    & (filtered_df[column] <= max_value)
                ]
            elif column_type == "categorical":
                value = min_value  # min_value == max_value == value
                filtered_df = filtered_df[filtered_df[column] == value]

            if filtered_df.empty:
                break  # Early exit if no data left

        return filtered_df

    def evaluate_fitness(self, query_conditions):
        """Apply query and calculate fitness."""
        filtered_df = self.apply_query(query_conditions, self.training_data)

        if len(filtered_df) < self.MIN_ROWS:
            return 0, 0, 0  # Low fitness for too few rows

        row_count = len(filtered_df)
        fitness = filtered_df[self.target].mean().round(2)
        avg_target = filtered_df[self.genetic_params.average_column].mean().round(2)

        return fitness, avg_target, row_count

    def generate_query_string(self, query_conditions):
        query_parts = []
        for condition in query_conditions:
            column, min_value, max_value, column_type = condition
            if column_type == "numeric":
                query_parts.append(f"{column}_{min_value}_{max_value}")
            elif column_type == "categorical":
                query_parts.append(f"{column}_{min_value}")
        return "__".join(query_parts)

    def initialize_population(self, allowed_features):
        """Generate the initial population of queries using allowed features."""
        return [
            self.generate_random_query(allowed_features)
            for _ in range(self.genetic_params.population_size)
        ]

    def select_parents(self, population_with_fitness):
        """Select the top N elites."""
        top_n = self.genetic_params.super_elite
        elite_size = max(
            top_n, int(len(population_with_fitness) * self.genetic_params.elite_size)
        )
        sorted_population = sorted(
            population_with_fitness, key=lambda x: x[1], reverse=True
        )
        elites = [individual for individual, _, _ in sorted_population[:elite_size]]
        return elites

    def crossover(self, parent1, parent2):
        """
        Perform crossover between two parents to produce an offspring.

        Returns:
            List[Tuple[str, float, float, str]]: The offspring individual.
        """
        min_length = min(len(parent1), len(parent2))
        if min_length < 2:
            return parent1.copy()

        split_point = random.randint(1, min_length - 1)
        return parent1[:split_point] + parent2[split_point:]

    def mutate(self, individual, allowed_features):
        """Mutate a query by changing one gene, possibly introducing a new column."""
        if random.random() < self.genetic_params.mutation_rate:
            idx_to_mutate = random.randint(0, len(individual) - 1)
            # Choose a new column from allowed_features
            new_column = random.choice(allowed_features)

            if new_column in self.cat_criteria:
                # Categorical column
                categories = self.genetic_params.categorical_columns[new_column]
                value = random.choice(categories)
                individual[idx_to_mutate] = (new_column, value, value, "categorical")
            else:
                # Numeric column
                criteria = self.criteria[new_column]
                min_limit = criteria["Min"]
                max_limit = criteria["Max"]
                min_delta = criteria["Min Delta"]
                max_delta = criteria["Max Delta"]

                if max_limit - min_limit < min_delta:
                    return individual  # Skip mutation if range is too small

                min_value = round(random.uniform(min_limit, max_limit - min_delta), 2)
                max_value = round(
                    random.uniform(
                        min_value + min_delta, min(min_value + max_delta, max_limit)
                    ),
                    2,
                )
                individual[idx_to_mutate] = (
                    new_column,
                    min_value,
                    max_value,
                    "numeric",
                )
        return individual

    def create_next_generation(self, elite_population, top_results, allowed_features):
        """Generate the next generation with the top N individuals and the rest filled via immigration or crossover/mutation."""
        top_n = self.genetic_params.super_elite
        # Extract only the queries from top_results
        top_queries = [res[0] for res in top_results[:top_n]]

        # Start with the top N queries
        next_generation = top_queries.copy()

        # Exclude top N from crossover
        crossover_pool = elite_population[top_n:]

        # Adjust the immigration rate as per your preference
        immigration_rate = 1 - self.genetic_params.elite_size

        while len(next_generation) < self.genetic_params.population_size:
            if random.random() < immigration_rate:
                # Immigration: Generate a completely new random query using allowed_features
                next_generation.append(self.generate_random_query(allowed_features))
            else:
                # Perform crossover and mutation
                if len(crossover_pool) < 2:
                    next_generation.append(self.generate_random_query(allowed_features))
                else:
                    parent1 = random.choice(crossover_pool)
                    parent2 = random.choice(crossover_pool)
                    child = self.crossover(parent1, parent2)
                    mutated_child = self.mutate(child, allowed_features)
                    next_generation.append(mutated_child)
        return next_generation

    def run(self):
        population = None  # Initialize population as None

        for generation in range(self.genetic_params.generations):
            # At the beginning of each generation, select 15 random features
            allowed_features = random.sample(
                list(self.criteria.keys()) + self.cat_criteria, 15
            )

            # For the first generation, initialize the population
            if population is None:
                population = self.initialize_population(allowed_features)

            results = []

            with concurrent.futures.ThreadPoolExecutor(
                max_workers=os.cpu_count()
            ) as executor:
                futures = {
                    executor.submit(
                        evaluate_individual,
                        query,
                        self.training_data,
                        self.target,
                        self.MIN_ROWS,
                        self.genetic_params.average_column,
                    ): query
                    for query in population
                }

                for future in concurrent.futures.as_completed(futures):
                    query = futures[future]
                    try:
                        fitness, avg_target, row_count = future.result()
                        results.append((query, fitness, avg_target, row_count))
                    except Exception as exc:
                        logging.error(f"Query {query} generated an exception: {exc}")

            # Select elites
            population_with_fitness = [
                (res[0], res[1], res[3])
                for res in results  # (query, fitness, row_count)
            ]
            elites = self.select_parents(population_with_fitness)

            # Print the top 10
            print(f"Generation {generation + 1}:")
            top_results = sorted(results, key=lambda x: x[1], reverse=True)[:10]
            table = PrettyTable(["Query", "Fitness", "Avg Target", "Row Count"])
            for res in top_results:
                query_str = self.generate_query_string(res[0])
                table.add_row([query_str, res[1], res[2], res[3]])
            print(table)

            # Create the next generation population, passing allowed_features
            population = self.create_next_generation(
                elites, top_results, allowed_features
            )


def evaluate_individual(
    query_conditions, training_data, target, min_rows, average_column
):
    """Apply query and calculate fitness."""
    filtered_df = training_data

    for condition in query_conditions:
        column, min_value, max_value, column_type = condition
        if column_type == "numeric":
            filtered_df = filtered_df[
                (filtered_df[column] >= min_value) & (filtered_df[column] <= max_value)
            ]
        elif column_type == "categorical":
            value = min_value
            filtered_df = filtered_df[filtered_df[column] == value]

        if filtered_df.empty:
            break  # Early exit if no data left

    if len(filtered_df) < min_rows:
        return 0, 0, 0  # Low fitness for too few rows

    fitness = filtered_df[target].mean().round(2)
    avg_target = filtered_df[average_column].mean().round(2)
    row_count = len(filtered_df)

    return fitness, avg_target, row_count
