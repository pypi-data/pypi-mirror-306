from enum import Enum
from typing import Dict, Tuple, List, Union, Optional

from dimod import ConstrainedQuadraticModel, QuadraticModel
from pydantic import BaseModel

from luna_sdk.exceptions.transformation import WeightedConstraintException
from luna_sdk.schemas.optimization_formats.qm import QMSchema


class CQMVarType(str, Enum):
    SPIN = "SPIN"
    BINARY = "BINARY"
    INTEGER = "INTEGER"
    REAL = "REAL"


class QuadraticModelSchema(QMSchema):
    offset: Union[float, int]
    var_types: Dict[str, CQMVarType]


class CQMSense(str, Enum):
    Le = "<="
    Ge = ">="
    Eq = "=="


class CQMPenaltyEnum(str, Enum):
    linear = "linear"
    quadratic = "quadratic"


class CQMConstraintsSchema(BaseModel):
    qm: QuadraticModelSchema
    sense: CQMSense
    rhs: Union[float, int]
    label: str
    penalty: CQMPenaltyEnum


class CQMVariableSchema(BaseModel):
    var_type: CQMVarType
    name: str
    lower_bound: Optional[float]
    upper_bound: Optional[float]


class CQMSchema(BaseModel):
    constraints: Dict[str, CQMConstraintsSchema]
    objective: QuadraticModelSchema
    variables: List[CQMVariableSchema]

    @classmethod
    def from_cqm(cls, cqm: ConstrainedQuadraticModel) -> "CQMSchema":
        var_types = {v: CQMVarType[cqm.vartype(v).name] for v in cqm.variables}
        constraints = {}
        for name, constraint in cqm.constraints.items():
            if constraint.lhs.is_soft():
                raise WeightedConstraintException
            constr = CQMConstraintsSchema(
                qm=QuadraticModelSchema(
                    linear=constraint.lhs.linear,
                    quadratic=constraint.lhs.quadratic,
                    offset=constraint.lhs.offset,
                    var_types=var_types,
                ),
                sense=CQMSense[constraint.sense.name],
                rhs=constraint.rhs,
                label=name,
                penalty=CQMPenaltyEnum.linear,
            )
            constraints[name] = constr
        objective = QuadraticModelSchema(
            linear=cqm.objective.linear,
            quadratic=cqm.objective.quadratic,
            offset=cqm.objective.offset,
            var_types=var_types,
        )
        variables = []
        for var in cqm.variables:
            variables.append(
                CQMVariableSchema(
                    name=var,
                    var_type=var_types[var],
                    lower_bound=cqm.lower_bound(var),
                    upper_bound=cqm.upper_bound(var),
                )
            )
        return cls(
            constraints=constraints,
            objective=objective,
            variables=variables,
        )

    def to_cqm(self) -> ConstrainedQuadraticModel:
        cqm = ConstrainedQuadraticModel()
        for variable in self.variables:
            cqm.add_variable(vartype=variable.var_type, v=variable.name)
        for name, constraint in self.constraints.items():
            qm = QuadraticModel(
                linear=constraint.qm.linear,  # type: ignore[arg-type]
                quadratic=constraint.qm._parsed_quadratic,  # type: ignore[arg-type]
                offset=constraint.qm.offset,
                vartypes=constraint.qm.var_types,  # type: ignore[arg-type]
            )
            cqm.add_constraint_from_model(
                qm=qm,
                sense=constraint.sense,
                rhs=constraint.rhs,
                label=constraint.label,
                penalty=constraint.penalty,
            )
        objective = QuadraticModel(
            linear=self.objective.linear,  # type: ignore[arg-type]
            quadratic=self.objective._parsed_quadratic,  # type: ignore[arg-type]
            offset=self.objective.offset,
            vartypes=self.objective.var_types,  # type: ignore[arg-type]
        )
        cqm.set_objective(objective)
        for variable in self.variables:
            if variable.var_type not in (CQMVarType.BINARY, CQMVarType.SPIN):
                if variable.upper_bound is not None:
                    cqm.set_upper_bound(variable.name, variable.upper_bound)
                if variable.lower_bound is not None:
                    cqm.set_lower_bound(variable.name, variable.lower_bound)
        return cqm
