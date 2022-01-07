import smtplib 
import subprocess
from subprocess import check_output
import sys
import os
import time

  
# creates SMTP session 
s = smtplib.SMTP('smtp.gmail.com', 587) 
  
# start TLS for security 
s.starttls() 
  
# Authentication 
s.login("dummy_sender@gmail.com", "password") 

loop_var = True
while loop_var:
    can_up = subprocess.check_output("ifconfig | grep can0 | awk '{print $1;}' &", shell=True)
    #print(can_up)
    if "can0:" in can_up:
        loop_var = False
        print("can interface is up")
        #300000
        can_status = subprocess.check_output("candump can0 -n 1 -T 60000 &", shell=True) # wait for atleast 1 can msg on can dump upto max timeout 1 min
        if can_status :
            print(can_status)
            print('Can data found')
            print('waiting 150sec to reboot the system')
            os.system('sleep 150')
            print('rebooting ...')
            os.system('reboot')
        else : 
            print("no can data")
            # message to be sent 
            message = "No Can data on bus waited for 1-min"
        
            # sending the mail 
            s.sendmail("dummy_sender@gmail.com", "report_to@gmail.com", message) 
            # terminating the session 
            s.quit()
    else:
        print("Can interface is not up yet sleeping 10 sec")
        os.system('sleep 10')

