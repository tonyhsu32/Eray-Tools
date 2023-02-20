import xml.etree.ElementTree as ET
import os
import re

# xml file path
# xml_path = "/home/eray/Documents/xml_2_json/2__00157.xml"   

# xml folder path
xml_folder_path = "/home/eray/Documents/xml_2_json/20220428_小揚/xml"


class ParseXML:
    def __init__(self, path):
        self.xml_path = path
        self.obj_name = []
        
    def parseTree(self):
        tree = ET.parse(self.xml_path)
        root = tree.getroot()

        return root

    def iterTree(self):
        root = self.parseTree()
        
        for obj in root.iter("object"):
            name = obj.find("name").text
            if name not in self.obj_name:
                self.obj_name.append(name)

        return self.obj_name
        
# xml_obj = ParseXML(xml_path).iterTree()
# print(xml_obj)


def cal_muti_xml_not_repeat_obj(dir_path):
    count = 0
    total_no_repeat_obj = []
    pattern = re.compile(r".xml$")
    for xml_path in os.listdir(dir_path):
        if re.search(pattern, xml_path):
            xml_obj = ParseXML(os.path.join(dir_path, xml_path)).iterTree()
            
            for obj in xml_obj:
                if obj not in total_no_repeat_obj:
                    total_no_repeat_obj.append(obj)
            
            print(os.path.join(dir_path, xml_path))
            count += 1
    print(f" =========== < {count} > xml files not repeat object has been calculated! ===========")
    print(f"total obj sample: {total_no_repeat_obj}")


if __name__ == "__main__":
    cal_muti_xml_not_repeat_obj(xml_folder_path)

    