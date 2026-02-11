from os import listdir
import ast 
import pandas as pd 

def find_csv_filenames(path_to_dir, suffix=".csv"):
    filenames = listdir(path_to_dir)
    return [filename for filename in filenames if filename.endswith(suffix)]


def file_read(file):
    """Reads in a single csv file, with 3 columns: time, pose (position of the insect, structured as 
    [top, middle, bottom]), and finally arduino data (stimulation side, frequency 
    of the stimulation and duration of the stimulation) """


    df = pd.read_csv(file)
    # Read in time, pose and arduino data. 
    time = df.get('time')
    differences = time.diff()
    fps = 1/differences.mean()


    pose_raw = df.get('pose')
    arduino_data = df.get('arduino_data')
    stim_deets = []     # Will contain a list of lists: [stimulation side, frequency] 
                        # or [None, None] if no stimulation has occured.
    stim_occur = []     #Simply a binary list denoting whether a stimulation has occured at specific time j. 

    pose = []
    # We iterate through both pose and arduino data lists. 
    for i, j in zip(pose_raw, arduino_data):

        # Convert the string representation of a list into an actual list
        i_list = ast.literal_eval(i)

        pose.append(i_list)
        # Check if arduino data is NOT an empty entry
        if isinstance(j, str) and j.strip():
            # If not, then append the stimulation information
            # print(file)
            try:
                # direction = j[0]
                # number = j[1:]
                # if direction == 'E': 
                #     direction = 'Both'
                # elif direction == 'A': 
                #     direction = 'Left'
                # elif direction == 'B': 
                #     direction ='Right'
                direction, number = j.split(", ")
                freq = int(number[:2])
                freq = int(number)
                stim_deets.append([direction, freq])
                stim_occur.append(1)
            except ValueError: 
                # If empty, no stimulation: [None, None, None]
                stim_deets.append([None, None])
                stim_occur.append(0)
        else: 
            # If empty, no stimulation: [None, None, None]
            stim_deets.append([None, None])
            stim_occur.append(0)


    # Return relevant lists. 
    return pose, stim_deets, stim_occur, fps
