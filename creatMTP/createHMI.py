# *-* coding=utf-8
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

import xml.etree.ElementTree as etree



def createNode(nodeRoot,id, tagname,x,y,w,h,role,ref=''):
    node= Element('node',{'id':id,'tagname':tagname,'x':x,'y':y,'w':w,'h':h,'role':role,'ref':ref})
    data =Element('data')
    node.append(data)
    # SubElement(node,'', attrib)
    nodeRoot.append(node)
    
def createPValue(pValueRoot,pvid,name,adressPV,accesstypePV,datatypePV,description='empty'):
    pValue = Element('pvalue',{'pvid':pvid,'name':name,'description':description})
    SubElement(pValue,'adress').text=adressPV
    SubElement(pValue, 'accsesstype').text=accesstypePV
    SubElement(pValue,'datatype').text=datatypePV
    pValueRoot.append(pValue) 

def createPC(ePCRoot,type,server):
    pConnect=Element('pconnection')
    pConnect.set('type',type)
    pConnect.set('server',server)
    ePCRoot.append(pConnect)
    createPValue(pConnect,'54564218', 'testi','sdf54652434235644','READWRITE','REAL')
    

def createGraph(graphRoot,id,name,width, height):
    graph=Element('graph')
    graph.set('id',id)
    graph.set('name',name)
    graph.set('w',width)
    graph.set('h',height)
    graphRoot.append(graph)
    createNode(graph, 'sd5s65d', 'L001', '5', '56', '66', '56', 'pump')
    

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



filename='hmi.xml'

root=Element('hmi')
root.set('version', '1.0')
tree=ElementTree(root)

createPC(root,'OPCUA','localhost')
createGraph(root,'5454746484','filter','1920','1024')




#root.set('id','123')
indent(root)
print(etree.tostring(root))
tree.write(open(filename,'wb+'),xml_declaration=True, encoding='UTF-8')









"""

filename="hmi.xml"

def CreateXml():
    
    hmiXML=ElementTree()
    purOrder =Element("hmi")
    
    book._setroot(purOrder)
    
    generated_on = str(datetime.datetime.now())
    
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
    return hmiXML




if __name__ == '__main__':
    hmiXML =CreateXml()
    hmiXML.write(filename,"utf-8")
    #book.write("book2.xml","utf-8",True) #true is with xml declaration
"""