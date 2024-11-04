import hvac

from mind_castle.stores.vault import HashiCorpVaultSecretStore


def test_put_secret():
    secret_store = HashiCorpVaultSecretStore()
    response = secret_store.put_secret("some_secret_value")

    # Read the secret from vault directly to check
    client = hvac.Client(url="http://localhost:8200", token="myroot")
    response = client.secrets.kv.read_secret_version(path=response["key"])
    assert response["data"]["data"].get("secret_value") == "some_secret_value"


def test_get_secret():
    secret_store = HashiCorpVaultSecretStore()
    # Add secret directly to vault
    client = hvac.Client(url="http://localhost:8200", token="myroot")
    client.secrets.kv.v2.create_or_update_secret(
        path="some_secret_key2", secret=dict(secret_value="some_secret_value")
    )

    assert secret_store.get_secret("some_secret_key2") == "some_secret_value"
