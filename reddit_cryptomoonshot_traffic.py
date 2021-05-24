import time
import urllib
from random import randint

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

PROXY = '62.210.205.97:19018'  # SET PROXY HERE

total_visit = 0

VISIT_TROUGH_GOOGLE = 1
VISIT_TROUGH_CMS = 2

def set_viewport_size(driver, width, height):
    window_size = driver.execute_script("""
        return [window.outerWidth - window.innerWidth + arguments[0],
          window.outerHeight - window.innerHeight + arguments[1]];
        """, width, height)
    driver.set_window_size(*window_size)

def gather_tendie_links(driver):
    links = []

    driver.get("https://www.reddit.com/search/?q=TendieSwap")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        overlay = driver.find_element_by_xpath('//*[@id="SHORTCUT_FOCUSABLE_DIV"]/div[3]/div[2]')
        driver.execute_script("arguments[0].style.display='none'", overlay) # Remove the EU cookie consent visibility because it obscures the page
    except Exception as e:
        pass

    link_elements = driver.find_elements_by_xpath('//a[@data-click-id="body"]')
    for link_element in link_elements:
        links.append(link_element.get_attribute('href'))

    return links

def get_webdriver():
    #firefoxOpt = new FirefoxOptions()
    firefox_profile = webdriver.FirefoxProfile()

    # Set of options, maybe its speed up the load time
    firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
    firefox_profile.set_preference("network.http.pipelining", True)
    firefox_profile.set_preference("network.http.proxy.pipelining", True)
    firefox_profile.set_preference("network.http.pipelining.maxrequests", 8)
    firefox_profile.set_preference("content.notify.interval", 500000)
    firefox_profile.set_preference("content.notify.ontimer", True)
    firefox_profile.set_preference("content.switch.threshold", 250000)
    firefox_profile.set_preference("browser.cache.memory.capacity", 65536) # Increase the cache capacity.
    firefox_profile.set_preference("browser.startup.homepage", "about:blank")
    firefox_profile.set_preference("reader.parse-on-load.enabled", False) # Disable reader, we won't need that.
    firefox_profile.set_preference("browser.pocket.enabled", False) # Duck pocket too!
    firefox_profile.set_preference("loop.enabled", False)
    firefox_profile.set_preference("browser.chrome.toolbar_style", 1) # Text on Toolbar instead of icons
    firefox_profile.set_preference("browser.display.show_image_placeholders", False) # Don't show thumbnails on not loaded images.
    firefox_profile.set_preference("browser.display.use_document_colors", False) # Don't show document colors.
    firefox_profile.set_preference("browser.display.use_document_fonts", 0) # Don't load document fonts.
    firefox_profile.set_preference("browser.display.use_system_colors", True) # Use system colors.
    firefox_profile.set_preference("browser.formfill.enable", False) # Autofill on forms disabled.
    firefox_profile.set_preference("browser.helperApps.deleteTempFileOnExit", True) # Delete temprorary files.
    firefox_profile.set_preference("browser.shell.checkDefaultBrowser", False)
    firefox_profile.set_preference("browser.startup.homepage", "about:blank")
    firefox_profile.set_preference("browser.startup.page", 0) # blank
    firefox_profile.set_preference("browser.tabs.forceHide", True) # Disable tabs, We won't need that.
    firefox_profile.set_preference("browser.urlbar.autoFill", False) # Disable autofill on URL bar.
    firefox_profile.set_preference("browser.urlbar.autocomplete.enabled", False) # Disable autocomplete on URL bar.
    firefox_profile.set_preference("browser.urlbar.showPopup", False) # Disable list of URLs when typing on URL bar.
    firefox_profile.set_preference("browser.urlbar.showSearch", False) # Disable search bar.
    firefox_profile.set_preference("extensions.checkCompatibility", False) # Addon update disabled
    firefox_profile.set_preference("extensions.checkUpdateSecurity", False)
    firefox_profile.set_preference("extensions.update.autoUpdateEnabled", False)
    firefox_profile.set_preference("extensions.update.enabled", False)
    firefox_profile.set_preference("general.startup.browser", False)
    firefox_profile.set_preference("plugin.default_plugin_disabled", False)
    firefox_profile.set_preference("permissions.default.image", 2) # Image load disabled again

    #print(PROXY)
    webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
        "httpProxy": PROXY,
        "proxyType": "MANUAL",
    }
    from selenium.webdriver.firefox.options import Options
    options = Options()
    options.add_argument("--headless")
    from fake_useragent import UserAgent
    ua = UserAgent()
    a = ua.random
    user_agent = ua.random
    #print(user_agent)
    options.add_argument(f'user-agent={user_agent}')
    try:
        driver = webdriver.Firefox(firefox_profile=firefox_profile, options=options)
    except:
        time.sleep(1)
        driver = webdriver.Firefox(firefox_profile=firefox_profile, options=options)
    set_viewport_size(driver, 1660, 1150)

    return driver
    

def visit_from_cryptomoonshot(driver, link):
    driver.get("https://www.reddit.com/search/?q=TendieSwap")
    #time.sleep(2)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        overlay = driver.find_element_by_xpath('//*[@id="SHORTCUT_FOCUSABLE_DIV"]/div[3]/div[2]')
        driver.execute_script("arguments[0].style.display='none'", overlay) # Remove the EU cookie consent visibility because it obscures the page
    except Exception as e:
        pass

    cms = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "{}")]//../../../../../..'.format(link.replace('https://www.reddit.com', '')))))

    cms.click()
    time.sleep(randint(3, 4))

def visit_from_google(driver, link):
    driver.get('https://www.google.com/search?q=' + link)

    try:
        overlay = driver.find_element_by_xpath('//*[@id="xe7COe"]')
        driver.execute_script("arguments[0].style.display='none'", overlay) # Remove the EU cookie consent visibility because it obscures the page
    except Exception as e:
        pass

    cms = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="rso"]/div/div/div/div/div[1]/a')))

    cms.click()
    time.sleep(randint(3, 4))

# Get all tendie links from reddit
driver = get_webdriver()
tendie_reddit_links = gather_tendie_links(driver)
print("*****************************************************")
print("The following links will be visited:")
for link in tendie_reddit_links:
    print(link)
print("*****************************************************")
driver.close()
driver.quit()
time.sleep(1)
del driver

for i in range(10000):
    driver = get_webdriver()
    # Open URL
    visit_rnd = randint(1, 2)
    if visit_rnd == VISIT_TROUGH_GOOGLE:
        for link in tendie_reddit_links:
            try:
                visit_from_google(driver, link)
                print("{} - visited".format(link))
                total_visit += 1
            except Exception as e:
                print("{} - cannot be visited due to some error")

    else:
        for link in tendie_reddit_links:
            try:
                visit_from_cryptomoonshot(driver, link)
                print("{} - visited".format(link))
                total_visit += 1
            except Exception as e:
                print("{} - cannot be visited due to some error")

    driver.close()
    driver.quit()
    time.sleep(1)

print("************************************")
print("* Total visits: ", total_visit)