# Finalization Problem Solution

## Introduction

This document provides a solution to the problem of finalizing datasets and preventing modifications after finalization. The solution involves using SQL triggers and functions to enforce the business rules. Additionally, we have included scripts for cleaning the database, setting up test data, and verifying the functionality of the triggers through various test cases.

## Solution Details

### Design Choices

- **Finalized Boolean**: A `finalized` boolean column was added to the `dataset` table to indicate whether the dataset is finalized. Once finalized, the dataset and its related data cannot be modified.
- **SQL Triggers**: Triggers are used to enforce the business rules. These triggers prevent deletions, insertions, and updates on finalized datasets, observations, and observation answers.

### Files and Their Purposes

1. **cleanup.sql**:
   - Drops existing tables, triggers, and functions to ensure a clean start.

2. **001_create_inital_tables.sql**:
   - Creates the necessary tables (`dataset`, `question`, `observation`, and `observation_answer`).

3. **002_add_finalized_boolean_and_create_triggers.sql**:
   - Adds the `finalized` boolean column to the `dataset` table.
   - Defines the functions and triggers to enforce the business rules.

4. **003_finalize_dataset_procedure.sql**:
   - Defines a stored procedure to finalize a dataset by setting its `finalized` column to `TRUE`.

5. **test_data.sql**:
   - Populates the database with test data for `dataset`, `question`, `observation`, and `observation_answer` tables.

6. **test_cases.sql**:
   - Contains test cases to verify that the triggers and functions work as expected. These tests include:
     - Preventing deletions of finalized datasets.
     - Preventing insertions of new observations into finalized datasets.
     - Preventing updates to the rejection status of observations in finalized datasets.
     - Preventing modifications to observation answers in finalized datasets.
     - Allowing operations on non-finalized datasets.

