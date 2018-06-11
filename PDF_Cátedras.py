from Prueba_1 import convert
from os import listdir
import re
import json
import spacy
import csv


def getComponents(text):
    comp = {}
    txtChars = r"[\\\a-zA-Z0-9áéíóúüñÁÉÍÓÚÜÑº*<>\?¿!¡\s:(),;.-]*"
    comp["text"] = text
    comp["proyecto"] = re.search("(?<=Número proyecto\:).*", text).group(0).replace("\n", " ").replace("\s", "").strip()
    comp["institucion"] = re.search(r"(?<=Institución\: \n).*", text).group(0).replace("\n", " ").replace("\f", "")
    comp["dependencia"] = re.search(r"(?<=Dependencia\: \n).*", text).group(0).replace("\n", " ").replace("\f", "")
    comp["departamento"] = re.search(r"(?<=División/Departamento\: \n).*", text
                                     ).group(0).replace("\n", " ").replace("\f", "")
    comp["titulo"] = re.search(r"(?<=Título del Proyecto\:\n)" + txtChars + "(?=Modalidad)",
                               text, re.MULTILINE).group(0).replace("\n", " ").replace("\f", "")
    comp["modalidad"] = re.search(r"(?<=Modalidad\:\n).*", text).group(0).replace("\n", " ").replace("\f", "")
    comp["peciti"] = re.search(r"(?<=Tema del PECiTI\: \n).*", text).group(0).replace("\n", " ").replace("\f", "")
    comp["reto"] = re.search(r"(?<=Reto\: \n).*", text).group(0).replace("\n", " ").replace("\f", "")
    comp["entidad"] = re.search(r"(?<=Entidad Federativa sede del proyecto\:\n).*",
                                text).group(0).replace("\n", " ").replace("\f", "")
    comp["proposito"] = re.search(r"(?<=Propósito de proyecto institucional\n)" + txtChars +
                                  r"(?= Objetivo general del proyecto)",
                                  text, re.MULTILINE).group(0)
    comp["objetivos"] = re.search(r"(?<=Objetivo general del proyecto\n)" + txtChars +
                                  r"(?= Motivos de la Institución para desarrollar el proyecto)",
                                  text, re.MULTILINE).group(0)
    comp["motivosInst"] = re.search(r"(?<=Motivos de la Institución para desarrollar el proyecto\n)" + txtChars +
                                    r"(?= Contribución esperada de la\(s\) cátedra\(s\))",
                                    text, re.MULTILINE).group(0)
    comp["contribucion"] = re.search(r"(?<=Contribución esperada de la\(s\) cátedra\(s\)\n)" + txtChars +
                                     r"(?= Resultados e impactos esperados \(a 5 y 10 años\))",
                                     text, re.MULTILINE).group(0)
    comp["resultados"] = re.search(r"(?<=Resultados e impactos esperados \(a 5 y 10 años\)\n)" + txtChars +
                                   r"(?=Vinculación, pertinencia y perspectivas de transferencia de conocimiento" +
                                   r" o tecnología)", text, re.MULTILINE).group(0)
    comp["vinculacion"] = re.search(r"(?<=Vinculación, pertinencia y perspectivas de transferencia de" +
                                    r" conocimiento o tecnología" + r" \(si aplica\)\n)" + txtChars +
                                    r"(?=Descripción del grupo de Investigación o personal académico asociado" +
                                    r" al proyecto)", text, re.MULTILINE).group(0)
    return comp


def cleanData(dict):
    for k, d in dict.items():
        d = re.sub(r"\s+", " ", d)
        d = re.sub(r" Página [0-9]+ ", " ", d)
        d = re.sub(r"Descripción del proyecto ", " ", d)
        d = re.sub(r"\(cid\:9\)", "", d)
        d = re.sub(r"¿ ", "¿", d)
        d = re.sub(r"\n+", " ", d)
        d = re.sub(r" +", " ", d)
        dict[k] = d
    return dict


# %% Main
pdf_files = [f for f in listdir(".") if f.endswith(".pdf")]
documents = [f for f in pdf_files if "generaR" in f]

# Get components
bowDocs, componentes = [], []
for doc in documents:
    text = convert(fname=doc, M=1, L=10, W=0.1, F=-1.00).decode("utf-8")
    docData = getComponents(text)
    componentes.append(docData)
    cleanData(docData)
    bow = "\n".join([docData["proposito"], docData["objetivos"], docData["motivosInst"],
                     docData["contribucion"], docData["resultados"], docData["vinculacion"]])

    with open("./temp/{}-catedra-CONACyT.json".format(docData["proyecto"]), "w", encoding="utf-8") as outFile:
        json.dump(docData, outFile)

    with open("./temp/{}-catedra-CONACyT.txt".format(docData["proyecto"]), "w", encoding="utf-8") as outFile:
        outFile.write(bow)

    bowDocs.append(bow)


nlp = spacy.load("es")

docs = [nlp(d) for d in bowDocs]
docs