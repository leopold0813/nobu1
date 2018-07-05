from NyaClass import nya
import threading
from time import sleep

if __name__ == '__main__':
    ts=[]
    accfile=open('buy_account.txt','r',encoding='utf-8')
    accs = accfile.readlines()
    accfile.close()
    for acc in accs:
        if acc.startswith('#'):
            continue        
        nya_obj=nya(acc.strip())
        t = threading.Thread(target=nya_obj.task, args=("buy-1",))
        t.start()
        ts.append(t)
        sleep(20)   
    for t in ts:
        t.join()
    print("loop\n")
    