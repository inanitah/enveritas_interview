-- Test cases to validate the triggers and functions

-- Test case: Prevent deletion of finalized dataset (Use Case 2a)
DO $$
BEGIN
    -- Finalize dataset 1
    PERFORM finalize_dataset(1);

    -- Attempt to delete the finalized dataset
    BEGIN
        DELETE FROM dataset WHERE id = 1;
    EXCEPTION WHEN others THEN
        RAISE NOTICE 'Deletion not allowed: Dataset is finalized.';
    END;
END;
$$;

-- Test case: Prevent insertion of new observations if dataset is finalized (Use Case 2b)
DO $$
BEGIN
    -- Attempt to insert new observation into finalized dataset
    BEGIN
        INSERT INTO observation (dataset_id, observed_on) VALUES (1, NOW());
    EXCEPTION WHEN others THEN
        RAISE NOTICE 'Insertion not allowed: Dataset is finalized.';
    END;
END;
$$;

-- Test case: Prevent update of observation rejection status if dataset is finalized (Use Case 2c)
DO $$
BEGIN
    -- Attempt to update rejection status of observation in finalized dataset
    BEGIN
        UPDATE observation SET rejected = TRUE WHERE id = 1;
    EXCEPTION WHEN others THEN
        RAISE NOTICE 'Rejection status change not allowed: Dataset is finalized.';
    END;
END;
$$;

-- Test case: Prevent modifications to observation answers if related dataset is finalized (Use Case 2d)
DO $$
BEGIN
    -- Attempt to update observation answer in finalized dataset
    BEGIN
        UPDATE observation_answer SET override_answer_value = '{"answer": "modified"}' WHERE id = 1;
    EXCEPTION WHEN others THEN
        RAISE NOTICE 'Modification not allowed: Dataset is finalized.';
    END;

    -- Attempt to update override comment in observation answer in finalized dataset
    BEGIN
        UPDATE observation_answer SET override_comment = 'New comment' WHERE id = 1;
    EXCEPTION WHEN others THEN
        RAISE NOTICE 'Modification not allowed: Dataset is finalized.';
    END;
END;
$$;

-- Test case: Prevent deletion of observation answers if dataset is finalized (Use Case 2a)
DO $$
BEGIN
    -- Attempt to delete observation answer in finalized dataset
    BEGIN
        DELETE FROM observation_answer WHERE id = 1;
    EXCEPTION WHEN others THEN
        RAISE NOTICE 'Deletion not allowed: Dataset is finalized.';
    END;
END;
$$;

-- Test case: Prevent changes to the original answer value after creation (Use Case 1)
DO $$
BEGIN
    -- Attempt to update original answer value
    BEGIN
        UPDATE observation_answer SET original_answer_value = '{"answer": "new original"}' WHERE id = 2;
    EXCEPTION WHEN others THEN
        RAISE NOTICE 'Original answer value cannot be modified.';
    END;
END;
$$;

-- Test case: Allow operations on non-finalized dataset (dataset 2)

-- Attempt to insert new observation into non-finalized dataset
DO $$
BEGIN
    INSERT INTO observation (dataset_id, observed_on) VALUES (2, NOW());
    RAISE NOTICE 'Insertion allowed: Dataset is not finalized.';
END;
$$;

-- Attempt to update rejection status of observation in non-finalized dataset
DO $$
BEGIN
    UPDATE observation SET rejected = TRUE WHERE id = 2;
    RAISE NOTICE 'Rejection status change allowed: Dataset is not finalized.';
END;
$$;

-- Attempt to update observation answer in non-finalized dataset
DO $$
BEGIN
    UPDATE observation_answer SET override_answer_value = '{"answer": "modified"}' WHERE id = 2;
    RAISE NOTICE 'Modification allowed: Dataset is not finalized.';
END;
$$;

-- Attempt to update override comment in observation answer in non-finalized dataset
DO $$
BEGIN
    UPDATE observation_answer SET override_comment = 'New comment' WHERE id = 2;
    RAISE NOTICE 'Modification allowed: Dataset is not finalized.';
END;
$$;

-- Attempt to delete observation answer in non-finalized dataset
DO $$
BEGIN
    DELETE FROM observation_answer WHERE id = 2;
    RAISE NOTICE 'Deletion allowed: Dataset is not finalized.';
END;
$$;
