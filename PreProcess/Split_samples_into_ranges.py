"""
5.
This code is to split the large dataset into regions
"""

import sys
import pickle


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
    interaction_matrix_file = sys.argv[1]
    range1 = sys.argv[2]
    range2 = sys.argv[3]

    interaction_matrix_dict = process_pickled_file(interaction_matrix_file)
    ranged_matrix_dict = dict()
    print len(interaction_matrix_dict)
    read_count = 0
    for interaction in interaction_matrix_dict:
        region1 = interaction[0]
        region2 = interaction[1]

        print read_count
        read_count += 1

        if region1 >= int(range1) and region2 <= int(range2):
            ranged_matrix_dict[interaction] = interaction_matrix_dict[interaction]

    print len(ranged_matrix_dict)
    pickle_data(ranged_matrix_dict, 'CN_chr1_' + str(range1) + '_' + str(range2) + '_interaction_matrix')


if __name__ == '__main__':
    main()
