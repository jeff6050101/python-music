from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import requests
import bs4
from time import sleep
import urllib.request
import os
import svglib
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF



result = []
options = Options()
options.add_argument('--ignore-certificate-errors')
# cookies = 'mscom_new=4974d84c232a9987c72c0736be93085a; mu_browser_bi=4940227759233120078; mu_browser_uni=vgBBg887; _mu_unified_id=1.1680946991.4542838; mu_unregister_user_id=536286385; mu_ab_experiment=2683.1_2746.3_2764.1_2779.2_2806.2_2830.1_2863.2; _csrf=wwCsGfsq8Dvwo6oGStV89QcWI8Wi-dtr; _mu_dc_regular={"v":1,"t":1680946991}; mu_has_static_cache=1680946991; __cf_bm=98q6QgZaC6RwDw7HGZEPYaiMrMqjsOn33akC7kc7L5M-1680946991-0-Ae+imEEYloqAqNbQsBS6K6hhHQsj58wDPJxmPBYyLmQNbZHWCRWnwPTpCMiRl45sOCpvry57X4S+LVwfAlY92I4=; _ga=GA1.2.369071499.1680946990; _gid=GA1.2.717026600.1680946990; _ym_uid=1680946990693995268; _ym_d=1680946990; _pbjs_userid_consent_data=3524755945110770; _pubcid=cc3fa3e5-566e-4691-8f69-24a4f746ce22; _ym_isad=2; __gads=ID=b1727e266f75b353:T=1680946991:S=ALNI_Ma6lN9P8CD8QDib4TIQk4d8LaAtMg; __gpi=UID=00000bef1a3e68df:T=1680946991:RT=1680946991:S=ALNI_MbidGEl7uhLKmkP6yQ7CFJ44fnwKA; _ym_visorc=w; _lr_retry_request=true; _lr_env_src_ats=false; pbjs-unifiedid={"TDID":"2d4ee6f9-6353-4790-ba50-923420aebf27","TDID_LOOKUP":"FALSE","TDID_CREATED_AT":"2023-04-08T09:43:15"}; pbjs-unifiedid_last=Sat, 08 Apr 2023 09:43:14 GMT; panoramaId_expiry=1681551795505; _cc_id=2a697ca42fa73690239791eec42633a; panoramaId=b6ed180f46e11052117a635614ae16d5393894d1372a3886b1e4b803a39da2b5; _lr_geo_location=TW; _mu_session_id=1.1680946990.1680947488; _gat=1; _ms_adScoreView=3'
# cookie = {i.split("=")[0]:i.split("=")[1] for i in cookies.split(";")} 
# headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
# }

#driver = webdriver.Chrome('./chromedriver.exe')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) 

#driver = Chrome()
url = input("請輸入音樂網址")
#url ='https://musescore.com/user/10919536/scores/2377386'

#requests.get(url,headers=headers, cookies=cookie)

#requests.get(url,headers=headers, cookies=cookie)
#driver.add_cookie(cookie_dict = cookie)
driver.get(url)
#driver.refresh()
#driver.implicitly_wait(200)
#print(driver)
#data = driver.find_element(By.CLASS_NAME, 'KfFlO').get_attribute('src')

title = driver.find_element(By.CLASS_NAME, 'nFRPI.V4kyC.z85vg.N30cN').text
#print(type(title))
sleep(3)

alt = driver.find_element(By.CLASS_NAME, 'KfFlO').get_attribute('alt')
page = int(alt[-7])


print(page)
target = driver.find_element(By.ID, "jmuse-scroller-component")

js = f"arguments[0].scrollTop=arguments[0].scrollHeight/{page};"

#用來計算的
pagecopy = page
sleep(2)

for item in range(0,int(page/2)+1):
    if item < page:
        
        driver.execute_script(js, target)
        sleep(1)
        data = driver.find_elements(By.CLASS_NAME, 'KfFlO')
        for temp in data:
            if temp.get_attribute('src') not in result:
                result.append(temp.get_attribute('src')) 
        pagecopy/=2
        js = f"arguments[0].scrollTop=arguments[0].scrollHeight/{pagecopy};"
        sleep(1)


#data = driver.find_elements(By.CLASS_NAME, 'KfFlO')


# for item in data:
#     result.append(item.get_attribute('src'))

#print(data)


#捲動螢幕 操控javascript
# target = driver.find_element(By.ID, "jmuse-scroller-component")

# js = "arguments[0].scrollTop=arguments[0].scrollHeight;"

# driver.execute_script(js, target)

#print(result)
driver.close()
#新增資料夾
path = f"D:/DT01ACA/R-STUDIO/3/元智課程/音樂爬蟲/{title}"
if not os.path.isdir(path):
    os.makedirs(path, mode=0o777)


#前往圖片網頁
imgurl1 = result[0]
header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}
req = urllib.request.Request(imgurl1,headers=header)
res = urllib.request.urlopen(req)
file_path = open(f"./{title}/picture1.svg",'wb')
info = res.read()
file_path.write(info)
 #轉檔
drawing = svg2rlg(f"./{title}/picture1.svg")
if not os.path.isfile(path):
    renderPDF.drawToFile(drawing, f"./{title}/picture1.pdf")
file_path.close()
res.close()

sleep(2)
number = 2
for item in result[1:]:
    imgurl = item
    req = urllib.request.Request(imgurl,headers=header)
    res = urllib.request.urlopen(req)
    file_path = open(f"./{title}/picture{number}.svg",'wb')
    info = res.read()
    file_path.write(info)
     #轉檔
    drawing = svg2rlg(f"./{title}/picture{number}.svg")
    if not os.path.isfile(path):
        renderPDF.drawToFile(drawing, f"./{title}/picture{number}.pdf")
    number+=1
file_path.close()
res.close()


