import xml.etree.cElementTree as ET
import copy
from time import sleep

# XML-Datei einlesen
mtf=ET.parse("manifest.xml").getroot()

tabs=""


class OPCUAXMLReference:
    def __init__(self,type,nodeid,is_forward):
        self.type=type
        self.nodeid=nodeid
        self.is_forward=is_forward
        
    def __str__(self):
        text="<Reference ReferenceType=\"{0}\" IsForward=\"{1}\">{2}</Reference>"
        return text.format(self.type,self.is_forward,self.nodeid)

class OPCUAXMLObject:
    def __init__(self,nodeid,name,references):
        self.nodeid=nodeid
        self.browse_name=name.strip()
        self.display_name=name
        self.references=references
        
    def __str__(self):
        text="<UAObject NodeId=\"{0}\" BrowseName=\"{1}\">\n"
        text+="\t<DisplayName>{2}</DisplayName>\n"
        if len(self.references)>0:
            text+="\t<References>\n"
            for r in self.references:
                text+="\t\t"+str(r)+"\n"
            text+="\t</References>\n"
        text+="</UAObject>\n"
        return text.format(self.nodeid,self.browse_name,self.display_name)
        
        
class OPCUAXMLVar:
    def __init__(self,nodeid,name,references,data_type,value):
        self.nodeid=nodeid
        self.browse_name=name.strip()
        self.display_name=name
        self.data_type=data_type
        self.references=references
        self.value=value
    
    def __str__(self):
        text="<UAVariable NodeId=\"{0}\" BrowseName=\"{1}\" DataType=\"{3}\">\n"
        text+="\t<DisplayName>{2}</DisplayName>\n"
        if len(self.references)>0:
            text+="\t<References>\n"
            for r in self.references:
                text+="\t\t"+str(r)+"\n"
            text+="\t</References>\n"
            text+="\t<Value><String>{4}</String></Value>\n"
        text+="</UAVariable>\n"
        return text.format(self.nodeid,self.browse_name,self.display_name,self.data_type,self.value)



nodeid=348957

object_list=[]
var_list=[]

# root-Objekt
#print(tabs+"Object: "+mtf.tag+" Parent: None "+"NodeID: "+str(nodeid))
object_list.append(OPCUAXMLObject(nodeid,str(mtf.tag),[]))
ne=[[mtf,nodeid]]
nodeid+=1


while len(ne)>0:
    tne=copy.deepcopy(ne)
    ne.clear()
    for e in tne:
        for se in e[0]:
            # TAG-Namen ausgeben
            # <Reference ReferenceType="HasSubtype" IsForward="false">i=27</Reference>
            #print(tabs+"Object: "+se.tag+" Parent: "+str(e[1])+" NodeID: "+str(nodeid))
            object_list.append(OPCUAXMLObject(nodeid,str(se.tag),[
                                OPCUAXMLReference("HasComponent",str(e[1]),"false")]))
            ne.append([se,nodeid])
            nodeid+=1
            # Alle Attribute ausgeben
            for a in se.attrib: 
                #print(tabs+"Property: "+a+" Value: "+se.attrib[a]+" Parent: "+" NodeID: "+str(nodeid))
                var_list.append(OPCUAXMLVar(nodeid,str(se.tag),[
                                OPCUAXMLReference("HasProperty",str(e[1]),"false")],
                                            "String",se.attrib[a]))
                nodeid+=1
            # Text-Attribut
            text=str(se.text)
            if text.strip()=="" or text=="None":
                text=""
            if text!="":
                #print(tabs+"Property: Text"+" Value: "+text+" Parent: "+str(e[1])+" NodeID: "+str(nodeid))
                var_list.append(OPCUAXMLVar(nodeid,"Text",[
                                OPCUAXMLReference("HasProperty",str(e[1]),"false")],
                                            "String",text))
            
            
            nodeid+=1
            


text="<UANodeSet Version=\"1.02\" LastModified=\"2013-03-06T05:36:43.4892317Z\"><Aliases><Alias Alias=\"Boolean\">i=1</Alias><Alias Alias=\"SByte\">i=2</Alias><Alias Alias=\"Byte\">i=3</Alias><Alias Alias=\"Int16\">i=4</Alias><Alias Alias=\"UInt16\">i=5</Alias><Alias Alias=\"Int32\">i=6</Alias><Alias Alias=\"UInt32\">i=7</Alias><Alias Alias=\"Int64\">i=8</Alias><Alias Alias=\"UInt64\">i=9</Alias><Alias Alias=\"Float\">i=10</Alias><Alias Alias=\"Double\">i=11</Alias><Alias Alias=\"DateTime\">i=13</Alias><Alias Alias=\"String\">i=12</Alias><Alias Alias=\"ByteString\">i=15</Alias><Alias Alias=\"Guid\">i=14</Alias><Alias Alias=\"XmlElement\">i=16</Alias><Alias Alias=\"NodeId\">i=17</Alias><Alias Alias=\"ExpandedNodeId\">i=18</Alias><Alias Alias=\"QualifiedName\">i=20</Alias><Alias Alias=\"LocalizedText\">i=21</Alias><Alias Alias=\"StatusCode\">i=19</Alias><Alias Alias=\"Structure\">i=22</Alias><Alias Alias=\"Number\">i=26</Alias><Alias Alias=\"Integer\">i=27</Alias><Alias Alias=\"UInteger\">i=28</Alias><Alias Alias=\"HasComponent\">i=47</Alias><Alias Alias=\"HasProperty\">i=46</Alias><Alias Alias=\"Organizes\">i=35</Alias><Alias Alias=\"HasEventSource\">i=36</Alias><Alias Alias=\"HasNotifier\">i=48</Alias><Alias Alias=\"HasSubtype\">i=45</Alias><Alias Alias=\"HasTypeDefinition\">i=40</Alias><Alias Alias=\"HasModellingRule\">i=37</Alias><Alias Alias=\"HasEncoding\">i=38</Alias><Alias Alias=\"HasDescription\">i=39</Alias></Aliases>\n"
for o in object_list:
    text+=str(o)
for v in var_list:
    text+=str(v)   
text+="</UANodeSet>"

# Ausgabe Datei erzeugen und beschreiben
out=open("opcua.xml",'w')
out.write(text)

