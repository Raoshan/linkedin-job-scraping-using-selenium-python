import os
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
options = Options()
rawdata = os.path.join('F:\\Selenium\\rawData')
saveData = os.path.join('F:\\Selenium\\saveData')
backupData = os.path.join('F:\\Selenium\\backupData')
driver = webdriver.Chrome(executable_path=r"F:\driver\\chromedriver.exe")
df = pd.read_csv('link.csv')
data = []
def login(email,password):
    url = "https://www.linkedin.com/"
    driver.get(url)
    driver.implicitly_wait(5)
    driver.maximize_window()
    driver.find_element_by_id('session_key').send_keys(email)
    driver.find_element_by_id('session_password').send_keys(password)
    driver.find_element_by_class_name('sign-in-form__submit-button').click()
    driver.implicitly_wait(5)
 
def extractData():
    for cat in df:
        for sub in df[cat]:
            '''details link extract data...............'''
            def GetDetailsOfItem(Link):
                driver.get(Link)
                driver.implicitly_wait(10)
                try:
                    state = driver.find_element_by_class_name('jobs-unified-top-card__bullet').text
                    Located =','.join(state.split(',')[1:-1]).strip()
                    print(Located)
                except:
                    Located = "Remote"    
                try:
                    numberOfEmployees = driver.find_element_by_xpath("n//div[@class='mt5 mb2']/div[2]/spa").text
                    print(numberOfEmployees)
                except:
                    numberOfEmployees = ""    
                try:
                    companiesDescription = driver.find_element_by_xpath("//p[@class='t-14 mt5']").text
                    print(companiesDescription)
                except:
                    companiesDescription = " "    
                    driver.implicitly_wait(10)
                    return pd.Series([companiesDescription, numberOfEmployees, Located])

            url = "https://www.linkedin.com/jobs/"
            driver.get(url)
            driver.implicitly_wait(5)
            driver.find_element_by_css_selector("input[class='jobs-search-box__text-input jobs-search-box__keyboard-text-input']").send_keys(sub)
            driver.find_element_by_xpath('//*[@id="global-nav-search"]/div/div[2]/button[1]').click()
            driver.implicitly_wait(5)
            text = driver.find_element_by_xpath("//small[@class='display-flex t-12 t-black--light t-normal']").text.strip("results")
            driver.implicitly_wait(30)
            comma = text.replace(',', '')
            totalCount = int(comma)
            print(totalCount)
            # loops = int(totalCount/25)+1
            loops = 2
            print(loops)
            '''loop running................'''
            for lo in range(loops):
                actions = ActionChains(driver)
                time.sleep(5)
                '''Scraping data like jobPosition, companyofferingtheJob, Location and also detailsLink '''
                for prod in driver.find_elements_by_class_name("occludable-update"):
                    actions.move_to_element(prod).perform()
                    try:
                        jobPosition = prod.find_element_by_class_name('job-card-list__title').text
                        print(jobPosition)
                    except:
                        jobPosition = ""
                    try:
                        companyName = prod.find_element_by_class_name('job-card-container__company-name').text
                        print(companyName)
                    except:
                        companyName = ""  
                              
                    try:
                        jobLocation = prod.find_element_by_class_name('job-card-container__metadata-wrapper').find_element_by_class_name("job-card-container__metadata-item").text
                        print(jobLocation)
                    except: 
                        jobLocation = "Remote" 
                    try:
                        detailsLink = prod.find_element_by_class_name("job-card-list__title").get_attribute('href')
                        print(detailsLink)
                    except: 
                        detailsLink = "" 
                    Category = cat 
                    subCategory = sub                
                    '''Data Append.........................................'''
                    data.append([jobPosition, companyName, jobLocation, Category, subCategory, detailsLink])

                '''next page link or see more jobs link'''  
                # print("Pagination==============================================================")
                try:
                    current_page_number = driver.find_element_by_css_selector("li[class='artdeco-pagination__indicator artdeco-pagination__indicator--number active selected ember-view']").text
                    pagenumber = int(current_page_number)
                    print(f"Processing page {current_page_number}..")
                    next_page_link = driver.find_element_by_css_selector("li[class='artdeco-pagination__indicator artdeco-pagination__indicator--number active selected ember-view']").find_element_by_xpath(f'//button[span = "{pagenumber + 1}"]')
                    print(next_page_link)
                    next_page_link.click()
                except:
                    print(f"Exiting. Last page: {current_page_number}.")
                    break
            if loops == 0:
                driver.close()
                pass
            else:
                datadf = pd.DataFrame(data, columns=['jobPosition', 'companyName', 'jobLocation', 'Category', 'subCategory', 'detailsLink'])
                datadf.to_csv(os.path.join(rawdata, 'linkedin'+subCategory+'.csv'), index=False) 
                if len(datadf) == 0:
                    driver.close()
                else:
                    datadf[['companiesDescription', 'numberOfEmployees', 'Located']] = datadf[['detailsLink']].apply(lambda x: GetDetailsOfItem(x[0]), axis=1)
                    datadf = datadf[['jobPosition', 'companyName', 'jobLocation', 'companiesDescription', 'numberOfEmployees', 'Located', 'Category', 'subCategory', 'detailsLink']]
                    datadf.to_csv(os.path.join(saveData, 'linkedinDetails'+subCategory+'.csv'), index=False)
login('raoshankumarsaw@gmail.com','rdats4321')
extractData()