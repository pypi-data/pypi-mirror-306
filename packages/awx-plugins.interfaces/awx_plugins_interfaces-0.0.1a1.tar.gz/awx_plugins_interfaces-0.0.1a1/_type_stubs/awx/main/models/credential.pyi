class ManagedCredentialType:
    def __init__(
        self,
        namespace: str,
        name: str,
        kind: str,
        inputs: dict[str, list[dict[str, bool | str] | str]],
        injectors: dict[str, dict[str, str]] | None = None,
        managed: bool = False,
    ): ...
