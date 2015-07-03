# *-* coding=utf-8
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import dump
from xml.etree.ElementTree import Comment
from xml.etree.ElementTree import tostring
import os

filename="pvalue.xml"
def CreateXml():
    value=ElementTree()
    pvalue =Element("pvalue",{"pvid":"","name":"","description":""})
    value._setroot(pvalue)

   
    
    address= Element("address")
    accesstype=Element("accesstype")
    datatype=Element("datatype")
    
    
    pvalue.append(address)
    pvalue.append(accesstype)
    pvalue.append(datatype)
    
    
    
    indent(pvalue)
    return value


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
    value =CreateXml()
    value.write(filename,"utf-8")
    #book.write("book2.xml","utf-8",True) #true is with xml declaration

