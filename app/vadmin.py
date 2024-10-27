from conexion import db
from reporte import generar_reportes
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from fpdf import FPDF
import tempfile
from datetime import datetime
import os

def estilo_admin():
    """
    Aplica estilos CSS modernos y profesionales al panel de administración,
    con énfasis en la legibilidad del texto.
    Esta función debe ser llamada al inicio de la aplicación.
    """
    
    
    st.markdown("""
        <style>
        /* Variables globales */
        :root {
            --primary: #2D3250;
            --secondary: #424769;
            --accent: #7077A1;
            --light: #F6B17A;
            --white: #ffffff;
            --text-primary: #E6E6E6;
            --dark: #1a1c2d;
            --success: #2ecc71;
            --danger: #e74c3c;
            --warning: #f1c40f;
            --shadow-sm: 0 2px 4px rgba(0,0,0,0.1);
            --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
            --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
            --transition: all 0.3s ease;
        }

        /* Estilos globales */
        .stApp {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: var(--text-primary);
            font-family: 'Inter', sans-serif;
            font-size: 16px;
        }

        /* Header y títulos */
        h1 {
            color: var(--light);
            font-weight: 700;
            font-size: 2.5rem;
            margin-bottom: 2rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }

        h2, h3 {
            color: var(--white);
            font-weight: 600;
            margin-top: 1.5rem;
            font-size: 1.75rem;
        }
                
        


        /* Labels y texto de formularios - FUERA DE LOS INPUTS */
        label, .stTextInput label, .stSelectbox label, 
        .stNumberInput label, .stDateInput label {
            color: var(--white) !important;
            font-size: 1.1rem !important;
            font-weight: 500 !important;
            margin-bottom: 0.5rem !important;
            letter-spacing: 0.3px;
        }

        /* Widgets y controles - DENTRO DE LOS INPUTS */
        .stTextInput > div > div > input,
        .stSelectbox > div,
        .stMultiSelect > div,
        .stNumberInput > div > div > input,
        .stDateInput > div > div > input {
            background: rgba(255, 255, 255, 0.9) !important;
            border: 1px solid rgba(112, 119, 161, 0.3);
            border-radius: 8px;
            color: #000000 !important;
            font-size: 1.1rem !important;
            padding: 0.75rem !important;
            transition: var(--transition);
        }

        /* Para los textos de los selectbox y otros inputs */
        .stTextInput input,
        .stNumberInput input,
        .stDateInput input,
        .stTextArea textarea,
        .stSelectbox div[data-baseweb="select"] span {
            color: #000000 !important;
            font-weight: 500 !important;
        }

        /* Estado focus de los inputs */
        .stTextInput > div > div > input:focus,
        .stSelectbox > div:focus-within,
        .stMultiSelect > div:focus-within,
        .stNumberInput > div > div > input:focus,
        .stDateInput > div > div > input:focus {
            border-color: var(--light);
            box-shadow: 0 0 0 2px rgba(246, 177, 122, 0.2);
        }

        /* Botones */
        .stButton > button {
            background: linear-gradient(45deg, var(--accent), var(--light));
            border: none;
            border-radius: 8px;
            color: var(--white);
            font-size: 1.1rem !important;
            font-weight: 600;
            padding: 0.75rem 2rem;
            transition: var(--transition);
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }

        /* DataFrames y tablas */
        .dataframe {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 10px;
            border: 1px solid rgba(112, 119, 161, 0.2);
            font-size: 1.1rem;
        }

        .dataframe th {
            background: var(--secondary);
            color: var(--white);
            padding: 1rem;
            font-weight: 600;
            font-size: 1.1rem;
        }

        .dataframe td {
            color: var(--white);
            padding: 0.75rem;
            font-size: 1.1rem;
            border-bottom: 1px solid rgba(112, 119, 161, 0.1);
        }

        /* Texto de error y validación */
        .stAlert {
            background: rgba(255, 255, 255, 0.08);
            border-radius: 10px;
            border-left: 4px solid var(--accent);
            padding: 1rem;
            font-size: 1.1rem;
            color: var(--white);
        }
        /* Formularios */
        form {
            background: rgba(255, 255, 255, 0.05);
            padding: 2rem;
            border-radius: 15px;
            border: 1px solid rgba(112, 119, 161, 0.2);
            margin: 1rem 0;
        }

        /* Estilo específico para el texto del selectbox */
        .css-1whk732, .css-81oif8,
        .st-emotion-cache-1whk732, .st-emotion-cache-81oif8 {
            background-color: rgba(255, 255, 255, 0.9) !important;
            color: #000000 !important;
            font-size: 1.3rem !important;
            font-weight: 500 !important;
        }

        /* Scrollbar personalizada */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }

        ::-webkit-scrollbar-track {
            background: var(--primary);
        }

        ::-webkit-scrollbar-thumb {
            background: var(--accent);
            border-radius: 5px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--light);
        }
        </style>
    """, unsafe_allow_html=True)

