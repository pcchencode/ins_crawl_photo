import pandas as pd
pd.set_option('display.max_rows', 250)
import random
from selenium import webdriver  #從library中引入webdriver
import time
import argparse

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
    from selenium import webdriver  #從library中引入webdriver
    #from selenium.webdriver.common.by import By
    from fake_useragent import UserAgent # !pip install fake-useragent
    from selenium.webdriver.chrome.options import Options
    import time

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

#這個函數前面一定要有setting好的browser
def get_likers(post_url, browser):
    import pandas as pd
    import random
    browser.get(post_url)
    time.sleep(1)
    video = browser.find_elements_by_xpath('//span[@aria-label="播放"]') #影片型post在網站抓不到likers，所以放棄
    if len(video)==0: #if the video is empty, we'll capture the likers-list
        try:
            like_list_button = browser.find_element_by_xpath('//button[@class="sqdOP yWX7d     _8A5w5    "]')
            time.sleep(1)
        except:
            browser.refresh()
            time.sleep(10)
            return get_likers(post_url, browser)
        like_list_button.click() #點擊按讚的癡漢

        time.sleep(5)

        likers = []       
        match = False
        while match==False:
        #試了老半天還是以頁面高度作為下拉原則，因為IG上面顯示的按讚數跟按讚用戶數數字對不上    
            try:
                height = browser.find_element_by_xpath("//html/body/div[4]/div/div[2]/div/div").value_of_css_property("padding-top")
            except:
                browser.refresh()
                time.sleep(10)
                return get_likers(post_url, browser)
            lastHeight = height

            # step 1
            elements = browser.find_elements_by_xpath("//*[@id]/div/a")

            # step 2
            for element in elements:
                likers.append(element.get_attribute('title'))

            # step 3
            try:
                browser.execute_script("return arguments[0].scrollIntoView();", elements[-1])
                time.sleep(random.uniform(1,2))
            except:
                browser.refresh()
                time.sleep(10)
                return get_likers(post_url, browser)

            # step 4
            try:
                height = browser.find_element_by_xpath("//html/body/div[4]/div/div[2]/div/div").value_of_css_property("padding-top")
            except:
                browser.refresh()
                time.sleep(10)
                return get_likers(post_url, browser)
            if lastHeight==height:
                match = True

        likers = list(set(likers))
 

    else:
        likers = []
    return likers

def main(target_id, user_ac, user_pw):
	post_hrefs = get_all_posts(target_id, user_ac, user_pw)
	browser = login_ins_browser(ac=user_ac, pw=user_pw)
	browser.get(post_hrefs[0])

	likers_list = []
	for link in post_hrefs:
	    likers_list.append(get_likers(link, browser))


	all_likers = []
	for i in range(0,len(likers_list)):
	    all_likers = all_likers + likers_list[i]

	data = pd.DataFrame(all_likers, columns=['liker_name'])
	likers_stat = pd.DataFrame(data['liker_name'].value_counts())

	print('Likers of '+target_id)
	print('Numbers of Posts: '+str(len(post_hrefs)))
	likers_stat.to_csv(str(target_id)+'_likers_stat.csv')



if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-target_id', action='store')
	parser.add_argument('-user_ac', action='store')
	parser.add_argument('-user_pw', action='store')
	args = parser.parse_args()
	main(args.target_id, args.user_ac, args.user_pw)





