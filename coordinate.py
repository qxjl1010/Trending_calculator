import time, os 

def re_exe(cmd, inc): 
    while True: 
        os.system(cmd); 
        time.sleep(inc) 

print("ready to excute scrapt...") 
re_exe("sudo supervisorctl restart trending", 60*60*3)