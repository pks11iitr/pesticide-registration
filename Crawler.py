import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
# from fake_useragent import UserAgent
import time
# ~ import mysql.connector
import re
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from tkinter import *
import csv
import urllib.request
import os
import mysql.connector

driver = None
dataurl = "https://pesticides-registrationindia.nic.in/Search/frmProductSearch.aspx"
homeurl = 'https://pesticides-registrationindia.nic.in/'
loginhomeurl = 'https://pesticides-registrationindia.nic.in/UserProfile/HomePage.aspx'
productaddurl = "https://pesticides-registrationindia.nic.in/DataCaptureForms/frmProductLabelLeafletData.aspx"
productlabelurl = "https://pesticides-registrationindia.nic.in/DataCaptureForms/frmLabelLeafLetForm_UploadLabelDetail.aspx"
productleafleturl = "https://pesticides-registrationindia.nic.in/DataCaptureForms/frmLabelLeafLetForm_UploadLeafletDetail.aspx"
current_url = None
current_product = None

hostname	=	'localhost'
username	=	'pankaj'
password	=	'pankaj'
database	=	'pesticides'
conn	=	mysql.connector.connect( host=hostname, user=username, passwd=password, db=database)
productspacking = []
txtfld1 = None
txtfld2 = None
siteusername = None
sitepassword = None


class element_has_length(object):
    """An expectation for checking that an element has a particular css class.

    locator - used to find the element
    returns the WebElement once it has the particular css class
    """

    def __init__(self, locator, length):
        self.locator = locator
        self.length = length

    def __call__(self, driver):
        element = driver.find_element(*self.locator)  # Finding the referenced element
        if len(element.get_attribute('value')) == self.length:
            return element
        else:
            return False


def save_to_database(product, itemtype):
    global conn
    crsr	=	conn.cursor()

    if itemtype=='product':
        type_id=''
        toxity_id=''

        if product['itemtype']=='Acaricide':
            type_id='12'
        elif product['itemtype']=='Antibiotic':
            type_id='1'
        elif product['itemtype']=='Degesch Plates':
            type_id='10'
        elif product['itemtype']=='Fungicide':
            type_id='2'
        elif product['itemtype']=='Fungicide + Insecticide':
            type_id='13'
        elif product['itemtype']=='Herbicide':
            type_id='3'
        elif product['itemtype']=='Insecticide':
            type_id='4'
        elif product['itemtype']=='Insecticide/Acaricide':
            type_id='5'
        elif product['itemtype']=='Molluscide':
            type_id='9'
        elif product['itemtype']=='Nematicide':
            type_id='14'
        elif product['itemtype']=='Plant Growth Regulator':
            type_id='6'
        elif product['itemtype']=='Rodenticide':
            type_id='7'
        elif product['itemtype']=='Selective Post Emergence Herbicide':
            type_id='8'

        if product['toxity_class'] == 'Extremly toxic':
            toxity_id='1'
        elif product['toxity_class'] == 'Highly toxic':
            toxity_id='2'
        elif product['toxity_class'] == 'Moderly toxic':
            toxity_id='3'
        elif product['toxity_class'] == 'Slightly toxic':
            toxity_id='4'

        insert_new_product = (
        "INSERT INTO `products3`(`name`, `type`, `type_id`, `shell_life`, `toxity_class`, `toxity_id`, `intro`, `intro_h`, `direction`, `direction_h`, `precaution`, `precaution_h`, `symptoms`, `symptoms_h`, `first_aid`, `first_aid_h`, `antidote`, `antidote_h`, `storage`, `storage_h`, `disposal`, `disposal_h`, `timeapp`, `timeapp_h`, `dosage`, `dosage_h`, `toxity`, `toxity_h`) "+
        "VALUES ('"+re.escape(product['name'])+"','"+re.escape(product['itemtype'])+"','"+type_id+"','"+re.escape(product['shell_life'])+"','"+re.escape(product['toxity_class'])+"','"+toxity_id+"','"+re.escape(product['introtext'])+"','"+re.escape(product['introtext_h'])+"','"+re.escape(product['directiontext'])+"','"+re.escape(product['directiontext_h'])+"','"+re.escape(product['precautiontext'])+"','"+re.escape(product['precautiontext_h'])+"','"+re.escape(product['symptomstext'])+"','"+re.escape(product['symptomstext_h'])+"','"+re.escape(product['first_aidtext'])+"','"+re.escape(product['first_aidtext_h'])+"','"+re.escape(product['antidote'])+"','"+re.escape(product['antidote_h'])+"','"+re.escape(product['storagetext'])+"','"+re.escape(product['storagetext_h'])+"','"+re.escape(product['disposaltext'])+"','"+re.escape(product['disposaltext_h'])+"','"+re.escape(product['timeapptext'])+"','"+re.escape(product['timeapptext_h'])+"','"+re.escape(product['dosagetext'])+"','"+re.escape(product['dosagetext_h'])+"','"+re.escape(product['toxitytext'])+"','"+re.escape(product['toxitytext_h'])+"')")
        crsr.execute(insert_new_product)
        conn.commit()
        id=crsr.lastrowid
        crsr.close()
        return id
    elif itemtype=='crop':
        print(product)
        insert_new_product=("INSERT INTO `crops3`( `product_id`, `name`, `name_h`, `use_against`, `use_against_h`, `ai`, `ai_h`, `formulation`, `formulation_h`, `dilution`, `dilution_h`, `waiting`, `waiting_h`) VALUES "+ "('"+str(product['productid'])+"','"+re.escape(product['name'])+"','"+re.escape(product['name_h'])+"','"+re.escape(product['use_against'])+"','"+re.escape(product['use_against_h'])+"','"+re.escape(product['ai'])+"','"+re.escape(product['ai_h'])+"','"+re.escape(product['formulation'])+"','"+re.escape(product['formulation_h'])+"','"+re.escape(product['dilution'])+"','"+re.escape(product['dilution_h'])+"','"+re.escape(product['waiting'])+"','"+re.escape(product['waiting_h'])+"')"
        )
        crsr.execute(insert_new_product)
        conn.commit()
        id=crsr.lastrowid
        crsr.close()
        return id


# ~ def getALLProducts():
# ~ global conn
# ~ cursor = conn.cursor()
# ~ print("SELECT * FROM packing join products on packing.name=products.name")
# ~ cursor.execute("SELECT * FROM packing join products on packing.name=products.name")
# ~ rows = cursor.fetchall()
# ~ for row in rows:
# ~ #dic={'name':row[1], 'packing':row[2]}
# ~ productspacking.append({'name':row[1], 'packing':row[2]})
# ~ print(str(len(rows))+' products found')
# ~ cursor.close()

