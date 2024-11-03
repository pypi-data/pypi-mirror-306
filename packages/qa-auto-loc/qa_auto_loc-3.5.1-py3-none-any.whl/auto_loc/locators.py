import re

import pyperclip
from selenium.webdriver.common.by import By


def get_xpath(driver, element):
    """Генерация короткого XPATH для элемента с приоритетом поиска по id, тексту, name и другим атрибутам, а также выводом placeholder."""
    first_tag = element.tag_name.lower()
    if first_tag == "svg" or len(first_tag) < 3 or first_tag == "path":
        tag = "*"
    else:
        tag = first_tag


    def is_dynamic_attribute(value):
        # Проверка на динамически сгенерированные атрибуты, например id со случайными числами
        return value.isdigit() or re.match(r".*-\d+", value)

    def generate_primary_xpath():
        # Priority 0: Search by data-e2e and test-id
        data_e2e = element.get_attribute("data-e2e")
        test_id = element.get_attribute("test-id")
        if data_e2e:
            return f"//{tag}[@data-e2e='{data_e2e}']"
        elif test_id:
            return f"//{tag}[@test-id='{test_id}']"
        else:
            # Priority 1: Search by id
            element_id = element.get_attribute("id")
            if element_id and not is_dynamic_attribute(element_id):
                return f"//{tag}[@id='{element_id}']"
            else:
                # Priority 2: Search by text
                text = element.text.strip()
                if text and len(text) < 20:
                    return f"//{tag}[contains(text(), '{text}')]"
                else:
                    # Priority 3: Search by name
                    element_name = element.get_attribute("name")
                    if element_name:
                        return f"//{tag}[@name='{element_name}']"
                    else:
                        # Priority 4: Search by classes
                        element_class = element.get_attribute("class")
                        siblings = driver.find_elements(By.XPATH, f"//*[@class='{element_class}']")
                        classes = ".".join(element_class.split())
                        if element_class:
                            xpath = f"//{tag}[contains(@class, '{classes}')]"
                            if len(siblings) > 1:
                                index = siblings.index(element) + 1
                                return f"{xpath}[{index}]"
                            else:
                                return xpath
                        else:
                            return f"//{tag}[contains(@class, '{classes}')]"

    primary_xpath = generate_primary_xpath()

    # Placeholder locator, if present
    placeholder = element.get_attribute("placeholder")
    placeholder_xpath = f"//{tag}[@placeholder='{placeholder}']" if placeholder else ""

    return primary_xpath + ("\n" + "Placeholder: " + placeholder_xpath if placeholder_xpath else "")


def get_css_selector(driver, element):
    """Генерация короткого CSS селектора для элемента с приоритетом поиска по id, тексту, name и другим атрибутам, а также выводом placeholder."""
    tag = element.tag_name.lower()

    def is_dynamic_attribute(value):
        # Проверка на динамически сгенерированные атрибуты, например id со случайными числами
        return value.isdigit() or re.match(r".*-\d+", value)

    # Priority 0: Search by data-e2e and test-id
    data_e2e = element.get_attribute("data-e2e")
    test_id = element.get_attribute("test-id")
    if data_e2e:
        primary_css = f"{tag}[data-e2e='{data_e2e}']"
    elif test_id:
        primary_css = f"{tag}[test-id='{test_id}']"
    else:
        # Priority 1: Search by id
        element_id = element.get_attribute("id")
        if element_id and not is_dynamic_attribute(element_id):
            primary_css = f"{tag}#{element_id}"
        else:
            # Priority 2: Search by text (CSS does not support direct text search)
            text = element.text.strip()
            if text and len(text) < 50:
                primary_css = f"{tag}:contains('{text}')"
            else:
                # Priority 3: Search by name
                element_name = element.get_attribute("name")
                if element_name:
                    primary_css = f"{tag}[name='{element_name}']"
                else:
                    # Priority 4: Search by classes
                    element_class = element.get_attribute("class")
                    if element_class:
                        classes = ".".join(element_class.split())
                        primary_css = f"{tag}.{classes}"
                    else:
                        # Priority 5: Indexing among tags of the same type
                        siblings = driver.find_elements(By.CSS_SELECTOR, tag)
                        if len(siblings) > 1:
                            index = siblings.index(element) + 1
                            primary_css = f"{tag}:nth-of-type({index})"
                        else:
                            primary_css = f"{tag}"

    # Placeholder locator, if present
    placeholder = element.get_attribute("placeholder")
    placeholder_css = f"{tag}[placeholder='{placeholder}']" if placeholder else ""

    return primary_css + ("\n" + "Placeholder: " + placeholder_css if placeholder_css else "")


def copy_to_clipboard(locator):
    """Копирование локатора в буфер обмена."""
    pyperclip.copy(locator)
    print("Локатор скопирован в буфер обмена!")