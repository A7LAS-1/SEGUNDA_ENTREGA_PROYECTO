# Proyecto Propio (Partes 1 a 3): Sistema de Seguros de Auto

**Unidad de Aprendizaje:** Bases de Datos  
**Institución:** Escuela Superior de Cómputo (ESCOM) - IPN  
**Equipo:**
- Bravo Mina Liam Valapai
- Navarro Domínguez Antonio
- Ávalos Hernández Joshua Jasiel

---

## 1. Registro y Verificación en la Base de Datos

La aplicación web ([`index.html`](index.html) / [`web/index.html`](web/index.html)) permite capturar y registrar datos directamente en PostgreSQL (`seguros_db`) mediante tres formularios principales:

1. **Registro de Cliente y Póliza** (`POST /api/clientes-polizas`):
   - **Campos capturados:** `id_cliente`, `rfc`, `nombre`, `codigo_postal`, `ciudad`, `calle`, `numero_exterior`, `colonia`, `telefono`, `num_poliza`, `cobertura`.
   - **Tablas afectadas:** `"CLIENTE"`, `"CLIENTE_TELEFONO"`, `"POLIZA"`, `"COBERTURA"`, `"POLIZA_COBERTURA"`.
2. **Registro de Vehículo** (`POST /api/vehiculos`):
   - **Campos capturados:** `matricula`, `tipo_vehiculo` (`AUTOMOVIL` o `MOTOCICLETA`), y atributos específicos de subtipo (`num_puertas`, `tipo_transmision` para automóvil; `cilindrada_cc`, `tipo_manillar` para motocicleta).
   - **Tablas afectadas:** `"VEHICULO"`, `"AUTOMOVIL"` o `"MOTOCICLETA"`.
3. **Registro de Reclamación y Pago** (`POST /api/reclamaciones`):
   - **Campos capturados:** `id_accidente`, `num_poliza`, `num_de_pago`, `monto`.
   - **Tablas afectadas:** `"ACCIDENTE"`, `"RECLAMACION"`, `"PAGO_RECLAMACION"`.

### Verificación en el Gestor (PostgreSQL)

Para comprobar que el registro de prueba capturado desde la interfaz web se almacenó correctamente y coincide con los datos enviados, se ejecuta `psql` contra el contenedor `postgres-practica4-5`:

```bash
docker exec -it postgres-practica4-5 psql -U postgres -d seguros_db
```

Consultas `SELECT` de verificación por clave primaria o valor identificable:

```sql
-- 1. Verificar Cliente, Teléfono, Póliza y Cobertura por ID_CLIENTE o NUM_POLIZA
SELECT 
    c."ID_CLIENTE", c."rfc", c."nombre", c."codigo_postal", c."ciudad",
    t."telefono", p."NUM_POLIZA", p."fecha_inicio", p."fecha_fin", p."prima_total",
    cob."descripcion" AS cobertura
FROM "CLIENTE" c
LEFT JOIN "CLIENTE_TELEFONO" t ON c."ID_CLIENTE" = t."ID_CLIENTE"
LEFT JOIN "POLIZA" p ON c."ID_CLIENTE" = p."ID_CLIENTE"
LEFT JOIN "POLIZA_COBERTURA" pc ON p."NUM_POLIZA" = pc."NUM_POLIZA"
LEFT JOIN "COBERTURA" cob ON pc."ID_COBERTURA" = cob."ID_COBERTURA"
WHERE c."ID_CLIENTE" = <ID_PRUEBA>; -- o p."NUM_POLIZA" = '<NUM_POLIZA_PRUEBA>'

-- 2. Verificar Vehículo y su subtipo (Automóvil / Motocicleta) por MATRICULA
SELECT 
    v."MATRICULA", v."tipo_vehiculo",
    a."num_puertas", a."tipo_transmision",
    m."cilindrada_cc", m."tipo_manillar"
FROM "VEHICULO" v
LEFT JOIN "AUTOMOVIL" a ON v."MATRICULA" = a."MATRICULA"
LEFT JOIN "MOTOCICLETA" m ON v."MATRICULA" = m."MATRICULA"
WHERE v."MATRICULA" = '<MATRICULA_PRUEBA>';

-- 3. Verificar Reclamación y Pago por clave compuesta
SELECT 
    r."ID_ACCIDENTE", r."NUM_POLIZA", r."NUM_DE_PAGO", r."estado",
    pr."monto", pr."fecha_pago"
FROM "RECLAMACION" r
LEFT JOIN "PAGO_RECLAMACION" pr
    ON r."ID_ACCIDENTE" = pr."ID_ACCIDENTE"
   AND r."NUM_POLIZA" = pr."NUM_POLIZA"
   AND r."NUM_DE_PAGO" = pr."NUM_DE_PAGO"
WHERE r."NUM_POLIZA" = '<NUM_POLIZA_PRUEBA>';
```

