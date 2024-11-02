from typing import Optional

from airflow.providers.google.cloud.secrets.secret_manager import CloudSecretManagerBackend


class BetterGoogleCloudSecretManagerBackend(CloudSecretManagerBackend):
    """
    https://github.com/apache/airflow/issues/19251

    Add the option secret_lookup_prefix to the GCP CloudSecretManagerBackend
    when set this option will only look inside GCP secret manager the variables or connections prefixed
    with the same value

    example:

    with secret_lookup_prefix=None
    Variable.get("TOTO") will call the GCP secret provider
    Connection.get("TOTO") will call the GCP secret provider

    with secret_lookup_prefix="secret_"
    Variable.get("TOTO") will NOT call the GCP secret provider
    Variable.get("secret_TOTO") will call the GCP secret provider with TOTO ( without the prefix secret_ )
    Connection.get("TOTO") will NOT call the GCP secret provider
    Connection.get("secret_TOTO") will call the GCP secret provider with TOTO ( without the prefix secret_ )

    """

    def __init__(
            self,
            secret_lookup_prefix: Optional[str] = None,
            **kwargs,
    ):
        super().__init__(**kwargs)
        self.secret_lookup_prefix = secret_lookup_prefix

    def get_variable(self, key: str) -> Optional[str]:
        if self.variables_prefix is None:
            return None

        if self.secret_lookup_prefix is not None:
            if not key.startswith(self.secret_lookup_prefix):
                return None
            else:
                key = key[len(self.secret_lookup_prefix):]

        return self._get_secret(self.variables_prefix, key)

    def get_conn_uri(self, conn_id: str) -> Optional[str]:
        if self.connections_prefix is None:
            return None

        if self.secret_lookup_prefix is not None:
            if not conn_id.startswith(self.secret_lookup_prefix):
                return None
            else:
                conn_id = conn_id[len(self.secret_lookup_prefix):]

        return self._get_secret(self.connections_prefix, conn_id)