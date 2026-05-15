'''
    Binary Value True/False. Implemented with priority array.
'''

class BinaryValue():

    def __init__(self, instance, name):
        self._instance = instance
        self._name = name
        self._newvalue = False
        self._lastvalue = False
        self._priority_array = {i: None for i in range(1, 17)}
        self._relinquish_default = False  

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
        logic_state = self.get_value()
        self._newvalue = True if logic_state == True else False 
        
    def write(self, val, priority=10):
        if isinstance(val, bool) or val is None:
            self._priority_array[priority] = val
            self.update_value()            
        else:
            return

    def changed(self):
        self.value
        if self._newvalue != self._lastvalue:
            val = True
        else:
            val = False
        self._lastvalue = self._newvalue
        return val

    def rising(self):
        self.value
        if self._newvalue != self._lastvalue:
            val = self._newvalue
        else:
            val = False
        self._lastvalue = self._newvalue
        return val

    def falling(self):
        self.value
        if (self._newvalue != self._lastvalue):
            val = not self._newvalue
        else:
            val = False
        self._lastvalue = self._newvalue
        return val

    #Get Property
    value = property(get_value)
    name = property(get_name)
    priority = property(get_priority_array)

#End

'''
# --- EXEMPLE D'UTILISATION ---
BV1 = BinaryValue(1, "BV1")

# 1. Le programme (Prio 10) démarre la BV
BV1.write(True,10) OR BV1.write(True) OR BV1.write(False)

# 2. Un technicien force l'arrêt manuellement (Prio 8)
BV1.write(False,8)  

# 3. Le technicien repasse en automatique (Libère la Prio 8)
BV1.write(None,8) # La pompe repasse à 1 (car Prio 10 est toujours active)

'''