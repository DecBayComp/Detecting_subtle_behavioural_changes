import argparse  # for command-line arguments
import array
# from variable import processus_nb
# from variable import larva
import glob
import os
import pickle
import re
import subprocess
import threading

import numpy as np
import pandas as pd

import data
import initialisation
from choose_version import choose, chooselabel
from constants import VARIABLE


def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


class MATRICE():

    def __init__(self, name_in, id, label, var):
        self.files = name_in
        self.id = id
        self.run(label, var)
        print(name_in)

    def run(self, label, var):

        path = r'/pasteur/projets/policy02/Larva-Screen/screens/' + var.type + '/'

        # names = ['t', 'crawl_large', 'bend_large', 'stop_large', 'head retraction_large', 'back crawl_large', 'roll_large', 'small_motion', 'straight_proba', 'straight_and _light _bend _proba',  'bend_proba', 'curl_proba', 'ball_proba',
        #          'larva_length _smooth _ 5', 'larva_length _deriv _smooth _ 5', 'S_smooth_5',  'S_deriv _smooth_5',
        #          'eig_smooth_5', 'eig_deriv_smooth_ 5', 'angle_upper_lower_smooth_5', 'angle_upper_lower_deriv_smooth_5',
        #          'angle_downer_upper_smooth_5', 'angle_downer_upper_deriv_smooth_5', 'd_eff_head_norm_smooth_5', 'd_eff_head_norm_deriv_smooth_5', 'd_eff_tail_norm_smooth_5',  'd_eff_tail _norm_deriv_smooth_5',
        #          'motion_velocity_norm_smooth_5', 'head_velocity_norm _smooth_5', 'tail_velocity _norm_smooth _ 5', 'As_smooth_5', 'prod_scal_1', 'prod_scal_2', 'motion_to_u_tail_head_smooth_5', 'motion_to_v_tail_head_smooth_5']
        #
        # # feats = ['t', 'crawl', 'bend', 'stop', 'head retraction', 'back crawl', 'roll', 'As_smooth_5']
        #
        # labels_ = ['crawl_large', 'bend_large', 'stop_large',
        #            'head retraction_large', 'back crawl_large', 'roll_large', 'small_motion']
        #
        # feats = ['t', 'crawl_large', 'bend_large', 'stop_large', 'head retraction_large',
        #          'back crawl_large', 'roll_large', 'small_motion', 'As_smooth_5']
        #
        # # ['t', 'crawl', 'bend', 'stop', 'head retraction', 'back crawl', 'roll', 'As_smooth_5']
        #
        # # labels_ = ['crawl', 'bend', 'stop', 'head retraction', 'back crawl', 'roll']

        N_be = len(label.labels_)

        subdir = list(os.listdir(path + self.files + '/'))
        print(subdir)
        FILES = []
        A = 0
        SUN = []
        for SUB in subdir:
            if '#s_020' in SUB:
                continue
           # print(SUB)
            Files_ = []
            # if 'p_8_45' in SUB:
            if not '.' in SUB and not 'hit' in SUB and not "s_020_0"in SUB:
                if '100_' in SUB:
                    for sub_subdir in list(os.listdir(path + self.files + '/' + SUB + '/')):

                        Files_ += glob.glob(path + self.files + '/' + SUB
                                            + '/' + sub_subdir + r"/State_Amplitude_large*.txt")
                    if len(Files_) > 3:
                        FILES.extend([Files_])
                        SUN.append(SUB)

        print(len(FILES), 'FILES')
        for sous in range(0, len(FILES)):
            print(sous, 'sous')
            # # print('../INITIALIZATION_DATA/' + label.nom + '/'
            # #       + var.type + '/' + self.files + SUN[sous] + '.pkl')
            # if os.path.exists('../LIKELIHOOD/' + var.type + '/' + self.files + SUN[sous] + '.pkl'):
            #     print('../LIKELIHOOD/' + var.type + '/'
            #           + self.files + SUN[sous] + '.pkl')
            #     continue

            if os.path.exists('../INITIALIZATION_DATA/' + label.nom + '/' + var.type + '/' + self.files + SUN[sous] + '.pkl'):
                print('../INITIALIZATION_DATA/' + label.nom + '/'
                      + var.type + '/' + self.files + SUN[sous] + '.pkl', 'Nooooo')
                continue
            # print(self.files + SUN[sous], 'reel')

            Initialisation = initialisation.INITIALISATION(
                len(FILES[sous]), N_be, label, var)
            Larva = -1
            DAT__ = data.DATA_(len(FILES[sous]), N_be, var, label)

            for name in sorted(FILES[sous]):

                name_ = open(name, 'rb')
                DATA = pd.read_csv(name_, sep='\t',
                                   header=None, names=label.names)
                Larva += 1
                for col in label.feats:
                    if DATA[col].dtype == object:
                        try:
                            DATA[col] = (DATA[col].str.split('+')).str[0]
                            # print(col, DATA[col])
                            DATA[col] = pd.to_numeric(
                                (DATA[col].str.split('[0-9]-')).str[0])
                        except:
                            break
                TOTAL_MOTION = np.zeros((len(DATA['t']), 4))
                # liste = [list(DATA['t']).index(element) for element in DATA['t']]
                COMP = np.zeros((N_be, len(DATA['t'])))
                # if len(liste)>0 :
                for j in label.labels_:
                    if DATA[j][0] == 1:
                        old = label.labels_.index(j)
                for i in range(0, len(DATA['t'])):
                    TOTAL_MOTION[i, 3] = DATA['As_smooth_5'][i]
                    # TOTAL_MOTION[i,4]=DATA['angle_downer_upper_smooth_5'][i]
                    strong = 0
                    for j in range(0, N_be):
                        if (DATA[str(label.labels_[j])][i] == 1):
                            strong = 1
                            TOTAL_MOTION[i, 1] = j
                            TOTAL_MOTION[i, 0] = DATA['t'][i]
                            TOTAL_MOTION[i, 2] = Larva
                    if strong == 0:
                        TOTAL_MOTION[i, 1] = 6
                        TOTAL_MOTION[i, 0] = DATA['t'][i]
                        TOTAL_MOTION[i, 2] = Larva

                DAT__.dat(TOTAL_MOTION, N_be, Larva, var, label)
                Initialisation.proba_ini(TOTAL_MOTION, Larva, N_be, label, var)
                Initialisation.parameters_active(
                    TOTAL_MOTION, Larva, N_be, label, var)
                # DATA_ALL.append(DATA_)
                if Larva % 100 == 0:
                    print(Larva)
            del TOTAL_MOTION
            Initialisation.regroupement_larva(Larva, N_be, label, var)
            # print(Initialisation.LAMBDA[29:33, :], np.sum(DAT__.DATA_ALL_OUT[:, :, 29 * 13:(29 + 1) * 13], axis=2), np.sum(DAT__.DATA_ALL_OUT[:, :, 30 * 13:(30 + 1) * 13], axis=2), np.sum(
            #     DAT__.DATA_ALL_OUT[:, :, 31 * 13:(31 + 1) * 13], axis=2), np.sum(DAT__.DATA_ALL_IN[:, 29 * 13:(29 + 1) * 13], axis=1), np.sum(DAT__.DATA_ALL_IN[:, 30 * 13:(30 + 1) * 13], axis=1), np.sum(DAT__.DATA_ALL_IN[:, 31 * 13:(31 + 1) * 13], axis=1))
            # # if not os.path.exists('../INITIALIZATION_DATA_TEST/' + self.files):
            #     os.makedirs('../INITIALIZATION_DATA_TEST/' + self.files)
            # print(DAT__.DATA_ALL_IN, '../LIKELIHOOD/' +
            #       var.type + '/' + self.files + SUN[sous] + '.pkl')
            # print(np.sum(Initialisation.OUT[:, 29 * 13:(29 + 1) * 13], axis=1), np.sum(
            #     Initialisation.OUT[:, 29 * 13: (29 + 1) * 13], axis=1))
            #
            # print('../INITIALIZATION_DATA/' + label.nom + '/' +
            #       var.type + '/' + self.files + SUN[sous] + '.pkl', "initialistionnn")
            # f = open('../LIKELIHOOD/' + var.type + '/' + label.nom + '/' +
            #          self.files + SUN[sous] + '.pkl', 'wb')
            # # print(DAT__.DATA_ALL_IN.shape)
            # pickle.dump((DAT__.DATA_ALL_IN, DAT__.DATA_ALL_OUT), f)

            f = open('../INITIALIZATION_DATA/' + label.nom + '/'
                     + var.type + '/' + self.files + SUN[sous] + '.pkl', 'wb')
            # print(Initialisation.Table)
            pickle.dump((Initialisation.mu_ini, Initialisation.LAMBDA, Initialisation.transtot, Initialisation.STAY,
                         Initialisation.out_t, Initialisation.OUT_TRANS, Initialisation.probabehavior, Initialisation.Table, Larva), f)

            # print('../INITIALIZATION_DATA/' + label.nom + '/' +
            #       var.type + '/' + self.files + SUN[sous] + '.pkl')

            # for i in range(0,len(Initialisation.mu_ini)):
            #     for j in range(0,len(Initialisation.mu_ini[0])):
            #         for h in range(0,len(Initialisation.mu_ini[0][0])):
            #             for g in range(0,len(Initialisation.mu_ini[0][0][0])):
            #                 if (Initialisation.mu_ini[i][j][h][g])>1 or (Initialisation.mu_ini[i][j][h][g])<-1 :
            #                     print(Initialisation.mu_ini[i][j][h][g],i,j,h,g,'mu_fini')
            f.close()


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
    print(var.end_time)
    id = input_args.id
    noeuds = MATRICE(name, id, label, var)
