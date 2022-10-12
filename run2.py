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

troops = {}

def handleAttack(driver):
    driver.get("https://ts31.x3.international.travian.com/village/statistics")
    time.sleep(3)
    attacks = len(driver.find_elements(By.XPATH,"//*[@class='att1']"))
    if attacks == 0:
        print("NO ATTACK")
    else:
        print("ATTACCO IN CORSO",datetime.now())
        if len(driver.window_handles) == 1:
            driver.execute_script('''window.open("https://www.youtube.com/watch?v=zdb3SaUver0","_blank");''')
        



def main():
    driver=get_chromedriver()
    login(driver)
    while 1:
        handleAttack(driver)
        print("OK")
        for village in ["17956"]:
            global troops
            driver.get(f"https://ts31.x3.international.travian.com/dorf2.php?newdid={village}")
            time.sleep(2)
            print("OK")
            try:
                farm(driver,village)
            except Exception as e:
                print(e)
                pass
            driver.find_element(By.XPATH,"//a[@accesskey='2']").click()
        r = random.randint(90, 250)
        c = r
        for x in range(0,r):
            print(c)
            time.sleep(1)
            c -= 1
    driver.quit()





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
    chrome_options.add_argument('--user-data-dir=/home/big0/.config/google-chromeTrav')
    # capa = DesiredCapabilities.CHROME
    # capa["pageLoadStrategy"] = "none"
    driver = webdriver.Chrome(executable_path="./chromedriver",chrome_options=chrome_options)
    driver.set_window_size(1980,1020)
    return driver
       


def login(driver):

    driver.get("https://ts31.x3.international.travian.com/dorf2.php")
    time.sleep(3)

    if "dorf2" in driver.current_url:
        return True

    driver.get("https://ts31.x3.international.travian.com/")
    
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

def farm(driver,village):
   
    if village == "17956":
        parse_troops(driver)
        if "Combattenti" in troops and troops["Combattenti"] >= 350:
            send_farmv2(driver,troops["Combattenti"],village,(0,3))
            driver.find_element(By.XPATH,"//a[@accesskey='2']").click()


def send_farmv2(driver,troops,village,s):
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
        

        print("OKOKK")
        time.sleep(3)
        f.find_element(By.XPATH,".//*[@class='markAll check']").click()
        time.sleep(2)
        f.find_element(By.XPATH,".//*[@value='Avvia']").click()


while 1:
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        print(e)
        pass
    time.sleep(3)
    