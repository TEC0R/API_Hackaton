from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Reglage et lancement du webdriver pour selenium

options = webdriver.ChromeOptions()

options.add_argument("--headless")  # Mode sans affichage
options.add_argument("--incognito")  # Mode incognito
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")  # Agent utilisateur

service = webdriver.chrome.service.Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

def deepl(texte, langue, trad): 
    link = f"https://www.deepl.com/fr/translator#{langue}/{trad}/{texte}"
    driver.get(link)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='textareasContainer']/div[3]/section/div[1]/d-textarea/div/p/span"))
    )
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    result = soup.find("div", {"class" : "rounded-inherit mobile:min-h-0 relative flex flex-1 flex-col"}).find("span").text
    return {langue : texte , trad : result}
