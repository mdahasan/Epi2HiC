import pickle


class DataProcess(object):
    def __init__(self, *argv):
        super(DataProcess, self).__init__()

        self.interaction_pickle_file = argv[0]
        self.neighbors_pickle_file = argv[1]
        self.epigenetics_pickle_file = argv[2]

    # this  method returns a dictionary that contains all valid
    # interacting pairs and the associated contact counts
    def get_interaction_information(self):
        return process_pickled_file(self.interaction_pickle_file)

    # this method returns a dictionary that contains all the neighbors
    # of an interacting pair
    def get_interacting_neighbor_information(self):
        return process_pickled_file(self.neighbors_pickle_file)

    # this method returns a dictionary that contains epigenetics
    # information for each region
    def get_epigenetics_information(self):
        return process_pickled_file(self.epigenetics_pickle_file)


def process_pickled_file(pickle_file):
    infile = open(pickle_file, 'rb')
    return_dict = pickle.load(infile)
    infile.close()

    return return_dict
