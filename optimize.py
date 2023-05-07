# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 09:56:55 2020

@author: Ipchi
"""
import time
import multiprocessing as mp
import random
import math
import matplotlib.pyplot as plt
from functions import f
LEDGER=[]
LENGTH=310;DIM=10 #Length should be multiplier of Dimension
GEN=1000 #an upper bound for execution,typically dont reach this
def hamming_distance(chaine1, chaine2):
    return sum(c1 != c2 for c1, c2 in zip(chaine1, chaine2))
def rand_key(p=LENGTH): #generate random binary string
    key1 = ""
    for i in range(p): 
        temp = str(random.randint(0, 1))
        key1 += temp 
    return(key1) 

def tobinary(n):
    return bin(n)
    
def todecimal(n,rng):
   x=int(n,2)
   s=n.replace('0','1') #for example convert 10010 to 11111
   upper=int(s,2)
   ratio=(rng[1]-rng[0])/upper
   
   return x*ratio+rng[0]

def find_dont_care(current_dc,bits_to_find): #setup sub-search-space
    dc=[]
    u=range(LENGTH)
    s=(list(list(set(u)-set(current_dc)) + list(set(current_dc)-set(u))))
    dc=random.sample(s, bits_to_find)
    return dc
def find_similar_pattern(pattern,ledger,method,search_bit,step): #find most simalar pattern from data store to select valuable bits
    #ledger is our shared memory that store partial good candidates
    # return [fitness,x*,dont care indexes]
    if method=="pareto":
        pair=[]    
        for x in range(len(ledger)):
            fit=ledger[x][0]
            dist=hamming_distance(pattern,ledger[x][1])
            pair.append([fit,dist])
            

        sorted_pair=sorted(pair)
        pareto_front = [sorted_pair[0]]
        for pair in sorted_pair[1:]:
            if pair[1] <= pareto_front[-1][1]:
                pareto_front.append(pair)
        output=random.choice(pareto_front)
        result=[item for item in ledger if item[0] == output[0] ]
        return result[0]
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # temp=LENGTH   
    # result=[]
    # search_scope=len(ledger[-1][2])
    # for cntr in reversed(range(len(ledger))):
    #     if len(ledger[cntr][2])!=search_scope:
    #         break
    #     if temp>hamming_distance(pattern,ledger[cntr][1]):
    #         temp=hamming_distance(pattern,ledger[cntr][1])
    #         result=ledger[cntr]
    # return result
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    elif method=="normal":
        temp=LENGTH   
        result=[]
        for cntr in range(len(ledger)):
            # if len(ledger[cntr][2])==search_bit-step:
            if temp>hamming_distance(pattern,ledger[cntr][1]):
                temp=hamming_distance(pattern,ledger[cntr][1])
                result=ledger[cntr]
        return result
def set_dont_care_with_pattern(i,search_bit,other,rnd,dc,curr_dc,similar_pattern): #copy valuable bits from similar pattern
    pattern=tobinary(i)[2:]
    pattern=pattern.zfill(search_bit)
    r2=list(rnd)    
    for j in range(search_bit): # set dont care bits with values
        r2[dc[j]]=pattern[j]
    
    for j in range(other): # set dont care bits with values
        r2[curr_dc[j]]=similar_pattern[curr_dc[j]]
    tempstr=''.join(r2) # r2 is x for f(x)  
    return tempstr

def plot(ledger,Type,lineformat,mylabel):
    temp=[t[0] for t in ledger]
    if Type=='total':        
        plt.plot(list(range(len(ledger))),temp)
        plt.xlabel('epoch')
        plt.ylabel('fitness')   
        plt.title('Fitness of function x')   
        return plt
    elif Type=='desc':
        temp2=[]
        for counter in range(1,len(temp)):
            temp2.append(min(temp[:counter]))
        last_min_idx=temp.index(min(temp2))
        plt.plot(list(range(len(ledger)-1)),temp2,linestyle=lineformat,label=mylabel)
        plt.xlabel('epoch')
        plt.ylabel('fitness')   
        plt.title('Best Fitness until now')
        plt.legend(loc="upper right")
        return plt
        print(last_min_idx,temp[last_min_idx])
# print(todecimal('0100011011',[-5,5]))
# print(f([3]*10))
def brute_force(dc,search_bit_init,search_bit,rnd,min_f,current_dc=None,similar_pattern=None,ans=None): #We can use brute force instead of inner swarm mechanism, but we dont use this in the paper
    current_f=10000000
    if search_bit==search_bit_init:
        for i in range(2**search_bit): #search whole the dont care space with brute force
            pattern=tobinary(i)[2:]
            pattern=pattern.zfill(search_bit)
            r2=list(rnd)                    
            for j in range(search_bit): # set dont care bits with values
                r2[dc[j]]=pattern[j]
                tempstr=''.join(r2) # r2 is x for f(x)
                current_f=f(tempstr)
                if current_f<min_f[-1][0]:
                    min_f.append([current_f,tempstr,dc])
                    # fitness[c][i]=[current_f,tempstr,dc]
    else:
        min_f=[[10000000000,'',[]]] #[fitness,x*,dont care]
        dc=find_dont_care(ans[2][0:search_bit-search_bit_init],search_bit_init)
        for i in range(2**len(dc)): #search whole the dont care space with brute force
            t=set_dont_care_with_pattern(i,search_bit_init,search_bit-search_bit_init,rnd,dc,current_dc,similar_pattern)
            current_f=f(t)
            if current_f<min_f[-1][0]:
                join_dc=dc+ans[2][0:search_bit-search_bit_init]
                min_f.append([current_f,t,join_dc])
                # fitness[c][i]=[current_f,tempstr,dc]
    return min_f[-1]
def meta_search(dc,swarm,rnd,similar_str="",copied_value=[]): #This method launches inner swarm code in proposed swarm*
    
    ########################## Copy current dont care from copied_value to random string
    r2=list(rnd)
    for j in range(len(copied_value)): # set dont care bits with values
        r2[copied_value[j]]=similar_str[copied_value[j]]
    ###########################
    t=swarm.opt(dc,r2)
    t.append(dc+copied_value)
    return t 
def optimize(mystep=2): # Main function
    search_bit_init=30
    search_bit=search_bit_init
    step=mystep  #increment search bit in each generation with this step
    no_of_each_length=2
    # fitness=[[0 for i1 in range(2**search_bit)] for j1 in range(miner_count)]#initialize fitness
    fitness=[]
    min_f=[[10000000000,'',[]]] #[fitness,x*,dont care]
    dc=[]
    ########################################## Select which inner swarm should be run in swarm* #########################################
    # import firefly.FFA as imprt
    # import Cuckoo_search.CS as imprt
    # import gray_wolf.GWO as imprt
    # import pso.pso as imprt
    # import _wale.WOA as imprt
    import _HHO.HHO as imprt
    ######################################################################################################################################
    for iteration in range(1,GEN):
        dc=random.sample(range(LENGTH), search_bit)
        rnd=rand_key()  #random string for processes to search within
        if iteration%no_of_each_length==0:
            search_bit+=step            
            if search_bit>LENGTH:break
        
        if search_bit==search_bit_init:
            # local_best=brute_force(dc,search_bit_init,search_bit,rnd,min_f)
            local_best=  meta_search(dc,imprt,rnd) 
            LEDGER.append(local_best)
            fitness.append(local_best[0])           
            
        else:
            rnd=rand_key() 
            ans=find_similar_pattern(rnd,LEDGER,'pareto',search_bit,step)  
            dc=find_dont_care(ans[2][0:search_bit-search_bit_init],search_bit_init) #setup sub-search-space
            # local_best=brute_force(dc,search_bit_init,search_bit,rnd,min_f,ans[2],ans[1],ans)
            start_time=time.time()
            local_best=meta_search(dc,imprt,rnd,ans[1],ans[2][0:search_bit-search_bit_init]) 
            end_time=time.time()  
            fitness.append(local_best[0])
            LEDGER.append(local_best)
            print(f"iteration {iteration:03d}  search bits {search_bit:-4d} / of {LENGTH} and finds {local_best[0]:.2f}  takes {end_time-start_time}s")
    return fitness
####################################@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#################################################
####################################@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#################################################
if __name__ == "__main__": # manage multiprocess mechanism in our code
    
    pool = mp.Pool(mp.cpu_count())
    miner_no=mp.cpu_count() #in paper we have 12 core
    step=20 #in paper we named this stride (you can change this to other values i.e. 5)
    s=time.time()
    param=[step]*miner_no
    results = pool.map(optimize,param)
    
    e=time.time()
    pool.close()
    print(f"takes {e-s} seconds")
    res=[results[0][0]]
    for row in results:
        for element in row:
            if element<res[-1]:
                res.append(element) # X-axis called epoch in document
    print(res)
    # r=optimize(20)
    # print(r)


#R=optimize(2,20)
# print(R)
# index=0
# for stp in range(1,5):
#     format=['solid',':','dashdot','dashed']
#     ans=optimize(6,stp)
#     plt=plot(ans, 'desc',format[index],str(stp))
#     index+=1
# plt.savefig('/home/mrish/Documents/steps.pdf',dpi=1200)
# plt.show()

