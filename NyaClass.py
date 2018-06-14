from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.support.select import Select
import time
from time import sleep
import threading

login_url='https://connect.mobage.jp/login'
game_url='http://sp.pf.mbga.jp/12004455'
main_url='http://sp.mbga.jp/'
home_url="http://sp.pf.mbga.jp/12004455?_isCnv=1&url=http%3A%2F%2F210.140.157.168%2Fmobile%2Fmobile_village.htm"
battle_url='http://sp.pf.mbga.jp/12004455?_isCnv=1&url=http%3A%2F%2F210.140.157.168%2Fmobile%2Fwar%2Fmobile_war_entry.htm'
trade_url='http://sp.pf.mbga.jp/12004455?_isCnv=1&url=http%3A%2F%2F210.140.157.168%2Fmobile%2Fcard%2Fmobile_trade_buy.htm'
map_url="http://sp.pf.mbga.jp/12004455?_isCnv=1&url=http%3A%2F%2F210.140.157.168%2Fmobile%2Fareamap%2Fmobile_areamap_top.htm"
info_url="http://sp.pf.mbga.jp/12004455?_isCnv=1&url=http%3A%2F%2F210.140.157.168%2Fmobile%2Fuser%2Fmobile_profile.htm"
deck_url="http://sp.pf.mbga.jp/12004455?_isCnv=1&url=http%3A%2F%2F210.140.157.168%2Fmobile%2Fcard%2Fmobile_manage_deck.htm"
town={"伊達家":1,"最上家":2,"北条家":3,"武田家":4,"上杉家":5,"徳川家":6,"織田家":7,"斎藤家":8,
      "三好家":9,"足利家":10,"毛利家":11,"尼子家":12,"長宗我部家":13,"龍造寺家":14,"大友家":15,"島津家":16}

