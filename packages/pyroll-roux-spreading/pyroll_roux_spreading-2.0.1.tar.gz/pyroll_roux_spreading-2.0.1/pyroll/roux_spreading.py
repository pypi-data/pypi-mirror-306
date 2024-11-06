import numpy as np
from pyroll.core import BaseRollPass, root_hooks, Unit, ThreeRollPass
from pyroll.core.hooks import Hook

VERSION = "2.0.1"

root_hooks.add(Unit.OutProfile.width)

BaseRollPass.first_roux_parameter = Hook[float]()
"""First parameter a of Roux's spread equation."""

BaseRollPass.second_roux_parameter = Hook[float]()
"""Second parameter b of Roux's spread equation."""


@BaseRollPass.first_roux_parameter
def first_roux_parameter(self: BaseRollPass):
    equivalent_height_change = self.in_profile.equivalent_height - self.out_profile.equivalent_height

    if np.isclose(equivalent_height_change, 0):
        return 1

    return (1 + 5 * (
            0.35 - equivalent_height_change / self.in_profile.equivalent_height) ** 2) * np.sqrt(
        self.in_profile.equivalent_height / equivalent_height_change - 1)


@BaseRollPass.second_roux_parameter
def second_roux_parameter(self: BaseRollPass):
    return (self.in_profile.equivalent_width / self.in_profile.equivalent_height - 1) * (
            self.in_profile.equivalent_width / self.in_profile.equivalent_width) ** (
            2 / 3)


@BaseRollPass.spread
def spread(self: BaseRollPass):
    equivalent_height_change = self.in_profile.equivalent_height - self.out_profile.equivalent_height

    second_factor = 1 / (
            (1 - equivalent_height_change / self.in_profile.equivalent_height) + (3 * self.first_roux_parameter) / (
            (2 * self.roll.working_radius) / self.in_profile.equivalent_height) ** (3 / 4))

    third_factor = (self.in_profile.equivalent_width / self.in_profile.equivalent_height) / (
            1 + 0.57 * self.second_roux_parameter)

    return 1 + (equivalent_height_change * second_factor * third_factor) / self.in_profile.equivalent_width


@BaseRollPass.OutProfile.width
def width(self: BaseRollPass.OutProfile):
    rp = self.roll_pass

    if not self.has_set_or_cached("width"):
        return None

    return rp.spread * rp.in_profile.width
