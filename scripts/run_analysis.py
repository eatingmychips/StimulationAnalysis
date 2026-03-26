from pathlib import Path
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1] 
sys.path.append(str(PROJECT_ROOT))

from src.config import FREQUENCIES, DATA_RAW
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
    frequency_plot_elytra
)


def main():
    files = load_files(DATA_RAW)
    lateral_velocity, forward_velocity, body_angles, angular_velocity, summary = run_stat_analysis(files)

    # Save max values (your existing JSON writes)
    outputs_dir = Path("outputs/json")
    outputs_dir.mkdir(parents=True, exist_ok=True)

    print("Number of Elytra trials is: ", summary["elytra_succ_no"])
    print("Success Elytra is: ", summary["elytra_succ_no"] / (summary["elytra_succ_no"] + summary["elytra_fail_no"]))


    lateral_max, fwd_max, angles_max, ang_vel_max = get_max_values(
        lateral_velocity, forward_velocity, body_angles, angular_velocity
    )

    with open(outputs_dir / "angles_max_vert_Acrylic.json", "w") as f:
        json.dump({str(k): v for k, v in angles_max.items()}, f)

    with open(outputs_dir / "fwd_max_vert_Acrylic.json", "w") as f:
        json.dump({str(k): v for k, v in fwd_max.items()}, f)

    # These are actually Elytra Time but we use antenna functions to get left / right functionality 
    antenna_time_plot_single(lateral_velocity, 20, "Lateral Velocity (mm / s)", save=True)
    antenna_time_plot(lateral_velocity, FREQUENCIES, "Lateral Velocity (mm / s)", save=True)
    antenna_trials_plot(lateral_velocity, FREQUENCIES, "Lateral Velocity (mm / s)", save=True)
    frequency_plot(lateral_max, FREQUENCIES, "Lateral Velocity (mm / s)", save=True)

    # antenna_time_plot_forward(forward_velocity, FREQUENCIES, "Forward Velocity (mm / s)", save=True)

    
if __name__ == "__main__":
    main()
