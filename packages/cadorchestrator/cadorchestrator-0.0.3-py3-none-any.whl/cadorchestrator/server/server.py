"""
This module containts the configuration server code which
is a FastAPI app.
"""

import os
import re
import json

from pathlib import Path
import shutil

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse, ORJSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from cadorchestrator.generate import generate
from cadorchestrator.settings import Settings


SETTINGS = Settings()
app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for the test page
SERVER_DIR = os.path.join(os.path.dirname(__file__), "app")
STATIC_DIR = os.path.join(SERVER_DIR, "static")
ASSETS_DIR = os.path.join(SERVER_DIR, "assets")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")
os.makedirs("_cache_", exist_ok=True)
app.mount("/cache", StaticFiles(directory="_cache_", html = True), name="cache")

MODULE_PATH = Path(".").resolve()

# http://127.0.0.1:8000/
@app.get("/")
async def read_index():
    """
    Loads a sample page so that the system can be tested end-to-end.
    """

    return FileResponse(os.path.join(SERVER_DIR, "index.html"))

# http://127.0.0.1:8000/get-project-css
@app.get("/get-project-css")
async def get_project_css():
    """
    Returns the custom CSS set by the project
    """
    if SETTINGS.css_file:
        return FileResponse(SETTINGS.css_file)

    headers = {
        'Content-Disposition': 'attachment; filename="project.css"'
    }
    css = ''
    return StreamingResponse(css, headers=headers)

# http://127.0.0.1:8000/get-ui-data
@app.get("/get-ui-data")
async def get_ui_data():
    """
    Returns strings used in the server UI
    """
    return ORJSONResponse({"title": SETTINGS.site_title,
                           "tagline": SETTINGS.site_tagline})


# http://127.0.0.1:8000/favicon
@app.get("/favicon")
def favicon():
    """
    Returns the configuration server's favion
    """
    if SETTINGS.site_favicon:
        return FileResponse(SETTINGS.site_favicon)
    return FileResponse(os.path.join(STATIC_DIR, 'images', 'favicon.png'))

# http://127.0.0.1:8000/logo.png
@app.get("/logo")
def logo():
    """
    Returns the logo used in the configuration server's UI
    """
    print("hello")
    if SETTINGS.site_logo:
        return FileResponse(SETTINGS.site_logo)
    return FileResponse(os.path.join(STATIC_DIR, 'images', 'CadOrchestrator.png'))

def get_unique_name(config):
    """
    Allows the caller to get a unique name for a configuration.
    """

    # Concatenate all the component names together
    unique_name = "!".join(config)

    # Replace spaces with underscores
    unique_name = unique_name.replace(" ", "_")

    # Delete all non-alphanumeric characters (other than _)
    unique_name = re.sub(r'[^a-zA-Z0-9_!]', '', unique_name)

    return unique_name


# http://127.0.0.1:8000
@app.post("/orchestrate")
async def orchestrate(request: Request):
    """
    Allows the caller to request documentation to be generated for the
    specific configuration that they pass.
    """

    req = await request.json()
    config = req['config']

    # Make sure that a config was passed
    if len(config) == 0:
        print("Nothing to build")
        return ORJSONResponse({"error": "Configuration must have components in it."},
                              status_code=500)

    print("Starting build for config:")
    print(config)

    # Create a clean, unique name for this build
    unique_name = get_unique_name(config)

    # Trigger the generation of all materials, but only if they do not already exist

    if not os.path.exists(MODULE_PATH / "_cache_" / f"{unique_name}.zip"):
        # Call all the  generator code
        generate(config, SETTINGS)

        # Create the zip file
        shutil.make_archive(str(MODULE_PATH / "_cache_" / unique_name),
                            'zip',
                            os.path.join(MODULE_PATH, "build"))

        if SETTINGS.assembly_model:
            model_3d = os.path.join(str(MODULE_PATH / "build" ), SETTINGS.assembly_model)
            if os.path.exists(model_3d):
                ext_3d = os.path.splitext(model_3d)[1]
                # Make a copy of the glTF preview file to cache it
                shutil.copyfile(model_3d,
                                str(MODULE_PATH / "_cache_" / f"{unique_name}{ext_3d}"))

        # Make a cached copy of the assembly docs so that they can be served to the user
        shutil.copytree(str(MODULE_PATH / "build" / "assembly-docs"),
                        str(MODULE_PATH / "_cache_" / f"{unique_name}_assembly_docs"))

    # Check to make sure we have the _cache_ directory that holds the distribution files
    if not os.path.isdir(str(MODULE_PATH / "_cache_")):
        os.makedirs(str(MODULE_PATH / "_cache_"))

    # Let the client know where they can download the file
    return ORJSONResponse({"unique_name": unique_name})


# http://127.0.0.1:8000/get-config-options
@app.get("/get-config-options")
async def get_config_options():
    """
    Returns JSON data specifying the configuration options that should be
    presented to the user.
    """
    if not SETTINGS.configuration_options:
        return ORJSONResponse({"options": []})
    with open(SETTINGS.configuration_options, 'r', encoding='utf-8') as component_file:
        component_data = json.load(component_file)
    return ORJSONResponse(component_data)


@app.get("/generated-docs")
def get_files(config):
    """
    Loads any auto-generated documentation files.
    """

    # Figure out what the build path is
    build_path = MODULE_PATH  / "_cache_" / config

    # Once the build exists we can send it to the user, but before that we give
    # them a temporary redirect
    if os.path.exists(str(build_path) + ".zip"):
        hdr_dict = {'Content-Disposition': 'attachment; filename=' + config + ".zip"}
        return FileResponse(str(build_path) + ".zip",
                            headers=hdr_dict)

    return HTMLResponse(content="<p>The File is Still Processing</p>",
                        status_code=307)


@app.get("/preview")
def get_preview(config):
    """
    Sends a 3D file to the client for preview.
    """

    if SETTINGS.assembly_model:
        ext_3d = os.path.splitext(SETTINGS.assembly_model)[1]
        # Figure out what the build and model path is
        model_3d =  f"{config}{ext_3d}"
        model_3d_path = MODULE_PATH  / "_cache_" / model_3d

        # If the model exists, send it to the client
        if os.path.exists(model_3d_path):
            hdr_dict = {'Content-Disposition': 'attachment; filename=' + model_3d}
            return FileResponse(str(model_3d_path),
                                headers=hdr_dict)
    return HTMLResponse(content="<p>Preview is not available.</p>",
                        status_code=500)