class nya(object):
    lock=threading.Lock()
    def __init__(self,acc,pw=''):
        self.acc=acc
        self.pw=pw
    def __start_driver(self,noimage=False):
        self.noimage=noimage
        mobile_emulation = {"deviceName":"iPhone 6"}
        options = webdriver.ChromeOptions()
        options.add_experimental_option('mobileEmulation', mobile_emulation)
        options.add_argument("--window-size=396,840")
        options.add_argument("--disable-web-security")
        options.add_argument(r"user-data-dir=.\%s_data" % self.acc)
        prefs = {"profile.managed_default_content_settings.images":2 if self.noimage else 1}
        options.add_experimental_option("prefs",prefs)
        self.driver = webdriver.Chrome(chrome_options=options)
        #self.driver.set_page_load_timeout(5)  
        #self.driver.set_script_timeout(5)        
        self.login=False
        self.setspell=True
        self.lowfood=False
        sleep(10)
    def __stop_driver(self):
        if self.driver is not None:
            self.driver.close()
    def __write_log(self,msg):
        self.lock.acquire()
        print("[%s]%s:%s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),self.acc,msg))
        self.lock.release()
    def __wait(self,sec):
        driver=self.driver
        driver.implicitly_wait(5)
        if sec>0:
            sleep(sec)
    def __goto(self,url):
        driver=self.driver
        driver.get(url)
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
        if 'flash' in driver.current_url:
            try:
                a=driver.find_element_by_id("canvas")            
                TouchActions(driver).tap(a).perform()
                return True
            except:
                return False
        else:
            try:
                if self.__check_scene("報告") or self.__check_scene("お知らせ"):
                    btn=driver.find_element_by_id("sp-header-middle-btn")
                    TouchActions(driver).tap(btn).perform()
                    return True
                else:                
                    return False
            except:
                return False
    def __check_meishou(self):
        driver=self.driver
        if self.__check_scene("名将探索"):
            try:
                a=driver.find_element_by_xpath("//*[contains(text(),'いいえ')]/..")
                TouchActions(driver).tap(a).perform()
                self.__wait(1)
            except:
                pass
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
                driver.find_element_by_name("move_button").send_keys(Keys.RETURN)
                driver.find_element_by_xpath("//input[@value='移動する' and @type='submit']").send_keys(Keys.RETURN)
                while self.__check_notice():
                    sleep(1)
                return True
            except:
                return False
    def __check_abacus(self):
        driver=self.driver
        if not self.__check_scene('全国地図'):
            return -1
        enemys=driver.find_elements_by_class_name('enemy_container')
        if len(enemys) == 0:
            return -1
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
        if len(enemys) == 0:
            return False
        a=enemys[index].find_element_by_xpath(".//div[@class='enemy_button']/a")
        self.__goto(a.get_attribute('href'))
        self.__wait(2)
        try:
            driver.find_element_by_id("sp_sc_5").submit()
            self.__wait(1)
            while self.__check_notice():
                sleep(1)
            return True
        except:
            return False
    def __change_food(self):
        driver=self.driver
        if not self.__check_scene('の里'):
            return False
        try:
            firetext=driver.find_element_by_xpath("//span[@id='element_fire']")
        except:
            return False
        if int(firetext.text) <= 0:
            return False
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
        except:
           return False
        return True
    def __set_abacus(self):        
        self.setspell=False
        driver=self.driver
        self.__goto(deck_url)
        self.__wait(2)
        #切换到奥义标签
        try:
            for i in range(3):
                tap3=driver.find_element_by_xpath("//*[contains(@class,'tabindex3') and contains(@class,'hensei_tab_ng')]")
                if not tap3.is_displayed():
                    break
                TouchActions(driver).tap(tap3).perform()
                self.__wait(1)
        except:
            self.__goto(home_url)
            self.__wait(2)
            return
        #一括補充
        driver.find_element_by_xpath("//input[@value='一括補充']").send_keys(Keys.RETURN)
        sleep(1)
        #持有奥义
        abacus=0
        abacus_bag=0
        frames=driver.find_elements_by_class_name("td-select-frame")
        for i in range(len(frames)):
            if '算盤術' in frames[i].text:
                info=(frames[i].text).split("\n")
                abacus=abacus+int(info[2])
        self.__wait(2)
        index=4        
        if abacus < 50:
            index = abacus//10
        for i in range(index,5):
            bhave = True
            if i == index and abacus%10 == 0:
                bhave = False
            else:
                bhave = False if i > index else True
            TouchActions(driver).tap(frames[i]).perform()
            self.__wait(2)
            sortset=['td-sort-element','td-sort-level','td-sort-system']
            inputset=['5','4','3']
            for j in range(3):
                select=driver.find_element_by_xpath("//select[@id='%s']" % sortset[j])
                Select(select).select_by_value(inputset[j])
                sleep(1)
            try:
                a=driver.find_element_by_xpath("//*[contains(@class,'td-reserve-frame') and contains(@class,'703')]")
                if '算盤術' in a.text:
                    if abacus_bag == 0:
                        info2=(a.text).split("\n")
                        abacus_bag=int(info2[1])
                    if bhave:
                        btn = driver.find_element_by_id("joint_skill_select_return")
                        TouchActions(driver).tap(btn).perform()
                        self.__wait(1)
                    else:
                        TouchActions(driver).tap(a).perform()
                        sleep(1)
                        btn = driver.find_element_by_id("joint_skill_select")
                        TouchActions(driver).tap(btn).perform()
                    self.__wait(1)
            except:
                btn = driver.find_element_by_id("joint_skill_select_return")
                TouchActions(driver).tap(btn).perform()
                self.__wait(1)
                break
        confirm=driver.find_element_by_class_name("confirm-button")
        if 'enable' in confirm.get_attribute("class"):
            TouchActions(driver).tap(confirm).perform()
            self.__wait(3)
        self.__write_log("算盤術: %d" % (abacus+abacus_bag))
        self.__goto(home_url)
        self.__wait(2)
    def __set_abacus_battle(self):
        driver=self.driver
        self.__goto(deck_url)
        self.__wait(2)
        #切换到奥义标签
        try:
            for i in range(3):
                tap3=driver.find_element_by_xpath("//*[contains(@class,'tabindex3') and contains(@class,'hensei_tab_ng')]")
                if not tap3.is_displayed():
                    break
                TouchActions(driver).tap(tap3).perform()
                self.__wait(1)
        except:
            self.__goto(home_url)
            self.__wait(2)
            return
        #一括補充
        driver.find_element_by_xpath("//input[@value='一括補充']").send_keys(Keys.RETURN)
        sleep(1)
        #持有奥义
        abacus=0
        frames=driver.find_elements_by_class_name("td-select-frame")
        for i in range(len(frames)):
            if '算盤術' in frames[i].text:
                info=(frames[i].text).split("\n")
                abacus=abacus+int(info[2])
        confirm=driver.find_element_by_class_name("confirm-button")
        if 'enable' in confirm.get_attribute("class"):
            TouchActions(driver).tap(confirm).perform()
            self.__wait(3)
        self.__write_log("算盤術: %d" % (abacus))
        self.__goto(home_url)
        self.__wait(2)    
    def __login_process(self):
        driver=self.driver
        self.__goto(game_url)
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
                    self.__goto(home_url)
                    self.__wait(2)
                else:
                    self.__wait(2)
            else:
                break
        self.__write_log("login end")
    def __check_login_button(self):
        driver=self.driver
        btns=driver.find_elements_by_id("login-button")
        if len(btns) <= 0: 
            return False
        else:
            return True        
    def __login_by_password(self):
        driver=self.driver
        self.__goto(login_url)
        self.__wait(2)
        yahoo_btn=driver.find_element_by_xpath("//div[@class='landscapeColumnLayout_right']/section/div[5]/a")
        self.__goto(yahoo_btn.get_attribute('href'))
        self.__wait(2)
        id_input=driver.find_element_by_id("username")
        id_input.send_keys(self.acc+Keys.RETURN)
        self.__wait(3)
        pw_input=driver.find_element_by_id("passwd")
        pw_input.send_keys(self.pw+Keys.RETURN)
        self.__wait(3)
        # self.__goto(game_url)
        # self.__wait(3)
        self.__goto(main_url)
        # self.__wait(3)
        # try:
        #     file=open(self.acc+"_cookies.txt", "w")
        #     for item in driver.get_cookies():
        #         if 'SP' in item['name']:
        #             file.write(item['name']+","+item['value']+'\n')
        # except Exception as e:
        #     self.__write_log("write cookies error :%s" % e)
        # file.close()
        # self.__login_process()
    def __login_by_cookies(self):
        self.__write_log("Login: %s" % self.acc)
        try:
            cookie_file=open(self.acc+"_cookies.txt", "r")
        except:
            self.__write_log("read cookies file error")
            return False
        main_url='http://sp.mbga.jp'
        driver=self.driver
        self.__goto(main_url)
        self.__wait(2)
        for line in cookie_file.readlines():
            ck=line.strip().split(',')
            add_ck={'name':ck[0],'value':ck[1]}
            driver.add_cookie(add_ck)
        cookie_file.close()    
        self.__goto(main_url)
        self.__wait(1)
        return True
    def find_abacus(self,a,b):
        driver=self.driver
        step=0
        hour=0
        try:
            if self.lowfood:
                self.lowfood = False
        except Exception as err:
            self.__write_log(err)
        while True:
            if step==0:
                if self.__check_login_button():
                    self.__login_process()
                    sleep(3)
                if not self.__check_scene('の里'):
                    if not self.__check_notice():
                        self.__goto(home_url)
                        self.__wait(1)
                    else:
                        self.__wait(1)
                else:
                    try:
                        foodtext=driver.find_element_by_xpath("//span[@id='element_food']")
                        food=int(foodtext.text)
                        if food < 1500:
                            self.__change_food()
                        if food < 620:
                            self.lowfood=True
                            return
                    except:
                        pass
                    try:
                        command=driver.find_element_by_class_name('sp_village_command')
                        if '到着' in command.text:
                            sleep(3)
                        else:
                            step = 1
                    except:
                        driver.refresh()
                        self.__wait(1)
            elif step==1:
                self.__check_meishou()
                if not self.__check_scene('全国地図'):
                    self.__goto(map_url)
                    self.__wait(1)
                else:
                    step=2
            elif step==2:
                if self.__get_stay_town() != a and self.__get_stay_town() != b:
                    self.__move_to_town(a)
                    self.__wait(2)
                    step=0
                else:
                    ret = self.__check_abacus()
                    if ret == -1:
                        step = 3
                    else: #bingo
                        self.__kill_enemy(ret)
                        step=0
            elif step==3:
                if self.__get_stay_town() != a:
                    self.__move_to_town(a)
                else:
                    self.__move_to_town(b)
                self.__wait(1)
                step=0
    def star_up(self,a,b):  #升星
        driver=self.driver
        step=0
        while True:
            if step==0:
                if not self.__check_scene('の里'):
                    if not self.__check_notice():
                        self.__goto(home_url)
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
                            sleep(10)
                            self.__wait(2)
                        else:
                            self.__wait(1)
                            step = 1
                    except:
                        driver.refresh()
                        self.__wait(2)
            elif step==1:
                self.__check_meishou()
                if not self.__check_scene('全国地図'):
                    self.__goto(map_url)
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
#                    elif len(enemys[0].find_elements_by_xpath(".//img[contains(@src,'difficulty_mark.png')]")) == 7:
#                        step=3
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
    def check_battle_move(self):
        driver=self.driver
        self.__goto(map_url)
        self.__wait(2)
        if not self.__check_scene('全国地図'):
            return False
        move=driver.find_elements_by_xpath("//div/img[contains(@class,'event_move')]")
        if len(move) < 2:
            return False
        TouchActions(driver).tap(move[0]).perform()
        sleep(1)
        driver.find_element_by_xpath("//input[@value='移動する' and @type='submit']").send_keys(Keys.RETURN)
        sleep(1)
        while self.__check_notice():
            sleep(1)
        return True
    def check_kaseki(self):
        driver=self.driver
        if not self.__check_scene('合戦状況'):
            return
        a=driver.find_elements_by_xpath("//*[contains(text(),'加勢中')]")
        if len(a) > 0:
            return
        else:
            b=driver.find_elements_by_xpath("//a/*[contains(text(),'加勢')]")
            if len(b)<2:
                return
            else:
                TouchActions(driver).tap(b[0]).perform()
                self.__wait(1)
                for i in range(2):
                    btn=driver.find_element_by_id("sp-header-middle-btn")
                    TouchActions(driver).tap(btn).perform()
                    self.__wait(1)
                sleep(2)
    def auto_select_road(self):
        driver=self.driver
        if not self.__check_scene('合戦状況'):
            return 1
        a= driver.find_elements_by_xpath("//img[contains(@src,'powerbalance')]")
        imax=int(a[0].get_attribute('src')[-6:-4])
        index=0
        for i in range(1,len(a)):
            value=int(a[1].get_attribute('src')[-6:-4])
            if value > imax:
                imax=value
                index=i
        return index+1
    def battle(self, road):     #合战
        driver=self.driver
        step=0
        hour=0
        self.check_battle_move()
        while True:
            timenow=time.localtime()
            if hour == 22 and timenow.tm_hour == 23:
                self.login=True
                return
            else:
                hour = timenow.tm_hour
            if step==0:
                if not self.__check_scene('の里'):
                    if not self.__check_notice():
                        self.__goto(home_url)
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
                        elif '到着' in command.text:
                            sleep(10)
                            self.__wait(2)
                        else:
                            self.__wait(1)
                            if road ==0:
                                self.__set_abacus_battle()
                            step = 1
                    except:
                        driver.refresh()
                        self.__wait(1)
            elif step==1:
                if not self.__check_scene('合戦状況'):
                    self.__goto(battle_url)
                    self.__wait(2)
                else:
                    self.check_kaseki()
                    btns=driver.find_elements_by_xpath("//a[contains(@href,'entry_btl')]")
                    if (len(btns) <= 0):
                        btn2s=driver.find_elements_by_xpath("//a[contains(@href,'warId')]")
                        if (len(btn2s) <= 0):
                            step=0
                        else:
                            self.__goto(btn2s[0].get_attribute('href'))
                            self.__wait(2)
                            try:
                                for i in range(3):
                                    btn=driver.find_element_by_id("sp-header-middle-btn")
                                    TouchActions(driver).tap(btn).perform()
                                    self.__wait(3)
                                else:
                                    step=2
                            except:
                                step=0
                    elif (len(btns) == 1):
                        self.__goto(btns[0].get_attribute('href'))
                        self.__wait(2)
                        try:
                            for i in range(3):
                                btn=driver.find_element_by_id("sp-header-middle-btn")
                                TouchActions(driver).tap(btn).perform()
                                self.__wait(3)
                            else:
                                step=2
                        except:
                            step=0
                    else:
                        road_tmp=1
                        if road==0:
                            road_tmp=self.auto_select_road()
                        else:
                            road_tmp=road
                        self.__goto(btns[road_tmp-1].get_attribute('href'))
                        self.__wait(2)
                        try:
                            for i in range(3):
                                btn=driver.find_element_by_id("sp-header-middle-btn")
                                TouchActions(driver).tap(btn).perform()
                                self.__wait(3)
                            else:
                                step=2
                        except:
                            pass
            elif step==2:
                if not self.__check_scene('の里'):
                    if not self.__check_notice():
                        self.__goto(home_url)
                        self.__wait(2)
                    else:
                        self.__wait(2)
                else:
                    food=driver.find_element_by_xpath("//span[@id='element_food']")
                    if (int(food.text)) < 1000:
                        self.__write_log("low food logout")
                        self.lowfood=True
                        return
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
        step=0
        while True:
            if step == 0:                
                if not self.__check_scene("交換所"):
                    self.__goto(trade_url)
                    self.__wait(2)
                else:
                    step=1
            elif step==1:
                if self.noimage:
                    step=2
                else:
                    try:
                        btn=driver.find_element_by_xpath("//img[@class='search_set_img' and @id='%d']/.." % page)
                        TouchActions(driver).tap(btn).perform()
                        self.__wait(2)
                        step=2
                    except:
                        driver.refresh()
                        self.__wait(1)
                        step=0
            elif step==2:
                try:
                    if '登用可能な武将がいません' not in driver.page_source:  
                        buybtns=driver.find_elements_by_xpath("//input[@value='登用']")                    
                        if len(buybtns) > 0:
                            buybtns[0].send_keys(Keys.RETURN)
                            self.__wait(0)
                            btns=driver.find_elements_by_id("neko-alert-dynamic-ok-button")
                            for btn in btns:
                                if btn.is_displayed():
                                    TouchActions(driver).tap(btn).perform()
                                    break
                            self.__wait(2)
                            step=0
                    driver.refresh()
                    self.__wait(2)
                except:
                    self.__goto(trade_url)
                    self.__wait(1)
                    step=0
    def sumo(self,times):
        driver=self.driver
        step=0
        t=0
        while t<times:
            if step==0:
                if not self.__check_scene('の里'):
                    if not self.__check_notice():
                        self.__goto(home_url)
                        self.__wait(2)
                    else:
                        self.__wait(2)
                else:
                    try:
                        command=driver.find_element_by_class_name('sp_village_command')
                        if '帰還' in command.text:
                            sleep(3)
                        elif '移動' in command.text:
                            sleep(3)
                        else:
                            self.__wait(1)
                            step = 1
                    except:
                        driver.refresh()
                        self.__wait(1)
            elif step==1:
                try:
                    a=driver.find_element_by_xpath("//area[contains(@title,'里門')]")
                    TouchActions(driver).tap(a).perform()
                    self.__wait(2)
                    if self.__check_scene('里門'):
                        step=2
                    else:
                        step=0
                except:
                    step=0
            elif step==2:
                for i in range(3):
                    btn=driver.find_element_by_id("sp-header-middle-btn")
                    TouchActions(driver).tap(btn).perform()
                    sleep(2)
                t=t+1
                self.__goto(home_url)
                sleep(2)
                step=0
    def task(self,task):
        #self.__start_driver(noimage=False)
        #self.__write_log("login start")
        #self.__login_by_password()
        # if not self.__login_by_cookies():
        #     self.__login_by_password()        
        # self.__login_process()
        # self.__stop_driver()
        # sleep(5)
        # self.__start_driver(noimage=True)
        #self.__login_by_cookies()
        #self.__goto(home_url)
        #self.__wait(1)
        self.quest=task
        self.__write_log("start task:[%s]" % self.quest)
        quest=((self.quest).strip()).split("-")
        self.__start_driver()
        while True:
            if quest[0] == 'b':
                self.__login_process()
                self.__goto(home_url)
                self.__wait(1)
                if self.lowfood:
                    self.__stop_driver()
                    return
                self.battle(int(quest[1]))
            elif quest[0] == 's':
                self.__goto(home_url)
                self.__wait(1)
                self.star_up(int(quest[1]),int(quest[2]))
            elif quest[0] == 'fa':
                self.__goto(home_url)
                self.__wait(1)
                if self.lowfood:
                    sleep(3600)
                    self.__goto(home_url)
                self.find_abacus(9,10)
            elif quest[0] == 'buy':
                self.buy(int(quest[1]))
    def login_first(self):
        self.__start_driver(noimage=False)
        print("login %s" % self.acc)
        sleep(10)
        self.__goto(login_url)
        sleep(20)
        self.__goto(game_url)
        self.__wait(2)
        self.__stop_driver()