# Manejamos el estado de "actualizado" en session_state
if 'updated' not in st.session_state:
    st.session_state.updated = False

def update_database():
    """Función para actualizar el estado de la base de datos en session_state."""
    st.session_state.updated = True
    st.rerun()  # Forzar la recarga de la página para actualizar los datos

def execute_db_operation(query, params, operation_name):
    """
    Ejecuta una operación en la base de datos con manejo de errores mejorado.
    
    Args:
        query (str): Consulta SQL a ejecutar
        params (tuple): Parámetros para la consulta
        operation_name (str): Nombre de la operación para mensajes de error
    
    Returns:
        bool: True si la operación fue exitosa, False en caso contrario
    """
    try:
        result = db.execute_query(query, params, commit=True)
        if result is not None:
            return True
        st.error(f"Error en {operation_name}: No se pudo completar la operación")
        return False
    except Exception as e:
        st.error(f"Error en {operation_name}: {str(e)}")
        return False

def mostrar_campos_comunes():
    usuario = st.text_input("Usuario")
    contrasenia = st.text_input("Contraseña", type="password")
    
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre")
        fecha_nacimiento = st.date_input("Fecha de Nacimiento")
        telefono = st.text_input("Teléfono")
    with col2:
        apellidos = st.text_input("Apellidos")
        direccion = st.text_input("Dirección")
    
    return {
        'usuario': usuario,
        'contrasenia': contrasenia,
        'nombre': nombre,
        'apellidos': apellidos,
        'fecha_nacimiento': fecha_nacimiento,
        'direccion': direccion,
        'telefono': telefono
    }

def get_available_groups():
    """Returns a list of predefined standard groups."""
    grades = range(1, 10)  # 1 to 9
    sections = ['A', 'B', 'C', 'D', 'G']
    groups = []
    
    for grade in grades:
        for section in sections:
            groups.append(f"{grade}{section}")
            
    return sorted(groups)

def mostrar_campos_jefe_grupo():
    try:
        # First try to get groups from database
        grupos_query = "SELECT DISTINCT grupo FROM profesor_materia ORDER BY grupo"
        grupos_disponibles = [row[0] for row in db.execute_query(grupos_query)]
        if not grupos_disponibles:
            # If no groups in database, use predefined list
            grupos_disponibles = get_available_groups()
    except:
        # If database query fails, fall back to predefined list
        grupos_disponibles = get_available_groups()
    
    grupo_asignado = st.selectbox(
        "Grupo a Asignar",
        options=grupos_disponibles,
        key="grupo_select"
    )
    return grupo_asignado

