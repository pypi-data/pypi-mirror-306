from enum import *
from types import *
from typing import *
from drivers.driver import Driver
from drivers.oscillograph.zds.zds5054.zds5054pro import ZDS5054ProDriver
from drivers.oscillograph.zds.zds2024.zds2024c import ZDS2024CDriver
from drivers.multimeter.dmm6000 import DMM6000Driver


class CustomStrEnum(Enum):
    """A custom base class for string Enums.

    This class provides better type hinting for the value property.
    """

    @property
    def name(self) -> str:  # pylint: disable=function-redefined,invalid-overridden-method
        """Return the name of the Enum member."""
        return self._name_  # pylint: disable=no-member

    @property
    def value(self) -> str:  # pylint: disable=invalid-overridden-method
        """Return the value of the Enum member."""
        return cast(str, self._value_)  # pylint: disable=no-member

    @classmethod
    def list_values(cls) -> List[str]:
        """Return a list of all the values of the enum."""
        return [enum_entry.value for enum_entry in cls]


class SupportedDriver(CustomStrEnum):
    ZDS5054PRO = "ZDS5054PRO"
    ZDS2024C = "ZDS2024C"
    DMM6000 = "multimeter"
    DMM6001 = "DMM6001"


INST_DRIVER_MAP: Mapping[SupportedDriver, Type[Driver]] = {
    SupportedDriver.ZDS5054PRO: ZDS5054ProDriver,
    SupportedDriver.ZDS2024C: ZDS2024CDriver,
    SupportedDriver.DMM6000: DMM6000Driver,
    SupportedDriver.DMM6001: DMM6000Driver
}

INST_DRIVER_MAPPING_GROUP: Mapping[str, Type[Driver]] = MappingProxyType(
    {key.value: value for key, value in INST_DRIVER_MAP.items()}
)
