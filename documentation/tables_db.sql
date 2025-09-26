-- =========================================================
-- Schema: cert_app_v2 / Modelo Relacional (PostgreSQL)
-- =========================================================

-- --------------------------
-- Genereal tables
-- --------------------------

CREATE TABLE archivos_generales (
    id     INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    indice BYTEA
);

-- --------------------------
-- Core reference tables
-- --------------------------

CREATE TABLE logo_emisor_certificados (
    id      INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    logo    BYTEA
);

CREATE TABLE centro_evaluador (
    id                   INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre               TEXT NOT NULL,
    fecha_creacion       DATE DEFAULT CURRENT_DATE,
    logo_centro_evaluador  BYTEA,                
    cedula               TEXT,
    triptico_derechos BYTEA,               
    id_logo_emisor_cert  INT                  
);

ALTER TABLE centro_evaluador
  ADD CONSTRAINT fk_ce_logo_emisor
    FOREIGN KEY (id_logo_emisor_cert)
    REFERENCES logo_emisor_certificados(id)
    ON UPDATE CASCADE ON DELETE SET NULL;

CREATE TABLE usuario (
    id                    INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    usuario               TEXT NOT NULL UNIQUE,
    contrasena            TEXT NOT NULL,
    fecha_creacion        DATE DEFAULT CURRENT_DATE,
    id_centro_evaluador   INT,                -- FK -> centro_evaluador
    cedula                TEXT,
    firma                 BYTEA,
    nombre                TEXT,
    correo                TEXT
);

ALTER TABLE usuario
  ADD CONSTRAINT fk_usuario_ce
    FOREIGN KEY (id_centro_evaluador)
    REFERENCES centro_evaluador(id)
    ON UPDATE CASCADE ON DELETE SET NULL;

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

CREATE TABLE roles (
    id      INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre  TEXT NOT NULL
);

CREATE TABLE permisos (
    id      INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre  TEXT NOT NULL
);

-- Relación muchos-a-muchos: usuarios ↔ roles
CREATE TABLE roles_usuarios (
    id_usuario INT NOT NULL,
    id_rol     INT NOT NULL,
    PRIMARY KEY (id_usuario, id_rol),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (id_rol)     REFERENCES roles(id)   ON UPDATE CASCADE ON DELETE CASCADE
);

-- Relación muchos-a-muchos: roles ↔ permisos
CREATE TABLE rol_permisos (
    id_rol     INT NOT NULL,
    id_permiso INT NOT NULL,
    PRIMARY KEY (id_rol, id_permiso),
    FOREIGN KEY (id_rol)     REFERENCES roles(id)     
        ON UPDATE CASCADE 
        ON DELETE CASCADE,
    FOREIGN KEY (id_permiso) REFERENCES permisos(id)  
        ON UPDATE CASCADE 
        ON DELETE CASCADE
);




-- --------------------------
-- Catálogo de Estándares
-- --------------------------

CREATE TABLE estandar_de_competencia (
    id                       INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre                   TEXT NOT NULL,
    codigo                   TEXT NOT NULL,
    id_examen_diagnostico    INT,
    fecha_creacion           DATE DEFAULT CURRENT_DATE,
    id_usuario_creador       INT,              -- FK -> usuario
    instrumento_evaluacion   BYTEA,
    plan_evaluacion          BYTEA,
    FOREIGN KEY (id_usuario_creador) REFERENCES usuario(id)
        ON UPDATE CASCADE 
        ON DELETE SET NULL
);

-- Tabla puente: Centro Evaluador ↔ Estándar de Competencia (CE_EC)
CREATE TABLE ce_ec (
    id_ce INT NOT NULL,
    id_ec INT NOT NULL,
    PRIMARY KEY (id_ce, id_ec),
    FOREIGN KEY (id_ce) REFERENCES centro_evaluador(id)       
        ON UPDATE CASCADE 
        ON DELETE CASCADE,
    FOREIGN KEY (id_ec) REFERENCES estandar_de_competencia(id) 
        ON UPDATE CASCADE 
        ON DELETE CASCADE
);


-- --------------------------
-- Proyectos, Grupos
-- --------------------------

CREATE TABLE logos (
    id                         INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    logo_org_certificador     BYTEA
);

CREATE TABLE proyecto (
    id              INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre          VARCHAR,
    fecha_creacion  DATE DEFAULT CURRENT_DATE,
    id_ce           INT,
    id_ec           INT,
    id_logos        INT,
    CONSTRAINT fk_proyecto_logos
        FOREIGN KEY (id_logos) REFERENCES logos(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    CONSTRAINT fk_proyecto_ce_ec
        FOREIGN KEY (id_ce, id_ec) REFERENCES ce_ec(id_ce, id_ec)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE grupo (
    id               INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre           TEXT NOT NULL,
    fecha_creacion   DATE DEFAULT CURRENT_DATE,
    id_proyecto      INT NOT NULL,     -- FK -> proyecto
    FOREIGN KEY (id_proyecto) REFERENCES proyecto(id)
        ON UPDATE CASCADE 
        ON DELETE CASCADE
);

-- --------------------------
-- Candidatos y su proceso
-- --------------------------

CREATE TABLE candidato (
    id               INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    fecha_creacion   DATE DEFAULT CURRENT_DATE,
    nombre           TEXT,
    ap_paterno       TEXT,
    ap_materno       TEXT,
    correo           TEXT UNIQUE,
    curp             BYTEA,
    ine_frente       BYTEA,
    ine_reverso      BYTEA,
    foto             BYTEA,
    firma            BYTEA
);

CREATE TABLE info_proceso_candidato (
    id                       INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_candidato             INT NOT NULL,
    id_grupo                 INT NOT NULL,
    fecha_creacion           DATE DEFAULT CURRENT_DATE,

    portada                          BYTEA,
    carta_recepcion_docs             BYTEA,
    ficha_registro              BYTEA,
    reporte_autenticidad        BYTEA,
    encuesta_satisfaccion       BYTEA,
    cedula_evaluacion           BYTEA,
    portafolio                  BYTEA,
    instrumento_de_evaluacion   BYTEA,
    plan_evaluacion             BYTEA,

    toda_la_documentacion    BOOLEAN DEFAULT FALSE,

    FOREIGN KEY (id_candidato) REFERENCES candidato(id)
        ON UPDATE CASCADE 
        ON DELETE CASCADE,
    FOREIGN KEY (id_grupo)     REFERENCES grupo(id)
        ON UPDATE CASCADE 
        ON DELETE CASCADE
);



