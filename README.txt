How to use this board ES32G15

Important note : There is a conflict with certains pins and the Wifi module. So the Wifi connot be used 
with this board, because ADC pins are used for Thermistors inputs.

The board is attached to raspberry pi through serial port. So the serial repl is accessible through text
editor from raspberry pi. The board is also connected to the raspberry pi through modbus RTU serial for
data exchange / logging with node-red on raspberry pi. we could connect another board #2 ...

Actually, the main folder is located at home/pi/Documents/python-venv/myenv1/es32g15/
I'm using a virtual-env because it was easier to install "ampy module" for managing files with the serial
repl. I've created a folder called "es32g15" and put all python files in this "main" location.
Git is activated on this "es32g15" folder.

I'm using vscode as the main editor for code creation/editing and also connection with the raspberry pi.
I've installed "Remote-SSH" package for remote connection to the raspberry file.

The local PC doesn't have direct access to esp32 !!!
Pattern: Local-PC vscode <-> access raspberry pi  <-> esp32 serial serial connection

1- Launch vscode and remote connect ssh to 192.168.0.173 (SSH: 192.168.0.713 on lower left ... in green)
2- Open Folder located here "home/pi/Documents/python-venv/myenv1/es32g15/"
3- Go back to "myenv" folder and activate virtual-env do: source bin/activate. return to "es32g15" folder.
4- Use screen app to connect to the esp32 : screen /dev/ttyUSB0 115200 (ctrl+a and k to exit)
5- Edit local files if needed and don't forget to "push" them to the esp32 with "ampy" app
   
ampy commands :
ampy --port /dev/ttyUSB0 ls (listing content of board)
ampy --port /dev/ttyUSB0 run test.py (runs code from host PC)
ampy --port /dev/ttyUSB0 run -n test.py (runs code from host PC no output)
ampy --port /dev/ttyUSB0 get boot.py (display file content)
ampy --port /dev/ttyUSB0 rm boot.py (remove file)
ampy --port /dev/ttyUSB0 mkdir dirname (create a folder)
ampy --port /dev/ttyUSB0 rmdir dirname (remove folder and all files)
ampy --port /dev/ttyUSB0 get boot.py boot.py (save boot.py from the board to the host PC)
ampy --port /dev/ttyUSB0 put main.py /main.py (save main.py from host PC to the board (at root))