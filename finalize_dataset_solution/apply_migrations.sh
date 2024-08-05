#!/bin/bash

# Concatenate all SQL files into a single migration file
cat 001_create_inital_tables.sql 002_add_finalized_boolean_and_create_triggers.sql 003_finalize_dataset_procedure.sql > all_migrations.sql

# Apply the combined migration file to the database
psql -U mikeradzewicz -d testdb -f all_migrations.sql

rm all_migrations.sql
