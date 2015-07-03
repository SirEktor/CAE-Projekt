# *-* coding=utf-8
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import dump
from xml.etree.ElementTree import Comment
from xml.etree.ElementTree import tostring
import os

filename="MTP.xml"
def CreateXml():
    book =ElementTree()
    purOrder =Element("MTP")
    book._setroot(purOrder)

    list = Element("account",{'id':'2390094'})
    purOrder.append(list)
    item = Element("item1",{"Adresse":"abcd","Attribute":"4"})
    SubElement(item,"Name").text="Ventil1"
    SubElement(item,"Description").text="Wasserleitung1"
    purOrder.append(item)
    
    item = Element("item2",{"Adresse":"gfhi","attribute":"40"})
    SubElement(item,"Name").text="Ventil2"
    SubElement(item,"Description").text="Wasserleitung2"
    purOrder.append(item)
    
    indent(purOrder)
    return book


def indent(elem,level=0):
    i ="\n"+level*"    "
    print (elem);
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        for e in elem:
            print (e)
            indent(e,level+1)
        if not e.tail or not e.tail.strip():
            e.tail =i
    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail =i
    return elem
if __name__ == '__main__':
    book =CreateXml()
    book.write(filename,"utf-8")
    #book.write("book2.xml","utf-8",True) #true is with xml declaration

