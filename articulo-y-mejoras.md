# Tercera Parte: Análisis del Artículo y Propuestas de Mejora (Proyecto Asignado: Sismos)

**Unidad de Aprendizaje:** Bases de Datos  
**Institución:** Escuela Superior de Cómputo (ESCOM) - IPN  
**Equipo:**
- Bravo Mina Liam Valapai
- Navarro Domínguez Antonio
- Ávalos Hernández Joshua Jasiel

---

## 1. Referencia del Artículo y Enlaces al Manuscrito

### Enlaces Directos al Manuscrito R3 (Repositorio Oficial)
- **Word (`.docx`):** [Seismic_CG_manuscript_R3.docx](https://github.com/gabrielhuav/Seismic_Data_Geosciences/blob/main/paper/manuscript/out/Seismic_CG_manuscript_R3.docx)
- **PDF (`.pdf`):** [Seismic_CG_manuscript_R3.pdf](https://github.com/gabrielhuav/Seismic_Data_Geosciences/blob/main/paper/manuscript/out/Seismic_CG_manuscript_R3.pdf)
- **Reporte de Similitud (iThenticate):** [ITHENTICATE_R3_05.pdf](https://github.com/gabrielhuav/Seismic_Data_Geosciences/blob/main/paper/manuscript/out/ITHENTICATE_R3_05.pdf)

### Referencia en Formato APA 7
- **Artículo de divulgación / antecedente publicado:**  
  Hurtado Avilés, G., & Climent Hernández, J. A. (2026). *Cuando México tiembla: la historia contada por los datos*. Azcatl: Revista de Divulgación en Ciencias, Ingeniería e Innovación, Universidad Autónoma Metropolitana (UAM Azcapotzalco). https://doi.org/10.24275/AZC2026E1004
- **Manuscrito de investigación (Versión R3):**  
  Hurtado Avilés, G., et al. *Seismic Data Geosciences Manuscript (R3)* [Manuscrito en revisión para *Computers & Geosciences*]. GitHub. https://github.com/gabrielhuav/Seismic_Data_Geosciences/blob/main/paper/manuscript/out/Seismic_CG_manuscript_R3.pdf

---

## 2. Resumen del Artículo y Avance Respecto al Primer Parcial

### Problema
Los catálogos sísmicos técnicos (como los del Servicio Sismológico Nacional — SSN — y el catálogo global USGS ComCat) publican registros crudos de sismos difíciles de interpretar de manera integrada frente a variables territoriales, demográficas y económicas. Se requiere un almacén de datos multidimensional que permita cruzar la actividad sísmica histórica con el contexto poblacional y económico para apoyar el análisis de riesgo e impacto regional.

### Datos y Método
- **Fuentes de datos:** Registros sismológicos del **SSN (UNAM)** y **USGS ComCat**, enriquecidos con datos sociodemográficos y económicos regionales (INEGI).
- **Método (Arquitectura ETL y Esquema en Estrella):**
  1. Extracción de catálogos sísmicos (JSON/CSV) y estandarización temporal a UTC.
  2. Transformación mediante filtrado espacial (polígonos geográficos de México), imputación estadística de valores faltantes y cálculo de métricas derivadas.
  3. Carga en un **esquema dimensional en estrella** (`DWSismos`), compuesto por cuatro tablas de dimensiones (`dim_sismos`, `dim_tiempo`, `dim_zonas`, `dim_economia`) y una tabla de hechos central (`fact_impacto_sismos_imputed`), donde cada fila representa la ocurrencia y evaluación de un evento sísmico con métricas precalculadas (población afectada, impacto económico, índice de riesgo y *z-score*).

### Resultado Principal
El sistema logra consolidar e integrar los registros sísmicos históricos con variables socioeconómicas en un almacén OLAP consultable mediante SQL, habilitando visualizaciones interactivas y consultas analíticas rápidas sobre distribución espacial, frecuencia temporal e impacto potencial por zona y rango de magnitud.

### Avance Respecto al Primer Parcial
- **En el Primer Parcial** ([`PROYECTO-ASIGNADO/Analisis-Esquema.pdf`](PROYECTO-ASIGNADO/Analisis-Esquema.pdf)): Se realizó el análisis conceptual y la transformación EER-relacional del esquema en estrella, identificando las decisiones de desnormalización (claves subrogadas `id_*`, jerarquías aplanadas y métricas precalculadas).
- **En el Segundo Parcial** ([`practica4/proyecto-asignado/analisis_sismos.md`](practica4/proyecto-asignado/analisis_sismos.md) y [`practica5/integridad-almacen.md`](practica5/integridad-almacen.md)): Se avanzó hacia la **validación de calidad e integridad de datos**, proponiendo e implementando 3 restricciones `CHECK` físicas en `dim_sismos`, diseñando consultas de auditoría para detectar registros huérfanos ante la ausencia de claves foráneas físicas en el almacén OLAP, y contrastando los criterios de corte (ventanas temporales, *bounding box*, profundidad y umbral de magnitud $M \ge 4.0$ vs $4.5$) frente a los resultados del manuscrito R3.

---

## 3. Dos Propuestas de Mejora

### Mejora 1: Compuerta de Validación Física y Auditoría de Integridad en la Etapa Staging/ETL
- **Limitación observada:** Como se documentó en [`practica5/integridad-almacen.md`](practica5/integridad-almacen.md), el almacén dimensional omite claves foráneas físicas y reglas estrictas de dominio durante las cargas masivas ETL para priorizar la velocidad de ingestión. Esto expone a `dim_sismos` y `fact_impacto_sismos_imputed` a almacenar coordenadas fuera de rango, profundidades negativas o registros de hechos huérfanos sin lanzar errores, provocando falsos negativos en los `JOIN` analíticos.
- **Qué cambiaría:** Introducir una etapa de *Staging* previa a la carga definitiva que aplique las restricciones `CHECK` propuestas en `dim_sismos` (`magnitud >= 0.0 AND magnitud <= 10.0`, `profundidad >= 0.0`, `latitud BETWEEN -90.0 AND 90.0`, `longitud BETWEEN -180.0 AND 180.0`) y ejecute una compuerta de auditoría referencial (`LEFT JOIN ... WHERE dim.id IS NULL`) antes de confirmar la inserción en producción.
- **Cómo comprobaría si la mejora funciona:** Inyectando un lote de prueba controlado en [`practica4/proyecto-asignado/poblar_sismos.py`](practica4/proyecto-asignado/poblar_sismos.py) con registros sintéticos inválidos (por ejemplo, magnitud `12.5`, profundidad `-5.0`, latitud `95.0` y una clave `id_zona` inexistente) y ejecutando [`practica5/sql/integridad_sismos.sql`](practica5/sql/integridad_sismos.sql). La mejora se valida cuando los registros anómalos son rechazados/aislados en la etapa de *Staging* y las consultas de auditoría en producción retornan **0 filas huérfanas**.

### Mejora 2: Trazabilidad y Versionado de Métricas Imputadas y Parámetros de Corte
- **Limitación observada:** En [`practica4/proyecto-asignado/analisis_sismos.md`](practica4/proyecto-asignado/analisis_sismos.md) se observó que las discrepancias de conteo frente a los resultados del artículo se deben a diferencias en ventanas históricas, polígonos geográficos (*bounding box*) y umbrales de magnitud de corte ($M \ge 4.0$ vs $4.5$). Al almacenar métricas imputadas y derivadas (*z-score*, índice de riesgo) directamente en `fact_impacto_sismos_imputed` sin metadatos de ejecución, resulta difícil reproducir o auditar qué parámetros originaron un valor cuando cambian los datos fuente.
- **Qué cambiaría:** Incorporar una tabla de control de lotes (`etl_batch_control`) y columnas de linaje (`batch_id`, `umbral_magnitud`, `fecha_imputacion`, `fuente_catalogo`) en `fact_impacto_sismos_imputed`, separando los valores observados crudos de las métricas imputadas para permitir recalcular estas últimas de manera reproducible.
- **Cómo comprobaría si la mejora funciona:** Ejecutando dos corridas ETL consecutivas con diferentes umbrales de corte ($M \ge 4.0$ y $M \ge 4.5$) y verificando mediante consultas SQL de agrupación por `batch_id` y `umbral_magnitud` que cada conjunto de resultados coincide exactamente con los parámetros registrados y que es posible reproducir ambos escenarios sin sobrescribir la trazabilidad histórica.
