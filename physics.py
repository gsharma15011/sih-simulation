import numpy as np

from environment import get_gravity, get_wind_velocity
from config import AIR_DENSITY, DRAG_COEFFICIENT, REFERENCE_AREA, MASS


def calculate_drag(velocity,wind_velocity=None):
    if wind_velocity is None:
        wind_velocity = get_wind_velocity()

    relative_velocity = velocity - wind_velocity

    speed = np.linalg.norm(relative_velocity)

    if speed == 0:
        return np.zeros(3)

    drag_magnitude = (
        0.5
        * AIR_DENSITY
        * DRAG_COEFFICIENT
        * REFERENCE_AREA
        * speed**2
    )

    drag_direction = -relative_velocity / speed

    drag_force = drag_magnitude * drag_direction

    return drag_force


def calculate_acceleration(velocity,wind_velocity=None):

    gravity = get_gravity()

    drag_force = calculate_drag(
        velocity,
         wind_velocity
     )

    drag_acceleration = drag_force / MASS

    total_acceleration = gravity + drag_acceleration

    return total_acceleration