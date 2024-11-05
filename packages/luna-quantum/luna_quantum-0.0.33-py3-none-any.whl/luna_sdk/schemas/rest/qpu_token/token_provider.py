from typing import Optional, Union

from pydantic import BaseModel, Extra

from luna_sdk.schemas import QpuToken, TokenProvider, QpuTokenSource
from luna_sdk.schemas.rest.qpu_token.qpu_token_source import _RESTQpuTokenSource


class _RestQpuToken(BaseModel):
    source: _RESTQpuTokenSource
    # A unique name for a stored token
    name: Optional[str] = None
    # This could be a QPU token, an API key or any token key for a QPU provider.
    # If the token is not passed from this API call, one stored in the user's
    # account will be used.
    token: Optional[str] = None

    @classmethod
    def from_qpu_token(cls, qpu_token: Optional[QpuToken]) -> Optional["_RestQpuToken"]:
        if qpu_token is None:
            return None
        # Organizational tokens were renamed to group in #1851
        # For smoother transition we only change naming in the SDK,
        # and therefore we need a mapping between Group and Organization here.
        # However, in backend for now QPU tokens still has source organization
        # TODO: Remove it when backend I/O schema is changed
        if qpu_token.source == QpuTokenSource.GROUP:
            return cls(
                source=_RESTQpuTokenSource.ORGANIZATION,
                name=qpu_token.name,
                token=qpu_token.token,
            )
        return cls.model_validate(qpu_token, from_attributes=True)


class AWSQpuTokens(BaseModel):
    aws_access_key: _RestQpuToken
    aws_secret_access_key: _RestQpuToken


class RestAPITokenProvider(BaseModel):
    dwave: Optional[_RestQpuToken] = None
    ibm: Optional[_RestQpuToken] = None
    fujitsu: Optional[_RestQpuToken] = None
    qctrl: Optional[_RestQpuToken] = None
    aws: Optional[AWSQpuTokens] = None

    @classmethod
    def from_sdk_token_provider(
        cls, token_provider: TokenProvider
    ) -> "RestAPITokenProvider":
        aws: Optional[AWSQpuTokens] = None
        if (
            token_provider.aws_access_key is not None
            or token_provider.aws_secret_access_key is not None
        ):
            # Ignoring mypy here to receive validation error, because we always need 2 tokens for aws
            aws = AWSQpuTokens(
                aws_access_key=_RestQpuToken.from_qpu_token(
                    getattr(token_provider, "aws_access_key", None)
                ),  # type: ignore[arg-type]
                aws_secret_access_key=_RestQpuToken.from_qpu_token(
                    getattr(  # type: ignore[arg-type]
                        token_provider, "aws_secret_access_key", None
                    )
                ),
            )
        return cls(
            dwave=_RestQpuToken.from_qpu_token(token_provider.dwave),
            ibm=_RestQpuToken.from_qpu_token(token_provider.ibm),
            fujitsu=_RestQpuToken.from_qpu_token(token_provider.fujitsu),
            qctrl=_RestQpuToken.from_qpu_token(token_provider.qctrl),
            aws=aws,
        )

    class Config:
        extra = Extra.forbid
