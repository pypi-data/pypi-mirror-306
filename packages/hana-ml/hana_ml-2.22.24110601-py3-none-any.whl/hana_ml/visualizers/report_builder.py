"""
This module represents the whole report builder.
A report can contain many pages, and each page can contain many items.
You can assemble different items into different pages.

The following classes are available:
    * :class:`ReportBuilder`
    * :class:`Page`
    * :class:`ChartItem`
    * :class:`TableItem`
    * :class:`DescriptionItem`
    * :class:`DigraphItem`
    * :class:`LocalImageItem`
    * :class:`RemoteImageItem`
    * :class:`ForcePlotItem`
    * :class:`AlertItem`
"""

# pylint: disable=invalid-name
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=no-member
# pylint: disable=too-few-public-methods
# pylint: disable=super-init-not-called
# pylint: disable=attribute-defined-outside-init
from typing import List
import base64
from urllib.parse import quote
from hana_ml.visualizers.shared import EmbeddedUI


class Item(object):
    def to_json(self):
        temp_json = {
            'title': self.title,
            'type': self.type,
            'config': self.config
        }
        if self.type == 'chart':
            if self.height is not None:
                temp_json['height'] = float(self.height)
            if self.width is not None:
                temp_json['width'] = float(self.width)
        return temp_json

class DescriptionItem(Item):
    """
    This item represents an description type, it contains multiple key and value values.

    Parameters
    ----------
    title : str
        The description item name.
    """
    def __init__(self, title: str):
        self.title: str = title
        self.type = 'description'
        self.config = []

    def add(self, key: str, value: str):
        """
        Add a key-value pair.

        Parameters
        ----------
        key : str
            The key of description item.

        value : str
            The value of description item.
        """
        if key is not None and value is not None:
            self.config.append({
                'name': key,
                'value': value
            })
        else:
            raise ValueError('Added key or value is none!')


class ChartItem(Item):
    """
    This item represents an chart type.

    Parameters
    ----------
    title : str
        The chart item name.

    config : json
        The chart item config.

    width : int, optional
        The chart's width.

    height : int, optional
        The chart's height.
    """
    def __init__(self, title: str, config, width=None, height=None):
        self.title: str = title
        self.type = 'chart'
        self.config = config
        self.width = width
        self.height = height


class TableItem(Item):
    """
    This item represents an table type.

    Parameters
    ----------
    title : str
        The table item name.
    """
    def __init__(self, title: str):
        self.title: str = title
        self.type = 'table'
        self.config = {
            'columns': [],
            'data': {}
        }
        self.data_count = -1

    def addColumn(self, name: str, data: List):
        """
        Add a dataset of single column.

        Parameters
        ----------
        name : str
            The column name of the single dataset.

        data : List
            The single dataset.
        """
        if name and data:
            if self.data_count == -1:
                self.data_count = len(data)
            elif len(data) != self.data_count:
                raise ValueError('Added data length is incorrect!')
            self.config['columns'].append(name)
            self.config['data'][name] = data
        else:
            raise ValueError('Added name or data is none!')


class RemoteImageItem(Item):
    """
    This item represents an remote image type.

    Parameters
    ----------
    title : str
        The image item name.

    url : str
        The image address.

    width : int, optional
        The image width.

        Default to original width of image.

    height : int, optional
        The image height.

        Default to original height of image.
    """
    def __init__(self, title: str, url: str, width: int = None, height: int = None):
        if title is None or url is None:
            raise ValueError('The title or url is none!')

        self.title: str = title
        self.type = 'image'
        self.config = {
            'url': url
        }

        if width:
            self.config['width'] = width
        if height:
            self.config['height'] = height


class LocalImageItem(Item):
    """
    This item represents an local image type.

    Parameters
    ----------
    title : str
        The image item name.

    file_path : str
        The image file path.

    width : int, optional
        The image width.

        Default to original width of image.

    height : int, optional
        The image height.

        Default to original height of image.
    """
    def __init__(self, title: str, file_path: str, width: int = None, height: int = None):
        if title is None or file_path is None:
            raise ValueError('The title or file path is none!')
        file = open(file_path, 'rb')
        imageContent = file.read()
        file.close()
        self.title: str = title
        self.type = 'image'
        base64_data = base64.b64encode(imageContent)
        image_str = "data:{mime_type};base64,{image_data}".format(mime_type="image/png", image_data=quote(base64_data))

        self.config = {
            'content': image_str
        }

        if width:
            self.config['width'] = width
        if height:
            self.config['height'] = height


class ForcePlotItem(Item):
    def __init__(self, title: str, config):
        self.title: str = title
        self.type = 'sp.force-plot'
        self.config = config


class DigraphItem(Item):
    def __init__(self, title: str, digraph):
        def escape(s):
            s = s.replace("&", "&amp;") # Must be done first!
            s = s.replace("<", "&lt;")
            s = s.replace(">", "&gt;")
            s = s.replace('"', "&quot;")
            s = s.replace('\'', "&quot;")
            return s
        self.title: str = title
        self.type = 'sp.digraph'
        self.config: str = escape(digraph.embedded_unescape_html)


