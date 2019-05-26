# author: Md Abid Hasan
# University of California Riverside
# Email: mhasa006@ucr.edu

import sys
import os
import argparse

from ProcessData import *
from EpiFeatureMatrix import *

parser = argparse.ArgumentParser(description="Epi2HiC: Hi-C interaction prediction")

group = parser.add_mutually_exclusive_group()
group.add_argument('-c', '--crossvalidation', action='store_true', help='Cross Validation')

parser.add_argument('-i', '--interaction', metavar='', required=True, help='Hi-C interaction file')
parser.add_argument('-n', '--neighbors', metavar='', required=True, help='Neighbor information for each interaction pair')
parser.add_argument('-e', '--epigenetics', metavar='', required=True, help='Epigenetics information for each interacting pair')

args = parser.parse_args()


def print_dictionary_sample(D):
    count = 0
    for key in D:
        print key, D[key], D[key].shape
        if count == 2:
            break
        count += 1


def main():
    # for cross validation
    if args.crossvalidation:
        data = DataProcess(args.interaction, args.neighbors, args.epigenetics)
        epi_matrix = MatrixFormation(data)
        epi_matrix.get_matrix_for_neighbor_matrix()


if __name__ == '__main__':
    main()
