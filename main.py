import xml.etree.ElementTree as ET
from os.path import isfile, join, abspath, dirname, lexists
from os import listdir
from sys import argv
import pdb


XML_TAG_SUFFIX = "%s"
INPUT_FILE = argv[1]
try:
  OVERRIDE_OPTION = (argv[2] == "-r")
except:
  OVERRIDE_OPTION = False
SSI_PLUGIN_NAME = ""
SSI_DIR_PREFIX = "%s"
SSI_CURRENT_PLUGIN_PREFIX = '%s'
SSI_INCLUDE_DIRECTORY = 'core\\include\\;'
SSI_LIB_DIRECTORY = 'libs\\Win32\\vc10\\;'
SSI_BIN_DIRECTORY = 'bin\\Win32\\vc10\\;'
SSI_PLUGINS_DIRECTORY = 'plugins\\'
SSI_PLUGINS_INCLUDE_DIRECTORY = 'plugins\\%s\\include\\;'
SSI_PLUGIN_SOURCE_DIRECTORY = "source\\%s"
SSI_PLUGIN_INCLUDE_DIRECTORY = "include\\%s"
#SSI_PLUGIN_SOURCE_DIRECTORY = "build\\%s"

def editItemGroup(rootnode):
  """
    <ItemGroup>
      <ClCompile Include="..\..\source\DummyTransformer1.cpp" />
      <ClCompile Include="..\..\source\ExportDummyTransformer1.cpp" />
    </ItemGroup>
    <ItemGroup>
      <ClInclude Include="..\..\include\DummyTransformer1.h" />
      <ClInclude Include="..\..\include\ssidummytransformer1.h" />
    </ItemGroup>
  """
    maincppfile_name = (SSI_CURRENT_PLUGIN_PREFIX % SSI_PLUGIN_SOURCE_DIRECTORY) % (SSI_PLUGIN_NAME + ".cpp")
    exportcppfile_name = (SSI_CURRENT_PLUGIN_PREFIX % SSI_PLUGIN_SOURCE_DIRECTORY) % ("Export" + SSI_PLUGIN_NAME + ".cpp")
    
    mainheaderfile_name = (SSI_CURRENT_PLUGIN_PREFIX % SSI_PLUGIN_INCLUDE_DIRECTORY) % (SSI_PLUGIN_NAME + ".h")
    ssiheaderfile_name = (SSI_CURRENT_PLUGIN_PREFIX % SSI_PLUGIN_INCLUDE_DIRECTORY) % ("ssi" + SSI_PLUGIN_NAME.lower() + ".h")
  """
    cppfilesGroup = createNewElement(rootnode, "ItemGroup")
    findChild(cppfilesGroup, "ClCompile").set("Include", maincppfile_name)
    findChild(cppfilesGroup, "ClCompile").set("Include", exportcppfile_name)
    
    headerfilesGroup = createNewElement(rootnode, "ItemGroup")
    findChild(headerfilesGroup, "ClCompile").set("Include", mainheaderfile_name)
    findChild(headerfilesGroup, "ClCompile").set("Include", ssiheaderfile_name)
  """
  files_names = (maincppfile_name, exportcppfile_name, mainheaderfile_name, ssiheaderfile_name)
  for file_name in files_names:
    if not lexists(file_name):
      with open(file_name, 'w') as outfile:
        outfile.write("")
        outfile.flush()
  pass

def writetree(tree, inputfile):
  treecontent = ET.tostring(tree.getroot()).replace("ns0:", "").replace(":ns0", "")
  if not OVERRIDE_OPTION:
    inputfile = inputfile + ".xml"
  with open(inputfile , 'w') as out_file:
    out_file.write(treecontent)
    out_file.flush()
  #tree.write(INPUT_FILE + ".xml")
  pass
def createNewElement(parentnode, newelement_name):
  newelement = ET.SubElement(parentnode, newelement_name)
  return newelement
  pass
def findChild(parentnode, childnode_name):
  if parentnode.find(XML_TAG_SUFFIX % childnode_name) is None:
    createNewElement(parentnode, childnode_name)
  return parentnode.find(XML_TAG_SUFFIX % childnode_name)
  pass
def editDebugProperties(properties_node):
  findChild(properties_node, "TargetName").text = "ssi$(ProjectName)d"
  findChild(properties_node, "OutDir").text =  SSI_DIR_PREFIX % SSI_BIN_DIRECTORY
  pass
def editReleaseProperties(properties_node):
  
  findChild(properties_node, "OutDir")
  findChild(properties_node, "TargetName").text = "ssi$(ProjectName)"
  findChild(properties_node, "OutDir").text =  SSI_DIR_PREFIX % SSI_BIN_DIRECTORY
  pass
def editReleaseLink(link_node):
  findChild(link_node, "AdditionalLibraryDirectories").text = (SSI_DIR_PREFIX % SSI_LIB_DIRECTORY) + (SSI_DIR_PREFIX % SSI_BIN_DIRECTORY)
  findChild(link_node, "AdditionalDependencies").text = ""
  findChild(link_node, "OutputFile").text = "$(TargetPath)"
  
  pass
def editReleaseClCompile(clcompile_node):
  findChild(clcompile_node, "AdditionalIncludeDirectories").text = (SSI_DIR_PREFIX % SSI_INCLUDE_DIRECTORY)
  pass
def editDebugClCompile(clcompile_node):
  findChild(clcompile_node, "AdditionalIncludeDirectories").text = (SSI_DIR_PREFIX % SSI_INCLUDE_DIRECTORY)
  pass
def editDebugLink(link_node):
  findChild(link_node, "AdditionalLibraryDirectories").text = (SSI_DIR_PREFIX % SSI_LIB_DIRECTORY) + (SSI_DIR_PREFIX % SSI_BIN_DIRECTORY)
  findChild(link_node, "AdditionalDependencies").text = ""
  findChild(link_node, "OutputFile").text = "$(TargetPath)"
  pass

def initialize():
  global SSI_DIR_PREFIX
  global SSI_CURRENT_PLUGIN_PREFIX
  global SSI_PLUGIN_NAME
  current_dir = abspath('')
  new_dir = SSI_DIR_PREFIX
  current_plugin_dir = SSI_CURRENT_PLUGIN_PREFIX
  dir_files = listdir(current_dir)
  while current_dir[-3:] != "ssi":
    current_dir = dirname(current_dir)
    new_dir =  '..\\'  + new_dir
    
    if not (dir_files.count("include") == 1 and dir_files.count("source") == 1 and dir_files.count("build") == 1):
      current_plugin_dir = '..\\'  + current_plugin_dir
      dir_files = listdir(current_dir)
      print "- ", dir_files
  SSI_DIR_PREFIX = new_dir
  SSI_CURRENT_PLUGIN_PREFIX = current_plugin_dir
  print "- ", INPUT_FILE, "- ", INPUT_FILE.rfind(".vcxproj")
  SSI_PLUGIN_NAME = INPUT_FILE[0:INPUT_FILE.rfind(".vcxproj")]
  
  
def main():
  global XML_TAG_SUFFIX
  tree = ET.parse(INPUT_FILE)
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
  editItemGroup(root)
  #print '- ', ET.tostringlist(root)
  writetree(tree, INPUT_FILE)
if __name__ == "__main__":
  initialize()
  main()