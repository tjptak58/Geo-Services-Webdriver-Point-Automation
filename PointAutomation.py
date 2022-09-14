import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException


#Open chrome and go to ArcGis Online
driver=webdriver.Chrome()
driver.get("https://www.arcgis.com/index.html")

#Navigate to and open the map
driver.find_element(By.XPATH,"//button[contains(@class, 'esri-header-account-control esri-header-account-control--signin')]").click()
driver.implicitly_wait(200)
driver.find_element(By.XPATH,"//input[@id='user_username']").send_keys("drew@geoservicesinc.net")
driver.find_element(By.XPATH,"//input[@id='user_password']").send_keys("Joseph232323*")
driver.find_element(By.XPATH,"//button[@id='signIn']").click()
driver.find_element(By.XPATH,"//a[@id='esri-header-menus-link-desktop-0-1']").click()
driver.find_element(By.XPATH,"//a[contains(@class, 'card-image-wrap card-last js-default-open')]").click()

#In ArcGIS, Navigate to a project name, Open the table, and take each of the names
#Click out of popup
driver.find_element(By.XPATH,"""//*[@id="dijit_form_Button_2_label"]""").click()
driver.implicitly_wait(700)

################################################INPUTS####################################################
pdftitle= "20122 PDF"#PDF title for sync
driver.find_element(By.XPATH,"""//*[@id="csv_3968_title"]""").click()  #XPATH for Title of specific Project in ARCGIS
driver.find_element(By.XPATH,"""//*[@id="csv_3968_tableTool"]/span""").click() #XPATH for Table Icon For Project
count=driver.find_element(By.XPATH,"""//*[@id="dijit_layout_ContentPane_4"]/div[4]""").text #XPATH for Content ID for project
num=int(count[-15:-14]) #Gets number of elements in the arcgis project 15(one digit) 16(2 digits) 17(three digits)
print(num)
################################################INPUTS####################################################

#proxyClick=str(num-1)
#driver.find_element(By.XPATH,"""//*[@id="dgrid_0-row-"""+proxyClick+""""]/table/tr/td[3]""").click() #click second to last
pdfs=[]
for x in range(int(num)):
        try:
                a=str(x)
                driver.find_element_by_xpath("""//*[@id="dgrid_0-row-"""+a+""""]/table/tr/td[3]/div""").click()
                pdfname=driver.find_element_by_xpath("""//*[@id="dgrid_0-row-"""+a+""""]/table/tr/td[3]/div""").text
                pdfs.append(pdfname)
        except AttributeError as exception:
                print("sheet")


                
#Open a new tab and navigate to Sync.com login page
driver2=webdriver.Chrome()
driver2.get("https://cp.sync.com/login?return_to=%252Ffiles%252F")
driver2.implicitly_wait(20)
driver2.find_element(By.XPATH,"//input[@id='text-auth-email']").send_keys("drewptak@geoservicesinc.net")
driver2.find_element(By.XPATH,"//input[@id='text-auth-password']").send_keys("Joseph23*")
driver2.find_element(By.XPATH,"//button").click()
driver2.find_element(By.XPATH,"//span[contains(@class, 'filelink showhand tool')]").click()
##driver2.find_element(By.XPATH,"""//li[contains(@class, 'pagination-next')]/a""").click()  #IF ITS ON PAGE 2
driver2.find_element_by_css_selector("[title='"+pdftitle+"']").click()

#Copy the url from a specific PDF
counter=0
switcher=0
for pdf in pdfs:
        index=str(counter)
        print(driver2.title)
        driver2.implicitly_wait(20)
        name=pdf + '.pdf'
        action = ActionChains(driver2)
        try:
                anchor = driver2.find_element_by_css_selector("[title='"+name+"']")
                driver2.implicitly_wait(20)
                action.move_to_element(anchor).perform()
                action.move_to_element_with_offset(anchor, 760, 10)
                action.click()
                action.perform()
                action.move_to_element_with_offset(anchor, 750, 62)
                action.click()
                action.perform()
                driver2.implicitly_wait(4000)
                driver2.find_element(By.XPATH,"/html/body/ngb-modal-window/div/div/sync-dialog-link/sync-link-manage/div[2]/div[1]/div/div/button[1]").click()
                driver2.find_element(By.XPATH,"//button[contains(@class, 'close')]/span").click()
                driver2.implicitly_wait(4000)

                #Navigate out of Sync and back to ArcGIS online to paste the link
                print(driver.title)
                print(index)
                print(name)
                driver.implicitly_wait(2000)
                bubble=driver.find_element_by_xpath("""//*[@id="dgrid_0-row-"""+index+""""]/table/tr/td[6]""")
                newaction=ActionChains(driver)
                newaction.double_click(bubble)
                newaction.perform()
                linktext=text = pyperclip.paste()
                driver.find_element(By.XPATH,"""//input[@id='dijit_form_ValidationTextBox_"""+index+"""']""").send_keys(linktext)
                driver.find_element_by_xpath("""//*[@id="dgrid_0-row-"""+index+""""]/table/tr/td[5]""").click()
                switch=str(switcher)
                if (switcher%100)>3:
                        dropper=str(((switcher%100)-4)*73)
                        driver2.execute_script("window.scrollTo(0,"+dropper+")")
                if ((switcher+1)%100)==0 and (switcher>0):
                        driver.implicitly_wait(30000)
                counter=counter+1
                switcher=switcher+1
        except NoSuchElementException as exception:
                print(driver.title)
                print("exception")
                driver.implicitly_wait(2000)
                bubble=driver.find_element_by_xpath("""//*[@id="dgrid_0-row-"""+index+""""]/table/tr/td[6]""")
                newaction=ActionChains(driver)
                
                newaction.double_click(bubble)
                newaction.perform()
                driver.find_element(By.XPATH,"""//input[@id='dijit_form_ValidationTextBox_"""+index+"""']""").send_keys("Log Not Found")
                driver.find_element_by_xpath("""//*[@id="dgrid_0-row-"""+index+""""]/table/tr/td[4]""").click()
                counter=counter+1
                
        
print("done")

