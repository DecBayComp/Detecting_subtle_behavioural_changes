
import numpy as np
import os.path
from scipy.optimize import curve_fit
from scipy.special import gamma
import scipy.stats
from math import factorial as fac
import math


def binomial(x, y):
    try:
        binom = fac(x) // fac(y) // fac(x - y)
    except ValueError:
        binom = 0
    return binom


def Function(transi, K, mu_, nl, nt, N, Table_x, version, N_be, label, var):   # The rosenbrock function

    OPTI = 0

    for i in range(1, len(N[0, 0, :]) - 1):
        for time in range(0, int(var.end_time / 5)):
            for j in range(0, N_be):

                Sum = 0
                for m in range(0, N_be):
                    # if type(transi[time][j][m])==np.float64 or type(transi[time][j][m])==np.float :
                    Sum += transi[time][j][m]
                    # else :
                    # Sum+=sum(transi[time][j][m])
                if Sum != 0:
                    OPTI += 1 * (Sum - 1)**2

                if K[int(time)][j] != 0:
                    OPTI += (K[time][j]) * 1 / 10 * sum(N[int(time * 5):int((time + 1) * 5), j, i]) - sum(sum(nl[int(time * 5):int((time + 1) * 5), j, :, i])) * \
                        np.log((K[time][j]) * 1 / 10) + 0.2 * \
                        (K[time][j] - K[time - 1][j])**2
            #    print(OPTI, 'prems')

                for time_d in range(int(time * 5), int((time + 1) * 5)):
                    for delta_time in range(0, len(Table_x[i][time_d][j])):
                        if len(Table_x[i][time_d][j][delta_time]) != 0:
                            for x in range(0, len(Table_x[i][time_d][j][delta_time])):
                                Sum_mix = 0
                                for kernel in range(10):
                                    Sum_mix += np.exp(-((Table_x[i][time_d][j][delta_time][x] - mu_[
                                                      time, j, delta_time, kernel]) / 0.1)**2)
                                # print(Sum_mix)
                                if Sum_mix != 0:
                                    OPTI += np.log(2 * np.sqrt(2 * 3.14)
                                                   ) - np.log(Sum_mix)
                #print(OPTI, 'deuz')
                for m in range(0, N_be):
                    # print(j,m,transi[time][j][m],type(transi[time][j][m]))
                    # if type(transi[time][j][m])==np.float64 or type(transi[time][j][m])==np.float:

                    if transi[time][j][m] != 0:
                        OPTI += - \
                            np.log(abs(transi[time]
                                       [j][m])) * sum(nl[int(time * 5):int((time + 1) * 5), j, m, i])

                    # else :
                    #     for u in range(N_be) :
                    #         if transi[time][j][m][u]!=0 and nt[i][time][j][m][u]!=0 :
                    #             OPTI+=-np.log(abs(transi[time][j][m][u]))*nt[i][time][j][m][u]
            #    print(OPTI, 'troiz')
    return OPTI