def alta_usuario():
    """Función para dar de alta a un nuevo usuario."""
    st.subheader("Alta de Usuario")
    
    # Primero solo mostrar el selector de tipo de usuario
    tipo_usuario = st.selectbox(
        "Tipo de Usuario",
        ["Seleccionar...", "profesor", "administrador", "jefe_grupo"]
    )
    
    # Solo mostrar el formulario si se ha seleccionado un tipo de usuario
    if tipo_usuario != "Seleccionar...":
        with st.form("alta_usuario_form"):
            # Obtener los campos comunes
            datos = mostrar_campos_comunes()
            
            # Campos específicos según el tipo de usuario
            grupo_asignado = None
            if tipo_usuario == "jefe_grupo":
                grupo_asignado = mostrar_campos_jefe_grupo()
            
            submitted = st.form_submit_button("Registrar Usuario")
            
            if submitted:
                # Validaciones básicas
                if not all([datos['usuario'], datos['contrasenia'], datos['nombre'], datos['apellidos']]):
                    st.error("Por favor complete todos los campos obligatorios")
                    return
                
                # Validación específica para jefe de grupo
                if tipo_usuario == "jefe_grupo" and not grupo_asignado:
                    st.error("Debe asignar un grupo al jefe de grupo")
                    return
                
                # Verificar si el usuario ya existe
                check_query = "SELECT usuario FROM usuarios WHERE usuario = %s"
                existing_user = db.execute_query(check_query, (datos['usuario'],))
                if existing_user:
                    st.error("El nombre de usuario ya existe")
                    return
                
                # Verificar si el grupo ya tiene un jefe asignado
                if tipo_usuario == "jefe_grupo":
                    check_grupo_query = "SELECT Usuario FROM jefes_grupo WHERE Grupos = %s"
                    existing_grupo = db.execute_query(check_grupo_query, (grupo_asignado,))
                    if existing_grupo:
                        st.error(f"El grupo {grupo_asignado} ya tiene un jefe asignado")
                        return
                
                # Iniciar las operaciones de base de datos
                success = True
                
                # Insertar en tabla usuarios
                user_query = """
                    INSERT INTO usuarios (Usuario, Contrasenia, tipo)
                    VALUES (%s, %s, %s)
                """
                success &= execute_db_operation(
                    user_query, 
                    (datos['usuario'], datos['contrasenia'], tipo_usuario),
                    "inserción de usuario"
                )
                
                if success:
                    # Preparar datos comunes
                    common_data = {
                        'Usuario': datos['usuario'],
                        'Nombre': datos['nombre'],
                        'Apellidos': datos['apellidos'],
                        'Fecha_nacimiento': datos['fecha_nacimiento'],
                        'Direccion': datos['direccion'],
                        'Telefono': datos['telefono']
                    }
                    
                    # Insertar según el tipo
                    if tipo_usuario == "profesor":
                        query = """
                            INSERT INTO profesores 
                            (Usuario, Nombre, Apellidos, Fecha_nacimiento, Direccion, 
                             Telefono)
                            VALUES (%(Usuario)s, %(Nombre)s, %(Apellidos)s, 
                                   %(Fecha_nacimiento)s, %(Direccion)s, %(Telefono)s)
                        """
                        success &= execute_db_operation(query, common_data, "inserción de profesor")
                    
                    elif tipo_usuario == "administrador":
                        query = """
                            INSERT INTO administracion
                            (Usuario, Nombre, Apellidos, Fecha_nacimiento, Direccion, 
                             Telefono)
                            VALUES (%(Usuario)s, %(Nombre)s, %(Apellidos)s, 
                                   %(Fecha_nacimiento)s, %(Direccion)s, %(Telefono)s)
                        """
                        success &= execute_db_operation(query, common_data, "inserción de administrador")
                    
                    elif tipo_usuario == "jefe_grupo":
                        jefe_data = common_data.copy()
                        jefe_data['Grupos'] = grupo_asignado
                        query = """
                            INSERT INTO jefes_grupo
                            (Usuario, Nombre, Apellidos, Fecha_nacimiento, Direccion, 
                             Telefono, Grupos)
                            VALUES (%(Usuario)s, %(Nombre)s, %(Apellidos)s, 
                                   %(Fecha_nacimiento)s, %(Direccion)s, %(Telefono)s, 
                                   %(Grupos)s)
                        """
                        success &= execute_db_operation(query, jefe_data, "inserción de jefe de grupo")
                
                if success:
                    st.success(f"Usuario {datos['usuario']} registrado exitosamente")
                    update_database()

def baja_usuario():
    """Función para dar de baja a un usuario existente."""
    st.subheader("Baja de Usuario")
    
    # Obtener usuarios activos con verificación de resultados
    query = """
        SELECT 
            u.Usuario as usuario,
            u.tipo as tipo,
            COALESCE(a.Nombre, p.Nombre, j.Nombre) as nombre,
            COALESCE(a.Apellidos, p.Apellidos, j.Apellidos) as apellidos,
            u.Estatus as estatus
        FROM usuarios u
        LEFT JOIN administracion a ON u.Usuario = a.Usuario
        LEFT JOIN profesores p ON u.Usuario = p.Usuario
        LEFT JOIN jefes_grupo j ON u.Usuario = j.Usuario
        WHERE u.Estatus = 'activo'
    """
    usuarios = db.execute_query(query)
    
    if not usuarios:
        st.warning("No hay usuarios activos en el sistema")
        return
    
    # Mostrar tabla de usuarios
    df_usuarios = pd.DataFrame(usuarios)
    st.dataframe(df_usuarios)
    
    # Selección de usuario a dar de baja
    usuario_options = [f"{u['usuario']} - {u['nombre']} {u['apellidos']}" for u in usuarios]
    usuario_selected = st.selectbox(
        "Seleccione el usuario a dar de baja",
        options=usuario_options
    )
    
    motivo = st.text_area("Motivo de la baja", "")
    
    if st.button("Dar de Baja"):
        if not motivo:
            st.error("Por favor, especifique el motivo de la baja")
            return
        
        usuario_id = usuario_selected.split(" - ")[0]
        
        # Actualizar estatus en tabla usuarios
        query_update = """
            UPDATE usuarios 
            SET Estatus = 'inactivo'
            WHERE Usuario = %s
        """
        if execute_db_operation(query_update, (usuario_id,), "baja de usuario"):
            st.success(f"Usuario {usuario_id} dado de baja exitosamente")
            update_database()

