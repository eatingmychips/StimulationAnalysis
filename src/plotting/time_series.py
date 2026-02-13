import matplotlib.pyplot as plt
import numpy as np 
from pathlib import Path 

FIG_DIR = Path(__file__).resolve().parents[2] / "outputs" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def resample_1d_list(original_list, new_len):
    # Remove invalid (non-float) entries
    filtered = [x for x in original_list if isinstance(x, (float, int, np.float32, np.float64))]
    old_len = len(filtered)
    if old_len == 0:
        # Return a list of np.nan if no valid numbers remain
        return [np.nan] * new_len
    if old_len == 1:
        return [filtered] * new_len
    old_idx = np.linspace(0, 1, old_len)
    new_idx = np.linspace(0, 1, new_len)
    return np.interp(new_idx, old_idx, filtered).tolist()


def antenna_time_plot(data_dict, frequencies, title, save = False, suffix = ""):

    fig, axes = plt.subplots(2, 3, figsize=(12, 8))

    def process_list(data):
        data = np.array(data, dtype=object)
        max_len = max(len(sublist) for sublist in data)

        resampled_data = np.array([
        resample_1d_list(sublist, max_len) for sublist in data
            ], dtype=float)
        means = np.nanmean(resampled_data, axis=0)
        stds = np.nanstd(resampled_data, axis=0)
        lower = means - stds     # One std dev below the mean
        upper = means + stds     # One std dev above the mean
        return max_len, means, lower, upper

    axes_flat = axes.flatten()

    for idx, freq in enumerate(frequencies):
        ax = axes_flat[idx]

        
        # Use .get() with default empty list if key not found
        list1 = data_dict.get(("Right", freq), [])
        list2 = data_dict.get(("Left", freq), [])


        if len(list1) < 1 and len(list2) < 1:
            # If no data at all for this frequency, just create empty plot
            ax.set_title(f'Freq: {freq} Hz (No Data)', fontsize=18)
            ax.set_xlim(0, 1.25)
            ax.set_ylabel(title, fontsize=16)
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            continue
    
        # Only process and plot if data exists
        if len(list1) > 0:
            max_len1, medians1, lower_quartiles1, upper_quartiles1 = process_list(list1)
            x1 = np.linspace(0, 1.25, max_len1)
            mask1 = (x1 >= 0.15) & (x1 <= 0.65)
            ax.fill_between(x1, lower_quartiles1, upper_quartiles1, color='lightgrey', alpha=0.3)
            ax.plot(x1, medians1, color='black', linewidth=2)
            ax.fill_between(x1[mask1], lower_quartiles1[mask1], upper_quartiles1[mask1], color='lightcoral', alpha=0.3)
            ax.plot(x1[mask1], medians1[mask1], color='red', linewidth=2, label='Right Stimulation')

        if len(list2) > 0:
            max_len2, medians2, lower_quartiles2, upper_quartiles2 = process_list(list2)
            x2 = np.linspace(0, 1.25, max_len2)
            mask2 = (x2 >= 0.15) & (x2 <= 0.65)
            ax.fill_between(x2, lower_quartiles2, upper_quartiles2, color='lightgrey', alpha=0.3)
            ax.plot(x2, medians2, color='black', linewidth=2)
            ax.fill_between(x2[mask2], lower_quartiles2[mask2], upper_quartiles2[mask2], color='lightgreen', alpha=0.3)
            ax.plot(x2[mask2], medians2[mask2], color='green', linewidth=2, label='Left Stimulation')

            


        # Formatting subplot
        ax.set_title(f'Freq: {freq} Hz', fontsize=18)
        ax.set_xlim(0, 1.1)
        ax.set_ylim(-80, 80)
        ax.axhline(y=0, color='black', linestyle='--', linewidth=1)
        ax.set_ylabel(title, fontsize=16)
        if freq == 10:
            ax.legend(fontsize=14)

        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

    if len(frequencies) < len(axes_flat):
        fig.delaxes(axes_flat[-1])

    # Set x-label only to bottom row plots
    for i in range(len(axes_flat)):
        if i >= len(axes_flat) - 4:
            axes_flat[i].set_xlabel('Time (s)', fontsize=20)
                        # Set custom x-ticks and labels for this subplot
            xtick_positions = np.arange(0, 1.05, 0.2)  # Tick positions every 0.2 seconds
            xtick_labels = [f"{tick:.1f}" for tick in xtick_positions]  # Labels as strings
            ax.set_xticks(xtick_positions)
            ax.set_xticklabels(xtick_labels)
    
    plt.tight_layout(h_pad=0.35)
    if save:
        fname = f"antenna_time_plot{suffix}.png"
        fig.savefig(FIG_DIR / fname, dpi=300, bbox_inches="tight")





