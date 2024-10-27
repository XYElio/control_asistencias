import streamlit as st
import hashlib
from datetime import datetime
from conexion import db  # Importamos la instancia global de DatabaseConnection
from vadmin import admin
from alumno import jefe_grupo



def estilo():
    st.markdown("""
        <style>
        /* Estilo para el contenedor principal */
        .main .block-container {
            padding-top: 2rem;
            max-width: 450px !important;
            margin: 0 auto;
        }

        /* Fondo de la aplicación */
        .stApp {
            background: linear-gradient(135deg, #2B2D42 0%, #1A1B2E 100%);
            min-height: 100vh;
        }

        /* Título principal centrado */
        .main .block-container h1 {
            text-align: center;
            font-size: 32px;
            margin-bottom: 35px;
            color: white;
            font-weight: 600;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            padding: 20px 0;
            font-family: sans-serif;
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
            width: 100%;
        }

        /* Estilos para el formulario de login */
        [data-testid="stForm"] {
            background: white;
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
            margin-top: 80px;
        }

        /* Contenedor de los inputs */
        [data-testid="stTextInput"] > div > div {
            margin-bottom: 25px;
            position: relative;
        }

        /* Estilizar los inputs */
        .stTextInput input {
            width: 100%;
            height: 45px;
            border: none;
            border-bottom: 2px solid #E5E5E5;
            font-size: 16px;
            padding: 10px 0;
            background: transparent;
            transition: all 0.3s ease;
        }

        .stTextInput input[type="password"] {
            padding-right: 45px;
        }

        .stTextInput input:focus {
            border-color: #2B2D42;
            box-shadow: none;
        }

        /* Estilo para las etiquetas */
        .stTextInput label {
            color: #2B2D42;
            font-size: 16px;
            font-weight: 500;
            margin-bottom: 8px;
        }

        /* Estilo para el botón de mostrar/ocultar contraseña */
        button[data-testid="passwordShowHideButton"] {
            position: absolute;
            right: 10px;  /* Ajuste la posición aquí */
            top: 70%;
            transform: translateY(-50%);
            background: transparent;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            padding: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background-color 0.2s ease;
            width: 36px;
            height: 36px;
        }

        button[data-testid="passwordShowHideButton"]:hover {
            background: #e9ecef;
        }

        /* Ajustar el ícono dentro del botón */
        button[data-testid="passwordShowHideButton"] svg {
            width: 18px;
            height: 18px;
            color: #495057;
            opacity: 0.8;
        }

        /* Botón de submit */
        .stButton > button {
            width: 100%;
            height: 50px;
            background: #2B2D42;
            color: white !important;
            font-size: 18px;
            font-weight: 500;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 20px;
            text-transform: none !important;
        }

        .stButton > button:hover {
            background: #1A1B2E;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(43, 45, 66, 0.2);
            color: white !important;
        }

        /* Ocultar elementos innecesarios de Streamlit */
        #MainMenu, footer, header {
            visibility: hidden;
        }
        </style>
    """, unsafe_allow_html=True)



def init_session_state():
    """Inicializa las variables de estado de la sesión"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None



def mostrar_interface_jefe_grupo(user_data):
    jefe_grupo(user_data)
def validate_user(username: str, password: str):
    """Valida las credenciales del usuario"""
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
    """Muestra el formulario de login"""
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
    """Muestra la interfaz del usuario según su rol"""
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
    st.title("Sistema de Control de Asistencia")

    init_session_state()

    if not st.session_state.logged_in:
        show_login_form()
    else:
        show_user_interface()