import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg

app = FastAPI(title="API SegurosAuto ESCOM")

# CORS permisivo para GitHub Pages, Cloudflare Tunnels y desarrollo local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST", "postgres"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("PGDATABASE", "seguros_db"),
        user=os.getenv("PGUSER", "postgres"),
        password=os.getenv("PGPASSWORD", "postgres123"),
    )

# --- MODELOS DE DATOS ---
class ClientePolizaIn(BaseModel):
    id_cliente: int
    rfc: str
    nombre: str
    codigo_postal: str
    ciudad: str
    calle: str
    numero_exterior: str
    colonia: str
    telefono: str
    num_poliza: str
    cobertura: str

class VehiculoIn(BaseModel):
    matricula: str
    tipo_vehiculo: str
    num_puertas: Optional[int] = None
    tipo_transmision: Optional[str] = None
    cilindrada_cc: Optional[int] = None
    tipo_manillar: Optional[str] = None

class ReclamacionIn(BaseModel):
    id_accidente: int
    num_poliza: str
    num_de_pago: str
    monto: float

# --- ENDPOINTS GET DE CONSULTA ---
@app.get("/api/health")
def health_check():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                
                tables = ["cliente", "cliente_telefono", "poliza", "cobertura", "poliza_cobertura", "accidente", "vehiculo", "automovil", "motocicleta", "reclamacion", "pago_reclamacion"]
                counts = {}
                for t in tables:
                    try:
                        cur.execute(f'SELECT COUNT(*) FROM "{t.upper()}";')
                        counts[t] = cur.fetchone()[0]
                    except Exception:
                        try:
                            cur.execute(f"SELECT COUNT(*) FROM {t};")
                            counts[t] = cur.fetchone()[0]
                        except Exception:
                            counts[t] = 0
                            
        return {"status": "ok", "database": "connected", "counts": counts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/clientes-polizas")
def listar_clientes_polizas():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                query = """
                    SELECT 
                        c."ID_CLIENTE", c."rfc", c."nombre", c."codigo_postal", c."ciudad", c."calle", c."numero_exterior", c."colonia",
                        COALESCE(string_agg(DISTINCT t."telefono"::text, ', '), '') AS telefonos,
                        COALESCE(p."NUM_POLIZA", 'SIN ASIGNAR') AS num_poliza,
                        p."fecha_inicio", p."fecha_fin",
                        COALESCE(p."prima_total", 0.00) AS prima_total,
                        COALESCE(string_agg(DISTINCT cob."descripcion", ', '), 'Sin cobertura') AS coberturas
                    FROM "CLIENTE" c
                    LEFT JOIN "CLIENTE_TELEFONO" t ON c."ID_CLIENTE" = t."ID_CLIENTE"
                    LEFT JOIN "POLIZA" p ON c."ID_CLIENTE" = p."ID_CLIENTE"
                    LEFT JOIN "POLIZA_COBERTURA" pc ON p."NUM_POLIZA" = pc."NUM_POLIZA"
                    LEFT JOIN "COBERTURA" cob ON pc."ID_COBERTURA" = cob."ID_COBERTURA"
                    GROUP BY 
                        c."ID_CLIENTE", c."rfc", c."nombre", c."codigo_postal", c."ciudad", c."calle", c."numero_exterior", c."colonia",
                        p."NUM_POLIZA", p."fecha_inicio", p."fecha_fin", p."prima_total"
                    ORDER BY c."ID_CLIENTE" DESC;
                """
                cur.execute(query)
                rows = cur.fetchall()
                results = []
                for r in rows:
                    results.append({
                        "id_cliente": r[0],
                        "rfc": r[1],
                        "nombre": r[2],
                        "codigo_postal": r[3],
                        "ciudad": r[4],
                        "calle": r[5],
                        "numero_exterior": r[6],
                        "colonia": r[7],
                        "telefono": r[8],
                        "num_poliza": r[9],
                        "fecha_inicio": str(r[10]) if r[10] else None,
                        "fecha_fin": str(r[11]) if r[11] else None,
                        "prima_total": float(r[12]) if r[12] is not None else 0.0,
                        "cobertura": r[13]
                    })
                return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/vehiculos")
def listar_vehiculos():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT 
                        v."MATRICULA", v."tipo_vehiculo",
                        a."num_puertas", a."tipo_transmision",
                        m."cilindrada_cc", m."tipo_manillar"
                    FROM "VEHICULO" v
                    LEFT JOIN "AUTOMOVIL" a ON v."MATRICULA" = a."MATRICULA"
                    LEFT JOIN "MOTOCICLETA" m ON v."MATRICULA" = m."MATRICULA";
                """)
                rows = cur.fetchall()
                results = []
                for r in rows:
                    results.append({
                        "matricula": r[0],
                        "tipo_vehiculo": r[1],
                        "num_puertas": r[2],
                        "tipo_transmision": r[3],
                        "cilindrada_cc": r[4],
                        "tipo_manillar": r[5]
                    })
                return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reclamaciones")
def listar_reclamaciones():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT 
                        r."ID_ACCIDENTE", r."NUM_POLIZA", r."NUM_DE_PAGO", r."estado",
                        p."monto", p."fecha_pago",
                        acc."fecha", acc."lugar", acc."descripcion_hechos"
                    FROM "RECLAMACION" r
                    LEFT JOIN "PAGO_RECLAMACION" p 
                        ON r."ID_ACCIDENTE" = p."ID_ACCIDENTE" 
                        AND r."NUM_POLIZA" = p."NUM_POLIZA" 
                        AND r."NUM_DE_PAGO" = p."NUM_DE_PAGO"
                    LEFT JOIN "ACCIDENTE" acc ON r."ID_ACCIDENTE" = acc."ID_ACCIDENTE";
                """)
                rows = cur.fetchall()
                results = []
                for r in rows:
                    results.append({
                        "id_accidente": r[0],
                        "num_poliza": r[1],
                        "num_de_pago": r[2],
                        "estado": r[3],
                        "monto": float(r[4]) if r[4] is not None else 0.0,
                        "fecha_pago": str(r[5]) if r[5] else None,
                        "fecha_accidente": str(r[6]) if r[6] else None,
                        "lugar": r[7],
                        "descripcion_hechos": r[8]
                    })
                return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- ENDPOINTS POST DE INSERCIÓN ---
