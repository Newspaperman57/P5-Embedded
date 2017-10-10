import pandas as pd
import numpy as np
from scipy import stats
from process_helpers import smoothing, make_acc_angle, make_gyro_rate, make_noise, shuffle \
    , get_sample_frequency, complementary_filter, calc_toal_acc, extract_shots, get_shots_index
from kmeans import group_shots, get_center_cords
from get_stats_from_shots import make_statistic_features


def process_data(path_csv):
    alpha = 0.2
    acc_sensitivity = 2048 / 90
    gyro_sensitivity = 16.4
    data = pd.read_csv(path_csv, sep=';', error_bad_lines=False)
    data = smoothing(data, alpha)
    data = make_acc_angle(data, acc_sensitivity)
    data = make_gyro_rate(data, gyro_sensitivity)
    sf = get_sample_frequency(data['time'])
    (roll) = complementary_filter(data['rx_rate'].values, data['x_ang'].values, sf, data.shape[0])
    data['roll'] = roll
    data = calc_toal_acc(data, acc_sensitivity)
    g = make_noise(data)
    df_no_noise = g[g['no_noise']== True]
    indexes = get_shots_index(df_no_noise.index, 20, 40)
    shots = extract_shots(data, indexes)

    # use dict mapping to use different feature extraction methods
    argument = "shot_stats"
    input_data_shots = mapping(argument, shots)
    shuffle(input_data_shots)
    return (input_data_shots, False)


def k_groups(shots):
    movements_grouped = group_shots(shots, 5)
    return np.array(get_center_cords(movements_grouped, 5))

def shot_stats(shots):
    return make_statistic_features(shots)

def mapping(argument,shots):
    switcher = {
        "k_groups": k_groups,
        "shot_stats": shot_stats
    }
    # Get the function from switcher dictionary
    func = switcher.get(argument, lambda: "nothing")
    # Execute the function
    return func(shots)
