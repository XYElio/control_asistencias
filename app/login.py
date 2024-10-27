"""
Sistema de Autenticación y Control de Acceso.

Este módulo implementa el sistema de autenticación y control de acceso para la aplicación
de control de asistencia. Maneja la interfaz de login, validación de usuarios y 
gestión de sesiones utilizando Streamlit.

Dependencias:
    - streamlit
    - hashlib
    - datetime
    - conexion (módulo local para manejo de base de datos)
    - vadmin (módulo local para interfaz de administrador)
    - alumno (módulo local para interfaz de jefe de grupo)

"""
import streamlit as st
import hashlib
from datetime import datetime
from conexion import db  
from vadmin import admin
from alumno import jefe_grupo



def estilo():

    """
    Aplica los estilos CSS personalizados a la interfaz de login.
    
    Descripción:
        Configura la apariencia visual de la interfaz de login aplicando
        estilos CSS personalizados a través de Streamlit.
    
    Elementos que personaliza:
        - Contenedor principal y fondo
        - Formulario de login
        - Campos de entrada
        - Botones
        - Títulos y textos
        - Efectos visuales y animaciones
    
    Nota:
        Los estilos se aplican usando st.markdown con unsafe_allow_html=True
    """
    st.markdown("""
        <style>
        /* Reset inicial */
        #root > div:nth-child(1) > div > div > div > div {
            all: unset;
        }
        
        /* Forzar color blanco en el título principal */
        div[class*="main"] div[class*="block-container"] h1 {
            color: white !important;
            text-align: center !important;
            font-weight: 600 !important;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2) !important;
        }
        
        /* Asegurar que cualquier título dentro del contenedor principal sea blanco */
        .main .block-container h1,
        .main h1,
        h1[data-testid*="stHeader"],
        div[class*="stMarkdown"] h1 {
            color: white !important;
            text-align: center !important;
        }
        
        /* Titulo específico con máxima especificidad */
        div[data-testid="stAppViewContainer"] 
        div[data-testid="stHeader"] 
        div[class*="stMarkdown"] 
        h1 {
            color: white !important;
        }
        /* Estilo para el contenedor principal - Aumentada especificidad */
        div[class*="main"] div[class*="block-container"] {
            padding-top: 2rem !important;
            max-width: 450px !important;
            margin: 0 auto !important;
        }

        /* Fondo de la aplicación - Forzado */
        div[class*="stApp"] {
            background: linear-gradient(135deg, #2B2D42 0%, #1A1B2E 100%) !important;
            min-height: 100vh !important;
        }

        /* Título principal centrado - Mayor especificidad */
        div[class*="main"] div[class*="block-container"] h1:first-of-type {
            text-align: center !important;
            font-size: 32px !important;
            margin-bottom: 35px !important;
            color: white !important;
            font-weight: 600 !important;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2) !important;
            padding: 20px 0 !important;
            font-family: sans-serif !important;
            position: absolute !important;
            left: 50% !important;
            transform: translateX(-50%) !important;
            width: 100% !important;
        }

        /* Estilos para el formulario de login - Forzado */
        div[data-testid="stForm"] {
            background: white !important;
            border-radius: 15px !important;
            padding: 40px !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15) !important;
            margin-top: 80px !important;
        }

        /* Contenedor de los inputs - Especificidad aumentada */
        div[data-testid="stTextInput"] > div > div {
            margin-bottom: 25px !important;
            position: relative !important;
        }

        /* Estilizar los inputs - Forzado */
        div[class*="stTextInput"] input {
            width: 100% !important;
            height: 45px !important;
            border: none !important;
            border-bottom: 2px solid #E5E5E5 !important;
            font-size: 16px !important;
            padding: 10px 0 !important;
            background: transparent !important;
            transition: all 0.3s ease !important;
        }

        div[class*="stTextInput"] input[type="password"] {
            padding-right: 45px !important;
        }

        div[class*="stTextInput"] input:focus {
            border-color: #2B2D42 !important;
            box-shadow: none !important;
        }

        /* Estilo para las etiquetas - Especificidad aumentada */
        div[class*="stTextInput"] label {
            color: #2B2D42 !important;
            font-size: 16px !important;
            font-weight: 500 !important;
            margin-bottom: 8px !important;
        }

        /* Estilo para el botón de mostrar/ocultar contraseña - Forzado */
        button[data-testid="passwordShowHideButton"] {
            position: absolute !important;
            right: 10px !important;
            top: 70% !important;
            transform: translateY(-50%) !important;
            background: transparent !important;
            border: none !important;
            border-radius: 4px !important;
            cursor: pointer !important;
            padding: 8px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            transition: background-color 0.2s ease !important;
            width: 36px !important;
            height: 36px !important;
        }

        button[data-testid="passwordShowHideButton"]:hover {
            background: #e9ecef !important;
        }

        button[data-testid="passwordShowHideButton"] svg {
            width: 18px !important;
            height: 18px !important;
            color: #495057 !important;
            opacity: 0.8 !important;
        }

        /* Botón de submit - Mayor especificidad */
        div[class*="stButton"] > button:first-child {
            width: 100% !important;
            height: 50px !important;
            background: #2B2D42 !important;
            color: white !important;
            font-size: 18px !important;
            font-weight: 500 !important;
            border: none !important;
            border-radius: 25px !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            margin-top: 20px !important;
            text-transform: none !important;
        }

        div[class*="stButton"] > button:first-child:hover {
            background: #1A1B2E !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 5px 15px rgba(43, 45, 66, 0.2) !important;
            color: white !important;
        }

        /* Ocultar elementos - Forzado */
        section[data-testid="stSidebar"],
        #MainMenu, 
        footer, 
        header {
            visibility: hidden !important;
            display: none !important;
        }
        
        /* Asegurar que no haya scrollbars innecesarios */
        .main .block-container {
            overflow: visible !important;
        }
        </style>
    """, unsafe_allow_html=True)



