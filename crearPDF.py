# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 13:17:58 2020

@author: Camilo Martínez
"""
import PyPDF2

pdfReader = PyPDF2.PdfFileReader('hola.pdf')
pdf_writer = PyPDF2.PdfFileWriter()
start = 1031
end = 1032
while start<=end:
    pdf_writer.addPage(pdfReader.getPage(start-1))
    start+=1

output_filename = 'out.pdf'
with open(output_filename,'wb') as out:
    pdf_writer.write(out)