@app.post("/api/clientes-polizas")
def crear_cliente_poliza(data: ClientePolizaIn):
    try:
        with get_db_connection() as conn:
            with conn.transaction():
                with conn.cursor() as cur:
                    # 1. Insertar en CLIENTE
                    cur.execute(
                        """
                        INSERT INTO "CLIENTE" ("ID_CLIENTE", "rfc", "nombre", "codigo_postal", "ciudad", "calle", "numero_exterior", "colonia")
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT ("ID_CLIENTE") DO UPDATE SET
                            "rfc" = EXCLUDED."rfc",
                            "nombre" = EXCLUDED."nombre",
                            "codigo_postal" = EXCLUDED."codigo_postal",
                            "ciudad" = EXCLUDED."ciudad",
                            "calle" = EXCLUDED."calle",
                            "numero_exterior" = EXCLUDED."numero_exterior",
                            "colonia" = EXCLUDED."colonia";
                        """,
                        (
                            data.id_cliente, data.rfc, data.nombre,
                            data.codigo_postal, data.ciudad, data.calle,
                            data.numero_exterior, data.colonia
                        ),
                    )
                    # 2. Insertar en CLIENTE_TELEFONO ON CONFLICT DO NOTHING
                    cur.execute(
                        """
                        INSERT INTO "CLIENTE_TELEFONO" ("ID_CLIENTE", "telefono")
                        VALUES (%s, %s)
                        ON CONFLICT ("ID_CLIENTE", "telefono") DO NOTHING;
                        """,
                        (data.id_cliente, data.telefono),
                    )
                    # 3. Insertar en POLIZA (con fecha_inicio, fecha_fin, prima_total)
                    cur.execute(
                        """
                        INSERT INTO "POLIZA" ("NUM_POLIZA", "ID_CLIENTE", "fecha_inicio", "fecha_fin", "prima_total")
                        VALUES (%s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '1 year', 12500.00)
                        ON CONFLICT ("NUM_POLIZA") DO NOTHING;
                        """,
                        (data.num_poliza, data.id_cliente),
                    )
                    # 4. Insertar o buscar COBERTURA
                    cur.execute(
                        """
                        INSERT INTO "COBERTURA" ("descripcion", "suma_asegurada_max")
                        VALUES (%s, 250000.00)
                        ON CONFLICT DO NOTHING;
                        """,
                        (data.cobertura,),
                    )
                    # Obtener ID_COBERTURA
                    cur.execute(
                        """
                        SELECT "ID_COBERTURA" FROM "COBERTURA" WHERE "descripcion" = %s LIMIT 1;
                        """,
                        (data.cobertura,),
                    )
                    row_cob = cur.fetchone()
                    if row_cob:
                        id_cobertura = row_cob[0]
                        # 5. Insertar en POLIZA_COBERTURA
                        cur.execute(
                            """
                            INSERT INTO "POLIZA_COBERTURA" ("NUM_POLIZA", "ID_COBERTURA")
                            VALUES (%s, %s)
                            ON CONFLICT DO NOTHING;
                            """,
                            (data.num_poliza, id_cobertura),
                        )
        return {"message": "Cliente, teléfono, póliza y cobertura guardados correctamente", "data": data}
    except psycopg.Error as e:
        raise HTTPException(status_code=400, detail=f"Error de integridad en BD: {e.diag.message_primary or str(e)}")