def jacobianF(transi, K, mu_, nl, nt, N, Table_x, version, N_be, label, var):

    jaclambda = np.zeros((int(var.end_time / 5 + 1), N_be))
    jac_mu = np.zeros((int(var.end_time / 5 + 1), N_be, 4, 10))
    # jac_beta=np.zeros((var.end_time+1,6))

    jactransition = np.zeros((int(var.end_time / 5 + 1), N_be, N_be))

    for i in range(0, len(N[0, 0, :])):
        for time in range(0, int(var.end_time / 5) - 1):
            for be in range(0, N_be):
                if K[time][be] != 0:
                    if time != 0 and time != var.end_time - 1:
                        jaclambda[time, be] += -sum(sum(nl[int(time * 5):int((time + 1) * 5), be, :, i])) / (K[time][be]) + 1 / 10 * sum(N[int(time * 5):int((time + 1) * 5), be, i]) + 0.4 * (
                            2 * K[time][be] - K[time - 1][be] - K[time + 1][be])
                    if time == 0:
                        jaclambda[time, be] += -sum(sum(nl[int(time * 5):int((time + 1) * 5), be, :, i])) / (
                            K[time][be]) + 1 / 10 * sum(N[int(time * 5):int((time + 1) * 5), be, i]) + 0.4 * (K[time][be] - K[time + 1][be])
                    if time == var.end_time - 1:
                        jaclambda[time, be] += -sum(sum(nl[int(time * 5):int((time + 1) * 5), be, :, i])) / (
                            K[time][be]) + 1 / 10 * sum(N[int(time * 5):int((time + 1) * 5), be, i]) + 0.4 * (K[time][be] - K[time - 1][be])

                for delta_time in range(0, len(Table_x[i][time][be])):
                    if len(Table_x[i][time][be][delta_time]) != 0:
                        for x in range(0, len(Table_x[i][time][be][delta_time])):
                            Sum_mix = 0
                            for kernel in range(10):
                                Sum_mix += np.exp(-((Table_x[i][time][be][delta_time][x] - mu_[
                                                  time, be, delta_time, kernel]) / 0.1)**2)
                            for kernel in range(10):
                                if mu_[time, be, delta_time, kernel] != 0 and (Table_x[i][time][be][delta_time][x] - mu_[time, be, delta_time, kernel]):
                                    jac_mu[time, be, delta_time, kernel] += (2 * np.exp(-((Table_x[i][time][be][delta_time][x] - mu_[time, be, delta_time, kernel]) / 0.1)**2) * (
                                        Table_x[i][time][be][delta_time][x] - mu_[time, be, delta_time, kernel])) / Sum_mix
                                    # if time==37 and be==1 and delta_time==1 and kernel==0 :
                                    #     print(jac_mu[time,be,delta_time,kernel],'jac first',time,be,delta_time,kernel,mu_[time,be,delta_time,kernel],Table_x[i][time][be][delta_time][x])

                Sum = 0
                for m in range(0, N_be):
                    # if type(transi[time][be][m])==np.float64 or type(transi[time][be][m])==np.float :
                    Sum += transi[time][be][m]
                    # jactransition[time][be][m]=0.0
                    if transi[time][be][m] != 0:
                        # jactransition[time][be][m]+=2*(sum(transi[time][be])-1)
                        jactransition[time][be][m] -= nl[time][be][m][i] / \
                            abs(transi[time][be][m])
                    # else :
                    #     transi[time][be][m]=[abs(number) for number in transi[time][be][m]]
                    #     Sum+=sum(transi[time][be][m])
                    #     for u in range(N_be) :
                    #         if transi[time][be][m][u]!=0:
                    #             #jactransition[time][be][m][u]+=2*(sum(transi[time][be][m][1])-1)
                    #             jactransition[time][be][m][u]-=nt[i][time][be][m][u]/transi[time][be][m][u]

                if Sum != 0:
                    for m in range(0, N_be):
                        # if type(transi[time][be][m])==np.float or type(transi[time][be][m])==np.float64:
                        if transi[int(time / 5)][be][m] != 0.0:
                            jactransition[time
                                          ][be][m] += 2 * (Sum - 1)
                        # else :
                        #     for u in range(0,N_be):
                        #         if transi[time][be][m][u]!=0.0 :
                        #             jactransition[time][be][m][u]+=2*(Sum-1)
    # print(jac_mu[37,1,1,0],'jac_mu')
    return jaclambda, jactransition, jac_mu


