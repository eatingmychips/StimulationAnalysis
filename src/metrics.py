import numpy as np 
from scipy import stats 



def get_post_stim(pose, stim_deets, stim_occur, fps):
    """
    Extracts data occurring just before and after a stimulation.
    
    This function should be used BEFORE applying EWMA filters to extract moments of interest.
    The post_frames and pre_frames variables can be adjusted to change the extraction window.
    
    Args:
    pose (list): List containing x, y, angle details.
    stim_deets (list): List containing stimulation details.
    stim_occur (list): List indicating stimulation occurrences (1 for stimulation, 0 otherwise).
    fps (int): Frames per second of the recording.

    Returns:
    tuple: A tuple containing stimulation details and extracted body part coordinates.
    """
    #Define the dictionary
    stim_dict = {}

    # Define the extraction window
    post_frames = int(fps * 1.25) 
    pre_frames = int(fps * 0.15)   
    
    # Find indices where stimulation occurred
    stim_index = [i for i, x in enumerate(stim_occur) if x == 1]
    
    
    # Extract data for the last stimulation
    for stim in stim_index:
        start = stim - pre_frames
        end = stim + post_frames
        if start < 0 or end > len(pose): 
            continue
        # Extract body part coordinates within the defined window
        pose_sect = pose[stim-pre_frames:stim+post_frames]
        
        
        # Get stimulation details
        side = stim_deets[stim][0]
        freq = stim_deets[stim][1]

        if (side, freq) not in stim_dict: 
            stim_dict[(side, freq)] = []

        stim_dict[(side, freq)].append(pose_sect)

    return stim_dict


def statistical_significance(data1, data2): 
    # Convert data to numpy arrays
    array1 = np.array(data1)
    array2 = np.array(data2)

    # Perform independent samples t-test
    t_statistic, p_value = stats.ttest_ind(array1, array2)

    # Print results
    print(f"T-statistic: {t_statistic}")
    print(f"P-value: {p_value}")

    # Interpret the results
    alpha = 0.05  # Set your significance level
    if p_value < alpha:
        print("Reject the null hypothesis. There is a significant difference between the two groups.")
    else:
        print("Fail to reject the null hypothesis. There is no significant difference between the two groups.")


def trial_is_outlier(angles, fwd_vel, key): 
    for i in range(len(angles) - 5): 
        if abs(angles[i] - angles[i+5]) > 40: 
            return True 
    if np.isnan(angles).all(): 
        return True
    
    if key[0] == "Right": 
        if angles[-1] > 5: 
            return True

    if key[0] == "Left": 
        if angles[-1] < -5:
            return True
        
    if key[0] == "Both": 
        if min(fwd_vel) < -5: 
            return True
    
    return False

def turning_fail(angles, key): 
    angles = angles[int(0.15/1.15*len(angles)):int(0.65/1.15*len(angles))]

    if key[0] == "Right": 
        if min(angles) > -3: 
            return True

    if key[0] == "Left": 
        if max(angles) < 3:
            return True

    return False


def elytra_fail(fwd_vel, key): 
    fwd_vel = fwd_vel[int(0.15/1.15*len(fwd_vel)):int(0.65/1.15*len(fwd_vel))]
    if key[0] == "Both": 
        if max(fwd_vel) < 3: 
            return True 
        
    return False