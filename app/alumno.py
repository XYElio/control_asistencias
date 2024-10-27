"""
Sistema de Registro de Asistencia de Profesores.

Este módulo implementa un sistema de registro y gestión de asistencias de profesores
utilizando Streamlit como framework de interfaz y PostgreSQL como base de datos.
El sistema está diseñado para ser utilizado por jefes de grupo para registrar
y monitorear la asistencia de los profesores asignados a sus grupos.

Dependencies:
    - streamlit
    - pytz
    - datetime
    - conexion (módulo local para manejo de base de datos)
"""

from conexion import db
from datetime import datetime, time
import streamlit as st
from typing import Dict, Optional, List
import pytz
import streamlit as st



def estilo_jefe():
    """
    Función para aplicar el estilo CSS en la interfaz de registro de asistencia para el jefe de grupo.

    Los estilos incluyen:
        - Configuración de fuentes y colores base
        - Estilos para formularios y campos de entrada
        - Diseño de botones y estados de hover
        - Estilos para mensajes de éxito y error
        - Formato de textos informativos

    Nota:
    Los estilos se aplican usando st.markdown con unsafe_allow_html=True
    """
    custom_css = """
        <style>
            /* Root variables para personalización */
            :root {
                --primary-color: #4A90E2;
                --secondary-color: #2ECC71;
                --background-color: #F8F9FA;
                --text-color: #2C3E50;
                --error-color: #E74C3C;
                --success-color: #27AE60;
                --border-radius: 8px;
                --box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }

            /* Estilos generales */
            .stApp {
                background-color: var(--background-color);
                color: var(--text-color);
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            }

            /* Estilos para headers */
            .css-10trblm {
                color: var(--primary-color);
                font-size: 2rem;
                font-weight: 700;
                margin-bottom: 2rem;
            }

            /* Estilos para formularios */
            .stForm {
                background: white;
                padding: 2rem;
                border-radius: var(--border-radius);
                box-shadow: var(--box-shadow);
            }

            /* Personalización de inputs */
            .stTextInput > div > div > input,
            .stSelectbox > div > div > input {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: var(--border-radius);
                padding: 0.5rem;
                transition: all 0.3s ease;
            }

            .stTextInput > div > div > input:focus,
            .stSelectbox > div > div > input:focus {
                border-color: var(--primary-color);
                box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
            }

            /* Estilos para botones */
            .stButton > button {
                background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
                color: white;
                border: none;
                border-radius: var(--border-radius);
                padding: 0.5rem 2rem;
                font-weight: 600;
                transition: all 0.3s ease;
            }

            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }

            /* Estilos para mensajes de estado */
            .stSuccess {
                background-color: rgba(46, 204, 113, 0.1);
                border: 1px solid var(--success-color);
                color: var(--success-color);
                padding: 1rem;
                border-radius: var(--border-radius);
            }

            .stError {
                background-color: rgba(231, 76, 60, 0.1);
                border: 1px solid var(--error-color);
                color: var(--error-color);
                padding: 1rem;
                border-radius: var(--border-radius);
            }

            /* Estilos para selectbox */
            .stSelectbox {
                margin-bottom: 1rem;
            }

            .stSelectbox > div > div > select {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: var(--border-radius);
                padding: 0.5rem;
            }

            /* Estilos para date input */
            .stDateInput {
                margin-bottom: 1rem;
            }

            .stDateInput > div > div > input {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: var(--border-radius);
                padding: 0.5rem;
            }

            /* Estilos para time input */
            .stTimeInput {
                margin-bottom: 1rem;
            }

            /* Estilos para textarea */
            .stTextArea textarea {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: var(--border-radius);
                padding: 0.5rem;
                min-height: 100px;
            }

            .stTextArea textarea:focus {
                border-color: var(--primary-color);
                box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
            }

            /* Estilos para info boxes */
            .stInfo {
                background-color: rgba(74, 144, 226, 0.1);
                border: 1px solid var(--primary-color);
                color: var(--primary-color);
                padding: 1rem;
                border-radius: var(--border-radius);
                margin-bottom: 1rem;
            }

            /* Responsive design adjustments */
            @media (max-width: 768px) {
                .stForm {
                    padding: 1rem;
                }

                .css-10trblm {
                    font-size: 1.5rem;
                }
            }
        </style>
    """
    
    # Aplicar los estilos usando st.markdown
    st.markdown(custom_css, unsafe_allow_html=True)