---

## 2. Conexión con la Base de Datos

### Flujo de Comunicación Frontend → Backend → PostgreSQL

1. **Interfaz Web (Cliente):**
   - La aplicación estática en [`index.html`](index.html) (desplegable en GitHub Pages o de forma local) utiliza **Alpine.js** y llamadas asíncronas `fetch()` en formato JSON.
   - El campo `apiUrl` permite apuntar tanto a un entorno local (`http://localhost:8000`) como a un túnel HTTPS accesible desde el navegador (`https://*.trycloudflare.com`), configurado en [`compose.yaml`](compose.yaml) mediante el servicio `cloudflared`.
2. **Backend / API REST (`BACKEND/main.py`):**
   - Desarrollado con **FastAPI** (`uvicorn main:app --host 0.0.0.0 --port 8000`) dentro del contenedor `api-seguros-escom` ([`BACKEND/Dockerfile`](BACKEND/Dockerfile)).
   - Configura `CORSMiddleware` para aceptar peticiones desde el navegador alojado en GitHub Pages o localhost.
   - Valida las cargas útiles mediante modelos **Pydantic** (`ClientePolizaIn`, `VehiculoIn`, `ReclamacionIn`) y se conecta a PostgreSQL usando el driver **psycopg** (v3).
   - Expone endpoints de lectura (`GET /api/health`, `GET /api/clientes-polizas`, `GET /api/vehiculos`, `GET /api/reclamaciones`) y escritura (`POST /api/clientes-polizas`, `POST /api/vehiculos`, `POST /api/reclamaciones`).
3. **Configuración Segura de Credenciales:**
   - Las credenciales de la base de datos (`DB_HOST`, `DB_PORT`, `PGDATABASE`, `PGUSER`, `PGPASSWORD`) se configuran **exclusivamente del lado del servidor** mediante variables de entorno en [`compose.yaml`](compose.yaml) y se leen en la función `get_db_connection()` de [`BACKEND/main.py`](BACKEND/main.py). El navegador nunca tiene acceso directo a la base de datos ni a sus credenciales.

---

## 3. Esquema y Reglas de Integridad

### Modelo Relacional y Tablas Intervinientes

El diseño conceptual y relacional actualizado se encuentra documentado en [`PROYECTO-PROPIO/MODELO_RELACIONAL.pdf`](PROYECTO-PROPIO/MODELO_RELACIONAL.pdf) y [`PROYECTO-PROPIO/Diccionario_de_Datos.pdf`](PROYECTO-PROPIO/Diccionario_de_Datos.pdf).

Las tablas que intervienen en el esquema completo (`SQL/esquema.sql`) son:
- **Núcleo de registro de clientes y pólizas:** `CLIENTE`, `CLIENTE_TELEFONO`, `POLIZA`, `COBERTURA`, `POLIZA_COBERTURA`.
- **Vehículos y especialización:** `VEHICULO`, `AUTOMOVIL`, `MOTOCICLETA`.
- **Siniestros, reclamaciones y talleres:** `ACCIDENTE`, `VEHICULO_ACCIDENTE`, `RECLAMACION`, `PAGO_RECLAMACION`, `TALLER`, `REPARACION`, `REPARA`.

### Ubicación de Scripts de Creación, Migración y Carga