def elytra_time_plot(data_dict, frequencies, title, save=False, suffix=""):

    fig, axes = plt.subplots(2, 3, figsize=(12, 8))

    def process_list(data):
            data = np.array(data, dtype=object)
            max_len = max(len(sublist) for sublist in data)

            resampled_data = np.array([
            resample_1d_list(sublist, max_len) for sublist in data
                ], dtype=float)
            means = np.nanmean(resampled_data, axis=0)
            stds = np.nanstd(resampled_data, axis=0)
            lower = means - stds     # One std dev below the mean
            upper = means + stds     # One std dev above the mean
            return max_len, means, lower, upper

    axes_flat = axes.flatten()
    for idx, freq in enumerate(frequencies):
        ax = axes_flat[idx]

        
        # Use .get() with default empty list if key not found
        list1 = data_dict.get(("Both", freq), [])

        if len(list1) < 1:
            # If no data at all for this frequency, just create empty plot
            ax.set_title(f'Freq: {freq} Hz (No Data)', fontsize=18)
            ax.set_xlim(0, 1.05)
            ax.set_ylabel('Lateral velocity\n(mm/s)', fontsize=16)
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            continue

        if len(list1) > 0: 
            max_len1, medians1, lower_quartiles1, upper_quartiles1 = process_list(list1)

            x = np.linspace(0, 1.25, max_len1)
            mask = (x >= 0.1) & (x <= 0.6)

            # Right stimulation plot
            ax.fill_between(x[:len(medians1)], lower_quartiles1, upper_quartiles1,
                            color='lightgrey', alpha=0.3)
            ax.plot(x[:len(medians1)], medians1, color='black', linewidth=2)
            ax.fill_between(x[:len(medians1)][mask], lower_quartiles1[mask], upper_quartiles1[mask],
                            color='lightcoral', alpha=0.3)
            ax.plot(x[:len(medians1)][mask], medians1[mask],
                    color='red', linewidth=2, label='Both Elytra Stimulation')

        # Formatting subplot
        ax.set_title(f'Freq: {freq} Hz', fontsize=18)
        ax.set_xlim(0, 1.05)
        ax.set_ylabel(title, fontsize=16)
        ax.axhline(y=0, color='black', linestyle='--', linewidth=1)
        if freq == 10:
            ax.legend(fontsize=14)
        
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

    if len(frequencies) < len(axes_flat):
        fig.delaxes(axes_flat[-1])

    # Set x-label only to bottom row plots
    for i in range(len(axes_flat)):
        if i >= len(axes_flat) - 4:
            axes_flat[i].set_xlabel('Time (s)', fontsize=20)
                        # Set custom x-ticks and labels for this subplot
            xtick_positions = np.arange(0, 1.05, 0.2)  # Tick positions every 0.2 seconds
            xtick_labels = [f"{tick:.1f}" for tick in xtick_positions]  # Labels as strings
            ax.set_xticks(xtick_positions)
            ax.set_xticklabels(xtick_labels)

    plt.tight_layout(h_pad=0.35)
    if save:
        fname = f"elytra_time_plot{suffix}.png"
        fig.savefig(FIG_DIR / fname, dpi=300, bbox_inches="tight")


