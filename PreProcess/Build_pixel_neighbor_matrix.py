"""
2.
This code builds a dictionary that contains each region in center of a
neighboring matrix of varying size matrix
"""

import sys
import math
import pickle
import pandas as pd


def find_neghbors(r1, r2, matrix_size, resolution):
    r1_start = r1 - resolution * int((math.floor(matrix_size/2)))
    r1_end = r1 + resolution * int((math.floor(matrix_size/2)))

    r2_start = r2 - resolution * int((math.floor(matrix_size/2)))
    r2_end = r2 + resolution * int((math.floor(matrix_size/2)))

    neighbors = [
        (r1_start, r2_start),
        (r1_start, r2_start + resolution),
        (r1_start, r2_start + resolution * 2),

        (r1_start + resolution, r2_start),
        (r1_start + resolution, r2_start + resolution),
        (r1_start + resolution, r2_start + resolution * 2),

        (r1_start + resolution * 2, r2_start),
        (r1_start + resolution * 2, r2_start + resolution),
        (r1_start + resolution * 2, r2_start + resolution * 2)
    ]

    return neighbors


def dump_with_pickle(interaction_dict, fileName, matrix_size):
    filename = str(fileName) + '_interactions_' + str(matrix_size) + '_neighbor_matrix'
    outfile = open(filename, 'wb')
    pickle.dump(interaction_dict, outfile)
    outfile.close()


def main():
    interaction_file = sys.argv[1]  # sampled interaction file made from the Make_region_pairs_for_experiment file
    fileName = sys.argv[2]          # name of the file
    resolution = 5000
    matrix_size = 3

    interaction_neighbor_3_dict = dict()
    interaction_neighbor_5_dict = dict()
    interaction_neighbor_7_dict = dict()
    interaction_neighbor_9_dict = dict()
    interaction_neighbor_11_dict = dict()
    interaction_neighbor_13_dict = dict()

    read_count = 0

    infile = open(interaction_file, 'rb')
    interaction_dict = pickle.load(infile)
    infile.close()

    print any(math.isnan(val) for val in interaction_dict.values())

    for pair in interaction_dict:
        region1 = int(pair[0])
        region2 = int(pair[1])

        if matrix_size == 3:
            interaction_neighbor_3_dict[(region1, region2)] = find_neghbors(region1, region2, 3, resolution)
        # if matrix_size == 5:
        #     interaction_neighbor_5_dict[(region1, region2)] = find_neghbors(region1, region2, 5, resolution)
        # if matrix_size == 7:
        #     interaction_neighbor_7_dict[(region1, region2)] = find_neghbors(region1, region2, 7, resolution)
        # if matrix_size == 9:
        #     interaction_neighbor_9_dict[(region1, region2)] = find_neghbors(region1, region2, 9, resolution)
        # if matrix_size == 11:
        #     interaction_neighbor_11_dict[(region1, region2)] = find_neghbors(region1, region2, 11, resolution)
        # if matrix_size == 13:
        #     interaction_neighbor_13_dict[(region1, region2)] = find_neghbors(region1, region2, 13, resolution)

    dump_with_pickle(interaction_neighbor_3_dict, fileName, 3)
    # dump_with_pickle(interaction_neighbor_5_dict, fileName, 5)
    # dump_with_pickle(interaction_neighbor_7_dict, fileName, 7)
    # dump_with_pickle(interaction_neighbor_9_dict, fileName, 9)
    # dump_with_pickle(interaction_neighbor_11_dict, fileName, 11)
    # dump_with_pickle(interaction_neighbor_13_dict, fileName, 13)


if __name__ == '__main__':
    main()
