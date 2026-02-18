from pathlib import Path
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1] 
sys.path.append(str(PROJECT_ROOT))

from src.config import VERTICAL_DATA_DIR, FREQUENCIES, C0_DIRECTORY, C3_DIRECTORY, C4_DIRECTORY, C9_DIRECTORY, C10_DIRECTORY
from src.stats_pipeline import load_files, run_stat_analysis
from src.plotting.time_series import (
    antenna_time_plot,
    antenna_time_plot_single,
    elytra_time_plot,
    elytra_time_plot_single,
    antenna_trials_plot,
    elytra_trials_plot,
)
from src.plotting.frequency import (
    get_max_values,
    frequency_plot,
    frequency_plot_elytra,
    frequency_scatter_regression, 
    all_roach_mean_std_plot, 
    all_roach_cerci_plot
)


def main():
    files = load_files(VERTICAL_DATA_DIR)
    
    lateral_velocity, forward_velocity, body_angles, angular_velocity, summary = run_stat_analysis(files)

    print(body_angles)

    # print("Number of Turning trials is: ", summary["turning_succ_no"])
    # print("Success Turning is: ", summary["turning_succ_no"] / (summary["turning_succ_no"] + summary["turning_fail_no"]))

    # print("Number of forward trials is: ", summary["elytra_succ_no"])
    # print("Success Forward is: ", summary["elytra_succ_no"] / (summary["elytra_succ_no"] + summary["elytra_fail_no"]))

    antenna_trials_plot(body_angles, FREQUENCIES, "Trials", save=True)

    # Save max values (your existing JSON writes)
    outputs_dir = Path("outputs/json")
    outputs_dir.mkdir(parents=True, exist_ok=True)

    lateral_max_all, fwd_max_all, angles_max_all, ang_vel_max = get_max_values(
        lateral_velocity, forward_velocity, body_angles, angular_velocity
    )

    files_C0 = load_files(C0_DIRECTORY)
    files_C3 = load_files(C3_DIRECTORY)
    files_C4 = load_files(C4_DIRECTORY)
    files_C9 = load_files(C9_DIRECTORY)
    files_C10 = load_files(C10_DIRECTORY)

    individual_roaches = [files_C0, files_C3, files_C4, 
                          files_C9, files_C10]
    
    roach_ids = ["C0", "C3", "C4", "C9", "C10"]

    results = {}
    for roach_id, roach_file in zip(roach_ids, individual_roaches): 
        lateral_velocity, forward_velocity, body_angles, angular_velocity, summary = run_stat_analysis(roach_file)
        lateral_max, fwd_max, angles_max, ang_vel_max = get_max_values(lateral_velocity, forward_velocity, 
                                                                       body_angles, angular_velocity)
        results[roach_id] = { 
            "lateral_max": lateral_max, 
            "fwd_max": fwd_max, 
            "angles_max": angles_max 
        }   

    all_roach_mean_std_plot(
    angles_dict_all=angles_max_all,
    results=results,
    frequencies=FREQUENCIES,
    direction="Right",
    title="Turning Angle (degs)",
    save=True,
    suffix="_Right",
    )

    all_roach_mean_std_plot(
    angles_dict_all=angles_max_all,
    results=results,
    frequencies=FREQUENCIES,
    direction="Left",
    title="Turning Angle (degs)",
    save=True,
    suffix="_Left",
    )

    individual_roaches = [files_C10, files_C3, files_C4, 
                          files_C9]
    
    roach_ids = ["C10", "C3", "C4", "C9"]

    results = {}
    for roach_id, roach_file in zip(roach_ids, individual_roaches): 
        lateral_velocity, forward_velocity, body_angles, angular_velocity, summary = run_stat_analysis(roach_file)
        lateral_max, fwd_max, angles_max, ang_vel_max = get_max_values(lateral_velocity, forward_velocity, 
                                                                       body_angles, angular_velocity)
        results[roach_id] = { 
            "lateral_max": lateral_max, 
            "fwd_max": fwd_max, 
            "angles_max": angles_max 
        }   
    all_roach_cerci_plot(
    fwd_max_all,
    results=results,
    frequencies=FREQUENCIES,
    direction="Both", 
    title="Forward Velocity (mm / s)",
    save=True,
    suffix="",
    )
if __name__ == "__main__":
    main()
