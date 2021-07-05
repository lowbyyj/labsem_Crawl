from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('uurl', type=str)

args = parser.parse_args()

paperURL = args.uurl

driver = webdriver.Chrome('C:/Users/Administrator/Documents/crmDriver/chromedriver.exe')
driver.implicitly_wait(3)

driver.get(paperURL)
driver.implicitly_wait(5)

title = driver.find_element_by_xpath("//h1[@class='document-title']")
paperFileName = title.text
#paperFileName = 'bless'
paperFilePath = 'C:/Users/Administrator/Documents/vsCode/labsemTXT/' + paperFileName + '.txt'

f = open(paperFilePath,'w',-1,"utf-8")

abst = driver.find_element_by_xpath("//div[@class='u-mb-1']")
f.write(abst.text)
f.write('\n\n')

driver.implicitly_wait(15)
# while section name
# section existence
sectionOpen = "//div[@class='section' and @id='sec"
sectionClose = "']"
sectionNum = 1
sectionDir = sectionOpen+str(sectionNum)+sectionClose
while True:
    try:
        sectionDir = sectionOpen+str(sectionNum)+sectionClose
        section = driver.find_element_by_xpath(sectionDir)
        f.write(section.text)
        f.write('\n\n')
        print('Section Number '+str(sectionNum)+' Collecting -> Finished')
        sectionNum = sectionNum+1
    except:
        print('Text Loading Finished')
        break

time.sleep(10)

driver.close()
f.close()

print('Initalize Summarization')

driverS = webdriver.Chrome('C:/Users/Administrator/Documents/crmDriver/chromedriver.exe')
driverS.implicitly_wait(3)

driverS.get('https://summariz3.herokuapp.com/')
driverS.implicitly_wait(5)

fr = open(paperFilePath,'r',-1,'utf-8')

paperFilePathS = 'C:/Users/Administrator/Documents/vsCode/labsemTXT/' + paperFileName + '_summary.txt'
fs = open(paperFilePathS,'w',-1,"utf-8")

lines = fr.readlines()
chunk = ""

for line in lines:
    if(len(line)<25):
        fs.write(line)
        fs.write("\n\n")
    elif(len(line)>100):
        chunk = chunk+line
        if(len(chunk)>800):
            box = driverS.find_element_by_name('content')
            box.clear()
            box.send_keys(chunk)
            driverS.find_element_by_xpath("//button[@class='v-btn v-btn--depressed v-btn--flat v-btn--outlined theme--light v-size--default primary--text' and @type='submit']").click()
            driverS.implicitly_wait(10)
            result = driverS.find_elements_by_class_name("v-card__text")
            latter = result.find_elements_by_tag_name('ol')
            fs.write(latter.text)
            fs.write("\n\n")
            driverS.implicitly_wait(5)
            chunk=""

time.sleep(10)

driverS.close()
