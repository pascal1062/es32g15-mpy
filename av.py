'''
    Analog Value. express a full number as integer or float
'''

class AnalogValue():

    def __init__(self, instance, name):
        self._instance = instance
        self._name = name
        self._priority_array = {i: None for i in range(1, 17)}
        self._relinquish_default = 0
        self._newvalue = 0
        self._lastvalue = 0 

    def get_name(self):
        return self._name
    
    def get_priority_array(self):
        return self._priority_array

    def get_value(self):
        for i in range(1, 17):
            val = self._priority_array[i]
            if val is not None:
                return val
        return self._relinquish_default
    
    def update_value(self):
        prio_value = self.get_value()
        self._newvalue = prio_value
        
    def write(self, val, priority=10):
        if isinstance(val, int) or isinstance(val, float) or val is None:
            self._priority_array[priority] = val
            self.update_value()            
        else:
            return 

    def changed(self):
        if self._newvalue != self._lastvalue:
            val = True
        else:
            val = False
        self._lastvalue = self._newvalue
        return val

    def greater(self):
        if (self._newvalue != self._lastvalue) and (self._newvalue > self._lastvalue):
            val = True
            self._lastvalue = self._newvalue
        else:
            val = False
        return val

    def smaller(self):
        if (self._newvalue != self._lastvalue) and (self._newvalue < self._lastvalue):
            val = True
            self._lastvalue = self._newvalue
        else:
            val = False
        return val

    #Set Property
    value = property(get_value)
    name = property(get_name)
    priority = property(get_priority_array)

#End