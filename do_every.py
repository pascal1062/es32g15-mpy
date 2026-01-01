import time

class DoEvery():
    
    def __init__(self, name, unit):
        self._name = name
        self._unit = unit
        self._end = time.time()
        self._newvalue = False
        self._lastvalue = False
        
    def every(self, t):
        val = False
        if self._unit == "sec":
            if (time.time() - self._end) >= t:
                self._end = time.time()
                self._newvalue = True
            else:
                self._newvalue = False
        elif self._unit == "min":
            if (time.time() - self._end) >= (t*60):
                self._end = time.time()
                self._newvalue = True
            else:
                self._newvalue = False
        elif self._unit == "hour":
            if (time.time() - self._end) >= (t*3600):
                self._end = time.time()
                self._newvalue = True
            else:
                self._newvalue = False
        else:
            self._newvalue = False
 
 
        if (self._newvalue != self._lastvalue) and (self._newvalue == True):
            val = True
        else:
            val = False
        self._lastvalue = self._newvalue

        return val
        
#End