def jefe_grupo(user_data: Dict):
    estilo_jefe()
    """
    Función principal para el registro de asistencia por parte del jefe de grupo
    
    Parámetros:
        user_data (Dict): Diccionario con la información del jefe de grupo autenticado.
                         Debe contener al menos la clave 'username'.
    
    Excepciones:
        Exception: Si hay errores en la conexión con la base de datos o en el registro.
    
    Nota:
        La función maneja:
            - Formulario de registro de asistencia
            - Selección de fecha y materia
            - Registro de horarios
            - Estado de la clase y observaciones
    """
    st.subheader("Registro de Asistencia de Profesores")
    
    # Obtener el grupo asignado al jefe de grupo
    grupo_jefe = obtener_grupo_jefe(user_data['username'])
    if not grupo_jefe:
        st.error("No se encontró un grupo asignado para este jefe de grupo")
        return
        
    # Obtener materias y profesores del grupo
    materias_grupo = obtener_materias_grupo(grupo_jefe)
    if not materias_grupo:
        st.error(f"No se encontraron materias asignadas al grupo {grupo_jefe}")
        return
        
    # Formulario de registro de asistencia
    with st.form("registro_asistencia"):
        # Selector de fecha
        fecha = st.date_input("Fecha de asistencia", datetime.now(pytz.UTC))
        
        # Selector de materia/profesor
        opciones_materia = [
            f"{m['materia_nombre']} - {m['profesor_nombre']} {m['profesor_apellidos']}"
            for m in materias_grupo
        ]
        materia_seleccionada = st.selectbox("Seleccione Materia y Profesor", opciones_materia)
        
        # Obtener índice de la materia seleccionada
        idx = opciones_materia.index(materia_seleccionada)
        materia_data = materias_grupo[idx]
        
        # Mostrar horario programado
        st.info(f"Horario programado: {materia_data['hora_inicio'].strftime('%H:%M')} - {materia_data['hora_fin'].strftime('%H:%M')}")
        st.info(f"Días programados: {materia_data['dias_semana']}")
        
        # Campos de hora - usando valores por defecto del horario programado
        col1, col2 = st.columns(2)
        with col1:
            hora_inicio = st.time_input(
                "Hora de inicio",
                value=materia_data['hora_inicio']
            )
        with col2:
            hora_fin = st.time_input(
                "Hora de fin",
                value=materia_data['hora_fin']
            )
        
        # Campo de estatus y observaciones
        estatus = st.selectbox(
            "Estatus", 
            ["impartida", "no_impartida", "retardo"],
            help="Seleccione el estatus de la clase"
        )
        observaciones = st.text_area(
            "Observaciones",
            height=100,
            help="Agregue cualquier observación relevante sobre la clase"
        )
        
        submitted = st.form_submit_button("Registrar Asistencia")
        
        if submitted:
            # Validar que la fecha corresponda a un día programado
            dia_semana = fecha.strftime("%A").lower()
            dias_programados = [d.strip().lower() for d in materia_data['dias_semana'].split(',')]
            
            if not validar_dia_clase(dia_semana, dias_programados):
                st.error("La fecha seleccionada no corresponde a un día programado para esta clase")
                return
                
            # Validar que no exista un registro previo
            if verificar_registro_existente(fecha, materia_data['profesor_usuario'], materia_data['materia_id'], grupo_jefe):
                st.error("Ya existe un registro de asistencia para esta clase en la fecha seleccionada")
                return
            
            # Validar el orden de las horas
            if hora_fin <= hora_inicio:
                st.error("La hora de fin debe ser posterior a la hora de inicio")
                return
                
            # Registrar la asistencia
            try:
                success = registrar_asistencia(
                    fecha=fecha,
                    hora_inicio=hora_inicio,
                    hora_fin=hora_fin,
                    profesor_usuario=materia_data['profesor_usuario'],
                    materia_id=materia_data['materia_id'],
                    grupo=grupo_jefe,
                    estatus=estatus,
                    observaciones=observaciones
                )
                
                if success:
                    st.success("Asistencia registrada correctamente")
                    # Limpiar el formulario usando rerun
                    st.experimental_rerun()
            except Exception as e:
                st.error(f"Error al registrar la asistencia: {str(e)}")

def obtener_grupo_jefe(usuario: str) -> Optional[str]:
    """
    Consulta y retorna el grupo asignado al jefe de grupo.
    
    Parámetros:
        usuario (str): Identificador único del jefe de grupo.
    
    Retorna:
        Optional[str]: Identificador del grupo asignado o None si no se encuentra.
    
    Excepciones:
        Exception: Si hay errores en la consulta a la base de datos.
    """
    query = """
    SELECT grupos 
    FROM jefes_grupo 
    WHERE usuario = %s
    """
    try:
        result = db.execute_query(query, (usuario,))
        return result[0]['grupos'] if result else None
    except Exception as e:
        st.error(f"Error al obtener grupo: {str(e)}")
        return None

