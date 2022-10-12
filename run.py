import time,os,string,sys,random,json
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from datetime import datetime
# exit 0 cambio account
# exit 1 streaming error
# exit 100 wrong account, delete

troops = {}
risorse = {}
coda = {}
building_queue = []
building_level = []
hero_attack = []

def handleAttack(driver):
    date_time_str = '10/09/22 05:50:19'

    date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')
    attacks = len(driver.find_elements(By.XPATH,"//*[@class='att1']"))
    if attacks == 0:
        print("NO ATTACK")
    else:
        print("ATTACCO IN CORSO",datetime.now())
        if len(driver.window_handles) == 1 and datetime.now() > date_time_obj:
            driver.execute_script('''window.open("https://www.youtube.com/watch?v=zdb3SaUver0","_blank");''')
        

def handleGrano(driver):
    if len(driver.window_handles) == 1:
        driver.execute_script('''window.open("https://www.youtube.com/watch?v=zdb3SaUver0","_blank");''')
        



def main():
    driver=get_chromedriver()
    login(driver)
    giro = 0
    while 1:
        #checkAttivo(driver)
        if giro % 3 == 0:
            overview(driver)
        #continue
        print(datetime.now())
        for village in ["17956","23257","26470"]:
            #checkAttivo(driver)

            global troops
            global risorse
            global coda
            global building_queue
            global building_level
            troops = {}
            risorse = {}
            coda = {}
            building_queue = []
            building_level = []
            print("VILLAGE",village)
            driver.get(f"https://ts31.x3.international.travian.com/dorf2.php?newdid={village}")

            parse_risorse(driver)


            if village == "17956":
                if risorse["q_grano"] <= 2:
                    handleGrano(driver)

            #parse_coda(driver)
            
            #fill_farm(driver,village)
            
            try:
                #checkAttivo(driver)
                farm(driver,village)
            except Exception as e:
                print(e)
                pass
            if village == "23257":
                npc_grano(driver,village,31)
                
                hero(driver)

                #raidStats(driver)
            # else:
            #     npc_grano_negativo(driver,village,22)
        giro += 1
        r = random.randint(90, 250)
        c = r
        for x in range(0,r):
            print(c)
            time.sleep(1)
            c -= 1
    driver.quit()

def checkAttivo(driver):
    try:
        while 1:
            attivo = int((driver.find_element(By.XPATH,"//*[@id='sidebarBoxLinklist']/div[2]/ul/li[6]/a/span").text).strip().split("=")[1])
            print("ATTIVO, ",attivo)
            if attivo == 1:
                return
            driver.find_element(By.XPATH,"//a[@accesskey='2']").click()
            time.sleep(60)
            driver.refresh()
    except:
        return

def raidStats(driver):
    driver.get("https://ts31.x3.international.travian.com/statistics/player?idSub=3")
    time.sleep(2)

    mio_raid = str(driver.find_element(By.XPATH,f"//*[@id='top10_raiders']/tbody/tr[12]/td[4]").text)
    top_10_raid = str(driver.find_element(By.XPATH,f"//*[@id='top10_raiders']/tbody/tr[10]/td[4]").text)

    stats = "timestamp: "+datetime.now().strftime("%m/%d/%Y, %H:%M:%S")+",io: "+mio_raid+",top10: "+top_10_raid+"\n"

    with open('raid', 'a+') as json_file:
        json_file.write(stats)

def npc_grano_negativo(driver,village,aid):

    if risorse["q_grano"] >= 95 and risorse["q_media"] < 70:
        if "dorf2" not in driver.current_url:
            driver.find_element(By.XPATH,"//a[@accesskey='2']").click()
        driver.get(f"https://ts31.x3.international.travian.com/dorf2.php?newdid={village}")
        time.sleep(2)
        driver.find_element(By.XPATH,f"//*[@data-aid='{aid}']").click()
        time.sleep(3)
        driver.find_element(By.XPATH,"//*[@value='Scambio risorse']").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//*[@value='Distribuisci le risorse rimanenti.']").click()
        time.sleep(4)
        driver.find_element(By.XPATH,"//*[@name='desired3']").clear()
        time.sleep(1)
        driver.find_element(By.XPATH,"//*[@name='desired3']").send_keys("0")
        time.sleep(3)
        driver.find_element(By.XPATH,"//*[@value='Distribuisci le risorse rimanenti.']").click()
        time.sleep(4)
        driver.find_element(By.XPATH,"//*[@value='Scambia']").click()
        time.sleep(2)



def npc_grano(driver,village,aid):

    if risorse["q_grano"] >= 95 and risorse["q_media"] < 70:
        if "dorf2" not in driver.current_url:
            driver.find_element(By.XPATH,"//a[@accesskey='2']").click()
        driver.get(f"https://ts31.x3.international.travian.com/dorf2.php?newdid={village}")
        time.sleep(2)
        driver.find_element(By.XPATH,f"//*[@data-aid='{aid}']").click()
        time.sleep(3)
        driver.find_element(By.XPATH,"//*[@value='Scambio risorse']").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//*[@value='Distribuisci le risorse rimanenti.']").click()
        time.sleep(4)
        driver.find_element(By.XPATH,"//*[@name='desired3']").clear()
        time.sleep(1)
        driver.find_element(By.XPATH,"//*[@name='desired3']").send_keys("0")
        time.sleep(3)
        driver.find_element(By.XPATH,"//*[@value='Distribuisci le risorse rimanenti.']").click()
        time.sleep(4)
        driver.find_element(By.XPATH,"//*[@name='desired3']").clear()
        time.sleep(1)
        driver.find_element(By.XPATH,"//*[@name='desired3']").send_keys("0")
        time.sleep(3)
        driver.find_element(By.XPATH,"//*[@value='Distribuisci le risorse rimanenti.']").click()
        time.sleep(4)
        driver.find_element(By.XPATH,"//*[@value='Scambia']").click()
        time.sleep(2)


def wait(driver,xpath,seconds,click=True):
    WebDriverWait(driver, seconds).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    if click==True:
        driver.find_element(By.XPATH,xpath).click()


def get_chromedriver():
    chrome_options = Options()
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--no-default-browser-check')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-default-apps')
    chrome_options.add_argument("--user-data-dir=/home/big0/.config/google-chromeTrav")
    # capa = DesiredCapabilities.CHROME
    # capa["pageLoadStrategy"] = "none"
    driver = webdriver.Chrome(executable_path="./chromedriver",chrome_options=chrome_options)
    driver.set_window_size(1980,1020)
    return driver

