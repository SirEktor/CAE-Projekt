import xml.etree.cElementTree as ET
import copy
import zipfile
import tempfile
import os
import sys
import shutil


class OPCUAXMLReference:
    def __init__(self,type,nodeid,is_forward):
        # Typ der Referenz,gibt an welche Beziehung verwendet wird
        self.type=type
        # Konten-Id des Knotens auf welchen referenziert wird
        self.nodeid=nodeid
        # Richtung der Referenz(Beziehung)
        self.is_forward=is_forward
        
    # Darstellung der Refrenz als XML
    def __str__(self):
        text="<Reference ReferenceType=\"{0}\" IsForward=\"{1}\">i={2}</Reference>"
        return text.format(self.type,self.is_forward,self.nodeid)

class OPCUAXMLObject:
    def __init__(self,nodeid,name,references):
        # Konten-Id des Objektes
        self.nodeid=nodeid
        # Suchname des Objektes
        self.browse_name=name.strip()
        # Anzeigenamen des Objektes
        self.display_name=name
        # Referenzen des Objektes
        self.references=references
        
    # Darstellung des Objektes als XML    
    def __str__(self):
        text="<UAObject NodeId=\"i={0}\" BrowseName=\"{1}\">\n"
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
        # Konten-Id der Variabel
        self.nodeid=nodeid
        # Suchname der Variabel
        self.browse_name=name.strip()
        # Anzeigenamen der Variabel
        self.display_name=name
        # Datentyp der Variabel
        self.data_type=data_type
        # Referenzen der Variabel
        self.references=references
        # Wert der Variabel
        self.value=value
    
    # Darstellung der Variabel als XML
    def __str__(self):
        text="<UAVariable NodeId=\"i={0}\" BrowseName=\"{1}\" DataType=\"{3}\">\n"
        text+="\t<DisplayName>{2}</DisplayName>\n"
        if len(self.references)>0:
            text+="\t<References>\n"
            for r in self.references:
                text+="\t\t"+str(r)+"\n"
            text+="\t</References>\n"
            text+="\t<Value><String>{4}</String></Value>\n"
        text+="</UAVariable>\n"
        return text.format(self.nodeid,self.browse_name,self.display_name,self.data_type,self.value.replace("&","&amp;").replace("\\","/"))

