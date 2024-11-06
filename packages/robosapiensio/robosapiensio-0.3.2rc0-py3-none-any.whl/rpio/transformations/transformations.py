#**********************************************************************************
# * Copyright (C) 2024-present Bert Van Acker (B.MKR) <bert.vanacker@uantwerpen.be>
# *
# * This file is part of the roboarch R&D project.
# *
# * RAP R&D concepts can not be copied and/or distributed without the express
# * permission of Bert Van Acker
# **********************************************************************************
from os import mkdir
from os.path import exists, dirname, join, isfile
import jinja2
from rpio.utils.auxiliary import *

#-----------------------------------------------------------------------------------
#-----------------------------------AUXILIARY---------------------------------------
#-----------------------------------------------------------------------------------
def _AddRequirementsFile(file="requirements.txt", path=None):
    """Function to add a requirement.txt to the provided path."""

    # --- open file ---
    f = open(path + "/" + file, "a")

    # --- custom file content ---
    f.write("rpio==0.1.0\n")
    f.write("jsonpickle==3.3.0\n")
    f.write("paho-mqtt==2.1.0\n")
    f.write("PyYAML==6.0.2\n")


    # --- close file ---
    f.close()

def _AddDockerFile(file="Dockerfile",cmpName="", path=None):
    """Function to add a requirement.txt to the provided path."""

    # --- open file ---
    f = open(path + "/" + file, "a")

    # --- custom file content ---
    f.write("FROM python:3.10\n")
    f.write("ENV PYTHONUNBUFFERED 1\n")
    f.write("\n")
    f.write("ADD . c:/src/app\n")
    f.write("WORKDIR c:/src/app\n")
    f.write("ENV PYTHONPATH c:/src/app:$PYTHONPATH\n")
    f.write("\n")
    f.write("COPY requirements.txt ./\n")
    f.write("RUN pip3 install --no-cache-dir -r requirements.txt\n")
    f.write("\n")
    f.write("COPY config.yaml ./\n")
    f.write("COPY messages.py ./\n")
    f.write("COPY . .\n")
    f.write("\n")
    f.write('CMD ["python3", "'+cmpName+'.py"]\n')
    f.write("\n")

    # --- close file ---
    f.close()


#-----------------------------------------------------------------------------------
#--------------------------------TRANSFORMATIONS------------------------------------
#-----------------------------------------------------------------------------------
def swc2code_py(system=None,path="output/generated"):
    """Function to generate python code from the system modeled within the AADL Intermediate Language

    :param [system]: [Adaptive system model within aadlil], defaults to [None]
    :type [system]: [system (aadlil)](, optional)

    :param [path]: [Adaptive system model within aadlil], defaults to ["output/generated/messages"]
    :type [path]: [string](, optional)
    ...
    :return: [Functions returns nothing]
    :rtype: [None]
    """


    if not exists(path):
        mkdir(path)

    # Initialize the Templates engine.
    this_folder = dirname(__file__)
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(this_folder), trim_blocks=True, lstrip_blocks=True)

    # Load the template
    template = jinja_env.get_template('templates/swc_py.template')
    templateConfig = jinja_env.get_template('templates/swc_config.template')
    templateMessages = jinja_env.get_template('templates/messages_py.template')


    # Extract all processes from AADL system model
    managingSystem = system.systems[0]
    for process in managingSystem.processes:

        # 0. Generate folder for each AADL process
        swcFolder = path + "/" + process.name
        if not exists(swcFolder):
            mkdir(swcFolder)

        #1. Check if SWC file exists
        swcExists = isfile(join(swcFolder, process.name+".py"))

        #2. If swc exists, store custom code added by the user
        if swcExists:
            with open(join(swcFolder, process.name+".py"), "r") as swcFile:
                content = swcFile.read()
                cc_include = getCustomCode(text=content,tag="include")
                cc_code = getCustomCode(text=content, tag="code")
                cc_init = getCustomCode(text=content, tag="init")
                cc_thread_code = []
                for thread in process.threads:
                    _cc_code = getCustomCode(text=content, tag="code_"+thread.name)
                    cc_thread_code.append(_cc_code)

        # 2. Generate code from AADL processes
        with open(join(swcFolder, process.name+".py"), 'w') as f:
            f.write(template.render(swc=process))

        # 3. If swc exists, replace custom code in generated template
        if swcExists:
            with open(join(swcFolder, process.name+".py"), "r") as swcFile:
                content = swcFile.read()
                content = replaceCustomCode(content,tag="include",replacement=cc_include)
                content = replaceCustomCode(content, tag="code", replacement=cc_code)
                content = replaceCustomCode(content, tag="init", replacement=cc_init)
                for i in range(0,len(process.threads),1):
                    content = replaceCustomCode(content, tag="code_"+process.threads[i].name, replacement=cc_thread_code[i])

            with open(join(swcFolder, process.name + ".py"), "w") as swcFile:
                swcFile.write(content)



        # 4. Generate config.yaml file from AADL processes
        with open(join(swcFolder, "config.yaml"), 'w') as f:
            f.write(templateConfig.render(swc=process))

        # 5. Generate messages for standalone components
        with open(join(swcFolder, "messages.py"), 'w') as f:
            f.write(templateMessages.render(messages=system.messages))

        # 6. Add requirements.txt if swc does not exist
        if not swcExists:
            _AddRequirementsFile(path=swcFolder)

        # 7. Add Docker file if swc does not exist
        if not swcExists:
            _AddDockerFile(cmpName=process.name, path=swcFolder)

def message2code_py(system=None,path="output/generated/messages"):
    """Function to generate python code from messages modeled within the AADL Intermediate Language

    :param [system]: [Adaptive system model within aadlil], defaults to [None]
    :type [system]: [system (aadlil)](, optional)

    :param [path]: [Adaptive system model within aadlil], defaults to ["output/generated/messages"]
    :type [path]: [string](, optional)

    ...
    :return: [Functions returns nothing]
    :rtype: [None]
    """

    if not exists(path):
        mkdir(path)

    # Initialize the Templates engine.
    this_folder = dirname(__file__)
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(this_folder), trim_blocks=True, lstrip_blocks=True)

    # Load the template
    template = jinja_env.get_template('templates/messages_py.template')

    # Extract all processes from AADL system model
    with open(join(path, "messages.py"), 'w') as f:
        f.write(template.render(messages=system.messages))





