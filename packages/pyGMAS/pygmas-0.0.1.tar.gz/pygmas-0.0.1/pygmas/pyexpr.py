
from pygmas.utils import is_single


class pyexpr :
    
    def __init__(self, expr, varb=None) :
        
        """
        Parameters
        ----------
        expr : str
            Mathematical expression.
        
        varb : None or set
            Name of the variables constituting the expression.
        """
        
        assert type(expr) == str, "argument 'expr' must be str"
        assert varb == None or type(varb) == set, "argument 'varb' must be None or set" 
        
        if varb != None :
            varb = set(varb)
        else :
            varb = set()
        
        self.expr = expr
        self.varb = varb
         
        
    def __add__(self, to_add) :
        
        """
        Parameters
        ----------
        to_add : float or pyexpr

        Returns
        -------
        pyexpr.pyexpr
        """
        
        if type(to_add) == int or type(to_add) == float :
            new_expr = self.expr + '+' + str(to_add)
            new_varb = self.varb
        elif isinstance(to_add, pyexpr) :
            new_expr = self.expr + '+' + to_add.expr
            new_varb = self.varb.union(to_add.varb)
        else :
            raise ValueError('argument must be a number or pyexpr')
            
        new_pyexpr = pyexpr(new_expr, varb=new_varb)
        
        return new_pyexpr
        
        
    def __radd__(self, to_add) :
        
        """
        Parameters
        ----------
        to_add : float or pyexpr

        Returns
        -------
        pyexpr.pyexpr
        """
        
        if type(to_add) == int or type(to_add) == float :
            new_expr = str(to_add) + '+' + self.expr
            new_varb = self.varb
        elif isinstance(to_add, pyexpr) :
            new_expr = to_add.expr + '+' + self.expr
            new_varb = self.varb.union(to_add.varb)
        else :
            raise ValueError('argument must be a number or pyexpr')
            
        new_pyexpr = pyexpr(new_expr, varb=new_varb)
        
        return new_pyexpr

    
    def __sub__(self, to_sub) :
        
        """
        Parameters
        ----------
        to_sub : float or pyexpr

        Returns
        -------
        pyexpr.pyexpr
        """
        
        if type(to_sub) == int or type(to_sub) == float :
            new_expr = self.expr + '-' + str(to_sub)
            new_varb = self.varb
        elif isinstance(to_sub, pyexpr) :
            new_expr = self.expr + '-' + to_sub.expr
            new_varb = self.varb.union(to_sub.varb)
        else :
            raise ValueError('argument must be a number or pyexpr')
            
        new_pyexpr = pyexpr(new_expr, varb=new_varb)
        
        return new_pyexpr
        
        
    def __rsub__(self, to_sub) :
        
        """
        Parameters
        ----------
        to_sub : float or pyexpr

        Returns
        -------
        pyexpr.pyexpr
        """
        
        if type(to_sub) == int or type(to_sub) == float :
            new_expr = str(to_sub) + '-' + self.expr
            new_varb = self.varb
        elif isinstance(to_sub, pyexpr) :
            new_expr = to_sub.expr + '-' + self.expr
            new_varb = self.varb.union(to_sub.varb)
        else :
            raise ValueError('argument must be a number or pyexpr')
            
        new_pyexpr = pyexpr(new_expr, varb=new_varb)
        
        return new_pyexpr
        
        
    def __mul__(self, to_mul) :
        
        """
        Parameters
        ----------
        to_mul : float or pyexpr

        Returns
        -------
        pyexpr.pyexpr
        """
        
        if is_single(self.expr) :
            if isinstance(to_mul, pyexpr) :
                if is_single(to_mul.expr) :
                    new_expr = self.expr + '*' + to_mul.expr
                else :
                    new_expr = self.expr + '*' + '('  + to_mul.expr + ')'
                new_varb = self.varb.union(to_mul.varb)
            elif type(to_mul) == int or type(to_mul) == float :
                new_expr = self.expr + '*' + str(to_mul)    
                new_varb = self.varb   
            else :
                raise ValueError('argument must be a number or pyexpr')
        else :
            if isinstance(to_mul, pyexpr) :
                if is_single(to_mul.expr) :
                    new_expr = '(' + self.expr + ')' + '*' + to_mul.expr
                else :
                    new_expr = '(' + self.expr + ')' + '*' + '('  + to_mul.expr + ')'
                new_varb = self.varb.union(to_mul.varb)
            elif type(to_mul) == int or type(to_mul) == float :
                new_expr = '(' + self.expr + ')' + '*' + str(to_mul)
                new_varb = self.varb
            else :
                raise ValueError('argument must be a number or pyexpr')
            
        new_pyexpr = pyexpr(new_expr, varb=new_varb)
        
        return new_pyexpr

    
    def __rmul__(self, to_mul) :
        
        """
        Parameters
        ----------
        to_mul : float or pyexpr

        Returns
        -------
        pyexpr.pyexpr
        """
        
        if is_single(self.expr) :
            if isinstance(to_mul, pyexpr) :
                if is_single(to_mul.expr) :
                    new_expr = to_mul.expr + '*' + self.expr
                else :
                    new_expr = '(' + to_mul.expr + ')' + '*' + self.expr
                new_varb = self.varb.union(to_mul.varb)
            elif type(to_mul) == int or type(to_mul) == float :
                new_expr = str(to_mul) + '*' + self.expr    
                new_varb = self.varb
            else :
                raise ValueError('argument must be a number or pyexpr') 
        else :
            if isinstance(to_mul, pyexpr) :
                if is_single(to_mul.expr) :
                    new_expr = to_mul.expr + '*' + '(' + self.expr + ')'
                else :
                    new_expr = '(' + to_mul.expr + ')' + '*' + '(' + self.expr + ')'
                new_varb = self.varb.union(to_mul.varb)
            elif type(to_mul) == int or type(to_mul) == float :
                new_expr = str(to_mul) + '*' + '(' + self.expr + ')' 
                new_varb = self.varb
            else :
                raise ValueError('argument must be a number or pyexpr')            
        
        new_pyexpr = pyexpr(new_expr, varb=new_varb)
        
        return new_pyexpr
        
        
    def __truediv__(self, to_div) : 
        
        """
        Parameters
        ----------
        to_div : float or pyexpr

        Returns
        -------
        pyexpr.pyexpr
        """
        
        if is_single(self.expr) :
            if isinstance(to_div, pyexpr) :
                if is_single(to_div.expr) :
                    new_expr = self.expr + '/' + to_div.expr
                else :
                    new_expr = self.expr + '/' + '('  + to_div.expr + ')'
                new_varb = self.varb.union(to_div.varb)
            elif type(to_div) == int or type(to_div) == float :
                new_expr = self.expr + '/' + str(to_div)   
                new_varb = self.varb
            else :
                raise ValueError('argument must be a number or pyexpr')     
        else :
            if isinstance(to_div, pyexpr) :
                if is_single(to_div.expr) :
                    new_expr = '(' + self.expr + ')' + '/' + to_div.expr
                else :
                    new_expr = '(' + self.expr + ')' + '/' + '('  + to_div.expr + ')'
                new_varb = self.varb.union(to_div.varb)
            elif type(to_div) == int or type(to_div) == float :
                new_expr = '(' + self.expr + ')' + '/' + str(to_div)   
                new_varb = self.varb
            else :
                raise ValueError('argument must be a number or pyexpr')            

        new_pyexpr = pyexpr(new_expr, varb=new_varb)
        
        return new_pyexpr
            
        
    def __rtruediv__(self, to_div) : 
        
        """
        Parameters
        ----------
        to_div : float or pyexpr

        Returns
        -------
        pyexpr.pyexpr
        """
        
        if is_single(self.expr) :
            if isinstance(to_div, pyexpr) :
                if is_single(to_div.expr) :
                    new_expr = to_div.expr + '/' + self.expr
                else :
                    new_expr = '(' + to_div.expr + ')' + '/' + self.expr
                new_varb = self.varb.union(to_div.varb)
            elif type(to_div) == int or type(to_div) == float :
                new_expr = str(to_div) + '/' + self.expr  
                new_varb = self.varb
            else :
                raise ValueError('argument must be a number or pyexpr')  
        else :
            if isinstance(to_div, pyexpr) :
                if is_single(to_div.expr) :
                    new_expr = to_div.expr + '/' + '(' + self.expr + ')'
                else :
                    new_expr = '(' + to_div.expr + ')' + '/' + '(' + self.expr + ')'
                new_varb = self.varb.union(to_div.varb)
            elif type(to_div) == int or type(to_div) == float :
                new_expr = str(to_div) + '/' + '(' + self.expr + ')' 
                new_varb = self.varb
            else :
                raise ValueError('argument must be a number or pyexpr')

        new_pyexpr = pyexpr(new_expr, varb=new_varb)
        
        return new_pyexpr
        
        
    def __pow__(self, to_pow) : 
        
        """
        Parameters
        ----------
        to_pow : float or pyexpr

        Returns
        -------
        pyexpr.pyexpr
        """
        
        if is_single(self.expr) :
            if isinstance(to_pow, pyexpr) :
                if is_single(to_pow.expr) :
                    new_expr = self.expr + '**' + to_pow.expr
                else :
                    new_expr = self.expr + '**' + '('  + to_pow.expr + ')'
                new_varb = self.varb.union(to_pow.varb)
            elif type(to_pow) == int or type(to_pow) == float :
                new_expr = self.expr + '**' + str(to_pow)       
                new_varb = self.varb
            else :
                raise ValueError('argument must be a number or pyexpr')   
        else :
            if isinstance(to_pow, pyexpr) :
                if is_single(to_pow.expr) :
                    new_expr = '(' + self.expr + ')' + '**' + to_pow.expr
                else :
                    new_expr = '(' + self.expr + ')' + '**' + '('  + to_pow.expr + ')'
                new_varb = self.varb.union(to_pow.varb)
            elif type(to_pow) == int or type(to_pow) == float :
                new_expr = '(' + self.expr + ')' + '**' + str(to_pow)      
                new_varb = self.varb
            else :
                raise ValueError('argument must be a number or pyexpr')
   
        new_pyexpr = pyexpr(new_expr, varb=new_varb)
        
        return new_pyexpr
         
        
    def __rpow__(self, to_pow) : 
        
        """
        Parameters
        ----------
        to_pow : float or pyexpr

        Returns
        -------
        pyexpr.pyexpr
        """
        
        if is_single(self.expr) :
            if isinstance(to_pow, pyexpr) :
                if is_single(to_pow.expr) :
                    new_expr = to_pow.expr + '**' + self.expr
                else :
                    new_expr = '(' + to_pow.expr + ')' + '**' + self.expr
                new_varb = self.varb.union(to_pow.varb)
            elif type(to_pow) == int or type(to_pow) == float :
                new_expr = str(to_pow) + '**' + self.expr
                new_varb = self.varb
            else :
                raise ValueError('argument must be a number or pyexpr')
        else :
            if isinstance(to_pow, pyexpr) :
                if is_single(to_pow.expr) :
                    new_expr = to_pow.expr + '**' + '(' + self.expr + ')'
                else :
                    new_expr = '(' + to_pow.expr + ')' + '**' + '(' + self.expr + ')'
                new_varb = self.varb.union(to_pow.varb)
            elif type(to_pow) == int or type(to_pow) == float :
                new_expr = str(to_pow) + '**' + '(' + self.expr + ')' 
                new_varb = self.varb
            else :
                raise ValueError('argument must be a number or pyexpr')            

        new_pyexpr = pyexpr(new_expr, varb=new_varb)
        
        return new_pyexpr
    
    
    def calc(self, varb_dict) :
        
        """
        Parameters
        ----------
        varb_dict : dict
            key : str, name of a variable.
            value : float, current value of the variable.

        Returns
        -------
        float
            Expression calculation result.
        """
        
        assert type(varb_dict) == dict, "argument must be dict"
        
        assert self.varb <= set(varb_dict.keys()), "some variable of the attribute 'varb' is not the key of the argument 'varb_dict'"
            
        for varb in self.varb :
            value = varb_dict[varb]
            exec('{} = {}'.format(varb,str(value)))
        
        result = eval(self.expr)
        
        return float(result) 
    
    