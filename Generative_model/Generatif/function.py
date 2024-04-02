
import numpy 
import random

def exp(x,tauinv) :
    return 1/tauinv*numpy.exp(-x/tauinv)

def where(A,value):
    idx = (np.abs(A-value)).argmin()
    if A[idx]<value :
        idx=idx+1
    return idx 

def aleatoire(x) :
    #print(x,sum(x))
    liste=[]
    s=sum(x)
    if s==0:
        inde=0
    else: 
        x=x/s
        [liste.append(sum(x[:i+1])) for i in range(0,len(x))]
        nb=random.random()
        nbt=0
        while nb>sum(x) :
            nbt+=1
            nb=random.random()
            if nbt>7 :
                print('error',x)
        liste.append(nb)
        inde=list(sorted(liste)).index(nb)
    return inde 

# def probadata(TAB,nb_groupe,N_be):
#     VARI=numpy.zeros(((end_time)*2+1,N_be))
#     PROBA=numpy.zeros(((end_time)*2+1,N_be))
#     NB=numpy.zeros(((end_time)*2+1))

#     for i in range(0,len(TAB)):
#         if int(TAB[i,0]*2)<91 :
#             PROBA[int(TAB[i,0]*2),int(TAB[i,1])]+=1
#             NB[int(TAB[i,0]*2)]+=1

#     for i in range(0,N_be) :
#         PROBA[:,i]=PROBA[:,i]/NB

#     numpy.nan_to_num(PROBA)
#     PROBAG=numpy.zeros((nb_groupe,(end_time)*2+1,N_be))
#     NBG=numpy.zeros((nb_groupe,(end_time)*2+1))
#     C=numpy.zeros(50)
#     GROUPE_TAB=numpy.zeros((2,len(TAB[1,:])))


#     for j in range(0,nb_groupe):
#         GROUPE_TAB=numpy.zeros((2,len(TAB[1,:])))
#         for i in range(0,50):
#             C[i]=random.choice(list(set(list(TAB[:,3]))))
#             GROUPE_TAB=numpy.concatenate(((TAB[(TAB[:,3]==C[i])]),GROUPE_TAB))
#         #print(len(GROUPE_TAB),len(TAB))
#         for i in range(0,len(GROUPE_TAB)):
#             if int(GROUPE_TAB[i,0]*2)<91 :
#                 PROBAG[j,int(GROUPE_TAB[i,0]*2),int(GROUPE_TAB[i,1])]+=1
#                 NBG[j,int(GROUPE_TAB[i,0]*2)]+=1

#         for i in range(0,N_be) :
#             PROBAG[j,:,i]=PROBAG[j,:,i]/NBG[j,:]
#     for i in range(0,N_be):
#         for time in range(0,len(PROBAG[0,:,i])):
#             for j in range(0,nb_groupe):
#                 VARI[time,i]+=(PROBAG[j,time,i]-PROBA[time,i])**2/nb_groupe

#             VARI[time,i]=numpy.sqrt(VARI[time,i])

#     #print(VARI)

#     return VARI, PROBA



def KL(P,Q):
# Epsilon is used here to avoid conditional code for
#checking that neither P nor Q is equal to 0. 
    epsilon = 0.00001
    divergence=numpy.zeros(len(P))

    # You may want to instead make copies to avoid changing the np arrays.
    P = P+epsilon
    Q = Q+epsilon
    for x in range(len(divergence)):
        divergence[x] = P[x]*numpy.log(P[x]/Q[x])
    return divergence