def antenna_time_plot_single(data_dict, frequency, title, save=False, suffix=""):
    fig, ax = plt.subplots(figsize=(9, 6), dpi=100)

    def process_list(data):
        data = np.array(data, dtype=object)
        max_len = max(len(sublist) for sublist in data)

        resampled_data = np.array([
        resample_1d_list(sublist, max_len) for sublist in data
            ], dtype=float)
        means = np.nanmean(resampled_data, axis=0)
        stds = np.nanstd(resampled_data, axis=0)
        lower = means - stds     # One std dev below the mean
        upper = means + stds     # One std dev above the mean
        return max_len, means, lower, upper

    
    # Use .get() with default empty list if key not found
    list1 = data_dict.get(("Right", frequency), [])
    list2 = data_dict.get(("Left", frequency), [])

    if len(list1) == 0 and len(list2) == 0:
        ax.set_title(f'Freq: {frequency} Hz (No Data)', fontsize=18)
        ax.set_xlim(0, 1.25)
        ax.set_ylabel(title, fontsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        plt.show()
        return

    max_len1, medians1, lower_quartiles1, upper_quartiles1 = process_list(list1)
    max_len2, medians2, lower_quartiles2, upper_quartiles2 = process_list(list2)

    x = np.linspace(0, 1.25, max(max_len1, max_len2))
    mask = (x >= 0.15) & (x <= 0.65)

    # Right stimulation plot
    ax.fill_between(x[:len(medians1)], lower_quartiles1, upper_quartiles1,
                    color='darkgrey', alpha=0.3)
    ax.plot(x[:len(medians1)], medians1, color='black', linewidth=2)
    ax.fill_between(x[:len(medians1)][mask], lower_quartiles1[mask], upper_quartiles1[mask],
                    color='lightcoral', alpha=0.3)
    ax.plot(x[:len(medians1)][mask], medians1[mask],
            color='red', linewidth=2, label='Right Stim - Inv')

    # Left stimulation plot
    ax.fill_between(x[:len(medians2)], lower_quartiles2, upper_quartiles2,
                    color='darkgrey', alpha=0.3)
    ax.plot(x[:len(medians2)], medians2,
            color='black', linewidth=2)
    
    ax.fill_between(x[:len(medians2)][mask], lower_quartiles2[mask], upper_quartiles2[mask],
                    color='lightgreen', alpha=0.3)
    ax.plot(x[:len(medians2)][mask], medians2[mask],
            color='green', linewidth=2, label='Left Stim - Inv')

    # ax.set_title(f'Freq: {frequency} Hz', fontsize=18)
    
    ax.set_ylabel(title, fontsize=21)
    ax.legend(fontsize=16, loc="upper left")

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    ax.set_xlabel('Time (s)', fontsize=21)
    xtick_positions = np.arange(0, 1.05, 0.2)
    xtick_labels = [f"{tick:.1f}" for tick in xtick_positions]
    ax.set_xticks(xtick_positions)
    ax.set_xticklabels(xtick_labels, fontsize = 19)
    ax.set_xlim(0, 1.05)
    ax.tick_params(axis='both', which='major', labelsize=19)
    plt.tight_layout(h_pad=0.35)
    if save:
        fname = f"antenna_time_plot_single{suffix}.png"
        fig.savefig(FIG_DIR / fname, dpi=300, bbox_inches="tight")


def elytra_time_plot_single(data_dict, frequency, title, save=False, suffix=""):
    fig, ax = plt.subplots(figsize=(9, 6), dpi=100)

    def process_list(data):
        data = np.array(data, dtype=object)
        max_len = max(len(sublist) for sublist in data)

        resampled_data = np.array([
        resample_1d_list(sublist, max_len) for sublist in data
            ], dtype=float)
        means = np.nanmean(resampled_data, axis=0)
        stds = np.nanstd(resampled_data, axis=0)
        lower = means - stds     # One std dev below the mean
        upper = means + stds     # One std dev above the mean
        return max_len, means, lower, upper

    # Use .get() with default empty list if key not found
    list1 = data_dict.get(("Both", frequency), [])

    if len(list1) == 0:
        ax.set_title(f'Freq: {frequency} Hz (No Data)', fontsize=18)
        ax.set_xlim(0, 1.05)
        ax.set_ylabel(title, fontsize=16)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        plt.show()
        return

    max_len1, medians1, lower_quartiles1, upper_quartiles1 = process_list(list1)

    x = np.linspace(0, 1.25, max_len1)
    mask = (x >= 0.1) & (x <= 0.6)

    # Both Elytra Stimulation plot
    ax.fill_between(x[:len(medians1)], lower_quartiles1, upper_quartiles1,
                    color='darkgrey', alpha=0.3)
    ax.plot(x[:len(medians1)], medians1, color='black', linewidth=2)
    ax.fill_between(x[:len(medians1)][mask], lower_quartiles1[mask], upper_quartiles1[mask],
                    color='lightcoral', alpha=0.3)
    ax.plot(x[:len(medians1)][mask], medians1[mask],
            color='red', linewidth=2, label='Both Elytra Stim.')

    # ax.set_title(f'Freq: {frequency} Hz', fontsize=18)
    ax.set_xlim(0, 1.05)
    ax.set_ylabel(title, fontsize=21)
    ax.set_xlabel('Time (s)', fontsize=21)
    ax.legend(fontsize=14)
    ax.set_ylim(-8, 33)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    ax.axhline(y=0, color='black', linestyle='--', linewidth=1)

    # Set custom x-ticks and labels with increased font size
    xtick_positions = np.arange(0, 1.05, 0.2)
    xtick_labels = [f"{tick:.1f}" for tick in xtick_positions]
    ax.set_xticks(xtick_positions)
    ax.set_xticklabels(xtick_labels, fontsize=19)
    ax.tick_params(axis='y', which='major', labelsize=19)  # Increase y-tick label size
    if save:
        fname = f"elytra_time_plot_single{suffix}.png"
        fig.savefig(FIG_DIR / fname, dpi=300, bbox_inches="tight")
    plt.tight_layout(h_pad=0.35)




def antenna_trials_plot(data_dict, frequencies, title, save=False, suffix=""):
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    axes_flat = axes.flatten()

    for idx, freq in enumerate(frequencies):
        ax = axes_flat[idx]
        # Get data for each frequency and side
        list1 = data_dict.get(("Right", freq), [])
        list2 = data_dict.get(("Left", freq), [])

        if len(list1) == 0 and len(list2) == 0:
            ax.set_title(f'Freq: {freq} Hz (No Data)', fontsize=18)
            ax.set_xlim(0, 1.05)
            ax.set_ylabel(title, fontsize=16)
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            continue

        # Plot all Right stimulation trials (red)
        for trial in list1:
            trial = np.array(trial)
            x = np.linspace(0, 1.25, len(trial))
            ax.plot(x, trial, color='red', alpha=0.5, linewidth=1, label='Right Stimulation' if 'Right Stimulation' not in ax.get_legend_handles_labels()[1] else "")

        # Plot all Left stimulation trials (green)
        for trial in list2:
            trial = np.array(trial)
            x = np.linspace(0, 1.25, len(trial))
            ax.plot(x, trial, color='green', alpha=0.5, linewidth=1, label='Left Stimulation' if 'Left Stimulation' not in ax.get_legend_handles_labels()[1] else "")

        # Formatting subplot
        ax.set_title(f'Freq: {freq} Hz', fontsize=18)
        ax.set_xlim(0, 1.05)
        ax.set_ylabel(title, fontsize=16)
        if freq == 10:  # Show legend on one plot only
            ax.legend(fontsize=14)

        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

    # Remove unused subplots if fewer than 6 frequencies
    if len(frequencies) < len(axes_flat):
        for i in range(len(frequencies), len(axes_flat)):
            fig.delaxes(axes_flat[i])

    # Set x-label only to bottom row plots
    for i in range(len(axes_flat)):
        if i >= len(axes_flat) - 3:
            axes_flat[i].set_xlabel('Time (s)', fontsize=20)
            xtick_positions = np.arange(0, 1.05, 0.2)
            xtick_labels = [f"{tick:.1f}" for tick in xtick_positions]
            axes_flat[i].set_xticks(xtick_positions)
            axes_flat[i].set_xticklabels(xtick_labels)

    plt.tight_layout(h_pad=0.35)
    if save:
        fname = f"antenna_trials_plot{suffix}.png"
        fig.savefig(FIG_DIR / fname, dpi=300, bbox_inches="tight")



def elytra_trials_plot(data_dict, frequencies, title, save=False, suffix=""):
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    axes_flat = axes.flatten()

    for idx, freq in enumerate(frequencies):
        ax = axes_flat[idx]
        # Get data for each frequency
        list1 = data_dict.get(("Both", freq), [])

        if len(list1) == 0:
            ax.set_title(f'Freq: {freq} Hz (No Data)', fontsize=18)
            ax.set_xlim(0, 1.05)
            ax.set_ylabel(title, fontsize=16)
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            continue

        # Plot all Both Elytra stimulation trials (blue)
        for trial in list1:
            trial = np.array(trial)
            x = np.linspace(0, 1.25, len(trial))
            # Only add label to the first line for the legend
            ax.plot(x, trial, color='blue', alpha=0.5, linewidth=1,
                    label='Both Elytra Stimulation' if 'Both Elytra Stimulation' not in ax.get_legend_handles_labels()[1] else "")

        # Formatting subplot
        ax.set_title(f'Freq: {freq} Hz', fontsize=18)
        ax.set_xlim(0, 1.05)
        ax.set_ylabel(title, fontsize=16)
        if freq == 10:
            ax.legend(fontsize=14)

        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

    # Remove unused subplots if fewer than 6 frequencies
    if len(frequencies) < len(axes_flat):
        for i in range(len(frequencies), len(axes_flat)):
            fig.delaxes(axes_flat[i])

    # Set x-label only to bottom row plots
    for i in range(len(axes_flat)):
        if i >= len(axes_flat) - 3:
            axes_flat[i].set_xlabel('Time (s)', fontsize=20)
            xtick_positions = np.arange(0, 1.05, 0.2)
            xtick_labels = [f"{tick:.1f}" for tick in xtick_positions]
            axes_flat[i].set_xticks(xtick_positions)
            axes_flat[i].set_xticklabels(xtick_labels)

    plt.tight_layout(h_pad=0.35)
    if save:
        fname = f"elytra_trials_plot{suffix}.png"
        fig.savefig(FIG_DIR / fname, dpi=300, bbox_inches="tight")