if __name__ == '__main__':
    # Debug
    debug=True
    
    
    # MTP-Datei öffnen und temporären Ordner erstellen
    filename=sys.argv[0]
    if filename==None:
        filename=filename
    mtp=zipfile.ZipFile('2014-12-10-PlantModule.mtp')
    tmp_dir=tempfile.mkdtemp()
    mtp.extractall(tmp_dir)
    
    # Manifest XML-Datei einlesen 
    mtf=ET.parse(os.path.join(tmp_dir,'PlantModule/Metadata/manifest.xml')).getroot()
    
    
    # Weitere Dateien suchen
    # Es wird in der Manifestdatei nach weiteren XML-Datein gesucht und innerhalb ihres 
    # Tags in die Manifest-XML-Datei eingebunden
    
    fn=mtf.findall(".//*[@FileName]")
    for f in fn:
        file=f.attrib["FileName"]
        file="PlantModule/"+file.replace("\\","/")[1:]
    
        
        if(file.find(".xml")>0):
            # Debugausgabe
            if debug:
                print(file)
            try:
                xmlf=ET.parse(os.path.join(tmp_dir,file)).getroot()
                f.append(copy.deepcopy(xmlf))
            except Exception as e:
                print("Fehler beim Laden von "+file+" :")
                print(e)
    
    

    # OPCUA Struktur erzeugen 
    
    nodeid=20000    # Startknoten ID
    
    object_list=[]  # Liste aller gefundenen OPCUA-Objekte
    var_list=[]     # Liste aller gefundenen OPCUA-Variabeln
    
    # Wuzelobjekt der Struktur erzeugen - Manifest-TAG
    object_list.append(OPCUAXMLObject(nodeid,str(mtf.tag),[OPCUAXMLReference("HasComponent",str(85),"false")]))
    # ne... Liste mit den nächsten XML-Elementen für den nächsten Iterationsschritt
    ne=[[mtf,nodeid]]
    nodeid+=1
    
    # Solange es noch weitere XML-Elemente gibt nach OPCUA Knoten suchen
    while len(ne)>0:
        # Liste der nächsten Elemente ne an tne kopieren und dann leeren,
        # sodass Elemente für den nächsten Iterationsschritt hinzugefügt werden können
        # und die aktuellen Elemente noch bearbeitet werden können
        tne=copy.deepcopy(ne)
        ne.clear()
        # Alle XML-Elemente iterieren
        for e in tne:
            # Alle Kinder-Elemente iterieren
            for se in e[0]:
                # TAG-Namen bearbeiten
                
                # Debugausgabe
                if debug:
                    print("Object: "+se.tag+" Parent: "+str(e[1])+" NodeID: "+str(nodeid))
                
                # Aus TAG-Namen OPCUA-Objekt erzeugen und auf Eltrenknoten referenzieren
                object_list.append(OPCUAXMLObject(nodeid,str(se.tag),[
                                    OPCUAXMLReference("HasComponent",str(e[1]),"false")]))
                ne.append([se,nodeid])
                nodeid+=1
                
                
                
                # Alle Attribute bearbeiten
                for a in se.attrib:
                    
                    # Debugausgabe
                    if debug: 
                        print("Property: "+a+" Value: "+se.attrib[a]+" Parent: "+" NodeID: "+str(nodeid))
                    
                    # Aus Attribut-Namen OPCUA-Variabel erzeugen und auf Elternknoten referenzieren
                    var_list.append(OPCUAXMLVar(nodeid,str(a),[
                                    OPCUAXMLReference("HasProperty",str(e[1]),"false")],
                                                "String",se.attrib[a]))
                    nodeid+=1
                
                # Text-Attribut bearbeiten
                # Falls nur Füllzeichen verwendet werden oder kein Text-Attribut verfügbar ist, dann nicht bearbeiten
                text=str(se.text)
                if text.strip()=="" or text=="None":
                    text=""
                if text!="":
                    # Debugausgabe
                    if debug:
                        print("Property: Text"+" Value: "+text+" Parent: "+str(e[1])+" NodeID: "+str(nodeid))
                    # Aus Text-Attribut OPCUA-Variabel erzeugen und auf Elternknoten referenzieren
                    var_list.append(OPCUAXMLVar(nodeid,"Text",[
                                    OPCUAXMLReference("HasProperty",str(e[1]),"false")],
                                                "String",text))
                    nodeid+=1
                
    
    # Alle Knoten als ihre XML-Repräsentation ausgeben
    text="<UANodeSet Version=\"1.02\" LastModified=\"2013-03-06T05:36:43.4892317Z\"><Aliases><Alias Alias=\"Boolean\">i=1</Alias><Alias Alias=\"SByte\">i=2</Alias><Alias Alias=\"Byte\">i=3</Alias><Alias Alias=\"Int16\">i=4</Alias><Alias Alias=\"UInt16\">i=5</Alias><Alias Alias=\"Int32\">i=6</Alias><Alias Alias=\"UInt32\">i=7</Alias><Alias Alias=\"Int64\">i=8</Alias><Alias Alias=\"UInt64\">i=9</Alias><Alias Alias=\"Float\">i=10</Alias><Alias Alias=\"Double\">i=11</Alias><Alias Alias=\"DateTime\">i=13</Alias><Alias Alias=\"String\">i=12</Alias><Alias Alias=\"ByteString\">i=15</Alias><Alias Alias=\"Guid\">i=14</Alias><Alias Alias=\"XmlElement\">i=16</Alias><Alias Alias=\"NodeId\">i=17</Alias><Alias Alias=\"ExpandedNodeId\">i=18</Alias><Alias Alias=\"QualifiedName\">i=20</Alias><Alias Alias=\"LocalizedText\">i=21</Alias><Alias Alias=\"StatusCode\">i=19</Alias><Alias Alias=\"Structure\">i=22</Alias><Alias Alias=\"Number\">i=26</Alias><Alias Alias=\"Integer\">i=27</Alias><Alias Alias=\"UInteger\">i=28</Alias><Alias Alias=\"HasComponent\">i=47</Alias><Alias Alias=\"HasProperty\">i=46</Alias><Alias Alias=\"Organizes\">i=35</Alias><Alias Alias=\"HasEventSource\">i=36</Alias><Alias Alias=\"HasNotifier\">i=48</Alias><Alias Alias=\"HasSubtype\">i=45</Alias><Alias Alias=\"HasTypeDefinition\">i=40</Alias><Alias Alias=\"HasModellingRule\">i=37</Alias><Alias Alias=\"HasEncoding\">i=38</Alias><Alias Alias=\"HasDescription\">i=39</Alias></Aliases>\n"
    for o in object_list:
        text+=str(o)
    for v in var_list:
        text+=str(v)   
    text+="</UANodeSet>"
    
    # Ausgabe Datei erzeugen und beschreiben
    out=open("mtpall.xml",'w')
    out.write(ET.tostring(mtf,"utf-8").decode("utf-8"))
    out=open("opcuanode.xml",'w')
    out.write(text)
    
    # temporäre Daten löschen
    shutil.rmtree(tmp_dir)

