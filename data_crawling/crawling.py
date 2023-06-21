import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC #추가 알아볼 대상
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from tqdm import tqdm
import time
import json
import re

# list JSON 파일을 리스트로 읽기
with open('../data/url_list_output.json', 'r') as f:
    url_list = json.load(f)

driver_path = "/Users/chanseonpark/chromedriver"

service = Service(driver_path)
service.start()

options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 브라우저 창을 표시하지 않음
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver,8)

data_list =[]
#data_list =[['duration','count','date','hashtag','good','game']]

for url in tqdm(url_list):

    driver.get(url)

    #영상길이
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ytp-time-duration")))
    duration_element = driver.find_element(By.CLASS_NAME, "ytp-time-duration")
    duration = duration_element.text.strip()
    time.sleep(20)#광고때문에.. -> 크롤링 이후에 광고인 애들 확인해야함.
    ##########################################################
    wait.until(EC.presence_of_element_located((By.ID, "expand")))
    button_element = driver.find_element(By.XPATH, "//*[@id='expand']")

    # 요소 클릭하기
    button_element.click()
    ########################################################
    wait.until(EC.presence_of_element_located((By.ID, "info")))
    #조회수
    count_element = driver.find_element(By.XPATH, "//*[@id='info']/span[1]")
    count_raw = count_element.text.strip()
    count = re.findall(r"[0-9]*,?[0-9]+", count_raw)[0]
    #업로드날짜
    date_element = driver.find_element(By.XPATH, "//*[@id='info']/span[3]")
    date = date_element.text.strip()
    #댓글개수 -> 무슨이유인지 안돼서 일단 누락.
    #count_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "yt-formatted-string.count-text.style-scope.ytd-comments-header-renderer > span:nth-child(2)")))
    #comment_count = count_element.text.strip()
    #해쉬태그
    try: 
        hash_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='description-inline-expander']/yt-attributed-string")))
        hash_raw = hash_element.text.strip()
        hashtag = re.findall(r"#.+", hash_raw)[0].split()
    except IndexError:
        hashtag = hash_raw
    #좋아요
    good_element = driver.find_element(By.XPATH, '//*[@id="segmented-like-button"]/ytd-toggle-button-renderer/yt-button-shape/button')
    good = good_element.text.strip()
    #게임 정보
    try: 
        game_element = driver.find_element(By.XPATH, '//*[@id="contents"]/ytd-rich-metadata-renderer[1]')
        #//*[@id="always-shown"]
        game = game_element.text.strip()
    except NoSuchElementException:
        game = 'None'

    data_list.append([duration,count,date,hashtag,good,game])

driver.quit()


with open('../data/data_output.json', 'w') as f:
     json.dump(data_list, f)

