
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

from pygmas.pyexpr import pyexpr
from pygmas.prework import *
from pygmas.utils import *
from pygmas.genetic_algorithm import *


# single : a string that does not contain operators('+', '-', '*', '/', '**')
def single_to_pyexpr(*args) :
    
    """
    Parameters
    ----------
    *args 
        Every element must be a string.
    
    Returns
    -------
    list
        Every element is pyexpr.pyexpr.
    """

    for arg in args :
        if is_single(arg) == False :
            raise ValueError('argument contains operators such as + and -')
            
    pyexprs = []
    for arg in args :
        try : 
            float(arg)
            pyexprs.append(pyexpr(arg))
        except ValueError :
            pyexprs.append(pyexpr(arg, varb={arg}))

    return pyexprs


def estimate_parameters(gmas, param_list, obs_t, obs_concens, max_iter, intvs=None) : 
    
    """
    Parameters
    ----------
    gmas : dict
        key : str, name of a protein
        value : pyexpr, Generalized mass action model.
    
    param_list : sequence
        List of all parameters that exist in the GMA system.
    
    obs_t : sequence
        Observation times.

    obs_concens : dict
        key : str, name of a protein.
        value : sequence, concentration data collected at the observation times.
        
    max_iter : int
        Maximum number of iterations for the genetic algorithm. 
        
    intvs : None or dict
        key : str, name of a parameter.
        value : sequence, parameter range of the form ``[minimum, maximum]``.

    Returns
    -------
    dict
        key : name of a protein.
        value : tuple, contains estimated parameter values and SSR.
    """
    
    check_obs_t(obs_t)
    
    pop = 200
    surv_num = 20
    
    prots = list(obs_concens.keys())
    
    estimates = {}
    for prot in prots :
        print("Protein '{}' start".format(prot))
        
        gma = gmas[prot]
        sub_prots = list(set(gma.varb).intersection(set(prots)))
        sub_param_list = list(set(gma.varb).intersection(set(param_list)))
        if intvs == None :
            intvs = {param:None for param in sub_param_list}
        
        obs_concen = obs_concens[prot]
        indivs = create_indivs(pop, sub_param_list, intvs)
        for i in range(max_iter) :
            print('Iteration : {}'.format(i+1))
            if i == 0 :
                indivs = next_generation(indivs, offs_num=2)         
                
                ssr_dict = {}
                for indiv in indivs :
                    params = {sub_param_list[i]:indiv[i*32:i*32+32] for i in range(len(sub_param_list))}
                    params = {param:rectified_ident_func(binary_to_float(binary), intvs[param]) for param, binary in params.items()}
                    pred_concen = []
                    for j in range(len(obs_t)) :
                        if j == 0 :
                            pred_concen.append(obs_concen[0])
                        else :
                            varb_dict = {}
                            for varb in gma.varb :
                                if varb in sub_prots :
                                    if varb != prot :
                                        varb_dict[varb] = obs_concens[varb][j-1]
                                    elif varb == prot :
                                        varb_dict[varb] = pred_concen[j-1]
                                elif varb in params.keys() :
                                    varb_dict[varb] = params[varb]
                            y0 = pred_concen[j-1]
                            dy0 = gma.calc(varb_dict)
                            y1 = euler_mtd(y0, dy0, obs_t[j]-obs_t[j-1])
                            pred_concen.append(y1)
                    ssr_dict[indiv] = get_ssr(obs_concen, pred_concen)
                    
                indivs = sorted(ssr_dict.items(), key=lambda x: x[1])
                indivs = indivs[:surv_num]
                indivs = [indiv[0] for indiv in indivs]
            else :
                offs_num = int((pop/surv_num - 1)*2)
                offsprings = next_generation(indivs, offs_num)
                indivs = indivs + offsprings
            
                ssr_dict = {}
                for indiv in indivs :
                    params = {sub_param_list[i]:indiv[i*32:i*32+32] for i in range(len(sub_param_list))}
                    params = {param:rectified_ident_func(binary_to_float(binary)) for param, binary in params.items()}
                    obs_concen = obs_concens[prot]
                    pred_concen = []
                    for j in range(len(obs_t)) :
                        if j == 0 :
                            pred_concen.append(obs_concen[0])
                        else :
                            varb_dict = {}
                            for varb in gma.varb :
                                if varb in sub_prots :
                                    if varb != prot :
                                        varb_dict[varb] = obs_concens[varb][j-1]
                                    elif varb == prot :
                                        varb_dict[varb] = pred_concen[j-1]
                                elif varb in params.keys() :
                                    varb_dict[varb] = params[varb]
                            y0 = pred_concen[j-1]
                            dy0 = gma.calc(varb_dict)              
                            y1 = euler_mtd(y0, dy0, obs_t[j]-obs_t[j-1])
                            pred_concen.append(y1)
                    ssr_dict[indiv] = get_ssr(obs_concen, pred_concen)
                    
                indivs = sorted(ssr_dict.items(), key=lambda x: x[1])
                indivs = indivs[:surv_num]
                indivs = [indiv[0] for indiv in indivs]
                
        print("Protein '{}' end\n".format(prot))
        
        indiv = indivs[0]
        ssr = ssr_dict[indiv]
        params = {sub_param_list[i]:indiv[i*32:i*32+32] for i in range(len(sub_param_list))}
        params = {param:rectified_ident_func(binary_to_float(binary)) for param, binary in params.items()}
        
        estimates[prot] = (params, ssr)
   
    return estimates
      