def HessF(transi, K, mu_, nl, nt, N, Table_x, version, N_be, label, var):
    Hesslambda = np.zeros((int(var.end_time / 5) + 1, N_be))
    HessBin = np.zeros((int(var.end_time / 5) + 1, N_be, 4, 10))

    Hesstransition = np.zeros((int(var.end_time / 5) + 1, N_be, N_be))

    # if version=='new' :
    #     Hesstransition=[]
    #     [Hesstransition.append([]) for i in range(0,var.end_time)]
    #     for time in range(var.end_time) :
    #         for i in range(N_be) :
    #             Hesstransition[time].append([])
    #             for j in range(N_be) :
    #                 if i in [1,4] and j in [1,4] and i!=j:
    #                     Hesstransition[time][i].extend([[0.0,0.0,0.0,0.0,0.0,0.0,0.0]])
    #                 if i in [1,2] and j in [1,2] and i!=j:
    #                     Hesstransition[time][i].extend([[0.0,0.0,0.0,0.0,0.0,0.0,0.0]])
    #                 else :
    #                     Hesstransition[time][i].append(0.0)

    for i in range(1, len(N[0, 0, :])):
        for time in range(0, int(var.end_time / 5)):
            for be in range(0, N_be):
                if K[time][be] != 0:
                    if time > 5 and time < var.end_time - 5:
                        Hesslambda[time, be] += sum(nl[time, be, :, i]) / \
                            K[time][be]**2 + 0.4 * 2
                    if time < 5:
                        Hesslambda[time,
                                   be] += sum(nl[time, be, :, i]) / K[time][be]**2 + 0.4
                    if time > var.end_time - 4:
                        Hesslambda[time,
                                   be] += sum(nl[time, be, :, i]) / K[time][be]**2 + 0.4

                for delta_time in range(0, len(Table_x[i][time][be])):
                    if len(Table_x[i][time][be][delta_time]) != 0:
                        for x in range(0, len(Table_x[i][time][be][delta_time])):
                            Sum_mix = 0
                            for kernel in range(10):
                                Sum_mix += np.exp(-((Table_x[i][time][be][delta_time][x] - mu_[
                                                  time, be, delta_time, kernel]) / 0.1)**2)

                            for kernel in range(10):
                                if mu_[time, be, delta_time, kernel] != 0:
                                    HessBin[time, be, delta_time, kernel] += (2 * np.exp(-((Table_x[i][time][be][delta_time][x] - mu_[time, be, delta_time, kernel]) / 0.1)**2) *
                                                                              (-2 * np.exp(-((Table_x[i][time][be][delta_time][x]-mu_[time, be, delta_time, kernel])/0.1)**2)*(0.1**2)*(Sum_mix) -
                                                                                 2 * (Table_x[i][time][be][delta_time][x] - mu_[time, be, delta_time, kernel])**2 + 2 * np.exp(-((Table_x[i][time][be][delta_time][x] -
                                                                                                                                                                                  mu_[time, be, delta_time, kernel]) / 0.1)**2) * (Sum_mix) * (Table_x[i][time][be][delta_time][x] - mu_[time, be, delta_time, kernel])**2)) / (Sum_mix**2 * 0.1**4)

                                # if time==37 and be==1 and delta_time==1 and kernel==0 :
                                #      #print(-2*np.exp(-((Table_x[i][time][be][delta_time][x]-mu_[time,be,delta_time,kernel])/0.1)**2),'hess')
                                #      print(HessBin[time,be,delta_time,kernel],Table_x[i][time][be][delta_time][x],Sum_mix,time,be,delta_time,kernel,mu_[time,be,delta_time,kernel],'hess')

                for m in range(0, N_be):
                    # if type(transi[time][be][m])==np.float64 or  type(transi[time][be][m])==np.float:
                    if transi[int(time / 5)][be][m] != 0:
                        Hesstransition[int(time / 5)][be][m] += 2
                    if transi[int(time / 5)][be][m] != 0:
                        Hesstransition[int(time / 5)][be][m] += nl[time][be][m][i] / \
                            abs(transi[int(time / 5)][be][m])**2
                    # else :
                    #     for u in range(0,N_be) :
                    #        # Hesstransition[time][be][m][u]=0.0
                    #         if transi[time][be][m][u]!=0:
                    #                 Hesstransition[time][be][m][u]+=2
                    #         if transi[time][be][m][u]!=0:
                    #             Hesstransition[time][be][m][u]+=nt[i][time][be][m][u]/abs(transi[time][be][m][u])**2

    return Hesslambda, Hesstransition, HessBin


