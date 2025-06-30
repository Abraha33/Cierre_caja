# Cierre de Caja

Este programa permite registrar el dinero inicial de la caja y generar comprobantes de pago o gastos. Está desarrollado con [Kivy](https://kivy.org/) y [KivyMD](https://kivymd.readthedocs.io/).

## Instalación

1. Instala las dependencias de Python:

```bash
pip install kivy kivymd
```

2. Ejecuta la aplicación:

```bash
python3 main.py
```

## Uso

Al iniciar se muestra la pantalla **Base de Caja** donde se ingresa la cantidad de cada billete y moneda que hay en la caja. En la parte inferior se calcula automáticamente el **Total base de caja**.

Después pulsa **Siguiente** para registrar un comprobante. En la pantalla de **Comprobantes** ingresa:

- **Uso** del comprobante (Gasto, Pago, Nómina, etc.). Al seleccionar "Gasto" se solicita una firma.
- **Concepto** del movimiento. Si escribes "abono a proveedores" se abrirá una ventana para seleccionar facturas relacionadas.
- **Monto** del comprobante.

Mientras llenas el formulario, la sección "Previsualización en Tiempo Real" actualiza los datos mostrados para revisar el recibo antes de guardarlo. Finalmente pulsa **Guardar comprobante**.

## Pruebas

Se incluye un pequeño conjunto de pruebas que verifican la creación de diálogos. Ejecuta:

```bash
pytest
```

