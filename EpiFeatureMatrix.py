import numpy as np


class MatrixFormation(object):
    def __init__(self, data):
        super(MatrixFormation, self).__init__()
        self.interacting_neighbors = data.get_interacting_neighbor_information()
        self.epigenetics_info = data.get_epigenetics_information()

    def get_matrix_for_neighbor_matrix(self):
        return process_neighbors_into_matrix(self.interacting_neighbors, self.epigenetics_info)


def process_neighbors_into_matrix(interacting_neighbors, epigenetics_info):

    interacting_neighbors_matrix_representation_dict = dict()
    for position in interacting_neighbors:
        center_position = position
        all_neighbors = interacting_neighbors[position]

        neighbor_matrix_list = list()
        for member in all_neighbors:
            neighbor_matrix_list.append(build_epi_matrix_for_each_pair(member, epigenetics_info))

        # perform element wise operation on all neighbor matrix to make into one
        # matrix that represent the center position region pair
        consensus_matrix = np.add(neighbor_matrix_list[0], neighbor_matrix_list[1])
        for i in range(2, len(neighbor_matrix_list)):
            consensus_matrix = np.add(consensus_matrix, neighbor_matrix_list[i])

        interacting_neighbors_matrix_representation_dict[center_position] = consensus_matrix

    return interacting_neighbors_matrix_representation_dict


def build_epi_matrix_for_each_pair(member, epigenetics_info):
    region1 = member[0]
    region2 = member[1]

    region1_epi_matrix = epigenetics_info[region1]
    region2_epi_matrix = epigenetics_info[region2]

    # perform martix multiplication on two matrices to make into one
    interacting_region_matrix = np.matmul(region1_epi_matrix.T, region2_epi_matrix)

    return interacting_region_matrix

