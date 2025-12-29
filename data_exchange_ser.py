from machine import UART, Pin
import select
import ujson
    
class DataExchange():

    def __init__(self, uart_id, baud_rate, tx_pin, rx_pin):
        self._uart = UART(uart_id, baudrate=baud_rate, tx=Pin(tx_pin), rx=Pin(rx_pin))
        self._poller = select.poll()
        self._poller.register(self._uart, select.POLLIN | select.POLLOUT)
        self._data = None
        self._data_in = None
        self._data_out = None
        self._rcvd_str = None
        self._buffer = b''

    def close(self):
        self._uart.deinit()

    def recv_data(self):
        while True:
            self._data = None
            res = self._poller.poll(1)
            if res:
                if res[0][1] & select.POLLIN:
                    try:
                        return self._uart.read()
                    except:
                        return None
                    break
            return None
            break

    def send_data(self, message):
        try:
            self._uart.write(ujson.dumps(message))
            self._uart.write('\n')
        except:
            pass

    def send_recv(self, msg=None):
        self._data_in = None
        self._rcvd_str = None
        self._data_out = msg
        events = self._poller.poll(1)
        if events:
            for obj, event in events:
                if event & select.POLLIN:
                    if self._uart.any():
                        char = self._uart.read(1)
                        if char != b'!':
                            self._buffer += char
                        else:    
                            self._data_in = self._buffer
                            self._buffer = b''
                if event & select.POLLOUT:
                    if self._data_out is not None: 
                        self._uart.write(ujson.dumps(self._data_out))
                        self._uart.write('\n')
                        self._data_out = None

            
            return self._data_in

#Fin