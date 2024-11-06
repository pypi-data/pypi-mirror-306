import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def translate_document(input_file_path, download_path, input_lag, output_lang):
    url = f'https://translate.google.com/?sl={input_lag}&tl={output_lang}&op=docs'

    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("window-size=1920,1080")
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("start-minimized")
    # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    # Set preferences for downloading files
    prefs = {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": False
    }
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_position(-2000, 0)
    try:
        driver.get(url)

        try:
            accept_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '//span[@class="VfPpkd-vQzf8d" and text()="Accept all"]')))
            accept_button.click()
        except:
            print("No 'Accept all' button found, continuing...")

        # Wait for the file input to be present
        drag_drop = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, '//input[@type="file"]')))

        # Use send_keys to upload the file
        drag_drop.send_keys(input_file_path)

        # Wait for the Translate button to be present and click it
        translate_button = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, '//span[@class="VfPpkd-vQzf8d" and text()="Translate"]')))
        ActionChains(driver).click(translate_button).perform()

        while True:
            try:
                download_translation = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[@class="VfPpkd-vQzf8d" and text()="Download translation"]'))
                )
                download_translation.click()
                break  # Exit the loop after clicking
            except Exception as e:
                print("Waiting for the Download translation button...")  # Debug statement
            time.sleep(1) 

        # Optionally, wait to ensure the download completes
        time.sleep(5)  # Adjust or remove if needed

    finally:
        # Close the browser
        driver.quit()