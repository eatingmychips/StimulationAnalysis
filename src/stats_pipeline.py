from collections import defaultdict
from pathlib import Path

from .io_utils import find_csv_filenames, file_read
from .preprocessing import angle_interpolate, pos_interpolate, remove_outliers_and_smooth, remove_outliers_and_smooth_1d
from .kinematics import get_body_angles, get_ang_vel, body_vel
from .metrics import turning_fail, trial_is_outlier, elytra_fail, get_post_stim
from .config import FREQUENCIES


def load_files(data_dir: Path):
    return [str(data_dir / fn) for fn in find_csv_filenames(data_dir)]


def run_stat_analysis(files):
    lateral_velocity = {}
    forward_velocity = {}
    body_angles = {}
    angular_velocity = {}

    turning_succ_no = 0
    turning_fail_no = 0
    elytra_succ_no = 0
    elytra_fail_no = 0

    turning_success_freq = defaultdict(list)
    elytra_success_freq = defaultdict(list)

    for file in files:
        parts, stim_deets, stim_occur, fps = file_read(file)
        stim_dict = get_post_stim(parts, stim_deets, stim_occur, fps)

        for key, value in stim_dict.items():
            for pose_lst in value:
                angles = [item[2] for item in pose_lst]
                angles = angle_interpolate(angles)
                pos = [[item[0], item[1]] for item in pose_lst]
                pos = pos_interpolate(pos)

                pos = remove_outliers_and_smooth(pos, alpha=0.2, z_thresh=2.5)
                angles = remove_outliers_and_smooth_1d(angles, alpha=0.2, z_thresh=2.5)

                body_angle = get_body_angles(angles, fps)
                ang_vel = get_ang_vel(body_angle, fps)
                in_line_vel, transv_vel = body_vel(pos, angles, fps)

                for dct in (lateral_velocity, forward_velocity, body_angles, angular_velocity):
                    dct.setdefault(key, [])

                # if turning_fail(body_angle, key):
                #     turning_success_freq[key[1]].append(0)
                #     turning_fail_no += 1
                #     continue

                if trial_is_outlier(body_angle, in_line_vel, key):
                    continue

                # if elytra_fail(in_line_vel, key):
                #     elytra_success_freq[key[1]].append(0)
                #     elytra_fail_no += 1

                lateral_velocity[key].append(transv_vel)
                forward_velocity[key].append(in_line_vel)
                body_angles[key].append(body_angle)
                angular_velocity[key].append(ang_vel)

                if key[0] == "Both":
                    elytra_succ_no += 1
                    elytra_success_freq[key[1]].append(1)


                elif key[0] in ("Right", "Left"):
                    turning_succ_no += 1
                    turning_success_freq[key[1]].append(1)

    summary = {
        "turning_succ_no": turning_succ_no,
        "turning_fail_no": turning_fail_no,
        "elytra_succ_no": elytra_succ_no,
        "elytra_fail_no": elytra_fail_no,
        "turning_success_freq": dict(turning_success_freq),
        "elytra_success_freq": dict(elytra_success_freq),
    }
    return lateral_velocity, forward_velocity, body_angles, angular_velocity, summary
