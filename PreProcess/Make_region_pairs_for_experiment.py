"""
1.
This code makes the pair for the experiment. After making region pairs
from here, we will build a sample interaction file that will be used
for the experiment, the input is 10000, 5000, 1000
"""

import sys
import pickle
import math
import time


def main():
    epi_feature_file = sys.argv[1]  # this file to get the existing positions (epi_signal file)
    interaction_file = sys.argv[2]  # this file to get the contact counts for the selected positions (original knorm interaction file)
    number_of_samples = sys.argv[3] # number of sample which will be (sample * sample)
    fileName = sys.argv[4]          # name of the file (cell line_chrm)

    start = time.time()
    infile = open(epi_feature_file, 'rb')
    epi_dict = pickle.load(infile)
    infile.close()
    end = time.time()
    print "Time to read epigenetics singnal file: ", (end - start)

    all_positions = list(epi_dict.keys())
    sorted_positions = sorted(all_positions)

    selected_positions = sorted_positions[0:int(number_of_samples)]

    selected_position_pairs = [(i, j) for i in selected_positions for j in selected_positions]

    interaction_dict = dict()
    with open(interaction_file, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            cols = line.split()

            region1 = int(float(cols[0]))
            region2 = int(float(cols[1]))
            contact_count = float(cols[2])
            if math.isnan(contact_count):
                print contact_count
                continue
            else:
                interaction_dict[(region1, region2)] = float(cols[2])

    selected_interaction_dict = dict()
    for pair in selected_position_pairs:
        if pair in interaction_dict:
            selected_interaction_dict[pair] = interaction_dict[pair]

    print len(selected_interaction_dict)

    filename = str(fileName) + '_' + str(len(selected_interaction_dict)) + '_interactions'
    outfile = open(filename, 'wb')
    pickle.dump(selected_interaction_dict, outfile)
    outfile.close()


if __name__ == '__main__':
    main()
