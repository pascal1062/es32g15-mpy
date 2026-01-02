
{"brd":1,"req":"set","id":"sys","val":"rst"}
{"brd":1,"req":"set","id":"sys","val":"tsync"}
{"brd":1,"req":"get","id":"sys","val":"time"}
{"brd":1,"req":"get","id":"T1","val":"null"}
{"brd":1,"req":"set","id":"CH4","val":"On"}

{"brd":1,"val":"tsync","t":"2025-12-30 11:18:05-5"}

msg = json.loads(_msg) # faire un try ...

if msg['brd'] == 1 and msg['val'] == "tsync" and regex.match(msg['t']):
	_set_time(msg['t'])

if msg['brd'] == 1 and msg['req'] == "get":
	if msg['id'] == "sys" and msg['val'] == "time": xfer.send_recv({"date-time":str(actualTime(time.localtime()))})
	
	if msg['id'] == "T1" and msg['val'] == "null": xfer.send_recv({"T1":plc.T1.value})
	if msg['id'] == "T2" and msg['val'] == "null": xfer.send_recv({"T1":plc.T2.value})
	if msg['id'] == "VI1" and msg['val'] == "null": xfer.send_recv({"T1":plc.VI1.value})
	if msg['id'] == "PHOTO" and msg['val'] == "null": xfer.send_recv({"T1":plc.PH4.value})
	
if msg['brd'] == 1 and msg['req'] == "set":
	if msg['id'] == "sys" and msg['val'] == "rst": _stop()
	if msg['id'] == "sys" and msg['val'] == "tsync": xfer.send_recv({"time-sync":"received"})
	
	if msg['id'] == "CH4": and msg['val'] == "On": plc.CH4.value = True
	if msg['id'] == "CH4": and msg['val'] == "Off": plc.CH4.value = False




#old files
def exec():
    read = xchg.send_recv()
    try:
        msg = read.decode("utf8")
    except:
        msg = ""
    
    if msg == "/es32g15/system/exit": _stop()
    if msg == "/es32g15/relayBoard/date-heure": xchg.send_recv({"date-time":str(actualTime(time.localtime()))})
    if msg == "/es32g15/relayBoard/ch4/set/1": plc.CH4.value = True
    if msg == "/es32g15/relayBoard/ch4/set/0": plc.CH4.value = False
    if msg == "/es32g15/relayBoard/t1/get": xchg.send_recv({"T1":plc.T1.value})
    if msg == "/es32g15/relayBoard/t2/get": xchg.send_recv({"T2":plc.T2.value})
    if msg == "/es32g15/relayBoard/photo/get": xchg.send_recv({"PHOTO":plc.PH4.value})
    if msg == "/es32g15/relayBoard/vi1/get": xchg.send_recv({"VI1":plc.VI1.value})


#To-Do
'''
 si l'heure est synchronisé avec une date inférieure, les timers ne fonctionnent plus
 il faudrait resetter tous les timers dans mes programmes
 
 scanner les entrées qui ne sont pas dans un pg --Fait--
 
 Analog output .value retour 0-100 au lien de 0-255
 
 faire du logging
 
 rename data_exchange-ser to rx_tx.py
 
 

'''

{"T1":plc.T1.value, "T2":plc.T2.value, "PHOTO":plc.PH4.value, "VI1":plc.VI1.value, "DI1":plc.IN1.value, 
 "CH1":plc.CH1.value, "CH2":plc.CH2.value, "CH3":plc.CH3.value, "CH4":plc.CH4.value, "AO1":plc.VO1.value, 
 "AO2":plc.VO2.value, "BV1":START_CH1.value
}