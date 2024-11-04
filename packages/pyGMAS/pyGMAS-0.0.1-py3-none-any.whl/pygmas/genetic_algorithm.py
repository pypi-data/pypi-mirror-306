
import struct
import numpy as np
import random

from pygmas.utils import combine_all


# Convert float to binary.
def float_to_binary(num):
    
    """
    Parameters
    ----------
    num : float
    
    Returns
    -------
    str
        Binary.
    """
    
    return format(struct.unpack('!I', struct.pack('!f', num))[0], '032b')


# Convert binary to float.
def binary_to_float(binary):
    
    """
    Parameters
    ----------
    binary : str
        Binary.
    
    Returns
    -------
    float
    """
    
    return round(struct.unpack('!f',struct.pack('!I', int(binary, 2)))[0], 5)


# Create an individual's DNA(concatenation of binary parameter values).
def create_indiv(param_list, intvs=None) : 
    
    """
    Parameters
    ----------
    param_list : sequence
          List of parameters.
    
    intvs : None or dict
        key : str, name of a parameter.
        value : sequence, parameter range of the form ``[minimum, maximum]``.
    
    Returns
    -------
    str 
        DNA of an individual(concatenation of binary parameter values).
    """
    
    if intvs == None :
        intvs = {param:None for param in param_list}
    
    indiv = ''
    for param in param_list :
        intv = intvs[param]
        if intv == None :
            indiv += float_to_binary(round(random.uniform(-100, 100), 5))
        else :
            indiv += float_to_binary(round(random.uniform(intv[0], intv[1]), 5))
        
    return indiv


# Create a population of individuals.
def create_indivs(pop, param_list, intvs=None) :
    
    """
    Parameters
    ----------
    pop : int
        Number of individuals.
    
    param_list : sequence
          List of parameters.
    
    intvs : None or dict
        key : str, name of a parameter.
        value : sequence, parameter range of the form ``[minimum, maximum]``.
    
    Returns
    -------
    list
        List of individuals.
    """
    
    if intvs == None :
        intvs = {param:None for param in param_list}
    
    indivs = []
    for i in range(pop) : 
        indiv = create_indiv(param_list, intvs)
        indivs.append(indiv)
        
    return indivs


# Create a mutated DNA.
def mutation(indiv, self=False) :
    
    """
    Parameters
    ----------
    indiv : str
        Individual.
        
    Returns
    -------
    str
        Mutations occur in some of the bits of the DNA.
    """
        
    mutated = indiv
    
    N = len(mutated)    
    subst_num = round(np.random.uniform(1, N/3))
        
    subst_num = abs(round(subst_num))
    subst_ind = np.random.choice(N, subst_num, False)
    
    for ind in subst_ind :
        swap = {'0':'1', '1':'0'}
        mutated = mutated[:ind] + swap[mutated[ind]] + mutated[ind+1:]
    
    return mutated


# Obtain offsprings by mating two individuals.
def mating(indiv1, indiv2, offs_num=1, prop=0.3) :
    
    """
    Parameters
    ----------
    indiv1 : str
        Father's DNA.
        
    indiv2 : str
        Mother's DNA.
        
    offs_num : int
        Number of offsprings.
        
    prop : float
        Proportion of the father's DNA inherited by the offspring.
    
    Returns
    -------
    list
        List of offspring's DNA.
    """
    
    cut_ind = round(len(indiv1) * prop)
    
    offsprings = []
    for i in range(offs_num) :
        offspring = indiv1[:cut_ind] + indiv2[cut_ind:]
        offspring = mutation(offspring)
        offsprings.append(offspring)
    
    return offsprings 


# Obtain the next generation of individuals(offsprings).
def next_generation(indivs, offs_num=1) : 
    
    """
    Parameters
    ----------
    indivs : sequence
        Individuals of current generation.
        len(indivis) must be even.
    
    Returns
    -------
    list
        Individuals of next generation(offsprings).
    """
    
    assert len(indivs) % 2 == 0, "length of the argument 'indivs' must be even"
    
    random.shuffle(indivs) 
    
    next_gen = []
    for i in range(0, len(indivs), 2) :
        indiv1 = indivs[i]
        indiv2 = indivs[i+1]
        offsprings = mating(indiv1, indiv2, offs_num)
        next_gen.append(offsprings)
        
    next_gen = combine_all(next_gen)
    
    return next_gen
    