def fill_farm(driver,village):
    driver.find_element(By.XPATH,"//*[@id='sidebarBoxLinklist']/div[2]/ul/li[1]/a/span").click()
    time.sleep(8)
    my_farm_list = driver.find_element(By.XPATH,f"//*[@data-listid='3281']")

    with open("farmlist.txt") as fppp:
        Lines = fppp.readlines()
        print(Lines)
        for line in Lines:
            
            try:
                print(line)
                info = json.loads(line.strip())
                print(info)

                exist = driver.find_elements(By.XPATH,f"//*[@href='/position_details.php?x={info['x']}&y={info['y']}']")
                if len(exist) > 0:
                    print("FARM GIA INSERITA")
                    continue

                my_farm_list.find_element(By.XPATH,f".//*[@class='addNewSlot']").click()
                time.sleep(1)
                driver.find_element(By.XPATH,f"//*[@id='xCoordInput']").clear()
                driver.find_element(By.XPATH,f"//*[@id='xCoordInput']").send_keys(info["x"])
                driver.find_element(By.XPATH,f"//*[@id='yCoordInput']").clear()
                driver.find_element(By.XPATH,f"//*[@id='yCoordInput']").send_keys(info["y"])
                driver.find_element(By.XPATH,f"//*[@id='save']").click()
                time.sleep(1)
                driver.find_element(By.XPATH,f"//*[@class='green dialogButtonOk ok textButtonV1']").click()
                time.sleep(5)
            except:
                continue



def overview(driver):
    start_troops(driver)

    for x in range(0,1):
        driver.get(f"https://ts31.x3.international.travian.com/dorf2.php?newdid=17956")
        if "statistics" not in driver.current_url:
            driver.find_element(By.XPATH,"//*[@id='sidebarBoxLinklist']/div[2]/ul/li[11]/a/span").click()
            time.sleep(1)
        handleAttack(driver)

        print("SLEEPING")

