-- Drop and create database
DROP DATABASE IF EXISTS control_asistencia;
CREATE DATABASE control_asistencia;
USE control_asistencia;

-- Tabla de usuarios 
CREATE TABLE usuarios (
    Usuario VARCHAR(10) PRIMARY KEY,
    Contrasenia VARCHAR(50) NOT NULL,
    Estatus VARCHAR(50) DEFAULT 'activo',
    tipo VARCHAR(50) NOT NULL
);

-- Tabla de jefes_grupo
CREATE TABLE jefes_grupo (
    Usuario VARCHAR(10) PRIMARY KEY,
    Nombre VARCHAR(50) NOT NULL,
    Apellidos VARCHAR(50) NOT NULL,
    Fecha_nacimiento DATE,
    Direccion VARCHAR(100),
    Telefono VARCHAR(100),
    Grupos VARCHAR(10),
    FOREIGN KEY (Usuario) REFERENCES usuarios(Usuario)
);

-- Tabla de profesores
CREATE TABLE profesores (
    Usuario VARCHAR(10) PRIMARY KEY,
    Nombre VARCHAR(50) NOT NULL,
    Apellidos VARCHAR(50) NOT NULL,
    Fecha_nacimiento DATE,
    Direccion VARCHAR(100),
    Telefono VARCHAR(100),
    estatus VARCHAR(20) DEFAULT 'activo',
    fecha_registro DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (Usuario) REFERENCES usuarios(Usuario)
);

-- Tabla de administracion
CREATE TABLE administracion (
    Usuario VARCHAR(10) PRIMARY KEY,
    Nombre VARCHAR(50) NOT NULL,
    Apellidos VARCHAR(50) NOT NULL,
    Fecha_nacimiento DATE,
    Direccion VARCHAR(100),
    Telefono VARCHAR(100),
    FOREIGN KEY (Usuario) REFERENCES usuarios(Usuario)
);

-- Tabla de carreras
CREATE TABLE carreras (
    id_carrera INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    coordinador VARCHAR(100)
);

-- Tabla de materias
CREATE TABLE materias (
    id_materia INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    carrera_id INT,
    FOREIGN KEY (carrera_id) REFERENCES carreras(id_carrera)
);

-- Tabla de profesor_materia
CREATE TABLE profesor_materia (
    id_asignacion INT PRIMARY KEY AUTO_INCREMENT,
    profesor_usuario VARCHAR(10),
    materia_id INT,
    grupo VARCHAR(10) NOT NULL,
    ciclo_escolar VARCHAR(20) NOT NULL,
    FOREIGN KEY (profesor_usuario) REFERENCES profesores(Usuario),
    FOREIGN KEY (materia_id) REFERENCES materias(id_materia)
);
ALTER TABLE profesor_materia
ADD COLUMN dias_semana VARCHAR(100),
ADD COLUMN hora_inicio TIME,
ADD COLUMN hora_fin TIME,
ADD COLUMN aula VARCHAR(20);

-- Tabla de asistencias
CREATE TABLE asistencias (
    id_asistencia INT PRIMARY KEY AUTO_INCREMENT,
    fecha DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    profesor_usuario VARCHAR(10),
    materia_id INT,
    grupo VARCHAR(10) NOT NULL,
    estatus VARCHAR(20) NOT NULL DEFAULT 'impartida',
    observaciones TEXT,
    alumno_id VARCHAR(10),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (profesor_usuario) REFERENCES profesores(Usuario),
    FOREIGN KEY (materia_id) REFERENCES materias(id_materia)
);
