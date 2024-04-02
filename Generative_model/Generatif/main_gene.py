import numpy as np
import GENERATIF
from choose_version import choose
from choose_version import chooselabel
from constants import VARIABLE
from likelihood_test import likelihood_ratio, binomial, multinomiale, transition_function
import glob
import subprocess
import re
import threading
import argparse         # for command-line arguments
import os
import array
import pickle
import math
import figure
from matplotlib import pyplot as plt
import matplotlib
# matplotlib.use('Agg')


def listing(proba, larva_number, nT, var, N_be, comp):
    liste_trans = np.zeros((N_be, N_be))
    liste = []
    [liste.append(sum(proba[int(nT * var.activation_time):int(nT
                                                              * (var.activation_time + 3)), j]) / (nT * 3)) for j in range(0, N_be)]
    liste = np.array(liste)
    for c in comp:
        if len(c) > 0:
            time = c[0][1]
            for i in range(1, len(c)):
                time += c[i][1]
               # print(time)
                if time > int(var.activation_time) and time < int((var.activation_time + 3)):
                    liste_trans[int(c[i][0]), int(c[i - 1][0])] += 1

    return liste, liste_trans


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
        # print(name_in)

    def run(self, label, var):
        # print(self.files)

        Larva = 0
        dossier = self.id

        doss = self.files
        name = doss.split('/')[-1]

        # if not os.path.isfile('../DONNE/'+type_+'/'+style+'/Sequence_first_'+doss.split('/')[-1]) :
        N_be = len(label.labels_)

        delta = 1

        fichier = open(doss, 'rb')
        (LAMBDA, TRANS, mu, probabehavior) = pickle.load(fichier)

        # LAMBDA_N = np.zeros((int(var.end_time / 3), N_be))
        # for time in range(0, var.end_time):
        #     LAMBDA_N[int(time / 3)] += LAMBDA[time, :]
        # LAMBDA_N = LAMBDA_N / 3
        #
        # TRANS_N = np.zeros((int(var.end_time / 3), N_be, N_be))
        # for time in range(0, var.end_time):
        #     TRANS_N[int(time / 3)] += TRANS[time, :, :]
        # TRANS_N = TRANS_N / 3

        # TRANS_ = np.zeros((var.end_time, N_be, N_be))
        # LAMBDA_ = np.zeros((var.end_time, N_be))
        #
        # for time in range(0, var.end_time):
        #     TRANS_[time] = TRANS_N[int(time / 3), :, :]
        #
        # for time in range(0, var.end_time):
        #     LAMBDA_[time] = LAMBDA_N[int(time / 3), :]
        # if len(probabehavior)==7 :
        #     os.rename(doss, doss.split('t5/')[0]+'t5/NOfalsel'+doss.split('/')[-1])
        if not os.path.exists('../FIGURE/fig_new/' + var.type + '/' + name.split('#n#')[0]):
            os.mkdir('../FIGURE/fig_new/' + var.type
                     + '/' + name.split('#n#')[0])

    #    print(N_be)

        TRANS = abs(TRANS)
        larva_number = 500
        print('../DATA_EXPERIMENTAL/' + var.type + '/' + label.nom + '/' +
              '_' + name)
        if os.path.isfile('../DATA_EXPERIMENTAL/' + var.type + '/' + label.nom + '/' + name):

            with open('../DATA_EXPERIMENTAL/' + var.type + '/'
                      + label.nom + '/' + name, 'rb') as fichier_data :

                #    print(fichier_data)
                (VAR, PROBA_TAB, MAX, compdata, gene,
                 nbb, Deb) = pickle.load(fichier_data)
                Deb = Deb[~(Deb == 0.0)]
                larva_number = len(compdata)
                data = 'yes'

        else:
            data = 'none'
            compdata = 0
            VAR = 0
            PROBA_TAB = 0

       #  ref = 'no'
       #  REF_ = glob.glob('../INFERENCE_DATA/' + label.nom
       #                   + '/' + var.type + '/MZZ_R_*' + name.split('@')[1] + '*')
       #  #print('../INFERENCE_DATA/' + label.nom + '/' +
       #  #      var.type + '/MZZ_R_*' + name.split('@')[1] + '*')
       # # print(REF_)
       #  if len(REF_) != 0:
       #      fichier_ref = open(REF_[0], 'rb')
       #      (LAMBDA_ref, TRANS_ref, mu_ref,
       #       probabehavior_ref) = pickle.load(fichier_ref)
       #      ref = 'yes'

        # if data == "yes":
        compo, generation, proba = GENERATIF.generatif(
            TRANS, LAMBDA, mu, probabehavior, larva_number, var, delta)





        nb_groupe = 10
        probaGR = np.zeros((var.end_time * 13, N_be, nb_groupe))

        for groupe in range(0, nb_groupe):

            larva_number_groupe = int(larva_number / 20)
            comp_var, gene_var, proba_var = GENERATIF.generatif(
                TRANS, LAMBDA, mu, probabehavior, larva_number_groupe, var, delta)

            for i in range(0, var.end_time * 13):
                for j in range(0, larva_number_groupe):
                    probaGR[i, int(gene_var[j, i]),
                            groupe] += 1 / larva_number_groupe

        moyenne = np.zeros((var.end_time * 13, N_be))
        variance = np.zeros((var.end_time * 13, N_be))

        for j in range(0, var.end_time * 13):
            for i in range(0, N_be):
                moyenne[j, i] = sum(probaGR[j, i, :])
        for j in range(0, var.end_time * 13):
            for i in range(0, N_be):
                for u in range(0, nb_groupe):
                    variance[j, i] += (probaGR[j, i, u] -
                                       moyenne[j, i] / nb_groupe)**2 / nb_groupe
                variance[j, i] = np.sqrt(variance[j, i])
                moyenne[j, i] = moyenne[j, i] / nb_groupe

        figure.proba(moyenne, proba, variance, name, VAR,
                     PROBA_TAB, data, N_be, var, label, delta)

        # if not os.path.exists('../FIGURE/fig_new/'+type_+'/'+name.split('#n#')[0]):
        #     os.mkdir('../FIGURE/fig_new/'+type_+'/'+name.split('#n#')[0])

        # fig = plt.figure()
        # ax = fig.add_subplot(111)
        # for i in range(0, N_be):
        #     plt.plot(np.linspace(0, var.end_time, len(
        #         LAMBDA[:, i])), LAMBDA[:, i], c=label.Color[i], linewidth=2.5)
        # ax.set_xlabel(r't')
        # ax.set_ylabel(r'\lambda')
        # fig.savefig('../FIGURE/fig_new/' + var.type + '/' + name.split('#n#')
        #             [0] + '/Lambda_' + label.nom + '_' + name.split('#n#')[0] + '.pdf')
        # fig.clf()
        # plt.close(fig)
        #
        # fig = plt.figure()
        # ax = fig.add_subplot(111)
        # # for i in range(0, 5):
        # plt.plot(np.linspace(0, var.end_time, len(
        #     TRANS[:, 0, 0])), TRANS[:, 0, 1], linewidth=2.5, label=r'crawl -> bend')
        # plt.plot(np.linspace(0, var.end_time, len(
        #     TRANS[:, i, 0])), TRANS[:, 1, 0], linewidth=2.5, label='bend -> crawl')
        # # plt.plot(np.linspace(0, var.end_time, len(
        # #     LAMBDA[:, i])), TRANS[:, 2, 0],  linewidth=2.5)
        # # plt.plot(np.linspace(0, var.end_time, len(
        # #     LAMBDA[:, i])), TRANS[:, 2, 1],  linewidth=2.5)
        # # plt.plot(np.linspace(0, var.end_time, len(
        # #     LAMBDA[:, i])), TRANS[:, 1, 2],  linewidth=2.5)
        # # plt.plot(np.linspace(0, var.end_time, len(
        # #     LAMBDA[:, i])), TRANS[:, 4, 1],  linewidth=2.5)
        # # plt.plot(np.linspace(0, var.end_time, len(
        # #     LAMBDA[:, i])), TRANS[:, 0, 4],  linewidth=2.5)
        # ax.set_xlabel(r't')
        # ax.set_ylabel(r'\mathbf{T}')
        # plt.legend()
        # fig.savefig('../FIGURE/fig_new/' + var.type + '/' + name.split('#n#')
        #             [0] + '/Transition_' + label.nom + '_' + name.split('#n#')[0] + '.pdf')
        # fig.clf()
        # plt.close(fig)
        #
        # fig = plt.figure()
        # ax = fig.add_subplot(111)
        # plt.plot(np.linspace(0, var.end_time, len(
        #     LAMBDA[:, i])), TRANS[:, 4, 1],  linewidth=2.5, label='hunch -> bend')
        # plt.plot(np.linspace(0, var.end_time, len(
        #     LAMBDA[:, i])), TRANS[:, 0, 4],  linewidth=2.5, label='crawl -> hunch')
        # plt.legend()
        # ax.set_xlabel(r't')
        # ax.set_ylabel(r'\mathbf{T}')
        # fig.savefig('../FIGURE/fig_new/' + var.type + '/' + name.split('#n#')
        #             [0] + '/Transition_Hunch_' + label.nom + '_' + name.split('#n#')[0] + '.pdf')
        # fig.clf()
        # plt.close(fig)
        # fig = plt.figure()
        # ax = fig.add_subplot(111)
        # plt.plot(np.linspace(0, var.end_time, len(
        #     LAMBDA[:, i])), TRANS[:, 2, 0],  linewidth=2.5, label='stop -> crawl')
        # plt.plot(np.linspace(0, var.end_time, len(
        #     LAMBDA[:, i])), TRANS[:, 2, 1],  linewidth=2.5, label='stop -> bend')
        # plt.plot(np.linspace(0, var.end_time, len(
        #     LAMBDA[:, i])), TRANS[:, 1, 2],  linewidth=2.5, label='bend -> stop')
        # # plt.plot(np.linspace(0, var.end_time, len(
        # #     LAMBDA[:, i])), TRANS[:, 4, 1],  linewidth=2.5)
        # # plt.plot(np.linspace(0, var.end_time, len(
        # #     LAMBDA[:, i])), TRANS[:, 0, 4],  linewidth=2.5)
        # ax.set_xlabel(r't')
        # ax.set_ylabel(r'\mathbf{T}')
        # plt.legend()
        # fig.savefig('../FIGURE/fig_new/' + var.type + '/' + name.split('#n#')
        #             [0] + '/Transition_Stop_' + label.nom + '_' + name.split('#n#')[0] + '.pdf')
        # fig.clf()
        # plt.close(fig)

        # fig = plt.figure()
        # ax = fig.subplots(4, 4)
        # for j in range(0, 15):
        #     print(j % 4, j // 4, j)
        #     im = ax[j % 4, j // 4
        #             ].imshow(TRANS[int(var.activation_time + j * 2), :, :], cmap="viridis", vmin=0, vmax=1)
        #     ax[j % 4, j // 4].set_axis_off()
        # ax[3, 3].set_axis_off()
        # #print(TRANS[int(j * 2), :, :], TRANS[var.activation_time, :, :])
        # #fig.colorbar(pcm, ax=ax[j % 4, j // 4])
        # cax = fig.add_axes([0.9, 0.1, 0.03, 0.8])
        # fig.colorbar(im, cax=cax)
        #
        # fig.savefig('../FIGURE/fig_new/' + var.type + '/' + name.split('#n#')
        #             [0] + '/Transition_mesh_' + label.nom + '_' + name.split('#n#')[0] + '.pdf')
        # fig.clf()
        # plt.close(fig)
        if data == 'yes':
            Histo_data_A, Histo_A, Histo_data_T, Histo_T = figure.histo(
                compo, compdata, name, data, N_be, label, var, delta)
        # Lenght_, Lenght_F, liste = figure.seq(
        # compo, compdata, name, data, N_be, var, label, delta)
            data_bis = figure.seq(compo, compdata, name,
                                  data, N_be, var, label, delta)

            fofo = open('../DONNE/' + var.type + '/' + label.nom + '/' + str(delta) +
                        'data_gene_' + doss.split('/')[-1], 'wb')
            pickle.dump((proba, variance, VAR, PROBA_TAB,
                         data_bis, Histo_data_A, Histo_A, Histo_data_T, Histo_T), fofo)
            fofo.close()

        # figure.proba(proba,variance,name,VAR, PROBA_TAB,data,N_be,delta)

        # f= open('../FIGURE/fig_new/'+type_+'/'+name.split('#n#')[0]+'/proba_'+doss.split('/')[-1], 'wb')
        # pickle.dump( (proba,variance, VAR, PROBA_TAB), f)
        # f.close()

        # fi= open('../FIGURE/fig_new/'+type_+'/'+name.split('#n#')[0]+'/small_sequence_'+doss.split('/')[-1], 'wb')
        # pickle.dump( (Lenght_F, Lenght_, liste), fi)
        # fi.close()

        # figure.sequence(compo,compdata,name,data,Deb,delta)

        # figure.seq(compo,compdata,name,data,N_be,delta)

        # figure.time_ampl(compo,compdata,name,data,N_be,delta)

        # f= open('../GENERATIF_DATA/Amplitude/'+type_+'/Generatif'+doss.split('/')[-1], 'wb')
        # PB=np.array(probabehavior)
        # pickle.dump( (compo, generation, Posterior,variance,moyenne), f)
        # f.close()


def main(arg_str):

    version = 20180409
    print(version)
    arg_parser = argparse.ArgumentParser(
        description='Larvae behavior analysis')
    arg_parser.add_argument(
        '-v', '--version', action='version', version='%(prog)s ' + str(version))
    arg_parser.add_argument('--id', required=True, action='store', type=int,
                            help='A simulation identifier to be added to the output file')
    arg_parser.add_argument('-n', '--name', action='store',
                            type=str, help='name_files')
    arg_parser.add_argument('-a', '--ac',
                            action='store', type=str, help='name_files')
    arg_parser.add_argument(
        '-s', '--state', action='store', type=str, help='name_files')

    input_args = arg_parser.parse_args(arg_str.split())
    state = input_args.state
    ac = input_args.ac
    name = input_args.name

    var = choose(ac)
    label = chooselabel(state)

    id = input_args.id
    noeuds = MATRICE(name, id, label, var)
