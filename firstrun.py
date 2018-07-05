from NyaClass import nya
import threading
from time import sleep

if __name__ == '__main__':
    taskfile=open('task.txt','r',encoding='utf-8')
    lines = taskfile.readlines()
    taskfile.close()
    for line in lines:
        if line.startswith('#'):
            continue
        print(line)
        data=(line.strip()).split(",")
        if(len(data))==3:
            nya_obj=nya(data[0],data[1])
            nya_obj.login_first()
            sleep(5) 
    #nya_obj=nya("boxpigstar0813",pw="cfalison")
    #nya_obj.login_first()
    #nya_obj.task("buy-1")
