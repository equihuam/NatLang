import spacy
from io import BytesIO

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import re
from os import listdir


def convert(fname, pages=None, M=1.0, L=0.3, W=0.2, F=0.5):
    """ Converts a pdf filename into plain text.

    Each value is specified not as an actual length, but as a proportion of the length
    to the size of each character in question.

    Parameters define layout analysis. In a PDF text is in several chunks of various types.
    Text extraction needs to recover text chunks which ar regarded as continuous if
    elements distance is closer than the char_margin (identified as M) and thus are
    grouped into one block. Two lines are part of the same text if they are closer than
    the line_margin (L). If the distance between two words is greater than the word_margin (W),
    blank characters (spaces) shall be inserted as necessary to keep format.
    Boxes flow (F) specifies how much a horizontal and vertical position of a text matters
    when determining text flow order. The value should be within the range from -1.0
    (only horizontal position matters) to +1.0 (only vertical position matters).

    Keyword arguments:

      fname -- PDF file name (string)
      pages -- Set of pages to extract (set)
      M -- char_margin (float)
      L -- line_margin (float)
      W -- word_margin (float)
      F -- boxes_flow (float)

    Return:
      text: pdf contents as plain text

    """
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = BytesIO()
    codec = "utf-8"

    manager = PDFResourceManager()
    laparams = LAParams()
    laparams.all_texts = True
    laparams.detect_vertical = False
    laparams.char_margin = M
    laparams.line_margin = L
    laparams.word_margin = W
    laparams.boxes_flow =  F
    converter = TextConverter(manager, output, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text


pdf_files = [f for f in listdir(".") if f.endswith(".pdf")]
text = convert(fname=pdf_files[2], M=8.0, L=2.0, W=0.2, F=0.5).decode("utf-8")

text_pp = re.split("[0-9]+[ \n]*\fProyecto de Nación 2018-2024 \n", text)
text_pp = [re.sub("( \n+)+", "\n", t).strip("\n") for t in text_pp]

# text = text.split("\n[0-9]+\b\fProyecto de Nación 2018-2024 \n\n")
# re.sub()

nlp = spacy.load('en')

doc = nlp(u'This is a sentence.')

