from NyaClass import nya
import threading
from time import sleep
import time

if __name__ == '__main__':
    ts=[]
    accfile=open('buy_account.txt','r',encoding='utf-8')
    accs = accfile.readlines()
    accfile.close()
    while True:
        for acc in accs:
            if acc.startswith('#'):
                continue        
            nya_obj=nya(acc.strip())
            nya_obj.task("buy-1")
