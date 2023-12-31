from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup as BS
from datetime import datetime
from random import *

import pandas as pd
import time
import pyperclip
import pyautogui
import sys, os


def find_css(css_selector, browser):
    return browser.find_element(By.CSS_SELECTOR, css_selector)
def finds_css(css_selector, browser):
    return browser.find_elements(By.CSS_SELECTOR, css_selector)

def find_xpath(xpath, browser):
    return browser.find_element(By.XPATH, xpath)
def finds_xpath(xpath, browser):
    return browser.find_elements(By.XPATH, xpath)

def find_id(e_id, browser):
    return browser.find_element(By.ID, e_id)

def find_className(cn, browser):
    return browser.find_element(By.CLASS_NAME, cn)
def finds_className(cn , browser):
    return browser.find_element(By.CLASS_NAME, cn)

def find_linktext(lt, browser):
    return browser.find_element(By.LINK_TEXT, lt)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def naverCafePostStart():    
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('no-sandox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--window-size=1080,800")
    options.add_argument('incognito')

    chrome_service = Service('chromedriver')
    chrome_service = Service(executable_path="chromedriver.exe")
    browser = webdriver.Chrome(service=chrome_service, options=options)

    browser.get("https://nid.naver.com/nidlogin.login")
    time.sleep(1.5)
    
    return browser



def naverLogin(NAVER_ID, NAVER_PW, browser):
    input_id = find_id('id', browser)
    input_pw = find_id('pw', browser)

    time.sleep(2)

    pyperclip.copy(NAVER_ID)
    input_id.send_keys(Keys.CONTROL, "v")

    pyperclip.copy(NAVER_PW)
    input_pw.send_keys(Keys.CONTROL, "v") 
    input_pw.send_keys("\n")

    try:
    # Not needed when it's headless
        no_save_btn = find_id('new.dontsave', browser)
        no_save_btn.click()
    except NoSuchElementException:
        pass
    

def naverLogout(browser):
    browser.get("https://nid.naver.com/nidlogin.logout")
    
    
def checkSubscriptionCafe(browser):
    browser.get("https://section.cafe.naver.com/ca-fe/")

    try:
        while True:
            time.sleep(1.5)
            more_cafeBtn = find_className("btn_mycafe_more", browser)
            more_cafeBtn.click() 
            time.sleep(1.5)

    except Exception as ex:
        soup = BS(browser.page_source, "html.parser")
        soup = soup.find_all(class_='user_mycafe_info')

        find_a, cafe_hrefs, cafe_name = [], [], []
        for i in soup:
            find_a.append(i.find(class_='name_area'))

        for href in find_a:
            cafe_hrefs.append(href["href"])
            cafe_name.append(href.text)
            
    return cafe_hrefs, cafe_name


# Get information from select box (homePage)
def CafeCategoryGet(browser, cafe_url):
    browser.get(cafe_url)
    
    soup = BS(browser.page_source, "html.parser")
    soup = soup.find(class_="box-g-m")
    
    sub_hrefs, ct_name, ct_name_t = [], [], []

    a_hrefs = soup.find_all("a")

    for href in a_hrefs:
        sub_hrefs.append(href["href"])
        ct_name.append(href.text)

    sub_hrefs = sub_hrefs[1:]
    ct_name = ct_name[1:]

    for ct in ct_name:
        ct_name_t.append(ct.strip())

    preprocess_da, final_hrefs = [], []

    for i in range(len(sub_hrefs)):
        preprocess_da.append(f"https://cafe.naver.com/appleiphone{sub_hrefs[i]}, {ct_name_t[i]}")

    for da in preprocess_da:
        if "ArticleList" in da:
            final_hrefs.append(da)

    final_hrefs_true, cafe_name_true = [], []

    for fh in final_hrefs:
        final_hrefs_true.append(fh.split(', ')[0].strip())
        cafe_name_true.append(fh.split(', ')[1].strip())

    final_hrefs_true = final_hrefs_true[1:]
    cafe_name_true = cafe_name_true[1:]
    
    return final_hrefs_true, cafe_name_true


def CafePostWriting(browser, TITLE, cafe_url, comments, PATH_IMG, tag_list, url_list):
    post_url = []
    pyperclip.copy(TITLE)

    
    browser.switch_to.window(browser.window_handles[0])
    browser.get(cafe_url)        

    time.sleep(1)
    n_cafe_name = find_css('h2.cafe_name', browser).text
    time.sleep(2)

    browser.switch_to.frame("cafe_main")



    try:
        find_id('writeFormBtn', browser).click()
        time.sleep(2)

        browser.switch_to.window(browser.window_handles[1])
        time.sleep(1)

        title_area = find_className('textarea_input', browser)

        title_area.send_keys(TITLE)
        time.sleep(1.5)

        editor_id = browser.find_elements(By.TAG_NAME, 'iframe')[-1]

        browser.switch_to.frame(editor_id)
        browser.find_element(By.TAG_NAME, 'body').send_keys(comments)
        browser.find_element(By.TAG_NAME, 'body').send_keys("\n")
        browser.find_element(By.TAG_NAME, 'body').send_keys("\n")
        time.sleep(1.5)

        browser.switch_to.window(browser.window_handles[1])
        time.sleep(3)

        # URL AREA
        if not url_list:
            pass
        else:
            if len(url_list) > 1:
                for url in url_list:
                    link_btn = find_className('se-link-toolbar-button' , browser)
                    link_btn.click()

                    time.sleep(1)

                    url_input = find_className('se-custom-layer-link-input' , browser)

                    pyperclip.copy(url)
                    url_input.send_keys(Keys.CONTROL, "v")
                    url_input.send_keys("\n")

                    editor_id = browser.find_elements(By.TAG_NAME, 'iframe')[-1]

                    browser.switch_to.frame(editor_id)
                    browser.find_element(By.TAG_NAME, 'body').send_keys("\n")
                    time.sleep(1.5)

                    browser.switch_to.window(browser.window_handles[1])

            else:
                link_btn = find_className('se-link-toolbar-button' , browser)
                link_btn.click()

                time.sleep(1)

                url_input = find_className('se-custom-layer-link-input' , browser)

                pyperclip.copy(url_list[0])
                url_input.send_keys(Keys.CONTROL, "v")
                url_input.send_keys("\n")

                editor_id = browser.find_elements(By.TAG_NAME, 'iframe')[-1]

                browser.switch_to.frame(editor_id)
                browser.find_element(By.TAG_NAME, 'body').send_keys("\n")
                time.sleep(1.5)

                browser.switch_to.window(browser.window_handles[1])


        # IAMGE PATH AREA
        img_btn = find_className('se-image-toolbar-button', browser)

        if not PATH_IMG:
            pass
        else:
            if len(PATH_IMG) > 1:
                for pi in PATH_IMG:
                    img_btn.click()
                    time.sleep(1)

                    pyperclip.copy(pi)

                    pyautogui.hotkey('ctrl', 'v')
                    pyautogui.hotkey('enter')

                    time.sleep(2)
            else:
                img_btn.click()
                time.sleep(1)

                pyperclip.copy(PATH_IMG[0])

                pyautogui.hotkey('ctrl', 'v')
                pyautogui.hotkey('enter')

        time.sleep(2)

        # TAG AREA
        tag_area = find_className('tag_input', browser)
        tag_area.send_keys('\n')

        if not tag_list:
            pass
        else:
            if len(tag_list) > 1:
                for tag in tag_list:
                    # tag_area.click()

                    pyperclip.copy(tag)

                    tag_area.send_keys(Keys.CONTROL, "v")
                    tag_area.send_keys("\n")
                    time.sleep(1)
            else:
                pyperclip.copy(tag_list[0])

                tag_area.send_keys(Keys.CONTROL, "v")
                tag_area.send_keys("\n")

        time.sleep(2)

        find_css('div.tool_area> a.BaseButton', browser).click()

        time.sleep(2)

        post_url.append(browser.current_url)

        screenshot_folder = 'screenshot/'
        start_num = 1

        if not os.path.exists(screenshot_folder):
            os.makedirs(screenshot_folder)

        esisting_files = os.listdir(screenshot_folder)
        screenshot_num = start_num + len(esisting_files)

        screenshot_path = f'{screenshot_folder}screenshot_{screenshot_num}.png'
        browser.save_screenshot(screenshot_path)

        time.sleep(1)

    except Exception as ex:
        print(ex)
        print("글을 적을 수 없는 게시판이거나 등급이 낮아 작성할 수 없는 게시판입니다.")
        print("다른 게시판을 선택해주시거나 여러 게시판을 선택 하셨다면 다른 게시판으로 넘어갑니다.")
        pass

    browser.close()
    
    return post_url, n_cafe_name


def start_post_write(browser, manuscript, naver_id_list, cafe_info_urls, PATH_IMG, tag_list, url_list):    
    title_list = []
    comments_list = []
    post_urls = []
    global n_cafe_name
    
    try:
        for i in range(len(manuscript)):
            title = manuscript[i].split('[')[1].split(']')[0]
            comment = manuscript[i].split(']')[1].split('\n')[2:]
            comment = '\n'.join(comment)

            title_list.append(title)
            comments_list.append(comment)

        c = 0

        while c != len(cafe_info_urls):
            for i in range(len(naver_id_list[0])):
                if len(cafe_info_urls) <= c:
                    break

                random_int = int(random() * len(title_list))

                TITLE = title_list[random_int]
                comments = comments_list[random_int]

                NAVER_ID = naver_id_list[0][i]
                NAVER_PW = naver_id_list[1][i]

                naverLogin(NAVER_ID, NAVER_PW, browser)
                if browser.current_url == 'https://nid.naver.com/nidlogin.login':
                    return 0, NAVER_ID

                cafe_url = cafe_info_urls[c]

                try:
                    post_url, n_cafe_name = CafePostWriting(browser, TITLE, cafe_url, comments, PATH_IMG, tag_list, url_list)
                except:
                    pass
                    return 2, NAVER_ID
                post_urls.append(post_url[0])

                browser.switch_to.window(browser.window_handles[0])
                time.sleep(1)
                naverLogout(browser)

                c += 1

        dt = datetime.now().strftime("%Y-%m-%d_%H%M")
        df = pd.DataFrame({'게시글 작성 URL' : post_urls})
        df.to_csv(f'{n_cafe_name}_ULR_{dt}.csv', index=False, encoding='utf-8-sig')

        browser.quit()

    except Exception as ex:
        print(ex)
        dt = datetime.now().strftime("%Y-%m-%d_%H%M")
        df = pd.DataFrame({'게시글 작성 URL' : post_urls})
        df.to_csv(f'{n_cafe_name}_ULR_{dt}.csv', index=False, encoding='utf-8-sig')

        browser.quit()
    return 1, post_urls