| Propósito | Archivo(s) |
| :--- | :--- |
| **Creación del esquema base** | [`SQL/esquema.sql`](SQL/esquema.sql) |
| **Migración 001 (Dominios, ENUMs, CHECK, UNIQUE)** | [`practica4/migraciones/001-dominios.sql`](practica4/migraciones/001-dominios.sql) |
| **Migración 002 (Claves foráneas y acciones referenciales)** | [`practica5/sql/002-referencias.sql`](practica5/sql/002-referencias.sql) |
| **Migración 003 (Roles y privilegios)** | [`practica4/migraciones/003-permisos.sql`](practica4/migraciones/003-permisos.sql) |
| **Datos de prueba y carga ETL** | [`practica4/datos/datos_prueba.sql`](practica4/datos/datos_prueba.sql), [`practica4/poblar/poblar.sh`](practica4/poblar/poblar.sh), [`practica4/poblar/poblar.py`](practica4/poblar/poblar.py) |
| **Orquestación inicial automática** | [`compose.yaml`](compose.yaml) (montaje en `/docker-entrypoint-initdb.d/`) |

### Claves, Restricciones de Dominio e Integridad Referencial

1. **Tipos Enumerados y Dominios (`001-dominios.sql`):**
   - **ENUMs:** `tipo_vehiculo_enum`, `tipo_transmision_enum`, `tipo_manillar_enum`, `rol_usuario_enum`.
   - **Dominios:** `monto_dinero` (`NUMERIC(12,2) >= 0`), `rfc_mexicano`, `codigo_postal_tipo` (5 dígitos), `telefono_tipo` (7–15 dígitos), `matricula_tipo`, `cilindrada_tipo` (`> 0 AND <= 3000`), `num_puertas_tipo` (`IN (2, 3, 4, 5)`).
   - **Restricciones `CHECK` y `UNIQUE`:** `chk_poliza_fechas` (`fecha_fin > fecha_inicio`), `chk_accidente_fecha_pasada`, `chk_vehiculo_anio`, `chk_reclamacion_estado`, `uq_cliente_rfc`, `uq_taller_rfc`.
2. **Acciones Referenciales (`002-referencias.sql`):**
   - Todas las claves foráneas se declaran con `ON UPDATE CASCADE` y `DEFERRABLE INITIALLY IMMEDIATE`.
   - **`ON DELETE RESTRICT`:** Aplicado en relaciones centrales (`POLIZA -> CLIENTE`, `RECLAMACION -> POLIZA`, `PAGO_RECLAMACION -> RECLAMACION`, entre otras) para impedir el borrado accidental de registros con historial contractual, jurídico o contable activo.
   - **`ON DELETE CASCADE`:** Aplicado en entidades débiles o tablas puente (`CLIENTE_TELEFONO -> CLIENTE`, `POLIZA_COBERTURA -> POLIZA`, `AUTOMOVIL / MOTOCICLETA -> VEHICULO`, `VEHICULO_ACCIDENTE -> ACCIDENTE`) que carecen de sentido sin su entidad padre.
3. **Permisos y Principio de Menor Privilegio (`003-permisos.sql`):**
   - `admin_seguros`: Administración total del esquema (`ALL PRIVILEGES`).
   - `app_seguros`: Operaciones transaccionales (`SELECT`, `INSERT`, `UPDATE`, `DELETE` controlado en tablas operativas; usado por el script `poblar.sh`).
   - `consulta_seguros`: Solo lectura (`SELECT`) para auditoría y reportes sin riesgo de alteración.
4. **Transacciones e Idempotencia (`BACKEND/main.py`):**
   - Cada endpoint `POST` envuelve las inserciones múltiples dentro de un bloque transaccional explícito (`with conn.transaction():`). Si alguna restricción de dominio o integridad referencial falla (por ejemplo, una póliza inexistente en `POST /api/reclamaciones`), se ejecuta `ROLLBACK` automático y la API devuelve `HTTP 400` con el detalle del error de PostgreSQL (`e.diag.message_primary`), evitando estados inconsistentes a medias.
   - Se emplea `ON CONFLICT DO UPDATE` / `ON CONFLICT DO NOTHING` para garantizar idempotencia controlada en registros repetidos.
