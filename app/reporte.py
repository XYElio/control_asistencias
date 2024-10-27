"""
Sistema de Control de Asistencia
=======================================

Este módulo implementa un sistema de reportes estadísticos para el control de asistencia docente
utilizando Streamlit, Plotly y FPDF. Permite generar visualizaciones y reportes PDF detallados
sobre el cumplimiento de asistencia por profesores, materias y carreras.

Funcionalidades Principales
-------------------------
- Generación de estadísticas de cumplimiento por carrera, profesor y materia
- Visualización de datos mediante gráficas interactivas
- Exportación de reportes detallados en formato PDF
- Interfaz web interactiva con Streamlit

Dependencias
-----------
- streamlit
- pandas
- plotly
- fpdf2
- conexion.db

Funciones de Consulta
-------------------
"""
from conexion import db
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from fpdf import FPDF
import tempfile
from datetime import datetime
import os

def obtener_estadisticas_carrera():
    
    """
    Obtiene estadísticas detalladas de asistencia por carrera desde la base de datos.

    Devuelve
    --------
    lista
        Lista de diccionarios con las siguientes claves:
        - carrera (str): Nombre de la carrera
        - total_clases (int): Total de clases programadas
        - clases_impartidas (int): Total de clases efectivamente impartidas
        - porcentaje_cumplimiento (float): Porcentaje de cumplimiento
    """
    query = """
    SELECT 
        c.nombre as carrera,
        COUNT(a.id_asistencia) as total_clases,
        SUM(CASE WHEN a.estatus = 'impartida' THEN 1 ELSE 0 END) as clases_impartidas,
        CASE 
            WHEN COUNT(a.id_asistencia) = 0 THEN 0
            ELSE ROUND(
                (SUM(CASE WHEN a.estatus = 'impartida' THEN 1 ELSE 0 END) * 100.0) / 
                COUNT(a.id_asistencia), 2
            )
        END as porcentaje_cumplimiento
    FROM carreras c
    LEFT JOIN materias m ON c.id_carrera = m.carrera_id
    LEFT JOIN asistencias a ON m.id_materia = a.materia_id
    GROUP BY c.nombre
    ORDER BY porcentaje_cumplimiento DESC
    """
    return db.execute_query(query)

def obtener_estadisticas_profesor():
    """
    Obtiene estadísticas detalladas de asistencia por profesor desde la base de datos.

    Devuelve
    --------
    lista
        Lista de diccionarios con las siguientes claves:
        - profesor (str): Nombre completo del profesor
        - total_clases (int): Total de clases programadas
        - clases_impartidas (int): Total de clases efectivamente impartidas
        - porcentaje_cumplimiento (float): Porcentaje de cumplimiento
        - total_materias (int): Total de materias asignadas
    """
    query = """
    SELECT 
        CONCAT(p.Nombre, ' ', p.Apellidos) as profesor,
        COUNT(a.id_asistencia) as total_clases,
        SUM(CASE WHEN a.estatus = 'impartida' THEN 1 ELSE 0 END) as clases_impartidas,
        CASE 
            WHEN COUNT(a.id_asistencia) = 0 THEN 0
            ELSE ROUND(
                (SUM(CASE WHEN a.estatus = 'impartida' THEN 1 ELSE 0 END) * 100.0) / 
                COUNT(a.id_asistencia), 2
            )
        END as porcentaje_cumplimiento,
        COUNT(DISTINCT m.id_materia) as total_materias
    FROM profesores p
    LEFT JOIN asistencias a ON p.Usuario = a.profesor_usuario
    LEFT JOIN materias m ON a.materia_id = m.id_materia
    WHERE p.estatus = 'activo'
    GROUP BY p.Usuario, p.Nombre, p.Apellidos
    ORDER BY porcentaje_cumplimiento DESC
    """
    return db.execute_query(query)

def obtener_estadisticas_materia():
    """
    Obtiene estadísticas detalladas de asistencia por materia desde la base de datos.

    Devuelve
    --------
    lista
        Lista de diccionarios con las siguientes claves:
        - materia (str): Nombre de la materia
        - carrera (str): Nombre de la carrera a la que pertenece
        - total_profesores (int): Número de profesores que imparten la materia
        - total_clases (int): Total de clases programadas
        - clases_impartidas (int): Total de clases efectivamente impartidas
        - porcentaje_cumplimiento (float): Porcentaje de cumplimiento
    """
    query = """
    SELECT 
        m.nombre as materia,
        c.nombre as carrera,
        COUNT(DISTINCT a.profesor_usuario) as total_profesores,
        COUNT(a.id_asistencia) as total_clases,
        SUM(CASE WHEN a.estatus = 'impartida' THEN 1 ELSE 0 END) as clases_impartidas,
        CASE 
            WHEN COUNT(a.id_asistencia) = 0 THEN 0
            ELSE ROUND(
                (SUM(CASE WHEN a.estatus = 'impartida' THEN 1 ELSE 0 END) * 100.0) / 
                COUNT(a.id_asistencia), 2
            )
        END as porcentaje_cumplimiento
    FROM materias m
    LEFT JOIN carreras c ON m.carrera_id = c.id_carrera
    LEFT JOIN asistencias a ON m.id_materia = a.materia_id
    GROUP BY m.id_materia, m.nombre, c.nombre
    ORDER BY porcentaje_cumplimiento DESC
    """
    return db.execute_query(query)

