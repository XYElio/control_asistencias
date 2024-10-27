from conexion import db
from datetime import datetime, time
import streamlit as st
from typing import Dict, Optional, List
import pytz
import streamlit as st

def estilo_jefe():
    """
    Función para aplicar el estilo CSS en la interfaz de registro de asistencia para el jefe de grupo.
    """
    st.markdown("""
    <style>
        /* General */
        body {
            font-family: Arial, sans-serif;
            color: #333;
            background-color: #f4f4f4;
        }

        /* Header y subheader */
        h1, h2, h3, h4 {
            color: #004085;
            font-weight: 600;
        }

        /* Formularios */
        .stForm {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        }

        /* Campos de entrada */
        .stTextInput, .stTextArea, .stSelectbox, .stDateInput, .stTimeInput {
            width: 100%;
            padding: 8px;
            margin-top: 8px;
            margin-bottom: 16px;
            border: 1px solid #ced4da;
            border-radius: 4px;
        }

        /* Botón de envío */
        .stButton > button {
            width: 100%;
            padding: 10px;
            background-color: #483D8B;
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
        }
        .stButton > button:hover {
            background-color: #FFFACD;
        }

        /* Mensajes de éxito y error */
        .stAlert.stAlert-success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
            border-radius: 4px;
        }
        .stAlert.stAlert-error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
            border-radius: 4px;
        }

        /* Información adicional */
        .stMarkdown p {
            font-size: 14px;
            color: #6c757d;
        }
    </style>
    """, unsafe_allow_html=True)


def jefe_grupo(user_data: Dict):
    estilo_jefe()
    """
    Función principal para el registro de asistencia por parte del jefe de grupo
    
    Args:
        user_data (Dict): Datos del jefe de grupo autenticado
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
    """Obtiene el grupo asignado al jefe de grupo"""
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
    """Obtiene las materias y profesores asignados al grupo"""
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
    """Valida si el día actual corresponde a un día programado"""
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
    """Verifica si ya existe un registro de asistencia para la fecha y clase"""
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
    """Registra la asistencia en la base de datos"""
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