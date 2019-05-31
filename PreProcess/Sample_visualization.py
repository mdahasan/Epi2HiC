"""
This code randomly selects samples to visualize
"""

import sys
import pickle
import random
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler


def process_pickled_file(pickle_file):
    infile = open(pickle_file, 'rb')
    return_dict = pickle.load(infile)
    infile.close()

    return return_dict


def pickle_data(D, file_name):
    filename = str(file_name)
    outfile = open(filename, 'wb')
    pickle.dump(D, outfile)
    outfile.close()


def main():
    process_sample_file = sys.argv[1]   # the file containing 100x100 matrices
    interaction_file = sys.argv[2]      # the pickle file containing intecation value

    sample_dict = process_pickled_file(process_sample_file)
    sample_interactions = process_pickled_file(interaction_file)

    # sample_dict_keys = sample_dict.keys()
    # key = random.sample(list(sample_dict_keys), 10)
    # randomly_selected_samples = dict()
    #
    # for i in range(len(key)):
    #     randomly_selected_samples[key[i]] = sample_dict[key[i]]
    #
    # pickle_data(randomly_selected_samples, 'random_100x100_samples')

    scaler = MinMaxScaler(feature_range=(0, 1))

    plt.figure()
    fig_index = 1
    for key in sample_dict:
        sample_matrix = sample_dict[key]
        scaled_sample_matrix = scaler.fit_transform(sample_matrix)
        plt.subplot(4, 3, fig_index)
        ax = sns.heatmap(scaled_sample_matrix)
        plt.title(str(key) + '-' + str(sample_interactions[key]))
        fig_index += 1

    plt.show()


if __name__ == '__main__':
    main()
