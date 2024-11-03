import time

import pyperclip
import selenium
from selenium import webdriver
from selenium.common import StaleElementReferenceException, JavascriptException

from auto_loc.locators import get_xpath, get_css_selector
from auto_loc.utils import highlight_element, save_locators_to_json
from pynput import keyboard   # Для отслеживания нажатий клавиш


class WebInspector:
    def __init__(self, browser="chrome", headless=False):
        self.options = webdriver.ChromeOptions()

        if headless:
            self.options.add_argument("--headless")
        if browser == 'chrome':
            self.driver = webdriver.Chrome(options=self.options)
            # self.driver.maximize_window()
        else:
            raise ValueError("Currently only Chrome is supported")

        self.last_element = None  # Последний выбранный элемент
        self.exit_flag = False  # Флаг для выхода


    def start(self, url):
        """Запуск инспектора на указанной странице."""
        self.driver.get(url)
        print(f"Открыл страницу {url}")
        print("Нажмите 'q' для выхода.")
        self._inspect_page()

    def _inspect_page(self):
        """Инспектор с возможностью:
        - Одинарный клик — блокировка действия и генерация локатора.
        - Клик с Shift — стандартное взаимодействие без генерации локатора.
        - Двойной клик — стандартное взаимодействие с элементом."""

        print(
            "Инспектор запущен. "
            "Одинарный клик — блокировка действия и генерация локатора, "
            "Shift + клик — стандартное взаимодействие без генерации локатора, "
            "Двойной клик — стандартное взаимодействие.")

        # Слушаем клики на странице
        self.driver.execute_script("""
                document.addEventListener('click', function(event) {
                    console.log('Click event detected');
                    if (event.detail === 1) {  // Одинарный клик
                        console.log('Single click detected');
                        if (!event.shiftKey) {  // Одинарный клик без Shift
                            console.log('Single click without Shift detected');
                            let element = event.target;
                            window.element_path = element;  // Сохраняем элемент в глобальной переменной
                            event.preventDefault();  // Блокируем стандартное действие клика
                            event.stopPropagation();  // Останавливаем дальнейшую обработку события
                        } else if (event.shiftKey) {  // Клик с Shift
                            console.log('Click with Shift detected');
                            // Оставляем стандартное поведение без сохранения элемента
                            return;  // Ничего не делаем, стандартное поведение браузера
                        }
                    }
                }, true);

                document.addEventListener('dblclick', function(event) {
                    console.log('Double click detected');
                    // Двойной клик: Оставляем стандартное поведение
                }, true);
            """)

        # Устанавливаем обработчик для клавиши 'q'
        listener = keyboard.Listener(on_press=self._on_key_press)
        listener.start()  # Запускаем слушатель в отдельном потоке

        retry_count = 0  # Счётчик повторных попыток
        max_retries = 2  # Максимальное количество попыток

        # Основной цикл работы инспектора
        while not self.exit_flag:
            try:
                element = self.driver.execute_script("return window.element_path;")

                # Проверяем, есть ли новый клик и отличается ли он от предыдущего элемента
                if element and element != self.last_element:
                    self.last_element = element
                    self._highlight_and_generate_locator(element)
                    retry_count = 0  # Сбрасываем счётчик при успешной операции
                    # Сбрасываем переменную в браузере, чтобы ждать новый клик
                    self.driver.execute_script("window.element_path = null;")

            except selenium.common.exceptions.StaleElementReferenceException as e:
                print(f"Stale element: {str(e)}. Попытка {retry_count + 1} из {max_retries}")
                retry_count += 1
                if retry_count >= max_retries:
                    print("Пропускаем элемент из-за устаревания.")
                    retry_count = 0
                    # Сбрасываем переменную в браузере
                    self.driver.execute_script("window.element_path = null;")
                    self.last_element = None  # Обнуляем последний элемент, чтобы искать новый

            except selenium.common.exceptions.JavascriptException as e:
                print(f"Ошибка JavaScript: {str(e)}")
                retry_count += 1
                if retry_count >= max_retries:
                    print("Пропускаем элемент из-за ошибки JavaScript.")
                    retry_count = 0
                    # Сбрасываем переменную в браузере
                    self.driver.execute_script("window.element_path = null;")
                    self.last_element = None

            except Exception as e:
                print(f"Общая ошибка: {str(e)}")
                retry_count += 1
                if retry_count >= max_retries:
                    print("Пропускаем элемент из-за общей ошибки.")
                    retry_count = 0
                    # Сбрасываем переменную в браузере
                    self.driver.execute_script("window.element_path = null;")
                    self.last_element = None

            time.sleep(0.5)  # Ждем перед следующей проверкой

        print("Выход из инспектора...")
        listener.stop()  # Останавливаем слушатель после выхода


    def _highlight_and_generate_locator(self, element):
        """Подсвечивание и генерация локатора с обработкой StaleElementReferenceException."""
        try:
            # Переобновляем элемент, если он стал устаревшим
            if not self._is_element_stale(element):
                # Подсвечиваем элемент
                highlight_element(self.driver, element)

                # Генерируем оба локатора
                xpath = get_xpath(self.driver, element)
                css_selector = get_css_selector(self.driver, element)

                # Выводим локаторы
                print(f"\nXPATH локатор: {xpath}")
                print(f"CSS локатор: {css_selector}")

                # Копируем XPATH в буфер обмена
                pyperclip.copy(xpath)
                print("XPATH локатор скопирован в буфер обмена!")

                # Сохраняем локаторы в файл
                save_locators_to_json(xpath, css_selector)
            else:
                print("Элемент устарел. Повторный поиск элемента.")
                # Переобновляем элемент (например, находим его снова)
                # element = self.driver.find_element(By.XPATH, "...") # пример поиска элемента заново
        except StaleElementReferenceException:
            print("Ошибка: Элемент устарел и недоступен. Попробуйте кликнуть снова.")
        except JavascriptException as e:
            print(f"Ошибка JavaScript: {e}")

    def _is_element_stale(self, element):
        """Проверка, является ли элемент устаревшим."""
        try:
            # Проверяем, доступен ли элемент
            element.is_enabled()
            return False
        except StaleElementReferenceException:
            return True

    def _on_key_press(self, key):
        """Устанавливает флаг выхода при нажатии 'q'."""
        try:
            if key.char == 'q':
                self._set_exit_flag()
                print("\nExit flag set to True.")
        except AttributeError:
            pass

    def _set_exit_flag(self):
        """Установка флага выхода при нажатии 'q'."""
        print("\nВыход из инспектора...")
        self.exit_flag = True

    def quit(self):
        """Закрытие браузера."""
        self.driver.quit()


# Пример использования
if __name__ == "__main__":
    # url = input("Введите URL для инспекции: ")
    # url = "https://demoqa.com/automation-practice-form"
    url = "https://3d4medical.com/"
    inspector = WebInspector()
    inspector.start(url)
    inspector.quit()
