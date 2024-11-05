from pydantic import BaseModel, Extra


class QpuTokenIn(BaseModel):
    """
    Pydantic model for creation QPU token.

    Attributes
    ----------
    name: str
        Name of the QPU token
    provider: ProviderEnum
        Name of provider
    token: str
        Token
    encryption_key: str
        Encryption key to be used for encryption of QPU tokens.
    """

    name: str
    provider: str
    token: str
    encryption_key: str

    class Config:
        extra = Extra.forbid
