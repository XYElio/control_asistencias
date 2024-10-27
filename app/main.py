
"""
Script principal que inicializa una aplicación web con Streamlit.
Implementa un sistema de inicio de sesión básico.

Módulos requeridos:
- streamlit: Para crear la interfaz web
- datetime: Para manejo de fechas (aunque no se usa en este código)
- conexion: Módulo personalizado que contiene la conexión a base de datos
- login: Módulo personalizado que maneja la autenticación

Uso:
Ejecutar el archivo directamente para iniciar la aplicación web.
"""

import streamlit as st
from datetime import datetime
from conexion import db
from login import login


def main():
    """Función principal que inicia la aplicación y muestra la pantalla de login"""
    login()

if __name__ == "__main__":
    main()