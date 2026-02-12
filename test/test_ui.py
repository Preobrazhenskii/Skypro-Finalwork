from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()))
base_url = "https://www.chitai-gorod.ru/"

# Поиск книги через каталог
def test_find_book_from_catalog():
    # Открытие главной страницы читай-город в полноразмерном окне
    browser.get(base_url)
    browser.maximize_window()
    waiter = WebDriverWait(browser, 15)
    # Закрытие уведомления о городе 
    browser.find_element(By.CSS_SELECTOR, ".header-location").click()
    # Переход в каталог
    catalog_button = waiter.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.catalog-btn__icon'))
    )
    catalog_button.click()
    # Нажатие на кнопку "Смотреть все товары"
    all_catgories = waiter.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.head-categories-menu__subtitle'))
    )
    all_catgories.click()
    # Проверка 
    result = waiter.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.app-products-list'))
    )
    assert result.is_displayed()

# Поиск по частичному названию. 
def test_find_book_by_partial_title():
    browser.get(base_url)
    browser.maximize_window()
    waiter = WebDriverWait(browser, 15)

    # Закрытие уведомления о городе 
    browser.find_element(By.CSS_SELECTOR, ".header-location").click()

    # Ввод имени в поиске
    browser.find_element(By.CSS_SELECTOR, "#app-search").send_keys("Войн мир")
    # Поиск товаров
    search_click = waiter.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type=submit]'))
    )
    search_click.click()
    # Проверка результатов поиска 
    result = waiter.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a[title="Война и мир. Книга 2 (Лев Толстой)"]'))
    )
    assert result.is_displayed()


# Поиск через выпадающий список подсказок.
def test_suggestion_book_search():
    browser.get(base_url)
    browser.maximize_window()
    waiter = WebDriverWait(browser, 15)

    # Закрытие уведомления о городе 
    browser.find_element(By.CSS_SELECTOR, ".header-location").click()
    # Ввод имени в поиске
    browser.find_element(By.CSS_SELECTOR, "#app-search").send_keys("Чебур")
    # Поиск товаров из выпадающего списка
    suggestions = waiter.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.suggests-list__link'))
    )
    suggestions[0].click()
    # Проверка результатов поиска
    result = waiter.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a[title="Чебурашка (Эдуард Успенский)"]'))
    )
    assert result.is_displayed()



# Добавление одной книги в корзину. 
def test_add_book_to_cart():
    # Открытие главной страницы читай-город в полноразмерном окне
    browser.get(base_url)
    browser.maximize_window()
    waiter = WebDriverWait(browser, 15)
    # Закрытие уведомления о городе 
    browser.find_element(By.CSS_SELECTOR, ".header-location").click()
    # Переход в каталог
    catalog_button = waiter.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.catalog-btn__icon'))
    )
    catalog_button.click()
    # Нажатие на кнопку "Смотреть все товары"
    all_catgories = waiter.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.head-categories-menu__subtitle'))
    )
    all_catgories.click()
    # Переход на страницу с описанием книги
    book_card = waiter.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'a[title="Скорбь Сатаны (Мария Корелли)"]'))
    )
    book_card.click()
    # Нажатие на кнопку "Купить"
    buy_button = waiter.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.product-buttons.product-offer__buttons'))
    )
    buy_button.click()
    cart_indicator = waiter.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.header-controls__indicator'))
    )
    # Проверка отображения книги в корзине
    assert cart_indicator.text == "1"

# Удаление товара из корзины.

def test_book_delete_from_cart():
    # Открытие главной страницы читай-город в полноразмерном окне
    browser.get(base_url)
    browser.maximize_window()
    waiter = WebDriverWait(browser, 15)
    # Закрытие уведомления о городе 
    browser.find_element(By.CSS_SELECTOR, ".header-location").click()
    # Ввод имени в поиске
    browser.find_element(By.CSS_SELECTOR, "#app-search").send_keys("1984")
    # Поиск товаров
    search_click = waiter.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type=submit]'))
    )
    search_click.click()
    # Переход на страницу с описанием книги
    book_card = waiter.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'a[title="1984 (новый перевод) (Джордж Оруэлл)"]'))
    )
    book_card.click()
    # Нажатие на кнопку "Купить"
    buy_button = waiter.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.product-buttons.product-offer__buttons'))
    )
    buy_button.click()
    # Переход на страницу корзины
    cart_icon = waiter.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Корзина"]'))
    )
    cart_icon.click()
    # Удаление книги из корзины 
    delete_button = waiter.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.cart-item__delete-button'))
    )
    delete_button.click()
    # Обновление страницы 
    browser.refresh()

    empty_cart = waiter.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h4.catalog-stub__title"))
    )
    assert empty_cart.text == "В корзине ничего нет"