"""
This module contains related class for generating the best pipeline report.

The following class is available:

    * :class:`BestPipelineReport`
"""

# pylint: disable=missing-module-docstring
# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-function-args
# pylint: disable=too-many-instance-attributes
# pylint: disable=trailing-whitespace
# pylint: disable=protected-access
# pylint: disable=no-self-use
import json
from hana_ml.dataframe import DataFrame
from hana_ml.algorithms.pal.auto_ml import _PipelineWalk
from hana_ml.visualizers.digraph import MultiDigraph
from hana_ml.visualizers.shared import EmbeddedUI


def escape(s):
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    s = s.replace('"', "&quot;")
    s = s.replace('\'', "&quot;")
    return s


class BestPipelineReport(object):
    """
    The instance of this class can generate the best pipeline report.

    Parameters
    ----------
    automatic_obj : :class:`~hana_ml.algorithms.pal.auto_ml.AutomaticClassification` or :class:`~hana_ml.algorithms.pal.auto_ml.AutomaticRegression` or :class:`~hana_ml.algorithms.pal.auto_ml.AutomaticTimeSeries`
        An instance of the AutomaticClassification / AutomaticRegression / AutomaticTimeSeries Class.

    Examples
    --------

    Create an AutomaticClassification instance:

    >>> progress_id = "automl_{}".format(uuid.uuid1())
    >>> auto_c = AutomaticClassification(generations=2,
                                         population_size=5,
                                         offspring_size=5,
                                         progress_indicator_id=progress_id)

    Training:

    >>> auto_c.fit(data=df_train)

    Plot the best pipeline:

    >>> BestPipelineReport(auto_c).generate_notebook_iframe()

    .. image:: image/best_pipeline_classification.png

    """
    def __init__(self, automatic_obj):
        if hasattr(automatic_obj, "best_pipeline_"):
            best_pipeline_df: DataFrame = automatic_obj.best_pipeline_
        else:
            best_pipeline_df = automatic_obj.model_[1]
        self.automatic_obj = automatic_obj
        self.best_pipeline_pandas_df = best_pipeline_df.collect()
        best_pipelines_str = self.best_pipeline_pandas_df.to_json()
        escaped_pipeline_iframe_html = escape(self.__convert_to_digraph().embedded_unescape_html)

        connections_json_str = ''
        for key_value in automatic_obj.info_.collect().to_dict('records'):
            if key_value['STAT_NAME'] == 'optimal_connections':
                connections_json_str = key_value['STAT_VALUE']
                break
        self.html_str = EmbeddedUI.get_resource_template('best_pipeline_report.html').render(data_json=best_pipelines_str, pipeline_iframe_html=escaped_pipeline_iframe_html, highlighted_metric_name=self.automatic_obj._get_highlight_metric(), connections_json_str=connections_json_str)

    def __convert_to_digraph(self) -> MultiDigraph:
        multi_digraph: MultiDigraph = MultiDigraph('Pipelines', embedded_mode=True)
        pipelines = self.best_pipeline_pandas_df["PIPELINE"]
        for index in range(0, len(pipelines)):
            p_content = []
            p_args = []
            pipeline = json.loads(pipelines.iat[index])
            pipe = _PipelineWalk(pipeline)
            for i in range(1, 100):
                p_content.append(pipe.current_content)
                p_args.append(pipe.current_args)
                pipe._next()
                if pipe.end:
                    p_content.append(pipe.current_content)
                    p_args.append(pipe.current_args)
                    break
            p_content.reverse()
            p_args.reverse()
            count = 0
            nodes = []
            for p_1, p_2 in zip(p_content, p_args):
                nodes.append((str(p_1), str(p_2), [str(count)], [str(count + 1)]))
                count = count + 1
            digraph = multi_digraph.add_child_digraph('pipeline_{}'.format(index))
            node = []
            for elem in nodes:
                node.append(digraph.add_python_node(elem[0],
                                                    elem[1],
                                                    in_ports=elem[2],
                                                    out_ports=elem[3]))
            for node_x in range(0, len(node) - 1):
                digraph.add_edge(node[node_x].out_ports[0], node[node_x + 1].in_ports[0])
        multi_digraph.build()
        return multi_digraph

    def generate_notebook_iframe(self, iframe_height: int = 1000):
        """
        Renders the best pipeline report as a notebook iframe.

        Parameters
        ----------
        iframe_height : int, optional
            Frame height.

            Defaults to 1000.
        """
        iframe_id = EmbeddedUI.get_uuid()
        iframe_str = EmbeddedUI.get_iframe_str(self.html_str, iframe_id=iframe_id, iframe_height=iframe_height)
        self.automatic_obj.report = iframe_str
        EmbeddedUI.render_html_str(iframe_str)

    def generate_html(self, filename: str):
        """
        Saves the best pipeline report as a html file.

        Parameters
        ----------
        filename : str
            Html file name.
        """
        EmbeddedUI.generate_file("{}_best_pipeline_report.html".format(filename), self.html_str)
