import random
from itertools import combinations
class Function:
  #function class is like each member
  #think of this as a Parent / child
  def __init__(self,max):
    """
    digits: list -> binary values
    """
    self.length = max
    self.digits = [0]*self.length
    self.difference = 0
    self.calc = 0
  def form_number(self,number):
    """
    Logic is 
    take a number in binary format -> [0,0,1,1,1]
    now if self.digits[i] == 1  then reserve numbers[i] else keep it same
    return the resulting list of booleans

    Example
    if self.digits = [1,1,0,0,0]
    numbers = [0,0,1,1,1]
    result will be [1,1,1,1,1]
    """
    temp = []
    for i in range(self.length):
      if self.digits[i] == 0:
        temp.append(number[i])
      else:
        temp.append( 0 if number[i] == 1 else 1)
    return temp
  def randomize(self):
    # To randomize each Parent/Child bits
    for i in range(self.length):
      self.digits[i] = random.randint(0,1)
    random.shuffle(self.digits)
  def crossover(self,second):
    #logic is to take half gene from first parent and half from another
    #second is another function
    a = self.digits[:]
    b = second.digits[:]
    m = self.length//2
    t = []
    for i in range(0,m+1):
      t.append(a[i])
    for i in range(m+1,self.length):
      t.append(b[i])
    temp = Function(self.length)
    temp.digits = t
    return temp
  def mutate(self):
    #to randomly switch 2 or 3 bits 
    t = random.randint(2,3)
    for i in range(t):
      l = random.randint(0,self.length-1)
      self.digits[l] = 0 if self.digits[l] == 1 else 1





def get_number(binaries):
  #convert binary to decimal
  summer = 0
  temp = binaries[::-1]
  for i in range(len(binaries)):
    summer+= pow(2,i) * temp[i]
  return summer

def get_difference(bin1,bin2):
  a = get_number(bin1)
  b = get_number(bin2)
  return a-b

def form_binary(number,max):
  #number to binary with max number of padded zeros on left
  elem = bin(number)[2:]
  left = max - len(elem)
  return list(map(int,list("0"*left+elem)))

# print(form_binary(7,7))

# f1 = Function()
# b1 = form_binary(9)
# f1f1 = f1.form_number(b1)
# print(get_number(f1f1))
# inval = 7
# invalbin = form_binary(inval) #input binary daa
# output =  24
# outputbin = form_binary(output) #output binary data
# print(outputbin,invalbin)
# initials = []
# population  = 10
# for i in range(population):
#   f1 = Function()
#   f1.randomize()
#   initials.append(f1)
# for i in range(population):
#   a = initials[i]
#   b = a.form_number(invalbin)
#   diff = get_difference(outputbin,b)
#   f1.difference = diff

# initials.sort(key =lambda a:a.difference)
# print(initials)
# for each in initials:
#   print(each.digits,get_number(each.digits))
# permits = combinations(initials,2)
# temp = []
# for each in permits:
#   t = each[0].crossover(each[1])
#   # t.mutate()
#   temp.append(t)
# fin = 0
# for each in temp:
#   print(each.digits)
#   l = each.form_number(invalbin)
#   if get_number(l) == 24:
#     print("matched")
#     fin = each
#     break

# a = int(input())
# l = fin.form_number(form_binary(a))
# print(get_number(l))

import math

class Genetic:
  def __init__(self,val,ins,outs,tops=5,max=7):
    """
    val is amount of initial parents
    ins is input number
    outs is output number 
    tops is number of childrens to choose after crossover
    max is maximum length of number when converted in binary format
    """
    
    self.max = val
    self.ins = ins
    self.outs = outs
    self.ins_bin = form_binary(ins,max)
    self.outs_bin = form_binary(outs,max)
    self.tops = tops
    self.functions = []
    self.temporary = []
    self.generation = 1
    #creating val number of randomized Parents - First generation
    for i in range(val):
      temp = Function(max)
      temp.randomize()
      self.functions.append(temp)
  def crossover_current(self):

    #Making all possible combinations of current generation and crossing them over
    t = combinations(self.functions,2)
    results = []
    for each in t:
      temp = each[0].crossover(each[1])
      temp.mutate()
      results.append(temp)
    self.temporary = results
  def filter(self):
    #filtering the temporary array which contains all the crossovers of current generation
    # self.temporary.extend(self.functions)
    for each in self.temporary:
      temp = each.form_number(self.ins_bin)
      each.difference = math.sqrt(abs(self.outs - get_number(temp)))
    self.temporary.sort(key = lambda a:a.difference)
    self.functions = self.temporary[:self.tops]
  def validate_generation(self):
    #validates if any element of the generation is able to find the function() we are looking for
    for each in self.functions:
      a = each.form_number(self.ins_bin)
      if get_number(a) == self.outs:
        return True,each
    return False,False
  def current_generation(self):
    #this is just for user understanding of what's going on in current generation
    best = self.outs
    b = -1
    f = 0
    for each in self.functions:
      a = each.form_number(self.ins_bin)
      if self.outs - get_number(a) <best:
          best = self.outs - get_number(a)
          f = each
          b = get_number(a)
    self.gap = best
    self.promising = f
    print("Generation best gap :",best," Closest value:",b,"Function :",f.digits)
MAX = 20 #Maximum bits when number is converted from decimal to binary

generation1 = Genetic(10,8,524296,10,MAX)


while True:
  result = generation1.validate_generation()
  print("Generation ",generation1.generation)
  generation1.current_generation()
  if result[0] or abs(generation1.gap)<100:
    print("Result found at",generation1.generation,"rd generation")
    if result[0]:
        print(result[1].digits)
    else:
        print(generation1.promising.digits)
    break
  else:
    generation1.crossover_current()
    generation1.filter()
  generation1.generation+=1
  
  # for each in generation1.functions:
  #   print(each.digits)
  # input()


