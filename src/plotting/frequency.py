import matplotlib.pyplot as plt
import numpy as np 
from pathlib import Path 


FIG_DIR = Path(__file__).resolve().parents[2] / "outputs" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def get_max_values(lateral_vel, fwd_vel, body_angle, ang_vel):


    #fig, axes = plt.subplots(len(4), 1, figsize=(12, 25), sharex=True)

    all_measures = [lateral_vel, fwd_vel, body_angle, ang_vel]

    lateral_max = {}
    fwd_vel_max = {}
    body_angle_max = {}
    ang_vel_max = {}

    max_induced_dicts = [lateral_max, fwd_vel_max, body_angle_max, ang_vel_max]

    
    for unit, dict in zip(all_measures, max_induced_dicts): 
        for key, value in unit.items():
            for list in value: 
                during_stim = list[int(0.15/1.15*len(list)):int(0.65/1.15*len(list))]
                if key not in dict: 
                    dict[key]  = []
                if key[0] == "Right":           
                    dict[key].append(min(during_stim)) 
                elif key[0] == "Left": 
                    dict[key].append(max(during_stim))
                elif key[0] == "Both":
                    if dict is fwd_vel_max:
                        dict[key].append(abs(max(during_stim)))
                    else:
                        dict[key].append(max(during_stim, key=abs))

    return lateral_max, fwd_vel_max, body_angle_max, ang_vel_max


def frequency_plot(data_dict, frequencies, title, save=False, suffix=""):
    # Create a single figure for the boxplot
    fig, ax = plt.subplots(figsize=(12, 8))

    # Prepare data for boxplots
    box_data = []       # Combined data for all frequencies
    positions = []      # X-axis positions for boxplots
    colors = []         # Colors for each boxplot

    # Iterate through frequencies and collect data
    for idx, freq in enumerate(frequencies):

        list1 = data_dict.get(("Right", freq), [])
        list2 = data_dict.get(("Left", freq), [])
        if len(list1) > 0:  # Add "Right" data if available
            box_data.append(list1)
            positions.append(freq)  # X-axis position corresponds to frequency
            colors.append("red")  # Color for "Right"

        if len(list2) > 0:  # Add "Left" data if available
            box_data.append(list2)
            positions.append(freq)  # X-axis position corresponds to frequency
            colors.append("green")   # Color for "Left"

    # Plot the boxplots
    boxplots = ax.boxplot(box_data, positions=positions, patch_artist=True, widths = 3.5)
    ax.axhline(y = 0, color = 'black', linestyle = '--', linewidth = 2)
    # Customize boxplot colors
    for patch, color in zip(boxplots['boxes'], colors):
        patch.set_facecolor(color)

    # Customize x-axis and labels
    ax.set_xticks(frequencies)  # Set x-ticks to frequencies
    ax.set_xticklabels(frequencies, fontsize=14)
    ax.set_xlabel("Frequency (Hz)", fontsize=16)
    ax.set_ylabel(title, fontsize=16)
    ax.set_title("Boxplot by Frequency", fontsize=18)
    ax.set_ylim(-75, 75)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)


    # Add a legend for "Right" and "Left"
    ax.legend(
        handles=[
            plt.Line2D([0], [0], color="red", lw=4, label="Right"),
            plt.Line2D([0], [0], color="green", lw=4, label="Left"),
        ],
        title="Side",
        loc="upper right",
        fontsize=12,
    )


    plt.tight_layout()
    if save:
        fname = f"frequency_plot{suffix}.png"
        fig.savefig(FIG_DIR / fname, dpi=300, bbox_inches="tight")
    plt.show()


def frequency_plot_elytra(data_dict, frequencies, title, save=False, suffix=""):
    fig, ax = plt.subplots(figsize=(12, 8))

    box_data = []
    positions = []
    colors = []

    for freq in frequencies:
        list1 = data_dict.get(("Both", freq), [])
        if freq == 10: 
            print(np.percentile(list1, 10))
        if len(list1) > 0:
            box_data.append(list1)
            positions.append(freq)
            colors.append("grey")

    # Explicitly handle empty data scenario
    if len(box_data) == 0:
        print("No data available for any frequency.")
        return

    # Plot boxplots
    boxplots = ax.boxplot(box_data, positions=positions, patch_artist=True, widths=5)

    # Customize colors
    for patch, color in zip(boxplots['boxes'], colors):
        patch.set_facecolor(color)

    # Set ticks to match positions exactly
    ax.set_xticks(positions)
    ax.set_xticklabels(positions, fontsize=14)

    ax.set_xlabel("Frequency (Hz)", fontsize=16)
    ax.set_ylabel(title, fontsize=16)
    ax.set_title("Boxplot by Frequency", fontsize=18)
    ax.set_ylim(-3, 80)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.legend(
        handles=[
            plt.Line2D([0], [0], color="grey", lw=4, label="Both Elytra Stimulation")
        ],
        loc="upper right",
        fontsize=12,
    )

    plt.grid(False)
    plt.tight_layout()
    if save:
        fname = f"frequency_plot_elytra{suffix}.png"
        fig.savefig(FIG_DIR / fname, dpi=300, bbox_inches="tight")
    plt.show()



def frequency_scatter_regression(data_dict, frequencies, title):
    import matplotlib.pyplot as plt
    import numpy as np

    fig, ax = plt.subplots(figsize=(12, 8))
    color_map = {'Right': 'red', 'Left': 'green'}
    side_data = {'Right': {'freqs': [], 'vals': []},
                 'Left': {'freqs': [], 'vals': []}}
    
    for freq in frequencies:
        for side in ("Right", "Left"):
            vals = data_dict.get((side, freq), [])
            if vals:
                # Jitter for visualization
                jitter = np.random.normal(0, 0.6, size=len(vals))
                jittered = [freq+j for j in jitter]
                ax.scatter(jittered, vals, color=color_map[side], alpha=0.7, s=60, edgecolor='k', label=side if freq==frequencies[0] else "")
                side_data[side]['freqs'].extend([freq]*len(vals))
                side_data[side]['vals'].extend(vals)
    
    # Regression per side, with equation and R^2 printouts
    for side in ("Right", "Left"):
        xs = np.array(side_data[side]['freqs'])
        ys = np.array(side_data[side]['vals'])
        if len(xs) > 1:
            coeffs = np.polyfit(xs, ys, 1)
            y_pred = np.polyval(coeffs, xs)
            # R^2 calculation
            ss_res = np.sum((ys - y_pred) ** 2)
            ss_tot = np.sum((ys - np.mean(ys)) ** 2)
            r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float('nan')
            # Print equation and R^2
            print(f"{side} Regression: y = {coeffs[0]:.4f}x + {coeffs[1]:.4f}, R^2 = {r2:.4f}")
            reg_x = np.linspace(min(frequencies), max(frequencies), 100)
            reg_y = np.polyval(coeffs, reg_x)
            ax.plot(reg_x, reg_y, color=color_map[side], lw=3, label=f"{side} Regression")
        
    ax.set_xticks(frequencies)
    ax.set_xticklabels(frequencies, fontsize=14)
    ax.set_xlabel("Frequency (Hz)", fontsize=16)
    ax.set_ylabel(title, fontsize=16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_title("Scatter by Frequency with Separate Regressions", fontsize=18)
    ax.axhline(y=0, color='black', linestyle='--', linewidth=2)
    handles = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', label='Right', markersize=10),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green', label='Left', markersize=10),
    ]
    ax.legend(title="Side", loc="upper right", fontsize=12)
    plt.tight_layout()
    plt.show()