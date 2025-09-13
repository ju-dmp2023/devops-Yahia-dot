from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.opertions import Opertions

T = TypeVar("T", bound="Calculation")


@_attrs_define
class Calculation:
    """
    Attributes:
        operation (Opertions):
        operand1 (float):
        operand2 (float):
    """

    operation: Opertions
    operand1: float
    operand2: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        operation = self.operation.value

        operand1 = self.operand1

        operand2 = self.operand2

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "operation": operation,
                "operand1": operand1,
                "operand2": operand2,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        operation = Opertions(d.pop("operation"))

        operand1 = d.pop("operand1")

        operand2 = d.pop("operand2")

        calculation = cls(
            operation=operation,
            operand1=operand1,
            operand2=operand2,
        )

        calculation.additional_properties = d
        return calculation

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
