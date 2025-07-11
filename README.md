# SmartTaskTool
Tray-iocns for task-bar, Drives, CPU, GPU, Network
=> only windows! (only Nvidia atm)

exe file on huggingface:
https://huggingface.co/kalle07/SmartTaskTool

Read / Write - Detection on your Hard Drives
CPU - Usage
RAM - Usage
GPU - Usage (all only nvidia)
VRAM - Usage
GPU Temperature
Network - download/upload
-> Update once per second

My Icons look like this: (depending on hard drives/partitions, Network, GPU)<br>
<img width="720" height="224" alt="grafik" src="https://github.com/user-attachments/assets/77123810-4938-452a-a4cf-7a6ba2eabcc2" />
<br>
At start you can choose:<br>
<img width="481" height="569" alt="grafik" src="https://github.com/user-attachments/assets/2e35330b-75a3-4070-a4c2-10a11db5585d" />
<br>


python (4 files, start main) or exe
with WMI so its slow(psutil dont work with partitions and network)
Iam not a coder so its a co-work of chatgpt and my brain ;)

GPU should be work with multi GPUs if nvidia, AMD has no python lib for windows
Network should be work with all connected network adapters (in tray-icon no name, but with mouse hover over you will see)
On start you will see a GUI, you have 10 secons to choose hardware.


Further work:
Iam on it to implement to save a config-file for reuse... all its not that easy for me ;) 


Hints:
Drive threshold 2MB (this means that only larger actions are displayed)
red - writing | green - reading | yellow - <read/write>
Network start at 0.1kB/s up to GB/s
Mouse hover - You see a little more detail, but it is not updated
If you put in autostart, try to delay start 5 to 10sec
mause "right click" - EXIT or Restart
reetart dont work on exe (dont know why)


=> All at your own risk !!!
