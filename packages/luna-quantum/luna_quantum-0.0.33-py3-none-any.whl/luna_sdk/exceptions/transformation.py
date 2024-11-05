from luna_sdk.exceptions.luna_exception import LunaException


class TransformationException(LunaException):
    def __str__(self):
        return "An unexpected error occurred during transformation, please contact support or open an issue."


class WeightedConstraintException(LunaException):
    def __str__(self):
        return "Weighted constraints for CQM are not supported"
