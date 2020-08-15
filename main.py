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
                    self.authorization = row[4]
                    self.manufacturing = row[5]
                    self.production = row[6]
                    self.pancard = row[7]
                    self.ssi = row[8]
                    self.self_affidavit_path = row[9]
                    self.consent_path = row[10]
                    self.final_doc_path = row[11]
                    self.signature_path = row[12]
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
        with open('products-data.csv', encoding="utf8") as csv_file:
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
        with open('products-sheet.csv', encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count > 0:
                    self.open_registration_form(row)
                    self.fill_product_data(row)
                line_count = line_count + 1

    def fill_product_data(self, data):
        if os.path.exists('/home/pankaj/Downloads/ReportForm1.pdf'):
            os.remove('/home/pankaj/Downloads/ReportForm1.pdf')
        self.fill_product_data_form_1(data)
        self.fill_product_data_form_2(data)
        self.fill_product_data_form_3()
        self.processing_step_3()
        self.modifying_main_document(data)

    def fill_product_data_form_1(self, data):
        elements = self.driver.find_elements_by_id('ctl00_default_ddlProductGroup')
        if elements:
            select = Select(elements[0])
            select.select_by_visible_text(data[2])
        time.sleep(1)

        if data[3]!='':
            elements = self.driver.find_elements_by_id('ctl00_default_ddlProductGroup2')
            if elements:
                select = Select(elements[0])
                select.select_by_visible_text(data[3])
            time.sleep(1)

        elements = self.driver.find_elements_by_id('ctl00_default_ddlInsecticideAct')
        if elements:
            select = Select(elements[0])
            select.select_by_value('59')
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
            select.select_by_value('216')
        time.sleep(1)

        button = self.driver.find_elements_by_id('ctl00_default_btnSave')
        if button:
            button[0].click()

    def fill_product_data_form_2(self, data):
        file = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl02_rowFileUpload')
        if file:
            file[0].send_keys(self.authorization)
            btn = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl02_rowbtnUpLoad')
            btn[0].click()
            time.sleep(2)

        file = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl03_rowFileUpload')
        if file:
            file[0].send_keys(self.authorization)
            btn = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl03_rowbtnUpLoad')
            btn[0].click()
            time.sleep(2)

        file = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl04_rowFileUpload')
        if file:
            file[0].send_keys(self.pancard)
            btn = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl04_rowbtnUpLoad')
            btn[0].click()
            time.sleep(2)

        file = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl05_rowFileUpload')
        if file:
            file[0].send_keys(self.ssi)
            btn = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl05_rowbtnUpLoad')
            btn[0].click()
            time.sleep(2)

        file = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl06_rowFileUpload')
        if file:
            file[0].send_keys(self.manufacturing)
            btn = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl06_rowbtnUpLoad')
            btn[0].click()
            time.sleep(2)

        file = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl07_rowFileUpload')
        if file:
            file[0].send_keys(self.production)
            btn = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl07_rowbtnUpLoad')
            btn[0].click()
            time.sleep(2)

        file = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl08_rowFileUpload')
        if file:
            file[0].send_keys(self.production)
            btn = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl08_rowbtnUpLoad')
            btn[0].click()
            time.sleep(2)

        file = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl09_rowFileUpload')
        if file:
            file_name = data[0]
            file_name = file_name.replace('.', '-').replace('/', '-') + '.pdf'
            file[0].send_keys(self.self_affidavit_path + '/' + file_name)
            btn = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl09_rowbtnUpLoad')
            btn[0].click()
            time.sleep(2)

        file = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl10_rowFileUpload')
        if file:
            file_name = data[2]
            file_name = file_name.replace('.', '-').replace('/', '-') + '.pdf'
            file[0].send_keys(self.consent_path + '/' + file_name)
            btn = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl10_rowbtnUpLoad')
            btn[0].click()
            time.sleep(2)

        product = self.search_product_details(data[0])

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
        self.driver.switch_to_window(window_after)

        pdf = self.driver.find_elements_by_id('rvRpt_ctl01_ctl05_ctl00')
        if pdf:
            selector = Select(pdf[0])
            selector.select_by_value('PDF')
            time.sleep(1)
            export = self.driver.find_elements_by_id('rvRpt_ctl01_ctl05_ctl01')
            export[0].click()
            time.sleep(3)

        self.driver.switch_to_window(self.window_parent)

        page2 = self.driver.find_elements_by_id('ctl00_default_hypBacktoPage2')
        if page2:
            page2[0].click()

    def modifying_main_document(self, data):

        final_path = self.startPDFProcessing('/home/pankaj/Downloads/ReportForm1.pdf',
                                             data[0].replace('.', '-').replace('/', '-'))

        delbtn = self.driver.find_elements_by_id('ctl00_default_gvForm1Checklist_ctl02_rowbtnDelete')
        if delbtn:
            delbtn[0].click()
        time.sleep(1)

        ale = self.driver.switch_to_alert();
        ale.accept()
        time.sleep(1)

        self.driver.switch_to_window(self.window_parent)

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
        self.pdf_pages_list = []
        pdf = PdfFileReader(open(file, 'rb'))
        pages = pdf.getNumPages()
        self.parsepdf(file, 0, pages - 1)
        print(self.pdf_pages_list)
        return self.add_signature_image(file, product_name)

    def parsepdf(self, filename, startpage, endpage):

        # Open a PDF file.
        fp = open(filename, 'rb')

        # Create a PDF parser object associated with the file object.
        parser = PDFParser(fp)

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
        c.drawImage(self.signature_path, x - 60, y - 60, 100, 40)
        c.showPage()
        c.save()
        # Get the watermark file you just created
        watermark = PdfFileReader(open("test.pdf", "rb"))

        return watermark

    def is_signature_required(self, page):
        for page1 in self.pdf_pages_list:
            if page1['page'] == page:
                return page1
        return False

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
        input_file = PdfFileReader(open(file, "rb"))

        # Number of pages in input document
        page_count = input_file.getNumPages()

        # Go through all the input file pages to add a watermark to them
        for page_number in range(page_count):

            input_page = input_file.getPage(page_number)
            details = self.is_signature_required(page_number)
            if details:
                print("Watermarking page {} of {}".format(page_number, page_count))
                # merge the watermark with the page
                watermark = self.create_watermark(details['x'], details['y'])
                input_page.mergePage(watermark.getPage(0))
                self.delete_temporary_files()
                # add page from input file to output document
            output_file.addPage(input_page)

        # finally, write "output" to document-output.pdf
        print(self.final_doc_path + '/' + product_name + '.pdf');
        with open(self.final_doc_path + '/' + product_name + '.pdf', "wb") as outputStream:
            output_file.write(outputStream)

        return self.final_doc_path + '/' + product_name + '.pdf'

    def delete_temporary_files(self):
        if os.path.exists('test.pdf'):
            os.remove('test.pdf')
        if os.path.exists('output.pdf'):
            os.remove('output.pdf')

    def start(self):
        self.initiate();
        self.getCompanyInfo()
        self.get_product_other_details()
        self.login()
        self.start_filling_data()
        #final_path = self.startPDFProcessing('/home/pankaj/Downloads/ReportForm1.pdf')


pdf_parser = ProductRegistration()
# pdf_parser.start1('sample.pdf')
pdf_parser.start()
# pdf_parser.add_image('/home/omsairam6/sample.pdf', 0, 0)
