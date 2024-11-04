
from pygmas.utils import combine_all


def check_time(t, dt) :
    
    if type(t) != int and type(t) != float :
        raise ValueError("argument 't' must be a number")
    elif type(dt) != int and type(dt) != float :
        raise ValueError("argument 'dt' must be a number") 
        
    if not 0 < dt <= t :
        raise ValueError("must 0 < dt <= t")
        

def check_init_concens(init_concens) : 
    
    assert type(init_concens) == dict, "argument 'init_concens' must be dict"
    
    for value in init_concens.values() :
        if type(value) != int and type(value) != float :
            raise ValueError('concentration must be a number')
        elif value < 0 :
            raise ValueError('concentration must be greater than or equal to 0')
            

def check_obs_t(obs_t) : 
    
    assert obs_t[0] == 0, "first element of the argument 'obs_t' must be 0"
    
    for i in range(len(obs_t) - 1) : 
        if obs_t[i] >= obs_t[i+1] : 
            raise ValueError("argument 'obs_t' must be sorted in ascending order")
    
