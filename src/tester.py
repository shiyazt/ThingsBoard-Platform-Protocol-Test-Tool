import sys
from PyQt5 import QtCore, QtGui, uic 
from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtPrintSupport import QPrintDialog, QPrintPreviewDialog, QPrinter
import requests
import json
import urllib3
import subprocess
# import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
# import resources
__author__ = "Shiyaz T"

#Load UI Files
uifile_1 = '../UI/MainPage.ui'
form_1, base_1 = uic.loadUiType(uifile_1)

uifile_2 = '../UI/AboutPage.ui'
form_2, base_2 = uic.loadUiType(uifile_2)

uifile_3 = '../UI/TestGuide.ui'
form_3, base_3 = uic.loadUiType(uifile_3)

class my_data():
    def __init__(self):
        self.url = ""
        self.token = ""
        self.protocol = ""
        self.payload_path = ""
        self.data = ""
        self.type = ""

user_data = my_data()

class Example(base_1, form_1):
    def __init__(self):
        super(base_1,self).__init__()
        self.setupUi(self)
        self.actionExit.triggered.connect(exitapp)
        self.actionAbout.triggered.connect(self.changeAbout)
        self.actionTest_Guide.triggered.connect(self.changeTestGuide)
        self.progressBar.setValue(0)
        self.comboBox.activated.connect(protocol_event)
        self.comboBox_2.activated.connect(dataType_event)
        self.lineEdit.textChanged.connect(url_event)
        self.lineEdit_2.textChanged.connect(token_event)
        #self.lineEdit_3.textChanged.connect(payload_event)
        self.pushButton_3.clicked.connect(self.upload_payload)
        self.pushButton_2.clicked.connect(send_msg)
        self.pushButton.clicked.connect(cancel_event)

    def changeAbout(self):
        self.main = AboutPage()
        self.main.show()

    def changeTestGuide(self):
        self.main = GuidePage()
        self.main.show()

    def upload_payload(self):
        user_data.payload_path = QFileDialog.getOpenFileName(self, 'Open File', '.')
        print ('Path file : ', user_data.payload_path)
        user_data.payload_path = user_data.payload_path[0]
        print(user_data.payload_path)
        user_data.data = open(user_data.payload_path).read()
        print("Data " , user_data.data)

    def export_pdf(self):
        fileName = QFileDialog.getSaveFileName(self, self.tr("Export document to PDF"), "", self.tr("PDF files (*.pdf)"))[0]
        if fileName:
            if not QFileInfo(fileName).suffix():
                fileName += ".pdf"
            title, htmltext, preview = self.currentTab.getDocumentForExport(includeStyleSheet=True,
                                            webenv=False)
            printer = self.standardPrinter(title)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(fileName)
            document = self.getDocumentForPrint(title, htmltext, preview)
            if document != None:
                document.print(printer)
class AboutPage(base_2, form_2):
    def __init__(self):
        super(base_2, self).__init__()
        self.setupUi(self)

class GuidePage(base_3, form_3):
    def __init__(self):
        super(base_3, self).__init__()
        self.setupUi(self)

def url_event(item):
    user_data.url = item
    print("URL: ", user_data.url)

def token_event(item):
    user_data.token = str(item)
    print("Access Token: ", user_data.token)




