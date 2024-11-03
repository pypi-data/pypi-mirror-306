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
