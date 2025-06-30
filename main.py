from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivy.properties import StringProperty, ListProperty, ObjectProperty, NumericProperty
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView

KV = '''
<StepHeader@MDBoxLayout>:
    orientation: "horizontal"
    size_hint_y: None
    height: "50dp"
    padding: "10dp"
    spacing: "10dp"
    MDLabel:
        text: "1. Base de Caja"
        theme_text_color: "Custom"
        text_color: (0, 0, 0, 1) if root.parent.current_step == 1 else (0.5, 0.5, 0.5, 1)
    MDLabel:
        text: "2. Comprobantes"
        theme_text_color: "Custom"
        text_color: (0, 0, 0, 1) if root.parent.current_step == 2 else (0.5, 0.5, 0.5, 1)

<CajaWizardScreen>:
    name: "caja"
    current_step: 1
    StepHeader:
        id: header
    ScrollView:
        MDBoxLayout:
            id: container
            orientation: "vertical"
            adaptive_height: True
            padding: "10dp"
            spacing: "20dp"
            MDLabel:
                text: "Monto en caja (billetes):"
                font_style: "Subtitle1"
            MDTextField:
                id: monto_field
                hint_text: "Ej: 250000"
                input_filter: "int"
                on_text: root.base_total = self.text
            MDLabel:
                id: base_caja_total
                text: "[b]Total base:[/b] $" + (root.base_total or "0")
                markup: True
            MDRaisedButton:
                text: "Siguiente"
                on_release: root.next_step()

<ComprobanteScreen>:
    name: "comprobante"
    MDBoxLayout:
        orientation: "vertical"
        padding: "10dp"
        spacing: "10dp"
        MDTextField:
            id: uso_field
            hint_text: "Uso: Gasto, Pago, Nómina"
            on_text: root.on_uso_changed(self.text)
        MDTextField:
            id: concepto_field
            hint_text: "Concepto"
            on_text: root.on_concepto_changed(self.text)
        MDTextField:
            id: monto_field
            hint_text: "Monto del comprobante"
            input_filter: "int"
        MDFlatButton:
            text: "Guardar comprobante"
            on_release: root.guardar_comprobante()
        MDRaisedButton:
            text: "Volver"
            on_release: app.root.current = "caja"
'''

class CajaWizardScreen(MDScreen):
    base_total = StringProperty("0")
    current_step = NumericProperty(1)

    def next_step(self):
        if self.ids.monto_field.text.strip() == "":
            self.dialog("Debes ingresar un monto")
            return
        self.manager.current = "comprobante"

    def dialog(self, mensaje):
        MDDialog(title="Atención", text=mensaje, buttons=[
            MDFlatButton(text="OK", on_release=lambda x: self.dialog_inst.dismiss())
        ])
        self.dialog_inst.open()

class ComprobanteScreen(MDScreen):
    def on_uso_changed(self, texto):
        if texto.lower() == "gasto":
            self.dialog_firma()

    def on_concepto_changed(self, concepto):
        if concepto.lower() == "abono a proveedores":
            self.dialog_facturas()

    def dialog_firma(self):
        self.dialog_inst = MDDialog(
            title="Requiere Firma",
            text="Este comprobante requiere capturar una firma del usuario.",
            buttons=[MDFlatButton(text="Firmar", on_release=lambda x: self.dialog_inst.dismiss())]
        )
        self.dialog_inst.open()

    def dialog_facturas(self):
        facturas = ["Factura F001 - $150.000", "Factura F002 - $90.000"]
        content = BoxLayout(orientation='vertical', size_hint_y=None, height="200dp")
        for factura in facturas:
            content.add_widget(MDLabel(text=factura))
        self.dialog_inst = MDDialog(
            title="Selecciona Facturas",
            type="custom",
            content_cls=content,
            buttons=[MDFlatButton(text="Aceptar", on_release=lambda x: self.dialog_inst.dismiss())]
        )
        self.dialog_inst.open()

    def guardar_comprobante(self):
        if not self.ids.uso_field.text or not self.ids.concepto_field.text or not self.ids.monto_field.text:
            self.dialog("Todos los campos son obligatorios.")
            return
        self.dialog("Comprobante guardado con éxito.")

    def dialog(self, mensaje):
        self.dialog_inst = MDDialog(
            title="Mensaje",
            text=mensaje,
            buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog_inst.dismiss())]
        )
        self.dialog_inst.open()

class RecibosApp(MDApp):
    def build(self):
        Builder.load_string(KV)
        sm = MDScreenManager()
        sm.add_widget(CajaWizardScreen(name="caja"))
        sm.add_widget(ComprobanteScreen(name="comprobante"))
        return sm

if __name__ == '__main__':
    RecibosApp().run()
