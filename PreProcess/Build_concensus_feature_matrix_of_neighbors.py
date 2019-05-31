"""
4.
This code reads all the neighboring interacting pair of the
desired interacting pair and process all interacting pairs
into a m x m matrix
"""

import pickle
import sys
import numpy as np


def pickle_data(D, file_name):
    filename = str(file_name)
    outfile = open(filename, 'wb')
    pickle.dump(D, outfile)
    outfile.close()


def process_pickled_file(pickle_file):
    infile = open(pickle_file, 'rb')
    return_dict = pickle.load(infile)
    infile.close()

    return return_dict


def main():
    interacting_neighbors_file = sys.argv[1]    # proper interactions which have 3x3 neighbors
    epigenetics_file = sys.argv[2]              # epi_signal file

    interacting_neighbors = process_pickled_file(interacting_neighbors_file)
    epigenetics_info = process_pickled_file(epigenetics_file)

    print len(interacting_neighbors)

    interacting_neighbors_matrix_representation_dict = dict()
    interaction_processed = 0
    for position in interacting_neighbors:
        center_position = position
        all_neighbors = interacting_neighbors[position]

        if interaction_processed % 100 == 0 and interaction_processed > 0:
            print interaction_processed
        interaction_processed += 1

        neighbor_matrix_list = list()

        for member in all_neighbors:
            neighbor_matrix_list.append(build_epi_matrix_for_each_pair(member, epigenetics_info))

        # perform element wise operation on all neighbor matrix to make into one
        # matrix that represent the center position region pair
        consensus_matrix = np.add(neighbor_matrix_list[0], neighbor_matrix_list[1])
        for i in range(2, len(neighbor_matrix_list)):
            if i % 2 == 0:
                consensus_matrix = np.add(consensus_matrix, neighbor_matrix_list[i])
            else:
                consensus_matrix = np.add(consensus_matrix, neighbor_matrix_list[i])

        print consensus_matrix.shape

        interacting_neighbors_matrix_representation_dict[center_position] = consensus_matrix

    pickle_data(interacting_neighbors_matrix_representation_dict, 'CN_chr1_' + str(len(interacting_neighbors_matrix_representation_dict)) + '_interacting_3x3_neighbors_processed_8x100_data')


def build_epi_matrix_for_each_pair(member, epigenetics_info):
    region1 = member[0]
    region2 = member[1]

    region1_epi_matrix = epigenetics_info[region1]
    region2_epi_matrix = epigenetics_info[region2]

    # perform martix multiplication on two matrices to make into one
    # interacting_region_matrix = np.matmul(region1_epi_matrix.T, region2_epi_matrix)
    interacting_region_matrix = np.add(region1_epi_matrix, region2_epi_matrix)

    return interacting_region_matrix


if __name__ == '__main__':
    main()
