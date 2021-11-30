import os
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from selenium.common import exceptions
from datetime import datetime
from find_url import Channel
from multiprocessing import Process

# from selenium.webdriver.common.proxy import Proxy, ProxyType
# from selenium.webdriver.firefox.options import Options

LOG_FILE = r'C:\Users\voreo\Documents\ProjectsPy\bot\LOG.txt'
CHANNEL_FILE = r'C:\Users\voreo\Documents\ProjectsPy\bot\CH.txt'
PROXY_FILE = r'C:\Users\voreo\Documents\ProjectsPy\bot\PROXY.txt'
COOKIE_DIR = r'C:\Users\voreo\Documents\ProjectsPy\bot\COOKIE_DIR'
SITES_FILE = r'C:\Users\voreo\Documents\ProjectsPy\bot\SITES.txt'

PIC_BANNER_ELEM = '/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div/div/div/ytd-player/div/div/div[4]/div[2]/div/div[3]/div[3]/img'
PLAY_BUT_ELEM = 'ytp-play-button.ytp-button'
FIRST_ADV_LINK_ELEM = 'ytp-ad-button.ytp-ad-visit-advertiser-button.ytp-ad-button-link'
SKIP_BUT_ELEM = 'ytp-ad-skip-button-icon'
ACCEPT_BUT_ELEM = '/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[2]/div[2]/div[5]/div[2]/ytd-button-renderer[2]/a/tp-yt-paper-button'

def exit():
    sys.exit(1)

def check_exists(driver:webdriver, parameter:By ,element:webdriver) -> bool:
    try:
        driver.find_element(parameter, element)
    except exceptions.NoSuchElementException:
        return False
    return True

def check_ad(driver:webdriver, window:webdriver, time_watch:int) -> bool:

    is_exists_ad = 0
    second = 0
    banner = 0

    for i in range(0, 2):

        time.sleep(1)
        driver.find_element(By.CLASS_NAME, PLAY_BUT_ELEM).click()
        time.sleep(1)

        if check_exists(driver, By.CLASS_NAME, FIRST_ADV_LINK_ELEM):
            driver.find_element(By.CLASS_NAME, FIRST_ADV_LINK_ELEM).click()
            time.sleep(1)
            driver.switch_to.window(window)
            time.sleep(1)
            driver.find_element(By.CLASS_NAME, PLAY_BUT_ELEM).click()
            time.sleep(4)
            is_exists_ad += 1
            if check_exists(driver, By.CLASS_NAME, SKIP_BUT_ELEM):
                driver.find_element(By.CLASS_NAME, SKIP_BUT_ELEM).click()
            else:
                time.sleep(6)
            
        else:
            driver.find_element(By.CLASS_NAME, PLAY_BUT_ELEM).click()
            if i == 1 and is_exists_ad == False:
                while second < time_watch:
                    time.sleep(1)

                    if check_exists(driver, By.XPATH, PIC_BANNER_ELEM) and banner == False:
                        try:
                            driver.find_element(By.XPATH, PIC_BANNER_ELEM).click()
                            banner += 1
                            driver.switch_to.window(window)
                            time.sleep(1)
                            driver.find_element(By.CLASS_NAME, PLAY_BUT_ELEM).click()
                        except:
                            pass

                    second += 1

    if is_exists_ad or banner:
        return True
    else:
        return False        

