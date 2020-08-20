from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer
from io import BytesIO
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import re
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import csv
import urllib.request
import os
import math
from selenium.webdriver.common.action_chains import ActionChains
# Python 3.x code
# Imports
import tkinter
from tkinter import messagebox

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


class ProductRegistration:

    def initiate(self):
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
        self.driver = webdriver.Chrome(chrome_options=options)

        # driver.find_elements_by_class_name('LoginSection-btn ')[0].click()
        # //print(driver.title)
        time.sleep(2)
        print("Initialization complete")

    def login(self):
        self.driver.get("https://pesticides-registrationindia.nic.in/")
        self.driver.execute_script("document.getElementById('txtUserName').value = '" + self.siteusername + "';")
        time.sleep(2)
        self.driver.execute_script("document.getElementById('txtPassword').value = '" + self.sitepassword + "';")
        try:
            wait = WebDriverWait(self.driver, 20)
            element = wait.until(element_has_length((By.ID, 'txtCaptcha'), 6))
        except:
            print("Timeout. Try again")

        self.driver.find_element_by_id('btnLogin').click()
        print("Login Tried")
        time.sleep(3)

    def getCompanyInfo(self):
        with open('address.csv', encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count > 0:
                    self.siteusername = row[0]
                    self.sitepassword = row[1]
                    self.is_private_ltd = row[2]
                    self.district = row[3]
                    self.address_info = row[4]
                    self.authorization = os.getcwd()+'/Documents/auth.pdf'
                    self.manufacturing = os.getcwd()+'/Documents/mfg.pdf'
                    self.production = os.getcwd()+'/Documents/production.pdf'
                    self.pancard = os.getcwd()+'/Documents/pancard.pdf'
                    self.ssi = os.getcwd()+'/Documents/ssi.pdf'
                    self.self_affidavit_path = os.getcwd()+'/Documents'
                    self.consent_path = os.getcwd()+'/Documents'
                    self.final_doc_path = os.getcwd()+'/final-docs'
                    self.signature_path = os.getcwd()+'/Documents/digitalsign.jpg'
                    self.incorporation_certificate = os.getcwd()+'/Documents/cin.pdf'
                    return
                line_count += 1

    def open_registration_form(self,data):
        elements = self.driver.find_elements_by_id('ctl00_IMISMenun0')
        if elements:
            action = ActionChains(self.driver);
            action.move_to_element(elements[0]).perform()
            menus = self.driver.find_elements_by_id('ctl00_IMISMenun6')
            if menus:
                menus[0].click()
                time.sleep(2)
                newform = self.driver.find_elements_by_id('ctl00_default_hypSubmit')
                if newform:
                    newform[0].click()
                    time.sleep(2)

                    if data[3]!='':
                        option=self.driver.find_elements_by_id('ctl00_default_rbProductType_1')
                        if option:
                            option[0].click()
                    next = self.driver.find_elements_by_id('ctl00_default_btnNext')
                    if next:
                        next[0].click()
                        time.sleep(2)

    def get_product_other_details(self):
        self.product_details = []
        with open('products-data.csv', encoding="utf8", errors='ignore') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count > 0:
                    self.product_details.append({
                        'name': row[0],
                        'toxicity': row[1],
                        'packing': row[2]
                    })
                line_count = line_count + 1

    def search_product_details(self, name):
        for product in self.product_details:
            if product['name'] == name:
                return product

    def start_filling_data(self):
        self.downloded_file="C:\\Users\dev\Downloads\ReportForm1.pdf"
        with open('products-sheet.csv', encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count > 0:
                    self.delete_temporary_files()
                    self.test_file=None
                    self.fp_downloaded = None
                    self.open_registration_form(row)
                    self.fill_product_data(row)
                line_count = line_count + 1

    def fill_product_data(self, data):
        self.fill_product_data_form_1(data)
        self.fill_product_data_form_2(data)
        self.fill_product_data_form_3()
        self.processing_step_3()
        self.modifying_main_document(data)

    def fill_product_data_form_1(self, data):
        elements = self.driver.find_elements_by_id('ctl00_default_ddlProductGroup')
        if elements:
            select = Select(elements[0])
            select.select_by_value(data[2])
        time.sleep(1)

        if data[3]!='':
            elements = self.driver.find_elements_by_id('ctl00_default_ddlProductGroup2')
            if elements:
                select = Select(elements[0])
                select.select_by_value(data[3])
            time.sleep(1)

        elements = self.driver.find_elements_by_id('ctl00_default_ddlInsecticideAct')
        if elements:
            select = Select(elements[0])
            select.select_by_value('61')
        time.sleep(1)

        elements = self.driver.find_elements_by_id('ctl00_default_ddlCategory')
        if elements:
            select = Select(elements[0])
            select.select_by_value('56')
        time.sleep(1)


        elements = self.driver.find_elements_by_id('ctl00_default_ddlCommonName')
        if elements:
            select = Select(elements[0])
            select.select_by_visible_text(data[0])
        time.sleep(1)

        elements = self.driver.find_elements_by_id('ctl00_default_gvPremisesAddr_ctl02_chkPremisesAddress')
        if elements:
            elements[0].click()
        time.sleep(1)
        if self.address_info == '1' or self.address_info == '1,2' or self.address_info == '1,3':
            elements = self.driver.find_elements_by_id('ctl00_default_gvPremisesAddr_ctl02_chkPremisesAddress')
            if elements:
                elements[0].click()
            time.sleep(1)
        if self.address_info == '2' or self.address_info == '1,2' or self.address_info == '2,3':
            elements = self.driver.find_elements_by_id('ctl00_default_gvPremisesAddr_ctl03_chkPremisesAddress')
            if elements:
                elements[0].click()
            time.sleep(1)
        if self.address_info == '3' or self.address_info == '1,3' or self.address_info == '2,3':
            elements = self.driver.find_elements_by_id('ctl00_default_gvPremisesAddr_ctl04_chkPremisesAddress')
            if elements:
                elements[0].click()
            time.sleep(1)


        elements = self.driver.find_elements_by_id('ctl00_default_ddl_repacked')
        if elements:
            select = Select(elements[0])
            select.select_by_value('Manuf_01')
        time.sleep(1)

        elements = self.driver.find_elements_by_id('ctl00_default_ddlConsumption')
        if elements:
            select = Select(elements[0])
            select.select_by_value('51')
        time.sleep(1)

        elements = self.driver.find_elements_by_id('ctl00_default_txtFormulationSource')
        if elements:
            elements[0].send_keys(data[1])
        time.sleep(1)

        elements = self.driver.find_elements_by_id('ctl00_default_ddlFormulationStatus')
        if elements:
            select = Select(elements[0])
            select.select_by_value('65')
        time.sleep(1)

        button = self.driver.find_elements_by_id('ctl00_default_btnSave')
        if button:
            button[0].click()

    def fill_product_data_form_2(self, data):
        file = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl02_rowFileUpload')
        if file:
            if not os.path.exists(self.authorization):
                messagebox.showinfo("Error", "Authorization Document Not Found")
                return False
            file[0].send_keys(self.authorization)
            btn = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl02_rowbtnUpLoad')
            btn[0].click()
            time.sleep(2)

        file = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl03_rowFileUpload')
        if file:
            if not os.path.exists(self.authorization):
                messagebox.showinfo("Error", "Authorization Document Not Found")
                return False
            file[0].send_keys(self.authorization)
            btn = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl03_rowbtnUpLoad')
            btn[0].click()
            time.sleep(2)

        if self.is_private_ltd=='yes':
            file = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl04_rowFileUpload')
            if file:
                if not os.path.exists(self.incorporation_certificate):
                    messagebox.showinfo("Error", "Incorporation Certificate Document Not Found")
                file[0].send_keys(self.incorporation_certificate)
                btn = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl04_rowbtnUpLoad')
                btn[0].click()
                time.sleep(2)

        seq='04'
        if self.is_private_ltd=='yes':
            seq='05'
        file = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl'+seq+'_rowFileUpload')
        if file:
            if not os.path.exists(self.pancard):
                messagebox.showinfo("Error", "Pancard Document Not Found")
            file[0].send_keys(self.pancard)
            btn = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl'+seq+'_rowbtnUpLoad')
            btn[0].click()
            time.sleep(2)

        seq = '05'
        if self.is_private_ltd == 'yes':
            seq = '06'
        file = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl'+seq+'_rowFileUpload')
        if file:
            if not os.path.exists(self.ssi):
                messagebox.showinfo("Error", "SSI Document Not Found")
            file[0].send_keys(self.ssi)
            btn = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl'+seq+'_rowbtnUpLoad')
            btn[0].click()
            time.sleep(2)

        seq = '06'
        if self.is_private_ltd == 'yes':
            seq = '07'
        file = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl'+seq+'_rowFileUpload')
        if file:
            if not os.path.exists(self.manufacturing):
                messagebox.showinfo("Error", "Manufacturing Document Not Found")
            file[0].send_keys(self.manufacturing)
            btn = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl'+seq+'_rowbtnUpLoad')
            btn[0].click()
            time.sleep(2)

        seq = '07'
        if self.is_private_ltd == 'yes':
            seq = '08'
        file = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl'+seq+'_rowFileUpload')
        if file:
            if not os.path.exists(self.production):
                messagebox.showinfo("Error", "Production Document Not Found")
            file[0].send_keys(self.production)
            btn = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl'+seq+'_rowbtnUpLoad')
            btn[0].click()
            time.sleep(2)

        seq = '08'
        if self.is_private_ltd == 'yes':
            seq = '09'
        file = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl'+seq+'_rowFileUpload')
        if file:
            if not os.path.exists(self.production):
                messagebox.showinfo("Error", "Production Document Not Found")
            file[0].send_keys(self.production)
            btn = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl'+seq+'_rowbtnUpLoad')
            btn[0].click()
            time.sleep(2)

        seq = '09'
        if self.is_private_ltd == 'yes':
            seq = '10'
        file = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl'+seq+'_rowFileUpload')
        if file:
            file_name = data[0]
            file_name = file_name.replace('.', '-').replace('/', '-') + '.pdf'
            if not os.path.exists(self.self_affidavit_path + '/' +file_name):
                print('Self Affidavit IS not Found')
                messagebox.showinfo("Error", "Self Affidavit Document Not Found: "+self.self_affidavit_path + '/' +file_name)
                
            file[0].send_keys(self.self_affidavit_path + '/' + file_name)
            btn = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl'+seq+'_rowbtnUpLoad')
            btn[0].click()
            time.sleep(2)

        seq = '10'
        if self.is_private_ltd == 'yes':
            seq = '11'
        file = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl'+seq+'_rowFileUpload')
        if file:
            file_name = data[2]
            file_name = file_name.replace('.', '-').replace('/', '-') + '.pdf'
            if not os.path.exists(self.consent_path + '/' +file_name):
                print('Consent IS not Found')
                messagebox.showinfo("Error", "Consent Document Not Found: "+self.consent_path + '/' +file_name)
            file[0].send_keys(self.consent_path + '/' + file_name)
            btn = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl'+seq+'_rowbtnUpLoad')
            btn[0].click()
            time.sleep(2)

        seq = '11'
        if self.is_private_ltd == 'yes':
            seq = '12'
        if data[3]!='':
            print('second schedule found')
            docoptions=self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl'+seq+'_ddlDocName')
            if docoptions:
                print('options found')
                file_name=data[3].replace('.', '-').replace('/','-') + '.pdf'
                if not os.path.exists(self.consent_path + '/' +file_name):
                    print('Consent IS not Found')
                    messagebox.showinfo("Error", "Consent Document Not Found: "+self.consent_path + '/' +file_name)
                print(file_name)
                docoptions=Select(docoptions[0])
                docoptions.select_by_value('36')
                fileupload=self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl'+seq+'_footerFileUpload')
                if fileupload:
                    fileupload[0].send_keys(self.consent_path+'/'+file_name)
                    extrabtn=self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl'+seq+'_footerbtnUpload')
                    if extrabtn:
                        extrabtn[0].click()


        product = self.search_product_details(data[0])
        if product == None:
            messagebox.showinfo("Error", "Product Toxity, Packing Details Not Found: "+data[0])

        toxity = self.driver.find_elements_by_id('ctl00_default_txtToxicity')
        if toxity:
            toxity[0].send_keys(product['toxicity'])

        bioefficacy = self.driver.find_elements_by_id('ctl00_default_txtBioefficacy')
        if bioefficacy:
            bioefficacy[0].send_keys('N.A.')

        firstaid = self.driver.find_elements_by_id('ctl00_default_txtFirstAid')
        if firstaid:
            firstaid[0].send_keys('N.A.')

        quality = self.driver.find_elements_by_id('ctl00_default_txtProdQlty')
        if quality:
            quality[0].send_keys('Not Required')

        analisis = self.driver.find_elements_by_id('ctl00_default_txtAnalysis')
        if analisis:
            analisis[0].send_keys('Not Required As Per The Discussion Of The RC')

        newanalysis = self.driver.find_elements_by_id('ctl00_default_txtAnalysis1New')
        if newanalysis:
            newanalysis[0].send_keys('N.A.')

        leaflet = self.driver.find_elements_by_id('ctl00_default_txtLeaflet')
        if leaflet:
            leaflet[0].send_keys('N.A.')

        packing = self.driver.find_elements_by_id('ctl00_default_txtPacking')
        if packing:
            packing[0].send_keys(product['packing'])

        btn = self.driver.find_elements_by_id('ctl00_default_btn_FinalSave')
        if btn:
            btn[0].click()
            time.sleep(1)

    def fill_product_data_form_3(self):
        district = self.driver.find_elements_by_id('ctl00_default_txtPlace')
        if district:
            district[0].send_keys(self.district)
        btn = self.driver.find_elements_by_id('ctl00_default_btnSave')
        if btn:
            btn[0].click()

    def processing_step_3(self):
        link = self.driver.find_elements_by_id('ctl00_default_hypPreview')
        if link:
            link[0].click()

        time.sleep(1)

        window_after = self.driver.window_handles[1]
        self.window_parent = self.driver.window_handles[0]
        self.driver.switch_to.window(window_after)

        pdf = self.driver.find_elements_by_id('rvRpt_ctl01_ctl05_ctl00')
        if pdf:
            selector = Select(pdf[0])
            selector.select_by_value('PDF')
            time.sleep(1)
            export = self.driver.find_elements_by_id('rvRpt_ctl01_ctl05_ctl01')
            export[0].click()
            time.sleep(3)

        self.driver.close()
        self.driver.switch_to.window(self.window_parent)

        page2 = self.driver.find_elements_by_id('ctl00_default_hypBacktoPage2')
        if page2:
            page2[0].click()

    def modifying_main_document(self, data):
        final_path = self.startPDFProcessing(self.downloded_file,
                                             data[0].replace('.', '-').replace('/', '-'))

        delbtn = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl02_rowbtnDelete')
        if delbtn:
            delbtn[0].click()
        time.sleep(5)

        ale = self.driver.switch_to.alert
        ale.accept()
        time.sleep(1)

        self.driver.switch_to.window(self.window_parent)

        file = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl02_rowFileUpload')
        if file:
            file[0].send_keys(final_path)
            btn = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl02_rowbtnUpLoad')
            btn[0].click()
            # os.remove('/home/pankaj/Downloads/ReportForm1.pdf')
            time.sleep(1)

        btn = self.driver.find_elements_by_id('ctl00_default_btn_FinalSave')
        if btn:
            btn[0].click()

    def startPDFProcessing(self, file, product_name):
        fp=open(file, 'rb')
        self.pdf_pages_list = []
        pdf = PdfFileReader(fp)
        pages = pdf.getNumPages()
        fp.close()
        self.parsepdf(file, 0, pages - 1)
        print(self.pdf_pages_list)
        return self.add_signature_image(file, product_name)

    def parsepdf(self, filename, startpage, endpage):

        # Open a PDF file.
        self.fp_downloaded = open(filename, 'rb')

        # Create a PDF parser object associated with the file object.
        parser = PDFParser(self.fp_downloaded)

        # Create a PDF document object that stores the document structure.
        # Password for initialization as 2nd parameter
        document = PDFDocument(parser)

        # Check if the document allows text extraction. If not, abort.
        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed

        # Create a PDF resource manager object that stores shared resources.
        rsrcmgr = PDFResourceManager()

        # Create a PDF device object.
        device = PDFDevice(rsrcmgr)

        # BEGIN LAYOUT ANALYSIS
        # Set parameters for analysis.
        laparams = LAParams()

        # Create a PDF page aggregator object.
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)

        # Create a PDF interpreter object.
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        i = 0
        # loop over all pages in the document
        for page in PDFPage.create_pages(document):
            if i >= startpage and i <= endpage:
                # read the page into a layout object
                interpreter.process_page(page)
                layout = device.get_result()

                # extract text from this object
                self.parse_obj(layout._objs, i)
            i += 1

        self.fp_downloaded.close()

    def parse_obj(self, lt_objs, page):
        # loop over the object list
        for obj in lt_objs:

            if isinstance(obj, pdfminer.layout.LTTextLine):
                # Signature of applicant with Seal
                if obj.get_text().find('Signature of applicant with Seal') != -1:
                    print("%6d, %6d, %s" % (obj.bbox[0], obj.bbox[1], obj.get_text().replace('\n', '_')))
                    self.pdf_pages_list.append({
                        'page': page,
                        'x': math.floor(obj.bbox[0]),
                        'y': math.floor(obj.bbox[1])
                    })

            # if it's a textbox, also recurse
            if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
                self.parse_obj(obj._objs, page)

            # if it's a container, recurse
            elif isinstance(obj, pdfminer.layout.LTFigure):
                self.parse_obj(obj._objs, page)

    def create_watermark(self, x, y):
        c = canvas.Canvas('test.pdf')
        # move the origin up and to the left
        c.translate(inch, inch)
        c.setFillColorRGB(1, 0, 1)
        # c.drawImage("/home/omsairam6/sample.png", 2, 2, 50, 50)
        # x = 422
        # y = 58
        # c.drawImage("sign.png", x - 60, y - 60, 100, 40)
        # x = 422
        # y = 211
        c.drawImage(self.signature_path, x - 65, y - 60, 120, 50)
        c.showPage()
        c.save()
        # Get the watermark file you just created
        if self.test_file==None:
            self.test_file=open("test.pdf", "rb")
        watermark = PdfFileReader(self.test_file)

        return watermark

    # def is_signature_required(self, page):
    #     for page1 in self.pdf_pages_list:
    #         if page1['page'] == page:
    #             return page1
    #     return False

    def add_signature_image(self, file, product_name):

        # # there are 66 slides (1.jpg, 2.jpg, 3.jpg...)
        # path = '/home/omsairam6/sign.png'
        # pdf = PdfFileWriter()
        #
        # #for num in range(1, 67):  # for each slide
        #     # Using ReportLab Canvas to insert image into PDF
        # imgTemp = BytesIO()
        # imgDoc = canvas.Canvas(imgTemp, pagesize=A4)
        # # Draw image on Canvas and save PDF in buffer
        # imgDoc.drawImage(path, x, y)
        # # x, y - start position
        # # in my case -25, -45 needed
        # imgDoc.save()
        # # Use PyPDF to merge the image-PDF into the template
        # pdf.addPage(PdfFileReader(BytesIO(imgTemp.getvalue())).getPage(0))
        #
        # pdf.write(open("", "wb"))
        # Get our files ready
        output_file = PdfFileWriter()
        self.fp_downloaded=open(file, "rb")
        input_file = PdfFileReader(self.fp_downloaded)

        # Number of pages in input document
        page_count = input_file.getNumPages()

        # Go through all the input file pages to add a watermark to them
        for page_number in range(page_count):

            input_page = input_file.getPage(page_number)
            #details = self.is_signature_required(page_number)
            for details in self.pdf_pages_list:
                if details['page']==page_number:
                    print("Watermarking page {} of {}".format(page_number, page_count))
                    # merge the watermark with the page
                    watermark = self.create_watermark(details['x'], details['y'])
                    input_page.mergePage(watermark.getPage(0))
                    #self.delete_temporary_files()
                    # add page from input file to output document
            output_file.addPage(input_page)

        # finally, write "output" to document-output.pdf
        print(self.final_doc_path + '/' + product_name + '.pdf');
        if not os.path.exists(self.final_doc_path):
            messagebox.showinfo("Error",
                                "Path Doesnt Exists: "+self.final_doc_path)

        with open(self.final_doc_path + '/' + product_name + '.pdf', "wb") as outputStream:
            output_file.write(outputStream)
        outputStream.close()    

        self.fp_downloaded.close()
        self.test_file.close()
        #self.test_file=None
        return self.final_doc_path + '/' + product_name + '.pdf'

    def delete_temporary_files(self):
            #self.test_file.close()
            if os.path.exists('test.pdf'):
                os.remove('test.pdf')
            #clear last downloaded file
            if os.path.exists(self.downloded_file):
                os.remove(self.downloded_file)


    def start(self):
        self.root = tkinter.Tk()
        self.root.withdraw()
        self.initiate();
        self.getCompanyInfo()
        self.get_product_other_details()
        while True:
            self.login()
            #print(driver.current_url)
            #print(loginhomeurl)
            if self.driver.current_url == 'https://pesticides-registrationindia.nic.in/UserProfile/HomePage.aspx':
                break
        self.start_filling_data()

        #final_path = self.startPDFProcessing('/home/pankaj/Downloads/ReportForm1.pdf')


pdf_parser = ProductRegistration()
# pdf_parser.start1('sample.pdf')
pdf_parser.start()
# pdf_parser.add_image('/home/omsairam6/sample.pdf', 0, 0)
