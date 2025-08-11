
from tkinter.filedialog import *
import PyPDF2
import pyttsx3
 
book=askopenfilename(title="Select a PDF file", filetypes=[("PDF files", "*.pdf")])
pdfreader=PyPDF2.PdfReader(book)
pages=len(pdfreader.pages)

for num in range(0,pages):
    page=pdfreader.pages[num]
    text=page.extract_text()
    speaker=pyttsx3.init()
    speaker.say(text)
    speaker.runAndWait()