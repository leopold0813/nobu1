from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.support.select import Select
import time
from time import sleep
import threading
from random import randint
town={"伊達家":1,"最上家":2,"北条家":3,"武田家":4,"上杉家":5,"徳川家":6,"織田家":7,"斎藤家":8,
      "三好家":9,"足利家":10,"毛利家":11,"尼子家":12,"長宗我部家":13,"龍造寺家":14,"大友家":15,"島津家":16}
skip_id=["6012","6015","6003","6007"]
#url
login_url='https://connect.mobage.jp/login'
game_url='http://sp.pf.mbga.jp/12004455'
main_url='http://sp.mbga.jp/'
home_url="http://sp.pf.mbga.jp/12004455?_isCnv=1&url=http%3A%2F%2F210.140.157.168%2Fmobile%2Fmobile_village.htm"
battle_url='http://sp.pf.mbga.jp/12004455?_isCnv=1&url=http%3A%2F%2F210.140.157.168%2Fmobile%2Fwar%2Fmobile_war_entry.htm'
trade_url='http://sp.pf.mbga.jp/12004455?_isCnv=1&url=http%3A%2F%2F210.140.157.168%2Fmobile%2Fcard%2Fmobile_trade_buy.htm'
map_url="http://sp.pf.mbga.jp/12004455?_isCnv=1&url=http%3A%2F%2F210.140.157.168%2Fmobile%2Fareamap%2Fmobile_areamap_top.htm"
info_url="http://sp.pf.mbga.jp/12004455?_isCnv=1&url=http%3A%2F%2F210.140.157.168%2Fmobile%2Fuser%2Fmobile_profile.htm"
'''
task说明
t 测试
b-r  合战路
s-a-b a,b升星
fa-a-b a,b刷算盘
'''
class nya(object):
    lock=threading.Lock()
    def __init__(self, task):
        mobile_emulation = {"deviceName":"iPhone 6"}
        options = webdriver.ChromeOptions()
        options.add_experimental_option('mobileEmulation', mobile_emulation)
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.set_window_size(396,766)
        self.acc=task[0]
        self.pw=task[1]
        self.quest=task[2]
    def __write_log(self,msg):
        self.lock.acquire()
        print("[%s]%s:%s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),self.acc,msg))
        self.lock.release()
    def __wait(self,sec):
        driver=self.driver
        driver.implicitly_wait(10)
        sleep(sec)        
    def __check_scene(self,scene):
        driver=self.driver
        try:
            a=driver.find_element_by_xpath("//div[@class='pagetitle_flare']/span")
            if (a.text).find(scene)!=-1:
                return True
            else:
                return False
        except:
            return False
    def __check_notice(self):
        driver=self.driver
        if self.__check_scene('の里'):
            return False
        try:
            if self.__check_scene("報告") or self.__check_scene("お知らせ"):
                btn=driver.find_element_by_id("sp-header-middle-btn")
                TouchActions(driver).tap(btn).perform()
                return True
            else:
                try:
                    a=driver.find_element_by_id("canvas")            
                    TouchActions(driver).tap(a).perform()
                    return True
                except:
                    return False
        except:
            return False                
    def __get_stay_town(self):
        driver=self.driver
        if not self.__check_scene('全国地図'):
            return 0
        else:
            a=driver.find_element_by_xpath("//*[contains(text(),'現在の拠点')]/..")
            return town[a.text[6:(a.text).find('家')+1]]
    def __move_to_town(self,town):
        driver=self.driver
        if not self.__check_scene('全国地図'):
            return False
        else:
            try:
                select=driver.find_element_by_xpath("//select[@name='id']")
                Select(select).select_by_value(str(town))
                sleep(1)
                driver.find_element_by_name("move_button").send_keys(Keys.RETURN)
                sleep(1)
                driver.find_element_by_xpath("//input[@value='移動する' and @type='submit']").send_keys(Keys.RETURN)
                sleep(1)
                while self.__check_notice():
                    sleep(2)
                return True
            except:
                return False
    def __check_abacus(self):
        driver=self.driver
        if not self.__check_scene('全国地図'):
            return -1
        enemys=driver.find_elements_by_class_name('enemy_container')
        for i,enemy in enumerate(enemys):
            if '算盤術' in enemy.text:
                return i
        else:
            return -1
    def __kill_enemy(self,index):
        driver=self.driver
        if not self.__check_scene('全国地図'):
            return False
        enemys=driver.find_elements_by_class_name('enemy_container')
        a=enemys[index].find_element_by_xpath(".//div[@class='enemy_button']/a")
        driver.get(a.get_attribute('href'))
        self.__wait(2)
        try:
            driver.find_element_by_id("sp_sc_5").submit()
            self.__wait(1)
            while self.__check_notice():
                sleep(2)
            return True
        except:
            return False
##    def find_rare(self):
##        driver=self.driver
##        driver.get(trade_url)
##        self.__wait(2)
##        if not self.__check_scene("交換所"):
##            print("check_rare error page")
##            return False
##        rare={}
##        while True:
##            btn5=driver.find_element_by_xpath("//img[@class='search_set_img' and @id='5']/..")
##            TouchActions(driver).tap(btn5).perform()
##            driver.implicitly_wait(10)
##            sleep(2)
##            cards=driver.find_elements_by_xpath("//*[contains(text(),'No.')]")
##            now_cards=[]
##            for card in cards:
##                a=card.text[-4:]
##                now_cards.append(a)
##            for card in now_cards:
##                if (card not in skip_id) and (card not in rare):
##                    rare[card]=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
##                    print("[%s]card %s found" % (rare[card],card))
##            for card in rare:
##                if card not in now_cards:
##                    print("[%s]card %s miss" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),card))
##                    rare.pop(card)                    
##            sleep(10)
    def __login_process(self):
        driver=self.driver
        driver.get(game_url)
        self.__wait(2)
        start_btn=driver.find_element_by_id("sp_sc_5")
        TouchActions(driver).tap(start_btn).perform()
        self.__wait(3)
        try:
            login_comfirm=driver.find_element_by_id("sp_sc_5")
            TouchActions(driver).tap(login_comfirm).perform()
            self.__wait(2)
        except:
            pass
        while self.__check_notice():
            self.__wait(2)
        while True:
            if not self.__check_scene('の里'):
                if not self.__check_notice():
                    driver.get(home_url)
                    self.__wait(2)
                else:
                    self.__wait(2)
            else:
                break
        driver.get(map_url)
        self.__wait(2)
        if self.__check_scene("名将探索"):
            try:
                a=driver.find_element_by_xpath("//*[contains(text(),'いいえ')]/..")
                TouchActions(driver).tap(a).perform()
                self.__wait(2)
            except:
                pass                            
        self.__write_log("login")
    def __login_by_password(self):
        driver=self.driver
        driver.get(login_url)
        self.__wait(2)
        yahoo_btn=driver.find_element_by_xpath("//section[@class='m-t-xl']/div[5]/a")
        driver.get(yahoo_btn.get_attribute('href'))
        self.__wait(2)
        id_input=driver.find_element_by_id("username")
        id_input.send_keys(self.acc+Keys.RETURN)
        self.__wait(2)
        pw_input=driver.find_element_by_id("passwd")
        pw_input.send_keys(self.pw+Keys.RETURN)
        self.__wait(5)
        driver.get(game_url)
        self.__wait(3)
        driver.get(main_url)
        self.__wait(3)
        try:
            file=open(self.acc+"_cookies.txt", "w")
            for item in driver.get_cookies():
                if 'SP' in item['name']:
                    file.write(item['name']+","+item['value']+'\n')
        except Exception as e:
            print("write cookies error :%s" % e)
        file.close()
        self.__login_process()
    def __login_by_cookies(self):
        try:
            cookie_file=open(self.acc+"_cookies.txt", "r")
        except:
            print("read cookies file error ")
            return False
        main_url='http://sp.mbga.jp'
        driver=self.driver
        driver.get(main_url)
        self.__wait(2)
        for line in cookie_file.readlines():
            ck=line.strip().split(',')
            add_ck={'name':ck[0],'value':ck[1]}
            driver.add_cookie(add_ck)
        cookie_file.close()    
        driver.get(main_url)
        self.__wait(2)
        self.__login_process()
        return True
    def find_abacus(self):
        driver=self.driver
        step=0
        times=0
        find=0
        while True:
            if step == 0:
                if not self.__check_scene('全国地図'):
                    driver.get(map_url)
                    self.__wait(2)
                else:
                    step=1
            elif step == 1:
                ret = self.__check_abacus()
                if ret == -1:                    
                    if self.__get_stay_town() != 9: #足利家
                        if not self.__move_to_town(9):
                            step=0
                        else:
                            times += 1
                            step=2
                    else:
                        if not self.__move_to_town(10):
                            step=0
                        else:
                            times += 1
                            step=2
                else: #bingo
                    if self.__kill_enemy(ret):
                        times += 1
                        find += 1
                        step=2
                    else:
                        step=0
            elif step == 2:
                if not self.__check_scene('の里'):
                    if not self.__check_notice():
                        driver.get(home_url)
                        self.__wait(2)
                    else:
                        self.__wait(2)
                else:
                    try:
                        command=driver.find_element_by_class_name('sp_village_command')
                        if '到着時間' in command.text:
                            sleep(10)
                        else:
                            self.__wait(1)
                            step=0
                            self.__write_log("find_abacus times=%d find=%d" % (times, find))
                    except:
                        pass
    def star_up(self,a,b):  #升星
        driver=self.driver
        home_url="http://sp.pf.mbga.jp/12004455?_isCnv=1&url=http%3A%2F%2F210.140.157.168%2Fmobile%2Fmobile_village.htm"
        map_url="http://sp.pf.mbga.jp/12004455?_isCnv=1&url=http%3A%2F%2F210.140.157.168%2Fmobile%2Fareamap%2Fmobile_areamap_top.htm"
        step=0
        step_before=0
        while True:
            if step==0:
                if not self.__check_scene('の里'):
                    if not self.__check_notice():
                        driver.get(home_url)
                        self.__wait(2)
                    else:
                        self.__wait(2)
                else:
                    try:
                        food=driver.find_element_by_xpath("//span[@id='element_food']")
                        if (int(food.text)) < 700:
                            self.__write_log("low food logout")
                            break
                    except:
                        pass
                    try:
                        command=driver.find_element_by_class_name('sp_village_command')
                        if '到着' in command.text:
                            sleep(60)
                            driver.refresh()
                            self.__wait(2)
                        else:
                            self.__wait(1)
                            step = 1
                    except:
                        driver.refresh()
                        self.__wait(2)
            elif step==1:
                if not self.__check_scene('全国地図'):
                    driver.get(map_url)
                    self.__wait(2)
                else:
                    step=2
            elif step==2:
                if self.__get_stay_town() != a and self.__get_stay_town() != b:
                    self.__move_to_town(a)
                    self.__wait(2)
                    step=0
                else:
                    enemys=driver.find_elements_by_class_name('enemy_container')
                    if len(enemys)==0:
                        step=3
                    elif len(enemys[0].find_elements_by_xpath(".//img[contains(@src,'difficulty_mark.png')]")) == 7:
                        step=3
                    else:
                        if self.__kill_enemy(0):
                            step=0
                        else:
                            step=0
            elif step==3:
                if self.__get_stay_town() != a:
                    self.__move_to_town(a)
                else:
                    self.__move_to_town(b)
                self.__wait(2)
                step=0
        driver.close()
    def battle(self, road):     #合战
        driver=self.driver
        step=0
        step_before=0
        while True:
            if step==0:
                if not self.__check_scene('の里'):
                    if not self.__check_notice():
                        driver.get(home_url)
                        self.__wait(2)
                    else:
                        self.__wait(2)
                else:
                    try:
                        command=driver.find_element_by_class_name('sp_village_command')
                        if '帰還' in command.text:
                            sleep(60)
                            driver.refresh()
                            self.__wait(2)
                        else:
                            self.__wait(1)
                            step = 1
                    except:
                        driver.refresh()
                        self.__wait(1)
            elif step==1:
                if not self.__check_scene('合戦状況'):
                    driver.get(battle_url)
                    self.__wait(2)
                else:
                    btns=driver.find_elements_by_xpath("//a[contains(@href,'entry_btl')]")
                    if (len(btns) <= 0):
                        self.__wait(2)
                        step = 0
                    elif (len(btns) == 1):
                        driver.get(btns[0].get_attribute('href'))
                        self.__wait(2)
                        try:
                            for i in range(3):
                                btn=driver.find_element_by_id("sp-header-middle-btn")
                                TouchActions(driver).tap(btn).perform()
                                self.__wait(2)
                            else:
                                step=2
                        except:
                            pass
                    else:
                        if road > 2:
                            road = 2
                        elif road < 0:
                            road = 0
                        driver.get(btns[road].get_attribute('href'))
                        self.__wait(2)
                        try:
                            for i in range(3):
                                btn=driver.find_element_by_id("sp-header-middle-btn")
                                TouchActions(driver).tap(btn).perform()
                                self.__wait(2)
                            else:
                                step=2
                        except:
                            pass
            elif step==2:
                if not self.__check_scene('の里'):
                    if not self.__check_notice():
                        driver.get(home_url)
                        self.__wait(2)
                    else:
                        self.__wait(2)
                else:
                    food=driver.find_element_by_xpath("//span[@id='element_food']")
                    if (int(food.text)) < 600:
                        sefl.__write_log("low food logout")
                        break
                    else:
                        try:
                            a=driver.find_element_by_xpath("//area[contains(@title,'楽市楽座')]")
                            TouchActions(driver).tap(a).perform()
                            sleep(1)
                            a=driver.find_element_by_xpath("//img[contains(@src,'btn_trade_all')]/..")
                            TouchActions(driver).tap(a).perform()
                            sleep(1)
                            btns=driver.find_elements_by_id("neko-alert-dynamic-ok-button")
                            for btn in btns:
                                if btn.is_displayed():
                                    TouchActions(driver).tap(btn).perform()
                                    break
                            self.__wait(2)
                            driver.refresh()
                            self.__wait(2)
                            step=0
                        except:
                           pass
    def buy(self, page):
        driver=self.driver
        if not self.__check_scene("交換所"):
            driver.get(trade_url)
            self.__wait(2)
        while True:
            try:
                btn=driver.find_element_by_xpath("//img[@class='search_set_img' and @id='%d']/.." % page)
                TouchActions(driver).tap(btn).perform()
                self.__wait(2)
                if '登用可能な武将がいません' not in driver.page_source:  
                    buybtns=driver.find_elements_by_xpath("//input[@value='登用']")                    
                    if len(buybtns) > 0:
                        buybtns[0].send_keys(Keys.RETURN)
                        self.__wait(1)
                        btns=driver.find_elements_by_id("neko-alert-dynamic-ok-button")
                        for btn in btns:
                            if btn.is_displayed():
                                TouchActions(driver).tap(btn).perform()
                                break
                        self.__wait(2)
                        driver.get(trade_url)
                        self.__wait(2)
                sleep(randint(3,5))
            except Exception as err:
                self.__write_log(err)   
                driver.get(trade_url)
                self.__wait(2)
    def task(self):        
        self.__write_log("start task:[%s]" % self.quest)
        if not self.__login_by_cookies():
            self.__login_by_password()
        quest=((self.quest).strip()).split("-")
        if quest[0] == 'b':
            self.battle(int(quest[1]))
        elif quest[0] == 's':
            self.star_up(int(quest[1]),int(quest[2]))
        elif quest[0] == 'fa':
            self.find_abacus()
        elif quest[0] == 'buy':
            self.buy(int(quest[1]))
        if quest[0] != 't':
            self.driver.close()
if __name__ == '__main__':
    tasks=[]    
    nyas=[]
    taskfile=open('task.txt','r',encoding='utf-8')
    for line in taskfile.readlines():
        data=(line.strip()).split(",")
        if(len(data))==3:
            tasks.append(data);
    taskfile.close()
    ts=[]
    for task in tasks:
        nyas.append(nya(task))
    for nya in nyas:
        ts.append(threading.Thread(target=nya.task, args=()))
    for t in ts:
        t.start()
    for t in ts:
        t.join()
