import pandas as pd
import random
from selenium import webdriver  # 從library中引入webdriver
# from selenium.webdriver.common.by import By
# from fake_useragent import UserAgent # !pip install fake-useragent
from selenium.webdriver.chrome.options import Options
import time
import urllib
import argparse
pd.set_option('display.max_rows', 250)

def get_all_posts(ins_id, user_ac, user_pw):
    browser = webdriver.Chrome('./chromedriver') #開啟chrome browser
    browser.get('https://www.instagram.com/'+str(ins_id)+'/') #開啟想要搜尋的帳號ＩＧ

    #先進行登入的動作
    button = browser.find_element_by_xpath("//button[@type='button'][text()='登入']") #尋找登入點擊按鈕
    button.click()
    time.sleep(5) #網頁反應沒那麼快，要等一下

    account = browser.find_elements_by_xpath("//input[@aria-label='電話號碼、用戶名稱或電子郵件']")
    account[0].send_keys(user_ac) #account只為長度1的list，很奇怪。輸入帳號名稱
    time.sleep(5)

    password = browser.find_elements_by_xpath("//input[@aria-label='密碼']")
    password[0].send_keys(user_pw) #account只為長度1的list，很奇怪。輸入帳號名稱
    time.sleep(5)

    confirm_button = browser.find_element_by_xpath("//button[@type='submit']") #尋找登入點擊按鈕
    confirm_button.click() #點擊登入按鈕
    time.sleep(5)

    num_post = browser.find_elements_by_xpath("//span[@class='-nal3 ']") #定位貼文置的位置
    num_post[0].text #顯示貼文數
    time.sleep(5)    
    
    num_post = browser.find_elements_by_xpath("//span[@class='-nal3 ']") #定位貼文置的位置
    num_post[0].text #抓取總文章數
    time.sleep(5)
    
    #撈取所有post的超連結
    post_hrefs=[]
    height = browser.execute_script("return document.body.scrollHeight") #一開始頁面的高度
    while str(len(post_hrefs))+' 貼文' != num_post[0].text:
        lastHeight = height

        # step 1
        elements = browser.find_elements_by_xpath('//a[contains(@href, "/p/")]')

        # step 2
        
        for element in elements:
            if element.get_attribute('href') not in post_hrefs:
                post_hrefs.append(element.get_attribute('href'))

        # step 3
        #browser.execute_script("return arguments[0].scrollIntoView();", elements[-1])
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
    browser.close()
    return post_hrefs

def login_ins_browser(ac, pw):
    browser = webdriver.Chrome('.//chromedriver')    #開啟chrome browser
    browser.get('https://www.instagram.com/po_chu_chen/')

    #先進行登入的動作
    button = browser.find_element_by_xpath("//button[@type='button'][text()='登入']") #尋找登入點擊按鈕
    button.click()
    time.sleep(2) #網頁反應沒那麼快，要等一下

    account = browser.find_elements_by_xpath("//input[@aria-label='電話號碼、用戶名稱或電子郵件']")
    account[0].send_keys(ac) #account只為長度1的list，很奇怪。輸入帳號名稱
    time.sleep(2)

    password = browser.find_elements_by_xpath("//input[@aria-label='密碼']")
    password[0].send_keys(pw) #account只為長度1的list，很奇怪。輸入帳號名稱
    time.sleep(2)

    confirm_button = browser.find_element_by_xpath("//button[@type='submit']") #尋找登入點擊按鈕
    confirm_button.click() #點擊登入按鈕
    time.sleep(5)
    return browser



def scrap_src(post_url, browser):
    browser.get(post_url)
    time.sleep(2)
    src_list = []
    img_pos = browser.find_elements_by_xpath('//div[@class="KL4Bh"]/img')
    src = img_pos[0].get_attribute('src')
    src_list.append(src)
    right_click_button = browser.find_elements_by_xpath('//button[@class="  _6CZji"]')
    while len(right_click_button)!=0:
        right_click_button[0].click()
        time.sleep(2)
        img_pos = browser.find_elements_by_xpath('//div[@class="KL4Bh"]/img')
        src = img_pos[0].get_attribute('src')
        src_list.append(src)
        right_click_button = browser.find_elements_by_xpath('//button[@class="  _6CZji"]')
    
    return src_list

def download_pic(src_list, save_path):
    for i in range(len(src_list)):
        save_path_img = save_path+str(time.ctime(time.time()))+'.png'
        pic_file = urllib.request.urlopen(src_list[i]).read()
        f = open(save_path_img, 'wb')
        f.write(pic_file)
        f.close()
        time.sleep(1)
        
    return


def main(target_id, user_ac, user_pw, save_path):
    post_hrefs = get_all_posts(target_id, user_ac, user_pw)
    browser = login_ins_browser(ac=user_ac, pw=user_pw)
    browser.get(post_hrefs[0])
    for i in range(len(post_hrefs)):
        browser.refresh()
        try:
            download_pic(scrap_src(post_hrefs[i], browser), save_path)
            time.sleep(random.uniform(2,5))
        except IndexError:
            pass
    browser.close()
        
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-target_id', action='store')
    parser.add_argument('-user_ac', action='store')
    parser.add_argument('-user_pw', action='store')
    parser.add_argument('-save_path', action='store')
    args = parser.parse_args()
    main(args.target_id, args.user_ac, args.user_pw, args.save_path)
