import numpy as np
from pyroll.core import Hook, SymmetricRollPass

VERSION = "3.0.0"

SymmetricRollPass.Roll.flattening_ratio = Hook[float]()
"""The ratio between flattened and nominal radius of the roll."""

SymmetricRollPass.Roll.flattened_radius = Hook[float]()
"""Flattened roll radius acc. to Hitchcock."""


@SymmetricRollPass.Roll.flattening_ratio
def flattening_ratio(self: SymmetricRollPass.Roll):
    """Calculates the ratio between flattened and initial roll radius using Hitchcocks formula."""
    roll_pass = self.roll_pass

    elastic_constant = (16 * (1 - self.poissons_ratio ** 2)) / (np.pi * self.elastic_modulus)
    height_change = roll_pass.in_profile.equivalent_rectangle.height - roll_pass.out_profile.equivalent_rectangle.height
    mean_width = (roll_pass.in_profile.equivalent_rectangle.width
                  + roll_pass.out_profile.equivalent_rectangle.width) / 2

    flattening_hitchcock = (elastic_constant * roll_pass.roll_force) / (height_change * mean_width)

    if flattening_hitchcock < 4.235:
        ratio = 1 + flattening_hitchcock

    else:
        ratio = 2 * flattening_hitchcock ** (2 / 3)

    self.logger.info(f"Calculated radius ratio of {ratio:.2f}")
    return ratio


@SymmetricRollPass.Roll.flattened_radius
def flattened_radius(self: SymmetricRollPass.Roll):
    """Calculates the flattened radius."""
    roll_pass = self.roll_pass

    if "roll_force" not in roll_pass.__dict__:
        radius = self.nominal_radius
    else:

        radius = roll_pass.roll.flattening_ratio * roll_pass.roll.nominal_radius
        self.logger.info(f"Calculated a roll radius of {radius * 1e3:.2f} mm using Hitchcook's model!")

    return radius


@SymmetricRollPass.Roll.max_radius
def max_radius(self: SymmetricRollPass.Roll):
    if self.has_value("flattened_radius"):
        radius = self.flattened_radius
        return radius


@SymmetricRollPass.Roll.min_radius
def min_radius(self: SymmetricRollPass.Roll):
    if self.has_value("flattened_radius"):
        radius = self.flattened_radius - self.groove.depth
        return radius


@SymmetricRollPass.Roll.working_radius
def working_radius(self: SymmetricRollPass.Roll):
    if self.has_value("flattened_radius"):
        radius = self.flattened_radius - self.groove.cross_section.centroid.y
        return radius
