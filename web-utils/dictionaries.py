import requests
import urllib.parse
import json
from xml.dom import minidom
import xml.etree.ElementTree as ET

def googleTranslator(text, src, dest='EN'):
    baseUrl = "https://translate.googleapis.com/translate_a/single"
    encodedText = urllib.parse.quote(text) 
    url = f"{baseUrl}?client=gtx&sl={src}&tl={dest}&dt=t&q={encodedText}"
    res = requests.get(url)
    if res.status_code == 200:
        return json.loads(res.content)
    else: 
        raise RuntimeError(f"Error [{res.status_code}] using google translator - {res.text}")

def leo(text, src, dest='en'):
    # baseUrl = "https://dict.leo.org/dictQuery/m-query/conf/ende/query.conf/strlist.json"
    baseUrl = "https://dict.leo.org/dictQuery/m-vocab/ende/query.xml"
    encodedText = urllib.parse.quote(text)
    # url = f"{baseUrl}?q={encodedText}&shortQuery&noDescription&sideInfo=on&where=both&term={encodedText}"
    url = f"{baseUrl}?lp=ende&lang={dest}&search={encodedText}&side=both&order=basic&partial=show&sectLenMax=16&n=1&filtered=-1&trigger="
    res = requests.get(url)

    # return res.text

    if res.status_code == 200:
        result = []
        root = ET.fromstring(res.text)
        entries =  root.findall(f".//side[@lang='{dest}']")
        
        for entry in entries:
            word = entry.find("./words/word[1]")
            # originalWord = entry.findall(f"../side[@lang='{src}']/words/word[1]")[0]
            print(f"../side[@lang='{src}']")
            originalWord = entry.findall(f"../side[@lang='{src}']")[0]
            print(originalWord.text)
            if originalWord is not None and originalWord.text == text:

                wordResult = []
                
                if word is not None:
                    result.append(wordResult)
                    # print(word.text)
                    wordResult.append(word.text)
                    wordType = entry.find(".//t")
                    if wordType is not None:
                        # print(wordType.text)
                        wordResult.append(wordType.text)
            
        # return json.loads(res.content)
        return result
    else: 
        raise RuntimeError(f"Error [{res.status_code}] using google translator - {res.text}")

if __name__ == "__main__":
    # res = googleTranslator("Hallo. Wie geht's?\nIch heiße Adriano", src='DE')
    # print("Google translator:\n")
    # # print(res)
    # lines = res[0]
    # for line in lines:
    #     print(f"{line[0]}")

    res = leo("schön", src='de')
    for entry in res:
        print(entry)
    # print("Leo translator:\n")
    # print(res)
    # print(minidom.parseString(res).toprettyxml(indent="    "))


    # file = open("leo.xml", 'wb')
    # print(type(res))
    # pretty =minidom.parseString(res).toprettyxml(indent="    ", encoding="utf8")
    # print(type(pretty))
    # file.write(pretty)
    # file.close()