def obtener_materias_grupo(grupo: str) -> Optional[List[Dict]]:
    """
    Obtiene las materias y profesores asignados a un grupo específico.
    
    Parámetros:
        grupo (str): Identificador del grupo a consultar.
    
    Retorna:
        Optional[List[Dict]]: Lista de diccionarios con la información de materias y profesores.
            Cada diccionario contiene:
            - profesor_usuario (str): ID del profesor
            - profesor_nombre (str): Nombre del profesor
            - profesor_apellidos (str): Apellidos del profesor
            - materia_id (int): ID de la materia
            - materia_nombre (str): Nombre de la materia
            - dias_semana (str): Días programados
            - hora_inicio (time): Hora de inicio de clase
            - hora_fin (time): Hora de fin de clase
            - aula (str): Aula asignada
    
    Excepciones:
        Exception: Si hay errores en la consulta a la base de datos.
    """
    query = """
    SELECT 
        pm.profesor_usuario,
        p.nombre as profesor_nombre,
        p.apellidos as profesor_apellidos,
        m.id_materia as materia_id,
        m.nombre as materia_nombre,
        pm.dias_semana,
        pm.hora_inicio::TIME as hora_inicio,
        pm.hora_fin::TIME as hora_fin,
        pm.aula
    FROM profesor_materia pm
    JOIN profesores p ON pm.profesor_usuario = p.usuario
    JOIN materias m ON pm.materia_id = m.id_materia
    WHERE pm.grupo = %s
    AND pm.ciclo_escolar = (
        SELECT ciclo_escolar 
        FROM profesor_materia 
        WHERE grupo = %s 
        ORDER BY ciclo_escolar DESC 
        LIMIT 1
    )
    """
    try:
        return db.execute_query(query, (grupo, grupo))
    except Exception as e:
        st.error(f"Error al obtener materias: {str(e)}")
        return None

def validar_dia_clase(dia_actual: str, dias_programados: List[str]) -> bool:
    """
    Valida si un día específico corresponde a los días programados para la clase.
    
    Parámetros:
        dia_actual (str): Día de la semana en inglés (ej: 'monday', 'tuesday').
        dias_programados (List[str]): Lista de días permitidos en español.
    
    Retorna:
        bool: True si el día es válido, False en caso contrario.
    
    Ejemplo:
        >>> validar_dia_clase('monday', ['lunes', 'miércoles'])
        True
    """
    dias = {
        'monday': 'lunes',
        'tuesday': 'martes',
        'wednesday': 'miércoles',
        'thursday': 'jueves',
        'friday': 'viernes',
        'saturday': 'sábado',
        'sunday': 'domingo'
    }
    return dias.get(dia_actual, '').lower() in [d.lower() for d in dias_programados]

def verificar_registro_existente(fecha: datetime, profesor: str, materia: int, grupo: str) -> bool:
    """
    Verifica si ya existe un registro de asistencia para una combinación específica.
    
    Parámetros:
        fecha (datetime): Fecha del registro a verificar.
        profesor (str): ID del profesor.
        materia (int): ID de la materia.
        grupo (str): ID del grupo.
    
    Retorna:
        bool: True si existe un registro, False en caso contrario.
    
    Excepciones:
        Exception: Si hay errores en la consulta a la base de datos.
    """
    query = """
    SELECT id_asistencia 
    FROM asistencias 
    WHERE fecha = %s::date 
    AND profesor_usuario = %s 
    AND materia_id = %s 
    AND grupo = %s
    """
    try:
        result = db.execute_query(query, (fecha, profesor, materia, grupo))
        return bool(result)
    except Exception as e:
        st.error(f"Error al verificar registro existente: {str(e)}")
        return True

def registrar_asistencia(
    fecha: datetime,
    hora_inicio: time,
    hora_fin: time,
    profesor_usuario: str,
    materia_id: int,
    grupo: str,
    estatus: str,
    observaciones: str
) -> bool:
    """
    Registra la asistencia de un profesor en la base de datos.
    
    Parámetros:
        fecha (datetime): Fecha de la clase.
        hora_inicio (time): Hora de inicio de la clase.
        hora_fin (time): Hora de finalización de la clase.
        profesor_usuario (str): ID del profesor.
        materia_id (int): ID de la materia.
        grupo (str): ID del grupo.
        estatus (str): Estado de la clase ('impartida', 'no_impartida', 'retardo').
        observaciones (str): Comentarios adicionales sobre la clase.
    
    Retorna:
        bool: True si el registro fue exitoso, False en caso contrario.
    
    Excepciones:
        Exception: Si hay errores en la inserción en la base de datos.
    
    Nota:
        El estatus solo puede ser uno de los siguientes valores:
        - 'impartida': Clase impartida normalmente
        - 'no_impartida': Clase no impartida
        - 'retardo': Clase impartida con retardo
    """
    query = """
    INSERT INTO asistencias (
        fecha, hora_inicio, hora_fin, profesor_usuario,
        materia_id, grupo, estatus, observaciones
    ) VALUES (%s::date, %s::time, %s::time, %s, %s, %s, %s, %s)
    """
    params = (
        fecha, hora_inicio, hora_fin, profesor_usuario,
        materia_id, grupo, estatus, observaciones
    )
    try:
        return db.execute_query(query, params, commit=True)
    except Exception as e:
        st.error(f"Error al registrar asistencia: {str(e)}")
        return False