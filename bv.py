'''
    Binary Value True/False
'''

class BinaryValue():

    def __init__(self, instance, name):
        self._instance = instance
        self._name = name
        self._newvalue = False
        self._lastvalue = False

    def get_name(self):
        return self._name

    def get_value(self):
        return self._newvalue

    def set_value(self, val):
        if isinstance(val, bool):
            self._newvalue = val
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

    #Set Property
    value = property(get_value, set_value)
    name = property(get_name)

#End