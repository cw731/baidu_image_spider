"""
百度图片下载
"""

import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import platform
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CollectLinks:
    def __init__(self):
        executable = ''

        if platform.system() == 'Windows':
            print('==>目标OS : Windows')
            executable = './chromedriver/chromedriver_win.exe'
        elif platform.system() == 'Linux':
            print('==>目标OS : Linux')
            executable = './chromedriver/chromedriver_linux'
        elif platform.system() == 'Darwin':
            print('==>目标OS : Mac')
            executable = './chromedriver/chromedriver_mac'
        else:
            assert False, 'Unknown OS Type'

        self.browser = webdriver.Chrome(executable)
        # self.browser = webdriver.phantomjs


    def get_scroll(self):
        pos = self.browser.execute_script("return window.pageYOffset;")
        return pos

    def wait_and_click(self, xpath):
        #  Sometimes click fails unreasonably. So tries to click at all cost.
        try:
            w = WebDriverWait(self.browser, 15)
            elem = w.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            elem.click()
        except Exception as e:
            print('Click time out - {}'.format(xpath))
            print('Refreshing browser...')
            self.browser.refresh()
            time.sleep(2)
            return self.wait_and_click(xpath)

        return elem

    def baidu(self, keyword):
        url = "https://image.baidu.com/"
        self.browser.get(url)

        time.sleep(1)

        input_box = self.browser.find_element_by_xpath('//*[@id="kw"]')
        input_box.send_keys(keyword)

        search_butten = self.browser.find_element_by_xpath('//*[@id="homeSearchForm"]/span[2]')
        search_butten.click()
        time.sleep(1)

        print('==>开始滚动网页_刷取图片_{}'.format(keyword))

        elem = self.browser.find_element_by_tag_name("body")

        for i in range(60):
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)

        photo_grid_boxes = self.browser.find_elements(By.XPATH, '//*[@id="imgid"]/div/ul/li')

        print('==>获取_组装_图片地址')

        links = []

        for box in photo_grid_boxes:
            try:
                imgs = box.find_elements(By.TAG_NAME, 'img')

                for img in imgs:
                    src = img.get_attribute("src")
                    # print(src)
                    if src[0] != 'd':
                        links.append(src)

            except Exception as e:
                print('[异常中断:] {}'.format(e))
        links = set(links)
        print('==> {} 图片链接获取数目: {}'.format(keyword, len(links)))
        self.browser.close()

        return links


if __name__ == '__main__':
    collect = CollectLinks()
    links = collect.baidu('无人机')
    print(len(links), links)
