'''
This module holds the code for generating complete documentation
from a given input configuration
'''

import os
import sys
import shutil
import subprocess
from importlib import import_module

import exsource_tools
import exsource_tools.cli
import exsource_tools.tools

from exsource_tools.exsource import ExSource

BUILD_DIR = "build"
DOCS_DIR = "documentation"
DOCS_TMP_DIR = "_gb_temp_"

def generate(config_str, settings):
    """
    Generate everything for a given configuration including, STL files,
    renders of assembly steps, and assembly documentation.
    """

    if settings.configuration_function:
        sys.path.insert(0, os.path.abspath('.'))
        module = import_module(settings.configuration_function['module'])
        conf_function = getattr(module, settings.configuration_function['function'])
        main_assembly = conf_function(config_str)
    else:
        raise RuntimeError("No configuration function set.")

    print("Starting Orchestration")
    components = main_assembly.all_components_and_assemblies

    print("Generating components")
    generate_components(components)

    print("Generating documentation")
    generate_docs(components)


def generate_components(components):
    """
    Generate all components (and renders)
    """
    if not os.path.exists(BUILD_DIR):
        os.makedirs(BUILD_DIR)

    exsource_path = os.path.join(BUILD_DIR, "exsource-def.yaml")
    component_dicts = {}

    for component in components:
        component_dicts.update(component.as_exsource_dict)
        #for each generated component write paramter file if needed.
        component.write_parameter_file(BUILD_DIR)

        for render in component.renders:
            component_dicts.update(render.as_exsource_dict)

    #loade into ExSource object to validate before saving
    exsource_obj = ExSource({'exports':component_dicts})

    exsource_obj.save(exsource_path)
    _run_exsource(exsource_path)


def generate_docs(components):
    """
    Run GitBuilding to generate documentation
    """
    if os.path.exists(DOCS_TMP_DIR):
        shutil.rmtree(DOCS_TMP_DIR)
    shutil.copytree(DOCS_DIR, DOCS_TMP_DIR)

    for component in components:
        #skip components without documentation
        if not (md := component.documentation):
            print(f"Skipping {component.key}: no docs")
            continue
        print(f"Generating docs for {component.key}")
        filename = component.documentation_filename
        filepath = os.path.join(DOCS_TMP_DIR, filename)
        with open(filepath, 'w', encoding="utf-8") as gb_file:
            gb_file.write(md)

    _run_gitbuilding()


def _run_gitbuilding():
    cur_dir = os.getcwd()
    os.chdir(DOCS_TMP_DIR)
    subprocess.run(
        ['gitbuilding', 'build-html'],
        check=True,
        capture_output=True
    )
    os.chdir(cur_dir)
    tmp_built_docs = os.path.join(DOCS_TMP_DIR, "_site")
    built_docs = os.path.join(BUILD_DIR, "assembly-docs")
    if os.path.exists(built_docs):
        shutil.rmtree(built_docs)
    shutil.copytree(tmp_built_docs, built_docs)


def _run_exsource(exsource_path):

    cur_dir = os.getcwd()
    # change into self._build_dir
    exsource_dir, exsource_filename = os.path.split(exsource_path)
    os.chdir(exsource_dir)

    headless = os.environ.get('DISPLAY') is None

    # run exsource-make
    exsource_def = exsource_tools.cli.load_exsource_file(exsource_filename)
    processor = exsource_tools.tools.ExSourceProcessor(exsource_def, headless=headless)
    processor.make()
    os.chdir(cur_dir)
