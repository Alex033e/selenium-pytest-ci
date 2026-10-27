import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Тестовые данные
VALID_USERNAME = "tomsmith"
VALID_PASSWORD = "SuperSecretPassword!"
INVALID_USERNAME = "wronguser"
INVALID_PASSWORD = "wrongpass"

def test_successful_login(driver):
    """
    Проверяет успешный вход в систему.
    """
    driver.get("https://the-internet.herokuapp.com/login")
    
    # Находим элементы формы
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    # Ищем кнопку по типу, это надежнее
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    
    # Заполняем форму валидными данными
    username_field.send_keys(VALID_USERNAME)
    password_field.send_keys(VALID_PASSWORD)
    login_button.click()
    
    # Явное ожидание появления сообщения (защита от случайных лагов)
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "flash"))
    )
    
    # Ассерт 1: проверяем текст сообщения об успехе
    flash_message = driver.find_element(By.ID, "flash")
    assert "You logged into a secure area!" in flash_message.text
    
    # Ассерт 2: проверяем, что URL изменился на защищенный
    # Это надежнее, чем проверка заголовка в headless-режиме
    assert "secure" in driver.current_url

def test_unsuccessful_login(driver):
    """
    Проверяет неудачную попытку входа.
    """
    driver.get("https://the-internet.herokuapp.com/login")
    
    # Находим элементы формы
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    
    # Заполняем форму невалидными данными
    username_field.send_keys(INVALID_USERNAME)
    password_field.send_keys(INVALID_PASSWORD)
    login_button.click()
    
    # Ассерт: проверяем наличие сообщения об ошибке красного цвета
    error_message = driver.find_element(By.CSS_SELECTOR, ".flash.error")
    assert "Your username is invalid!" in error_message.text