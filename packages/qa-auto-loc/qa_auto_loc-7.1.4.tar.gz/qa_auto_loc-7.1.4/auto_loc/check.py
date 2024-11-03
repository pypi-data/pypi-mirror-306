from auto_loc.inspector import WebInspector

def test_inspector(locator_attributes: list=None, url: str=None):
    inspector = WebInspector(test_attributes=locator_attributes)
    inspector.start(url)
    inspector.quit()


if __name__ == '__main__':
    url = "you_url_address"
    locator_attributes = ["data-test-id", "data-e2e", "test-id"]
    test_inspector(locator_attributes, url)
