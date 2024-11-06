from attr import dataclass


@dataclass
class ClientAuthorizationData:
    token: str
