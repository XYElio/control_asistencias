# Sistema de Registro de Clases para Control de Asistencia Docente
**Reporte Técnico Detallado**

---

## Equipo de Desarrollo
- **Martínez Rodríguez Elio Gabriel**
- **Gómez Ruiz Edwin Elizeo**
- **De la Fuente Alberto Xesus**
- **Contreras Rodríguez Marco Jesus**
- **Cuevas García Nahum Misael**

---

## Introducción
En el contexto de la educación moderna, la necesidad de mantener un registro preciso y eficiente de la asistencia docente es cada vez más crucial. Para responder a esta necesidad, nuestro equipo ha desarrollado un **Sistema de Registro de Clases para Control de Asistencia Docente**, una solución integral que optimiza el proceso de seguimiento de la actividad docente en instituciones educativas.

---

## Identificación del Problema
El proyecto surge de la observación de los retos que enfrentan las instituciones educativas al intentar mantener registros precisos de clases impartidas. Los métodos tradicionales, como el papel o las hojas de cálculo, son propensos a errores y consumen tiempo valioso del personal administrativo.

---

## Objetivos del Sistema
El objetivo principal de este sistema es proporcionar una solución tecnológica intuitiva y eficiente para registrar la asistencia docente, facilitar la generación de reportes y apoyar la toma de decisiones informada en la gestión académica.

---

## Arquitectura del Sistema

### Interfaz de Usuario
La columna vertebral del sistema es una **interfaz de usuario desarrollada con Streamlit**, elegida por su capacidad para crear experiencias web intuitivas y responsivas. Esta interfaz permite a los usuarios principales (jefes de grupo) registrar fácilmente la asistencia diaria de los profesores. Con unos pocos clics, se puede indicar si una clase fue impartida, especificar el profesor y la materia, y añadir observaciones relevantes.

### Almacenamiento de Datos
Para gestionar y almacenar los datos, se utilizó una base de datos **PostgreSQL**, seleccionada por su robustez y simplicidad. La estructura de la base de datos mantiene registros organizados de profesores, materias, carreras y los registros de asistencia, asegurando una integridad de la información y consultas rápidas y eficientes.

---

## Funcionalidades Clave

### Registro de Asistencia
El sistema permite a los usuarios registrar de manera sencilla la asistencia docente. Se realizan validaciones para verificar que el profesor esté activo, que imparta la materia indicada, y que no existan duplicados en los registros.

### Generación de Reportes
Una de las funcionalidades más potentes del sistema es la **generación de reportes detallados**. Los usuarios pueden obtener estadísticas sobre la asistencia de cualquier profesor, el cumplimiento en cualquier materia, o el desempeño global de una carrera. Los reportes incluyen visualizaciones que facilitan la identificación de patrones y tendencias.

### Seguridad y Validación
La seguridad de los datos es prioritaria. El sistema implementa validaciones exhaustivas para asegurar que cada registro sea preciso y legítimo. Además, cada operación se registra en un log del sistema, permitiendo el seguimiento detallado de las actividades.

---

## Desarrollo y Documentación

### Metodología de Desarrollo
El desarrollo siguió una **metodología ágil**, adaptada a nuestras necesidades. El equipo trabajó en iteraciones cortas, enfocándose en la entrega de funcionalidades específicas y utilizables. La retroalimentación constante de los usuarios de prueba ayudó a refinar la interfaz y las funcionalidades del sistema.

### Documentación del Sistema
Para asegurar una documentación técnica precisa y actualizada, utilizamos **pdoc**. Esta herramienta permite generar documentación directamente desde el código fuente, garantizando consistencia con la implementación del sistema.

---

## Retos y Soluciones

### Diseño de Interfaz
Uno de los mayores retos fue diseñar una interfaz accesible para usuarios nuevos, sin sacrificar funcionalidades para usuarios avanzados. La solución fue un diseño por niveles, en el que las funciones básicas están disponibles de inmediato y las avanzadas se pueden acceder fácilmente.

---

## Conclusión
Nuestro **Sistema de Registro de Clases para Control de Asistencia Docente** representa un avance significativo hacia la modernización de la gestión educativa. Al automatizar el proceso de registro, no solo optimizamos el tiempo administrativo, sino que ofrecemos herramientas de análisis útiles para la toma de decisiones informada.

Este proyecto demuestra que la tecnología, aplicada con enfoque centrado en el usuario, puede transformar significativamente los procesos educativos, mejorando la eficiencia administrativa y la calidad de la educación.
