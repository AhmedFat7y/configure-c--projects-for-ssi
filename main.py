import xml.etree.ElementTree as ET
from os.path import isfile, join, abspath, dirname
from os import listdir
from sys import argv

XML_TAG_SUFFIX = "%s"

SSI_DIR_PREFIX = "%s"
SSI_INCLUDE_DIRECTORY = r'core\include\;'
SSI_LIB_DIRECTORY = r'libs\Win32\vc10\;'
SSI_BIN_DIRECTORY = r'bin\Win32\vc10\;'
SSI_PLUGINS_DIRECTORY = 'plugins\'
SSI_PLUGINS_INCLUDE_DIRECTORY = 'plugins\%s\include\;'

def editDebugProperties(properties_node):
  properties_node.find(XML_TAG_SUFFIX % "TargetName").text = "ssi$(ProjectName)d"
  properties_node.find(XML_TAG_SUFFIX % "OutDir").text =  SSI_DIR_PREFIX % SSI_BIN_DIRECTORY
  pass
def editReleaseProperties(properties_node):
  properties_node.find(XML_TAG_SUFFIX % "TargetName").text = "ssi$(ProjectName)"
  properties_node.find(XML_TAG_SUFFIX % "OutDir").text =  SSI_DIR_PREFIX % SSI_BIN_DIRECTORY
  pass
def editReleaseLink(link_node):
  link_node.find(XML_TAG_SUFFIX % "AdditionalLibraryDirectories") = (SSI_DIR_PREFIX % SSI_LIB_DIRECTORY) + (SSI_DIR_PREFIX % SSI_BIN_DIRECTORY)
  link_node.find(XML_TAG_SUFFIX % "AdditionalDependencies") = ""
  link_node.find(XML_TAG_SUFFIX % "OutputFile") = "$(TargetPath)"
  
  pass
def editReleaseClCompile(clcompile_node):
  link_node.find(XML_TAG_SUFFIX % "AdditionalIncludeDirectories") = (SSI_DIR_PREFIX % SSI_INCLUDE_DIRECTORY)
  pass
def editDebugClCompile(clcompile_node):
  link_node.find(XML_TAG_SUFFIX % "AdditionalIncludeDirectories") = (SSI_DIR_PREFIX % SSI_INCLUDE_DIRECTORY)
  pass
def editDebugLink(Link_node):
  link_node.find(XML_TAG_SUFFIX % "AdditionalLibraryDirectories") = (SSI_DIR_PREFIX % SSI_LIB_DIRECTORY) + (SSI_DIR_PREFIX + SSI_BIN_DIRECTORY)
  link_node.find(XML_TAG_SUFFIX % "AdditionalDependencies") = ""
  link_node.find(XML_TAG_SUFFIX % "OutputFile") = "$(TargetPath)"
  pass

def initialize():
  current_dir = dirname(abspath(''))
  new_dir = ""
  while current_dir[-3:] != "ssi":
    current_dir = dirname(current_dir)
    new_dir =  r'..\'  + new_dir
  SSI_DIR_PREFIX = new_dir
  
  
def main():
  tree = ET.parse(argv[0])
  root = tree.getroot()
  roottag = root.tag
  XML_TAG_SUFFIX = roottag[roottag.find("{") : roottag.find("}") + 1] + XML_TAG_SUFFIX
  for child in root:
    if child.tag == XML_TAG_SUFFIX % "PropertyGroup" and not child.attrib.has_key("Label") and child.attrib.has_key("Condition"):
      if child.attrib["Condition"] == "'$(Configuration)|$(Platform)'=='Debug|Win32'":
        editDebugProperties(child)
      elif child.attrib["Condition"] == "'$(Configuration)|$(Platform)'=='Release|Win32'":
        editReleaseProperties(child)
      else:
        pass
    elif child.tag == XML_TAG_SUFFIX % "ItemDefinitionGroup" and child.attrib.has_key("Condition"):
      compile_child = child.find(XML_TAG_SUFFIX % "ClCompile")
      link_child = child.find(XML_TAG_SUFFIX % "Link")
      
      if child.attrib["Condition"] == "'$(Configuration)|$(Platform)'=='Release|Win32'":
        editReleaseClCompile(compile_child)
        editReleaseLink(link_child)
      else:
        editReleaseClCompile(compile_child)
        editDebugLink(link_child)
    else:
      pass
if __name__ == "main"
  main()