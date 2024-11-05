from pydantic import BaseModel


class LPSchema(BaseModel):
    lp_string: str

    @classmethod
    def from_lp(cls, lp: str) -> "LPSchema":
        return cls(lp_string=lp)
