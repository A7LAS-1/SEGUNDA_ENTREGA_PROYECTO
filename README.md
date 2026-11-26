# Proyecto del Segundo Parcial — Bases de Datos

**Unidad de Aprendizaje:** Bases de Datos  
**Plan de Estudios:** Ingeniería en Sistemas Computacionales (2020)  
**Institución:** Escuela Superior de Cómputo (ESCOM) - IPN  

---

## Entregables del Segundo Parcial

### 1. Proyecto Propio (Sistema de Seguros de Auto)
* **Aplicación Web:** [`index.html`](index.html) (copia en [`web/index.html`](web/index.html)) — Ejecutable localmente con `docker compose up -d` (API en `http://localhost:8000`) o mediante túnel HTTPS (`cloudflared`).
* **Documentación Partes 1 a 3 (Registro, Conexión, Esquema e Integridad):** [`proyecto-propio-parte-1-3.md`](proyecto-propio-parte-1-3.md)
* **Esquema y Modelos:** [`SQL/esquema.sql`](SQL/esquema.sql), [`PROYECTO-PROPIO/MODELO_RELACIONAL.pdf`](PROYECTO-PROPIO/MODELO_RELACIONAL.pdf), [`PROYECTO-PROPIO/Diccionario_de_Datos.pdf`](PROYECTO-PROPIO/Diccionario_de_Datos.pdf)
* **Backend y Scripts:** [`BACKEND/main.py`](BACKEND/main.py), [`practica4/migraciones/`](practica4/migraciones/), [`practica5/sql/`](practica5/sql/), [`practica4/poblar/poblar.sh`](practica4/poblar/poblar.sh)
* **Evidencia de Registro y Ejecución:** [`EVIDENCIAS/logs_ejecucion.md`](EVIDENCIAS/logs_ejecucion.md)
* **Práctica Integrada (6, 7 y 8):** `normalizacion.md`, `algebra.md` y grupo de RelaX *(en integración)*.

