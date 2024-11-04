'''
This module is used to read the project settings file that
configures how cadorchestrator builds a project and the interface
for the configuration server.
'''

import os
import yaml

class Settings():
    """
    This class reads the `cadorchestration.yml` file and provides
    access to the information inside it.
    """

    def __init__(self):
        if os.path.exists("cadorchestration.yml"):
            with open("cadorchestration.yml", "r", encoding="utf-8") as stream:
                self._data = yaml.safe_load(stream)
        else:
            raise RuntimeError("No cadorchestration.yml file found")

    @property
    def configuration_function(self):
        """
        Returns the name of the Python function this project uses for
        configuration of their hardware system. This function should
        have 1 input (the configuration json) and one output an
        cadorchestrator.components.Assembly object

        If no function is set in the configuration file then `None`
        will be returned.
        """

        if 'configuration-function' in self._data:
            return self._data['configuration-function']
        return None

    @property
    def configuration_options(self):
        """
        Returns the filename of the json file that describes the
        configuration options that can be specified.

        If not set in the configuration file then `None`
        will be returned.
        """
        if 'configuration-options' in self._data:
            return self._data['configuration-options']
        return None

    @property
    def css_file(self):
        """
        Returns the filename of the css file used for custom
        styling of the configuration server UI.

        If not set in the configuration file then `None`
        will be returned.
        """
        if 'css-file' in self._data:
            return self._data['css-file']
        return None

    @property
    def site_title(self):
        """
        Returns the title to be used in the configuration server UI.

        If not set in the configuration file then the default title
        `CadOrchestrator Configuratator` will be returned.
        """
        if 'site-title' in self._data:
            return self._data['site-title']
        return "CadOrchestrator Configuratator"

    @property
    def site_tagline(self):
        """
        Returns the tagline to be used in the configuration server UI.

        If not set in the configuration file then the default tagline is `Configure your hardware:`
        will be returned.
        """
        if 'site-tagline' in self._data:
            return self._data['site-tagline']
        return "Configure your hardware:"

    @property
    def site_logo(self):
        """
        Returns the filepath of the logo to be used in the configuration
        server UI.

        If not set in the configuration file then `None`
        will be returned.
        """
        if 'site-logo' in self._data:
            return self._data['site-logo']
        return None

    @property
    def site_favicon(self):
        """
        Returns the filepath of the favicon to be used for the configuration
        server.

        If not set in the configuration file then `None`
        will be returned.
        """
        if 'site-favicon' in self._data:
            return self._data['site-favicon']
        return None

    @property
    def assembly_model(self):
        """
        The model of the assembly to display
        """
        if 'assembly-model' in self._data:
            return self._data['assembly-model']
        return None
