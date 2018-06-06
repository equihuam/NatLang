import spacy
from spacy import displacy
from pathlib import Path

nlp = spacy.load('en')
sentences = ["This is an example.", "This is another one."]
doc = nlp("The big grey dog ate all of the chocolate, but fortunately he wasn't sick!")
#displacy.serve(doc, style='dep')

for sent in sentences:
    doc = nlp(sent)
    svg = displacy.render(doc, style='dep')
    file_name = '-'.join([w.text for w in doc if not w.is_punct]) + '.svg'
    output_path = Path('C:/Users/equih/PycharmProjects/NatLang-1/images/' + file_name)
    output_path.open('w', encoding='utf-8').write(svg)

text = """But Google is starting from behind. The company made a late push
into hardware, and Apple’s Siri, available on iPhones, and Amazon’s Alexa
software, which runs on its Echo and Dot devices, have clear leads in
consumer adoption."""

nlp = spacy.load('custom_ner_model')
doc = nlp(text)
displacy.serve(doc, style='ent')