def modificar_usuario():
    """Función para modificar datos de un usuario existente."""
    st.subheader("Modificar Usuario")
    
    query = """
        SELECT 
            u.Usuario as usuario,
            u.tipo as tipo,
            COALESCE(a.Nombre, p.Nombre, j.Nombre) as nombre,
            COALESCE(a.Apellidos, p.Apellidos, j.Apellidos) as apellidos,
            COALESCE(a.Telefono, p.Telefono, j.Telefono) as telefono,
            COALESCE(a.Direccion, p.Direccion, j.Direccion) as direccion,
            COALESCE(j.Grupos, '') as grupos
        FROM usuarios u
        LEFT JOIN administracion a ON u.Usuario = a.Usuario
        LEFT JOIN profesores p ON u.Usuario = p.Usuario
        LEFT JOIN jefes_grupo j ON u.Usuario = j.Usuario
        WHERE u.Estatus = 'activo'
    """
    
    usuarios = db.execute_query(query)
    
    if not usuarios:
        st.warning("No hay usuarios activos para modificar")
        return
    
    usuario_options = [f"{u['usuario']} - {u['nombre']} {u['apellidos']}" for u in usuarios]
    usuario_selected = st.selectbox(
        "Seleccione el usuario a modificar",
        options=usuario_options
    )
    
    usuario_id = usuario_selected.split(" - ")[0]
    usuario = next(u for u in usuarios if u['usuario'] == usuario_id)
    
    with st.form("modificar_usuario_form"):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre", value=usuario['nombre'])
            telefono = st.text_input("Teléfono", value=usuario['telefono'])
        with col2:
            apellidos = st.text_input("Apellidos", value=usuario['apellidos'])
            direccion = st.text_input("Dirección", value=usuario['direccion'])
        
        if usuario['tipo'] == 'jefe_grupo':
            grupos = st.text_input("Grupos", value=usuario['grupos'])
        
        nueva_contrasenia = st.text_input("Nueva Contraseña (dejar en blanco para mantener la actual)", type="password")
        
        submitted = st.form_submit_button("Actualizar Datos")
        
        if submitted:
            success = True
            
            if nueva_contrasenia:
                query = "UPDATE usuarios SET Contrasenia = %s WHERE Usuario = %s"
                success &= execute_db_operation(
                    query, 
                    (nueva_contrasenia, usuario_id),
                    "actualización de contraseña"
                )
            
            if success:
                if usuario['tipo'] == 'profesor':
                    query = """
                        UPDATE profesores
                        SET Nombre = %s, Apellidos = %s, Telefono = %s,
                            Direccion = %s
                        WHERE Usuario = %s
                    """
                    values = (nombre, apellidos, telefono, direccion, usuario_id)
                
                elif usuario['tipo'] == 'administrador':
                    query = """
                        UPDATE administracion
                        SET Nombre = %s, Apellidos = %s, Telefono = %s,
                            Direccion = %s
                        WHERE Usuario = %s
                    """
                    values = (nombre, apellidos, telefono, direccion, usuario_id)
                
                elif usuario['tipo'] == 'jefe_grupo':
                    query = """
                        UPDATE jefes_grupo
                        SET Nombre = %s, Apellidos = %s, Telefono = %s,
                            Direccion = %s, Grupos = %s
                        WHERE Usuario = %s
                    """
                    values = (nombre, apellidos, telefono, direccion, grupos, usuario_id)
                
                success &= execute_db_operation(query, values, "actualización de datos")
            
            if success:
                st.success("Datos actualizados exitosamente")
                update_database()

