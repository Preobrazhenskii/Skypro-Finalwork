from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import allure 


browser = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()))
base_url = "https://www.chitai-gorod.ru/"

@allure.title("Поиск книги через каталог")
@allure.description("Проверка перехода в каталог и отображения списка товаров")
@allure.feature("UI Тесты. Каталог")
@allure.severity(allure.severity_level.CRITICAL)
def test_find_book_from_catalog():
    with allure.step("Открытие главной страницы читай-город в полноразмерном окне"):
        browser.get(base_url)
        browser.maximize_window()
        waiter = WebDriverWait(browser, 15)

    with allure.step ("Закрытие уведомления о городе"): 
        browser.find_element(By.CSS_SELECTOR, ".header-location").click()
    with allure.step ("Переход в каталог"):
        catalog_button = waiter.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.catalog-btn__icon'))
        )
        catalog_button.click()
    with allure.step('Нажатие на кнопку "Смотреть все товары"'):
        all_catgories = waiter.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.head-categories-menu__subtitle'))
        )
        all_catgories.click()
    with allure.step("Проверка отображения результата"): 
        result = waiter.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.app-products-list'))
        )
    assert result.is_displayed()

@allure.title("Поиск по частичному названию")
@allure.description("Проверка поиска книги по неполному названию")
@allure.feature("UI Тесты. Поиск")
@allure.severity(allure.severity_level.CRITICAL)
def test_find_book_by_partial_title():
    with allure.step("Открытие главной страницы читай-город в полноразмерном окне"):
        browser.get(base_url)
        browser.maximize_window()
        waiter = WebDriverWait(browser, 15)

    with allure.step("Закрытие уведомления о городе"): 
        browser.find_element(By.CSS_SELECTOR, ".header-location").click()

    with allure.step("Ввод имени в поиске"):
        browser.find_element(By.CSS_SELECTOR, "#app-search").send_keys("Войн мир")

    with allure.step("Поиск товаров"):
        search_click = waiter.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type=submit]'))
        )
        search_click.click()

    with allure.step("Проверка результатов поиска"): 
        result = waiter.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[title="Война и мир. Книга 2 (Лев Толстой)"]'))
        )
    assert result.is_displayed()

@allure.title("Поиск через выпадающий список подсказок")
@allure.description("Проверка, что клик по подсказке приводит к результатам поиска")
@allure.feature("UI Тесты. Поиск")
@allure.severity(allure.severity_level.NORMAL)
def test_suggestion_book_search():
    with allure.step("Открытие главной страницы читай-город в полноразмерном окне"):
        browser.get(base_url)
        browser.maximize_window()
        waiter = WebDriverWait(browser, 15)

    with allure.step("Закрытие уведомления о городе"): 
        browser.find_element(By.CSS_SELECTOR, ".header-location").click()

    with allure.step("Ввод имени в поиске"):
        browser.find_element(By.CSS_SELECTOR, "#app-search").send_keys("Чебур")
    with allure.step("Поиск товаров из выпадающего списка"):
        suggestions = waiter.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.suggests-list__link'))
        )
        suggestions[0].click()

    with allure.step("Проверка результатов поиска"):
        result = waiter.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[title="Чебурашка (Эдуард Успенский)"]'))
        )
        
    assert result.is_displayed()

@allure.title("Добавление одной книги в корзину")
@allure.description("Проверка, что книга добавляется в корзину и счётчик обновляется")
@allure.feature("UI Тесты. Корзина")
@allure.severity(allure.severity_level.CRITICAL)
def test_add_book_to_cart():
    with allure.step("Открытие главной страницы читай-город в полноразмерном окне"):
        browser.get(base_url)
        browser.maximize_window()
        waiter = WebDriverWait(browser, 15)
    with allure.step("Закрытие уведомления о городе"): 
        browser.find_element(By.CSS_SELECTOR, ".header-location").click()
    with allure.step("Переход в каталог"):
        catalog_button = waiter.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.catalog-btn__icon'))
        )
        catalog_button.click()
    with allure.step('Нажатие на кнопку "Смотреть все товары"'):
        all_catgories = waiter.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.head-categories-menu__subtitle'))
        )
        all_catgories.click()
    with allure.step("Переход на страницу с описанием книги"):
        book_card = waiter.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'a[title="Скорбь Сатаны (Мария Корелли)"]'))
        )
        book_card.click()
    with allure.step('Нажатие на кнопку "Купить"'):
        buy_button = waiter.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '.product-buttons.product-offer__buttons'))
        )
        buy_button.click()
    with allure.step("Проверка отображения книги в корзине"):
        cart_indicator = waiter.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '.header-controls__indicator'))
        )
    
    assert cart_indicator.text == "1"

@allure.title("Удаление товара из корзины")
@allure.description("Проверка, что товар удаляется и корзина становится пустой")
@allure.feature("UI Тесты. Корзина")
@allure.severity(allure.severity_level.CRITICAL)
def test_book_delete_from_cart():
    with allure.step("Открытие главной страницы читай-город в полноразмерном окне"):
        browser.get(base_url)
        browser.maximize_window()
        waiter = WebDriverWait(browser, 15)

    with allure.step("Закрытие уведомления о городе"): 
        browser.find_element(By.CSS_SELECTOR, ".header-location").click()

    with allure.step("Ввод имени в поиске"):
        browser.find_element(By.CSS_SELECTOR, "#app-search").send_keys("1984")

    with allure.step("Поиск товаров"):
        search_click = waiter.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type=submit]'))
        )
        search_click.click()

    with allure.step("Переход на страницу с описанием книги"):
        book_card = waiter.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'a[title="1984 (новый перевод) (Джордж Оруэлл)"]'))
        )
        book_card.click()
    
    with allure.step('Нажатие на кнопку "Купить"'):
        buy_button = waiter.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '.product-buttons.product-offer__buttons'))
        )
        buy_button.click()

    with allure.step("Переход на страницу корзины"):
        cart_icon = waiter.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Корзина"]'))
        )
        cart_icon.click()

    with allure.step("Удаление книги из корзины"): 
        delete_button = waiter.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.cart-item__delete-button'))
        )
        delete_button.click()

    with allure.step("Обновление страницы"): 
        browser.refresh()

    empty_cart = waiter.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h4.catalog-stub__title"))
    )
    assert empty_cart.text == "В корзине ничего нет"