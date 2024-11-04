import boto3
import json


def get_secret(secret_name: str) -> dict:
    """
    Retrieves a secret from AWS Secrets Manager.

    :param secret_name: Name of the secret to retrieve.
    :return: Dictionary containing the secret's key-value pairs.
    """
    client = boto3.client("secretsmanager")

    try:
        response = client.get_secret_value(SecretId=secret_name)
        return json.loads(response["SecretString"])
    except Exception as e:
        print(f"Error retrieving secret: {e}")
        return {}