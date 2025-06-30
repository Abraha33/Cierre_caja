import sys
import types
import inspect
import importlib
import importlib.util
import os

import pytest

def setup_dummy_kivy():
    # Minimal stub modules for kivy
    kivy = types.ModuleType('kivy')
    kivy.__path__ = []
    props = types.ModuleType('kivy.properties')
    class DummyProp:
        def __init__(self, *args, **kwargs):
            pass
    for name in ['StringProperty', 'ListProperty', 'ObjectProperty', 'NumericProperty']:
        setattr(props, name, DummyProp)
    kivy.properties = props
    lang = types.ModuleType('kivy.lang')
    lang.Builder = types.SimpleNamespace(load_string=lambda *a, **k: None)
    kivy.lang = lang
    sys.modules.setdefault('kivy', kivy)
    sys.modules.setdefault('kivy.properties', props)
    sys.modules.setdefault('kivy.lang', lang)

    uix_pkg = types.ModuleType('kivy.uix')
    uix_pkg.__path__ = []
    sys.modules.setdefault('kivy.uix', uix_pkg)

    boxlayout = types.ModuleType('kivy.uix.boxlayout')
    class BoxLayout:
        def __init__(self, *args, **kwargs):
            pass
        def add_widget(self, w):
            pass
    boxlayout.BoxLayout = BoxLayout
    sys.modules.setdefault('kivy.uix.boxlayout', boxlayout)

    scrollview = types.ModuleType('kivy.uix.scrollview')
    class ScrollView:
        pass
    scrollview.ScrollView = ScrollView
    sys.modules.setdefault('kivy.uix.scrollview', scrollview)

    # Minimal stub modules for kivymd
    kivymd = types.ModuleType('kivymd')
    kivymd.__path__ = []
    sys.modules.setdefault('kivymd', kivymd)

    md_uix_pkg = types.ModuleType('kivymd.uix')
    md_uix_pkg.__path__ = []
    sys.modules.setdefault('kivymd.uix', md_uix_pkg)

    app = types.ModuleType('kivymd.app')
    class MDApp:
        pass
    app.MDApp = MDApp
    sys.modules.setdefault('kivymd.app', app)

    sm = types.ModuleType('kivymd.uix.screenmanager')
    class MDScreenManager:
        pass
    sm.MDScreenManager = MDScreenManager
    sys.modules.setdefault('kivymd.uix.screenmanager', sm)

    screen = types.ModuleType('kivymd.uix.screen')
    class MDScreen:
        def __init__(self, *args, **kwargs):
            self.ids = {}
            self.manager = types.SimpleNamespace(current="")
    screen.MDScreen = MDScreen
    sys.modules.setdefault('kivymd.uix.screen', screen)

    button = types.ModuleType('kivymd.uix.button')
    class MDRaisedButton:
        pass
    class MDFlatButton:
        def __init__(self, *args, **kwargs):
            pass
    button.MDRaisedButton = MDRaisedButton
    button.MDFlatButton = MDFlatButton
    sys.modules.setdefault('kivymd.uix.button', button)

    dialog = types.ModuleType('kivymd.uix.dialog')
    class BaseDialog:
        def __init__(self, *args, **kwargs):
            pass
        def open(self):
            pass
        def dismiss(self):
            pass
    dialog.MDDialog = BaseDialog
    sys.modules.setdefault('kivymd.uix.dialog', dialog)

    label = types.ModuleType('kivymd.uix.label')
    class MDLabel:
        pass
    label.MDLabel = MDLabel
    sys.modules.setdefault('kivymd.uix.label', label)

    textfield = types.ModuleType('kivymd.uix.textfield')
    class MDTextField:
        def __init__(self, *args, **kwargs):
            self.text = ''
    textfield.MDTextField = MDTextField
    sys.modules.setdefault('kivymd.uix.textfield', textfield)

def test_dialog(monkeypatch):
    setup_dummy_kivy()
    spec = importlib.util.spec_from_file_location('main', os.path.join(os.path.dirname(__file__), '..', 'main.py'))
    main = importlib.util.module_from_spec(spec)
    sys.modules['main'] = main
    spec.loader.exec_module(main)

    class DummyDialog:
        def __init__(self, title=None, text=None, buttons=None):
            self.title = title
            self.text = text
            self.buttons = buttons
            self.open_called = False
        def open(self):
            self.open_called = True
        def dismiss(self):
            pass

    def dialog_factory(*args, **kwargs):
        frame = inspect.currentframe().f_back
        screen = frame.f_locals.get('self')
        dlg = DummyDialog(*args, **kwargs)
        if screen is not None:
            screen.dialog_inst = dlg
        return dlg

    monkeypatch.setattr(main, 'MDDialog', dialog_factory)

    screen = main.CajaWizardScreen(name='caja')
    screen.dialog('mensaje')

    assert hasattr(screen, 'dialog_inst')
    assert screen.dialog_inst.title == 'Atención'

