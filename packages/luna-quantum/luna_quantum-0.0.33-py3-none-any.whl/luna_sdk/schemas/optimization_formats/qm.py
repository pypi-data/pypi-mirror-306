from typing import Any, Dict, Tuple

from pydantic import BaseModel, field_validator


class QMSchema(BaseModel):
    quadratic: Dict[str, float]
    linear: Dict[str, float]

    @property
    def _parsed_quadratic(self) -> Dict[Tuple[str, ...], float]:
        q = {}
        for k, v in self.quadratic.items():
            parsed_key = eval(k) if isinstance(k, str) else k
            formatted_key = tuple(
                str(x) if not isinstance(x, str) else x for x in parsed_key
            )
            q[formatted_key] = v
        return q

    @field_validator("quadratic", mode="before")
    @classmethod
    def transform_quadratic(cls, quadratic: Dict[Any, Any]) -> Dict[str, Any]:
        if quadratic:
            q = {}
            for k, v in quadratic.items():
                k = str(k) if not isinstance(k, str) else k
                q[k] = v
            return q
        return quadratic
