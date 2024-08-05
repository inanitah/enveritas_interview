-- This migration contains:
--  1. Add finalized column to dataset table
--  2. Dataset triggers and functions
--  3. Observation triggers and functions
--  4. Observation answer triggers and functions


-- 1. Add finalized column to dataset table
ALTER TABLE dataset ADD COLUMN finalized BOOL NOT NULL DEFAULT FALSE;

-- 2. Dataset triggers and functions

-- Function to prevent deletions of dataset if finalized
CREATE OR REPLACE FUNCTION dataset_prevent_deletion_if_finalized()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT finalized FROM dataset WHERE id = OLD.id) THEN
        RAISE EXCEPTION 'Deletion not allowed: Dataset is finalized.';
    END IF;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Prevent deletion of datasets if finalized
CREATE TRIGGER prevent_dataset_deletion_if_finalized
BEFORE DELETE ON dataset
FOR EACH ROW EXECUTE FUNCTION dataset_prevent_deletion_if_finalized();

-- 3. Observation triggers and functions

-- Function to prevent deletions of observation if dataset is finalized
CREATE OR REPLACE FUNCTION observation_prevent_deletion_if_finalized()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT finalized FROM dataset WHERE id = OLD.dataset_id) THEN
        RAISE EXCEPTION 'Deletion not allowed: Dataset is finalized.';
    END IF;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Prevent deletion of observations if dataset is finalized
CREATE TRIGGER prevent_observation_deletion_if_finalized
BEFORE DELETE ON observation
FOR EACH ROW EXECUTE FUNCTION observation_prevent_deletion_if_finalized();

-- Function to prevent insertion of new observations if dataset is finalized
CREATE OR REPLACE FUNCTION observation_prevent_insertion_if_finalized()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT finalized FROM dataset WHERE id = NEW.dataset_id) THEN
        RAISE EXCEPTION 'Insertion not allowed: Dataset is finalized.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Prevent insertion of new observations if dataset is finalized
CREATE TRIGGER prevent_observation_insertion_if_finalized
BEFORE INSERT ON observation
FOR EACH ROW EXECUTE FUNCTION observation_prevent_insertion_if_finalized();


-- Function to prevent update of observation rejection status if the related dataset is finalized
CREATE OR REPLACE FUNCTION observation_prevent_rejection_status_change_if_finalized()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'UPDATE' AND NEW.rejected IS DISTINCT FROM OLD.rejected AND
        (SELECT finalized FROM dataset WHERE id = OLD.dataset_id)) THEN
        RAISE EXCEPTION 'Rejection status change not allowed: Dataset is finalized.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Prevent update of observations rejection status if dataset is finalized
CREATE TRIGGER prevent_observation_rejection_status_change_if_finalized
BEFORE UPDATE OF rejected ON observation
FOR EACH ROW EXECUTE FUNCTION observation_prevent_rejection_status_change_if_finalized();

-- 4. Observation answer triggers and functions

-- Function to prevent changes to the original answer value after creation
CREATE OR REPLACE FUNCTION observation_answer_prevent_original_modification()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'UPDATE' AND NEW.original_answer_value IS DISTINCT FROM OLD.original_answer_value) THEN
        RAISE EXCEPTION 'Original answer value cannot be modified.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Prevent changes to the original answer value after creation
CREATE TRIGGER prevent_observation_answer_original_modification
BEFORE UPDATE ON observation_answer
FOR EACH ROW EXECUTE FUNCTION observation_answer_prevent_original_modification();

-- Function to prevent observation answer deletions if the related dataset is finalized
CREATE OR REPLACE FUNCTION observation_answer_prevent_deletion_if_finalized()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT finalized
        FROM dataset
        WHERE id = (SELECT dataset_id FROM observation WHERE id = OLD.observation_id)) THEN
        RAISE EXCEPTION 'Deletion not allowed: Related dataset is finalized.';
    END IF;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Prevent deletion of observation answers if dataset is finalized
CREATE TRIGGER prevent_observation_answer_deletion_if_finalized
BEFORE DELETE ON observation_answer
FOR EACH ROW EXECUTE FUNCTION observation_answer_prevent_deletion_if_finalized();

-- Function to prevent observation answer modifications if the related dataset is finalized
CREATE OR REPLACE FUNCTION observation_answer_prevent_modification_if_finalized()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT finalized
        FROM dataset
        WHERE id = (SELECT dataset_id FROM observation WHERE id = NEW.observation_id)) THEN
        RAISE EXCEPTION 'Modification not allowed: Related dataset is finalized.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Prevent update of observation answers if related dataset is finalized
CREATE TRIGGER prevent_observation_answer_update_if_finalized
BEFORE UPDATE ON observation_answer
FOR EACH ROW EXECUTE FUNCTION observation_answer_prevent_modification_if_finalized();

-- Prevent insertion of new observation answers if related dataset is finalized
CREATE TRIGGER prevent_observation_answer_insertion_if_finalized
BEFORE INSERT ON observation_answer
FOR EACH ROW EXECUTE FUNCTION observation_answer_prevent_modification_if_finalized();


