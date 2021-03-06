import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from scrapy.selector import Selector

browser = webdriver.Chrome()

url = 'https://www.kaistart.com/project/more.html'

try:
    browser.get(url)
    wait = WebDriverWait(browser, 20)
    wait.until(lambda dr: dr.find_element_by_class_name('project-detail').is_displayed())
    js1 = 'return document.body.scrollHeight'
    js2 = 'window,scrollTo(0, document.body.scrollHeight)'
    old_scroll_height = 0
    while browser.execute_script(js1) >= old_scroll_height:
        old_scroll_height = browser.execute_script(js1)
        browser.execute_script(js2)
        time.sleep(1)
    se1 = Selector(text=browser.page_source)
    project_list = se1.xpath('//li[@class="project-li"]')
finally:
    pass

