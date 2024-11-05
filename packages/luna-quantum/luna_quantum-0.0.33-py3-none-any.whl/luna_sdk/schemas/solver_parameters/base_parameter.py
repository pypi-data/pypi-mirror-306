from pydantic import BaseModel, ConfigDict


class BaseParameter(BaseModel):
    model_config = ConfigDict(extra="forbid")
