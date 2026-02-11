from pathlib import Path
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1] 
sys.path.append(str(PROJECT_ROOT))

from src.config import VERTICAL_DATA_DIR, FREQUENCIES
from src.config import VERTICAL_DATA_DIR, FREQUENCIES
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
    files = load_files(VERTICAL_DATA_DIR)
    lateral_velocity, forward_velocity, body_angles, angular_velocity, summary = run_stat_analysis(files)

    # Save max values (your existing JSON writes)
    outputs_dir = Path("outputs/json")
    outputs_dir.mkdir(parents=True, exist_ok=True)

    lateral_max, fwd_max, angles_max, ang_vel_max = get_max_values(
        lateral_velocity, forward_velocity, body_angles, angular_velocity
    )

    with open(outputs_dir / "angles_max_vert.json", "w") as f:
        json.dump({str(k): v for k, v in angles_max.items()}, f)

    with open(outputs_dir / "fwd_max_vert.json", "w") as f:
        json.dump({str(k): v for k, v in fwd_max.items()}, f)

    # Antenna plots
    antenna_time_plot_single(body_angles, 30, "Angular Deviation (degrees)")
    antenna_time_plot(body_angles, FREQUENCIES, "Angular Deviation (degrees)", save=True)
    antenna_trials_plot(body_angles, FREQUENCIES, "Angular Deviation (degrees)", save=True)
    frequency_plot(angles_max, FREQUENCIES, "Angular Deviation (degrees)", save=True)

    # Elytra plots
    elytra_time_plot_single(forward_velocity, 30, "Forward Velocity (mm/s)")
    elytra_time_plot(forward_velocity, FREQUENCIES, "Forward Velocity (mm/s)", save=True)
    elytra_trials_plot(forward_velocity, FREQUENCIES, "Forward Velocity (mm/s)", save=True)
    frequency_plot_elytra(fwd_max, FREQUENCIES, "Forward Velocity (mm/s)", save=True)

if __name__ == "__main__":
    main()
