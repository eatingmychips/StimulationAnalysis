import numpy as np
import pandas as pd


def body_vel(pos, angles, fps):
    """Calculate the in-line and transverse velocities of the beetle.
    
    Args:
        pos: position as [[x, y], [x1, y1], .....]
        fps (int): frames per second that the data has been recorded at. 
    
    Returns:
        tuple: A tuple containing lists of in-line velocity and signed transverse velocity.
               Transverse velocity is negative in one direction and positive in the opposite direction.
    """

    body_v_in_line = []
    body_v_transverse = []

    for i in range(1, len(pos)):
        # Velocity vector of middle point
        delta = np.subtract(pos[i], pos[i-1])

        
        fwd_vector = [np.cos(np.radians(angles[i])), np.sin(np.radians(angles[i]))]
        norm = np.linalg.norm(fwd_vector)
        body_axis_unit = fwd_vector / norm

        # Calculate perpendicular vector to body axis (rotated 90 degrees CCW)
        perp_body_axis_unit = np.array([-body_axis_unit[1], body_axis_unit[0]])

        # Calculate velocities
        in_line_velocity = np.dot(delta, body_axis_unit)
        transverse_velocity = np.dot(delta, perp_body_axis_unit)

        pixels_per_mm = 4.1033
        scale_factor = fps/pixels_per_mm
        body_v_in_line.append(in_line_velocity * scale_factor)
        body_v_transverse.append(transverse_velocity * scale_factor)

        # Lateral velocity with sign using dot product with perpendicular axis
        lateral_velocity_signed = np.dot(delta, perp_body_axis_unit) * scale_factor
        body_v_transverse.append(lateral_velocity_signed)

    # Exponential smoothing
    alpha = 0.25
    body_v_in_line = pd.Series(body_v_in_line).ewm(alpha=alpha, adjust=False).mean()
    body_v_in_line = round(body_v_in_line, 5).tolist()
    
    body_v_transverse = pd.Series(body_v_transverse).ewm(alpha=alpha, adjust=False).mean()
    body_v_transverse = round(body_v_transverse, 5).tolist()
    
    # Normalization (baseline subtraction)
    ref_idx = int(0.1 * fps)
    if ref_idx >= len(body_v_in_line):
        ref_idx = 0

    ref_in_line = body_v_in_line[ref_idx]
    ref_transverse = body_v_transverse[ref_idx]

    body_v_in_line = [v - ref_in_line for v in body_v_in_line]
    body_v_transverse = [v - ref_transverse for v in body_v_transverse]

    return body_v_in_line, body_v_transverse

def get_body_angles(angles, fps):
    # Initialize normalized angles list with the first angle
    
    normalized_angles = [angles[0]] 
    
    # Normalize subsequent angles to avoid large jumps
    for i in range(1, len(angles)):
        # Calculate the difference between current and previous angle
        delta = angles[i] - angles[i - 1]
        
        # Adjust for jumps greater than 180 degrees
        # This ensures the smallest angle difference is always used
        delta = (delta + 180) % 360 - 180
        
        # Add the adjusted delta to the previous normalized angle
        normalized_angles.append(normalized_angles[-1] + delta)

    reference = reference = normalized_angles[int(0.15 * fps)]
    # Return the list of normalized angles
    return [angle - reference for angle in normalized_angles]

def get_ang_vel(angles, fps):
    """Calculate angular velocity (degs/s) from a list of angles over uniform time intervals (specify fps)."""
    if len(angles) < 2:
        return []  # Not enough data to calculate velocity

    angular_velocities = []
    time_interval = 1 / fps  # Time interval between measurements in seconds (100fps)

    for i in range(2, len(angles)):
        delta_angle = angles[i] - angles[i - 1]  # Change in angle
        angular_velocity = delta_angle / time_interval  # Angular velocity = delta_angle / delta_time
        angular_velocities.append(angular_velocity)

    return angular_velocities