def ss(driver):
    driver.get(f"https://ts31.x3.international.travian.com/dorf2.php?newdid=17956")
    time.sleep(1)
    parse_risorse(driver)
    
    if "statistics" not in driver.current_url:
        driver.find_element(By.XPATH,"//*[@id='sidebarBoxLinklist']/div[2]/ul/li[11]/a/span").click()
        time.sleep(1)
    time.sleep(3)
    roma = driver.find_element(By.XPATH,"//*[@id='overview']/tbody/tr[7]")

    

    try:
        asce_in_coda = int(roma.find_element(By.XPATH,".//*[@href='/build.php?newdid=19087&gid=19']/img").get_attribute("alt").split("x ")[0])
    except:
        asce_in_coda = 0
    
    try:
        asce_in_coda_grande = int(roma.find_element(By.XPATH,".//*[@href='/build.php?newdid=19087&gid=29']/img").get_attribute("alt").split("x ")[0])
    except:
        asce_in_coda_grande = 0

    try:
        tk_in_coda = int(roma.find_element(By.XPATH,".//*[@href='/build.php?newdid=19087&gid=20']/img").get_attribute("alt").split("x ")[0])
    except:
        tk_in_coda = 0

    try:
        tk_in_coda_grande = int(roma.find_element(By.XPATH,".//*[@href='/build.php?newdid=19087&gid=30']/img").get_attribute("alt").split("x ")[0])
    except:
        tk_in_coda_grande = 0

    try:
        cata_in_coda = int(roma.find_element(By.XPATH,".//*[@class='unit u18']").get_attribute("alt").split("x ")[0])
    except:
        cata_in_coda = 0

    try:
        arieti_in_coda = int(roma.find_element(By.XPATH,".//*[@class='unit u17']").get_attribute("alt").split("x ")[0])
    except:
        arieti_in_coda = 0

    ASCE_SEC = 52/60
    ASCE_SEC_GRANDE = 52/60
    TK_SEC = 128/60
    TK_SEC_GRANDE = 128/60
    CATA_SEC = 389/60
    ARIETI_SEC = 182/60
    asce_time = (asce_in_coda * ASCE_SEC)
    asce_time_grande = (asce_in_coda_grande * ASCE_SEC_GRANDE)

    tk_time = (tk_in_coda * TK_SEC)
    tk_time_grande = (tk_in_coda_grande * TK_SEC_GRANDE)
    cata_time = (cata_in_coda * CATA_SEC)
    arieti_time = (arieti_in_coda * ARIETI_SEC)
    print("ASCE:",asce_in_coda,asce_time)
    print("ASCE G:",asce_in_coda_grande,asce_time_grande)
    print("TK:",tk_in_coda,tk_time)
    print("TK G:",tk_in_coda_grande,tk_time_grande)
    print("CATA:",cata_in_coda,cata_time)
    print("ARIETI:",arieti_in_coda,arieti_time)


    CODA_MIN = 30

    if risorse["grano"] < 30000:
        CODA_MIN = 0


    code = [asce_time,tk_time,asce_time_grande,tk_time_grande,arieti_time]
    print(code)
    index = code.index(min(code))
    print("MINIMO INDEX:",index)

    if index == 0:
        parse_risorse(driver)
        if risorse["q_media"] > 85:
            CODA_MIN = asce_time + 150
        if asce_time < CODA_MIN:
            da_incodare = int((CODA_MIN+30 - asce_time)//ASCE_SEC)
            print(da_incodare)
            truppav2(driver,"asce",da_incodare,"19087",32)
    elif index == 1:
        parse_risorse(driver)
        if risorse["q_media"] > 85:
            CODA_MIN = tk_time + 150
        
        if tk_time < CODA_MIN:
            da_incodare = int((CODA_MIN+30 - tk_time)//TK_SEC)
            print(da_incodare)
            truppav2(driver,"tk",da_incodare,"19087",33)
    elif index == 2:
        parse_risorse(driver)
        if risorse["q_media"] > 85:
            CODA_MIN = asce_time_grande + 150
        

        if asce_time_grande < CODA_MIN:
            da_incodare = int((CODA_MIN+30 - asce_time_grande)//ASCE_SEC_GRANDE)
            print(da_incodare)
            truppav2(driver,"asceg",da_incodare,"19087",28)
    elif index == 3:
        parse_risorse(driver)
        if risorse["q_media"] > 85:
            CODA_MIN = tk_time_grande + 150
        
        if tk_time_grande < CODA_MIN:
            da_incodare = int((CODA_MIN+30 - tk_time_grande)//TK_SEC_GRANDE)
            print(da_incodare)
            truppav2(driver,"tkg",da_incodare,"19087",34)
    elif index == 4:
        parse_risorse(driver)
        if risorse["q_media"] > 85:
            CODA_MIN = cata_time + 150
        if cata_time < CODA_MIN:
            da_incodare = int((CODA_MIN+30 - cata_time)//CATA_SEC)
            print(da_incodare)
            truppav2(driver,"cata",da_incodare,"19087",36)

        # parse_risorse(driver)
        # if risorse["q_media"] > 85:
        #     CODA_MIN = arieti_time + 150
        # if arieti_time < CODA_MIN:
        #     da_incodare = int((CODA_MIN+30 - arieti_time)//ARIETI_SEC)
        #     print(da_incodare)
        #     truppav2(driver,"arieti",da_incodare,"19087",36)





def amsterdam_troops(driver):
    driver.get(f"https://ts31.x3.international.travian.com/dorf2.php?newdid=27117")
    time.sleep(1)
    parse_risorse(driver)
    
    if "statistics" not in driver.current_url:
        driver.find_element(By.XPATH,"//*[@id='sidebarBoxLinklist']/div[2]/ul/li[4]/a/span").click()
        time.sleep(1)
    time.sleep(3)
    amsterdam = driver.find_element(By.XPATH,"//*[@id='overview']/tbody/tr[9]")

    

    try:
        mazze_in_coda = int(amsterdam.find_element(By.XPATH,".//*[@href='/build.php?newdid=27117&gid=19']/img").get_attribute("alt").split("x ")[0])
    except:
        mazze_in_coda = 0
    
    try:
        mazze_in_coda_grande = int(amsterdam.find_element(By.XPATH,".//*[@href='/build.php?newdid=27117&gid=29']/img").get_attribute("alt").split("x ")[0])
    except:
        mazze_in_coda_grande = 0

    try:
        tk_in_coda = int(amsterdam.find_element(By.XPATH,".//*[@href='/build.php?newdid=27117&gid=20']/img").get_attribute("alt").split("x ")[0])
    except:
        tk_in_coda = 0

    try:
        tk_in_coda_grande = int(amsterdam.find_element(By.XPATH,".//*[@href='/build.php?newdid=27117&gid=30']/img").get_attribute("alt").split("x ")[0])
    except:
        tk_in_coda_grande = 0

    try:
        cata_in_coda = int(amsterdam.find_element(By.XPATH,".//*[@class='unit u18']").get_attribute("alt").split("x ")[0])
    except:
        cata_in_coda = 0

    try:
        arieti_in_coda = int(amsterdam.find_element(By.XPATH,".//*[@class='unit u17']").get_attribute("alt").split("x ")[0])
    except:
        arieti_in_coda = 0

    MAZZE_SEC = 13/60
    MAZZE_SEC_GRANDE = 13/60
    TK_SEC = 54/60
    TK_SEC_GRANDE = 54/60
    CATA_SEC = 389/60
    ARIETI_SEC = 91/60
    mazze_time = (mazze_in_coda * MAZZE_SEC)
    mazze_time_grande = (mazze_in_coda_grande * MAZZE_SEC_GRANDE)

    tk_time = (tk_in_coda * TK_SEC)
    tk_time_grande = (tk_in_coda_grande * TK_SEC_GRANDE)
    cata_time = (cata_in_coda * CATA_SEC)
    arieti_time = (arieti_in_coda * ARIETI_SEC)
    print("MAZZE:",mazze_in_coda,mazze_time)
    print("MAZZE G:",mazze_in_coda_grande,mazze_time_grande)
    print("TK:",tk_in_coda,tk_time)
    print("TK G:",tk_in_coda_grande,tk_time_grande)
    print("CATA:",cata_in_coda,cata_time)
    print("ARIETI:",arieti_in_coda,arieti_time)


    CODA_MIN = 100

    if risorse["grano"] < 100000:
        CODA_MIN = 0
        return

    code = [mazze_time,tk_time,mazze_time_grande,tk_time_grande,arieti_time]

    index = code.index(min(code))
    print("MINIMO INDEX:",index)
    if index == 0:
        parse_risorse(driver)
        # if risorse["q_media"] > 85:
        #     CODA_MIN = mazze_time + 150
        
        # if mazze_time < CODA_MIN:
        #     da_incodare = int((CODA_MIN+30 - mazze_time)//MAZZE_SEC)
        #     print(da_incodare)
        #     truppav2(driver,"mazze",da_incodare,"27117",32)

    elif index == 1:
        parse_risorse(driver)
        # if risorse["q_media"] > 85:
        #     CODA_MIN = tk_time + 150
        
        # if tk_time < CODA_MIN:
        #     da_incodare = int((CODA_MIN+30 - tk_time)//TK_SEC)
        #     print(da_incodare)
        #     truppav2(driver,"tk",da_incodare,"27117",33)

    elif index == 2:
        parse_risorse(driver)
        if risorse["q_media"] > 85:
            CODA_MIN = mazze_time_grande + 150

        if mazze_time_grande < CODA_MIN:
            da_incodare = int((CODA_MIN+30 - mazze_time_grande)//MAZZE_SEC_GRANDE)
            print(da_incodare)
            truppav2(driver,"mazzeg",da_incodare,"27117",27)

    elif index == 3:
        parse_risorse(driver)
        if risorse["q_media"] > 85:
            CODA_MIN = tk_time_grande + 150
        
        if tk_time_grande < CODA_MIN:
            da_incodare = int((CODA_MIN+30 - tk_time_grande)//TK_SEC_GRANDE)
            print(da_incodare)
            truppav2(driver,"tkg",da_incodare,"27117",30)
        
    # elif index == 4:
    #     parse_risorse(driver)
    #     if risorse["q_media"] > 85:
    #         CODA_MIN = arieti_time + 150
    #     if arieti_time < CODA_MIN:
    #         print("DEVO FARE ARIETI")
    #         da_incodare = int((CODA_MIN+20 - arieti_time)//ARIETI_SEC)
    #         print(da_incodare)
    #         truppav2(driver,"arieti",da_incodare,"27117",37)

    # if cata_time < CODA_MIN:
    #     da_incodare = int((CODA_MIN+20 - cata_time)//CATA_SEC)
    #     print(da_incodare)
    #     truppav2(driver,"cata",da_incodare,"27117",37)



def start_troops(driver):

    driver.get(f"https://ts31.x3.international.travian.com/dorf2.php?newdid=17956")
    time.sleep(1)
    
    parse_risorse(driver)
    
    if "statistics" not in driver.current_url:
        driver.find_element(By.XPATH,"//*[@id='sidebarBoxLinklist']/div[2]/ul/li[11]/a/span").click()
        time.sleep(1)
    time.sleep(3)
    dracarys = driver.find_element(By.XPATH,"//*[@id='overview']/tbody/tr[1]")

    

    try:
        mazze_in_coda = int(dracarys.find_element(By.XPATH,".//*[@class='unit u11']").get_attribute("alt").split("x ")[0])
    except:
        mazze_in_coda = 0

    try:
        mazze_in_coda_grande = int(dracarys.find_element(By.XPATH,".//*[@href='/build.php?newdid=17956&gid=29']/img").get_attribute("alt").split("x ")[0])
    except:
        mazze_in_coda_grande = 0
    
    try:
        tk_in_coda = int(dracarys.find_element(By.XPATH,".//*[@class='unit u16']").get_attribute("alt").split("x ")[0])
    except:
        tk_in_coda = 0

    try:
        tk_in_coda_grande = int(dracarys.find_element(By.XPATH,".//*[@href='/build.php?newdid=17956&gid=30']/img").get_attribute("alt").split("x ")[0])
    except:
        tk_in_coda_grande = 0

    try:
        cata_in_coda = int(dracarys.find_element(By.XPATH,".//*[@class='unit u18']").get_attribute("alt").split("x ")[0])
    except:
        cata_in_coda = 0

    try:
        arieti_in_coda = int(dracarys.find_element(By.XPATH,".//*[@class='unit u17']").get_attribute("alt").split("x ")[0])
    except:
        arieti_in_coda = 0


    MAZZE_SEC = 32/60
    MAZZE_SEC_GRANDE = 60/60
    TK_SEC = 121/60
    TK_SEC_GRANDE = 270/60
    CATA_SEC = 389/60
    ARIETI_SEC = 185/60
    mazze_time = (mazze_in_coda * MAZZE_SEC)
    mazze_time_grande = (mazze_in_coda_grande * MAZZE_SEC_GRANDE)

    tk_time = (tk_in_coda * TK_SEC)
    tk_time_grande = (tk_in_coda_grande * TK_SEC_GRANDE)
    cata_time = (cata_in_coda * CATA_SEC)
    arieti_time = (arieti_in_coda * ARIETI_SEC)
    print("MAZZE:",mazze_in_coda,mazze_time)
    print("MAZZE G:",mazze_in_coda_grande,mazze_time_grande)
    print("TK:",tk_in_coda,tk_time)
    print("TK G:",tk_in_coda_grande,tk_time_grande)
    print("CATA:",cata_in_coda,cata_time)
    print("ARIETI:",arieti_in_coda,arieti_time)

    CODA_MIN = 25

    if risorse["grano"] < 5000:
        CODA_MIN = 0
        return

    code = [mazze_time,tk_time,mazze_time_grande,tk_time_grande,arieti_time]

    index = code.index(min(code))
    print("MINIMO INDEX:",index)
    if index == 0:
        parse_risorse(driver)
        if risorse["q_media"] > 85:
            CODA_MIN = mazze_time + 150
        
        if mazze_time < CODA_MIN:
            da_incodare = int((CODA_MIN+30 - mazze_time)//MAZZE_SEC)
            print(da_incodare)
            truppav2(driver,"mazze",da_incodare,"17956",21)

    elif index == 1:
        parse_risorse(driver)
        if risorse["q_media"] > 85:
            CODA_MIN = tk_time + 150
        
        if tk_time < CODA_MIN:
            da_incodare = int((CODA_MIN+30 - tk_time)//TK_SEC)
            print(da_incodare)
            truppav2(driver,"tk",da_incodare,"17956",23)

    elif index == 2:
        parse_risorse(driver)
        if risorse["q_media"] > 85:
            CODA_MIN = mazze_time_grande + 150

        if mazze_time_grande < CODA_MIN:
            da_incodare = int((CODA_MIN+30 - mazze_time_grande)//MAZZE_SEC_GRANDE)
            print(da_incodare)
            truppav2(driver,"mazzeg",da_incodare,"17956",32)

    elif index == 3:
        parse_risorse(driver)
        if risorse["q_media"] > 85:
            CODA_MIN = tk_time_grande + 150
        
        if tk_time_grande < CODA_MIN:
            da_incodare = int((CODA_MIN+30 - tk_time_grande)//TK_SEC_GRANDE)
            print(da_incodare)
            truppav2(driver,"tkg",da_incodare,"17956",25)
        
    elif index == 4:
        parse_risorse(driver)
        if risorse["q_media"] > 85:
            CODA_MIN = arieti_time + 150
        if arieti_time < CODA_MIN:
            print("DEVO FARE ARIETI")
            da_incodare = int((CODA_MIN+20 - arieti_time)//ARIETI_SEC)
            print(da_incodare)
            truppav2(driver,"arieti",da_incodare,"17956",24)

def attack_oasis(driver):

    if "Cavalieri Teutonici" in troops:
        number_of_tk = troops["Cavalieri Teutonici"]

        if number_of_tk <= 2000:
            return

        with open('oasi.json', 'r') as json_file:
            oasis = json.load(json_file)
        random.shuffle(oasis)
        for line in oasis:
            try:
                print("TK LEFT=",number_of_tk)
                if number_of_tk <= 100:
                    break
                belve_oasi = {}

                if line["last_time"] != "":
                    if datetime.now() < (datetime.strptime(line["last_time"], "%m/%d/%Y, %H:%M:%S") + timedelta(hours=4)):
                        continue

                driver.get(f"https://ts31.x3.international.travian.com/position_details.php?x={line['x']}&y={line['y']}")
                time.sleep(2)
                belve = driver.find_elements(By.XPATH,"//*[@id='troop_info']/tbody/tr")
                for b in belve:
                    try:
                        info = b.text
                        n = int(info.split(" ")[0])
                        t = info.split(" ")[1]
                        if "Top" in t:
                            t2 = "u1"
                        elif "Ragn" in t:
                            t2 = "u2"
                        elif "Serpent" in t:
                            t2 = "u3"
                        elif "Pipistrell" in t:
                            t2 = "u4"
                        elif "Cinghial" in t:
                            t2 = "u5"
                        elif "Lup" in t:
                            t2 = "u6"
                        elif "Ors" in t:
                            t2 = "u7"
                        elif "Coccodrill" in t:
                            t2 = "u8"
                        elif "Tigr" in t:
                            t2 = "u9"
                        elif "Elefant" in t:
                            t2 = "u10"
                        belve_oasi[t2] = n
                    except:
                        pass
                
                if len(belve_oasi) > 0:
                    print("BELVE:",belve_oasi)
                    number_of_belve = 0
                    for kk in belve_oasi:
                        number_of_belve += belve_oasi[kk]
                    
                    if number_of_belve < 8:
                        line["last_time"] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                        with open('oasi.json', 'w') as json_file:
                            json.dump(oasis, json_file)
                        continue

                    c = 0
                    while 1:
                        tk = 50 + (50*c)
                        if tk > 1100 or tk > number_of_tk:
                            print("TOO MUCH")
                            line["last_time"] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                            with open('oasi.json', 'w') as json_file:
                                json.dump(oasis, json_file)
                            break
                        po_loss = simulator(**belve_oasi,o6=tk)

                        perdite = round(tk * po_loss)
                        print("PERDITE:",perdite)
                        if perdite <= 1:
                            tk += 100
                            print(f"!!!OASI DA ATTACCARE CON {tk} TK!!!")
                            driver.find_element(By.XPATH,"//*[contains(text(), 'Attacco oasi libera')]").click()
                            time.sleep(2)
                            driver.find_element(By.XPATH,"//*[@name='troop[t6]']").clear()
                            driver.find_element(By.XPATH,"//*[@name='troop[t6]']").send_keys(tk)
                            driver.find_element(By.XPATH,"//*[@value='ok']").click()
                            time.sleep(2)

                            tk_effettivi = int(driver.find_element(By.XPATH,"//*[@id='troopSendForm']/table[2]/tbody[2]/tr/td[6]").text)
                            if tk_effettivi != tk:
                                break
                            driver.find_element(By.XPATH,"//*[@id='c']").click()
                            print("LANCIATO")
                            line["last_time"] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                            number_of_tk -= tk

                            with open('oasi.json', 'w') as json_file:
                                json.dump(oasis, json_file)
                            break
                        else:
                            i = 1
                            if c > 6:
                                i = 2

                            c += i
                        
                        time.sleep(1)
                time.sleep(3)
            except Exception as e:
                print(e)
                continue

    driver.get("https://ts31.x3.international.travian.com/dorf2.php")
  

            



def load_building_queue():
    global building_queue
    with open('build_queue.json', 'r') as f:
        building_queue = json.load(f)
        print("BUILDING QUEUE:",building_queue)

def login(driver):

    driver.get("https://ts31.x3.international.travian.com/dorf2.php")
    time.sleep(3)

    if "dorf2" in driver.current_url:
        return True

    driver.get("https://ts31.x3.international.travian.com")
    
    #wait(driver,"//form[@name='login']",20,False)
    driver.find_element(By.XPATH,"//input[@name='name']").send_keys("YAMOSHI")
    time.sleep(1)
    driver.find_element(By.XPATH,"//input[@name='password']").send_keys("Teonabbo10")
    time.sleep(2)
    driver.find_element(By.XPATH,"//button[@value='Login']").click()
    time.sleep(3)
    if "dorf1" in driver.current_url:
        return True
    return False

def parse_troops(driver):
    if "dorf1" not in driver.current_url:
        driver.find_element(By.XPATH,"//a[@accesskey='1']").click()
    t = driver.find_element(By.XPATH,"//*[@id='troops']/tbody")
    try:
        for tr in t.find_elements(By.XPATH,".//tr"):
            td = tr.find_elements(By.XPATH,".//td")[::-1]
            troops[td[0].text] = int(td[1].text)
    except:
        pass
    print(troops)
    return troops

def send_farmv2_am(driver,troops,village,s):
    driver.find_element(By.XPATH,"//*[@id='sidebarBoxLinklist']/div[2]/ul/li[1]/a/span").click()
    time.sleep(8)
    my_farm_list = driver.find_element(By.XPATH,f"//*[@data-did='{village}' and @class='villageWrapper']")
    
    farm_lists = my_farm_list.find_elements(By.XPATH,f".//*[@class='raidList']")[s[0]::]
    #random.shuffle(farm_lists)
    for f in farm_lists:
        gialli = f.find_elements(By.XPATH,".//*[@alt='Perso come attaccante.' or @alt='Vinto come attaccante subendo perdite.']")
        if len(gialli) > 0:
            for g in gialli:
                row = g.find_element(By.XPATH,"./../../..")
                if row.get_attribute("class") != "slotRow slotInactive":
                    row.find_element(By.XPATH,".//*[@class='edit']").click()
                    time.sleep(4)
                    driver.find_element(By.XPATH,"//*[@class='deactivateTarget']").click()
                    time.sleep(4)
                    driver.find_element(By.XPATH,"//*[@value='Salva']").click()
                    time.sleep(1)

        time.sleep(3)
        f.find_element(By.XPATH,".//*[@class='markAll check']").click()
        time.sleep(2)
        f.find_element(By.XPATH,".//*[@value='Avvia']").click()


def send_farmv2_am_tk(driver,troops,village,s):
    driver.find_element(By.XPATH,"//*[@id='sidebarBoxLinklist']/div[2]/ul/li[1]/a/span").click()
    time.sleep(8)
    my_farm_list = driver.find_element(By.XPATH,f"//*[@data-did='{village}' and @class='villageWrapper']")
    
    farm_lists = my_farm_list.find_elements(By.XPATH,f".//*[@class='raidList']")[s[0]:s[1]]
    #random.shuffle(farm_lists)
    for f in farm_lists:
        gialli = f.find_elements(By.XPATH,".//*[@alt='Perso come attaccante.' or @alt='Vinto come attaccante subendo perdite.']")
        if len(gialli) > 0:
            for g in gialli:
                row = g.find_element(By.XPATH,"./../../..")
                if row.get_attribute("class") != "slotRow slotInactive":
                    row.find_element(By.XPATH,".//*[@class='edit']").click()
                    time.sleep(4)
                    driver.find_element(By.XPATH,"//*[@class='deactivateTarget']").click()
                    time.sleep(4)
                    driver.find_element(By.XPATH,"//*[@value='Salva']").click()
                    time.sleep(1)

        time.sleep(3)
        f.find_element(By.XPATH,".//*[@class='markAll check']").click()
        time.sleep(2)
        f.find_element(By.XPATH,".//*[@value='Avvia']").click()



def send_farmv2(driver,troops,village,s):
    driver.find_element(By.XPATH,"//*[@id='sidebarBoxLinklist']/div[2]/ul/li[1]/a/span").click()
    time.sleep(8)
    my_farm_list = driver.find_element(By.XPATH,f"//*[@data-did='{village}' and @class='villageWrapper']")
    
    farm_lists = my_farm_list.find_elements(By.XPATH,f".//*[@class='raidList']")[s[0]::]
    #random.shuffle(farm_lists)
    for f in farm_lists:
        try:
            gialli = f.find_elements(By.XPATH,".//*[@alt='Perso come attaccante.' or @alt='Vinto come attaccante subendo perdite.']")
            if len(gialli) > 0:
                for g in gialli:
                    row = g.find_element(By.XPATH,"./../../..")
                    if row.get_attribute("class") != "slotRow slotInactive":
                        row.find_element(By.XPATH,".//*[@class='edit']").click()
                        time.sleep(4)
                        driver.find_element(By.XPATH,"//*[@class='deactivateTarget']").click()
                        time.sleep(4)
                        driver.find_element(By.XPATH,"//*[@value='Salva']").click()
                        time.sleep(1)
            print("OKOKK")
            time.sleep(3)
            f.find_element(By.XPATH,".//*[@class='markAll check']").click()
        except:
            pass
        

        
        time.sleep(2)
        f.find_element(By.XPATH,".//*[@value='Avvia']").click()



def send_farmv2_tk(driver,troops,village,s):
    driver.find_element(By.XPATH,"//*[@id='sidebarBoxLinklist']/div[2]/ul/li[1]/a/span").click()
    time.sleep(8)
    my_farm_list = driver.find_element(By.XPATH,f"//*[@data-did='{village}' and @class='villageWrapper']")
    
    farm_lists = my_farm_list.find_elements(By.XPATH,f".//*[@class='raidList']")[s[0]:s[1]]
    #random.shuffle(farm_lists)
    for f in farm_lists:
        gialli = f.find_elements(By.XPATH,".//*[@alt='Perso come attaccante.' or @alt='Vinto come attaccante subendo perdite.']")
        if len(gialli) > 0:
            for g in gialli:
                row = g.find_element(By.XPATH,"./../../..")
                if row.get_attribute("class") != "slotRow slotInactive":
                    row.find_element(By.XPATH,".//*[@class='edit']").click()
                    time.sleep(4)
                    driver.find_element(By.XPATH,"//*[@class='deactivateTarget']").click()
                    time.sleep(4)
                    driver.find_element(By.XPATH,"//*[@value='Salva']").click()
                    time.sleep(1)

        time.sleep(3)
        f.find_element(By.XPATH,".//*[@class='markAll check']").click()
        time.sleep(2)
        f.find_element(By.XPATH,".//*[@value='Avvia']").click()


def send_farm(driver,troops,village):

    driver.find_element(By.XPATH,"//*[@id='sidebarBoxLinklist']/div[2]/ul/li[1]/a/span").click()
    time.sleep(5)
    my_farm_list = driver.find_element(By.XPATH,f"//*[@data-did='{village}' and @class='villageWrapper']")
    
    farm_lists = my_farm_list.find_elements(By.XPATH,f".//*[@class='raidList']")

    n_attack = min(100*len(farm_lists),troops//2)
    print("NUMERO ATT",n_attack)

    c = 0
    for f in farm_lists[::-1]:
        time.sleep(5)
        f.find_element(By.XPATH,".//*[@class='sorting']").click()
        time.sleep(1)
        f.find_elements(By.XPATH,".//*[@class='sortOption ']")[1].click()
        time.sleep(2)
        f.find_element(By.XPATH,".//*[@class='sorting']").click()
        time.sleep(1)
        f.find_elements(By.XPATH,".//*[@class='sortOption active']")[0].click()
        f.find_elements(By.XPATH,".//*[@class='distance sortable']")[0].click()

        time.sleep(3)

        slot = f.find_elements(By.XPATH,".//*[@class='slotRow slotActive']")
        slot_checked = set()
        for i in range(0,len(slot)-1):
            s = slot[i]
            if i in slot_checked:
                continue
            try:
                if c >= n_attack or c >= len(slot):
                    break
                last_raid = s.find_elements(By.XPATH,".//*[@class='lastRaid']/div/*")
                last_status = s.find_elements(By.XPATH,".//*[@class='lastRaid']/div/img[1]")
                running = s.find_elements(By.XPATH,".//*[@class='target']/i")
                if last_raid == []:
                    s.find_element(By.XPATH,".//*[@class='checkbox']").click()
                    c+=1
                    slot_checked.add(i)
                    time.sleep(1)
                elif "senza aver subito perdite" in last_status[0].get_attribute("alt") and "inactive" in running[0].get_attribute("class"):
                    s.find_element(By.XPATH,".//*[@class='checkbox']").click()
                    c+=1
                    slot_checked.add(i)
                    time.sleep(1)
            except Exception as e:
                print(e)
                continue

        if c < n_attack:
            for i in range(0,len(slot)-1):
                s = slot[i]
                if i in slot_checked:
                    continue
                try:
                    if c >= n_attack or c >= len(slot):
                        break
                    last_raid = s.find_elements(By.XPATH,".//*[@class='lastRaid']/div/*")
                    last_status = s.find_elements(By.XPATH,".//*[@class='lastRaid']/div/img[1]")
                    running = s.find_elements(By.XPATH,".//*[@class='target']/i")
                    if last_raid == []:
                        s.find_element(By.XPATH,".//*[@class='checkbox']").click()
                        c+=1
                        slot_checked.add(i)
                        time.sleep(1)
                    elif "senza aver subito perdite" in last_status[0].get_attribute("alt"):
                        s.find_element(By.XPATH,".//*[@class='checkbox']").click()
                        c+=1
                        slot_checked.add(i)
                        time.sleep(1)
                except Exception as e:
                    print(e)
                    continue

        time.sleep(3)
        f.find_element(By.XPATH,".//button[@value='Invia i raid']").click()
    return True

def simulator(o1=0,o2=0,o3=0,o4=0,o5=0,o6=0,o7=0,o8=0,o9=0,o10=0,u1=0,u2=0,u3=0,u4=0,u5=0,u6=0,u7=0,u8=0,u9=0,u10=0):


    cookies = {
        'dpi': '96',
        '_ga': 'GA1.2.493928063.1650902197',
        'show_surv': '',
        '_gid': 'GA1.2.520603616.1652092431',
        '_gat': '1',
    }

    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7,kn;q=0.6,ar;q=0.5',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-type': 'application/x-www-form-urlencoded',
        'Origin': 'http://travian.kirilloid.ru',
        'Pragma': 'no-cache',
        'Referer': 'http://travian.kirilloid.ru/warsim2.php',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
    }

    defender = f"[{u1},{u2},{u3},{u4},{u5},{u6},{u7},{u8},{u9},{u10}]"
    offender = f"[{o1},{o2},{o3},{o4},{o5},{o6},{o7},{o8},{o9},{o10}]"
    data = 'data=[{"p":500,"r":3},{"r":3,"u":'+defender+',"U":[0,0,0,0,0,0,0,0],"side":"def"},{"r":1,"R":1,"u":'+offender+',"U":[0,0,0,0,0,15,0,0],"b":[0,0],"side":"off"}]&mode=9'
    print(data)
    response = requests.post('http://travian.kirilloid.ru/awar2.php', cookies=cookies, headers=headers, data=data, verify=False)
    print(response.json())
    return response.json()[1]["losses"][0]

def farm(driver,village):
   
    if village == "17956":
        parse_troops(driver)
        if "Combattenti" in troops and troops["Combattenti"] >= 550:
            send_farmv2(driver,troops["Combattenti"],village,(0,2))
            driver.find_element(By.XPATH,"//a[@accesskey='2']").click()

    if village == "26470":
        parse_troops(driver)
        if "Combattenti" in troops and troops["Combattenti"] >= 180:
            send_farmv2(driver,troops["Combattenti"],village,(0,2))
            driver.find_element(By.XPATH,"//a[@accesskey='2']").click()
            

def parse_risorse(driver):
    risorse["legno"] = int(driver.find_element(By.XPATH,"//*[@id='l1']").text.replace('.',''))
    risorse["q_legno"] = int(re.findall(r'\d+', driver.find_element(By.XPATH,"//*[@id='lbar1']").get_attribute("style"))[0])
    risorse["argilla"] = int(driver.find_element(By.XPATH,"//*[@id='l2']").text.replace('.',''))
    risorse["q_argilla"] = int(re.findall(r'\d+', driver.find_element(By.XPATH,"//*[@id='lbar2']").get_attribute("style"))[0])
    risorse["ferro"] = int(driver.find_element(By.XPATH,"//*[@id='l3']").text.replace('.',''))
    risorse["q_ferro"] = int(re.findall(r'\d+', driver.find_element(By.XPATH,"//*[@id='lbar3']").get_attribute("style"))[0])
    risorse["grano"] = int(driver.find_element(By.XPATH,"//*[@id='l4']").text.replace('.',''))
    risorse["q_grano"] = int(re.findall(r'\d+', driver.find_element(By.XPATH,"//*[@id='lbar4']").get_attribute("style"))[0])
    risorse["q_media"] = (risorse["q_legno"] + risorse["q_argilla"] + risorse["q_ferro"] + risorse["q_grano"])/4
    risorse["totale"] = risorse["legno"] + risorse["argilla"] + risorse["ferro"] + risorse["grano"]
    print(risorse)
    return risorse

def parse_building_level(driver):
    if "dorf2" not in driver.current_url:
        driver.find_element(By.XPATH,"//a[@accesskey='2']").click()
        time.sleep(2)
    fields = driver.find_elements(By.XPATH,"//div[contains(@class, 'buildingSlot') and not(@data-gid='0')]")
    for f in fields:
        try:
            aid = f.get_attribute("data-aid")
            gid = f.get_attribute("data-gid")
            data_name = f.get_attribute("data-name")
            level = int(f.find_element(By.XPATH,".//*[contains(@class, 'level')]").get_attribute("data-level"))
            building_level.append({"data-name":data_name,"data-aid":aid,"data-gid":gid,"l":level})
        except:
            continue
    print("BUILDING:",building_level)

def build(driver):
    if "dorf2" not in driver.current_url:
        driver.find_element(By.XPATH,"//a[@accesskey='2']").click()
    time.sleep(1)


def truppav2(driver,unita,n,village,aid):
    
    driver.get(f"https://ts31.x3.international.travian.com/dorf2.php?newdid={village}")
    if (unita == "mazze" and risorse["legno"] > 95 and risorse["argilla"] > 75 and risorse["ferro"] > 40 and risorse["grano"] > 40) or (unita == "mazzeg" and risorse["legno"] > 285 and risorse["argilla"] > 225 and risorse["ferro"] > 120 and risorse["grano"] > 120):

            # try:
            #     driver.get("https://ts31.x3.international.travian.com/hero")
            #     time.sleep(1)
            #     in_casa = driver.find_elements(By.XPATH,"//*[@alt='Nel villaggio di appartenenza']")
            #     if len(in_casa) > 0:
            #         driver.find_element(By.XPATH,"//*[@id='helmet']").click()
            #         time.sleep(1)
            #         driver.find_element(By.XPATH,"//*[@id='item_858606']").click()
            #         time.sleep(1)
            # except Exception as e:
            #     print(e)
            #     pass

            driver.find_element(By.XPATH,"//a[@accesskey='2']").click()
            time.sleep(2)
            driver.find_element(By.XPATH,f"//*[@data-aid='{aid}']").click()
            time.sleep(2)

            try:
                n_troops_available = int(driver.find_element(By.XPATH,"//*[@id='nonFavouriteTroops']/div[1]/div/div[2]/div[4]/a").text)
                n_troops = int(max(1,min(n,n_troops_available)*0.45))
                if n_troops == 0:
                    return
            except Exception as e:
                return

            driver.find_element(By.XPATH,"//input[@name='t1']").clear()
            driver.find_element(By.XPATH,"//input[@name='t1']").send_keys(str(n_troops))
            time.sleep(1)
            driver.find_element(By.XPATH,"//button[@name='s1']").click()
            time.sleep(1)
            driver.find_element(By.XPATH,"//a[@accesskey='2']").click()
            print("INCODATO",n_troops," MAZZE")

    if (unita == "asce" and risorse["legno"] > 130 and risorse["argilla"] > 120 and risorse["ferro"] > 170 and risorse["grano"] > 70) or (unita == "asceg" and risorse["legno"] > 390 and risorse["argilla"] > 360 and risorse["ferro"] > 510 and risorse["grano"] > 210):

            # try:
            #     driver.get("https://ts31.x3.international.travian.com/hero")
            #     time.sleep(1)
            #     in_casa = driver.find_elements(By.XPATH,"//*[@alt='Nel villaggio di appartenenza']")
            #     if len(in_casa) > 0:
            #         driver.find_element(By.XPATH,"//*[@id='helmet']").click()
            #         time.sleep(1)
            #         driver.find_element(By.XPATH,"//*[@id='item_858606']").click()
            #         time.sleep(1)
            # except Exception as e:
            #     print(e)
            #     pass

            driver.find_element(By.XPATH,"//a[@accesskey='2']").click()
            time.sleep(2)
            driver.find_element(By.XPATH,f"//*[@data-aid='{aid}']").click()
            time.sleep(2)

            try:
                n_troops_available = int(driver.find_element(By.XPATH,"//*[@id='nonFavouriteTroops']/div[3]/div/div[2]/div[4]/a").text)
                n_troops = int(max(1,min(n,n_troops_available)*0.45))
                if n_troops == 0:
                    return
            except Exception as e:
                print(e)
                return

            driver.find_element(By.XPATH,"//input[@name='t3']").clear()
            driver.find_element(By.XPATH,"//input[@name='t3']").send_keys(str(n_troops))
            time.sleep(1)
            driver.find_element(By.XPATH,"//button[@name='s1']").click()
            time.sleep(1)
            driver.find_element(By.XPATH,"//a[@accesskey='2']").click()
            print("INCODATO",n_troops," ASCE")


    if (unita == "tk" and risorse["legno"] > 450 and risorse["argilla"] > 515 and risorse["ferro"] > 480 and risorse["grano"] > 80) or (unita == "tkg" and risorse["legno"] > 1350 and risorse["argilla"] > 1545 and risorse["ferro"] > 1440 and risorse["grano"] > 240):
  
            # try:
            #     driver.get("https://ts31.x3.international.travian.com/hero")
            #     time.sleep(1)
            #     in_casa = driver.find_elements(By.XPATH,"//*[@alt='Nel villaggio di appartenenza']")
            #     if len(in_casa) > 0:
            #         driver.find_element(By.XPATH,"//*[@id='helmet']").click()
            #         time.sleep(1)
            #         driver.find_element(By.XPATH,"//*[@id='item_854130']").click()
            #         time.sleep(1)
            # except Exception as e:
            #     print(e)
            #     pass
            
            
            driver.find_element(By.XPATH,"//a[@accesskey='2']").click()
            time.sleep(2)
            driver.find_element(By.XPATH,f"//*[@data-aid='{aid}']").click()
            time.sleep(4)

            try:
                n_troops_available = int(driver.find_element(By.XPATH,"//*[@id='favouriteTroops']/div[6]/div/div[2]/div[4]/a").text) 
                n_troops = int(max(1,min(n,n_troops_available)*0.45))
                if n_troops == 0:
                    return
            except Exception as e:
                print(e)
                return

            driver.find_element(By.XPATH,"//input[@name='t6']").clear()
            time.sleep(1)
            driver.find_element(By.XPATH,"//input[@name='t6']").send_keys(str(n_troops))
            time.sleep(1)
            driver.find_element(By.XPATH,"//button[@name='s1']").click()
            time.sleep(1)
            driver.find_element(By.XPATH,"//a[@accesskey='2']").click()
            print("INCODATO",n_troops," TK")


    if unita == "cata":

        if risorse["legno"] > 900 and risorse["argilla"] > 1200 and risorse["ferro"] > 600 and risorse["grano"] > 60:
            driver.find_element(By.XPATH,"//a[@accesskey='2']").click()
            time.sleep(2)
            driver.find_element(By.XPATH,f"//*[@data-aid='{aid}']").click()
            time.sleep(5)

            try:
                n_troops_available = int(driver.find_element(By.XPATH,"//*[@id='nonFavouriteTroops']/div[8]/div/div[2]/div[4]/a").text)
                n_troops = int(max(1,min(n,n_troops_available)*0.45))
                if n_troops == 0:
                    return
            except Exception as e:
                print(e)
                return

            driver.find_element(By.XPATH,"//input[@name='t8']").clear()
            time.sleep(1)
            driver.find_element(By.XPATH,"//input[@name='t8']").send_keys(str(n_troops))
            time.sleep(1)
            driver.find_element(By.XPATH,"//button[@name='s1']").click()
            time.sleep(1)
            driver.find_element(By.XPATH,"//a[@accesskey='2']").click()
            print("INCODATO",n_troops," CATA")
        return

    
    if unita == "arieti":

        if risorse["legno"] > 1000 and risorse["argilla"] > 300 and risorse["ferro"] > 350 and risorse["grano"] > 70:
            driver.find_element(By.XPATH,"//a[@accesskey='2']").click()
            time.sleep(2)
            driver.find_element(By.XPATH,f"//*[@data-aid='{aid}']").click()
            time.sleep(5)
            try:
                n_troops_available = int(driver.find_element(By.XPATH,"//*[@id='nonFavouriteTroops']/div[7]/div/div[2]/div[4]/a").text)
                n_troops = int(max(1,min(n,n_troops_available)*0.45))
                if n_troops == 0:
                    return
            except Exception as e:
                print(e)
                return

            driver.find_element(By.XPATH,"//input[@name='t7']").clear()
            time.sleep(1)
            driver.find_element(By.XPATH,"//input[@name='t7']").send_keys(str(n_troops))
            time.sleep(1)
            driver.find_element(By.XPATH,"//button[@name='s1']").click()
            time.sleep(1)
            driver.find_element(By.XPATH,"//a[@accesskey='2']").click()
            print("INCODATO",n_troops," ARIETI")
        return

    

def truppa(driver):
    if risorse["q_media"] >= 10:
        print("[+] Comincio a truppare!")
        driver.find_element(By.XPATH,"//a[@accesskey='2']").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//*[@data-aid='30']").click()
        time.sleep(2)
        try:

            if risorse["q_grano"] >= 80:
                time.sleep(3)
                driver.find_element(By.XPATH,"//*[@value='Scambio risorse']").click()
                #and not contains(@class, 'disabled')
                time.sleep(2)
                driver.find_element(By.XPATH,"//*[@value='Distribuisci le risorse rimanenti.']").click()
                time.sleep(4)
                driver.find_element(By.XPATH,"//*[@value='Scambia']").click()
                time.sleep(2)


            n_troops_available = int(driver.find_element(By.XPATH,"//*[@id='nonFavouriteTroops']/div[1]/div/div[2]/div[4]/a").text)
            if n_troops_available == 0:
                return
        except Exception as e:
            print(e)
            driver.find_element(By.XPATH,"//a[@accesskey='1']").click()
            return
        n_troops_available = int(n_troops_available * 0.65)
        driver.find_element(By.XPATH,"//input[@name='t1']").clear()
        driver.find_element(By.XPATH,"//input[@name='t1']").send_keys(str(n_troops_available))
        time.sleep(1)
        driver.find_element(By.XPATH,"//button[@name='s1']").click()
        time.sleep(1)
        driver.find_element(By.XPATH,"//a[@accesskey='1']").click()

def parse_coda(driver):
    if "dorf1" not in driver.current_url:
        driver.find_element(By.XPATH,"//a[@accesskey='1']").click()
    try:
        e = driver.find_element(By.XPATH,"//*[@class='buildingList']")
        building = e.find_elements(By.XPATH,".//*[@class='name']")
        coda["len"] = len(building)
        for b in building:
            coda[b.text.strip().split("Livello")[0].strip()] = int(re.findall(r'\d+',b.find_element(By.XPATH,".//*[@class='lvl']").text)[0])
    except:
        pass
    print(coda)
    return coda

def muoviti_random(driver):
    mosse = [
        [],
    ]

def coloni(driver):
    if risorse["totale"] >= 20001:
        driver.find_element(By.XPATH,"//a[@accesskey='2']").click()
        time.sleep(2)
        driver.get("https://ts31.x3.international.travian.com/build.php?id=29&gid=25")
        time.sleep(3)
        driver.find_element(By.XPATH,"//*[@value='Scambio risorse']").click()
        #and not contains(@class, 'disabled')
        time.sleep(2)
        driver.find_element(By.XPATH,"//*[@value='Distribuisci le risorse rimanenti.']").click()
        time.sleep(4)
        driver.find_element(By.XPATH,"//*[@value='Scambia']").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//*[@name='t10']").clear()
        driver.find_element(By.XPATH,"//*[@name='t10']").send_keys("1")
        time.sleep(1)
        driver.find_element(By.XPATH,"//*[@name='s1']").click()

def hero(driver):
    if "Eroe" in troops:
        pass


while 1:
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        print(e)
        pass
    time.sleep(3)
    