from __future__ import annotations
from enum import Enum
import operator


class Length:
    
    class UnitType(Enum):
        MILIMETER = "milimeter"
        METER = "meter"
        KILOMETER = "kilometer"

        @classmethod
        def get_unit_types(cls) -> list[str]:
            return [unit.value for unit in cls]
    
    # multipying factors for converting key-unit into meter-unit
    __CONVERSION_FACTOR: dict[str, float] = {
        UnitType.MILIMETER.value: 1e-3,
        UnitType.METER.value: 1,
        UnitType.KILOMETER.value: 1e3,
    }

    # checks if input unitType is valid unitType 
    def __get_checked_input_unit(self, unit: str | UnitType | None) -> str | None:
        if not unit:
            return None
        
        if isinstance(unit, self.UnitType):
            unit = unit.value

        if unit not in self.__units:
            raise ValueError("Length Unit Invalid")
        
        return unit
    
    # checks if input value is valid value 
    def __get_checked_input_value(self, value: str | float | int | None, label="Length Value") -> float:
        try:
            value = float(value)
            if value < 0:
                raise ValueError(f"{label} Negative")
        except Exception:
            raise ValueError(f"{label} Invalid")
            
        return value
        
    def __init__(self, value: float | int | str, /, unit: str | UnitType = UnitType.METER) -> None:
        """
        Initializes a Length object.

        Paramters:
        ----------
        param1: (required) amount of Length
        param2: (optional) unitType of Length. By default = Length.UnitType.METER
        """
        self.__units = self.UnitType.get_unit_types()
        unit = self.__get_checked_input_unit(unit=unit)
        value = self.__get_checked_input_value(value=value)
        
        # mantaining value in meters for internal calculations
        self.__value = float(value * self.__CONVERSION_FACTOR[unit])
        self.__unit = str(unit)

    def convert_to(self, unit: str | UnitType, /) -> None:
        """
        Convert Length object to a specified unit.

        Paramters:
        ----------
        param1: (required) The target unitType for conversion
        """
        unit = self.__get_checked_input_unit(unit=unit)
        self.__unit = unit
    
    @property
    def value(self) -> float:
        return self.__get_value_in_units(value=self.__value, unit=self.__unit)
    
    @property
    def unit(self) -> str:
        return self.__unit
    
    # string representation of Length object
    def __repr__(self) -> str:
        return f"{type(self).__name__}(value={self.value},unit={self.unit})"
    
    # converts value into unitType from meters
    def __get_value_in_units(self, value: float, unit: str) -> float:
        return float(value / self.__CONVERSION_FACTOR[unit])
    
    # helper function for adding & subtracting Length values
    def __addition_subtraction_helper(
        self, self_value: float, self_unit: str, other_value: float, other_unit: str, operation
    ) -> tuple[float, str]:
        """
        if self_unit == other_unit:
            returns (some_value (in self_unit), self_unit)
        else:
            returns (some_value (in smaller_unit_type), smaller_unit_type)
        """
        new_value, new_unit = None, None
        self_factor = self.__CONVERSION_FACTOR[self_unit]
        other_factor = self.__CONVERSION_FACTOR[other_unit]
        divFactor = self_factor / other_factor
        
        if self_unit == other_unit:
            new_unit = self_unit
            new_value = float(operation(self_value, other_value))
        else:
            # factor < 1 means self_unit < other_unit
            new_unit = self_unit if divFactor < 1 else other_unit
            new_value = float(operation(float(self_value * self_factor), float(other_value * other_factor)))
            new_value = self.__get_value_in_units(value=new_value, unit=new_unit)

        if new_value < 0:
            new_value = float(0)
        
        return (new_value, new_unit)
    
    # dunder method for adding two Length objects, returns new Length object
    def __add__(self, other: Length) -> Length:
        new_value, new_unit = self.__addition_subtraction_helper(
            self_value=self.value,
            self_unit=self.unit,
            other_value=other.value,
            other_unit=other.unit,
            operation=operator.add
        )
        return Length(new_value, unit=new_unit)
    
    # dunder method for subtracting two Length objects, returns new Length object
    def __sub__(self, other: Length) -> Length:
        new_value, new_unit = self.__addition_subtraction_helper(
            self_value=self.value,
            self_unit=self.unit,
            other_value=other.value,
            other_unit=other.unit,
            operation=operator.sub
        )
        return Length(new_value, unit=new_unit)

    # dunder method for multiplying Length object by a factor, returns new Length object
    def __mul__(self, scalar: int | float | str) -> Length:
        scalar = self.__get_checked_input_value(
            value=scalar,
            label="Length Multiplication Factor"
        )
        return Length(float(self.value * scalar), unit=self.unit)
    
    # dunder method for dividing Length object by a factor, returns new Length object
    def __truediv__(self, scalar: int | float | str) -> Length:
        scalar = self.__get_checked_input_value(
            value=scalar,
            label="Length Division Factor"
        )
        return Length(float(self.value / scalar), unit=self.unit)
    
    # dunder method for int-dividing Length object by a factor, returns new Length object
    def __floordiv__(self, scalar: int | float | str) -> Length:
        scalar = self.__get_checked_input_value(
            value=scalar,
            label="Length Division Factor"
        )
        return Length(float(self.value // scalar), unit=self.unit)
    
    # dunder method for checking if Length object is strictly shorter than other Length object
    def __lt__(self, other: Length) -> bool:
        self_value = float(self.value * self.__CONVERSION_FACTOR[self.unit])
        other_value = float(other.value * self.__CONVERSION_FACTOR[other.unit])

        return self_value < other_value
    
    # dunder method for checking if Length object is shorter than or equals to other Length object
    def __le__(self, other: Length) -> bool:
        self_value = float(self.value * self.__CONVERSION_FACTOR[self.unit])
        other_value = float(other.value * self.__CONVERSION_FACTOR[other.unit])

        return self_value <= other_value
    
    # dunder method for checking if Length object is strictly greater than other Length object
    def __gt__(self, other: Length) -> bool:
        self_value = float(self.value * self.__CONVERSION_FACTOR[self.unit])
        other_value = float(other.value * self.__CONVERSION_FACTOR[other.unit])

        return self_value > other_value
    
    # dunder method for checking if Length object is greater than or equals to other Length object
    def __ge__(self, other: Length) -> bool:
        self_value = float(self.value * self.__CONVERSION_FACTOR[self.unit])
        other_value = float(other.value * self.__CONVERSION_FACTOR[other.unit])

        return self_value >= other_value
    
    # dunder method for checking if Length object is equals to other Length object
    def __eq__(self, other: Length) -> bool:
        self_value = float(self.value * self.__CONVERSION_FACTOR[self.unit])
        other_value = float(other.value * self.__CONVERSION_FACTOR[other.unit])

        return self_value == other_value