def send_msg():
    if ((user_data.url != "") & (user_data.token != "") & (user_data.data != "")):
        ex.textBrowser.setText("URL : " + user_data.url)
        ex.textBrowser.append("Access Token : " + user_data.token)
        ex.textBrowser.append("Protocol : " + user_data.protocol)
        ex.textBrowser.append("payload : " + user_data.data)
        ex.textBrowser.append("Data Type : " + user_data.type)
        ex.progressBar.setValue(50)
        if (user_data.protocol == "HTTP"):
            ex.textBrowser.append("Sending HTTP Request ...")
            if (user_data.type == "Telemetry"):  # Telemetry Data
                headers = {'Content-type': 'application/json'}
                url = (user_data.url) + "/api/v1/" + (user_data.token) + "/telemetry"
                response = requests.post(url, data=(user_data.data), headers=headers)
                code = response.status_code
                print("Status Code: " + str(code))
                #Working Code below
                # url = user_data.url
                # payload = user_data.payload_path
                # header = '"Content-Type:application/json"'
                # data = "curl -v -X POST -d  @" + (payload) +" "+(url) + " --header" + " "+(header) 
                # print(data)
                # os.system(data)
                if (code == 200):
                    ex.textBrowser.append("Data Sent Successfully")
                    ex.progressBar.setValue(100)
                elif (code != 200):
                    ex.textBrowser.append("Data Sent Failed with Error code" + str(code))
            elif (user_data.type == "Attributes"):
                headers = {'Content-type': 'application/json'}
                url = (user_data.url) + "/api/v1/" + (user_data.token) + "/attributes"
                response = requests.post(url, data=(user_data.data), headers=headers)
                code = response.status_code
                print("Status Code: " + str(code))
                if (code == 200):
                    ex.textBrowser.append("Data Sent Successfully")
                    ex.progressBar.setValue(100)
                elif (code != 200):
                    ex.textBrowser.append("Data Sent Failed with Error code" + str(code))

        elif (user_data.protocol == "CoAP"):  # Beta 
            ex.textBrowser.append("Sending CoAP Request ...")
            if (user_data.type == "Telemetry"):
                payload = "cat " + (user_data.payload_path) + " | coap post " + (user_data.url) + "/api/v1/" + (user_data.token) + "/telemetry"
                # os.system(payload)
                subprocess.check_output(payload, shell=True)
                ex.textBrowser.append("Data Sent Successfully")
                ex.progressBar.setValue(100)
            elif (user_data.type == "Attributes"):
                payload = "cat " + (user_data.payload_path) + " | coap post " + (user_data.url) + "/api/v1/" + (user_data.token) + "/attributes"
                #os.system(payload)
                subprocess.check_output(payload, shell=True)
                ex.textBrowser.append("Data Sent Successfully")
                ex.progressBar.setValue(100)
        elif (user_data.protocol == "MQTT"):
            ex.textBrowser.append("Sending MQTT Message ...")
            # client = mqtt.Client()
            #client.on_connect = on_connect
            # client.username_pw_set(user_data.token)
            # client.connect(user_data.url, 1883, 60)
            # client.loop_start()
            token  = {'username': user_data.token}
            if (user_data.type == "Telemetry"):
                try:
                    ret = publish.single('v1/devices/me/telemetry', payload=(user_data.data), qos=0, hostname=user_data.url, auth=token)
                    # client.publish('v1/devices/me/telemetry',(user_data.data),0)
                    time.sleep(1)
                    print("Telemetry Data Published\n")
                    print("ret: " + str(ret))
                    ex.progressBar.setValue(100)
                    ex.textBrowser.append("Send MQTT Message Successfully")
                except:
                    print("Telemetry Data Send Failed\n")
                    ex.textBrowser.append("Send MQTT Message Failed")

            elif (user_data.type == "Attributes"):
                try:
                    ret = publish.single('v1/devices/me/attributes', payload=(user_data.data), qos=0, hostname=user_data.url, auth=token)
                    time.sleep(1)
                    print("ret: " + str(ret))
                    # client.publish('v1/devices/me/attributes', (user_data.data),1)
                    print("Attributes Data Published\n")
                    ex.progressBar.setValue(100)
                    ex.textBrowser.append("Send MQTT Message Successfully")
                except:
                    print("Telemetry Data Send Failed\n")
                    ex.textBrowser.append("Send MQTT Message Failed")
            
            
            # client.loop_stop()
            # client.disconnect()
    else:
        print("Invalid Data")
        ex.textBrowser.append("Invalid Data")

def protocol_event(item):
    if (item == 0):
        user_data.protocol = "CoAP"
    elif (item == 1):
        user_data.protocol = "HTTP"
    elif (item == 2):
        user_data.protocol = "MQTT"
    print("Protocol: ", user_data.protocol)

def dataType_event(item):
    if (item == 0):
        user_data.type = "Attributes"
    elif (item == 1):
        user_data.type = "Telemetry"

def cancel_event():
    ex.textBrowser.setText("Cancelled")
    ex.progressBar.setValue(0)
    ex.lineEdit.clear()
    ex.lineEdit_2.clear()

def exitapp():
    sys.exit()

if __name__=='__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
