-- ============================================================================
-- Migracion 004: Normalizacion a BCNF (Practica 6, Ejercicio 1.3)
-- Descomposicion de CLIENTE -> CODIGO_POSTAL y VEHICULO -> CATALOGO_MODELO
-- ============================================================================

BEGIN;

-- ----------------------------------------------------------------------------
-- 1. NORMALIZACIoN DE CLIENTE (Eliminacion de codigo_postal -> ciudad)
-- ----------------------------------------------------------------------------

-- 1.1 Crear tabla catalogo CODIGO_POSTAL reutilizando el dominio codigo_postal_tipo
CREATE TABLE IF NOT EXISTS "CODIGO_POSTAL" (
    "codigo_postal" codigo_postal_tipo PRIMARY KEY,
    "ciudad" VARCHAR(100) NOT NULL
);

-- 1.2 Migrar datos existentes desde CLIENTE sin perdida ni duplicados
DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = 'CLIENTE'
          AND column_name = 'ciudad'
    ) THEN
        INSERT INTO "CODIGO_POSTAL" ("codigo_postal", "ciudad")
        SELECT DISTINCT ON ("codigo_postal") "codigo_postal", "ciudad"
        FROM "CLIENTE"
        WHERE "codigo_postal" IS NOT NULL AND "ciudad" IS NOT NULL
        ORDER BY "codigo_postal", "ciudad"
        ON CONFLICT ("codigo_postal") DO NOTHING;
    END IF;
END $$;

-- 1.3 Agregar llave foranea de CLIENTE hacia CODIGO_POSTAL
ALTER TABLE "CLIENTE" DROP CONSTRAINT IF EXISTS "fk_cliente_codigo_postal";
ALTER TABLE "CLIENTE"
    ADD CONSTRAINT "fk_cliente_codigo_postal"
    FOREIGN KEY ("codigo_postal")
    REFERENCES "CODIGO_POSTAL" ("codigo_postal")
    ON UPDATE CASCADE
    ON DELETE RESTRICT
    DEFERRABLE INITIALLY IMMEDIATE;

-- 1.4 Eliminar columna transitiva ciudad de CLIENTE
ALTER TABLE "CLIENTE" DROP COLUMN IF EXISTS "ciudad";


-- ----------------------------------------------------------------------------
-- 2. NORMALIZACIoN DE VEHICULO (Eliminacion de modelo -> marca)
-- ----------------------------------------------------------------------------

-- 2.1 Crear tabla catalogo CATALOGO_MODELO
CREATE TABLE IF NOT EXISTS "CATALOGO_MODELO" (
    "modelo" VARCHAR(50) PRIMARY KEY,
    "marca" VARCHAR(50) NOT NULL
);

-- 2.2 Migrar datos existentes desde VEHICULO sin perdida ni duplicados
DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = 'VEHICULO'
          AND column_name = 'marca'
    ) THEN
        INSERT INTO "CATALOGO_MODELO" ("modelo", "marca")
        SELECT DISTINCT ON ("modelo") "modelo", "marca"
        FROM "VEHICULO"
        WHERE "modelo" IS NOT NULL AND "marca" IS NOT NULL
        ORDER BY "modelo", "marca"
        ON CONFLICT ("modelo") DO NOTHING;
    END IF;
END $$;

-- 2.3 Agregar llave foranea de VEHICULO hacia CATALOGO_MODELO
ALTER TABLE "VEHICULO" DROP CONSTRAINT IF EXISTS "fk_vehiculo_modelo";
ALTER TABLE "VEHICULO"
    ADD CONSTRAINT "fk_vehiculo_modelo"
    FOREIGN KEY ("modelo")
    REFERENCES "CATALOGO_MODELO" ("modelo")
    ON UPDATE CASCADE
    ON DELETE RESTRICT
    DEFERRABLE INITIALLY IMMEDIATE;

-- 2.4 Eliminar columna transitiva marca de VEHICULO
ALTER TABLE "VEHICULO" DROP COLUMN IF EXISTS "marca";

COMMIT;