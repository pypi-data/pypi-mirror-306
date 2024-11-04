
import math
import numpy as np


def combine_all(arrs) :
    
    """
    Parameters
    ----------
    arrs : sequence
        Every element must be a sequence.
    
    Returns
    -------
    list
    """
    
    combined = []
    for arr in arrs :
        combined += list(arr)
        
    return combined


# For a number x and an interval [a, b], If a < x < b, returns x, if x <= a, returns a, and if x >= b, returns b.
def rectified_ident_func(num, intv=None) : 
    
    """
    Parameters
    ----------
    num : float
    
    intv : None or sequence
        If not None, must be of the form ``[minimum, maximum]``.
    
    Returns
    -------
    float
    """
    
    if intv == None :
        intv = [-100, 100]
        
    a = intv[0]
    b = intv[1]
    
    if num <= a :
        num = a
    elif num >= b :
        num = b
    elif math.isnan(num) :
        num = 0
    
    return num
    

# Whether the operator is in the expression or not.
def is_single(expr) :
    
    """
    Parameters
    ----------
    expr : str
    
    Returns
    -------
    str
    """
    
    assert type(expr) == str, "argument must be str"
    
    if any(opt in expr for opt in ['+','-','*','/','**']) :
        return False
    else :
        return True


# Euler method.
def euler_mtd(y0, dy0, h) :

    """
    Parameters
    ----------
    y0 : float
        Value of y at the initial time.
        
    dy0 : float
        Derivative value of y at the initial time.
    
    h : float
        Step size.

    Returns
    -------
    float
        Value of y at the next time step.
    """

    y1 = y0 + h*dy0
    
    return y1
        

# Sum of squared residuals.
def get_ssr(arr1, arr2) : 

    """
    Parameters
    ----------
    arr1 : sequence

    arr2 : sequence

    Returns
    -------
    float
        Sum of squared residuals.
    """

    arr1 = np.array(arr1)
    arr2 = np.array(arr2)

    ssr = np.sum((arr1 - arr2)**2)

    return float(ssr)

