import numpy
import random
import function
from random import gauss
import function
import sys
import math
from numpy.random import beta
import random


def generatif(trans_begin, LAMBDA_begin, mu_begin, probabehavior, larvaNB, var, delta):

    N_be = len(probabehavior)
    gene = numpy.zeros((larvaNB, var.end_time * 13))
    Posterior_func = numpy.zeros((larvaNB, var.end_time + 1))
    comp = []
    [comp.append([]) for i in range(0, larvaNB)]
    Posterior_func += 1
    nomber_chut = 0
    trans = numpy.copy(trans_begin)

    for i in range(0, N_be):
        if sum(sum(trans[:, i, :])) == 0:
            for j in range(0, int(var.end_time / delta)):
                for x in range(0, N_be):
                    trans[j, x, i] = 0

    # for larva in range(0,larvaNB):

    #     trans=numpy.copy(trans_begin)
    #     LAMBDA=numpy.copy(LAMBDA_begin)
    #     mu=numpy.copy(mu_begin)

    #     Behav=function.aleatoire(probabehavior)
    #     time_total=0

    #     while time_total < end_time :

    #         if time_total>0 :
    #             Behav_old=Behav
    #             Behav0=function.aleatoire(trans[j][Behav])
    #             chut=0

    #             while Behav0==6 :
    #                 nomber_chut=+1
    #                 chut+=1
    #                 Behav0=function.aleatoire(trans[j][Behav])
    #                 if chut > 10 :
    #                     break

    #             if (sum(trans[j][Behav0])<0.2) :
    #               #  print('transition',Behav0,j,trans[j])
    #                 Index_=[]
    #                 for index in range(0,end_time):
    #                     if sum(trans[index][Behav0])>0.2:
    #                         Index_.append(index)

    #                 idx=(numpy.abs(numpy.array(Index_)-j)).argmin()
    #                 if Index_!=[] :
    #                     chut_2=0
    #                     trans[j][Behav0]=trans[Index_[idx]][Behav0]
    #                     while (sum(trans[j][Behav0])+sum(trans[j+1][Behav0])<0.2):
    #                         chut_2+=1
    #                         Behav0=function.aleatoire(trans[j][Behav])
    #                         if chut_2 >10 :
    #                             break
    #             Behav=Behav0

    #         if (LAMBDA[int(time_total)][Behav]==0):
    #             Index_=[]
    #             for index in range(0,end_time):
    #                 if sum(trans[index][Behav0])>0.76:
    #                     Index_.append(index)
    #             idx=(numpy.abs(numpy.array(Index_)-time_total)).argmin()
    #             LAMBDA[int(time_total)][Behav]=LAMBDA[Index_[idx]][Behav]
    #         if LAMBDA[int(time_total)][Behav]==0 :
    #             LAMBDA[int(time_total)][Behav]=10

    #         dt= -1/(LAMBDA[int(time_total)][Behav])*numpy.log(random.random())
    #         j=int(time_total)

    #         if dt >= 26 :
    #             DT=9
    #         else :
    #             DT=int((dt*10)/26)

    #         if sum(mu[int(time_total),Behav,DT,:])<0.05 :
    #             Index_=[]
    #             for index in range(0,end_time):
    #                 if sum(mu[index,Behav,DT,:])>0.05:
    #                     Index_.append(index)

    #                 if len(Index_)>0:
    #                     idx=(numpy.abs(numpy.array(Index_)-j)).argmin()
    #                     mu[j,Behav,DT,:]=mu[Index_[idx],Behav,DT,:]

    #         liste_ampl=[]

    #         [liste_ampl.append(random.gauss(mu[int(time_total),Behav,DT,nombre],0.1)) for nombre in range(0,10)]
    #         Ampl_=sum(liste_ampl)

    #         comp[larva].extend([[Behav,dt,Ampl_]])

    #         for number in range(int(time_total*13),min(int((time_total+dt)*13),int(end_time*13))):
    #             gene[larva,number]=Behav

    #         time_total=time_total+dt
    #         j=int(time_total)

    # return comp, gene

    for larva in range(0, larvaNB):
        # print(larva)
        trans = numpy.copy(trans_begin)
        LAMBDA = numpy.copy(LAMBDA_begin)
        mu = numpy.copy(mu_begin)

        Ampl_ = []
        Behav = function.aleatoire(probabehavior)
        # print(Behav)
        #print(probabehavior, Behav, LAMBDA.shape)
        # Posterior_func[larva,0]=Posterior_func[larva,0]*probabehavior[Behav]
        time_comp = 0
        for j in range(0, var.end_time):
            # print(j)

            for delta_t in range(0, 13):
                time_comp += 1 / 13
                gene[larva, j * 13 + delta_t] = Behav
