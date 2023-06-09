import functions
import numpy
import math
# import benchmarks as Fit
import matplotlib.pyplot as plt
import sys
sys.path.append(r"D:\My_Code")


def alpha_new(alpha, NGen):
    # % alpha_n=alpha_0(1-delta)^NGen=10^(-4);
    # % alpha_0=0.9
    delta = 1-(10**(-4)/0.9)**(1/NGen)
    alpha = (1-delta)*alpha
    return alpha


def opt(dc, str_with_copies):
   # General parameters
   lb = 0
   ub = 1
   MaxGeneration = 250
   dim = len(dc)
   n = 50

   # FFA parameters
   alpha = 0.5  # Randomness 0--1 (highly random)
   betamin = 0.20  # minimum value of beta
   gamma = 1   # Absorption coefficient
   if not isinstance(lb, list):
      lb = [lb] * dim
   if not isinstance(ub, list):
      ub = [ub] * dim

   zn = numpy.ones(n)
   zn.fill(float("inf"))

   ns = numpy.zeros((n, dim)).astype(int)
   for i in range(dim):
      ns[:, i] = numpy.random.randint(2, size=n)
   Lightn = numpy.ones(n)
   Lightn.fill(float("inf"))

   convergence = []

   # Main loop
   for k in range(0, MaxGeneration):     # start iterations

      # % This line of reducing alpha is optional
      alpha = alpha_new(alpha, MaxGeneration)

      # % Evaluate new solutions (for all n fireflies)
      for i in range(0, n):
         ###############################
         temp_x = numpy.array(str_with_copies)
         # for j in range(len(dc)): # set dont care bits with values
         #   temp_x[dc[j]]=temp_position[j]
         # temp_x=[int(s) for s in temp_x]
         numpy.put(temp_x, dc, ns[i, :])
         ###############################
         zn[i] = functions.f(temp_x)
         Lightn[i] = zn[i]

      # Ranking fireflies by their light intensity/objectives

      Lightn = numpy.sort(zn)
      Index = numpy.argsort(zn)
      ns = ns[Index, :]

      # Find the current best
      nso = ns
      Lighto = Lightn
      nbest = ns[0, :]
      Lightbest = Lightn[0]
      # % For output only
      fbest = Lightbest

      # % Move all fireflies to the better locations
      scale = []
      for b in range(dim):
         scale.append(abs(ub[b] - lb[b]))
      scale = numpy.array(scale)
      for i in range(0, n):
         # The attractiveness parameter beta=exp(-gamma*r)
         for j in range(0, n):
               r = numpy.sqrt(numpy.sum((ns[i, :]-ns[j, :])**2))
               # Update moves
               if Lightn[i] > Lighto[j]:  # Brighter and more attractive
                  beta0 = 1
                  beta = (beta0-betamin)*math.exp(-gamma*r**2)+betamin
                  tmpf = alpha*(numpy.random.rand(dim)-0.5)*scale
                  tmp_ns = ns[i, :].astype(float)
                  tmp_ns = tmp_ns*(1-beta)+nso[j, :]*beta+tmpf
                  sigV = 1/(1+(numpy.exp((-tmp_ns))))
                  ns[i, :] = (sigV > numpy.random.rand(
                     ns[i, :].size)).astype(int)

      convergence.append(fbest)

      IterationNumber = k
      BestQuality = fbest

   #    print(['At iteration ' + str(k) + ' the best fitness is ' + str(BestQuality)])

   # # Data for plotting
   # plt.plot(convergence)
   # plt.xlabel('Iteration')
   # plt.ylabel('Cost')
   # plt.title('Cost Function in Itterations')

   # function to show the plot
   # plt.show()
   ###############################
   temp=numpy.array(str_with_copies)
   numpy.put(temp,dc,nbest)
   temp_lst=temp.tolist()
   ###############################
   x_star="".join(temp_lst)
   return [BestQuality,x_star]
   print(convergence[-1])
   print(nbest)
   print(functions.f([int(x) for x in nbest]))
