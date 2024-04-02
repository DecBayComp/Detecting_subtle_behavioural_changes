
import copy
import os.path

import numpy
import pandas as pd
from scipy.optimize import curve_fit


class INITIALISATION():

    def __init__(self, larva, N_be, label, var):

        self.LAMBDA = numpy.zeros((var.end_time + 1, N_be))
        # self.A_=numpy.zeros((end_time+1,6))
        self.transtot = numpy.zeros((var.end_time + 1, N_be, N_be))
        self.probabehavior = numpy.zeros(N_be)
        self.OUT = numpy.zeros((N_be, int((var.end_time + 1) * 13) + 1))
        self.IN = numpy.zeros((N_be, int((var.end_time + 1) * 13) + 1))
        self.IS = numpy.zeros((N_be, int((var.end_time + 1) * 13) + 1))
        self.STAY = numpy.zeros((int((var.end_time + 1)), N_be, larva))
        self.OUT_TRANS = numpy.zeros(
            (int((var.end_time + 1)), N_be, N_be, larva))
        self.out_t = numpy.zeros((larva, var.end_time + 1, N_be, N_be))

        self.number = numpy.zeros((int((var.end_time + 1)), N_be, larva))
        self.X = numpy.zeros((var.end_time + 1, N_be, 50, larva))
        self.mu_ini = numpy.zeros((var.end_time + 1, N_be, 4, 10))
        # self.Table=numpy.zeros((end_time+1,6,13,50,larva))

        self.Table = []

    def proba_ini(self, TAB, l, N_be, label, var):
        PRO = []
        [PRO.append([]) for i in range(0, N_be)]
        # print(PRO)
        #PRO = [[], [], [], [], [], [], []]
        for j in range(5, var.activation_time - 3):
            TITI = TAB[((TAB[:, 0] > j))]
            TITI = TITI[((TITI[:, 0] < j + 1))]
            if len(TITI) > 1:
                [PRO[i].append((list(TITI[:, 1]).count(float(i))) /
                               max(1, len(TITI[:, 1]))) for i in range(0, 6)]
        del TITI

        for j in range(0, N_be):
            self.probabehavior[j] = (
                self.probabehavior[j] + sum(PRO[j]) / max(1, len(PRO[j])))

    def parameters_active(self, TAB, l, N_be, label, var):
        #print('larva', l, self.LAMBDA)
        a = []
        [a.append([[], [], [], []]) for i in range(0, N_be)]
        Tabl = []
        #print(len(self.Table),l, len(self.Table))
        [Tabl.append(a) for j in range(var.end_time + 1)]

        # print(l,Tabl)
       # print(len(Tabl),len(Tabl[0]),len(Tabl[0][0]))

        old = None
        TAB_LARVA = TAB[~(TAB[:, 0] < 5)]
        TAB_LARVA = TAB_LARVA[~(TAB_LARVA[:, 0] > var.end_time - 0.01)]
        Ampl = []
        a = 0
        delta_t = 0

        for k in range(1, len(TAB_LARVA)):

            self.IS[int(TAB_LARVA[k - 1, 1]),
                    int(TAB_LARVA[k - 1, 0] * 13)] += 1
            if int(TAB_LARVA[k, 0] * 13) - int(TAB_LARVA[k - 1, 0] * 13) == 2:
                self.IS[int(TAB_LARVA[k - 1, 1]),
                        int(TAB_LARVA[k - 1, 0] * 13 + 1)] += 1
            # if int(TAB_LARVA[k - 1, 1]) == 6:
            #     print(self.IS[int(TAB_LARVA[k - 1, 1]),
            #                   int(TAB_LARVA[k - 1, 0] * 13)])
            # self.Ax_[int(TAB_LARVA[k,0]),int(TAB_LARVA[k,1]),l]+=(abs(TAB_LARVA[k,3]))
            self.number[int(TAB_LARVA[k, 0]), int(TAB_LARVA[k, 1]), l] += 1
            #print(k, TAB_LARVA[k - 1, 1], TAB_LARVA[k - 1, 0], TAB_LARVA[k, 3])
            Ampl.append(TAB_LARVA[k, 3])

            if TAB_LARVA[k, 1] != TAB_LARVA[k - 1, 1]:
                # print(Tabl[int(TAB_LARVA[k-1,0])][int(TAB_LARVA[k-1,1])],'before',int(TAB_LARVA[k-1,0]))
                # self.X[int(TAB_LARVA[k,0]),int(TAB_LARVA[k-1,1]),a,l]=max(Ampl)
                # print(Ampl)
                Index_amp = [abs(Ampl[i]) for i in range(len(Ampl))].index(
                    max([abs(Ampl[i]) for i in range(len(Ampl))]))
                if int(delta_t / 65) >= 4:
                    delta_t = 259

                if int(TAB_LARVA[k - 1, 0]) < var.activation_time - 3:
                    for time in range(0, var.activation_time - 3):
                        #    print(int(TAB_LARVA[k - 1, 0]), time)
                        Tabl[time][int(TAB_LARVA[k - 1, 1])
                                   ][int(delta_t / 65)].append(Ampl[Index_amp])
                else:
                    #    print(int(TAB_LARVA[k - 1, 0]), int(TAB_LARVA[k - 1, 1]))
                    Tabl[int(TAB_LARVA[k - 1, 0])][int(TAB_LARVA[k - 1, 1])
                                                   ][int(delta_t / 65)].append(Ampl[Index_amp])
            #    print(Tabl, 'table')
                Ampl = []
                delta_t = 0

                self.OUT[int(TAB_LARVA[(k - 1), 1]),
                         int(TAB_LARVA[k, 0] * 13)] += 1
                self.IN[int(TAB_LARVA[k, 1]), int(TAB_LARVA[k, 0] * 13)] += 1
                self.transtot[int(TAB_LARVA[k, 0]), int(
                    TAB_LARVA[k - 1, 1]), int(TAB_LARVA[k, 1])] += 1

                # if old is not None :

                #     self.trans_3[int(TAB_LARVA[k,0]),old,int(TAB_LARVA[k-1,1]),int(TAB_LARVA[k,1])]+=1

                self.OUT_TRANS[int(TAB_LARVA[k, 0]), int(
                    TAB_LARVA[k - 1, 1]), int(TAB_LARVA[k, 1]), l] += 1

                # if type(self.out_t[l][int(TAB_LARVA[k,0])][int(TAB_LARVA[k,1])][int(TAB_LARVA[k-1,1])])==int :
                self.out_t[l][int(TAB_LARVA[k, 0])][int(
                    TAB_LARVA[k, 1])][int(TAB_LARVA[k - 1, 1])] += 1

                # else :
                #     if old is not None :
                #         self.out_t[l][int(TAB_LARVA[k,0])][int(TAB_LARVA[k,1])][int(TAB_LARVA[k-1,1])][old]+=1
                # old=int(TAB_LARVA[k-1,1])
            else:

                # if int(TAB_LARVA[k-1,0])< activation_time-3 :
                #    time_=0
                # else :
                #    time_=int(TAB_LARVA[k-1,0])
                #Index_amp=[abs(Ampl[i]) for i in range(len(Ampl))].index(max([abs(Ampl[i]) for i in range(len(Ampl))]))
                # self.Table[l][time_][int(TAB_LARVA[k-1,1])][int(delta_t/5)].append(Ampl[Index_amp])
                # Ampl=[]

                delta_t += 1

                self.STAY[int(TAB_LARVA[k - 1, 0]),
                          int(TAB_LARVA[k - 1, 1]), l] += 1

        if len(Ampl) > 0:
            Index_amp = [abs(Ampl[i]) for i in range(len(Ampl))].index(
                max([abs(Ampl[i]) for i in range(len(Ampl))]))
            if int(delta_t / 26) >= 10:
                delta_t = 259

            if int(TAB_LARVA[k - 1, 0]) < var.activation_time - 3:
                for time in range(0, var.activation_time - 3):
                    Tabl[time][int(TAB_LARVA[k - 1, 1])
                               ][int(delta_t / 65)].append(Ampl[Index_amp])
            else:
                Tabl[int(TAB_LARVA[k, 0])][int(TAB_LARVA[k - 1, 1])
                                           ][int(delta_t / 65)].append(Ampl[Index_amp])

        del Ampl
        del delta_t
        del TAB_LARVA

        # for time in range(1,activation_time-3):
        #     for j in range(0,6):
        #         for i in range(0,10):
        #             self.Table[l][0][j][i].extend(self.Table[l][time][j][i])

        # for time in range(1,activation_time-3):
        #     self.Table[l][time]=self.Table[l][0]
        if l == 0:
            self.Table.append([])
         #   print(self.Table)
            self.Table[0] = copy.deepcopy(Tabl)
        else:
            self.Table.append([])
            self.Table[l] = copy.deepcopy(Tabl)
        #print(self.Table, 'table a voir')

        for j in range(5, var.activation_time - 3):
            for k in range(N_be):
                for m in range(N_be):
                  #      if type(self.out_t[l][0][k][m])==int :
                    self.out_t[l][0][k][m] += self.out_t[l][j][k][m]
                    # else :
                    #     for x in range(N_be) :
                    #         self.out_t[l][0][k][m][x]+=self.out_t[l][j][k][m][x]

        for j in range(1, var.activation_time - 3):
            self.out_t[l][j] = self.out_t[l][0]

    def regroupement_larva(self, larva, N_be, label, var):
        # OMEGA_ACTIVE=numpy.zeros((6,end_time+1))
        LAMBDA_ACTIVE = numpy.zeros((var.end_time + 1, N_be))
        trans = self.transtot

        Bin_ = numpy.zeros((var.end_time + 1, N_be, 10))

        for j in range(0, (var.end_time)):
            for i in range(0, N_be):
                SOMME = 0
                NB = 0
                # Somme_log_1=0.0
                # Somme_log_=0.0
                if i in [0, 1, 6]:
                    for time in range(int((j) * 13), min(int((j + 1) * 13), int((var.end_time + 1) * 13))):
                        if self.IS[i, time - 1] != 0:
                            SOMME += 13 * \
                                (self.OUT[i, time] / self.IS[i, time - 1])
                            NB += 1
                    for x in range(0, 10):
                        Bin_[j, i, x] = sum(self.X[j, i, x, :])

                    LAMBDA_ACTIVE[j, i] = SOMME / max(1, NB)

                if i in [2, 3, 4, 5]:
                    for time in range(int((j) * 13), min(int((j + 3) * 13), int((var.end_time + 1) * 13))):
                        if self.IS[i, time - 1] != 0:
                            SOMME += 13 * \
                                (self.OUT[i, time] / self.IS[i, time - 1])
                            NB += 1

                    for x in range(0, 10):
                        Bin_[j, i, x] = sum(self.X[j, i, x, :])

                    LAMBDA_ACTIVE[j, i] = SOMME / max(1, NB)

        for j in range(var.activation_time - 3, var.end_time):
            for i in range(0, N_be):
                som_ = sum(Bin_[j, i, :])
                if som_ != 0:
                    for x in range(0, 10):
                        Bin_[j, i, x] = Bin_[j, i, x] / som_
        for j in range(5, var.end_time + 1):
            for i in range(0, N_be):
                SUM = []
                [SUM.append(sum(trans[j, i, :])) for k in range(0, N_be)]
                if SUM[0] != 0:
                    trans[j, i, :] = list(trans[j, i, :] / numpy.asarray(SUM))
        nb = numpy.zeros(N_be)
        nb3 = numpy.zeros((N_be, N_be))
        # NN=numpy.zeros(6)
        for j in range(5, var.activation_time - 3):
            for k in range(0, N_be):

                if sum(trans[j][k]) != 0:
                    nb[k] += 1
                for m in range(0, N_be):
                    trans[0, k, m] += trans[j, k, m]

            self.STAY[0, :, :] += self.STAY[j, :, :]
  #          self.Table[0,:,:,:]+=self.Table[j,:,:,:]
            self.OUT_TRANS[0, :, :, :] += self.OUT_TRANS[j, :, :, :]
            LAMBDA_ACTIVE[0, :] += LAMBDA_ACTIVE[j, :]
            self.number[0, :, :] += self.number[j, :, :]
            # self.X[0,:,:,:]+=self.X[j,:,:,:]

        for i in range(0, N_be):
            som = sum(sum(Bin_[5:var.activation_time - 3, i, :]))
            if som != 0:
                for x in range(10):
                    Bin_[0, i, x] = sum(
                        Bin_[5:var.activation_time - 3, i, x]) / som

        for j in range(1, var.activation_time - 3):
            for k in range(0, N_be):
                Bin_[j, k, :] = Bin_[0, k, :]
                LAMBDA_ACTIVE[j, k] = LAMBDA_ACTIVE[0, k] / max(1, nb[k])
                # alpha_[j,k]=alpha_[0,k]/max(1,NN[k])
                # beta_[j,k]=beta_[0,k]/max(1,NN[k])
                for m in range(N_be):
                    trans[j][k][m] = trans[0][k][m] / (max(1, nb[k]))

                for u in range(0, len(self.STAY[0, 0, :])):
                    self.STAY[j, k, u] = self.STAY[0, k, u]
                    # self.X[j,k,:,u]=self.X[0,k,:,u]
                    # self.log_Ax_[j,k,u]=self.log_Ax_[0,k,u]
                    self.number[j, k, u] = self.number[0, k, u]
                    for m in range(0, N_be):
                        self.OUT_TRANS[j, k, m, u] = self.OUT_TRANS[0, k, m, u]

        del nb3
        b = []
        [b.append([]) for i in range(var.end_time)]
        a = []
        [a.append(b) for i in range(0, N_be)]
        opp = []
        [opp.append(a) for j in range(var.end_time)]

        op = copy.deepcopy(opp)

        for larva in range(0, len(self.Table)):
            for i in range(0, var.end_time):
                for j in range(0, N_be):
                    for D_T in range(0, 4):
                        op[i][j][D_T].extend(self.Table[larva][i][j][D_T])

        for i in range(0, var.end_time):
            for j in range(0, N_be):
                for D_T in range(0, 4):
                    if len(op[i][j][D_T]) != 0:
                        op[i][j][D_T] = sorted(op[i][j][D_T])
                        number = max([1, len(op[i][j][D_T]) / 10])
                        # print(number)
                        for number_kernel in range(10):
                            self.mu_ini[i, j, D_T, number_kernel] = sum(op[i][j][D_T][int(number * number_kernel):int(
                                (number_kernel + 1) * number)]) / (int((number_kernel + 1) * number) - int(number * number_kernel))
                           # print(op[i][j][D_T][int(number*number_kernel):int((number_kernel+1)*number)],(int((number_kernel+1)*number)-int(number*number_kernel)))
        # for i in range(0, len(self.mu_ini)):
        #     for j in range(0, len(self.mu_ini[i])):
        #         for h in range(0, len(self.mu_ini[i][j])):
        #             for g in range(0, len(self.mu_ini[i][j][h])):
        #                 if (self.mu_ini[i][j][h][g]) > 1 or (self.mu_ini[i][j][h][g]) < -1:
        #                     print(self.mu_ini[i][j][h][g], i, j, h, g, 'mu')

        trans[0] = trans[1]
        # self.Table[0,:,:]=self.Table[1,:,:]
        self.STAY[0, :, :] = self.STAY[1, :, :]
        self.OUT_TRANS[0, :, :, :] = self.OUT_TRANS[1, :, :, :]

        LAMBDA_ACTIVE[0, :] = LAMBDA_ACTIVE[1, :]

        self.LAMBDA = LAMBDA_ACTIVE
        self.transtot = trans
        self.bin_ = Bin_

        del LAMBDA_ACTIVE
        del trans
        del Bin_
