''' This file should be located in D:\my_code
and also will be used by all other files'''
import math
def todecimal(x,rng):
   n=int(x,2)
   s=x.replace('0','1') #for example convert 10010 to 11111
   upper=int(s,2)
   ratio=(rng[1]-rng[0])/upper
   
   return n*ratio+rng[0]
######################################################### MAIN FUNCTION ####################################################################################
#############################################################################################################################################################
def f(x,name='Rosenbrock',dim=10): # change "name" default arg to othere name if you want test other benchmark functions i.e. name='Sphere' or name='Rastrigin'.
#x is binary string; dim is dimension of benchmark function
    if name=='Sphere':
        chunk_len=len(x)//dim
        new_x=[]
        for c in range(0, len(x), chunk_len):

            temp=todecimal(''.join(map(str, x[c:chunk_len+c])),rng=[-100,100])
            new_x.append(temp)
        
        res=0
        for cntr in range(len(new_x)):
            res+=(new_x[cntr]**2)
        return res
    elif name=='Rosenbrock':
        chunk_len=len(x)//dim
        new_x=[todecimal(str(''.join(map(str, x[i:chunk_len+i]))),rng=[-32,32]) for i in range(0, len(x), chunk_len)]
        res=0
        for cntr in range(len(new_x)-1):
            res+=(100*(new_x[cntr]**2-new_x[cntr+1])**2+(1-new_x[cntr])**2)
        return res
    elif name=='Rastrigin':
        chunk_len=len(x)//dim
        new_x=[todecimal(''.join(map(str, x[i:chunk_len+i])),rng=[-5.12,5.12]) for i in range(0, len(x), chunk_len)]
        res=0
        for cntr in range(len(new_x)):
            res+=(new_x[cntr]**2-10*math.cos(2*math.pi*new_x[cntr])+10)
        return res
    elif name=='Schwefel':
        chunk_len=len(x)//dim
        new_x=[todecimal(''.join(map(str, x[i:chunk_len+i])),rng=[-500,500]) for i in range(0, len(x), chunk_len)]
        res=0
        for cntr in range(len(new_x)):
            res+=(-new_x[cntr]*math.sin(math.sqrt(abs(new_x[cntr]))))
        return res + 4189.82
    elif name=='Griewank':
        chunk_len=len(x)//dim
        new_x=[todecimal(''.join(map(str, x[i:chunk_len+i])),rng=[-100,100]) for i in range(0, len(x), chunk_len)]
        res=0;part1=0;part2=0
        for cntr in range(1,len(new_x)):
            part1 =part1* math.cos(new_x[cntr]/math.sqrt(cntr))
            part2 =part2 + new_x[cntr]**2/4000
        return part1+part2+1
    elif name=='Zakharov':
        chunk_len=len(x)//dim
        new_x=[todecimal(''.join(map(str, x[i:chunk_len+i])),rng=[-5,10]) for i in range(0, len(x), chunk_len)]
        res=0;part_1=0;part_2=0
        for cntr in range(1,len(new_x)):
            part_1 += new_x[cntr]**2
            part_2 += new_x[cntr]*cntr
        return part_1+(.5*part_2)**2 + (.5*part_2)**4