-- Drop triggers if they exist
DROP TRIGGER IF EXISTS prevent_dataset_deletion_if_finalized ON dataset;
DROP TRIGGER IF EXISTS prevent_observation_deletion_if_finalized ON observation;
DROP TRIGGER IF EXISTS prevent_observation_insertion_if_finalized ON observation;
DROP TRIGGER IF EXISTS prevent_observation_rejection_status_change_if_finalized ON observation;
DROP TRIGGER IF EXISTS prevent_observation_answer_deletion_if_finalized ON observation_answer;
DROP TRIGGER IF EXISTS prevent_observation_answer_update_if_finalized ON observation_answer;
DROP TRIGGER IF EXISTS prevent_observation_answer_insertion_if_finalized ON observation_answer;
DROP TRIGGER IF EXISTS prevent_observation_answer_original_modification ON observation_answer;

-- Drop functions if they exist
DROP FUNCTION IF EXISTS dataset_prevent_deletion_if_finalized;
DROP FUNCTION IF EXISTS observation_prevent_deletion_if_finalized;
DROP FUNCTION IF EXISTS observation_prevent_insertion_if_finalized;
DROP FUNCTION IF EXISTS observation_prevent_rejection_status_change_if_finalized;
DROP FUNCTION IF EXISTS observation_answer_prevent_modification_if_finalized;
DROP FUNCTION IF EXISTS observation_answer_prevent_deletion_if_finalized;
DROP FUNCTION IF EXISTS observation_answer_prevent_original_modification;
DROP FUNCTION IF EXISTS finalize_dataset;

-- Drop tables if they exist
DROP TABLE IF EXISTS observation_answer;
DROP TABLE IF EXISTS observation;
DROP TABLE IF EXISTS question;
DROP TABLE IF EXISTS dataset;