def init_session_state():
    """
    Inicializa las variables de estado de la sesión.
    
    Descripción:
        Configura las variables iniciales en st.session_state para controlar
        el estado de la sesión del usuario.
    
    Variables que inicializa:
        - logged_in: Estado de la sesión del usuario
        - user_data: Datos del usuario autenticado
    """
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None



def mostrar_interface_jefe_grupo(user_data):
    """
    Muestra la interfaz específica para jefes de grupo.
    
    Parámetros:
        user_data (dict): Diccionario con la información del jefe de grupo.
            Debe contener:
            - username: Identificador del usuario
            - role: Rol del usuario
            - status: Estado del usuario
            - nombre: Nombre del usuario
            - apellidos: Apellidos del usuario
    """
    jefe_grupo(user_data)
def validate_user(username: str, password: str):
    """
    Valida las credenciales del usuario contra la base de datos.
    
    Parámetros:
        username (str): Nombre de usuario a validar
        password (str): Contraseña del usuario
    
    Retorna:
        tuple: (bool, dict) 
            - bool: True si la validación es exitosa, False en caso contrario
            - dict: Datos del usuario si la validación es exitosa, None en caso contrario
                Contiene: username, role, status, nombre, apellidos
    
    Excepciones:
        Exception: Si hay errores en la consulta a la base de datos
    
    Nota:
        La contraseña se procesa con hash SHA-256 antes de la validación
    """
    try:
        # Hash de la contraseña
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Consulta usando el execute_query de DatabaseConnection
        query = """
            SELECT u.usuario, u.tipo, u.estatus,
                COALESCE(a.nombre, p.nombre, j.nombre) as nombre,
                COALESCE(a.apellidos, p.apellidos, j.apellidos) as apellidos
            FROM usuarios u
            LEFT JOIN administracion a ON u.usuario = a.usuario
            LEFT JOIN profesores p ON u.usuario = p.usuario
            LEFT JOIN jefes_grupo j ON u.usuario = j.usuario
            WHERE u.usuario = %s 
            AND u.contrasenia = %s 
            AND u.estatus = 'activo'
        """

        result = db.execute_query(query, (username, password))

        if result and len(result) > 0:
            user_data = {
                'username': result[0]['usuario'],
                'role': result[0]['tipo'],
                'status': result[0]['estatus'],
                'nombre': result[0]['nombre'],
                'apellidos': result[0]['apellidos']
            }
            return True, user_data

        return False, None

    except Exception as e:
        st.error(f"Error en la validación: {str(e)}")
        return False, None

def show_login_form():
    estilo()
    """
    Muestra el formulario de inicio de sesión.
    
    Descripción:
        Crea y muestra un formulario con campos para usuario y contraseña,
        y maneja el proceso de autenticación cuando se envía el formulario.
    
    Elementos del formulario:
        - Campo de usuario
        - Campo de contraseña (oculto)
        - Botón de inicio de sesión
    
    Nota:
        Actualiza el estado de la sesión si la autenticación es exitosa
    """
    with st.form("login_form"):
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Iniciar Sesión")

        if submit and username and password:
            success, user_data = validate_user(username, password)
            if success:
                st.session_state.logged_in = True
                st.session_state.user_data = user_data
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")

def show_user_interface():
    """
    Muestra la interfaz correspondiente al rol del usuario autenticado.
    
    Descripción:
        Determina y muestra la interfaz apropiada basada en el rol del usuario:
        - Administrador: Muestra la interfaz de administración
        - Jefe de grupo: Muestra la interfaz de jefe de grupo
    
    Funcionalidades:
        - Muestra información básica del usuario
        - Proporciona botón de cierre de sesión
        - Redirige a la interfaz específica según el rol
    
    Nota:
        Al cerrar sesión, limpia el estado y cierra la conexión a la base de datos
    """
    st.write(f"Bienvenido, {st.session_state.user_data['nombre']} {st.session_state.user_data['apellidos']}")
    st.write(f"Rol: {st.session_state.user_data['role']}")

   # En tu función main o donde manejes la navegación principal
    if st.session_state.user_data['role'] == "administrador":  
        admin()
    elif st.session_state.user_data['role'] == "jefe_grupo":
        # Pasamos los datos del usuario almacenados en session_state
        mostrar_interface_jefe_grupo(st.session_state.user_data)

    if st.button("Cerrar Sesión"):
        st.session_state.logged_in = False
        st.session_state.user_data = None
        db.close()  # Cerramos la conexión al cerrar sesión
        st.rerun()

def login():
    
    """
    Función principal que maneja el flujo de autenticación.
    
    Descripción:
        Controla el flujo principal de la autenticación y navegación del sistema.
        Inicializa el estado de la sesión y muestra la interfaz apropiada según
        el estado de autenticación del usuario.
    
    Flujo de ejecución:
        1. Muestra el título de la aplicación
        2. Inicializa el estado de la sesión
        3. Muestra el formulario de login o la interfaz de usuario según corresponda
    """
    st.title("Sistema de Control de Asistencia")

    init_session_state()

    if not st.session_state.logged_in:
        show_login_form()
    else:
        show_user_interface()