def ad_click(settings, channel, proxy, cookie_file_path, sites):

    ch = Channel(channel) 
    click_list = ch.get_click_list(settings['num_watch_per'], settings['num_click_per'])
    with open(LOG_FILE, 'a') as log_file:
        log_file.write('\n' + 'Proxy loaded: ' + proxy + '\n')
    ua = UserAgent()
    user_agent = ua.random 
    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={user_agent}')
    # options.add_argument('--proxy-server=%s' % proxy.rstrip())
    options.add_argument('--proxy-server=socks5://' + proxy.rstrip())
    browser = webdriver.Chrome(options=options)

    if settings['cookie_mode']:
        with open(cookie_file_path, 'r') as cookie_file:
            cookies = [cookie.rstrip().split('\t') for cookie in cookie_file]
        
        for cookie in cookies:
            try:
                if 'www' in cookie:
                    browser.get('http://' + cookie[0])
                elif cookie[0][0] == '.':
                    browser.get('http://www' + cookie[0])
                else:
                    browser.get('http://www.' + cookie[0])
                browser.add_cookie({'name': cookie[5],
                                    'value': cookie[6],
                                    'path': cookie[2],
                                    'domain': cookie[0],
                                    'secure': False,
                                    'sameSite': 'Strict'})
            
                with open(LOG_FILE, 'a') as log_file:
                    log_file.write('Cookie successfully loaded from: ' + str(COOKIE_DIR + '\\' + cookie_file_path) + '\n')

            except (exceptions.WebDriverException, exceptions.InvalidCookieDomainException) as ex:
                with open(LOG_FILE, 'a') as log_file:
                    log_file.write(str(datetime.today()) + '\n' + ex.msg + '\n' + 'Cookie load error.' + '\n' + str(cookie) + '\n')

    else:
        try:
            for site in sites:
                browser.get(site)
                time.sleep(2)
            with open(LOG_FILE, 'a') as log_file:
                    log_file.write('Cookie successfully recorded.' + '\n')
        except exceptions.WebDriverException as ex:
                with open(LOG_FILE, 'a') as log_file:
                    log_file.write(str(datetime.today()) + '\n' + ex.msg + '\n' + 'Cookie record error.' + '\n' + site + '\n')


    # Настройки для Mozilla Firefox

    # options = Options()
    # options.add_argument(f'user-agent={user_agent}')
    # my_proxy = Proxy({
    #              'proxyType': ProxyType.MANUAL,
    #              'httpProxy': proxy,
    #              'ftpProxy': proxy,
    #              'sslProxy': proxy,
    #              'noProxy': '' # set this value as desired
    #             })
    # browser = webdriver.Firefox(proxy=my_proxy, options=options)

    with open(LOG_FILE, 'a') as log_file:
                        log_file.write('\n' + '===Channel loaded===' + str(ch))
    skipped_adv = 0 
    click = 0

    for video in range(0, ch.num_watch):
        try:
            prev_window = None
            browser.get(ch.video_links[video])
            current_window = browser.current_window_handle
            with open(LOG_FILE, 'a') as log_file:
                            log_file.write('\n' + 'Video loaded: ' + str(ch.video_links[video]) + '\n')
            
            if check_exists(browser, By.XPATH, ACCEPT_BUT_ELEM):
                browser.find_element(By.XPATH, ACCEPT_BUT_ELEM).click()

            if check_exists(browser, By.CLASS_NAME, 'ytp-ad-button.ytp-ad-visit-advertiser-button.ytp-ad-button-link') == False:
                browser.switch_to.new_window('tab')
                browser.get(ch.video_links[video])
                prev_window = current_window
                current_window = browser.current_window_handle

            # browser.find_element(By.CLASS_NAME, PLAY_BUT_ELEM).click()

            if video in click_list:
                if check_ad(browser, current_window, settings['time_watch']) == False:
                    time.sleep(1)
                    skipped_adv =+ 1
                else:
                    time.sleep(1)
                    click += 1
                    with open(LOG_FILE, 'a') as log_file:
                        log_file.write('\n' + 'Adv click. Total clicks: ' + str(click) + ' of ' + str(ch.num_click) + '\n')

            else:
                if skipped_adv:
                    if check_ad(browser, current_window, settings['time_watch']) == False:
                        time.sleep(1)
                        skipped_adv += 1
                    else:
                        time.sleep(1)
                        skipped_adv -= 1
                        click += 1
                        with open(LOG_FILE, 'a') as log_file:
                            log_file.write('\n' + 'Adv click. Total clicks: ' + str(click) + ' of ' + str(ch.num_click) + '\n')
                else:
                    for i in range(2):
                        if check_exists(browser, By.CLASS_NAME, FIRST_ADV_LINK_ELEM):
                            time.sleep(5)
                            if check_exists(browser, By.CLASS_NAME, SKIP_BUT_ELEM):
                                browser.find_element(By.CLASS_NAME, SKIP_BUT_ELEM).click()
                            else:
                                time.sleep(6)

                    time.sleep(settings['time_watch'])

            if prev_window:
                browser.close()
                browser.switch_to.window(prev_window)

            with open(LOG_FILE, 'a') as log_file:
                        log_file.write('View completed. Video ' + str(video + 1) + ' of ' + str(ch.num_watch))

        except exceptions.WebDriverException as ex:
            print(ex)
            with open(LOG_FILE, 'a') as log_file:
                log_file.write('\n' + str(datetime.today()) + '\n' + ex.msg + '\n' + proxy + 'Video: ' + str(ch.video_links[video]) + '\n\n')

    browser.quit()

def main(cookie_mode:bool, num_watch_per:int, num_click_per:int, time_watch:int) -> None:
    
    num_channel = 0
    num_cookie = 0
    proxy_thread = []
    proxy_threads = []
    processes = []

    settings = {
        'cookie_mode': cookie_mode,
        'num_watch_per': num_watch_per,
        'num_click_per': num_click_per,
        'time_watch': time_watch,
    }

    cookie_list = os.listdir(COOKIE_DIR)

    with open(LOG_FILE, 'a') as log_file:
        log_file.write('\n\n' + str(datetime.today()) + '\n' + '=====================================START=====================================' + '\n')

    with open(PROXY_FILE, 'r') as proxy_file:
        proxies = [stroke for stroke in proxy_file]

    with open(CHANNEL_FILE, 'r') as channel_file:
        channels = [stroke for stroke in channel_file]

    with open(SITES_FILE, 'r') as sites_file:
        sites = [stroke for stroke in sites_file]

    for proxy in proxies:
        if len(proxy_thread) < 10:
            proxy_thread.append(proxy)
        else:
            proxy_threads.append(proxy_thread)
            proxy_thread = []
            proxy_thread.append(proxy)
    proxy_threads.append(proxy_thread)
    
    for proxy_list in proxy_threads:

        for proxy in proxy_list:

            if num_channel >= len(channels):
                num_channel = 0
            if num_cookie >= len(cookie_list):
                num_cookie = 0

            process = Process(target=ad_click, args=(settings, channels[num_channel], proxy, COOKIE_DIR + cookie_list[num_cookie], sites))
            process.start()
            processes.append(process)
            num_channel += 1
            num_cookie += 1
            time.sleep(10)

        for process in processes:
            process.join()
            

    with open(LOG_FILE, 'a') as log_file:
        log_file.write(str(datetime.today()) + '\n' + '=====================================END=====================================' + '\n\n')

if __name__ == '__main__':
    main(False, 1, 25, 20)

