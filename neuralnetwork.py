from math import *
from random import *
import numpy as np
import matplotlib.pyplot as plt

import matplotlib.animation as animation

alpha=0.05

class Neurone():
    def __init__(self,n):
        self.weights=[2*random()-1 for i in range(n)]
        self.threshold=0
    def output(self,input):
        s=0
        for i in range(len(input)):
            s+=input[i]*self.weights[i]
        return(1/(1+exp(self.threshold-10*s)))
    def get_mutation(self):
        mutation=Neurone(len(self.weights))
        mutation.weights=[]
        for w in self.weights:
            mutation.weights.append(w+alpha*(2*random()-1)) 
        mutation.threshold=self.threshold+alpha*(2*random()-1)
        return(mutation)
        
class Layer():
    def __init__(self,n_i,n_o):
        self.neurones=[Neurone(n_i) for i in range(n_o)]
        self.n_i=n_i
        self.n_o=n_o
    def output(self,input):
        return([n.output(input) for n in self.neurones])
    def get_mutation(self):
        mutation=Layer(self.n_i,self.n_o)
        mutation.neurones=[]
        for i in self.neurones:
            mutation.neurones.append(i.get_mutation())
        return(mutation)
    
class Network():
    def __init__(self,n):
        self.layers=[]
        for i in range(len(n)-1):
            self.layers.append(Layer(n[i],n[i+1]))
            self.sizes=n
    def output(self,input):
        for i in range(len(self.layers)):
            input=self.layers[i].output(input)
        res=input
        return(res.index(max(res))-1)
    def get_mutation(self):
        mutation=Network(self.sizes)
        mutation.layers=[]
        for i in self.layers:
            mutation.layers.append(i.get_mutation())
        return(mutation)
        

bar_size=0.1
bar_speed=0.6
ball_speed=0.56

dt=0.1

data_to_show=[]

