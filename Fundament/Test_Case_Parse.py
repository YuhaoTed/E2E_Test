from xml.dom.minidom import parse
import xml.dom.minidom

def TestCaseParse(file,res):
    DOMTree = xml.dom.minidom.parse(file)
    TestCases = DOMTree.documentElement
    Modules = TestCases.getElementsByTagName('Module')
    for Module in Modules:
        for TestCase in Module.getElementsByTagName('TestCase'):
            if TestCase.getElementsByTagName('TestExec')[0].childNodes[0].data=='Y':
                res.append([Module.getAttribute('Name'),TestCase.getElementsByTagName('Name')[0].childNodes[0].data])