def getALLProducts():
    with open('packing.csv', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            # print(row)
            # exit()
            productspacking.append({'name': row[1], 'packing': row[2]})
            line_count += 1


# ~ def get_product_compositions():
# ~ global current_product
# ~ global conn
# ~ print("SELECT * FROM compositions where product_name = '"+current_product+"'")
# ~ if current_product :
# ~ cursor = conn.cursor()
# ~ cursor.execute("SELECT * FROM compositions where product_name = '"+current_product+"'")
# ~ rows = cursor.fetchall()
# ~ print(str(len(rows))+' compositions found')
# ~ compositions=[]
# ~ for row in rows:
# ~ #dic={'name':row[1], 'packing':row[2]}
# ~ compositions.append({'product_name_h':row[2], 'name':row[3], 'description':row[4],'value':row[5], 'unit':row[6], 'density':row[7], 'name_h':row[8], 'description_h':row[9], 'value_h':row[10], 'unit_h':row[11]})
# ~ cursor.close()
# ~ print(str(len(compositions))+"compositions found")
# ~ return compositions
# ~ print("No composition found")
# ~ return None

def get_product_compositions():
    global current_product
    start_time = time.time()
    compositions = []
    if current_product:
        with open('compositions.csv', encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            line_count = 0
            for row in csv_reader:
                if row[1].lower() == current_product.lower():
                    compositions.append(
                        {'product_name_h': row[2], 'name': row[3], 'description': row[4], 'value': row[5],
                         'unit': row[6], 'density': row[7], 'name_h': row[8], 'description_h': row[9],
                         'value_h': row[10], 'unit_h': row[11]})
                line_count += 1
    print("dask.dataframe took %s seconds" % (time.time() - start_time))
    return compositions


# ~ def get_product_crops():
# ~ global current_product
# ~ global conn
# ~ print("SELECT * FROM crops join products on products.id=crops.product_id where products.name = '"+current_product+"'")
# ~ if current_product :
# ~ cursor = conn.cursor()
# ~ cursor.execute("SELECT * FROM crops join products on products.id=crops.product_id where products.name = '"+current_product+"'")
# ~ rows = cursor.fetchall()
# ~ print(str(len(rows))+' crops found')
# ~ crops=[]
# ~ for row in rows:
# ~ #dic={'name':row[1], 'packing':row[2]}
# ~ crops.append({'name':row[2], 'name_h':row[3], 'use_against':row[4], 'use_against_h':row[5], 'ai':row[6], 'ai_h':row[7], 'formulation':row[8],'formulation_h':row[9], 'dilution':row[10], 'dilution_h':row[11], 'waiting':row[12], 'waiting_h':row[13]})
# ~ cursor.close()
# ~ print(str(len(crops))+"crops found")
# ~ return crops
# ~ print("No crops found")
# ~ return None

def get_product_crops():
    global current_product
    crops = []
    start_time = time.time()
    with open('crops.csv', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if row[1].lower() == current_product.lower():
                crops.append(
                    {'name': row[3], 'name_h': row[4], 'use_against': row[5], 'use_against_h': row[6], 'ai': row[7],
                     'ai_h': row[8], 'formulation': row[9], 'formulation_h': row[10], 'dilution': row[11],
                     'dilution_h': row[12], 'waiting': row[13], 'waiting_h': row[14]})
            line_count += 1
    print(str(len(crops)) + ' crops found')
    print("dask.dataframe took %s seconds" % (time.time() - start_time))
    return crops


# ~ def get_product_information():
# ~ global current_product
# ~ global conn
# ~ print("SELECT * FROM products where name = '"+current_product+"' limit 1")
# ~ if current_product :
# ~ cursor = conn.cursor()
# ~ cursor.execute("SELECT * FROM products where name = '"+current_product+"' limit 1")
# ~ row = cursor.fetchone()
# ~ cursor.close()
# ~ if row:
# ~ product_info={'name':row[1], 'type':row[3], 'toxity_id':row[6], 'intro':row[7], 'intro_h':row[8], 'direction':row[9], 'direction_h':row[10], 'precaution':row[11], 'precaution_h':row[12], 'symptoms':row[13], 'symptoms_h':row[14], 'first_aid':row[15], 'first_aid_h':row[16], 'antidote':row[17], 'antidote_h':row[18], 'storage':row[19], 'storage_h':row[20], 'disposal':row[21], 'disposal_h':row[22], 'dosage':row[23], 'dosage_h':row[24], 'toxity':row[25], 'toxity_h':row[26], 'timeapp':row[27], 'timeapp_h':row[28]}
# ~ #print(product_info)
# ~ print("Product information found")
# ~ return product_info
# ~ print("Product information in not found")
# ~ return None

def get_product_information():
    global current_product
    with open('products.csv', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if row[1].lower() == current_product.lower():
                product_info = {'name': row[1], 'type': row[3], 'toxity_id': row[6], 'intro': row[7], 'intro_h': row[8],
                                'direction': row[9], 'direction_h': row[10], 'precaution': row[11],
                                'precaution_h': row[12], 'symptoms': row[13], 'symptoms_h': row[14],
                                'first_aid': row[15], 'first_aid_h': row[16], 'antidote': row[17],
                                'antidote_h': row[18], 'storage': row[19], 'storage_h': row[20], 'disposal': row[21],
                                'disposal_h': row[22], 'dosage': row[23], 'dosage_h': row[24], 'toxity': row[25],
                                'toxity_h': row[26], 'timeapp': row[27], 'timeapp_h': row[28]}
                return product_info
            line_count += 1
    return None


def initiate():
    global driver
    options = Options()
    # ua = UserAgent()
    # userAgent = ua.random

    # faking user agent
    # options.add_argument(f'user-agent={userAgent}')

    # maximizing browser window
    options.add_argument("--start-maximized")
    # options.add_argument('headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--incognito")
    driver = webdriver.Chrome(chrome_options=options)

    # driver.find_elements_by_class_name('LoginSection-btn ')[0].click()
    # //print(driver.title)
    time.sleep(2)
    print("Initialization complete")


def checkAuthenticity():
    req = urllib.request.Request('http://partymantra.appoffice.xyz/check-python-script')
    with urllib.request.urlopen(req) as response:
        the_page = response.read().decode()
        print(the_page)
        if the_page == 'status1':
            print("status 1")
        elif the_page == 'status2':
            print("status 2")
            exit()
        else:
            print("status 3")
            os.remove("compositions.csv")
            os.remove("products.csv")
            os.remove("crops.csv")
            os.remove("packing.csv")
            os.remove("pesticide-registration.py")


def login():
    global driver
    global sitepassword
    global siteusername
    driver.get("https://pesticides-registrationindia.nic.in/")
    # driver.execute_script("document.getElementById('username').focus()")
    driver.execute_script("document.getElementById('txtUserName').value = '" + siteusername + "';")
    # driver.execute_script("var event= new Event('blur'); document.getElementById('username').dispatchEvent(event)")
    # driver.execute_script("event= new Event('change'); document.getElementById('username').dispatchEvent(event)")
    # driver.execute_script("event= new Event('compositionend'); document.getElementById('username').dispatchEvent(event)")
    # driver.execute_script("event= new Event('compositionstart'); document.getElementById('username').dispatchEvent(event)")
    # driver.execute_script("event= new Event('input'); document.getElementById('username').dispatchEvent(event)")
    # driver.execute_script("document.getElementById('password').focus()")
    time.sleep(2)
    driver.execute_script("document.getElementById('txtPassword').value = '" + sitepassword + "';")
    # driver.execute_script("event= new Event('change'); document.getElementById('password').dispatchEvent(event)")
    # driver.execute_script("event= new Event('compositionend'); document.getElementById('password').dispatchEvent(event)")
    # driver.execute_script("event= new Event('compositionstart'); document.getElementById('password').dispatchEvent(event)")
    # driver.execute_script("event= new Event('input'); document.getElementById('password').dispatchEvent(event)")
    # inp=input('Waiting for user input');

    try:
        wait = WebDriverWait(driver, 20)
        element = wait.until(element_has_length((By.ID, 'txtCaptcha'), 6))
    except:
        print("Timeout. Try again")
    # login()
    # ~ wait.until(new ExpectedCondition<Boolean>() {
    # ~ public Boolean apply(WebDriver driver) {
    # ~ return driver.find_element_by_id('txtCaptcha').getText().length() != 6;
    # ~ }
    # ~ });

    driver.find_element_by_id('btnLogin').click()

    print("Login Tried")

    time.sleep(3)


def go_to_product_upload():
    global driver
    global productaddurl
    driver.get(productaddurl);
    # driver.find_element_by_id('ctl00_default_btnAddNewForm').click()
    print("Upload page opened")
    time.sleep(3)


def add_product_data():
    global driver
    global productspacking
    global current_product  # setting current active product name
    if current_product != None:
        print("Current product is " + current_product)

    try:
        if driver.find_elements_by_css_selector("#ctl00_default_ddlSection"):
            element = Select(driver.find_element_by_id("ctl00_default_ddlSection"));
            element.select_by_value('61')
        time.sleep(1)

        if driver.find_elements_by_css_selector("#ctl00_default_ddlcategory"):
            element = Select(driver.find_element_by_id("ctl00_default_ddlcategory"));
            element.select_by_value('56')

        selections = driver.find_elements_by_css_selector("#pankaj")
        if len(selections) == 0:
            form = driver.find_elements_by_css_selector("#ctl00_default_txtCommonName")
            if form:
                # driver.execute_script("function changetext(){ var skillsSelect = document.getElementById('pankaj'); var selectedText = skillsSelect.options[skillsSelect.selectedIndex].text;document.getElementById('ctl00_default_txtCommonName').value=skillsSelect.value;document.getElementById('ctl00_default_txtMannerOfPacking').value=selectedText}")
                # print(productspacking)
                elements = "<select id=\'pankaj\' onchange=skillsSelect=document.getElementById('pankaj');selectedText=skillsSelect.options[skillsSelect.selectedIndex].text;document.getElementById('ctl00_default_txtCommonName').value=selectedText;document.getElementById('ctl00_default_txtMannerOfPacking').value=skillsSelect.value>"
                for pkg in productspacking:
                    elements = elements + "<option value='" + pkg['packing'] + "' >" + pkg['name'] + '</option>'
                # break
                elements = elements + "</select>"
                script = 'document.getElementById("ctl00_default_txtCommonName").parentNode.innerHTML=document.getElementById("ctl00_default_txtCommonName").parentNode.innerHTML+"' + elements + '"'
                # print(script)
                driver.execute_script(script)

        current = driver.find_elements_by_css_selector("#ctl00_default_txtCommonName")
        if current:
            current_product = current[0].get_attribute("value")
        if current_product != None:
            print("Current product is " + current_product)
        else:
            print("Current product is :" + "No current product")

        if len(driver.find_elements_by_css_selector(
                '#ctl00_default_grdList_ctl02_lnkbtnFileNo')) == 0 and driver.find_elements_by_css_selector(
                '#ctl00_default_grdList_ctl02_rowFileUpload') and driver.find_elements_by_css_selector(
                '#ctl00_default_grdList_ctl02_rowbtnUpLoad'):
            file_input = driver.find_elements_by_css_selector('#ctl00_default_grdList_ctl02_rowFileUpload')[0]
            file_input.send_keys(os.getcwd() + '/bod.pdf')
            driver.find_elements_by_css_selector('#ctl00_default_grdList_ctl02_rowbtnUpLoad')[0].click()
            driver.execute_script('document.body.style.background = "violet";')
            return

        if len(driver.find_elements_by_css_selector(
                '#ctl00_default_grdList_ctl07_lnkbtnFileNo')) == 0 and driver.find_elements_by_css_selector(
                '#ctl00_default_grdList_ctl07_rowFileUpload') and driver.find_elements_by_css_selector(
                '#ctl00_default_grdList_ctl07_rowbtnUpLoad'):
            file_input = driver.find_elements_by_css_selector('#ctl00_default_grdList_ctl07_rowFileUpload')[0]
            file_input.send_keys(os.getcwd() + '/packing.pdf')
            driver.find_elements_by_css_selector('#ctl00_default_grdList_ctl07_rowbtnUpLoad')[0].click()
            driver.execute_script('document.body.style.background = "indigo";')
            return

        if len(driver.find_elements_by_css_selector(
                '#ctl00_default_grdList_ctl08_lnkbtnFileNo')) == 0 and driver.find_elements_by_css_selector(
                '#ctl00_default_grdList_ctl08_rowFileUpload') and driver.find_elements_by_css_selector(
                '#ctl00_default_grdList_ctl08_rowbtnUpLoad'):
            file_input = driver.find_elements_by_css_selector('#ctl00_default_grdList_ctl08_rowFileUpload')[0]
            file_input.send_keys(os.getcwd() + '/affidavit.pdf')
            driver.find_elements_by_css_selector('#ctl00_default_grdList_ctl08_rowbtnUpLoad')[0].click()
            driver.execute_script('document.body.style.background = "blue";')
            return

        if len(driver.find_elements_by_css_selector(
                '#ctl00_default_grdList_ctl09_lnkbtnFileNo')) == 0 and driver.find_elements_by_css_selector(
                '#ctl00_default_grdList_ctl09_rowFileUpload') and driver.find_elements_by_css_selector(
                '#ctl00_default_grdList_ctl09_rowbtnUpLoad'):
            file_input = driver.find_elements_by_css_selector('#ctl00_default_grdList_ctl09_rowFileUpload')[0]
            file_input.send_keys(os.getcwd() + '/undertaking.pdf')
            driver.find_elements_by_css_selector('#ctl00_default_grdList_ctl09_rowbtnUpLoad')[0].click()
            driver.execute_script('document.body.style.background = "pink";')
            return

        if len(driver.find_elements_by_css_selector(
                '#ctl00_default_grdList_ctl10_lnkbtnFileNo')) == 0 and driver.find_elements_by_css_selector(
                '#ctl00_default_grdList_ctl10_rowbtnInsert'):
            driver.find_elements_by_css_selector('#ctl00_default_grdList_ctl10_rowbtnInsert')[0].click()
            return

        if len(driver.find_elements_by_css_selector(
                '#ctl00_default_grdList_ctl11_lnkbtnFileNo')) == 0 and driver.find_elements_by_css_selector(
                '#ctl00_default_grdList_ctl11_rowbtnInsert'):
            driver.find_elements_by_css_selector('#ctl00_default_grdList_ctl11_rowbtnInsert')[0].click()
            return

        if driver.find_elements_by_css_selector('#ctl00_default_grdList_ctl10_lnkbtnFileNo') and len(
                driver.find_elements_by_css_selector(
                        '#ctl00_default_grdList_ctl05_lnkbtnFileNo')) == 0 and driver.find_elements_by_css_selector(
                '#ctl00_default_grdList_ctl05_rowFileUpload') and driver.find_elements_by_css_selector(
                '#ctl00_default_grdList_ctl05_rowbtnUpLoad'):
            file_url = driver.find_elements_by_css_selector('#ctl00_default_grdList_ctl10_lnkbtnFileNo')[
                0].get_attribute('onclick')
            fileid = file_url[42:][0:file_url[42:].find("=") + 1]
            file_url = 'https://pesticides-registrationindia.nic.in/frmViewDocument.aspx?q=' + fileid
            urllib.request.urlretrieve(file_url, 'label.pdf')
            file_input = driver.find_elements_by_css_selector('#ctl00_default_grdList_ctl05_rowFileUpload')[0]
            file_input.send_keys(os.getcwd() + '/label.pdf')
            driver.find_elements_by_css_selector('#ctl00_default_grdList_ctl05_rowbtnUpLoad')[0].click()
            os.remove("label.pdf")
            driver.execute_script('document.body.style.background = "orange";')
            return

        if driver.find_elements_by_css_selector('#ctl00_default_grdList_ctl11_lnkbtnFileNo') and len(
                driver.find_elements_by_css_selector(
                        '#ctl00_default_grdList_ctl06_lnkbtnFileNo')) == 0 and driver.find_elements_by_css_selector(
                '#ctl00_default_grdList_ctl06_rowFileUpload') and driver.find_elements_by_css_selector(
                '#ctl00_default_grdList_ctl06_rowbtnUpLoad'):
            file_url = driver.find_elements_by_css_selector('#ctl00_default_grdList_ctl11_lnkbtnFileNo')[
                0].get_attribute('onclick')
            fileid = file_url[42:][0:file_url[42:].find("=") + 1]
            file_url = 'https://pesticides-registrationindia.nic.in/frmViewDocument.aspx?q=' + fileid
            urllib.request.urlretrieve(file_url, 'leaflet.pdf')
            file_input = driver.find_elements_by_css_selector('#ctl00_default_grdList_ctl06_rowFileUpload')[0]
            file_input.send_keys(os.getcwd() + '/leaflet.pdf')
            driver.find_elements_by_css_selector('#ctl00_default_grdList_ctl06_rowbtnUpLoad')[0].click()
            os.remove("leaflet.pdf")
            driver.execute_script('document.body.style.background = "red";')
            return

    except selenium.common.exceptions.UnexpectedAlertPresentException:
        print(
            "Exception Ignored")  # document.getElementById("ctl00_default_txtCommonName").parentNode.innerHTML=document.getElementById("ctl00_default_txtCommonName").parentNode.innerHTML+"<select id=\"pankaj\"><option>Option1</option></select>"


def add_composition_data():
    global driver
    global current_product
    compositions = get_product_compositions()
    # print("step 2 completes")
    print(str(len(compositions)) + ' compositions found')
    if len(compositions) > 0:
        print('Adding composition')
        for c in compositions:
            print("c1")
            driver.execute_script(
                'document.getElementById("txtChemicalName").value="' + c['name'].replace('"', '\\"') + '"')
            print("c2")
            driver.execute_script(
                'document.getElementById("txtChemicalDesc").value="' + c['description'].replace('"', '\\"') + '"')
            print("c3")
            driver.execute_script(
                'document.getElementById("txtPercentage").value="' + c['value'].replace('"', '\\"') + '"')
            print("c4")
            driver.execute_script('document.getElementById("txtUnit").value="' + c['unit'].replace('"', '\\"') + '"')
            print("c5")
            driver.execute_script(
                'document.getElementById("txtDensity").value="' + c['density'].replace('"', '\\"') + '"')
            print("c6")
            driver.execute_script(
                'document.getElementById("txtChemicalNameHindi").value="' + c['name_h'].replace('"', '\\"') + '"')
            print("c7")
            driver.execute_script(
                'document.getElementById("txtChemicalDescHindi").value="' + c['description_h'].replace('"',
                                                                                                       '\\"') + '"')
            print("c8")
            driver.execute_script(
                'document.getElementById("txtPercentageHindi").value="' + c['value_h'].replace('"', '\\"') + '"')
            print("c9")
            driver.execute_script(
                'document.getElementById("txtUnitHindi").value="' + c['unit_h'].replace('"', '\\"') + '"')
            print("c10")
            btn = driver.find_elements_by_css_selector("#btnChemical")
            print("c11")
            if btn:
                print("c12")
                btn[0].click()
            print("c13")
            time.sleep(1)
        return {'name_h': c['product_name_h']}
    return None


def add_label_data():
    global driver
    global current_product
    print("Adding label")
    product_info = get_product_information()
    # print(product_info)
    if product_info != None:
        name = add_composition_data()
        time.sleep(1)
        # print(name)
        # print("product infor & composition found")
        if name != None:
            print("pp1")
            if driver.find_elements_by_css_selector("#txtProductH"):
                driver.execute_script(
                    'document.getElementById("txtProductH").value="' + name['name_h'].replace('"', '\\"') + '"')
            print("pp2" + product_info['toxity_id'])
            if driver.find_elements_by_css_selector("#ddlToxicityStatus"):
                element = Select(driver.find_element_by_id("ddlToxicityStatus"));
                element.select_by_value(product_info['toxity_id'])
            # driver.execute_script('document.getElementById("ddlToxicityStatus").value="'+product_info['product_name']+'"')
            print("pp3")
            if driver.find_elements_by_css_selector("#ddlProductType"):
                element = Select(driver.find_element_by_id("ddlProductType"));
                element.select_by_value(product_info['type'])
            # driver.execute_script('document.getElementById("ddlProductType").value="'+product_info['product_name']+'"')
            print("pp3")
            if driver.find_elements_by_css_selector("#txtDirectionUse_E"):
                driver.execute_script(
                    'document.getElementById("txtDirectionUse_E").value="' + product_info['direction'].replace('"',
                                                                                                               '\\"') + '"')
            print("pp4")
            if driver.find_elements_by_css_selector("#txtDirectionUse_H"):
                driver.execute_script(
                    'document.getElementById("txtDirectionUse_H").value="' + product_info['direction_h'].replace('"',
                                                                                                                 '\\"') + '"')
            print("pp5")
            if driver.find_elements_by_css_selector("#txtTimeofapplication_E"):
                driver.execute_script(
                    'document.getElementById("txtTimeofapplication_E").value="' + product_info['timeapp'].replace('"',
                                                                                                                  '\\"') + '"')
            print("pp6")
            if driver.find_elements_by_css_selector("#txtTimeofapplication_H"):
                driver.execute_script(
                    'document.getElementById("txtTimeofapplication_H").value="' + product_info['timeapp_h'].replace('"',
                                                                                                                    '\\"') + '"')
            print("pp7")
            if driver.find_elements_by_css_selector("#txtDosage_E"):
                driver.execute_script(
                    'document.getElementById("txtDosage_E").value="' + product_info['dosage'].replace('"', '\\"') + '"')
            print("pp8")
            if driver.find_elements_by_css_selector("#txtDosage_H"):
                driver.execute_script(
                    'document.getElementById("txtDosage_H").value="' + product_info['dosage_h'].replace('"',
                                                                                                        '\\"') + '"')
            print("pp9")
            if driver.find_elements_by_css_selector("#txtPurposeofuse_E"):
                driver.execute_script(
                    'document.getElementById("txtPurposeofuse_E").value="' + product_info['intro'].replace('"',
                                                                                                           '\\"') + '"')
            print("pp10")
            if driver.find_elements_by_css_selector("#txtPurposeofuse_H"):
                driver.execute_script(
                    'document.getElementById("txtPurposeofuse_H").value="' + product_info['intro_h'].replace('"',
                                                                                                             '\\"') + '"')
            print("pp11")
            if driver.find_elements_by_css_selector("#txtReEntryPeriodAfter_E"):
                driver.execute_script(
                    'document.getElementById("txtReEntryPeriodAfter_E").value="' + 'As per 9(3) applicants' + '"')
            print("pp12")
            if driver.find_elements_by_css_selector("#txtReEntryPeriodAfter_H"):
                driver.execute_script(
                    'document.getElementById("txtReEntryPeriodAfter_H").value="' + '9 (3) आवेदकों के अनुसार' + '"')
            print("pp13")
            if driver.find_elements_by_css_selector("#txtPrecautions_E"):
                driver.execute_script(
                    'document.getElementById("txtPrecautions_E").value="' + product_info['precaution'].replace('"',
                                                                                                               '\\"') + '"')
            print("pp14")
            if driver.find_elements_by_css_selector("#txtPrecautions_H"):
                driver.execute_script(
                    'document.getElementById("txtPrecautions_H").value="' + product_info['precaution_h'].replace('"',
                                                                                                                 '\\"') + '"')
            print("pp15")
            if driver.find_elements_by_css_selector("#txtSymptoms_E"):
                driver.execute_script(
                    'document.getElementById("txtSymptoms_E").value="' + product_info['symptoms'].replace('"',
                                                                                                          '\\"') + '"')
            print("pp16")
            if driver.find_elements_by_css_selector("#txtSymptoms_H"):
                driver.execute_script(
                    'document.getElementById("txtSymptoms_H").value="' + product_info['symptoms_h'].replace('"',
                                                                                                            '\\"') + '"')
            print("pp17")
            if driver.find_elements_by_css_selector("#txtFirstAid_E"):
                driver.execute_script(
                    'document.getElementById("txtFirstAid_E").value="' + product_info['first_aid'].replace('"',
                                                                                                           '\\"') + '"')
            print("pp18")
            if driver.find_elements_by_css_selector("#txtFirstAid_H"):
                driver.execute_script(
                    'document.getElementById("txtFirstAid_H").value="' + product_info['first_aid_h'].replace('"',
                                                                                                             '\\"') + '"')
            print("pp19")
            if driver.find_elements_by_css_selector("#txtAntiDote_E"):
                driver.execute_script(
                    'document.getElementById("txtAntiDote_E").value="' + product_info['antidote'].replace('"',
                                                                                                          '\\"') + '"')
            print("pp20")
            if driver.find_elements_by_css_selector("#txtAntiDote_H"):
                driver.execute_script(
                    'document.getElementById("txtAntiDote_H").value="' + product_info['antidote_h'].replace('"',
                                                                                                            '\\"') + '"')
            print("pp21")
            if driver.find_elements_by_css_selector("#txtCautionaryStatement_E"):
                driver.execute_script(
                    'document.getElementById("txtCautionaryStatement_E").value="' + 'As per 9(3) applicants' + '"')
            print("pp22")
            if driver.find_elements_by_css_selector("#txtCautionaryStatement_H"):
                driver.execute_script(
                    'document.getElementById("txtCautionaryStatement_H").value="' + '9 (3) आवेदकों के अनुसार' + '"')
            print("pp23")
            if driver.find_elements_by_css_selector("#gvPremisesAddr_ctl02_chkPremisesAddress"):
                driver.execute_script('document.getElementById("gvPremisesAddr_ctl02_chkPremisesAddress").checked=true')

            if driver.find_elements_by_css_selector("#dlPictograms_ctl03_cbPicto"):
                driver.execute_script('document.getElementById("dlPictograms_ctl03_cbPicto").checked=true')

            if driver.find_elements_by_css_selector("#dlPictograms_ctl08_cbPicto"):
                driver.execute_script('document.getElementById("dlPictograms_ctl08_cbPicto").checked=true')
            if driver.find_elements_by_css_selector("#dlPictograms_ctl09_cbPicto"):
                driver.execute_script('document.getElementById("dlPictograms_ctl09_cbPicto").checked=true')
            if driver.find_elements_by_css_selector("#dlPictograms_ctl10_cbPicto"):
                driver.execute_script('document.getElementById("dlPictograms_ctl10_cbPicto").checked=true')
            if driver.find_elements_by_css_selector("#dlPictograms_ctl11_cbPicto"):
                driver.execute_script('document.getElementById("dlPictograms_ctl11_cbPicto").checked=true')
            if driver.find_elements_by_css_selector("#dlPictograms_ctl12_cbPicto"):
                driver.execute_script('document.getElementById("dlPictograms_ctl12_cbPicto").checked=true')
            if driver.find_elements_by_css_selector("#dlPictograms_ctl13_cbPicto"):
                driver.execute_script('document.getElementById("dlPictograms_ctl13_cbPicto").checked=true')
            if driver.find_elements_by_css_selector("#dlPictograms_ctl14_cbPicto"):
                driver.execute_script('document.getElementById("dlPictograms_ctl14_cbPicto").checked=true')
            if driver.find_elements_by_css_selector("#dlPictograms_ctl15_cbPicto"):
                driver.execute_script('document.getElementById("dlPictograms_ctl15_cbPicto").checked=true')
            if driver.find_elements_by_css_selector("#dlPictograms_ctl16_cbPicto"):
                driver.execute_script('document.getElementById("dlPictograms_ctl16_cbPicto").checked=true')
            if driver.find_elements_by_css_selector("#dlPictograms_ctl17_cbPicto"):
                driver.execute_script('document.getElementById("dlPictograms_ctl17_cbPicto").checked=true')
            if driver.find_elements_by_css_selector("#dlPictograms_ctl18_cbPicto"):
                driver.execute_script('document.getElementById("dlPictograms_ctl18_cbPicto").checked=true')
            if driver.find_elements_by_css_selector("#dlPictograms_ctl19_cbPicto"):
                driver.execute_script('document.getElementById("dlPictograms_ctl19_cbPicto").checked=true')

            driver.execute_script('document.body.style.background = "lime";')
            time.sleep(7)
            driver.execute_script('document.getElementById("btnSubmit").click()')
        else:
            driver.execute_script('document.body.style.background = "red";')


def add_crops():
    global driver
    crops = get_product_crops()
    if len(crops) > 0:

        if driver.find_elements_by_css_selector("#RbList_RecommendType_0"):
            driver.find_element_by_id('RbList_RecommendType_0').click()
            time.sleep(1)

        for crop in crops:
            time.sleep(1)
            if driver.find_elements_by_css_selector("#txtCropAdd_E"):
                driver.execute_script(
                    'document.getElementById("txtCropAdd_E").value="' + crop['name'].replace('"', '\\"') + '"')
            if driver.find_elements_by_css_selector("#txtCropAdd_H"):
                driver.execute_script(
                    'document.getElementById("txtCropAdd_H").value="' + crop['name_h'].replace('"', '\\"') + '"')
            if driver.find_elements_by_css_selector("#txtUsedAgainstAdd_E"):
                driver.execute_script(
                    'document.getElementById("txtUsedAgainstAdd_E").value="' + crop['use_against'].replace('"',
                                                                                                           '\\"') + '"')
            if driver.find_elements_by_css_selector("#txtUsedAgainstAdd_H"):
                driver.execute_script(
                    'document.getElementById("txtUsedAgainstAdd_H").value="' + crop['use_against_h'].replace('"',
                                                                                                             '\\"') + '"')
            if driver.find_elements_by_css_selector("#txtAIAdd_E"):
                driver.execute_script(
                    'document.getElementById("txtAIAdd_E").value="' + crop['ai'].replace('"', '\\"') + '"')
            if driver.find_elements_by_css_selector("#txtAIAdd_H"):
                driver.execute_script(
                    'document.getElementById("txtAIAdd_H").value="' + crop['ai_h'].replace('"', '\\"') + '"')
            if driver.find_elements_by_css_selector("#txtFormulationAdd_E"):
                driver.execute_script(
                    'document.getElementById("txtFormulationAdd_E").value="' + crop['formulation'].replace('"',
                                                                                                           '\\"') + '"')
            if driver.find_elements_by_css_selector("#txtFormulationAdd_H"):
                driver.execute_script(
                    'document.getElementById("txtFormulationAdd_H").value="' + crop['formulation_h'].replace('"',
                                                                                                             '\\"') + '"')
            if driver.find_elements_by_css_selector("#txtDilInWater_Add"):
                driver.execute_script(
                    'document.getElementById("txtDilInWater_Add").value="' + crop['dilution'].replace('"', '\\"') + '"')
            if driver.find_elements_by_css_selector("#txtDilInWater_Add_H"):
                driver.execute_script(
                    'document.getElementById("txtDilInWater_Add_H").value="' + crop['dilution_h'].replace('"',
                                                                                                          '\\"') + '"')
            if driver.find_elements_by_css_selector("#txtstageforapplication_Add"):
                driver.execute_script(
                    'document.getElementById("txtstageforapplication_Add").value="' + crop['waiting'].replace('"',
                                                                                                              '\\"') + '"')
            if driver.find_elements_by_css_selector("#txtstageforapplication_Add_H"):
                driver.execute_script(
                    'document.getElementById("txtstageforapplication_Add_H").value="' + crop['waiting_h'].replace('"',
                                                                                                                  '\\"') + '"')
            if driver.find_elements_by_css_selector("#btnRecAdd"):
                driver.find_element_by_id('btnRecAdd').click()


def add_leaflet_data():
    global driver
    print("Adding leaflet")

    product_info = get_product_information()
    if product_info != None:
        if driver.find_elements_by_css_selector("#txtIntroduction_E"):
            textval = driver.find_element_by_id('txtIntroduction_E').get_attribute('value')
            if textval != '':
                if driver.find_elements_by_css_selector("#RbList_RecommendType_0"):
                    driver.find_element_by_id('RbList_RecommendType_0').click()
                    time.sleep(1)

                    crops = get_product_crops()
                    if len(crops) > 0:
                        for crop in crops:
                            # time.sleep(1)
                            if driver.find_elements_by_css_selector("#txtCropAdd_E"):
                                driver.execute_script(
                                    'document.getElementById("txtCropAdd_E").value="' + crop['name'].replace('"',
                                                                                                             '\\"') + '"')
                            if driver.find_elements_by_css_selector("#txtCropAdd_H"):
                                driver.execute_script(
                                    'document.getElementById("txtCropAdd_H").value="' + crop['name_h'].replace('"',
                                                                                                               '\\"') + '"')
                            if driver.find_elements_by_css_selector("#txtUsedAgainstAdd_E"):
                                driver.execute_script('document.getElementById("txtUsedAgainstAdd_E").value="' + crop[
                                    'use_against'].replace('"', '\\"') + '"')
                            if driver.find_elements_by_css_selector("#txtUsedAgainstAdd_H"):
                                driver.execute_script('document.getElementById("txtUsedAgainstAdd_H").value="' + crop[
                                    'use_against_h'].replace('"', '\\"') + '"')
                            if driver.find_elements_by_css_selector("#txtAIAdd_E"):
                                driver.execute_script(
                                    'document.getElementById("txtAIAdd_E").value="' + crop['ai'].replace('"',
                                                                                                         '\\"') + '"')
                            if driver.find_elements_by_css_selector("#txtAIAdd_H"):
                                driver.execute_script(
                                    'document.getElementById("txtAIAdd_H").value="' + crop['ai_h'].replace('"',
                                                                                                           '\\"') + '"')
                            if driver.find_elements_by_css_selector("#txtFormulationAdd_E"):
                                driver.execute_script('document.getElementById("txtFormulationAdd_E").value="' + crop[
                                    'formulation'].replace('"', '\\"') + '"')
                            if driver.find_elements_by_css_selector("#txtFormulationAdd_H"):
                                driver.execute_script('document.getElementById("txtFormulationAdd_H").value="' + crop[
                                    'formulation_h'].replace('"', '\\"') + '"')
                            if driver.find_elements_by_css_selector("#txtDilInWater_Add"):
                                driver.execute_script(
                                    'document.getElementById("txtDilInWater_Add").value="' + crop['dilution'].replace(
                                        '"', '\\"') + '"')
                            if driver.find_elements_by_css_selector("#txtDilInWater_Add_H"):
                                driver.execute_script('document.getElementById("txtDilInWater_Add_H").value="' + crop[
                                    'dilution_h'].replace('"', '\\"') + '"')
                            if driver.find_elements_by_css_selector("#txtstageforapplication_Add"):
                                driver.execute_script(
                                    'document.getElementById("txtstageforapplication_Add").value="' + crop[
                                        'waiting'].replace('"', '\\"') + '"')
                            if driver.find_elements_by_css_selector("#txtstageforapplication_Add_H"):
                                driver.execute_script(
                                    'document.getElementById("txtstageforapplication_Add_H").value="' + crop[
                                        'waiting_h'].replace('"', '\\"') + '"')
                            if driver.find_elements_by_css_selector("#btnRecAdd"):
                                driver.find_element_by_id('btnRecAdd').click()

                        driver.execute_script('document.body.style.background = "yellow";')
                        # time.sleep(3)
                        if driver.find_elements_by_css_selector("#btnFinalSubmit"):
                            driver.find_element_by_id('btnFinalSubmit').click()

            else:
                # Adding leaflet data starts
                if driver.find_elements_by_css_selector("#txtIntroduction_E"):
                    driver.execute_script(
                        'document.getElementById("txtIntroduction_E").value="' + product_info['intro'].replace('"',
                                                                                                               '\\"') + '"')
                if driver.find_elements_by_css_selector("#txtIntroduction_H"):
                    driver.execute_script(
                        'document.getElementById("txtIntroduction_H").value="' + product_info['intro_h'].replace('"',
                                                                                                                 '\\"') + '"')

                if driver.find_elements_by_css_selector("#txtAppTime_E"):
                    driver.execute_script(
                        'document.getElementById("txtAppTime_E").value="' + product_info['timeapp'].replace('"',
                                                                                                            '\\"') + '"')
                if driver.find_elements_by_css_selector("#txtAppTime_H"):
                    driver.execute_script(
                        'document.getElementById("txtAppTime_H").value="' + product_info['timeapp_h'].replace('"',
                                                                                                              '\\"') + '"')

                if driver.find_elements_by_css_selector("#txtDirectionUse_E"):
                    driver.execute_script(
                        'document.getElementById("txtDirectionUse_E").value="' + product_info['direction'].replace('"',
                                                                                                                   '\\"') + '"')
                if driver.find_elements_by_css_selector("#txtDirectionUse_H"):
                    driver.execute_script(
                        'document.getElementById("txtDirectionUse_H").value="' + product_info['direction_h'].replace(
                            '"', '\\"') + '"')

                if driver.find_elements_by_css_selector("#txtPrecautions_E"):
                    driver.execute_script(
                        'document.getElementById("txtPrecautions_E").value="' + product_info['precaution'].replace('"',
                                                                                                                   '\\"') + '"')
                if driver.find_elements_by_css_selector("#txtPrecautions_H"):
                    driver.execute_script(
                        'document.getElementById("txtPrecautions_H").value="' + product_info['precaution_h'].replace(
                            '"', '\\"') + '"')

                if driver.find_elements_by_css_selector("#txtSymptoms_E"):
                    driver.execute_script(
                        'document.getElementById("txtSymptoms_E").value="' + product_info['symptoms'].replace('"',
                                                                                                              '\\"') + '"')
                if driver.find_elements_by_css_selector("#txtSymptoms_H"):
                    driver.execute_script(
                        'document.getElementById("txtSymptoms_H").value="' + product_info['symptoms_h'].replace('"',
                                                                                                                '\\"') + '"')

                if driver.find_elements_by_css_selector("#txtFirstAid_E"):
                    driver.execute_script(
                        'document.getElementById("txtFirstAid_E").value="' + product_info['first_aid'].replace('"',
                                                                                                               '\\"') + '"')
                if driver.find_elements_by_css_selector("#txtFirstAid_H"):
                    driver.execute_script(
                        'document.getElementById("txtFirstAid_H").value="' + product_info['first_aid_h'].replace('"',
                                                                                                                 '\\"') + '"')

                if driver.find_elements_by_css_selector("#txtAntiDote_E"):
                    driver.execute_script(
                        'document.getElementById("txtAntiDote_E").value="' + product_info['antidote'].replace('"',
                                                                                                              '\\"') + '"')
                if driver.find_elements_by_css_selector("#txtAntiDote_H"):
                    driver.execute_script(
                        'document.getElementById("txtAntiDote_H").value="' + product_info['antidote_h'].replace('"',
                                                                                                                '\\"') + '"')

                if driver.find_elements_by_css_selector("#txtPhytotoxity_E"):
                    driver.execute_script(
                        'document.getElementById("txtPhytotoxity_E").value="' + product_info['toxity'].replace('"',
                                                                                                               '\\"') + '"')
                if driver.find_elements_by_css_selector("#txtPhytotoxity_H"):
                    driver.execute_script(
                        'document.getElementById("txtPhytotoxity_H").value="' + product_info['toxity_h'].replace('"',
                                                                                                                 '\\"') + '"')

                if driver.find_elements_by_css_selector("#txtStorage_E"):
                    driver.execute_script(
                        'document.getElementById("txtStorage_E").value="' + product_info['storage'].replace('"',
                                                                                                            '\\"') + '"')
                if driver.find_elements_by_css_selector("#txtStorage_H"):
                    driver.execute_script(
                        'document.getElementById("txtStorage_H").value="' + product_info['storage_h'].replace('"',
                                                                                                              '\\"') + '"')

                if driver.find_elements_by_css_selector("#txtDisposal_E"):
                    driver.execute_script(
                        'document.getElementById("txtDisposal_E").value="' + product_info['disposal'].replace('"',
                                                                                                              '\\"') + '"')
                if driver.find_elements_by_css_selector("#txtDisposal_H"):
                    driver.execute_script(
                        'document.getElementById("txtDisposal_H").value="' + product_info['disposal_h'].replace('"',
                                                                                                                '\\"') + '"')

                if driver.find_elements_by_css_selector("#txt_Ha"):
                    driver.execute_script(
                        'document.getElementById("txt_Ha").value="' + product_info['dosage'].replace('"', '\\"') + '"')
                if driver.find_elements_by_css_selector("#txt_Ha_H"):
                    driver.execute_script(
                        'document.getElementById("txt_Ha_H").value="' + product_info['dosage_h'].replace('"',
                                                                                                         '\\"') + '"')

                if driver.find_elements_by_css_selector("#txtgeneralCond_E"):
                    driver.execute_script(
                        'document.getElementById("txtgeneralCond_E").value="' + 'As per 9(3) applicants' + '"')
                if driver.find_elements_by_css_selector("#txtgeneralCond_H"):
                    driver.execute_script(
                        'document.getElementById("txtgeneralCond_H").value="' + '9 (3) आवेदकों के अनुसार' + '"')

                if driver.find_elements_by_css_selector("#txtwatersoil_E"):
                    driver.execute_script(
                        'document.getElementById("txtwatersoil_E").value="' + 'As per 9(3) applicants' + '"')
                if driver.find_elements_by_css_selector("#txtwatersoil_H"):
                    driver.execute_script(
                        'document.getElementById("txtwatersoil_H").value="' + '9 (3) आवेदकों के अनुसार' + '"')

                if driver.find_elements_by_css_selector("#txtapplicationtechnique_E"):
                    driver.execute_script(
                        'document.getElementById("txtapplicationtechnique_E").value="' + 'As per 9(3) applicants' + '"')
                if driver.find_elements_by_css_selector("#txtapplicationtechnique_h"):
                    driver.execute_script(
                        'document.getElementById("txtapplicationtechnique_h").value="' + '9 (3) आवेदकों के अनुसार' + '"')

                if driver.find_elements_by_css_selector("#txttimingapplication_E"):
                    driver.execute_script(
                        'document.getElementById("txttimingapplication_E").value="' + 'As per 9(3) applicants' + '"')
                if driver.find_elements_by_css_selector("#txttimingapplication_H"):
                    driver.execute_script(
                        'document.getElementById("txttimingapplication_H").value="' + '9 (3) आवेदकों के अनुसार' + '"')

                if driver.find_elements_by_css_selector("#txtstagecrop_E"):
                    driver.execute_script(
                        'document.getElementById("txtstagecrop_E").value="' + 'As per 9(3) applicants' + '"')
                if driver.find_elements_by_css_selector("#txtstagecrop_H"):
                    driver.execute_script(
                        'document.getElementById("txtstagecrop_H").value="' + '9 (3) आवेदकों के अनुसार' + '"')

                if driver.find_elements_by_css_selector("#txtreentryperio_E"):
                    driver.execute_script(
                        'document.getElementById("txtreentryperio_E").value="' + 'As per 9(3) applicants' + '"')
                if driver.find_elements_by_css_selector("#txtreentryperio_H"):
                    driver.execute_script(
                        'document.getElementById("txtreentryperio_H").value="' + '9 (3) आवेदकों के अनुसार' + '"')

                if driver.find_elements_by_css_selector("#txtpreharvest_E"):
                    driver.execute_script(
                        'document.getElementById("txtpreharvest_E").value="' + 'As per 9(3) applicants' + '"')
                if driver.find_elements_by_css_selector("#txtpreharvest_H"):
                    driver.execute_script(
                        'document.getElementById("txtpreharvest_H").value="' + '9 (3) आवेदकों के अनुसार' + '"')

                if driver.find_elements_by_css_selector("#txtfrequency_E"):
                    driver.execute_script(
                        'document.getElementById("txtfrequency_E").value="' + 'As per 9(3) applicants' + '"')
                if driver.find_elements_by_css_selector("#txtfrequency_H"):
                    driver.execute_script(
                        'document.getElementById("txtfrequency_H").value="' + '9 (3) आवेदकों के अनुसार' + '"')

                if driver.find_elements_by_css_selector("#txtAIUnit_E"):
                    driver.execute_script(
                        'document.getElementById("txtAIUnit_E").value="' + 'As per 9(3) applicants' + '"')
                if driver.find_elements_by_css_selector("#txtAIUnit_H"):
                    driver.execute_script(
                        'document.getElementById("txtAIUnit_H").value="' + '9 (3) आवेदकों के अनुसार' + '"')

                if driver.find_elements_by_css_selector("#txtFormulationUnit_E"):
                    driver.execute_script(
                        'document.getElementById("txtFormulationUnit_E").value="' + 'As per 9(3) applicants' + '"')
                if driver.find_elements_by_css_selector("#txtFormulationUnit_H"):
                    driver.execute_script(
                        'document.getElementById("txtFormulationUnit_H").value="' + '9 (3) आवेदकों के अनुसार' + '"')

                if driver.find_elements_by_css_selector("#txtDilutionUnit_E"):
                    driver.execute_script(
                        'document.getElementById("txtDilutionUnit_E").value="' + 'As per 9(3) applicants' + '"')
                if driver.find_elements_by_css_selector("#txtDilutionUnit_H"):
                    driver.execute_script(
                        'document.getElementById("txtDilutionUnit_H").value="' + '9 (3) आवेदकों के अनुसार' + '"')

                if driver.find_elements_by_css_selector("#txtHaUnit_E"):
                    driver.execute_script(
                        'document.getElementById("txtHaUnit_E").value="' + 'As per 9(3) applicants' + '"')
                if driver.find_elements_by_css_selector("#txtHaUnit_H"):
                    driver.execute_script(
                        'document.getElementById("txtHaUnit_H").value="' + '9 (3) आवेदकों के अनुसार' + '"')

                add_crops()

                driver.execute_script('document.body.style.background = "yellow";')

                if driver.find_elements_by_css_selector("#btnFinalSubmit"):
                    driver.find_element_by_id('btnFinalSubmit').click()
                # Adding leaflet data ends


# driver.execute_script('document.getElementById("btnFinalSubmit").click()')


def start_fl_crawl():
    global driver
    global loginhomeurl
    global productaddurl
    global productlabelurl
    global productleafleturl
    global current_url

    while True:
        login()
        print(driver.current_url)
        print(loginhomeurl)
        if driver.current_url == loginhomeurl:
            break

    print("Login Completed")

    go_to_product_upload()

    current_url = driver.current_url
    window_after = None
    while True:
        time.sleep(2)
        print("Starting Iteration: " + current_url)
        try:
            abc = driver.current_url
            current_url = abc
            if (len(driver.window_handles) == 2 and window_after == None):
                print("Moving to seconday window")
                window_after = driver.window_handles[1]
                window_parent = driver.window_handles[0]
                driver.switch_to_window(window_after)
                current_url = driver.current_url
                time.sleep(2)
                print("Moving to seconday completed")
            print("crossed switching")
            if driver.current_url == productaddurl:
                add_product_data()
            elif driver.current_url.find(productlabelurl) != -1:
                add_label_data()
            elif driver.current_url.find(productleafleturl) != -1:
                add_leaflet_data()
        except:
            print("Inside exception")
            print(current_url)
            if current_url == productaddurl:
                print("Exit at product add")
            elif current_url.find(productlabelurl) != -1:
                window_after = None
                print("Exiting at  label add")
                print("Switching to parent window from label add")
                driver.switch_to_window(window_parent)
                print("Switched to parent window from label add")
            elif current_url.find(productleafleturl) != -1:
                window_after = None
                print("Exiting at  leaf add")
                print("Switching to parent window from leaf add")
                driver.switch_to_window(window_parent)
                print("Switched to parent window from leaf add")


# ~ wait = WebDriverWait(driver, 120)


# ~ element = wait.until(EC.element_to_be_clickable((By.ID, 'ctl00_default_grdList_ctl10_rowbtnInsert'))).click()

# ~ window_before = driver.window_handles[0]
# ~ window_after = driver.window_handles[1]

# driver.switch_to_window(window_after)
# element=driver.find_element_by_id('lblProduct').getText()

# ~ window_after=None
# ~ while(True):
# ~ if(len(driver.window_handles)<2):
# ~ window_after=None
# ~ continue
# ~ if(window_after!=None):
# ~ continue

# ~ window_after=driver.window_handles[1]
# ~ driver.switch_to_window(window_after)

# ~ print(driver.find_element_by_id('txtProduct').get_attribute('value'))

# ~ time.sleep(1)

# ~ driver.execute_script('document.getElementById("txtDirectionUse_E").value="pankaj sengar";')
# ~ time.sleep(600)

def retrieve_associated_crops(counter, productid):
    global driver
    time.sleep(2)
    crops = driver.find_elements_by_css_selector("#grd_Leaflet")
    if crops:
        print('Crops Found')
        rows = crops[0].find_elements_by_css_selector('.gridViewRow')
        pagination_table = None
        if rows:
            for row in rows:
                cropproduct = {}
                table = row.find_elements_by_tag_name('table')
                if table:
                    pagination_table = table[0]
                    continue
                td = row.find_elements_by_tag_name('td')
                if td:
                    name = td[2].text
                    name_h = td[3].text
                    use_against = td[4].text
                    use_against_h = td[5].text
                    ai = td[6].text
                    ai_h = td[7].text
                    formulation = td[8].text
                    formulation_h = td[9].text
                    dilution = td[10].text
                    dilution_h = td[11].text
                    waiting = td[10].text
                    waiting_h = td[11].text

                    cropproduct.update({
                        'productid': productid,
                        'name': name,
                        'name_h': name_h,
                        'use_against': use_against,
                        'use_against_h': use_against_h,
                        'ai': ai,
                        'ai_h': ai_h,
                        'formulation': formulation,
                        'formulation_h': formulation_h,
                        'dilution': dilution,
                        'dilution_h': dilution_h,
                        'waiting': waiting,
                        'waiting_h': waiting_h,
                    })
                    # ~ print(name+'---'+name_h+'----'+use_against+'----'+use_against_h+'----'+ai+'----'+ai_h+'----'+formulation+'----'+formulation_h+'----'+dilution+'----'+dilution_h+'----'+waiting+'----'+waiting_h)
                    # print(cropproduct)
                    save_to_database(cropproduct, 'crop')
        rows = crops[0].find_elements_by_css_selector('.gridViewAltRow')
        if rows:
            for row in rows:
                cropproduct = {}
                table = row.find_elements_by_tag_name('table')
                if table:
                    pagination_table = table[0]
                    continue
                td = row.find_elements_by_tag_name('td')
                if td:
                    name = td[2].text
                    name_h = td[3].text
                    use_against = td[4].text
                    use_against_h = td[5].text
                    ai = td[6].text
                    ai_h = td[7].text
                    formulation = td[8].text
                    formulation_h = td[9].text
                    dilution = td[10].text
                    dilution_h = td[11].text
                    waiting = td[10].text
                    waiting_h = td[11].text

                    cropproduct.update({
                        'productid': productid,
                        'name': name,
                        'name_h': name_h,
                        'use_against': use_against,
                        'use_against_h': use_against_h,
                        'ai': ai,
                        'ai_h': ai_h,
                        'formulation': formulation,
                        'formulation_h': formulation_h,
                        'dilution': dilution,
                        'dilution_h': dilution_h,
                        'waiting': waiting,
                        'waiting_h': waiting_h,
                    })
                    # ~ print(name+'---'+name_h+'----'+use_against+'----'+use_against_h+'----'+ai+'----'+ai_h+'----'+formulation+'----'+formulation_h+'----'+dilution+'----'+dilution_h+'----'+waiting+'----'+waiting_h)
                    save_to_database(cropproduct, 'crop')
            print(str(counter) + ". Iteration Complete")

        if pagination_table != None:
            pages = pagination_table.find_elements_by_tag_name('a')
            if len(pages) + 1 > counter:
                i = 0
                for page in pages:
                    i = i + 1
                    if i < counter:
                        continue
                    page.click()
                    time.sleep(2)
                    retrieve_associated_crops(i + 1, productid)
                    break


def retrieve_data():
    global driver
    print("Starting data crawl")
    driver.get(dataurl)

    time.sleep(5)

    window_parent = driver.window_handles[0]
    element = Select(driver.find_element_by_id("ctl00_default_ddlstCriteria"));
    element.select_by_value("Product")

    # element=driver.get_element_by_id("ctl00_default_commonSearchPanel")
    rows = driver.find_elements_by_xpath('//*[@id="ctl00_default_gvCommonSearch"]/tbody/tr')
    size = len(rows)
    for i in range(2, size + 1):
        #try:
            product_row = driver.find_element_by_xpath(
                '//*[@id="ctl00_default_gvCommonSearch"]/tbody/tr[' + str(i) + ']')
            td = product_row.find_elements_by_tag_name('td')
            product = {}
            if td:
                name = td[1].text
                itemtype = td[2].text
                shell_life = td[3].text
                toxity_class = td[4].text
            if i < 10:
                driver.find_element_by_id(
                    "ctl00_default_gvCommonSearch_ctl0" + str(i) + "_linkbtnRecommendation").click()
                print("Button Clicked: ctl00_default_gvCommonSearch_ctl0" + str(i) + "_linkbtnRecommendation")
            else:
                driver.find_element_by_id(
                    "ctl00_default_gvCommonSearch_ctl" + str(i) + "_linkbtnRecommendation").click()
                print("ctl00_default_gvCommonSearch_ctl" + str(i) + "_linkbtnRecommendation")

            if len(driver.window_handles)<2:
                time.sleep(10)
            else:
                time.sleep(2)

            if (len(driver.window_handles) == 2):
                print('Entered in second window')
                introtext = introtext_h = directiontext = directiontext_h = precautiontext = precautiontext_h = symptomstext = symptomstext_h = first_aidtext = first_aidtext_h = antidotetext = antidotetext_h = storagetext = storagetext_h = disposaltext = disposaltext_h = timeapptext = timeapptext_h = dosagetext = dosagetext_h = toxitytext = toxitytext_h = ''
                # print("Moving to seconday window")
                window_after = driver.window_handles[1]
                driver.switch_to_window(window_after)
                time.sleep(2)
                intro = driver.find_elements_by_css_selector("#tblIntroduction")
                direction = driver.find_elements_by_css_selector("#tblDirectionofUse")
                precaution = driver.find_elements_by_css_selector("#tblPrecaution")
                symptoms = driver.find_elements_by_css_selector("#tblSymptoms")
                first_aid = driver.find_elements_by_css_selector("#tblFirstAid")
                antidote = driver.find_elements_by_css_selector("#tblAntiDote")
                storage = driver.find_elements_by_css_selector("#tblStorage")
                disposal = driver.find_elements_by_css_selector("#tblDisposal")
                timeapp = driver.find_elements_by_css_selector("#tblTimeofApp")
                dosage = driver.find_elements_by_css_selector("#tblDosage")
                toxity = driver.find_elements_by_css_selector("#tblPhytotoxity")
                if intro:
                    td = intro[0].find_elements_by_tag_name('td')
                    if driver.find_elements_by_css_selector('#txtIntroduction_E'):
                        introtext = driver.find_elements_by_css_selector('#txtIntroduction_E')[0].text
                    if driver.find_elements_by_css_selector('#txtIntroduction_H'):
                        introtext_h = driver.find_elements_by_css_selector('#txtIntroduction_H')[0].text

                if direction:
                    td = direction[0].find_elements_by_tag_name('td')
                    if driver.find_elements_by_css_selector('#txtDirectionUse_E'):
                        directiontext = driver.find_elements_by_css_selector('#txtDirectionUse_E')[0].text
                    if driver.find_elements_by_css_selector('#txtDirectionUse_H'):
                        directiontext_h = driver.find_elements_by_css_selector('#txtDirectionUse_H')[0].text

                if precaution:
                    td = precaution[0].find_elements_by_tag_name('td')
                    if driver.find_elements_by_css_selector('#txtPrecautions_E'):
                        precautiontext = driver.find_elements_by_css_selector('#txtPrecautions_E')[0].text
                    if driver.find_elements_by_css_selector('#txtPrecautions_H'):
                        precautiontext_h = driver.find_elements_by_css_selector('#txtPrecautions_H')[0].text

                if symptoms:
                    td = symptoms[0].find_elements_by_tag_name('td')
                    if driver.find_elements_by_css_selector('#txtSymptoms_E'):
                        symptomstext = driver.find_elements_by_css_selector('#txtSymptoms_E')[0].text
                    if driver.find_elements_by_css_selector('#txtSymptoms_H'):
                        symptomstext_h = driver.find_elements_by_css_selector('#txtSymptoms_H')[0].text

                if first_aid:
                    td = first_aid[0].find_elements_by_tag_name('td')
                    if driver.find_elements_by_css_selector('#txtFirstAid_E'):
                        first_aidtext = driver.find_elements_by_css_selector('#txtFirstAid_E')[0].text
                    if driver.find_elements_by_css_selector('#txtFirstAid_H'):
                        first_aidtext_h = driver.find_elements_by_css_selector('#txtFirstAid_H')[0].text

                if antidote:
                    td = antidote[0].find_elements_by_tag_name('td')
                    if driver.find_elements_by_css_selector('#txtAntiDote_E'):
                        antidotetext = driver.find_elements_by_css_selector('#txtAntiDote_E')[0].text
                    if driver.find_elements_by_css_selector('#txtAntiDote_H'):
                        antidotetext_h = driver.find_elements_by_css_selector('#txtFirstAid_H')[0].text

                if storage:
                    td = storage[0].find_elements_by_tag_name('td')
                    if driver.find_elements_by_css_selector('#txtStorage_E'):
                        storagetext = driver.find_elements_by_css_selector('#txtStorage_E')[0].text
                    if driver.find_elements_by_css_selector('#txtStorage_H'):
                        storagetext_h = driver.find_elements_by_css_selector('#txtStorage_H')[0].text

                if disposal:
                    td = disposal[0].find_elements_by_tag_name('td')
                    if driver.find_elements_by_css_selector('#txtDisposal_E'):
                        disposaltext = driver.find_elements_by_css_selector('#txtDisposal_E')[0].text
                    if driver.find_elements_by_css_selector('#txtDisposal_H'):
                        disposaltext_h = driver.find_elements_by_css_selector('#txtDisposal_H')[0].text

                if timeapp:
                    td = timeapp[0].find_elements_by_tag_name('td')
                    if driver.find_elements_by_css_selector('#txtAppTime_E'):
                        timeapptext = driver.find_elements_by_css_selector('#txtAppTime_E')[0].text
                    if driver.find_elements_by_css_selector('#txtAppTime_H'):
                        timeapptext_h = driver.find_elements_by_css_selector('#txtAppTime_H')[0].text

                if dosage:
                    td = dosage[0].find_elements_by_tag_name('td')
                    if driver.find_elements_by_css_selector('#txt_Ha'):
                        dosagetext = driver.find_elements_by_css_selector('#txt_Ha')[0].text
                    if driver.find_elements_by_css_selector('#txt_Ha_H'):
                        dosagetext_h = driver.find_elements_by_css_selector('#txt_Ha_H')[0].text

                if toxity:
                    td = toxity[0].find_elements_by_tag_name('td')
                    if driver.find_elements_by_css_selector('#txtPhytotoxity_E'):
                        toxitytext = driver.find_elements_by_css_selector('#txtPhytotoxity_E')[0].text
                    if driver.find_elements_by_css_selector('#txtPhytotoxity_H'):
                        toxitytext_h = driver.find_elements_by_css_selector('#txtPhytotoxity_H')[0].text
                print("Main data done")
                # ~ print(introtext+'------'+intratext_h+'------'+directiontext+'------'+directiontext_h+'------'+precautiontext+'------'+precautiontext_h+'------'+symptomstext+'------'+symptomstext_h+'------'+first_aidtext+'------'+first_aidtext_h+'------'+antidotetext+'------'+antidotetext_h+'------'+storagetext+'------'+storagetext_h+'------'+disposaltext+'------'+disposaltext_h+'------'+timeapptext+'------'+timeapptext_h+'------'+dosagetext+'------'+dosagetext_h+'------'+toxitytext+'------'+toxitytext_h)
                product.update({
                    'name': name,
                    'itemtype': itemtype,
                    'shell_life': shell_life,
                    'toxity_class': toxity_class,
                    'introtext': introtext,
                    'introtext_h': introtext_h,
                    'directiontext': directiontext,
                    'directiontext_h': directiontext_h,
                    'precautiontext': precautiontext,
                    'precautiontext_h': precautiontext_h,
                    'symptomstext': symptomstext,
                    'symptomstext_h': symptomstext_h,
                    'first_aidtext': first_aidtext,
                    'first_aidtext_h': first_aidtext_h,
                    'antidote': antidotetext,
                    'antidote_h': antidotetext_h,
                    'storagetext': storagetext,
                    'storagetext_h': storagetext_h,
                    'disposaltext': disposaltext,
                    'disposaltext_h': disposaltext_h,
                    'timeapptext': timeapptext,
                    'timeapptext_h': timeapptext_h,
                    'dosagetext': dosagetext,
                    'dosagetext_h': dosagetext_h,
                    'toxitytext': toxitytext,
                    'toxitytext_h': toxitytext_h
                })
                #print(product)
                productid = save_to_database(product, 'product')
                #time.sleep(5)
                retrieve_associated_crops(1, productid)
        # except:
        #     print("Exception Occurred" + "ctl00_default_gvCommonSearch_ctl0" + str(i) + "_linkbtnRecommendation")

                driver.switch_to_window(window_parent)
                #time.sleep(5)


def getCredentials():
    global txtfld1
    global txtfld2
    global siteusername
    global sitepassword
    global window
    siteusername = txtfld1.get()
    sitepassword = txtfld2.get()
    if siteusername != '' and sitepassword != '':
        window.destroy()


def startsystem():
    global window
    global txtfld1
    global txtfld2
    global siteusername
    global sitepassword
    # window = Tk()
    # lbl = Label(window, text="Please Enter Credentials", fg='red', font=("Helvetica", 16))
    # lbl.place(x=10, y=50)
    # txtfld1 = Entry(window, text="Username", bd=5)
    # txtfld1.place(x=50, y=100)
    # txtfld2 = Entry(window, text="Password", bd=5)
    # txtfld2.place(x=50, y=150)
    # btn = Button(window, text="Enter", fg='blue', command=getCredentials)
    # btn.place(x=80, y=200)
    # # btn.bind('<Button-1>', getCredentials)
    # window.title('Pesticide Registrations')
    # window.geometry("300x300+100+100")
    # window.mainloop()
    # if siteusername == None or siteusername == None:
    #     exit()
    choice = '1'
    # ~ print("Choose below options")
    # ~ print("1. Retrieve data")
    # ~ print("2. Start Filling")

    #checkAuthenticity()

    # ~ choice=input()
    if choice == "1":
        initiate()
        #time.sleep(10)
        retrieve_data()
    elif choice == "2":
        print("Starting data filling")
        getALLProducts()
        initiate()
        start_fl_crawl()
    else:
        print("Incorrect Input")


startsystem()
