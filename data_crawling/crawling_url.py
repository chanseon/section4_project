import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import json

#########################
driver_path = "/Users/chanseonpark/chromedriver"
# Service 객체 생성
service = Service(driver_path)
# 크롬 드라이버 인스턴스 생성
driver = webdriver.Chrome(service=service)

# 스트리머 채널 URL
base_url = input("스트리머의 기본 주소 입력:")
channel_url =  base_url + "/videos"

#driver 구동
driver.get(channel_url)
wait = WebDriverWait(driver, 10)  

def scroll_down(driver):
    # 페이지의 높이 가져오기
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        # 페이지 스크롤링
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        # 스크롤링 후 잠시 대기
        time.sleep(5)
        # 새로운 높이 계산
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        # 높이 변화가 없으면 스크롤링 종료
        if new_height == last_height:
            break
        # 높이 업데이트
        last_height = new_height

def get_all_video_urls():  
    # 모든 비디오 링크 추출
    video_links = driver.find_elements(By.XPATH, "//a[@id='video-title-link']")
    video_urls = [link.get_attribute("href") for link in video_links]
    return video_urls


scroll_down(driver)
url_list = get_all_video_urls()
# 리스트를 JSON으로 변환하여 파일에 저장
with open('../data/url_list_output.json', 'w') as f:
     json.dump(url_list, f)