def crear_grafica_carreras(df):
    """
    Crea una gráfica de barras horizontales para visualizar estadísticas por carrera.

    Parámetros
    ----------
    df : pandas.DataFrame
        DataFrame con las estadísticas de carreras

    Devuelve
    --------
    plotly.graph_objects.Figure
        Gráfica de barras horizontales con el porcentaje de cumplimiento por carrera
    """
    fig = go.Figure()
    
    # Asegurar que porcentaje_cumplimiento sea numérico y manejar valores NULL
    df['porcentaje_cumplimiento'] = pd.to_numeric(df['porcentaje_cumplimiento'], errors='coerce').fillna(0)
    
    # Ordenar por porcentaje de cumplimiento
    df = df.sort_values('porcentaje_cumplimiento', ascending=True)
    
    fig.add_trace(go.Bar(
        y=df['carrera'],
        x=df['porcentaje_cumplimiento'],
        text=df['porcentaje_cumplimiento'].apply(lambda x: f'{x:.1f}%'),
        textposition='auto',
        orientation='h',
        marker_color='rgb(55, 83, 109)'
    ))
    
    fig.update_layout(
        title='Porcentaje de Cumplimiento por Carrera',
        xaxis_title='Porcentaje de Cumplimiento',
        yaxis_title='Carrera',
        xaxis_range=[0, 100],
        height=400,
        margin=dict(l=200)
    )
    
    return fig

def crear_grafica_profesores(df):
    """
    Crea una gráfica de barras horizontales para visualizar estadísticas por profesor.

    Parámetros
    ----------
    df : pandas.DataFrame
        DataFrame con las estadísticas de profesores

    Devuelve
    --------
    plotly.graph_objects.Figure
        Gráfica de barras horizontales con el porcentaje de cumplimiento por profesor
    """
    fig = go.Figure()
    
    # Asegurar que porcentaje_cumplimiento sea numérico y manejar valores NULL
    df['porcentaje_cumplimiento'] = pd.to_numeric(df['porcentaje_cumplimiento'], errors='coerce').fillna(0)
    
    # Ordenar por porcentaje de cumplimiento
    df = df.sort_values('porcentaje_cumplimiento', ascending=True)
    
    fig.add_trace(go.Bar(
        y=df['profesor'],
        x=df['porcentaje_cumplimiento'],
        text=df['porcentaje_cumplimiento'].apply(lambda x: f'{x:.1f}%'),
        textposition='auto',
        orientation='h',
        marker_color='rgb(55, 83, 109)'
    ))
    
    fig.update_layout(
        title='Porcentaje de Cumplimiento por Profesor',
        xaxis_title='Porcentaje de Cumplimiento',
        yaxis_title='Profesor',
        xaxis_range=[0, 100],
        height=600,
        margin=dict(l=200)
    )
    
    return fig

def crear_grafica_materias(df):
    """
    Crea una gráfica de barras horizontales para visualizar estadísticas por materia.

    Parámetros
    ----------
    df : pandas.DataFrame
        DataFrame con las estadísticas de materias

    Devuelve
    --------
    plotly.graph_objects.Figure
        Gráfica de barras horizontales con el porcentaje de cumplimiento por materia
    """
    fig = go.Figure()
    
    # Asegurar que porcentaje_cumplimiento sea numérico y manejar valores NULL
    df['porcentaje_cumplimiento'] = pd.to_numeric(df['porcentaje_cumplimiento'], errors='coerce').fillna(0)
    
    # Ordenar por porcentaje de cumplimiento
    df = df.sort_values('porcentaje_cumplimiento', ascending=True)
    
    fig.add_trace(go.Bar(
        y=df['materia'],
        x=df['porcentaje_cumplimiento'],
        text=df['porcentaje_cumplimiento'].apply(lambda x: f'{x:.1f}%'),
        textposition='auto',
        orientation='h',
        marker_color='rgb(55, 83, 109)'
    ))
    
    fig.update_layout(
        title='Porcentaje de Cumplimiento por Materia',
        xaxis_title='Porcentaje de Cumplimiento',
        yaxis_title='Materia',
        xaxis_range=[0, 100],
        height=500,
        margin=dict(l=200)
    )
    
    return fig

