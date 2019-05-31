import pickle


class DataProcess(object):
    def __init__(self, *argv):
        super(DataProcess, self).__init__()

        self.interaction_pickle_file = argv[0]
        self.samples_into_matrix = argv[1]

    # this  method returns a dictionary that contains all valid
    # interacting pairs and the associated contact counts
    def get_interaction_information(self):
        return process_pickled_file(self.interaction_pickle_file)

    # this method returns a dictionary that contains each interaction
    # sample epigenetics information converted into matrix format
    def get_processed_sample_matrix_format_data(self):
        return process_pickled_file(self.samples_into_matrix)


def process_pickled_file(pickle_file):
    infile = open(pickle_file, 'rb')
    return_dict = pickle.load(infile)
    infile.close()

    return return_dict
