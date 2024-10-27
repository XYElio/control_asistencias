import psycopg2
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
import streamlit as st
from urllib.parse import urlparse
from typing import Optional, Any, Union, List, Dict

class DatabaseConnection:
    """
    Clase Singleton para manejar conexiones a PostgreSQL.
    Implementa el patrón Singleton para asegurar una única instancia de conexión.
    """
    _instance = None
    _DATABASE_URL = "postgresql://control_asistencia_owner:cSbo4dq0HTRp@ep-holy-fire-a4907vi1.us-east-1.aws.neon.tech/control_asistencia"

    def __new__(cls) -> 'DatabaseConnection':
        """Implementa el patrón Singleton."""
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.connection = None
        return cls._instance

    def __init__(self):
        """Constructor de la clase."""
        self.connection = None

    def connect(self) -> Optional[psycopg2.extensions.connection]:
        """
        Establece la conexión con la base de datos PostgreSQL.
        
        Returns:
            Optional[psycopg2.extensions.connection]: Conexión a la base de datos o None si hay error
        """
        if not self.connection:
            try:
                url = urlparse(self._DATABASE_URL)
                
                self.connection = psycopg2.connect(
                    dbname=url.path[1:],
                    user=url.username,
                    password=url.password,
                    host=url.hostname,
                    port=url.port or 5432,
                    sslmode='require'
                )
            except Error as e:
                st.error(f"Error de conexión: {str(e)}")
                return None
        return self.connection

    def get_cursor(self, dictionary: bool = True) -> Optional[psycopg2.extensions.cursor]:
        """
        Obtiene un cursor de la base de datos.
        
        Args:
            dictionary (bool): Si True, retorna resultados como diccionarios
        
        Returns:
            Optional[psycopg2.extensions.cursor]: Cursor o None si hay error
        """
        conn = self.connect()
        if conn:
            cursor_factory = RealDictCursor if dictionary else None
            return conn.cursor(cursor_factory=cursor_factory)
        return None

    def execute_query(
        self, 
        query: str, 
        params: Optional[Union[tuple, List, Dict]] = None, 
        commit: bool = False
    ) -> Optional[List]:
        """
        Ejecuta una consulta SQL y opcionalmente hace commit.
        
        Args:
            query (str): Consulta SQL a ejecutar
            params (Optional[Union[tuple, List, Dict]]): Parámetros para la consulta
            commit (bool): Si True, realiza commit después de la consulta
        
        Returns:
            Optional[List]: Resultados de la consulta o None si hay error
        """
        cursor = None
        try:
            cursor = self.get_cursor()
            if not cursor:
                return None
                
            cursor.execute(query, params)
            
            if commit:
                self.connection.commit()
                return True
            
            return cursor.fetchall()
            
        except Error as e:
            st.error(f"Error en la consulta: {str(e)}")
            if commit:
                self.connection.rollback()
            return None
        finally:
            if cursor:
                cursor.close()

    def close(self) -> None:
        """Cierra la conexión a la base de datos."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def __del__(self):
        """Destructor que asegura el cierre de la conexión."""
        self.close()

# Instancia global de la conexión
db = DatabaseConnection()