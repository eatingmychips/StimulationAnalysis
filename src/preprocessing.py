import pandas as pd 
import numpy as np 
from scipy import stats
import math 

def exp_weighted_ma(part, alpha):
    """An application of an exponential weighted moving average filter to 
    smooth data - alpha close to 1 means minimal smoothing"""
    # Initialize empty lists to store x and y coordinates separately
    partx = []
    party = []
    
    # Separate x and y coordinates from the input list
    for i in part: 
        partx.append(i[0])
        party.append(i[1])
    
    # Convert lists to pandas Series for easier manipulation
    partx = pd.Series(partx)
    party = pd.Series(party)
    
    # Apply exponential weighted moving average to x coordinates
    # Round to 5 decimal places and convert back to list
    partx = round(partx.ewm(alpha, adjust=False).mean(), 5)
    partx = partx.tolist()

    # Apply exponential weighted moving average to y coordinates
    # Round to 5 decimal places and convert back to list
    party = round(party.ewm(alpha, adjust=False).mean(), 5)
    party = party.tolist()

    # Combine smoothed x and y coordinates back into a single list
    smooth_data = []
    for i in range(len(partx)):
        smooth_data.append([partx[i], party[i]])

    # Return the smoothed data
    return smooth_data


def remove_outliers_and_smooth(data, alpha=0.1, z_thresh=2):
    """
    Removes outliers from 2D data and applies EWMA smoothing.
    - data: list of [x, y] points
    - alpha: EWMA smoothing factor (0 < alpha <= 1)
    - z_thresh: z-score threshold for outlier detection
    """
    # Convert to numpy array for easier math
    arr = np.array(data)
    x, y = arr[:, 0], arr[:, 1]
    
    # Outlier detection using z-score
    z_x = np.abs(stats.zscore(x, nan_policy='omit'))
    z_y = np.abs(stats.zscore(y, nan_policy='omit'))
    mask = (z_x < z_thresh) & (z_y < z_thresh)
    
    # Remove outliers
    # x_clean, y_clean = x[mask], y[mask]
    
    # Or maybe we can replace outliers with NaN and interpolate 
    x_clean = x.copy()
    y_clean = y.copy()
    x_clean[~mask] = np.nan
    y_clean[~mask] = np.nan
    x_clean = pd.Series(x_clean).interpolate().bfill().ffill().values
    y_clean = pd.Series(y_clean).interpolate().bfill().ffill().values
    
    # Apply EWMA smoothing
    x_smooth = pd.Series(x_clean).ewm(alpha=alpha, adjust=False).mean().values
    y_smooth = pd.Series(y_clean).ewm(alpha=alpha, adjust=False).mean().values
    
    # Combine back to [x, y] pairs
    smoothed_data = np.column_stack((x_smooth, y_smooth)).tolist()
    return smoothed_data # mask shows which points were kept

def remove_outliers_and_smooth_1d(data, alpha=0.1, z_thresh=2):
    """
    Removes outliers from 1D data and applies EWMA smoothing.
    - data: list of numeric values
    - alpha: EWMA smoothing factor (0 < alpha <= 1)
    - z_thresh: z-score threshold for outlier detection
    """
    arr = np.array(data, dtype=float)  # convert to float for NaN support

    # Outlier detection using z-score
    z = np.abs(stats.zscore(arr, nan_policy='omit'))
    mask = z < z_thresh

    # Replace outliers with NaN and interpolate
    clean = arr.copy()
    clean[~mask] = np.nan
    clean = pd.Series(clean).interpolate().bfill().ffill().values

    # Apply EWMA smoothing
    smooth = pd.Series(clean).ewm(alpha=alpha, adjust=False).mean().values

    return smooth.tolist()

def angle_interpolate(values): 
    angles_deg = [math.degrees(x) if x is not None else float('nan') for x in values]
    arr = np.array(angles_deg, dtype = np.float64)
    nans = np.isnan(arr)
    if nans.any(): 
        arr[nans] = np.interp(np.flatnonzero(nans), np.flatnonzero(~nans), arr[~nans])

    return arr.tolist()


def pos_interpolate(pos):
    """
    pos: list of [x, y] (with values or None)
    Returns a list of [x, y] with None values interpolated.
    """
    pos_array = np.array([
        [v if v is not None else np.nan for v in pt]
        for pt in pos
    ], dtype=np.float64)  # shape (n, 2)

    # Interpolate x and y independently
    for i in range(2):  # For x and y
        col = pos_array[:, i]
        nans = np.isnan(col)
        if nans.any() and (~nans).any():
            col[nans] = np.interp(
                np.flatnonzero(nans),
                np.flatnonzero(~nans),
                col[~nans]
            )
        pos_array[:, i] = col

    # Convert back to list of lists
    return pos_array.tolist()