-- Insert test data into dataset table
INSERT INTO dataset (name) VALUES ('Test Dataset 1');
INSERT INTO dataset (name) VALUES ('Test Dataset 2');

-- Insert test data into question table
INSERT INTO question (text, answer_validation_schema, answer_contains_personal_identifying_information)
VALUES ('Test Question 1', '{}', FALSE);

-- Insert test data into observation table
INSERT INTO observation (dataset_id, observed_on) VALUES (1, NOW());
INSERT INTO observation (dataset_id, observed_on) VALUES (2, NOW());

-- Insert test data into observation_answer table
INSERT INTO observation_answer (observation_id, question_id, original_answer_value) VALUES (1, 1, '{"answer": "original 1"}');
INSERT INTO observation_answer (observation_id, question_id, original_answer_value) VALUES (2, 1, '{"answer": "original 2"}');