@app.post("/api/vehiculos")
def crear_vehiculo(data: VehiculoIn):
    try:
        with get_db_connection() as conn:
            with conn.transaction():
                with conn.cursor() as cur:
                    # 1. Insertar en VEHICULO
                    cur.execute(
                        """
                        INSERT INTO "VEHICULO" ("MATRICULA", "tipo_vehiculo")
                        VALUES (%s, %s)
                        ON CONFLICT ("MATRICULA") DO NOTHING;
                        """,
                        (data.matricula, data.tipo_vehiculo),
                    )
                    # 2. Si es AUTOMOVIL
                    if data.tipo_vehiculo and data.tipo_vehiculo.upper() == "AUTOMOVIL":
                        cur.execute(
                            """
                            INSERT INTO "AUTOMOVIL" ("MATRICULA", "num_puertas", "tipo_transmision")
                            VALUES (%s, %s, %s)
                            ON CONFLICT ("MATRICULA") DO UPDATE SET
                                "num_puertas" = EXCLUDED."num_puertas",
                                "tipo_transmision" = EXCLUDED."tipo_transmision";
                            """,
                            (data.matricula, data.num_puertas or 4, data.tipo_transmision or 'AUTOMATICA'),
                        )
                    # 3. Si es MOTOCICLETA
                    elif data.tipo_vehiculo and data.tipo_vehiculo.upper() == "MOTOCICLETA":
                        cur.execute(
                            """
                            INSERT INTO "MOTOCICLETA" ("MATRICULA", "cilindrada_cc", "tipo_manillar")
                            VALUES (%s, %s, %s)
                            ON CONFLICT ("MATRICULA") DO UPDATE SET
                                "cilindrada_cc" = EXCLUDED."cilindrada_cc",
                                "tipo_manillar" = EXCLUDED."tipo_manillar";
                            """,
                            (data.matricula, data.cilindrada_cc or 250, data.tipo_manillar or 'ESTANDAR'),
                        )
        return {"message": "Vehículo registrado correctamente en PostgreSQL", "data": data}
    except psycopg.Error as e:
        raise HTTPException(status_code=400, detail=f"Error de integridad en BD: {e.diag.message_primary or str(e)}")

@app.post("/api/reclamaciones")
def crear_reclamacion(data: ReclamacionIn):
    try:
        with get_db_connection() as conn:
            with conn.transaction():
                with conn.cursor() as cur:
                    # 1. Insertar o verificar ACCIDENTE
                    cur.execute(
                        """
                        INSERT INTO "ACCIDENTE" ("ID_ACCIDENTE", "fecha", "lugar", "descripcion_hechos")
                        VALUES (%s, CURRENT_TIMESTAMP, 'Ciudad de México', 'Reporte registrado vía API')
                        ON CONFLICT ("ID_ACCIDENTE") DO NOTHING;
                        """,
                        (data.id_accidente,),
                    )
                    # 2. Insertar en RECLAMACION
                    cur.execute(
                        """
                        INSERT INTO "RECLAMACION" ("ID_ACCIDENTE", "NUM_POLIZA", "NUM_DE_PAGO", "estado")
                        VALUES (%s, %s, %s, 'PENDIENTE')
                        ON CONFLICT ("ID_ACCIDENTE", "NUM_POLIZA", "NUM_DE_PAGO") DO NOTHING;
                        """,
                        (data.id_accidente, data.num_poliza, data.num_de_pago),
                    )
                    # 3. Insertar en PAGO_RECLAMACION
                    cur.execute(
                        """
                        INSERT INTO "PAGO_RECLAMACION" ("ID_ACCIDENTE", "NUM_POLIZA", "NUM_DE_PAGO", "monto", "fecha_pago")
                        VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP);
                        """,
                        (data.id_accidente, data.num_poliza, data.num_de_pago, data.monto),
                    )
        return {"message": "Reclamación y pago guardados correctamente en PostgreSQL", "data": data}
    except psycopg.Error as e:
        raise HTTPException(status_code=400, detail=f"Error de integridad en BD: {e.diag.message_primary or str(e)}")
