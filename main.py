# author: Md Abid Hasan
# University of California Riverside
# Email: mhasa006@ucr.edu

import sys
import os
import pickle
import argparse

from ProcessData import *
from DatasetMaking import *
from NNModel import *

parser = argparse.ArgumentParser(description="Epi2HiC: Hi-C interaction prediction")

group = parser.add_mutually_exclusive_group()
group.add_argument('-c', '--crossvalidation', action='store_true', help='Cross Validation')

parser.add_argument('-i', '--interaction', metavar='', required=True, help='Hi-C interaction file')
parser.add_argument('-n', '--matrix', metavar='', required=True, help='Matrix format data for each interaction')

args = parser.parse_args()


def pickle_data(D, file_name):
    filename = str(file_name)
    outfile = open(filename, 'wb')
    pickle.dumb(D, outfile)
    outfile.close()


def main():
    # for cross validation
    if args.crossvalidation:
        read = DataProcess(args.interaction, args.matrix)
        data = MakeDataset(read)

        interaction_matrix_file_path = args.matrix
        interaction_name = interaction_matrix_file_path.split('/')[1]

        fopen = open(str(interaction_name) + '.txt', 'w')
        fopen.write('Iteration' + '\t' + '#Training_sample' + '\t' + '#Testing_sample' + '\t' +
                    'Train_SP' + '\t' + 'Test_SP' + '\t' +
                    'Train_PR' + '\t' + 'Test_PR' + '\n')

        for iteration in range(1, 6):
            model = Model(data)
            result = model.get_model_performance()

            fopen.write(str(iteration) + '\t' + str(result['train_sample']) + '\t' + str(result['test_sample']) + '\t' +
                        str(result['train_sp']) + '\t' + str(result['test_sp']) + '\t' +
                        str(result['train_pr']) + '\t' + str(result['test_pr']) + '\n')

        fopen.close()


if __name__ == '__main__':
    main()
