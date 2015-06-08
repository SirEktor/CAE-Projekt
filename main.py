import xml.etree.cElementTree as ET
import copy

# XML-Datei einlesen
root=ET.parse("filter.xml").getroot()
# Device mit Attribut Description=="Filter" suchen
filter=root.find("./Device[@Description='Filter']")

# leere Liste erstellen , welche alle Devices in einer Ebene speichert
rml=[]
# 1. Ebene Filter hinzufügen
rml.append(filter)
while len(rml)>0:
    # Durch alle Device Objekte in einer Ebene iterieren
    for o in rml:
        print(o.attrib["Description"])
        # alle Device Kinder finden kopieren und an Eltern Device anhängen, um dann löschen zu können
        for e in o.findall("./Elements/Device"):
            c=copy.deepcopy(e)
            o.append(c)
            rml.append(c)
        # Alle Unterelemente von Device löschen, die keine weiteren Devices sind    
        for e in o.findall('./*'):            
            if(e.tag!='Device'):
                o.remove(e)
        
        # Bearbeitetes Device aus Liste löschen
        rml.remove(o)

# Ausgabe Datei erzeugen und beschreiben
out=open("new_filter.xml",'w')
out.write(ET.tostring(filter,"utf-8").decode("utf-8"))
    

    
       



