import os

from luna_sdk.schemas.rest.qpu_token.qpu_token_source import _RESTQpuTokenSource
from luna_sdk.schemas.rest.qpu_token.token_provider import (
    RestAPITokenProvider,
    AWSQpuTokens,
    _RestQpuToken,
)


def extract_qpu_tokens_from_env() -> RestAPITokenProvider:
    ibm_token = os.environ.get("LUNA_IBM_TOKEN")
    dwave_token = os.environ.get("LUNA_DWAVE_TOKEN")
    qctrl_token = os.environ.get("LUNA_QCTRL_TOKEN")
    fujitsu_token = os.environ.get("LUNA_FUJITSU_TOKEN")
    aws_access_key = os.environ.get("LUNA_AWS_ACCESS_KEY")
    aws_access_secret_key = os.environ.get("LUNA_AWS_SECRET_ACCESS_KEY")
    return RestAPITokenProvider(
        ibm=_RestQpuToken(
            source=_RESTQpuTokenSource.INLINE,
            token=ibm_token,
        )
        if ibm_token
        else None,
        dwave=_RestQpuToken(
            source=_RESTQpuTokenSource.INLINE,
            token=dwave_token,
        )
        if dwave_token
        else None,
        qctrl=_RestQpuToken(
            source=_RESTQpuTokenSource.INLINE,
            token=qctrl_token,
        )
        if qctrl_token
        else None,
        fujitsu=_RestQpuToken(
            source=_RESTQpuTokenSource.INLINE,
            token=fujitsu_token,
        )
        if fujitsu_token
        else None,
        aws=AWSQpuTokens(
            aws_access_key=_RestQpuToken(
                source=_RESTQpuTokenSource.INLINE,
                token=aws_access_key,
            ),
            aws_secret_access_key=_RestQpuToken(
                source=_RESTQpuTokenSource.INLINE,
                token=aws_access_secret_key,
            ),
        ),
    )
