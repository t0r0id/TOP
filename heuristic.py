import numpy as np
from variables_class import Solution
from read_data import read, find_segments
from constraints import status

data=read("data.xlsx")
t=find_segments(data[:,:2])
p=data[:,2]
d=data[:,3]
e=data[:,4]
l=data[:,5]
T=data[:,6]
n=data.shape[0]-2
m=2
M=10000
Tmax=230
Q=50

def insert_element(R,element,position):
    new_R=[]
    R_temp=np.delete(R,position[0],0)
    temp = np.insert(R[position[0]],position[1],element)
    for i in range(R.shape[0]):
        j=0
        if i==position[0]:
           new_R.append(temp)
        else:
            new_R.append(R_temp[j])
            j=j+1
    return np.array(new_R)

def cost1(sol,temp,para,i,j,v):
    N1=para[0]*(t[sol.R[i][j-1],v]+t[v,sol.R[i][j]]-t[sol.R[i][j-1],sol.R[i][j]] + para[2]*T[v])
    #print temp.pi[temp.R[i][j+1],i]
    N2=para[1]*(temp.pi[temp.R[i][j+1],i]-temp.pi[sol.R[i][j],i])
    D=p[v]**para[3]
    return (N1+N2)/D

def heu1(sol,rmvd=[]):
    sol_temp=sol
    not_visited=sol_temp.not_visited
    not_visited=np.union1d(not_visited,[item for sublist in rmvd for item in sublist])
    for i in range (sol_temp.R.shape[0]):
        to_be_visited=np.setdiff1d(not_visited,rmvd[i])
        j=1
        while j<len(sol_temp.R[i]):
            flag=0
            update=0
            min_cost=999
            for v in (to_be_visited):
                R_temp=insert_element(sol_temp.R,v,[i,j])
                temp=Solution(R_temp)
                cost=cost1(sol_temp,temp,[0.9,0.1,0.9,2],i,j,v)
                if (cost<min_cost and status(temp,t,p,m,n,d,l,T,M,Q,Tmax)[0]):
                    min_cost=cost
                    flag=1
                    update=temp
            if flag==1:
                j=0
                sol_temp=update
            j=j+1
    
    for i in range (sol_temp.R.shape[0]):
        while j<len(sol_temp.R[i]):
            flag=0
            update=0
            min_cost=999
            for v in (rmvd[i]):
                R_temp=insert_element(sol_temp.R,v,[i,j])
                temp=Solution(R_temp)
                cost=cost1(sol_temp,temp,[0.9,0.1,0.9,2],i,j,v)
                if (cost<min_cost and status(temp,t,p,m,n,d,l,T,M,Q,Tmax)[0]):
                    min_cost=cost
                    flag=1
                    update=temp
            if flag==1:
                j=0
                sol_temp=update
            j=j+1

                
    return sol_temp
                
                    
                    
                
                
            
            
            
