import re

import pyperclip
from selenium.webdriver.common.by import By


def get_xpath(driver, element):
    """Генерация короткого XPATH для элемента с приоритетом поиска по id, тексту, name и другим атрибутам, а также выводом placeholder."""
    first_tag = element.tag_name.lower()
    if first_tag == "svg":
        tag = "*"
    else:
        tag = first_tag


    def is_dynamic_attribute(value):
        # Проверка на динамически сгенерированные атрибуты, например id со случайными числами
        return bool(re.search(r'\d+', value))

    # Приоритет 1: Поиск по id
    element_id = element.get_attribute("id")
    if element_id and not is_dynamic_attribute(element_id):
        primary_xpath = f"//{tag}[@id='{element_id}']"
    else:
        # Приоритет 2: Поиск по тексту
        text = element.text.strip()
        if text and len(text) < 20:
            primary_xpath = f"//{tag}[contains(text(), '{text}')]"
        else:
            # Приоритет 3: Поиск по name
            element_name = element.get_attribute("name")
            if element_name:
                primary_xpath = f"//{tag}[@name='{element_name}']"
            else:
                # Приоритет 4: Поиск по классам
                element_class = element.get_attribute("class")
                siblings = driver.find_elements(By.XPATH, f"//*[@class='{element_class}']")
                classes = ".".join(element_class.split())
                if element_class:
                    xpath = f"//{tag}[contains(@class, '{classes}')]"
                # else:
                # Приоритет 5: Индексация среди тегов одного типа

                    if len(siblings) > 1:
                        index = siblings.index(element) + 1
                        primary_xpath = f"{xpath}[{index}]"
                else:
                    primary_xpath = f"//{tag}[contains(@class, '{classes}')]"

    # Placeholder локатора, если он есть
    placeholder = element.get_attribute("placeholder")
    placeholder_xpath = f"//{tag}[@placeholder='{placeholder}']" if placeholder else ""

    return primary_xpath + ("\n" + "Placeholder: " + placeholder_xpath if placeholder_xpath else "")


def get_css_selector(driver, element):
    """Генерация короткого CSS селектора для элемента с приоритетом поиска по id, тексту, name и другим атрибутам, а также выводом placeholder."""
    tag = element.tag_name.lower()

    # Основной CSS локатор
    primary_css = ""

    # Приоритет 1: Поиск по id
    element_id = element.get_attribute("id")
    if element_id:
        primary_css = f"{tag}#{element_id}"
    else:
        # Приоритет 2: Поиск по тексту (CSS не поддерживает прямой поиск по тексту)
        text = element.text.strip()
        if text and len(text) < 50:
            primary_css = f"{tag}:contains('{text}')"
        else:
            # Приоритет 3: Поиск по name
            element_name = element.get_attribute("name")
            if element_name:
                primary_css = f"{tag}[name='{element_name}']"
            else:
                # Приоритет 4: Поиск по классам
                element_class = element.get_attribute("class")
                if element_class:
                    classes = ".".join(element_class.split())
                    primary_css = f"{tag}.{classes}"
                else:
                    # Приоритет 5: Индексация среди тегов одного типа
                    siblings = driver.find_elements(By.CSS_SELECTOR, tag)
                    if len(siblings) > 1:
                        index = siblings.index(element) + 1
                        primary_css = f"{tag}:nth-of-type({index})"
                    else:
                        primary_css = f"{tag}"

    # Placeholder локатор, если он есть
    placeholder = element.get_attribute("placeholder")
    placeholder_css = f"{tag}[placeholder='{placeholder}']" if placeholder else ""

    return primary_css + ("\n" + "Placeholder: " + placeholder_css if placeholder_css else "")


def copy_to_clipboard(locator):
    """Копирование локатора в буфер обмена."""
    pyperclip.copy(locator)
    print("Локатор скопирован в буфер обмена!")