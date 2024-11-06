import re
import threading
import os
import io
import zipfile
from subprocess import Popen, CREATE_NEW_CONSOLE
import subprocess
import xml.etree.ElementTree as ET

def getCustomCode(text,tag):
    pattern = r"#<!-- cc_"+tag+" START--!>(.*?)#<!-- cc_"+tag+" END--!>"
    matches = re.findall(pattern, text, re.DOTALL)
    return matches if matches else None

def replaceCustomCode(text,tag,replacement):
    pattern = r"#<!-- cc_"+tag+" START--!>(.*?)#<!-- cc_"+tag+" END--!>"
    start_tag = "#<!-- cc_"+tag+" START--!>"
    end_tag = "#<!-- cc_" + tag + " END--!>"
    return re.sub(pattern,start_tag+replacement[0]+end_tag,text,flags=re.DOTALL)


#----------------------------------------------------------------------------------------------------------------------
#------------------------------------------------CLI FUNCTIONS---------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
def run_command(command):
    try:
        # result = subprocess.run(command[0][0], shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process = Popen(command[0], shell=True, cwd=command[1])
        stdout, stderr = process.communicate()
        print(process.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Command: {command}\nError: {e.stderr.decode('utf-8')}")


def execute_commands(commands):
    """
    Execute multiple command line functions concurrently.

    Parameters:
    commands (list of str): List of command line commands to execute.
    """
    threads = []
    for command in commands:
        thread = threading.Thread(target=run_command, args=(command,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

def extractCommands(launchDescription):
    commands = []
    for component in launchDescription.components:
        commands.append([component.cmd, component.path])
    return commands


#----------------------------------------------------------------------------------------------------------------------
#--------------------------------------------LAUNCH FILE FUNCTIONS-----------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------

# Example usage
xml_string = """
<launch>
    <node name="monitor" path="C:/Users/Bert/UAntwerpen/Documenten/00_UA/02_Projects/01_RoboSAPIENS/98_Sandbox/Redis/pythonProject/PyLauncher/monitor"/>
    <node name="analysis" path="C:/Users/Bert/UAntwerpen/Documenten/00_UA/02_Projects/01_RoboSAPIENS/98_Sandbox/Redis/pythonProject/PyLauncher/analysis"/>
</launch>
"""

class Component:
    def __init__(self, name, path,formalism):
        self.name = name
        self.path = path
        if formalism == 'python':
            self.cmd= ['python', name+'.py']
        if formalism == 'c++':
            self.cmd = [path+'/'+name+'.exe']

    def __repr__(self):
        return f"Swc(name='{self.name}', cmd='{self.cmd}')"

class Launch:
    def __init__(self, nodes):
        self.components = nodes

    def __repr__(self):
        return f"Launch(components={self.components})"
def parse_launch_xml(file,formalism="python"):
    with open(file, 'r') as f:
        data = f.read()
        root = ET.fromstring(data)
        components = []
        for node_elem in root.findall('node'):
            name = node_elem.get('name')
            path = node_elem.get('path')
            components.append(Component(name, path,formalism))
        return Launch(components)


#----------------------------------------------------------------------------------------------------------------------
#-------------------------------------------FILE HANDLING FUNCTIONS----------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
def decompress_folder(data, output_path):
    # Decompress the byte stream into the output folder
    with zipfile.ZipFile(io.BytesIO(data), 'r') as zip_file:
        zip_file.extractall(output_path)
    print(f"Folder decompressed to '{output_path}'.")

def compress_folder(folder_path):
    # Compress the folder into a byte stream
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, os.path.relpath(file_path, folder_path))
    zip_buffer.seek(0)
    return zip_buffer.read()