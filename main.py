from json2xml import json2xml
from json2xml.utils import readfromstring
import time


def my_json_to_xml(strJsonFile):
    class MyStack:
        def __init__(self):
            self.arr = []

        def push(self, elem):
            self.arr.append(elem)

        def pop(self):
            return self.arr.pop()

        def size(self):
            return len(self.arr)

        def empty(self):
            return bool(len(self.arr))

    stackOfTags = MyStack()

    it = 0
    tagMode = True

    xmlText = '<?xml version="1.0" ?>\n'
    stackOfTags.push("root")
    xmlText += "<root>"

    while it < len(strJsonFile):

        if strJsonFile[it] == ',':
            xmlText += "</" + stackOfTags.pop() + ">\n"

        if strJsonFile[it] == '}':
            xmlText += "</" + stackOfTags.pop() + ">\n" + "\t" * (stackOfTags.size() - 1)

        if strJsonFile[it] == '{':
            xmlText += "\n"
            tagMode = True

        if strJsonFile[it] == '"':

            if tagMode:
                currentTag = ""
                it += 1
                while strJsonFile[it] != '"':
                    currentTag += strJsonFile[it]
                    it += 1

                xmlText += "\t" * stackOfTags.size() + '<{}>'.format(currentTag)
                stackOfTags.push(currentTag)

                it += 1
                tagMode = False

            else:
                currentBody = ""
                it += 1
                while strJsonFile[it] != '"':
                    currentBody += strJsonFile[it]
                    it += 1

                xmlText += currentBody

                tagMode = True

        it += 1

    xmlText += "</" + stackOfTags.pop() + ">"

    return xmlText


def auto_json_to_xml(strJsonFile):
    data = readfromstring(strJsonFile)
    return json2xml.Json2xml(data, attr_type=True).to_xml()


def test_100_iter(strJsonFile, mode):
    for _ in range(100):
        if mode:
            my_json_to_xml(strJsonFile)
        else:
            auto_json_to_xml(strJsonFile)


def normal_start():
    jsonFile = open("inFile.json", "r", encoding="utf-8")
    myXmlFile = open("myOutFile.xml", "w", encoding="utf-8")
    autoXmlFile = open("autoOutFile.xml", "w", encoding="utf-8")

    strJsonFile = jsonFile.read()

    myXmlText = my_json_to_xml(strJsonFile)
    autoXmlText = auto_json_to_xml(strJsonFile)

    myXmlFile.write(myXmlText)
    autoXmlFile.write(autoXmlText)

    jsonFile.close()
    myXmlFile.close()
    autoXmlFile.close()


def time_test_start():
    jsonFile = open("inFile.json", "r", encoding="utf-8")
    strJsonFile = jsonFile.read()

    start_time = time.time()
    test_100_iter(strJsonFile, True)
    myTime = time.time() - start_time

    start_time = time.time()
    test_100_iter(strJsonFile, False)
    autoTime = time.time() - start_time

    print("json2xml парсер: {}c".format(round(autoTime, 4)))
    print("     мой парсер: {}с".format(round(myTime, 4)))


normal_start()
time_test_start()
