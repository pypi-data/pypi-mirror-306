import numpy as np
from pyroll.core import BaseRollPass, Hook

VERSION = "2.0.2"

BaseRollPass.roll_gap_ratio = Hook[float]()
"""Calculate cross-section ratio used in Hensel-Poluchin master curves."""

BaseRollPass.rolling_efficiency = Hook[float]()
"""Calculate rolling efficiency according to Hensel-Poluchin master curve."""

BaseRollPass.lever_arm_coefficient = Hook[float]()
"""Calculate lever coefficient according to Hensel-Poluchin master curve."""


@BaseRollPass.roll_gap_ratio
def roll_gap_ratio(self: BaseRollPass):
    mean_cross_section = (self.in_profile.cross_section.area + 2 * self.out_profile.cross_section.area) / 3
    return self.roll.contact_area / mean_cross_section


@BaseRollPass.rolling_efficiency
def rolling_efficiency(self: BaseRollPass):
    inverse_efficiency = (0.9901 + 0.106 * self.roll_gap_ratio + 0.0283 * self.roll_gap_ratio ** 2
                          + 1.5718 * np.exp(-2.4609 * self.roll_gap_ratio)
                          + 0.3117 * np.exp(-15.625 * self.roll_gap_ratio ** 2))
    return inverse_efficiency ** -1


@BaseRollPass.DiskElement.deformation_resistance
def deformation_resistance(self: BaseRollPass.DiskElement):
    mean_flow_stress = (self.in_profile.flow_stress + self.out_profile.flow_stress) / 2
    return mean_flow_stress / self.roll_pass.rolling_efficiency


@BaseRollPass.deformation_resistance
def deformation_resistance(self: BaseRollPass):
    mean_flow_stress = (self.in_profile.flow_stress + 2 * self.out_profile.flow_stress) / 3
    return mean_flow_stress / self.rolling_efficiency


@BaseRollPass.lever_arm_coefficient
def lever_arm_coefficient(self: BaseRollPass):
    mean_temperature = (self.in_profile.temperature + self.out_profile.temperature) / 2
    return ((np.exp(-0.6 * self.roll_gap_ratio) + 0.076 * self.roll_gap_ratio)
            * self.velocity ** 0.005 * np.exp(
                -0.0003 * (mean_temperature - 273.15 - 900)))


@BaseRollPass.roll_force
def roll_force(self: BaseRollPass):
    return self.deformation_resistance * self.roll.contact_area


@BaseRollPass.Roll.roll_torque
def roll_torque(self: BaseRollPass.Roll):
    return self.roll_pass.roll_force * self.contact_length * self.roll_pass.lever_arm_coefficient
