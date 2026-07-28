import numpy as np
from dataclasses import dataclass

@dataclass
class barrier_inputs:
    """Class for keeping track of inputs."""
    water_depth: float
    kentledge_mass: float
    mu_membrane_ground: float
    mu_barrier_ground: float
    mu_kentledge_ground: float
    barrier_width: float = 1.0
    barrier_angle_deg: float = 38.7
    membrane_width: float = 2.0
    barrier_mass: float = 26.5
    alpha: float = 0.203          # Tuned as discussed in supporting document
    slope_height: float = 0.72
    required_fos: float = 1.5
    water_density: float = 1000.0
    gravity: float = 9.81


@dataclass
class barrier_outputs:
    """Class for keeping track of outputs."""
    slope_horiz_force: float
    vert_wall_horiz_force: float
    total_driving_force: float
    resisting_force: float
    actual_fos: float
    passes: bool
    required_kentledge_mass: float




def sliding_check(inputs: barrier_inputs) -> barrier_outputs:
    """Calculates the sliding check for a barrier.

    Args:
        inputs (barrier_inputs): The inputs for the sliding check.

    Returns:
        barrier_outputs: The outputs for the sliding check.
    """

    theta = np.deg2rad(inputs.barrier_angle_deg)

    h_wetted_slope = min(inputs.water_depth, inputs.slope_height)

    slope_horizontal_force = inputs.water_density * inputs.gravity * inputs.barrier_width * h_wetted_slope * (inputs.water_depth - 0.5 * h_wetted_slope)

    slope_vertical_force = slope_horizontal_force / np.tan(theta)

    h_wetted_vertical = max(
        inputs.water_depth - inputs.slope_height,
        0.0,
    )

    vertical_face_force = (
        0.5
        * inputs.water_density
        * inputs.gravity
        * h_wetted_vertical**2
        * inputs.barrier_width
    )

    driving_force = (
        slope_horizontal_force
        + vertical_face_force
    )

    membrane_load = (
        inputs.water_density
        * inputs.gravity
        * inputs.water_depth
        * inputs.membrane_width
        * inputs.barrier_width
        * inputs.alpha
    )

    barrier_weight = inputs.barrier_mass * inputs.gravity
    kentledge_weight = inputs.kentledge_mass * inputs.gravity

    membrane_resistance = (
        inputs.mu_membrane_ground
        * membrane_load
    )

    barrier_resistance = (
        inputs.mu_barrier_ground
        * barrier_weight
    )

    kentledge_resistance = (
        inputs.mu_kentledge_ground
        * kentledge_weight
    )

    total_resisting_force = (
        membrane_resistance
        + barrier_resistance
        + kentledge_resistance
    )

    if driving_force > 0:
        observed_fos = total_resisting_force / driving_force
    else:
        observed_fos = np.inf

    passes = observed_fos >= inputs.required_fos

    required_kentledge_mass_for_FoS = max(0, ((driving_force * inputs.required_fos - inputs.mu_membrane_ground * membrane_load - inputs.mu_barrier_ground * (barrier_weight + slope_vertical_force)) / (inputs.mu_kentledge_ground * inputs.gravity)))


    return barrier_outputs(
        slope_horiz_force_kN = slope_horizontal_force / 1000.0,
        vert_wall_horiz_force_kN = vertical_face_force / 1000.0,
        total_driving_force_kN = driving_force / 1000.0,
        resisting_force_kN = total_resisting_force / 1000.0,
        actual_fos = observed_fos,
        passes = passes,
        required_kentledge_mass_kg = required_kentledge_mass_for_FoS
    )