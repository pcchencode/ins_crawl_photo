## `script_scrap_photo` 爬蟲出你鎖定的IG帳號，所有貼文的照片！！

### 參數說明
*	`target_id`: 輸入您想要查找的`ins account`
*	`user_ac`: 輸入您所要登入的帳號
*	`user_pw`: 輸入您所登入帳號的密碼
*	`save_path`: 輸入您檔案要儲存的路徑
	- `default='./default_save'`: 預設會建立並儲存在資料夾 `default_save` 中

### 套件需求
* `pandas`
* `selenium`
* [chromerdriver](https://chromedriver.storage.googleapis.com/index.html?path=80.0.3987.106/) for selenium
	- version: 80.0.3987.106
	- `chrome` is for mac
	- `chromedriver.exe` is for windows

### 執行方法
* 程式碼：`script_scrap_photo.py`
* clone this repo and cd into it
* `python3 script_scrap_photo.py -target_id {YOUR_TARGET_ACCT} -user_ac {YOUR_LOGIN_ACCT} -user_pw {YOUR_PASSWORD} -save_path {YOUR_FILE_SAVING_PATH}`



### 貼心小提醒
* 請確保網路連線順利，selenium很容易因為網路不順當掉，小心使用

Happy scraping :))) 