### 2. Proyecto Asignado (Sismos — DWSismos / Seismic Data Visualization System)
* **Repositorio del Proyecto:** `https://github.com/A7LAS-1/SEGUNDA_ENTREGA_PROYECTO.git` (sistema de referencia: [gabrielhuav/Seismic-Data-Visualization-System](https://github.com/gabrielhuav/Seismic-Data-Visualization-System))
* **Análisis del Esquema e Integridad:** [`PROYECTO-ASIGNADO/Analisis-Esquema.pdf`](PROYECTO-ASIGNADO/Analisis-Esquema.pdf), [`practica4/proyecto-asignado/analisis_sismos.md`](practica4/proyecto-asignado/analisis_sismos.md), [`practica5/integridad-almacen.md`](practica5/integridad-almacen.md)
* **Montaje y Consultas:** [`practica4/proyecto-asignado/poblar_sismos.py`](practica4/proyecto-asignado/poblar_sismos.py), [`practica5/sql/integridad_sismos.sql`](practica5/sql/integridad_sismos.sql)

### 3. Artículo y Exposición
* **Referencia en APA 7:**  
  Hurtado Avilés, G., & Climent Hernández, J. A. (2026). *Cuando México tiembla: la historia contada por los datos*. Azcatl: Revista de Divulgación en Ciencias, Ingeniería e Innovación, Universidad Autónoma Metropolitana. https://doi.org/10.24275/AZC2026E1004  
  *(Manuscrito R3 del proyecto asignado: [Seismic_CG_manuscript_R3.pdf](https://github.com/gabrielhuav/Seismic_Data_Geosciences/blob/main/paper/manuscript/out/Seismic_CG_manuscript_R3.pdf) | [Word](https://github.com/gabrielhuav/Seismic_Data_Geosciences/blob/main/paper/manuscript/out/Seismic_CG_manuscript_R3.docx) | [iThenticate](https://github.com/gabrielhuav/Seismic_Data_Geosciences/blob/main/paper/manuscript/out/ITHENTICATE_R3_05.pdf))*
* **Análisis del Artículo y Dos Propuestas de Mejora:** [`articulo-y-mejoras.md`](articulo-y-mejoras.md)
* **Aportaciones de los Integrantes:** [`practica5/integrantes/`](practica5/integrantes/)

---

## Integrantes del Equipo

* **Bravo Mina Liam Valapai** — [`trabajo-integrante-liam-bravo.md`](practica5/integrantes/trabajo-integrante-liam-bravo.md)
* **Navarro Domínguez Antonio** — [`trabajo-integrante-antonio-navarro.md`](practica5/integrantes/trabajo-integrante-antonio-navarro.md)
* **Ávalos Hernandez Joshua Jasiel** — [`trabajo-integrante-joshua-avalos.md`](practica5/integrantes/trabajo-integrante-joshua-avalos.md)

---

## Información de los Proyectos

* **Proyecto Propio:** Sistema de Seguros de Auto (Base de Datos Transaccional OLTP + API FastAPI + Frontend Web)
* **Proyecto Asignado:** Sistema de Visualización de Datos Sísmicos / DWSismos (Almacén de Datos Dimensional OLAP / Esquema en Estrella)
* **Gestor de Base de Datos:** PostgreSQL 16 (desplegado mediante Docker Compose)

---

## Estructura del Repositorio

```text
.
├── .gitignore                      # Exclusión de carpeta IGNORE/
├── compose.yaml                    # Orquestación Docker: PostgreSQL 16, API FastAPI y Cloudflared
├── index.html                      # Aplicación web principal (Alpine.js + Tailwind)
├── proyecto-propio-parte-1-3.md    # Documentación Proyecto Propio (Registro, Conexión, Esquema/Integridad)
├── articulo-y-mejoras.md           # Documentación Tercera Parte (Resumen de artículo R3 y 2 mejoras)
├── BACKEND/                        # API REST en FastAPI + psycopg3
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── web/                            # Copia estática de la interfaz web
│   └── index.html
├── PROYECTO-PROPIO/                # Artefactos conceptuales y relacionales del Proyecto Propio
│   ├── MODELO_RELACIONAL.pdf
│   ├── Diccionario_de_Datos.pdf
│   ├── Transformacion_Modelo_EER.pdf
│   └── Inventario Modelo EER.pdf
├── PROYECTO-ASIGNADO/              # Análisis conceptual del Proyecto Asignado (Sismos)
│   └── Analisis-Esquema.pdf
├── SQL/
│   └── esquema.sql                 # DDL base generado en Práctica 3
├── practica4/                      # PARTE 1: Práctica 4 (DDL, Dominios, Permisos, Carga ETL)
│   ├── dominios.md                 # Ejercicio 1.1: Diccionario de datos, tipos y dominios
│   ├── fuente.md                   # Ejercicio 1.3: Análisis de fuente de datos (SSRN/FARS/CRSS)
│   ├── pruebas-dominio.md          # Ejercicio 1.5: 10 casos de prueba de violación de restricciones
│   ├── permisos.md                 # Ejercicio 1.6: Gestión de roles, usuarios y matriz de permisos
│   ├── migraciones/
│   │   ├── 001-dominios.sql        # Migración ALTER TABLE: dominios, ENUMs, NOT NULL, DEFAULT, CHECKs
│   │   └── 003-permisos.sql        # Migración DDL para roles (app, consulta, admin) y GRANTs
│   ├── datos/
│   │   ├── fars_crss_sample_10.csv # Muestra cruda extraída (~10 casos para pruebas)
│   │   ├── clean_sample_10.csv     # Muestra procesada y mapeada
│   │   └── datos_prueba.sql        # Inserciones SQL transaccionales (ON CONFLICT DO NOTHING)
│   ├── poblar/
│   │   ├── poblar.sh               # Script de un solo comando para poblar la base de datos
│   │   └── poblar.py               # Script Python transaccional, ordenado, idempotente y con benchmark
│   └── proyecto-asignado/
│       ├── analisis_sismos.md      # Ejercicio 1.7: Análisis de datos, dominios y discrepancias
│       └── poblar_sismos.py        # Población del almacén dimensional de sismos
├── practica5/                      # PARTE 2: Práctica 5 (Integridad Referencial, DML, Transacciones)
│   ├── referencias.md              # Ejercicio 2.1 y 2.2: Inventario de FKs y justificación de acciones
│   ├── pruebas-referenciales.md    # Ejercicio 2.3: Pruebas de CASCADE, RESTRICT, SET NULL y auditoría
│   ├── edicion-de-valores.md       # Ejercicio 2.4: DML avanzado, UPSERT, UPDATE con CASE y transacciones
│   ├── integridad-almacen.md       # Ejercicio 2.5: Análisis de integridad en el almacén de Sismos
│   ├── integrantes/                # Ejercicio 2.6: Trabajo individual firmado por cada integrante
│   │   ├── trabajo-integrante-antonio-navarro.md
│   │   ├── trabajo-integrante-liam-bravo.md
│   │   └── trabajo-integrante-joshua-avalos.md
│   └── sql/
│       ├── 002-referencias.sql     # Migración ALTER TABLE con todas las FKs y acciones referenciales
│       ├── transacciones.sql       # Consultas DML avanzadas, SAVEPOINTs y manejo de errores
│       ├── consultas_integridad.sql# Consultas de verificación que deben retornar 0 filas
│       ├── integridad_sismos.sql   # Pruebas de integridad en almacén asignado
│       ├── navarro_poliza_cliente.sql
│       ├── bravo_poliza_cobertura.sql
│       └── avalos_pago_reclamacion.sql
└── EVIDENCIAS/
    ├── compose.yaml
    └── logs_ejecucion.md           # Trazas de terminal y resultados de ejecución de pruebas
```

---

## Guía de Ejecución Rápida

### 1. Despliegue Completo (PostgreSQL + API FastAPI + Túnel)
```bash
docker compose up -d
```
El servicio `postgres` inicializa automáticamente `SQL/esquema.sql`, las migraciones `001`, `002`, `003` y `datos_prueba.sql` mediante `/docker-entrypoint-initdb.d/`. La API queda disponible en `http://localhost:8000` (verificando estado en `GET /api/health`).

### 2. Ejecución Manual del Esquema Base y Migraciones
Toda modificación al esquema se ejecuta mediante archivos de migración numerados:
```bash
# Variables de conexión (Cero credenciales en el repositorio)
export PGHOST=localhost
export PGPORT=5432
export PGDATABASE=seguros_db
export PGUSER=postgres
export PGPASSWORD=postgres123

# Esquema inicial limpio (Práctica 3)
psql -h $PGHOST -p $PGPORT -U $PGUSER -d $PGDATABASE -f SQL/esquema.sql

# Migración 001: Dominios, tipos personalizados y restricciones CHECK
psql -h $PGHOST -p $PGPORT -U $PGUSER -d $PGDATABASE -f practica4/migraciones/001-dominios.sql

# Migración 002: Claves foráneas y acciones referenciales (ON DELETE / ON UPDATE)
psql -h $PGHOST -p $PGPORT -U $PGUSER -d $PGDATABASE -f practica5/sql/002-referencias.sql

# Migración 003: Roles, usuarios y privilegios
psql -h $PGHOST -p $PGPORT -U $PGUSER -d $PGDATABASE -f practica4/migraciones/003-permisos.sql
```

### 3. Población Automatizada de Datos (Script de un Solo Comando)
El script `poblar.sh` se conecta empleando el rol de aplicación (`app_seguros`), garantizando el principio de menor privilegio:
```bash
# Ejecutar población (idempotente, transaccional, con reporte de filas)
bash practica4/poblar/poblar.sh

# Al ejecutarlo por segunda vez, se verifica que no duplica registros ni termina en error
bash practica4/poblar/poblar.sh
```

### 4. Ejecución de Consultas de Auditoría e Integridad
Para corroborar que la base de datos se encuentra completamente íntegra (0 filas huérfanas, 0 duplicados, 0 violaciones de nulos):
```bash
psql -h $PGHOST -p $PGPORT -U $PGUSER -d $PGDATABASE -f practica5/sql/consultas_integridad.sql
```

### 5. Almacén de Datos Asignado (Sismos)
Para ejecutar la verificación dimensional y la prueba de las tres restricciones de dominio propuestas:
```bash
python3 practica4/proyecto-asignado/poblar_sismos.py
```

---

## Resumen de Decisiones de Diseño

1. **Montos y Precisión:** Se utiliza estrictamente `NUMERIC(12,2)` para cantidades monetarias (primas, montos de reclamación, sumas aseguradas) y nunca punto flotante (`FLOAT`/`REAL`), eliminando errores de redondeo financiero.
2. **Restricciones de Dominio:** Se definieron dominios personalizados (`rfc_mexicano`, `codigo_postal_tipo`, `monto_dinero`) y tipos enumerados (`tipo_vehiculo_enum`, `tipo_transmision_enum`, `tipo_manillar_enum`), junto con más de 10 restricciones `CHECK` que modelan la lógica real de negocio de una aseguradora.
3. **Acciones Referenciales:**
   - `ON DELETE RESTRICT`: Aplicado en relaciones centrales de negocio (`POLIZA -> CLIENTE`, `VEHICULO -> CLIENTE`, `RECLAMACION -> POLIZA`, `PAGO_RECLAMACION -> RECLAMACION`) para preservar la trazabilidad contractual, jurídica y contable.
   - `ON DELETE CASCADE`: Aplicado estrictamente en entidades débiles o tablas puente (`POLIZA_COBERTURA -> POLIZA`, `VEHICULO_ACCIDENTE -> ACCIDENTE`) que carecen de significado sin la entidad padre.
4. **Almacén Dimensional vs. Base Relacional:** Se analizó el esquema en estrella del proyecto asignado (`DWSismos`), explicando por qué los data warehouses omiten claves foráneas físicas en favor del rendimiento en cargas ETL masivas paralelas, y contrastándolo con los riesgos de inconsistencia que ello conlleva.
