from typing import Any, List, Literal, Optional, Tuple, Union

from numpy.typing import NDArray
from pydantic import ConfigDict, Field, field_serializer
from typing_extensions import Annotated

from luna_sdk.schemas.solver_parameters.base_parameter import BaseParameter

OneHot = Literal["no_way", "one_way", "two_way"]


class VarShapeBase(BaseParameter):
    name: str
    one_hot: OneHot = "no_way"


class WithConstantBits(VarShapeBase):
    shape: Optional[List[int]] = None
    constant_bits: Optional[NDArray] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_serializer("constant_bits")
    def serialize_constant_bits(self, constant_bits: Optional[NDArray], _):
        if constant_bits is None:
            return None
        return constant_bits.tolist()


class BitArrayShape(WithConstantBits):
    """An object of the class :class:`BitArrayShape` represents an array structure as part of a bit vector. It allows
    multidimensional indexed access to the bit variables of a :class:`BinPol` polynomial. :class:`BitArrayShape`
    objects are used inside :class:`VarShapeSet` objects, which organize index data of a complete bit vector for
    a polynomial. Bit variables of such polynomials can then be accessed by name and indices according
    to the shape specified in the :class:`BitArrayShape` object.

    Parameters
    ----------
    shape: List[int]
        shape of the index; specify the length of each dimension
    constant_bits: Optional[NDArray]
        numpy array of type int8 with same shape as the previous parameter containing 0 and 1 for constant bits and -1 variable bits
    one_hot: OneHot
        define variable as one_hot section
    axis_names: Optional[List[str]]
        Names for the axis.
    index_offsets: Optional[List[int]]
        index_offsets of the index, specify the index_offsets of each dimension
    """

    type: Literal["BitArrayShape"] = "BitArrayShape"
    axis_names: Optional[List[str]] = None
    index_offsets: Optional[List[int]] = None


class Variable(WithConstantBits):
    """A ``Variable`` is a binary polynomial, that represents a numerical value according to values of the underlying bits.
    The variable is defined by a value range and a specific representation scheme that is realized in respective
    inherited classes.

    Parameters
    ----------
    name: str
        name of the variable
    start: float
        first number in the list of values to be represented by the variable
    stop: float
        stop value for the list of numbers to be represented by the variable; stop is omitted
    step: float
        increment for the list of numbers to be represented by the variable
    shape: List[int]
        shape of the index; specify the length of each dimension
    constant_bits: Optional[NDArray]
        numpy array of type int8 with same shape as the previous parameter containing 0 and 1 for constant bits and -1 variable bits
    one_hot: OneHot
        define variable as one_hot section
    """

    type: Literal["Variable"] = "Variable"
    start: float
    stop: float
    step: float


class Category(VarShapeBase):
    """An object of the class :class:`Category` represents an array structure as part of a bit vector. It allows
    indexed access to the bit variables of a :class:`BinPol` polynomial. :class:`Category`
    objects are used inside :class:`VarShapeSet` objects, which organize index data of a complete bit vector for
    a polynomial. Bit variables of such polynomials can then be accessed by ``name`` and categorical indices according
    to the ``values`` specified in the :class:`BitArrayShape` object. A categorical index can be any sequence of
    unique values.

    Parameters
    ----------
    name: str
        name of the new index
    values: List[Any]
        list of unique values for this category
    one_hot: OneHot
        define variable as one_hot section
    axis_names: List[str]
        Names for the axis.
    """

    type: Literal["Category"] = "Category"
    values: List[Any] = []
    axis_names: Optional[List[str]] = None


VarDef = Annotated[
    Union[BitArrayShape, Variable, Category], Field(discriminator="type")
]


class OneHotGroup(BaseParameter):
    """O:class:`dadk.BinPol.OneHotGroup` is used to define a one-way-one-hot group within a set of bit variables.
    In particular, the entries of the one-way-one-hot group are specified as tuples including the name of the variable
    specified in a BitArrayShape and (optionally) the indices of the variable in every dimension. Here, a single number
    for a particular dimension means the index of the variable with the specified numbers in the dimensions is
    included in the one-way-one-hot group. Another possibility is to specify a list or a range of indices for each dimension in
    order to include all indices of the variables with these specified numbers in the dimensions in the one-way-one-hot group.
    Finally, one can specify the value None for a dimension. In this case, the whole range of that dimension is considered for the
    one-way-one-hot group.

    Parameters
    ----------
    entries: Union[List, Tuple]
        one or more Lists or Tuples specifying the members of a one-way-one-hot group.
    """

    entries: List[Union[List, Tuple]] = []


class VarShapeSet(BaseParameter):
    """:class:`dadk.BinPol.VarShapeSet` defines an indexing structure for the bits of a BinPol polynomial. Plain BinPol
    polynomials are defined on a set of bits indexed by a ``range(N)`` for some integer ``N``. The ``VarShapeSet`` lays
    a sequence of disjoint named sections over this linear structure. Bits within a section can be addressed by the
    defined name. With a ``BitArrayShape`` a section can be defined as multidimensional array and single bits in the
    section can be addressed by an appropriate tuple of indices. With a ``Variable`` definition the section represents
    a number encoded in certain bit schemes; in this case it is possible to retrieve the represented value instead of
    reading single bits.

    Parameters
    ----------
    var_defs: Union[BitArrayShape, Variable, Category]
        one or more section definitions of type :class:`BitArrayShape`, :class:`Variable` or :class:`Category`
    one_hot_groups: Optional[List[OneHotGroup]]
        optional list of special one_hot group definitions
    """

    var_defs: List[VarDef] = []
    one_hot_groups: Optional[List[OneHotGroup]] = None


class PartialConfig(BaseParameter):
    """:class:`PartialConfig` produces a dictionary that can be used to initialize bits for the annealing algorithm.

    The start state for an annealing or parallel tempering optimization can be specified.
    The used dictionary addresses bits with their flattened index. With the class
    :class:`PartialConfig` those bits can be specified on the symbolic level of
    :class:`BitArrayShape` or :class:`Variable` and the offsets in a :class:`VarShapeSet` are calculated automatically.
    Flat indices can be used directly, if they are known. For variables, indices are used directly and do not need
    to be adjusted by a global index consideration from the :class:`VarShapeSet`. After setting the start state accordingly,
    a string can be created with the method ``as_json``. If one_hot or two_hot specifications are given in :class:`VarShapeSet`, the dictionary
    generated in the methods ``get_dict`` or ``as_json`` is build up with respect to the set bit variables and one-way or two-way rules.

    The object is initialized by a :class:`VarShapeSet` object or None. An initialization with None can be used for :class:`BinPol`.

    Parameters
    ----------

    var_shape_set: Optional[VarShapeSet]
        This parameter should be an object of :class:`VarShapeSet` or ``None``
    auto_fill_cold_bits: bool
        In case ``var_shape_set`` is defined and contains a 1-hot group, and a hot bit is set to ``True`` and this parameter is also set to ``True``, then all related cold bits are set to ``False``. Default is ``True``
    """

    var_shape_set: Optional[VarShapeSet] = None
    auto_fill_cold_bits: bool = True
