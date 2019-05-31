import random
import numpy as np

def reshape_matrix(matrix):
    row, col = matrix[0].shape
    reshaped_matrix = np.zeros((len(matrix), row, col), dtype = float)
    for sample_id in range(len(matrix)):
        for i in range(row):
            for j in range(col):
                reshaped_matrix[sample_id, i, j] = matrix[sample_id][i][j]

    return reshaped_matrix


def reshape_list(list, dtype):
    reshaped_list = np.zeros((len(list), 1), dtype = dtype)
    for sample_id in range(len(list)):
        reshaped_list[sample_id] = list[sample_id]

    return reshaped_list

class MakeDataset(object):
    def __init__(self, read):
        super(MakeDataset, self).__init__()

        self.interaction_contact_count_dict = read.get_interaction_information()
        self.interaction_sample_matrix_format_dict = read.get_processed_sample_matrix_format_data()

    def get_dataset_for_nn(self):
        return process_dataset(self.interaction_contact_count_dict, self.interaction_sample_matrix_format_dict)


def process_dataset(interaction_dict, sample_matrix_dict):

    interacting_regions = list(sample_matrix_dict.keys())
    num_sample = len(interacting_regions)
    N1 = int(num_sample * 0.8)
    N2 = int(num_sample * 0.9)

    random.shuffle(interacting_regions)
    training_regions = interacting_regions[0:N1]
    validating_regions = interacting_regions[N1:N2]
    testing_regions = interacting_regions[N2:num_sample]

    training_sample_matrices = [sample_matrix_dict[i] for i in training_regions]
    training_sample_contact_count = [interaction_dict[i] for i in training_regions]

    validating_sample_matrices = [sample_matrix_dict[i] for i in validating_regions]
    validating_sample_contact_count = [interaction_dict[i] for i in validating_regions]

    testing_sample_matrices = [sample_matrix_dict[i] for i in testing_regions]
    testing_sample_contact_count = [interaction_dict[i] for i in testing_regions]

    dataset = {
        'X_train': reshape_matrix(training_sample_matrices),
        'X_valid': reshape_matrix(validating_sample_matrices),
        'X_test': reshape_matrix(testing_sample_matrices),

        'Y_train': reshape_list(training_sample_contact_count, float),
        'Y_valid': reshape_list(validating_sample_contact_count, float),
        'Y_test': reshape_list(testing_sample_contact_count, float),

        'training_interactions': training_regions,
        'validating_interactions': validating_regions,
        'testing_interactions': testing_regions
    }

    return dataset
