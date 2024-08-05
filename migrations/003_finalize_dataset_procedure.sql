-- Finalize dataset function
CREATE OR REPLACE FUNCTION finalize_dataset(dataset_id INT) RETURNS VOID AS $$
BEGIN
    UPDATE dataset SET finalized = TRUE WHERE id = dataset_id;
END;
$$ LANGUAGE plpgsql;