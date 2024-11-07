import pyarrow as pa
import pyarrow.flight as fl
import os
import requests


def sample(host=None, genuine=1000000, fraud=100000, seed=4711, from_days=180, to_days=30):
    """Returns a data sample for machine learning."""
    if host is None:
        host = os.environ.get("HOST", None)
    if host is None:
        raise Exception(
            "The flight server host must be either passed as the `host` argument or set in the `HOST` environment variable."
        )
    client = pa.flight.connect(host)
    reader = client.do_get(fl.Ticket("sample"))
    flight_data = reader.read_all()
    data = flight_data.to_pandas()
    data_genuine = data.iloc[:, data.columns != "Fraud"]
    data_fraud = data["Fraud"].astype("int")

    return data_genuine, data_fraud


def persist(pipeline_id, compute_id, model_name, model, host=None):
    """Persists a model in a scoring compute referenced by a pipeline and compute id"""
    if host is None:
        host = os.environ.get("UI_HOST", None)
    if host is None:
        raise Exception(
            "The FraudAverse UI server host must be either passed as the `host` argument or set in the `UI_HOST` environment variable."
        )
    try:
        response = requests.put(
            host + "/api/pipeline/" + pipeline_id + "/compute/" + compute_id + "/",
            json={"name": model_name, "model": model},
        )
        response.raise_for_status()  # Raises an HTTPError if the status code is 4xx, 5xx
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except requests.exceptions.RequestException as err:
        print(f"Request error occurred: {err}")

    return response.text
