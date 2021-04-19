import os
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# Chromeを起動する関数


def set_driver(driver_path, headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless') # 画面を表示せずに動作するモード

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(executable_path=os.getcwd() + "/" + driver_path, options=options)

# main処理


def main():
    search_keyword = input('Enter word:') #"高収入"
    # driverを起動
    # driverを起動
    driver = webdriver.Chrome(ChromeDriverManager().install())
    '''
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)
    else:
        driver = set_driver("chromedriver_linux", False)
    '''
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
 
    try:
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        pass
    
    # 検索窓に入力
    driver.find_element_by_class_name(
        "topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()
    time.sleep(5)

    cols =["会社名","仕事内容","対象となる方","勤務地","給与","初年度年収"]
    df = pd.DataFrame(index=[], columns=cols)

    page = 1
    while True:
        # ページ終了まで繰り返し取得
        exp_name_list = []

        # 検索結果の一番上の会社名を取得
        name_list = driver.find_elements_by_class_name("cassetteRecruit__name")
        tableelem = driver.find_elements_by_class_name("tableCondition")
        
        if len(name_list) == 0:
            print('FINISH')
            break

        # 1ページ分繰り返し
        # print(len(name_list))

        print(str(page)+"ページ目")
        for i in range(len(name_list)):
            exp_name_list.append(name_list[i].text)
            # 広告回避
            if page == 1:
                ths = tableelem[i+2].find_elements(By.TAG_NAME, "th")
                tds = tableelem[i+2].find_elements(By.TAG_NAME, "td")
            else:
                ths = tableelem[i].find_elements(By.TAG_NAME, "th")
                tds = tableelem[i].find_elements(By.TAG_NAME, "td")
            
            rec = [name_list[i].text]
            cols = ["会社名"]
            for j in range(len(tds)):
                cols.append(ths[j].text)
                rec.append(tds[j].text)
            
            print(cols)
            print(rec)

            df1 = pd.Series(rec, index=cols)    
            df = df.append(df1, ignore_index=True)

            print(name_list[i].text)
            print("  " + ths[0].text)
            print("  " + ths[1].text)
            print("  " + ths[2].text)

        print(df)
        page += 1
        try:
            nextpage = driver.find_element_by_class_name("iconFont--arrowLeft").get_attribute("href")
            driver.get(nextpage)
            time.sleep(5)
        except :
            df.to_csv("data.csv", index=True)
            print('FINISH')
            break

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