class AlertItem(Item):
    """
    This item represents an alert type.
    There are four styles to describe message arrays: success, info, warning, error.

    Parameters
    ----------
    title : str
        The chart item name.
    """
    def __init__(self, title: str):
        self.title: str = title
        self.type = 'alert'
        self.config = []

        self.success_msgs = []
        self.info_msgs = []
        self.warning_msgs = []
        self.error_msgs = []

    def to_json(self):
        if len(self.success_msgs) > 0:
            self.config.append({
                'type': 'success',
                'msgs': self.success_msgs
            })
        if len(self.info_msgs) > 0:
            self.config.append({
                'type': 'info',
                'msgs': self.info_msgs
            })
        if len(self.warning_msgs) > 0:
            self.config.append({
                'type': 'warning',
                'msgs': self.warning_msgs
            })
        if len(self.error_msgs) > 0:
            self.config.append({
                'type': 'error',
                'msgs': self.error_msgs
            })
        return {
            'title': self.title,
            'type': self.type,
            'config': self.config
        }

    @staticmethod
    def check_msg(msg: str):
        if msg is not None:
            msg = msg.strip()
            if msg != '':
                return msg
        raise ValueError('Added message is none!')

    def add_success_msg(self, msg: str):
        """
        Add a successful message.

        Parameters
        ----------
        msg : str
            Message content.
        """
        msg = AlertItem.check_msg(msg)
        self.success_msgs.append(msg)

    def add_info_msg(self, msg: str):
        """
        Add a informational message.

        Parameters
        ----------
        msg : str
            Message content.
        """
        msg = AlertItem.check_msg(msg)
        self.info_msgs.append(msg)

    def add_warning_msg(self, msg: str):
        """
        Add a warning message.

        Parameters
        ----------
        msg : str
            Message content.
        """
        msg = AlertItem.check_msg(msg)
        self.warning_msgs.append(msg)

    def add_error_msg(self, msg: str):
        """
        Add a error message.

        Parameters
        ----------
        msg : str
            Message content.
        """
        msg = AlertItem.check_msg(msg)
        self.error_msgs.append(msg)


class Page(object):
    """
    Every report consists of many pages. Each page contains multiple items.

    Parameters
    ----------
    title : str
        The page name.
    """
    def __init__(self, title: str):
        self.title: str = title
        self.items: List[Item] = []

    def addItem(self, item: Item):
        """
        Add a item instance to page instance.

        Parameters
        ----------
        item : Item
            Each page contains multiple items.
        """
        if item is not None:
            if item.config is not None:
                self.items.append(item.to_json())
        else:
            raise ValueError('Added item is none!')

    def addItems(self, items):
        """
        Add many item instances to page instance.

        Parameters
        ----------
        items : Item or List[Item]
            Each page contains multiple items.
        """
        if isinstance(items, (list, tuple)):
            if items and len(items) > 0:
                for item in items:
                    self.addItem(item)
            else:
                raise ValueError('Added items is none or no data items!')
        else:
            self.addItem(items)

    def to_json(self):
        """
        Return the config data of single page.
        This method is automatically called by the internal framework.
        """
        return {
            'title': self.title,
            'items': self.items
        }


class ReportBuilder(object):
    """
    This class is a report builder and the base class for report building. Can be inherited by custom report builder classes.

    Parameters
    ----------
    title : str
        The report name.
    """
    def __init__(self, title: str):
        self.title: str = title
        self.pages: List[Page] = []
        self.html_str = None

    def addPage(self, page: Page):
        """
        Add a page instance to report instance.

        Parameters
        ----------
        page : Page
            Every report consists of many pages.
        """
        if page:
            self.pages.append(page.to_json())
        else:
            raise ValueError('Added page is none!')

    def addPages(self, pages: List[Page]):
        """
        Add many page instances to report instance.

        Parameters
        ----------
        pages : List[Page]
            Every report consists of many pages.
        """
        if pages and len(pages) > 0:
            for page in pages:
                self.addPage(page)
        else:
            raise ValueError('Added pages is none or no data items!')

    def to_json(self):
        """
        Return the all config data of report.
        This method is automatically called by the internal framework.
        """
        return {
            'title': self.title,
            'pages': self.pages
        }

    def build(self, debug=False):
        """
        Build HTML string based on current config.

        Parameters
        ----------
        debug : bool
            Whether the log should be printed to the console.

            Defaults to False.
        """
        if debug is False:
            debug = 'false'
        else:
            debug = 'true'
        self.html_str = EmbeddedUI.get_resource_template('report_builder.html').render(debug=debug, reportConfig=self.to_json())

    def generate_html(self, filename):
        """
        Save the report as a html file.

        Parameters
        ----------
        filename : str
            HTML file name.
        """
        if self.html_str is None:
            self.build()
        EmbeddedUI.generate_file('{}_report.html'.format(filename), self.html_str)

    def generate_notebook_iframe(self, iframe_height=600):
        """
        Render the report as a notebook iframe.

        Parameters
        ----------
        iframe_height : int
            iframe height.

            Defaults to 600.
        """
        if self.html_str is None:
            self.build()
        ifrme_str = EmbeddedUI.get_iframe_str(self.html_str, iframe_height=iframe_height)
        EmbeddedUI.render_html_str(ifrme_str)

    def getHTMLText(self):
        if self.html_str is None:
            self.build()
        return self.html_str

    def getIframeHTMLText(self, iframe_height=600):
        if self.html_str is None:
            self.build()
        ifrme_str = EmbeddedUI.get_iframe_str(self.html_str, iframe_height=iframe_height)
        return ifrme_str