def generar_reporte_pdf(df, tipo_reporte):
    """Genera un reporte PDF mejorado con estadísticas detalladas, gráficos y formato profesional
    Parámetros
    ----------
    df : pandas.DataFrame
        DataFrame con los datos a incluir en el reporte
    tipo_reporte : str
        Tipo de reporte a generar ('Profesores', 'Materias' o 'Carreras')

    Devuelve
    --------
    str
        Ruta temporal del archivo PDF generado
    
    Notas
    -----
    El reporte incluye:
    - Encabezado y pie de página personalizados
    - Resumen general de estadísticas
    - Tabla detallada de datos
    - Notas y observaciones
    - Formato profesional con colores alternados en las tablas
    """
    class PDF(FPDF):
        def header(self):
            # Encabezado
            self.set_font('Arial', 'B', 15)
            self.cell(80)
            self.cell(30, 10, f'Reporte de Asistencia - {tipo_reporte}', 0, 0, 'C')
            self.ln(20)
            
            # Línea separadora
            self.set_draw_color(0, 80, 180)
            self.set_line_width(0.5)
            self.line(10, 28, 200, 28)
        
        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.set_text_color(128)
            self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')
            self.cell(0, 10, f'Generado el {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}', 0, 0, 'R')

    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Información del reporte
    pdf.set_font('Arial', 'B', 12)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 10, 'Resumen General', 1, 1, 'C', fill=True)
    pdf.ln(5)
    
    # Estadísticas generales con formato mejorado
    pdf.set_font('Arial', '', 10)
    
    # Crear tabla de resumen
    estadisticas = [
        ['Total de Registros:', f"{len(df)}"],
        ['Promedio de Cumplimiento:', f"{df['porcentaje_cumplimiento'].mean():.1f}%"],
        ['Máximo Cumplimiento:', f"{df['porcentaje_cumplimiento'].max():.1f}%"],
        ['Mínimo Cumplimiento:', f"{df['porcentaje_cumplimiento'].min():.1f}%"]
    ]
    
    # Agregar estadísticas específicas según el tipo de reporte
    if tipo_reporte == "Profesores":
        estadisticas.extend([
            ['Total de Materias:', f"{df['total_materias'].sum()}"],
            ['Promedio de Materias por Profesor:', f"{df['total_materias'].mean():.1f}"]
        ])
    elif tipo_reporte == "Materias":
        estadisticas.extend([
            ['Total de Profesores:', f"{df['total_profesores'].sum()}"],
            ['Promedio de Profesores por Materia:', f"{df['total_profesores'].mean():.1f}"]
        ])
    
    # Dibujar tabla de resumen
    col_width = 95
    row_height = 8
    for stat in estadisticas:
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(col_width, row_height, stat[0], 1)
        pdf.set_font('Arial', '', 10)
        pdf.cell(col_width, row_height, stat[1], 1)
        pdf.ln()
    
    pdf.ln(10)
    
    # Agregar sección de análisis
    pdf.set_font('Arial', 'B', 12)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 10, 'Análisis Detallado', 1, 1, 'C', fill=True)
    pdf.ln(5)
    
    # Tabla de datos principal
    pdf.set_font('Arial', 'B', 9)
    
    # Calcular ancho de columnas basado en el contenido
    columnas = df.columns
    anchos_columnas = {}
    for col in columnas:
        # Convertir todos los valores a string y encontrar el más largo
        max_length = max(
            len(str(col)),
            df[col].astype(str).apply(len).max()
        )
        anchos_columnas[col] = min(max_length * 2.5, 50)  # Limitar el ancho máximo
    
    # Ajustar anchos si superan el ancho de página
    total_width = sum(anchos_columnas.values())
    if total_width > 190:  # 190 es aproximadamente el ancho útil de la página
        factor = 190 / total_width
        anchos_columnas = {k: v * factor for k, v in anchos_columnas.items()}
    
    # Encabezados de columna con color
    pdf.set_fill_color(55, 83, 109)
    pdf.set_text_color(255, 255, 255)
    for col in columnas:
        pdf.cell(anchos_columnas[col], 10, str(col).title(), 1, 0, 'C', fill=True)
    pdf.ln()
    
    # Datos de la tabla con formato alternado
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', '', 8)
    for i, (_, row) in enumerate(df.iterrows()):
        # Alternar color de fondo para mejor legibilidad
        if i % 2 == 0:
            pdf.set_fill_color(245, 245, 245)
        else:
            pdf.set_fill_color(255, 255, 255)
            
        for col in columnas:
            valor = row[col]
            # Formato especial para porcentajes
            if 'porcentaje' in col.lower():
                valor = f"{float(valor):.1f}%"
            # Formato para números grandes
            elif isinstance(valor, (int, float)):
                valor = f"{valor:,}"
            pdf.cell(anchos_columnas[col], 8, str(valor), 1, 0, 'C', fill=True)
        pdf.ln()
    
    # Agregar notas y observaciones
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 10, 'Notas y Observaciones:', 0, 1)
    pdf.set_font('Arial', '', 9)
    pdf.multi_cell(0, 5, (
        "* Los porcentajes de cumplimiento se calculan sobre el total de clases programadas.\n"
        "* Este reporte es generado automáticamente por el Sistema de Control de Asistencia Docente.\n"
        "* Para cualquier aclaración, favor de contactar al departamento académico."
    ))
    
    # Guardar PDF
    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    pdf.output(temp_pdf.name)
    return temp_pdf.name

