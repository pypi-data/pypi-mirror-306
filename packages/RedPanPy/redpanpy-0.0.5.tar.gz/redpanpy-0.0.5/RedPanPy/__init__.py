# RedPanPy.py
import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QUrl, QObject, pyqtSlot
import importlib.resources

# Read the qwebchannel.js file

class CallHandler(QObject):
    """
    This class handles interactions with HTML elements.
    """
    def __init__(self):
        super().__init__()
        self.callbacks = {}

    @pyqtSlot(str, str)
    def call(self, element_id, event_type):
        key = (element_id, event_type)
        if key in self.callbacks:
            self.callbacks[key]()

    def register_callback(self, element_id, event_type, callback):
        key = (element_id, event_type)
        self.callbacks[key] = callback

class RedPanPyApp:
    def __init__(self, html_path, *args, **kwargs):
        title = kwargs.get('title', 'RedPanPy App')
        width = kwargs.get('width', 800)
        height = kwargs.get('height', 600)

        self.app = QApplication(sys.argv)
        self.window = QMainWindow()
        self.window.setWindowTitle(title)
        self.window.setGeometry(100, 100, width, height)
    
        # Create a web engine view and load the HTML file
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl.fromLocalFile(html_path))
        self.window.setCentralWidget(self.browser)
        
        # Create a QWebChannel and register the CallHandler
        self.channel = QWebChannel()
        self.handler = CallHandler()
        self.channel.registerObject('handler', self.handler)

        self.browser.page().setWebChannel(self.channel)
        
        # Inject JavaScript code after the page has finished loading
        self.browser.page().loadFinished.connect(self.register_binds)
        
        # Store binds and JavaScript commands to be registered after page load
        self.pending_binds = []
        self.pending_js = []
        self.page_loaded = False

    def register_binds(self):
        with importlib.resources.open_text("RedPanPy", "qwebchannel.js") as f:
            js_code = f.read()
        self.browser.page().runJavaScript(js_code)
        # Initialize the QWebChannel only once
        js_code = """
        if (typeof channelInitialized === 'undefined') {
            channelInitialized = true;
            new QWebChannel(qt.webChannelTransport, function(channel) {
                window.handler = channel.objects.handler;
            });
        }
        """
        self.browser.page().runJavaScript(js_code)

        # Bind pending events
        for bind_args in self.pending_binds:
            self._bind_js(*bind_args)
        self.pending_binds.clear()

        # Run pending JavaScript commands
        for js_code in self.pending_js:
            self.browser.page().runJavaScript(js_code)
        self.pending_js.clear()

        self.page_loaded = True

    def bind(self, element_id, event_type, callback):
        # Register the callback in CallHandler
        self.handler.register_callback(element_id, event_type, callback)
        # If the page has not loaded yet, store the bind to register later
        if self.page_loaded:
            self._bind_js(element_id, event_type)
        else:
            self.pending_binds.append((element_id, event_type))

    def _bind_js(self, element_id, event_type):
        # Add the event listener for the element
        js_code = f"""
        (function() {{
            var element = document.getElementById({json.dumps(element_id)});
            if (element) {{
                element.addEventListener({json.dumps(event_type)}, function() {{
                    handler.call({json.dumps(element_id)}, {json.dumps(event_type)});
                }});
            }}
        }})();
        """
        self.browser.page().runJavaScript(js_code)

    def set_element_text(self, element_id, text):
        """
        Sets the innerHTML of an HTML element by its ID.
        """
        js_code = f"""
        (function() {{
            var element = document.getElementById({json.dumps(element_id)});
            if (element) {{
                element.innerHTML = {json.dumps(text)};
            }}
        }})();
        """
        if self.page_loaded:
            self.browser.page().runJavaScript(js_code)
        else:
            self.pending_js.append(js_code)
    def set_element_value(self, element_id, value):
        """
        Sets the innerHTML of an HTML element by its ID.
        """
        js_code = f"""
        (function() {{
            var element = document.getElementById({json.dumps(element_id)});
            if (element) {{
                element.value = {json.dumps(value)};
            }}
        }})();
        """
        if self.page_loaded:
            self.browser.page().runJavaScript(js_code)
        else:
            self.pending_js.append(js_code)
    def get_element_value(self, element_id, callback):
        """
        Gets the value of an HTML input element by its ID.
        """
        js_code = f"""
        (function() {{
            var element = document.getElementById({json.dumps(element_id)});
            if (element) {{
                return element.value;
            }} else {{
                return null;
            }}
        }})();
        """
        self.browser.page().runJavaScript(js_code, callback)

    def get_element_text(self, element_id, callback):
        """
        Gets the innerHTML of an HTML element by its ID.
        Returns the text directly by blocking until the result is available.
        """
        js_code = f"""
        (function() {{
            var element = document.getElementById({json.dumps(element_id)});
            if (element) {{
                return element.innerHTML;
            }} else {{
                return null;
            }}
        }})();
        """
        self.browser.page().runJavaScript(js_code, callback)
    def run(self):
        self.window.show()
        sys.exit(self.app.exec_())