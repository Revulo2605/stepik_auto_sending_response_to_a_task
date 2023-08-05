import time
import data

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


def check_auth(browser):
    check = browser.find_elements(By.CSS_SELECTOR, 'div.navbar__profile')
    if not check:
        return False
    else:
        return True


# Описание входящих параметров:
# answer - решение задачи, которое вы хотите загрузить в поле ответа на странице курса.
# l_url - ссылка на страницу куда вы хотите загрузить ответ.

# Функция для автоматического ввода данных в поле ответа на сайте Stepik
def send_answer(answer, l_url):
    # Откроем браузер Chrome и страницу авторизации
    browser = webdriver.Chrome()
    browser.get(data.A_URL)

    # Проверим авторизован ли пользователь, а если нет, то авторизуемся.
    # Похоже каждая новая сессия "чистая", т.е. если вы уже авторизованы на сайте в этом же браузере,
    # то при запуске этого скрипта, вам придётся пройти авторизацию повторно.
    # На всякий случай пока оставлю этот цикл проверки.
    check_a = check_auth(browser)
    if check_a is False:
        # Убедимся, что форма регистрации открылась и проведём авторизацию
        WebDriverWait(browser, 12).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'input[id="id_login_email"]'))).send_keys(data.LOGIN)
        browser.find_element(By.CSS_SELECTOR, 'input[id="id_login_password"]').send_keys(data.PASSWORD)
        browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        # Подождём пока не пройдёт авторизация. Ожидаем загрузки выпадающего списка профиля.
        WebDriverWait(browser, 12).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div.navbar__profile')))
    else:
        pass

    # Отправим ответ на задание, для этого:
    # 1. Откроем страницу с заданием.
    browser.get(l_url)
    # 2. Убедимся, что поле для ввода ответа загрузилось.
    WebDriverWait(browser, 12).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, 'textarea.ember-text-area.ember-view')))
    # 3. Проверим, что поле ввода не находится в состоянии "correct", т.е. задача ещё не решена.
    check = browser.find_elements(By.CSS_SELECTOR, 'div[data-state="correct"]')
    if not check:
        # Профилактика поля ввода ответа от наличия предыдущих попыток решения задачи.
        browser.find_element(By.CSS_SELECTOR, 'textarea.ember-text-area.ember-view').clear()
        # Отправим своё решение задачи на проверку.
        browser.find_element(By.CSS_SELECTOR, 'textarea.ember-text-area.ember-view').send_keys(answer)
        browser.find_element(By.CSS_SELECTOR, 'button.submit-submission').click()
        time.sleep(5)  # Не нужен. Поставил, чтобы наглядно увидеть результат проверки решения задачи.
        browser.close()
    else:
        print('Задача уже успешно выполнена! Проверьте, верна ли указана ссылка на страницу с заданием?')
        print("Ваш ответ на задание можно скопировать здесь: ", answer)
        browser.close()