def match(brain_1,brain_2,show=0):
    x_ball=0.5
    y_ball=0.5
    angle=random()*2*pi
    vx_ball=ball_speed*cos(angle)
    vy_ball=ball_speed*sin(angle)
    while abs(vx_ball)<0.4 or abs(vx_ball)>0.5:
        angle=random()*2*pi
        vx_ball=ball_speed*cos(angle)
        vy_ball=ball_speed*sin(angle)
    if vx_ball>0:
        next_contact_1=0.5
        next_contact_2=0.5+(1/2)*vy_ball/vx_ball
        if next_contact_2>1:
            c=0
            while next_contact_2>1:
                c+=1
                next_contact_2-=1
            if (c%2):
                next_contact_2=1-next_contact_2
        elif next_contact_2<0:
            c=0
            while next_contact_2<0:
                c+=1
                next_contact_2+=1
            if (c%2):
                next_contact_2=1-next_contact_2
    elif vx_ball<0:
        next_contact_2=0.5
        next_contact_1=0.5-(1/2)*vy_ball/vx_ball
        if next_contact_1>1:
            c=0
            while next_contact_1>1:
                c+=1
                next_contact_1-=1
            if (c%2):
                next_contact_1=1-next_contact_1
        elif next_contact_1<0:
            c=0
            while next_contact_1<0:
                c+=1
                next_contact_1+=1
            if (c%2):
                next_contact_1=1-next_contact_1
    y_1=0.5
    y_2=0.5
    over=False
    winner=0
    n_bounce_1=0
    n_bounce_2=0
    t=0
    nc1=[next_contact_1]
    nc2=[next_contact_2]
    yb=[0.5]
    xb=[0.5]
    yb1=[0.5]
    yb2=[0.5]
    integ1=0.1
    integ2=0.1
    while not over and t<30:
        t+=dt
        
        y_1+=brain_1.output([x_ball,y_ball,vx_ball,vy_ball,y_1])*bar_speed*dt
        if y_1>1-bar_size/2:
            y_1=1-bar_size/2
        elif y_1<bar_size/2:
            y_1=bar_size/2
        
        y_2+=brain_2.output([1-x_ball,y_ball,-vx_ball,vy_ball,y_2])*bar_speed*dt
        if y_2>1-bar_size/2:
            y_2=1-bar_size/2
        elif y_2<bar_size/2:
            y_2=bar_size/2
        x_ball+=vx_ball*dt
        y_ball+=vy_ball*dt
        if y_ball>1:
            vy_ball=-vy_ball
            y_ball=2-y_ball
        elif y_ball<0:
            vy_ball=-vy_ball
            y_ball=-y_ball
        if x_ball<0:
            if y_ball>(y_1-bar_size/2) and y_ball<(y_1+bar_size/2):
                vx_ball=-vx_ball
                x_ball=-x_ball
                n_bounce_1+=1
                next_contact_1=0.5
                next_contact_2=y_ball+(1-x_ball)*vy_ball/vx_ball
                if next_contact_2>1:
                    c=0
                    while next_contact_2>1:
                        c+=1
                        next_contact_2-=1
                    if (c%2):
                        next_contact_2=1-next_contact_2
                elif next_contact_2<0:
                    c=0
                    while next_contact_2<0:
                        c+=1
                        next_contact_2+=1
                    if (c%2):
                        next_contact_2=1-next_contact_2
            else:
                winner=2
                over=1
        elif x_ball>1:
            if y_ball>(y_2-bar_size/2) and y_ball<(y_2+bar_size/2):
                vx_ball=-vx_ball
                x_ball=2-x_ball
                n_bounce_2+=1
                next_contact_2=0.5
                next_contact_1=y_ball-x_ball*vy_ball/vx_ball
                if next_contact_1>1:
                    c=0
                    while next_contact_1>1:
                        c+=1
                        next_contact_1-=1
                    if (c%2):
                        next_contact_1=1-next_contact_1
                elif next_contact_1<0:
                    c=0
                    while next_contact_1<0:
                        c+=1
                        next_contact_1+=1
                    if (c%2):
                        next_contact_1=1-next_contact_1
            else:
                winner=1
                over=1
        integ1+=abs(y_1-next_contact_1)
        integ2+=abs(y_2-next_contact_2)
        yb.append(y_ball)
        xb.append(x_ball)
        yb1.append(y_1)
        yb2.append(y_2)
        nc1.append(next_contact_1)
        nc2.append(next_contact_2)
    n=len(yb)
    fit1=n/integ1
    fit2=n/integ2
    if show:
        for i in range(n):
            data_to_show.append([[0,0,0,xb[i],1,1,1],[yb1[i]-bar_size/2,yb1[i]+bar_size/2,yb1[i],yb[i],yb2[i],yb2[i]-bar_size/2,yb2[i]+bar_size/2]])
    return([winner,fit1,fit2])
        
    
#pop=[Network([5,3]) for i in range(20)]


def enhance(pop,show=0):
    results=[0 for i in range(len(pop))]
    bounces=[0 for i in range(len(pop))]
    nmatch=0
    for i in range(len(pop)):
        nmatch=0
        for j in range(len(pop)):
            if j!=i:
                res,n_bounce_i,n_bounce_j=match(pop[i],pop[j])
                nmatch+=1
                if res==1:
                    results[i]+=1
                else:
                    results[j]+=1
                bounces[i]+=n_bounce_i
                bounces[j]+=n_bounce_j
    winner=results.index(max(results))
    for i in range(len(pop)):
        if i!=winner:
            if random()>0.1:
                pop[i]=pop[winner].get_mutation()
            else:
                pop[i]=Network([5,3])
    if show:
        print(winner)
    match(pop[winner],pop[winner],show)
    return(pop[winner])



def createandtrain(pop,n):
    #pop=[Network([5,3]) for i in range(20)]
    for i in range(n):
        winner=enhance(pop)
        print(i)
    return(winner)
    
# brain=enhance(pop,1)


# fig, ax = plt.subplots()
# plt.axis([-0.1,1.1,-0.1,1.1])
# x=[0,1,1,0,0]
# y=[1,1,0,0,1]

# line, = ax.plot(x, y,color="black")


# def animate(i):
#     line.set_data(data_to_show[i][0],data_to_show[i][1])  # update the data
#     return line,

# def init():
#     line.set_data(np.ma.array(x, mask=True),np.ma.array(x, mask=True))
#     return line,

# ani = animation.FuncAnimation(fig, animate, np.arange(0,len(data_to_show)), init_func=init,
#                               interval=150, blit=True)
# plt.show()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

