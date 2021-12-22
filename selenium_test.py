from selenium import webdriver

from selenium.webdriver.support.select import Select

driver = webdriver.Firefox()
driver.get("http://127.0.0.1:8000/cal_con")

textbox=driver.find_element_by_name('value')
textbox.send_keys("3")

dropdown1=Select(driver.find_element_by_id('currency-1'))
dropdown1.select_by_index(0)

dropdown2=Select(driver.find_element_by_id('currency-2'))
dropdown2.select_by_index(1)

submit=driver.find_element_by_class_name('btn')
submit.click()