class INFERENCE_CLASS():

    def __init__(self, N_be, label, var):
        self.LAMBDA = np.zeros((int(var.end_time / 5), N_be))
        self.mu = np.zeros((int(var.end_time / 5), N_be, 10, 10))
        # self.beta=np.zeros((var.end_time+1,N_be))
        self.TRANS = np.zeros((int(var.end_time / 5), N_be, N_be))

    def inference(self, LAMBDA, transtot, nt_lam, OUT_TRANS, STAY, table, mu, version, N_be, label, var):

        omega = np.zeros((int(var.end_time / 5), N_be))  # learning rate
        omega_ = np.zeros((int(var.end_time / 5), N_be, N_be))
        omega__ = np.zeros((int(var.end_time / 5), N_be, 4, 10))
        omega = omega + 0.1
        omega_ = omega_ + 0.1
        omega__ = omega__ + 0.1

        nb_max_iter = 200  # Nb max d'iteration
        eps = 10  # stop condition
        # print(LAMBDA.shape)
        lamb1 = LAMBDA
        mu1 = mu

        trans1 = transtot
        # print(trans1)
        z0 = Function(trans1, lamb1, mu1, nt_lam,
                      OUT_TRANS, STAY, table, version, N_be, label, var)
        # print(z0)

        cond = eps + 100.0  # start with cond greater than eps (assumption)
        nb_iter = 0
        tmp_z0 = z0
        lamb2 = np.zeros((int(var.end_time / 5), N_be))
        mu2 = np.zeros((int(var.end_time / 5), N_be, 4, 10))

        grad_eval_L = np.zeros((int(var.end_time / 5), N_be))
        grad_eval_Bin = np.zeros((int(var.end_time / 5), N_be, 4, 10))

        if version == 'old':
            grad_eval_T = np.zeros((int(var.end_time / 5), N_be, N_be))
            HessT = np.zeros((int(var.end_time / 5), N_be, N_be))
            trans2 = np.zeros((int(var.end_time / 5), N_be, N_be))

        # if version=='new' :
        #     grad_eval_T=[]
        #     trans2=[]
        #     HessT=[]
        #     [trans2.append([]) for i in range(0,var.end_time)]
        #     [HessT.append([]) for i in range(0,var.end_time)]
        #     [grad_eval_T.append([]) for i in range(0,var.end_time)]
        #     for time in range(var.end_time) :
        #         for i in range(N_be) :
        #             grad_eval_T[time].append([])
        #             trans2[time].append([])
        #             HessT[time].append([])
        #             for j in range(N_be) :
        #                 if i in [1,4] and j in [1,4] and i!=j:
        #                     grad_eval_T[time][i].extend([[0.0,0.0,0.0,0.0,0.0,0.0,0.0]])
        #                     trans2[time][i].extend([[0.0,0.0,0.0,0.0,0.0,0.0,0.0]])
        #                     HessT[time][i].extend([[0.0,0.0,0.0,0.0,0.0,0.0,0.0]])
        #                 elif i in [1,2] and j in [1,2] and i!=j:
        #                     grad_eval_T[time][i].extend([[0.0,0.0,0.0,0.0,0.0,0.0,0.0]])
        #                     trans2[time][i].extend([[0.0,0.0,0.0,0.0,0.0,0.0,0.0]])
        #                     HessT[time][i].extend([[0.0,0.0,0.0,0.0,0.0,0.0,0.0]])
        #                 else :
        #                     grad_eval_T[time][i].append(0.0)
        #                     trans2[time][i].append(0.0)
        #                     HessT[time][i].append(0.0)

    #    print(grad_eval_L, 'grad_eval_L')
    #    print(cond, eps, nb_iter, nb_max_iter)
    #    print((cond > eps and nb_iter < nb_max_iter))
        while (cond > eps and nb_iter < nb_max_iter):

            print(grad_eval_L)

            jacL, jacT, jac_mu = jacobianF(
                trans1, lamb1, mu1, nt_lam, OUT_TRANS, STAY, table, version, N_be, label, var)
            HessL, HessT, HessBin = HessF(
                trans1, lamb1, mu1, nt_lam, OUT_TRANS, STAY, table, version, N_be, label, var)

            for u in range(0, int(var.end_time / 5)):
                for h in range(0, N_be):
                    if HessL[u, h] != 0:
                        grad_eval_L[u][h] = jacL[u, h] / HessL[u, h]

            for u in range(0, int(var.end_time / 5)):
                for h in range(0, N_be):
                    for k in range(0, N_be):
                        # if type(grad_eval_T[u][h][k])==np.float64 or  type(grad_eval_T[u][h][k])==np.float:
                        if HessT[u][h][k] != 0:
                            grad_eval_T[u][h][k] = jacT[u][h][k] / \
                                HessT[u][h][k]
                        # else :
                        #     for m in range(0,N_be):
                        #         if HessT[u][h][k][m]!=0.0 :
                        #             grad_eval_T[u][h][k][m] = jacT[u][h][k][m]/HessT[u][h][k][m]

            for u in range(0, int(var.end_time / 5)):
                for h in range(0, N_be):
                    for k in range(0, 4):
                        for f in range(0, 10):
                            if HessBin[u, h, k, f] != 0:
                                grad_eval_Bin[u, h, k, f] = jac_mu[u,
                                                                   h, k, f] / HessBin[u, h, k, f]

                                # if(u==37 and h==1 and k==1 and f==0) :
                                #     print(grad_eval_Bin[u,h,k,f], jac_mu[u,h,k,f],HessBin[u,h,k,f],mu1[u,h,k,f],'evaluation')

            grad_eval_Bin = np.round(grad_eval_Bin, 5)

            #print(HessBin, 'Hess')
            # print(jac_mu,'jac')
        #    print(omega.shape, grad_eval_L.shape, lamb2.shape, lamb1.shape)
            lamb2 = lamb1 - omega * grad_eval_L
            lamb1 = abs(lamb2)
            # print(grad_eval_Bin[0,0,:,:])
            mu2 = mu1 - omega__ * grad_eval_Bin
            mu2 = np.round(mu1, 5)
            # print('mu',mu2)

            # for i in range(0,len(mu2)):
            #     for j in range(0,len(mu2[0])):
            #         for h in range(0,len(mu2[0][0])):
            #             for g in range(0,len(mu2[0][0][0])):
            #                 if (mu2[i][j][h][g])>1 or (mu2[i][j][h][g])<-1 :
            #                     print(mu2[i][j][h][g],i,j,h,g,'mu_fini')
            #                     print(HessBin[i,j,h,g])
            #                     print(jac_mu[i,j,h,g])

            mu1 = mu2

            #q1[q1 < 0] = 0.00001
            #q1[q1 > 1] = 1.0
            for u in range(0, int(var.end_time / 5)):
                for h in range(0, N_be):
                    for k in range(0, N_be):
                        # if type(grad_eval_T[u][h][k])==np.float64 or  type(grad_eval_T[u][h][k])==np.float:
                        trans2[u][h][k] = abs(
                            abs(trans1[u][h][k]) - 0.2 * grad_eval_T[u][h][k])

                        # if trans2[u][h][k]<0 :
                        #     trans2[u][h][k]=0.00001

                        # else :
                        #     for m in range(0,N_be):
                        #         trans2[u][h][k][m]=abs(abs(trans1[u][h][k][m]) - 0.2*grad_eval_T[u][h][k][m])

                        # if trans2[u][h][k][m]<0 :
                        #     trans2[u][h][k][m]=0.0001

            # print('trans',trans2[-7:-3])
          #  print('grad_eval',grad_eval_T[-7:-3])
            # for time in range(0,activation_time-2):
            #     for i_test in range(0,6):
            #         if sum(trans1[time][i_test,:])==0.0 :
            #             trans2[time][:,i_test]=np.zeros(6)
            #             trans2[time][i_test,:]=np.zeros(6)
            # if time > activation_time-3 :
            #     for i_test in range(0,6):
            #         ab=time
            #         while sum(trans1[ab][i_test,:])==0.0 :
            #             trans2[ab][i_test,:]=trans2[ab-1][i_test,:]
            #             trans2[ab][:,i_test]=np.zeros(6)
            #             ab=time-1

            # print(lamb1)
            trans1 = (trans2)
            z0 = Function(trans1, lamb1, mu1, nt_lam,
                          OUT_TRANS, STAY, table, version, N_be, label, var)
          #  print(z0,tmp_z0)

            nb_iter = nb_iter + 1
            # print(z0)
            cond = abs(tmp_z0 - z0)
            tmp_z0 = z0

           # print(cond)

            if nb_iter % 10 == 0:
                print(nb_iter)
        #    print(cond, eps, nb_iter, nb_max_iter)
        # print(nb_iter)

        self.LAMBDA = lamb1.round(3)
        self.TRANS = trans1
        self.mu = mu1.round(3)

        # print(trans1)
        # print(self.q)
