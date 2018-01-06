import numpy as np
import copy
def draw():
    card = np.random.random_integers(1,10)
    return card

def step(a,state): # s[1] - value | s[2] - terminal or not
    s = copy.deepcopy(state)
    r = 0
    if(a == 0): #stick
        s[2] = 1 #terminal
        #dealer's turn
        v = s[0]
        if(v < 17):
            v = v + draw()

        if(v > 21):
            s[2] = -1
            r = 1
        else:
            if(s[1] > v):
                r = 1
            if(s[1] == v):
                r = 0
            if(s[1] < v):
                r = -1
        return s,r
    if(a == 1): #hit
        s[1] = s[1] + draw()

        if(s[1] > 21):
            s[2] = 1 #terminal
            r = -1
            return s,r
        else:
            return s,r

def fisrt_vist_mc():
    #First-Visit Monte-Carlo Policy
    Ns = np.zeros([10,21]) + 0.0000001
    Ss = np.zeros([10,21])
    s = np.zeros(3)
    #start

    #double for lop for all states
    for x in range(1000):
        #start
        card_dealer = draw()-1
        card_player = draw()-1
        s[0] = card_dealer+1 # dealer
        s[1] = card_player+1 # player

        #mc
        s[2] = 0
        episo = []
        while(s[2] < 1):
            a = np.random.random_integers(0,1) #policy
            episo.append(s) #in python, if 's' changes, 'episo' will also change
            #print('before:',episo)
            s2,r = step(a,s)
            #print('after:',episo)
            for x in episo:
                Ss[int(x[0]-1),int(x[1]-1)] = Ss[int(x[0]-1),int(x[1]-1)] + r
            Ns[int(s[0]-1),int(s[1]-1)] = Ns[int(s[0]-1),int(s[1]-1)] + 1
            s = s2

    Vs = Ss/Ns
    return Vs

def fisrt_vist_mc_control():
    #First-Visit Monte-Carlo Policy
    Ns = np.zeros([10,21]) + 0.0000001
    Ss = np.zeros([10,21])
    s = np.zeros(3)
    #start

    #double for lop for all states
    for x in range(100000):
        e = 1.0/(x+1.0)**0.5
        #start
        card_dealer = draw()-1
        card_player = draw()-1
        s[0] = card_dealer+1 # dealer
        s[1] = card_player+1 # player

        #mc
        s[2] = 0
        episo = []
        while(s[2] < 1):

            exp = np.random.random() # exploration rate!!!
            #print(exp)
            if exp > e:
                a = argmax_q(s,Ss/Ns) #policy
            else:
                a = np.random.random_integers(0,1) #policy
            episo.append(s) #in python, if 's' changes, 'episo' will also change
            #print('before:',episo)
            s2,r = step(a,s)
            #print('after:',episo)
            for x in episo:
                Ss[int(x[0]-1),int(x[1]-1)] = Ss[int(x[0]-1),int(x[1]-1)] + r
            Ns[int(s[0]-1),int(s[1]-1)] = Ns[int(s[0]-1),int(s[1]-1)] + 1
            s = s2

    Vs = Ss/Ns
    return Vs

def argmax_q(s,v):
#    print(s[0],s[1])

    a = v[int(s[0]) - 1,int(s[1]) - 1]
    q = 0
    for i in range(10):
        if s[1] + i <= 21:
            q = v[int(s[0]) - 1,int(s[1]) + i - 1] + q
        else:
            q = -1 + q

    q = q/10.0
    if a > q:
        return 0 # stick
    else:
        return 1 # hit

v = fisrt_vist_mc_control()
# print(mc_control(s,v))
np.savetxt('angle.txt',v,fmt='%f',delimiter=',',newline='\r\n')
print(v)

#The dealer always sticks on any sum of 17 or greater, and hits otherwise