def alta_asignatura():
    """Función para dar de alta una nueva asignatura."""
    st.subheader("Alta de Asignatura")
    
    # Obtener carreras existentes
    carreras = db.execute_query("SELECT id_carrera, nombre FROM carreras")
    
    with st.form("alta_asignatura_form"):
        nombre = st.text_input("Nombre de la Asignatura")
        carrera_id = st.selectbox(
            "Carrera",
            options=[(c['id_carrera'], c['nombre']) for c in carreras],
            format_func=lambda x: x[1]
        )
        
        submitted = st.form_submit_button("Registrar Asignatura")
        
        if submitted:
            if not nombre:
                st.error("Por favor ingrese el nombre de la asignatura")
                return
                
            query = "INSERT INTO materias (nombre, carrera_id) VALUES (%s, %s)"
            if execute_db_operation(query, (nombre, carrera_id[0]), "alta de asignatura"):
                st.success(f"Asignatura '{nombre}' registrada exitosamente")
                update_database()

def asignar_materia():
    """Función para asignar materias a profesores."""
    st.subheader("Asignación de Materias")
    
    # Obtener profesores activos - Note the lowercase column aliases
    profesores = db.execute_query("""
        SELECT 
            p.Usuario as usuario,  
            CONCAT(p.Nombre, ' ', p.Apellidos) as nombre_completo
        FROM profesores p
        JOIN usuarios u ON p.Usuario = u.Usuario
        WHERE u.Estatus = 'activo'
    """)
    
    # Obtener materias
    materias = db.execute_query("""
        SELECT 
            m.id_materia,
            m.nombre,
            c.nombre as carrera
        FROM materias m
        JOIN carreras c ON m.carrera_id = c.id_carrera
    """)
    
    if not profesores:
        st.warning("No hay profesores activos disponibles")
        return
        
    if not materias:
        st.warning("No hay materias disponibles")
        return
    
    with st.form("asignar_materia_form"):
        profesor = st.selectbox(
            "Profesor",
            options=[(p['usuario'], p['nombre_completo']) for p in profesores],
            format_func=lambda x: x[1]
        )
        
        materia = st.selectbox(
            "Materia",
            options=[(m['id_materia'], f"{m['nombre']} - {m['carrera']}") for m in materias],
            format_func=lambda x: x[1]
        )
        
        grupo = st.text_input("Grupo")
        ciclo_escolar = st.text_input("Ciclo Escolar (ejemplo: 2024-1)")
        
        submitted = st.form_submit_button("Asignar Materia")
        
        if submitted:
            if not all([grupo, ciclo_escolar]):
                st.error("Por favor complete todos los campos")
                return
            
            # Verificar si ya existe la asignación
            check_query = """
                SELECT * FROM profesor_materia 
                WHERE profesor_usuario = %s 
                AND materia_id = %s 
                AND grupo = %s 
                AND ciclo_escolar = %s
            """
            existing = db.execute_query(check_query, 
                                     (profesor[0], materia[0], grupo, ciclo_escolar))
            
            if existing:
                st.error("Esta asignación ya existe")
                return
            
            query = """
                INSERT INTO profesor_materia 
                (profesor_usuario, materia_id, grupo, ciclo_escolar)
                VALUES (%s, %s, %s, %s)
            """
            if execute_db_operation(query, 
                                  (profesor[0], materia[0], grupo, ciclo_escolar),
                                  "asignación de materia"):
                st.success("Materia asignada exitosamente")
                update_database()

def admin():
    """Función principal de administración que maneja todas las operaciones administrativas."""
    estilo_admin()
    st.title("Panel de Administración")
    
    admin_option = st.sidebar.selectbox(
        "Seleccione una operación",
        ["Alta de Usuario", "Baja de Usuario", "Modificar Usuario","Alta de Asignatura", "Asignación de Materias", "Reportes"]
    )
    
    if admin_option == "Alta de Usuario":
        alta_usuario()
    elif admin_option == "Baja de Usuario":
        baja_usuario()
    elif admin_option == "Modificar Usuario":
        modificar_usuario()
    if admin_option == "Alta de Asignatura":
        alta_asignatura()
    elif admin_option == "Asignación de Materias":
        asignar_materia()
    elif admin_option == "Reportes":
        generar_reportes()