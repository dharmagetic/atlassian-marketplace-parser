import time

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

from django.conf import settings

from marketplace_parser.models import Vendor, Addon


def get_vendor_name(browser, url):
    relative_url = '/'.join(url.split('/')[4:])
    css_selector = "a[href*='{}']".format(relative_url)
    url = browser.find_element_by_css_selector(css_selector)
    # Save the window opener (current window, do not mistaken with tab... not the same)
    main_window = browser.current_window_handle
    # Open the link in a new tab by sending key strokes on the element
    # Use: Keys.CONTROL + Keys.SHIFT + Keys.RETURN to open tab on top of the stack
    url.send_keys(Keys.CONTROL + Keys.RETURN)
    # Switch tab to the new tab, which we will assume is the next one on the right
    browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
    # Put focus on current window which will, in fact, put focus on the current visible tab
    # browser.switch_to_window(main_window)
    tabs = browser.window_handles
    browser.switch_to.window(tabs[1])
    vendor_name = browser.find_element_by_class_name('plugin-vendor-name').text
    # Close current tab
    browser.close()
    # browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
    # Put focus on current window which will be the window opener
    browser.switch_to_window(main_window)

    return vendor_name


def parse_download_count_string(count_string):
    count_string = count_string.split(' ')[0]
    if 'k' in count_string:
        return int(float(count_string.replace('k', '')) * 1000)
    else:
        return int(count_string)


def get_downloads_count(addon_block_html):
    try:
        downloads_count_string = addon_block_html\
            .find_element_by_class_name(settings.MARKETPLACE_PARSER_ADDON_DOWNLOAD_COUNT_CSS_CLASS).text
    except NoSuchElementException:
        downloads_count_string = '0'
    count = parse_download_count_string(downloads_count_string)
    return count


def parse_addon(browser, addon_block_html, addons):
    addon_name = addon_block_html\
        .find_element_by_class_name(settings.MARKETPLACE_PARSER_ADDON_NAME_CSS_CLASS).text
    addon_url = addon_block_html\
        .find_element_by_class_name(settings.MARKETPLACE_PARSER_ADDON_URL_CSS_CLASS).get_attribute('href')
    vendor_name = get_vendor_name(browser, addon_url)
    downloads_count = get_downloads_count(addon_block_html)

    vendor = Vendor.objects.get_or_create(name=vendor_name)[0]
    addon = Addon.objects.create(vendor=vendor, name=addon_name, link=addon_url, downloads_count=downloads_count)


def parse():
    # Turn off images
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome(chrome_options=chrome_options)

    browser.get(settings.MARKETPLACE_PARSER_TOP_SELLING_ADDONS_URL)

    load_more_button = browser.find_element_by_class_name(settings.MARKETPLACE_PARSER_LOAD_MORE_BUTTON_CSS_CLASS)
    addons_html_content = browser.find_elements_by_class_name(settings.MARKETPLACE_PARSER_ADDON_CONTENT_CSS_CLASS)
    addons_total_count = 1000


    while len(addons_html_content) < addons_total_count:
        try:
            load_more_button.click()
        except StaleElementReferenceException:
            pass
        # I'm too lazy to use explicit Selenium waits
        time.sleep(2)
        addons_html_content = browser.find_elements_by_class_name(settings.MARKETPLACE_PARSER_ADDON_CONTENT_CSS_CLASS)
        print len(addons_html_content)

    parsed_addons = []
    for addon in addons_html_content:
        parse_addon(browser, addon, parsed_addons)

    browser.close()


if __name__ == "__main__":
    parse()