def generar_reportes():
    """Función principal para generar y mostrar reportes

    Crea una interfaz web con tres pestañas:
    1. Reporte por Profesor: Estadísticas y métricas de asistencia docente
    2. Reporte por Materia: Análisis de cumplimiento por asignatura
    3. Reporte por Carrera: Visión general del cumplimiento por programa académico
    
    Cada pestaña incluye:
    - Gráfica interactiva de cumplimiento
    - Métricas clave en tiempo real
    - Opción para exportar reporte PDF detallado
    """
    st.title("Sistema de Control de Asistencia Docente")
    st.subheader("Reportes Estadísticos")
    
    # Crear tabs para los diferentes tipos de reportes
    tab_profesores, tab_materias, tab_carreras = st.tabs([
        "👨‍🏫 Reporte por Profesor",
        "📚 Reporte por Materia",
        "🏫 Reporte por Carrera"
    ])
    
    # Tab de Profesores
    with tab_profesores:
        st.subheader("Estadísticas por Profesor")
        datos_profesores = obtener_estadisticas_profesor()
        if datos_profesores:
            df_profesores = pd.DataFrame(datos_profesores)
            fig_profesores = crear_grafica_profesores(df_profesores)
            st.plotly_chart(fig_profesores, use_container_width=True)
            
            # Mostrar métricas
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Profesores", len(df_profesores))
            with col2:
                st.metric("Promedio Cumplimiento", f"{df_profesores['porcentaje_cumplimiento'].mean():.1f}%")
            with col3:
                st.metric("Total Clases", df_profesores['total_clases'].sum())
            
            # Opción para exportar
            if st.button("Exportar Reporte de Profesores"):
                pdf_path = generar_reporte_pdf(df_profesores, "Profesores")
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        "⬇️ Descargar PDF",
                        pdf_file,
                        "reporte_profesores.pdf",
                        "application/pdf"
                    )
                os.unlink(pdf_path)
    
    # Tab de Materias
    with tab_materias:
        st.subheader("Estadísticas por Materia")
        datos_materias = obtener_estadisticas_materia()
        if datos_materias:
            df_materias = pd.DataFrame(datos_materias)
            fig_materias = crear_grafica_materias(df_materias)
            st.plotly_chart(fig_materias, use_container_width=True)
            
            # Mostrar métricas
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Materias", len(df_materias))
            with col2:
                st.metric("Promedio Cumplimiento", f"{df_materias['porcentaje_cumplimiento'].mean():.1f}%")
            with col3:
                st.metric("Total Profesores", df_materias['total_profesores'].sum())
            
            # Opción para exportar
            if st.button("Exportar Reporte de Materias"):
                pdf_path = generar_reporte_pdf(df_materias, "Materias")
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        "⬇️ Descargar PDF",
                        pdf_file,
                        "reporte_materias.pdf",
                        "application/pdf"
                    )
                os.unlink(pdf_path)
    
    # Tab de Carreras
    with tab_carreras:
        st.subheader("Estadísticas por Carrera")
        datos_carreras = obtener_estadisticas_carrera()
        if datos_carreras:
            df_carreras = pd.DataFrame(datos_carreras)
            fig_carreras = crear_grafica_carreras(df_carreras)
            st.plotly_chart(fig_carreras, use_container_width=True)
            
            # Mostrar métricas
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Carreras", len(df_carreras))
            with col2:
                st.metric("Promedio Cumplimiento", f"{df_carreras['porcentaje_cumplimiento'].mean():.1f}%")
            with col3:
                st.metric("Total Clases", df_carreras['total_clases'].sum())
            
            # Opción para exportar
            if st.button("Exportar Reporte de Carreras"):
                pdf_path = generar_reporte_pdf(df_carreras, "Carreras")
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        "⬇️ Descargar PDF",
                        pdf_file,
                        "reporte_carreras.pdf",
                        "application/pdf"
                    )
                os.unlink(pdf_path)

