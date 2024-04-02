import numpy
import INFER
from choose_version import choose
from choose_version import chooselabel
from constants import VARIABLE
# from variable import processus_nb
# from variable import larva
import glob
import subprocess
import re
import threading
import argparse         # for command-line arguments
import os
import array

import pickle


def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


class MATRICE():

    def __init__(self, name_in, id, label, var):
        self.files = name_in
        self.id = id
        self.run(label, var)
        # print(name_in)

    def run(self, label, var):
        Larva = 0
        dossier = self.id

        name = self.files
        # print(doss)
       # FILES=glob.glob(doss+'/*.pkl')
       # print(FILES)
        #proc = subprocess.Popen(['find '+doss+'/ -name "*.pkl"'], stdout=subprocess.PIPE, shell=True)
        #(files, err) = proc.communicate()
        # files0=str(files)

        N_be = 7

        if name != 0:
            # FILES[0]=FILES[0][2:]
            # print(name)
            # if os.path.isfile('../INFERENCE_DATA/Amplitude/first/'+type+'/'+name.split('/')[-1]):
            #     print('continue')
            # else :
            version = 'old'
            palier = 'first'
            #mu_ini = numpy.zeros((int(var.end_time / 3) + 1, N_be, 10, 10))
            it = numpy.zeros((int(var.end_time / 5), N_be))
            it_t = numpy.zeros((int(var.end_time / 5), N_be))
            #LAMBDA = numpy.zeros((int(var.end_time / 3) + 1, N_be))
            #TRANS = numpy.zeros((int(var.end_time / 3) + 1, N_be, N_be))
            larva = 0
            probabehavior = numpy.zeros(N_be)

            fichier = open(name, 'rb')
            #(mu_ini,Lambda, Trans, stay_, out_trans_,out_lambda_, probabehavior,table,larva) =pickle.load(fichier)
            (mu_ini, Lambda1, Trans1, stay_, out_trans_, out_lambda_,
             probabehavior, table, larva) = pickle.load(fichier)
            # print(table, 'table')
            # print(Lambda, 'lambda')
            # print(Trans, 'trans')
            # print(Lambda)
            # print(mu_ini,'muini')
            for i in range(0, len(mu_ini)):
                for j in range(0, len(mu_ini[0])):
                    for h in range(0, len(mu_ini[0][0])):
                        for g in range(0, len(mu_ini[0][0][0])):
                            mu_ini[i][j][h][g] = numpy.around(
                                mu_ini[i][j][h][g], 5)

            for i in range(0, len(table)):
                for j in range(0, len(table[i])):
                    for h in range(0, len(table[i][j])):
                        for g in range(0, len(table[i][j][h])):
                            for x in range(0, len(table[i][j][h][g])):
                                table[i][j][h][g][x] = round(
                                    table[i][j][h][g][x], 5)
            Lambda1 = numpy.around(Lambda1, decimals=5)
            Trans1 = numpy.around(Trans1, decimals=5)

            Trans = numpy.zeros((int(var.end_time / 5), N_be, N_be))
            for time in range(0, var.end_time):
                Trans[int(time / 5)] += Trans1[time, :, :]
            Trans = Trans / 5

            Lambda = numpy.zeros((int(var.end_time / 5), N_be))
            for time in range(0, var.end_time):
                Lambda[int(time / 5)] += Lambda1[time, :]
            Lambda = Lambda / 5

            MU = numpy.zeros((int(var.end_time / 5), N_be, 4, 10))
            for time in range(0, var.end_time):
                MU[int(time / 5)] += mu_ini[time]
            MU = MU / 5

            Tabl_ = []
            a = []
            [a.append([[], [], [], []]) for i in range(0, N_be)]
            Tabl_ = []
            #print(len(self.Table),l, len(self.Table))
            [Tabl_.append(a) for j in range(int(var.end_time / 5) + 1)]
            #print(len(Tabl_), len(Tabl_[0]), len(Tabl_[0][0]), len(table))
            for i in range(len(Tabl_)):
                for j in range(len(Tabl_[i])):
                    for be in range(len(Tabl_[i][j])):
                        for dt in range(len(Tabl_[i][j][be])):
                            for x in range(len(Tabl_[i][j][be][dt])):
                                for t in range(int(time * 5), int(time + 1) * 5):
                                    A_M.append(table[i][t][be][dt])
                                Tabl_[i][j][be][dt][x].append(A_M)

            Trans_plus = Trans

            # for i in range(0, len(mu_ini)):
            #     for j in range(0, len(mu_ini[0])):
            #         for h in range(0, len(mu_ini[0][0])):
            #             for g in range(0, len(mu_ini[0][0][0])):
            #                 if (mu_ini[i][j][h][g]) > 1 or (mu_ini[i][j][h][g]) < -1:
            #                     print(mu_ini[i][j][h][g],
            #                           i, j, h, g, 'mu_ini')

            probabehavior = probabehavior / sum(probabehavior)
            Infer = INFER.INFERENCE_CLASS(N_be, label, var)
            Infer.inference(Lambda, Trans, out_lambda_,
                            out_trans_, stay_, table, MU, version, N_be, label, var)

            # print('../INFERENCE_DATA/Amplitude/first/'+type+'/'+name.split('/')[-1])
            #f= open('../INFERENCE_DATA/small/'+type+'/'+name.split('/')[-1], 'wb')
            f = open('../INFERENCE_DATA/' + label.nom + '/'
                     + var.type + '_5s/' + name.split('/')[-1], 'wb')
            pickle.dump((Infer.LAMBDA, Infer.TRANS,
                         Infer.mu, probabehavior), f)
            f.close()
#


def main(arg_str):

    version = 20180409
    arg_parser = argparse.ArgumentParser(
        description='Larvae behavior analysis')
    arg_parser.add_argument(
        '-v', '--version', action='version', version='%(prog)s ' + str(version))
#    arg_parser.add_argument('-D', '--D_case', required = True, action = 'store', type = int, choices = range(1, max_D_case + 1), metavar = 'D_case', help = 'D case to be simulated')
    arg_parser.add_argument('--id', required=True, action='store', type=int,
                            help='A simulation identifier to be added to the output file')
    arg_parser.add_argument('-n', '--name', action='store',
                            type=str, help='name_files')
    arg_parser.add_argument('-a', '--ac',
                            action='store', type=str, help='name_files')
    arg_parser.add_argument(
        '-s', '--state', action='store', type=str, help='name_files')

#   arg_parser.add_argument('--ksi', '--alpha_over_D', required = True, action = 'store', type = float,
#       help = 'Total force over the diffusivity gradient')

    # Analyze arguments
    input_args = arg_parser.parse_args(arg_str.split())
    state = input_args.state
    ac = input_args.ac
    name = input_args.name

    var = choose(ac)
    label = chooselabel(state)
    id = input_args.id
    noeuds = MATRICE(name, id, label, var)
