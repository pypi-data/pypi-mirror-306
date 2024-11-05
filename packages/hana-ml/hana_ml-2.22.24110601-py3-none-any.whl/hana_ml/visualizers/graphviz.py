"""
This module contains related class for generating the graphviz graph.

The following class is available:

    * :class:`Graphviz`
"""

# pylint: disable=missing-module-docstring
# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-function-args
# pylint: disable=too-many-instance-attributes
# pylint: disable=trailing-whitespace
# pylint: disable=protected-access
# pylint: disable=no-self-use
from hana_ml.visualizers.shared import EmbeddedUI


# https://www.graphviz.org/
class Graphviz(EmbeddedUI):
    def __init__(self, graphviz_str):
        super().__init__()
        if graphviz_str is None or graphviz_str == '':
            raise ValueError('No value was passed to the graphviz_str parameter!')
        self.html_str = self.get_resource_template('graphviz.html').render(graphviz_str=graphviz_str.replace('\n', '').replace('\r\n', ''))

    def generate_notebook_iframe(self, iframe_height: int = 1000):
        """
        Renders the graphviz graph as a notebook iframe.

        Parameters
        ----------
        iframe_height : int, optional
            Frame height.

            Defaults to 1000.
        """
        iframe_str = self.get_iframe_str(self.html_str, iframe_height=iframe_height)
        self.render_html_str(iframe_str)

    def generate_html(self, filename: str):
        """
        Saves the graphviz graph as a html file.

        Parameters
        ----------
        filename : str
            Html file name.
        """
        self.generate_file("{}_graphviz.html".format(filename), self.html_str)
