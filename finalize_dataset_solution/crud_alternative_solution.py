import psycopg2
from psycopg2.extras import RealDictCursor

# Database connection
conn = psycopg2.connect(
    dbname="testdb",
    user="",
    password="",
    host="localhost"
)

def fetch_one(query, params=None):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query, params)
        return cur.fetchone()

def execute_query(query, params=None):
    with conn.cursor() as cur:
        cur.execute(query, params)
        conn.commit()

def finalize_dataset(dataset_id):
    query = "UPDATE dataset SET finalized = TRUE WHERE id = %s"
    execute_query(query, (dataset_id,))

def can_modify_dataset(dataset_id):
    dataset = fetch_one("SELECT finalized FROM dataset WHERE id = %s", (dataset_id,))
    return dataset and not dataset['finalized']

def insert_observation(dataset_id, observed_on):
    if can_modify_dataset(dataset_id):
        query = "INSERT INTO observation (dataset_id, observed_on) VALUES (%s, %s)"
        execute_query(query, (dataset_id, observed_on))
    else:
        print("Insertion not allowed: Dataset is finalized.")

def update_observation_rejected(observation_id, rejected):
    observation = fetch_one("SELECT dataset_id FROM observation WHERE id = %s", (observation_id,))
    if observation and can_modify_dataset(observation['dataset_id']):
        query = "UPDATE observation SET rejected = %s WHERE id = %s"
        execute_query(query, (rejected, observation_id))
    else:
        print("Rejection status change not allowed: Dataset is finalized.")

def update_observation_answer(observation_answer_id, override_answer_value=None, override_comment=None):
    observation_answer = fetch_one("SELECT observation_id FROM observation_answer WHERE id = %s", (observation_answer_id,))
    if observation_answer:
        observation = fetch_one("SELECT dataset_id FROM observation WHERE id = %s", (observation_answer['observation_id'],))
        if observation and can_modify_dataset(observation['dataset_id']):
            query = "UPDATE observation_answer SET override_answer_value = %s, override_comment = %s WHERE id = %s"
            execute_query(query, (override_answer_value, override_comment, observation_answer_id))
        else:
            print("Modification not allowed: Dataset is finalized.")

def delete_dataset(dataset_id):
    if can_modify_dataset(dataset_id):
        query = "DELETE FROM dataset WHERE id = %s"
        execute_query(query, (dataset_id,))
    else:
        print("Deletion not allowed: Dataset is finalized.")

def delete_observation(observation_id):
    observation = fetch_one("SELECT dataset_id FROM observation WHERE id = %s", (observation_id,))
    if observation and can_modify_dataset(observation['dataset_id']):
        query = "DELETE FROM observation WHERE id = %s"
        execute_query(query, (observation_id,))
    else:
        print("Deletion not allowed: Dataset is finalized.")

def delete_observation_answer(observation_answer_id):
    observation_answer = fetch_one("SELECT observation_id FROM observation_answer WHERE id = %s", (observation_answer_id,))
    if observation_answer:
        observation = fetch_one("SELECT dataset_id FROM observation WHERE id = %s", (observation_answer['observation_id'],))
        if observation and can_modify_dataset(observation['dataset_id']):
            query = "DELETE FROM observation_answer WHERE id = %s"
            execute_query(query, (observation_answer_id,))
        else:
            print("Deletion not allowed: Dataset is finalized.")


# Example Usage
if __name__ == "__main__":
    finalize_dataset(1)
    insert_observation(1, '2023-08-01 10:00:00')  # Should print: Insertion not allowed: Dataset is finalized.
    insert_observation(2, '2023-08-01 10:00:00')  # Should succeed
    update_observation_rejected(1, True)  # Should print: Rejection status change not allowed: Dataset is finalized.
    update_observation_rejected(2, True)  # Should succeed
    update_observation_answer(1, '{"answer": "modified"}', 'New comment')  # Should print: Modification not allowed: Dataset is finalized.
    update_observation_answer(2, '{"answer": "modified"}', 'New comment')  # Should succeed
    delete_dataset(1)  # Should print: Deletion not allowed: Dataset is finalized.
    delete_dataset(2)  # Should succeed
    delete_observation(1)  # Should print: Deletion not allowed: Dataset is finalized.
    delete_observation(2)  # Should succeed
    delete_observation_answer(1)  # Should print: Deletion not allowed: Dataset is finalized.
    delete_observation_answer(2)  # Should succeed
