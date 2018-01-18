# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 12:05:41 2017

"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# =============================================================================
# Convex Sets visualization
# 
# For a set to be convex, for any x1 and x2 in the set the following condition must hold:
# 
#     f(alpha*x1+(1-alpha)*x2)<=alpha*f(x1)+(1-alpha)f(x2), where 0<=alpha<=1
# 
#  For the set between x1o and x2o to be convex, each line in the animation should be green
#  red lines signify that the inequality condition is not true
# 
# =============================================================================

# parameters to change

#x1o must be smaller than x2o 
x1o=-4;x2o=5;#two points which all convex combinations will be simulated between


res=50;#resolution of lines
alpha=np.linspace(1,0,res+1)
p=.2 #magnitude of border around function 
ccpr=3 #convex combination of points resolution (lower if it is running slow)
diff=np.abs(x2o-x1o)
t=50 # time (milliseconds) between each frame


# Function to visualize, try x^2, x^3, e^x , abs(x)

def func(X):
    #change function returned to try other functions
    return (-10*X+6*np.square(X)+.1*np.power(X,3)-.2*np.power((X-1),4))

#function1= f(alpha*x1+(1-alpha)*x2):
def leftSide(x1=x1o,x2=x2o,alpha=alpha):
    param=(alpha*x1)+(1-alpha)*x2
    return func(param)
#function2= alpha*f(x1)+(1-apha)f(x2):    
def rightSide(x1=x1o,x2=x2o,alpha=alpha):
    return alpha*func(x1)+(1-alpha)*func(x2)
    
def funcDomain(x1,x2):
    domain=np.linspace(int(x1-p*diff),int(x2+p*diff),int(res*(1+p)))
    return domain


fD=funcDomain(x1o,x2o)
steps=int(ccpr*diff)
Domain=[];linear=[]

x1=x1o;x2=x2o;

def createLines(x1,x2):
     
    ix1=x1;
    for j in range(steps):
        x1=ix1; 
        DomainGroup=np.zeros((steps-j,res+1))
        lineGroup=np.zeros((steps-j,res+1))
        
        for i in range(steps-j):

            DomainGroup[i]=np.linspace(x1,x2,res+1)
            lineGroup[i]=rightSide(x1=x1,x2=x2).copy()
            x1+=(1/steps)*diff

        Domain.append(DomainGroup.copy())
        linear.append(lineGroup.copy())
        x2-=(1/steps)*diff
    return Domain,linear
    
# creation of all linear lines
Domain,linear=createLines(x1,x2)

# animation
fig, ax = plt.subplots(figsize=(8,6))
plt.plot(fD,func(fD),c='cyan')
plt.scatter(x1o,func(x1o),color='black',s=30)
plt.scatter(x2o,func(x2o),color='black',s=30)
plt.title('Convex Visualisation')
ymin=np.min(func(fD));
ymax=np.max(func(fD));
ydiff=abs(ymax-ymin);
ax.set(xlim=((x1-p*diff), (x2+p*diff)), ylim=((ymin-p*ydiff),(ymax+p*ydiff)))


line = ax.plot(Domain[0][0], linear[0][0], color='r', lw=2)[0]
# conc and conc2 are the concatenated arrays of the data that represents each line
conc=np.array(Domain[0])
for indx in range(len(Domain)-1):
    conc=np.vstack((conc,Domain[indx+1]))
conc2=np.array(linear[0])
for indx1 in range(len(linear)-1):
    conc2=np.vstack((conc2,linear[indx1+1]))
    
#create array for the line color 
lineColor=np.any((func(conc)>conc2),axis=1)
lineColor=np.array(['red' if lc==True else 'green' for lc in lineColor])    

def animate(k):
    line.set_color(lineColor[k])
    line.set_xdata(conc[k])
    line.set_ydata(conc2[k])

anim = FuncAnimation(fig, animate, interval=t, frames=int(steps*(steps+1)/2))

plt.draw()
plt.show()