#                print(Behav)
                if (LAMBDA[int(j / delta)][Behav] == 0):
                    Index_ = []
                    for index in range(0, int(var.end_time / delta)):
                        if LAMBDA[index][Behav] > 0:
                            Index_.append(index)
                    try:
                        idx = (numpy.abs(numpy.array(Index_)
                                         - int(j / delta))).argmin()
                        LAMBDA[int(j / delta)
                               ][Behav] = LAMBDA[Index_[idx]][Behav]
                    except:
                        # LAMBDA[j][Behav]==0 :
                        LAMBDA[int(j / delta)][Behav] = 10

                nbb = random.random()
                if nbb < (1 - numpy.exp(-LAMBDA[int(j / delta)][Behav] * (1 / 13))):

                    if time_comp >= 26:
                        DT = 3
                    else:
                        DT = int((time_comp * 10) / 65)

                    liste = [0, 1, 2, 3]

                    while sum(mu[int(j / delta), Behav, DT, :]) == 0:
                        Index_ = []
                        idx = liste[(
                            numpy.abs(numpy.array(liste) - DT)).argmin()]

                        for index in range(int(var.end_time / delta)):
                            if sum(mu[index, Behav, idx, :]) != 0:
                                Index_.append(index)
                            if len(Index_) > 0:
                                idx2 = (
                                    numpy.abs(numpy.array(Index_) - int(j / delta))).argmin()
                                mu[int(j / delta), Behav, DT, :] = mu[Index_[
                                    idx2], Behav, idx, :]
                        liste.remove(idx)
                        # print(idx,DT,Behav,j)
                        if len(liste) == 0:
                            # print('fini')
                            break

                    # print(mu[j,Behav,DT,:],DT,j,Behav)

                    liste_ampl = []
                    for nombre in range(0, 10):

                        if mu[int(j / delta), Behav, DT, nombre] > -1.1 and mu[int(j / delta), Behav, DT, nombre] < 1.1 and mu[int(j / delta), Behav, DT, nombre] != 0:
                            a = random.gauss(
                                mu[int(j / delta), Behav, DT, nombre], 0.1)
                            # print(mu[j,Behav,DT,nombre],'mu')
                            nb = 0

                            while a > 1 or a < -1:
                                nb += 1
                                a = random.gauss(
                                    mu[int(j / delta), Behav, DT, nombre], 0.1)

                                if mu[int(j / delta), Behav, DT, nombre] > 1.1:
                                    a = random.gauss(
                                        mu[int(j / delta), Behav, DT, nombre], mu[int(j / delta), Behav, DT, nombre] - 1)
                                if mu[int(j / delta), Behav, DT, nombre] < -1.1:
                                    a = random.gauss(
                                        mu[int(j / delta), Behav, DT, nombre], -mu[int(j / delta), Behav, DT, nombre] + 1)

                                # if nb%1000==0 :
                                #     print(nb , mu[j,Behav,DT,nombre] ,'f')

                            liste_ampl.append(a)
                    #print(liste_ampl,'liste ampl',Behav)
                    if len(liste_ampl) > 0:
                        Ampl_ = random.choice(liste_ampl)
                    else:
                       # print(mu[j,Behav,:,:],j,Behav,DT)
                        Ampl_ = 0
                    # try :
                    #     if Behav_old==Behav and len(compo[larva])>0 :
                    #         print(trans[j][Behav],Behav,j,Behav_old,'humhum')
                    # except :
                    #     print('uu')
                    comp[larva].extend([[Behav, time_comp, Ampl_]])
                    # print(Behav,'prems')
                    Ampl_ = []

                    Behav0 = function.aleatoire(trans[int(j / delta)][Behav])
                    # try :
                    #     if Behav0==Behav :
                    #         print(trans[j][Behav],j,Behav,Behav0,'beuh')
                    # except :
                    # print('uu')

                    chut = 0
                    while Behav0 == N_be:
                        nomber_chut = +1
                        chut += 1
                        Behav0 = function.aleatoire(
                            trans[int(j / delta)][Behav])
                        if chut > 10:
                            break

                    if (sum(trans[int(j / delta)][Behav0]) < 0.2):
                        Index_ = []
                        for index in range(0, int(var.end_time / delta)):
                            if sum(trans[index][Behav0]) > 0.2:
                                Index_.append(index)

                        if Index_ != []:
                            idx = (numpy.abs(numpy.array(Index_)
                                             - int(j / delta))).argmin()
                            trans[int(j / delta)
                                  ][Behav0] = trans[Index_[idx]][Behav0]

                        # if j==end_time-1 :
                        #     break

                        chut_2 = 0
                        Behav0 = function.aleatoire(
                            trans[int(j / delta)][Behav])
                        while Behav0 == Behav or Behav0 == N_be:
                            chut_2 += 1
                            Behav0 = function.aleatoire(
                                trans[int(j / delta)][Behav])
                            #print('dernier', Behav0)
                            if chut_2 > 10:
                                break

                    Behav_old = Behav
                    # if Behav==Behav0 :
                    #     print(Behav, Behav0,j,trans[j][Behav])
                    Behav = Behav0
                   # print(Behav,'deux')

                    time_comp = 1 / 13

        if time_comp >= 26:
            DT = 3
        else:
            DT = int((time_comp * 10) / 65)

        liste = [0, 1, 2, 3]

        while sum(mu[int(j / delta), Behav, DT, :]) == 0:
            idx = liste[(numpy.abs(numpy.array(liste) - DT)).argmin()]
            Index_ = []
            for index in range(int(var.end_time / delta)):
                if sum(mu[index, Behav, idx, :]) != 0:
                    Index_.append(index)
                if len(Index_) > 0:
                    idx2 = (numpy.abs(numpy.array(
                        Index_) - int(j / delta))).argmin()
                    mu[int(j / delta), Behav, DT,
                       :] = mu[Index_[idx2], Behav, idx, :]
            liste.remove(idx)
            if len(liste) == 0:
                # print('fini')
                break

        liste_ampl = []

        for nombre in range(0, 10):
            if mu[int(j / delta), Behav, DT, nombre] != 0:
                a = random.gauss(mu[int(j / delta), Behav, DT, nombre], 0.1)
                nb = 0
                while a > 1 or a < -1:
                    nb += 1
                    a = random.gauss(
                        mu[int(j / delta), Behav, DT, nombre], 0.1)
                    if mu[int(j / delta), Behav, DT, nombre] > 1.1:
                        a = random.gauss(
                            mu[int(j / delta), Behav, DT, nombre], mu[int(j / delta), Behav, DT, nombre] - 1)
                    if mu[int(j / delta), Behav, DT, nombre] < -1.1:
                        a = random.gauss(
                            mu[int(j / delta), Behav, DT, nombre], -mu[int(j / delta), Behav, DT, nombre] + 1)
                    # if nb% 1000==0 :
                    #     print(nb,mu[j,Behav,DT,nombre])

                liste_ampl.append(a)

        if len(liste_ampl) > 0:
            Ampl_ = random.choice(liste_ampl)
        else:
           # print(mu[j,Behav,:,:],j,Behav,DT)
            Ampl_ = 0

        comp[larva].extend([[Behav, time_comp, Ampl_]])

        # if larva%50==0 :
        #     print(larva)
    proba = numpy.zeros((var.end_time * 13, N_be))
    for i in range(0, var.end_time * 13):
        for j in range(0, len(gene[:, 0])):
            proba[i, int(gene[j, i])] += 1 / len(gene[:, 0])

    return comp, gene, proba
