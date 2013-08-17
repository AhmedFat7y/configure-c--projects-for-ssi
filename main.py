import xml.etree.ElementTree as ET
from os.path import isfile, join, abspath, dirname, lexists
from os import listdir
from sys import argv
import argparse
import pdb, getopt

class ProjectConfigurator:
  #SSI_PLUGIN_SOURCE_DIRECTORY = "build\\%s"
  def __init__(self, argv):
    self.XML_TAG_SUFFIX = "%s"
    self.INPUT_FILE = ""
    self.SSI_PLUGIN_NAME = ""
    self.SSI_DIR_PREFIX = "%s"
    self.SSI_CURRENT_PLUGIN_PREFIX = '%s'
    self.SSI_INCLUDE_DIRECTORY = 'core\\include\\;'
    self.SSI_LIB_DIRECTORY = 'libs\\Win32\\vc10\\;'
    self.SSI_BIN_DIRECTORY = 'bin\\Win32\\vc10\\;'
    self.SSI_PLUGINS_DIRECTORY = 'plugins\\'
    self.SSI_PLUGINS_INCLUDE_DIRECTORY = 'plugins\\%s\\include\\;'
    self.SSI_PLUGIN_SOURCE_DIRECTORY = "source\\%s"
    self.SSI_PLUGIN_INCLUDE_DIRECTORY = "include\\%s"
    self.parseCommandLineOptions()
    self.initializeRelativePaths()

  def parseCommandLineOptions(self):
    parser = argparse.ArgumentParser(description='Configure c++ project for ssi framework.')
    parser.add_argument('iFile', metavar='input-file',
                       help='The project file to be edited.')
    parser.add_argument('-p', '--inlculde-plugins', nargs="*", dest="included_plugins",
                       help='Name of plugins to add their include folders to the current project')
    parser.add_argument('-l', '--additional-deps', nargs="*", dest="additional_dependencies",
                       help='Additional dependencies (ex: xsens.lib)')
    parser.add_argument('-d', '--additional-libs-dirs', nargs="*", dest="additional_libs_directries",
                       help='Starting with a plugin name specify the folder to additiona libraries directories (ex: xsens\\build\\bin\\)')
    args = parser.parse_args()
    self.INPUT_FILE = args.iFile
    
    #pdb._trace()
  def editItemGroup(self, rootnode):
    maincppfile_name = (self.SSI_CURRENT_PLUGIN_PREFIX % self.SSI_PLUGIN_SOURCE_DIRECTORY) % (self.SSI_PLUGIN_NAME + ".cpp")
    exportcppfile_name = (self.SSI_CURRENT_PLUGIN_PREFIX % self.SSI_PLUGIN_SOURCE_DIRECTORY) % ("Export" + self.SSI_PLUGIN_NAME + ".cpp")
    
    mainheaderfile_name = (self.SSI_CURRENT_PLUGIN_PREFIX % self.SSI_PLUGIN_INCLUDE_DIRECTORY) % (self.SSI_PLUGIN_NAME + ".h")
    ssiheaderfile_name = (self.SSI_CURRENT_PLUGIN_PREFIX % self.SSI_PLUGIN_INCLUDE_DIRECTORY) % ("ssi" + self.SSI_PLUGIN_NAME.lower() + ".h")
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

  def writetree(self, tree, inputfile):
    treecontent = ET.tostring(tree.getroot()).replace("ns0:", "").replace(":ns0", "")
    with open(inputfile , 'w') as out_file:
      out_file.write(treecontent)
      out_file.flush()
    #tree.write(INPUT_FILE + ".xml")
    pass
  def createNewElement(self, parentnode, newelement_name):
    newelement = ET.SubElement(parentnode, self.XML_TAG_SUFFIX % newelement_name)
    return newelement
    pass
    
  def findChild(self, parentnode, childnode_name):
    if parentnode.find(self.XML_TAG_SUFFIX % childnode_name) is None:
      self.createNewElement(parentnode, childnode_name)
    return parentnode.find(self.XML_TAG_SUFFIX % childnode_name)
    pass
    
  def editDebugProperties(self, properties_node):
    #pdb.set_trace()
    self.findChild(properties_node, "TargetName").text = "ssi$(ProjectName)d"
    self.findChild(properties_node, "OutDir").text =  self.SSI_DIR_PREFIX % self.SSI_BIN_DIRECTORY
    pass
  def editReleaseProperties(self, properties_node):
    
    self.findChild(properties_node, "OutDir")
    self.findChild(properties_node, "TargetName").text = "ssi$(ProjectName)"
    self.findChild(properties_node, "OutDir").text =  self.SSI_DIR_PREFIX % self.SSI_BIN_DIRECTORY
    pass
  def editReleaseLink(self, link_node):
    self.findChild(link_node, "AdditionalLibraryDirectories").text = (self.SSI_DIR_PREFIX % self.SSI_LIB_DIRECTORY) + (self.SSI_DIR_PREFIX % self.SSI_BIN_DIRECTORY)
    self.findChild(link_node, "AdditionalDependencies").text = ""
    self.findChild(link_node, "OutputFile").text = "$(TargetPath)"
    
    pass
  def editReleaseClCompile(self, clcompile_node):
    self.findChild(clcompile_node, "AdditionalIncludeDirectories").text = (self.SSI_DIR_PREFIX % self.SSI_INCLUDE_DIRECTORY) + (self.SSI_CURRENT_PLUGIN_PREFIX % (self.SSI_PLUGIN_INCLUDE_DIRECTORY % ""))
    pass
  def editDebugClCompile(self, clcompile_node):
    self.findChild(clcompile_node, "AdditionalIncludeDirectories").text = (self.SSI_DIR_PREFIX % self.SSI_INCLUDE_DIRECTORY) + (self.SSI_CURRENT_PLUGIN_PREFIX % (self.SSI_PLUGIN_INCLUDE_DIRECTORY % ""))
    pass
  def editDebugLink(self, link_node):
    self.findChild(link_node, "AdditionalLibraryDirectories").text = (self.SSI_DIR_PREFIX % self.SSI_LIB_DIRECTORY) + (self.SSI_DIR_PREFIX % self.SSI_BIN_DIRECTORY)
    self.findChild(link_node, "AdditionalDependencies").text = ""
    self.findChild(link_node, "OutputFile").text = "$(TargetPath)"
    pass

  def initializeRelativePaths(self):
    current_dir = abspath('')
    new_dir = self.SSI_DIR_PREFIX
    current_plugin_dir = self.SSI_CURRENT_PLUGIN_PREFIX
    dir_files = listdir(current_dir)
    while current_dir[-3:] != "ssi":
      current_dir = dirname(current_dir)
      new_dir =  '..\\'  + new_dir
      
      if not (dir_files.count("include") == 1 and dir_files.count("source") == 1 and dir_files.count("build") == 1):
        current_plugin_dir = '..\\'  + current_plugin_dir
        dir_files = listdir(current_dir)
        print "- ", dir_files
    self.SSI_DIR_PREFIX = new_dir
    self.SSI_CURRENT_PLUGIN_PREFIX = current_plugin_dir
    print "- ", self.INPUT_FILE, "- ", self.INPUT_FILE.rfind(".vcxproj")
    self.SSI_PLUGIN_NAME = self.INPUT_FILE[0:self.INPUT_FILE.rfind(".vcxproj")]
  
  
  def start(self):
    tree = ET.parse(self.INPUT_FILE)
    root = tree.getroot()
    roottag = root.tag
    self.XML_TAG_SUFFIX = roottag[roottag.find("{") : roottag.find("}") + 1] + self.XML_TAG_SUFFIX
    for child in root:
      if child.tag == self.XML_TAG_SUFFIX % "PropertyGroup" and not child.attrib.has_key("Label") and child.attrib.has_key("Condition"):
        if child.attrib["Condition"] == "'$(Configuration)|$(Platform)'=='Debug|Win32'":
          self.editDebugProperties(child)
        elif child.attrib["Condition"] == "'$(Configuration)|$(Platform)'=='Release|Win32'":
          self.editReleaseProperties(child)
        else:
          pass
      elif child.tag == self.XML_TAG_SUFFIX % "ItemDefinitionGroup" and child.attrib.has_key("Condition"):
        compile_child = child.find(self.XML_TAG_SUFFIX % "ClCompile")
        link_child = child.find(self.XML_TAG_SUFFIX % "Link")
        
        if child.attrib["Condition"] == "'$(Configuration)|$(Platform)'=='Release|Win32'":
          self.editReleaseClCompile(compile_child)
          self.editReleaseLink(link_child)
        else:
          self.editReleaseClCompile(compile_child)
          self.editDebugLink(link_child)
      else:
        pass
    self.editItemGroup(root)
    #print '- ', ET.tostringlist(root)
    self.writetree(tree, self.INPUT_FILE)

if __name__ == "__main__":
  instance = ProjectConfigurator(argv)
  instance.start()