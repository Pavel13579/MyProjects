import os 
import PyPDF2
from PyPDF2 import PdfReader , PdfWriter, PdfMerger
from tkinter import Tk
from tkinter.filedialog import askopenfilename

Tk().withdraw() 
pdfFile1 = askopenfilename() 
pdfFile2 = askopenfilename()

print(pdfFile1)
print(pdfFile2)

pdfFiles = []

pdfFiles.append(pdfFile1)
pdfFiles.append(pdfFile2)
pdfWriter = PyPDF2.PdfWriter()


interval_to_keep_first = []
interval_to_keep_second = []

first1 = input('Add first intervalnmuber to first pdf')
first2 = input('Add second intervalnmuber to first pdf')
second1 = input('Add first intervalnmuber to second pdf')
second2 = input('Add second intervalnmuber to first pdf')

interval_to_keep_first.append(int(first1))
interval_to_keep_first.append(int(first2))
interval_to_keep_second.append(int(second1))
interval_to_keep_second.append(int(second2))

cnt = 0
for filename in pdfFiles: 
    if filename.lower().endswith('.pdf'):
        pdfFileObj = open(filename, 'rb') 
        pdfReader = PyPDF2.PdfReader(pdfFileObj) 
        if(cnt == 0):
            for i in range(len(pdfReader.pages)):
                if i in interval_to_keep_first:
                    p = pdfReader.pages[i]
                    pdfWriter.add_page(p)
        elif(cnt == 1):
            for i in range(len(pdfReader.pages)):
                if i in interval_to_keep_second:
                    p = pdfReader.pages[i]
                    pdfWriter.add_page(p)
        cnt += 1
    else:
        exit()






pdfOutput = open('Power_BI_Test_Files.pdf', 'wb') 
pdfWriter.write(pdfOutput)
pdfOutput.close()
        