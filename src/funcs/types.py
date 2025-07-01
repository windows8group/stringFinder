import os
from libtextworker.general import WalkCreation
import xml.etree.ElementTree as ET

TEMPLATE_RES: str = open(os.path.join(os.path.dirname(__file__), "template.xml"), "r").read()

class ATranslation:
    """
    A struct presenting a translation/string
    resource in ResX-formatted files
    """

    name: str
    value: str
    comment: str

    def to_element(this) -> ET.Element:
        assert this.name

        result = ET.Element("data")
        result.set("name", this.name)
        result.set("xml.space", "preserve")

        ET.SubElement(result, "value").text = this.value

        if this.comment:
            ET.SubElement(result, "comment").text = this.comment
        
        return result

class ATranslationFile:
    """
    Presents a resw/resx file.
    """

    strings: list[ATranslation]
    tree: ET.ElementTree
    input_file: str
    language: str

    def read(this, input_str: str):
        if not os.path.isfile(input_str):
            WalkCreation(os.path.dirname(input_str))
            open(input_str, "w").write(TEMPLATE_RES)

        this.language = os.path.split(os.path.dirname(input_str))
        assert this.language
        
        this.tree = ET.ElementTree()
        this.tree.parse(input_str)
        this.input_file = input_str

        # Now time to find for translations
        for child in this.tree.getroot().iter("data"):
            newobj = ATranslation()
            newobj.name = child.attrib["name"]
            
            if value := child.find("value"):
                newobj.value = value.text

            if comment := child.find("comment"):
                newobj.comment = comment.text

            this.strings.append(newobj)

    def write(this):
        for stringelm in this.strings:
            this.tree.getroot().append(stringelm.to_element())
        this.tree.write(this.input_file, "utf-8")
