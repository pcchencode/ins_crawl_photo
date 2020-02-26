## `script_scrap_photo` 爬蟲出你鎖定的IG帳號，所有貼文的照片！！

### 參數說明
*	`target_id`: 輸入您想要查找的`ins account`
*	`user_ac`: 輸入您所要登入的帳號
*	`user_pw`: 輸入您所登入帳號的密碼
*	`save_path`: 輸入您檔案要儲存的路徑（建議使用`絕對`路徑）

### 套件需求
* `pandas`
* `selenium`
* `chromedriver.exe`

### 執行方法
* 程式碼：`script_scrap_photo.py`
* '''
python3 -targer_id YOUR_TARGET_ACCT -user_ac YOUR_LOGIN_ACCT -user_pw YOUR_PASSWORD -save_path YOUR_FILE_SAVING_PATH
'''

### 貼心小提醒
* 請確保網路連線順利，selenium很容易因為網路不順當掉，小心使用

Happy scraping :))) 
