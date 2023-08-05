import math

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

import send_auto

# Параметры для выполнения учебного задания:
# 1. Ссылка на страницу с задачей:
L_URL = 'https://stepik.org/lesson/181384/step/8'
# 2. Ссылка на объект тестирования:
URL = 'http://suninjuly.github.io/explicit_wait2.html'


# Функция для запуска Chrome браузера и ссылки (URL) на нём
def open_site_on_chrome(url):
    browser_new = webdriver.Chrome()
    browser_new.get(url)
    return browser_new


# Функция для расчёта параметра y
def calc_y(x):
    return str(math.log(abs(12 * math.sin(int(x)))))


try:
    # Откроем ссылку в браузере Chrome
    URL = 'http://suninjuly.github.io/explicit_wait2.html'
    browser = open_site_on_chrome(URL)

    # Подождём пока выполнится условие $ = 100
    WebDriverWait(browser, 12).until(ec.text_to_be_present_in_element((By.ID, 'price'), '$100'))

    # Найдём кнопку Book и кликнем по ней
    browser.find_element(By.ID, 'book').click()

    # Найдём величину x и рассчитаем y(x)
    x = browser.find_element(By.ID, 'input_value').text
    y = calc_y(x)

    # Вставим результат расчёта в поле ответа и отправим на проверку
    browser.find_element(By.ID, 'answer').send_keys(y)
    browser.find_element(By.ID, 'solve').click()

    # Вытащим из alert текст с ответом и очистим его от лишнего:
    # 1. Скопируем текст с ответом.
    answer_green = browser.switch_to.alert.text
    # 2. Удалим лишний текст.
    # В настоящее время "костыль", т.к. метод split даёт на выходе, например, такое: ['', '29.035249889140367']
    answer = answer_green.split("Congrats, you've passed the task! Copy this code as the answer to Stepik quiz: ")

    # Внесём результаты расчёта в форму для ответа на задание, страница: 2.4 Настройка ожиданий, шаг 8.
    send_auto.send_answer(answer, L_URL)

finally:
    browser.quit()
