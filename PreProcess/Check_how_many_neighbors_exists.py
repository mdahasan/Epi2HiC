"""
3.
This code checks how many of the neighbor for each positions
actually exists in the interaction file
"""

import sys
import pickle
import math

def main():
    neighbor_matrix_file = sys.argv[1]  # neighbor matrix file to get all the neighbor pair
    interaction_file = sys.argv[2]      # interaction file to see if these neighbors exists in the interaction file
    matrix_size = sys.argv[3]           # to check if all neighbors exists
    fileName = sys.argv[4]              # name of the file containing all nxn neighbors

    matrix_dim = int(math.sqrt(int(matrix_size)))

    infile_neighbor = open(neighbor_matrix_file, 'rb')
    neighbor_matrix_dict = pickle.load(infile_neighbor)
    infile_neighbor.close()

    infile_interaction = open(interaction_file, 'rb')
    interaction_dict = pickle.load(infile_interaction)
    infile_interaction.close()

    # this part checks if all the neighbors does have interaction values.
    # for each list of neighbors from neighbor matrix file, it checks from
    # the original interaction file and only keeps if all neighbors
    # interaction information is available
    properly_neighbored_matrix = dict()
    proper_interactions = dict()
    for position in neighbor_matrix_dict:
        neighbors = neighbor_matrix_dict[position]
        neighbor_exist_count = 0
        for i in range(len(neighbors)):
            if neighbors[i] in interaction_dict:
                neighbor_exist_count += 1

        if neighbor_exist_count == matrix_dim * matrix_dim:
            properly_neighbored_matrix[position] = neighbors
            proper_interactions[position] = interaction_dict[position]

    # print 'Total sample: ', len(neighbor_matrix_dict)
    # print 'Sample with all 3x3 neighbors: ', good_sample

    # saving for each interaction pair, the list of neighbors
    filename = str(fileName) + '_' + str(len(properly_neighbored_matrix)) + '_' + str(matrix_dim) + 'x' + str(matrix_dim) + '_neighbor_matrix'
    outfile = open(filename, 'wb')
    pickle.dump(properly_neighbored_matrix, outfile)
    outfile.close()

    print len(properly_neighbored_matrix)

    # saving for each interaction pair the contact counts where each interaction pair
    # has proper number of neighbors
    filename = str(fileName) + '_' + str(len(proper_interactions)) + '_interactions'
    outfile = open(filename, 'wb')
    pickle.dump(proper_interactions, outfile)
    outfile.close()

    print len(proper_interactions)


if __name__ == '__main__':
    main()
