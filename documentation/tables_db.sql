CREATE TABLE Centro_evaluador (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR,
    fecha_creacion DATE DEFAULT CURRENT_DATE,
    logo_centro_evaluador BYTEA
);

CREATE TABLE Usuario (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    usuario VARCHAR UNIQUE,
    contrasena VARCHAR,
    fecha_creacion DATE DEFAULT CURRENT_DATE,
    id_centro_evaluador INT REFERENCES Centro_evaluador(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- Trigger: normaliza "usuario" a minúsculas
CREATE OR REPLACE FUNCTION normalizar_usuario()
RETURNS TRIGGER AS $$
BEGIN
    NEW.usuario := LOWER(NEW.usuario);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_normaliza_usuario
BEFORE INSERT OR UPDATE ON Usuario
FOR EACH ROW
EXECUTE FUNCTION normalizar_usuario();


CREATE TABLE Roles (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR
);

CREATE TABLE Permisos (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR
);

CREATE TABLE Roles_usuarios (
    id_usuario INT,
    id_rol INT,
    PRIMARY KEY (id_usuario, id_rol),
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (id_rol) REFERENCES Roles(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Rol_permisos (
    id_rol INT,
    id_permiso INT,
    PRIMARY KEY (id_rol, id_permiso),
    FOREIGN KEY (id_rol) REFERENCES Roles(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (id_permiso) REFERENCES Permisos(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Logos (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    logo_org_certificadora BYTEA,
    logo_emisor_certificados BYTEA
);

CREATE TABLE Estandar_de_competencia (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre TEXT,
    codigo TEXT,
    id_examen_diagnostico INT,
    fecha_creacion DATE DEFAULT CURRENT_DATE,
    id_usuario_creador INT REFERENCES Usuario(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

CREATE TABLE CE_EC (
    id_ce INT,
    id_ec INT,
    PRIMARY KEY (id_ce, id_ec),
    FOREIGN KEY (id_ce) REFERENCES Centro_evaluador(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (id_ec) REFERENCES Estandar_de_competencia(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Proyecto (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR,
    fecha_creacion DATE DEFAULT CURRENT_DATE,
    id_ce INT,
    id_ec INT,
    id_logos INT REFERENCES Logos(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    FOREIGN KEY (id_ce, id_ec) REFERENCES CE_EC(id_ce, id_ec)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Grupo (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR,
    fecha_creacion DATE DEFAULT CURRENT_DATE,
    id_estandar_de_competencia INT,
    id_proyecto INT,
    FOREIGN KEY (id_estandar_de_competencia) REFERENCES Estandar_de_competencia(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    FOREIGN KEY (id_proyecto) REFERENCES Proyecto(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Candidato (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    fecha_creacion DATE DEFAULT CURRENT_DATE,
    nombre VARCHAR,
    ap_paterno VARCHAR,
    ap_materno VARCHAR,
    correo VARCHAR UNIQUE,
    curp VARCHAR,
    foto BYTEA,
    ine BYTEA
);

CREATE TABLE Info_proceso_candidato (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_candidato INT REFERENCES Candidato(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    id_grupo INT REFERENCES Grupo(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    fecha_creacion DATE DEFAULT CURRENT_DATE,
    portada BYTEA,
    indice BYTEA,
    carta_recepcion_docs BYTEA,
    fecha_registro_generado DATE,
    reporte_autenticidad BYTEA,
    triptico_derechos_img BYTEA,
    plan_evaluacion BYTEA,
    encuesta_satisfaccion BYTEA,
    instrumento_evaluacion BYTEA,
    cedula_evaluacion BYTEA
);