class gma_system : 
    
    def __init__(self, gmas, init_concens, t, dt, params=None) :
        
        """
        Parameters
        ----------
        gmas : dict
            key : str, name of a protein
            value : pyexpr, Generalized mass action model to represent the reaction rate of the protein.

        init_concens : dict
            key : str, name of a protein.
            value : float, initial concentration of the protein.
            
        t : float 
            Total time.

        dt : float 
            Must be greater than 0 and less than t.
        
        params : dict
            key : str, name of a GMA parameter.
            value : float, parameter value.
        """
        
        if params == None :
            params = {}
        
        check_time(t, dt)
        check_init_concens(init_concens)
    
        prots = list(gmas.keys())
        
        self.prots = prots
        self.gmas = gmas
        self.init_concens = init_concens
        self.params = params
        self.t = t
        self.dt = dt
        
        
    def run(self) : 
            
        concens = {prot:[self.init_concens[prot]] for prot in self.prots}
        rates = {prot:[] for prot in self.prots}
        
        for i in range(math.floor(self.t / self.dt)) :
            for prot in self.prots :
                gma = self.gmas[prot]
                
                varb_dict = {}
                for varb in gma.varb :
                    if varb in self.prots :
                        varb_dict[varb] = concens[varb][i]
                    elif varb in self.params.keys() :
                        varb_dict[varb] = self.params[varb]
                        
                y0 = concens[prot][i]
                dy0 = gma.calc(varb_dict)
                y1 = euler_mtd(y0, dy0, self.dt)
                
                rates[prot].append(dy0)
                concens[prot].append(y1)

        self.concens = concens
        self.rates = rates
        
        
    def update(self, addit_t, addit_concens=None) :
        
        """
        Parameters
        ----------
        addit_t : float
            Additional time.
        
        addit_concens : dict
            Additional protein concentrations.
        """
        
        assert self.concens, 'please run the run() method first'
        
        for key, value in addit_concens.items() :
            if key in self.prots :
                self.concens[key][-1] += value

        N = math.floor(self.t / self.dt) 
        for i in range(math.floor((self.t + addit_t - N * self.dt) / self.dt)) :
            for prot in self.prots :
                gma = self.gmas[prot]
                
                varb_dict = {}
                for varb in gma.varb :
                    if varb in self.prots :
                        varb_dict[varb] = self.concens[varb][-1]
                    elif varb in self.params.keys() :
                        varb_dict[varb] = self.params[varb]
                        
                y0 = self.concens[prot][i]
                dy0 = gma.calc(varb_dict)
                y1 = euler_mtd(y0, dy0, self.dt)
                
                self.rates[prot].append(dy0)
                self.concens[prot].append(y1)

        self.t += addit_t

    
    def search(self, query_t, query_prots=None) :
        
        """
        Parameters
        ----------
        query_t : float
            Time to search.
        
        query_prots : None or sequence
            Proteins to search.
            
        Returns
        -------
        query_t : float
            Input argument ``query_t``.
            
        result : dict
            key : str, protein in the input argument ``query_prots``.
            value : dict, concentration and reaction rate.
        """
        
        assert self.concens, 'please run the run() method first'
        assert 0 <= query_t <= self.t, "must 0 <= argument 'query_t' <= attribute 't'"
        
        if query_prots == None :
            query_prots = self.prots
        
        result = {prot:{} for prot in query_prots}
        
        ind = math.floor(query_t / self.dt)
        for prot in query_prots :
            if ind == math.floor(self.t / self.dt) :
                rate = None
            else : 
                rate = self.rates[prot][ind]
                
            concen = self.concens[prot][ind]
            result[prot] = {'concen':concen, 'rate': rate}
        
        return query_t, result
    
    
    def search_final(self, query_prots=None) :
        
        """
        Parameters
        ----------
        query_prots : None or sequence
            Proteins to search.
            
        Returns
        -------
        dict
            key : 'final_concen' and 'final_rate'
            value : dict, concentration and reaction rate at the final time step.
        """
        
        assert self.concens, 'please run the run() method first'
        
        if query_prots == None :
            query_prots = self.prots
        
        final_concen = {prot : self.concens[prot][-1] for prot in query_prots}
        final_rate = {prot : self.rates[prot][-1] for prot in query_prots}
        
        self.final_concen = final_concen
        self.final_rate = final_rate
        
        return {'final_concen':final_concen, 'final_rate': final_rate}
        
        
    def gma_solve(self) :
        
        """ 
        Returns
        -------
        dict
            key : str, name of a protein.
            value : float, concentration where the reaction rate is 0.
        """
        
        init_concen_list = list(self.init_concens.values())
                    
        solution = fsolve(self.gmas_to_rates(self.gmas, self.params), init_concen_list)
        solution = {self.prots[i] : solution[i] for i in range(len(self.prots))}
        
        self.solution = solution
        
        return solution
        

    def back(self, back_t) :
        
        """
        Parameters
        ----------
        back_t : float
            Time to return.
        """
        
        assert self.concens, 'please run the run() method first'
        assert 0 <= back_t < self.t, "must 0 <= argument 'back_t' < attribute 't'"
        
        ind = math.floor(back_t / self.dt)
        
        self.concens = {prot : self.concens[prot][:ind+1] for prot in self.prots}
        self.rates = {prot : self.rates[prot][:ind+1] for prot in self.prots}
        self.t = back_t
        
        
    def estimate_convergence(self, tol) :
        
        """
        Parameters
        ----------
        tol : float
            Toleration.
            
        Returns
        -------
        dict
            key : str, name of a protein.
            value : bool, whether converges or not.
        """
        
        assert self.concens, 'please run the run() method first'
        
        convergence = {}
        for prot in self.prots :
            final_rate = self.rates[prot][-1]
            if abs(final_rate) < tol :
                convergence[prot] = True
            else :
                convergence[prot] = False
            
        return convergence
        
        
    def plot(self, intv=None) : 
        
        """
        Parameters
        ----------
        intv : sequence 
            Must be of the form ``[start, end]``.
            
        Returns
        -------
        pyplot.plot
        """
        
        assert self.concens, 'please run the run() method first'
        
        if intv == None :
            intv = [0, self.t]

        start_ind = math.ceil(intv[0] / self.dt)
        end_ind = math.floor(intv[1] / self.dt)
        if not 0 <= start_ind <= end_ind :
            raise ValueError("invalid argument 'intv'")
        
        start_t = start_ind * self.dt
        end_t = end_ind * self.dt
                
        max_concen = max([max(self.concens[prot][start_ind:end_ind+1]) for prot in self.prots])
        min_concen = min([min(self.concens[prot][start_ind:end_ind+1]) for prot in self.prots])
        if max_concen > 0 :
            max_concen = max_concen*1.2
        else :
            max_concen = max_concen*0.8
        if min_concen > 0 :
            min_concen = min_concen*0.8
        else :
            min_concen = min_concen*1.2
                
        fig = plt.figure(figsize=(12,7))
        x = np.arange(start_t, end_t+self.dt/2, self.dt)
        for prot, concen in self.concens.items() :
            plt.plot(x, concen[start_ind:end_ind+1], label=prot)
        
        plt.xlim(intv)
        plt.ylim([min_concen, max_concen])
        plt.legend()
        plt.show() 

        
    def gmas_to_rates(self, gmas, params) :
        
        """
        Parameters
        ----------
        gmas : dict
            key : str, name of a protein
            value : pyexpr, Generalized mass action model.
        
        params : dict
            key : str, name of a GMA parameter.
            value : float, parameter value.
            
        Returns
        -------
        function
            Returns a list containing the reaction rate of proteins.
        """

        def get_rates(concen_list) :
            
            """
            Parameters
            ----------
            concen_list : list
                Protein concentrations.

            Returns
            -------
            
            """

            prots = list(gmas.keys())

            rates = []
            for gma in gmas.values() :
                varb_dict = {}
                for i in range(len(prots)) :
                    varb_dict[prots[i]] = concen_list[i]
                for param, value in params.items() :
                    varb_dict[param] = value            
                rates.append(gma.calc(varb_dict))

            return rates

        return get_rates
        
   