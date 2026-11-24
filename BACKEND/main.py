import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg

app = FastAPI(title="API SegurosAuto ESCOM")

# Permite peticiones desde GitHub Pages y pruebas locales
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringirlo a "https://tu-usuario.github.io"
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

# --- MODELOS DE DATOS (coinciden con los v-model de index.html) ---
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

# --- ENDPOINTS ---
@app.get("/api/health")
def health_check():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/clientes-polizas")
def crear_cliente_poliza(data: ClientePolizaIn):
    try:
        with get_db_connection() as conn:
            # Transacción atómica: si falla POLIZA, se revierte CLIENTE
            with conn.transaction():
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO cliente (id_cliente, rfc, nombre, codigo_postal, ciudad, calle, numero_exterior, colonia)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                        """,
                        (
                            data.id_cliente, data.rfc, data.nombre,
                            data.codigo_postal, data.ciudad, data.calle,
                            data.numero_exterior, data.colonia
                        ),
                    )
                    cur.execute(
                        """
                        INSERT INTO cliente_telefono (id_cliente, telefono)
                        VALUES (%s, %s);
                        """,
                        (data.id_cliente, data.telefono),
                    )
                    cur.execute(
                        """
                        INSERT INTO poliza (num_poliza, id_cliente, cobertura)
                        VALUES (%s, %s, %s);
                        """,
                        (data.num_poliza, data.id_cliente, data.cobertura),
                    )
        return {"message": "Cliente, teléfono y póliza guardados en PostgreSQL", "data": data}
    except psycopg.Error as e:
        raise HTTPException(status_code=400, detail=f"Error de integridad en BD: {e.diag.message_primary or str(e)}")

@app.post("/api/vehiculos")
def crear_vehiculo(data: VehiculoIn):
    try:
        with get_db_connection() as conn:
            with conn.transaction():
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO vehiculo (matricula) VALUES (%s);",
                        (data.matricula,),
                    )
                    if data.tipo_vehiculo == "AUTOMOVIL":
                        cur.execute(
                            """
                            INSERT INTO automovil (matricula, num_puertas, tipo_transmision)
                            VALUES (%s, %s, %s);
                            """,
                            (data.matricula, data.num_puertas, data.tipo_transmision),
                        )
                    elif data.tipo_vehiculo == "MOTOCICLETA":
                        cur.execute(
                            """
                            INSERT INTO motocicleta (matricula, cilindrada_cc, tipo_manillar)
                            VALUES (%s, %s, %s);
                            """,
                            (data.matricula, data.cilindrada_cc, data.tipo_manillar),
                        )
        return {"message": "Vehículo registrado en PostgreSQL", "data": data}
    except psycopg.Error as e:
        raise HTTPException(status_code=400, detail=f"Error de integridad en BD: {e.diag.message_primary or str(e)}")

@app.post("/api/reclamaciones")
def crear_reclamacion(data: ReclamacionIn):
    try:
        with get_db_connection() as conn:
            with conn.transaction():
                with conn.cursor() as cur:
                    # Verifica/inserta el accidente si no existe (ajusta columnas según tu esquema.sql)
                    cur.execute(
                        "INSERT INTO accidente (id_accidente) VALUES (%s) ON CONFLICT (id_accidente) DO NOTHING;",
                        (data.id_accidente,),
                    )
                    cur.execute(
                        """
                        INSERT INTO reclamacion (id_accidente, num_poliza)
                        VALUES (%s, %s) ON CONFLICT DO NOTHING;
                        """,
                        (data.id_accidente, data.num_poliza),
                    )
                    cur.execute(
                        """
                        INSERT INTO pago_reclamacion (id_accidente, num_poliza, num_de_pago, monto)
                        VALUES (%s, %s, %s, %s);
                        """,
                        (data.id_accidente, data.num_poliza, data.num_de_pago, data.monto),
                    )
        return {"message": "Reclamación y pago guardados en PostgreSQL", "data": data}
    except psycopg.Error as e:
        raise HTTPException(status_code=400, detail=f"Error de integridad en BD: {e.diag.message_primary or str(e)}")