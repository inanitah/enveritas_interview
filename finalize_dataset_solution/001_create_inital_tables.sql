 CREATE TABLE dataset (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL
);
    CREATE TABLE question (
        id SERIAL PRIMARY KEY,
        text TEXT NOT NULL,
        answer_validation_schema JSONB NOT NULL,
        answer_contains_personal_identifying_information BOOL NOT NULL
);
    CREATE TABLE observation (
        id SERIAL PRIMARY KEY,
        dataset_id INT NOT NULL REFERENCES dataset(id) ON DELETE CASCADE,
        observed_on TIMESTAMP WITH TIME ZONE NOT NULL,
        rejected BOOL NOT NULL DEFAULT FALSE
);
    CREATE TABLE observation_answer (
        id SERIAL PRIMARY KEY,
        observation_id INT NOT NULL REFERENCES observation(id) ON DELETE CASCADE,
        question_id INT NOT NULL REFERENCES question(id) ON DELETE RESTRICT,
        original_answer_value JSONB NOT NULL,
        override_answer_value JSONB,
        override_comment TEXT,
        active_answer_value JSONB NOT NULL GENERATED ALWAYS AS (
            COALESCE(override_answer_value, original_answer_value)
        ) STORED
);