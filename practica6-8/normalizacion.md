# Parte 1. Dependencias funcionales y normalizacion

---

## Ejercicio 1.1. Pautas de diseño

A continuacion se describe la semantica de cada una de las 15 tablas del esquema actual del **Sistema de Seguros de Auto** mediante la oracion *cada fila es...* y se evalua su cumplimiento frente a las cuatro pautas informales de diseño relacional:

1. **Semantica clara:** Los atributos de la tabla describen una unica entidad o relacion bien definida, sin mezclar conceptos independientes.
2. **Sin anomalias de actualizacion:** No existen redundancias que provoquen anomalias de insercion, borrado o modificacion.
3. **Pocos valores nulos:** Los atributos aplican a la gran mayoria de las tuplas sin generar columnas vacias innecesarias.
4. **Sin tuplas espurias:** Al descomponer y reunir tablas mediante reuniones naturales (`NATURAL JOIN`), no se generan combinaciones falsas.

| Tabla | Semantica (Cada fila es...) | Evaluacion contra las 4 pautas y fallas detectadas |
| :--- | :--- | :--- |
| **`CLIENTE`** | Cada fila es un cliente registrado en la aseguradora con su RFC unico, nombre y direccion fiscal. | **Falla Pauta 1 (Semantica clara) y Pauta 2 (Sin anomalias):** Mezcla los datos personales del cliente con la relacion geografica entre `codigo_postal` y `ciudad`. Repite la misma ciudad en todos los clientes de un mismo codigo postal (anomalia de actualizacion y redundancia). Cumple Pautas 3 y 4. |
| **`CLIENTE_TELEFONO`** | Cada fila es un numero telefonico de contacto asociado a un cliente especifico. | **Cumple las 4 pautas:** Semantica atomica de atributo multivaluado, sin nulos (`NOT NULL`), sin redundancia ni tuplas espurias. |
| **`POLIZA`** | Cada fila es un contrato de seguro vigente o historico contratado por un cliente, con su periodo de cobertura y prima total. | **Cumple las 4 pautas:** Todos los atributos describen directamente al contrato identificado por `NUM_POLIZA` y no hay valores nulos. |
| **`COBERTURA`** | Cada fila es un tipo de proteccion o amparo ofrecido por la aseguradora con su descripcion y suma asegurada maxima. | **Cumple las 4 pautas:** Tabla de catalogo limpia, sin nulos y sin dependencias entre atributos no clave. |
| **`POLIZA_COBERTURA`** | Cada fila es la asignacion de una cobertura especifica incluida dentro de una poliza contratada. | **Cumple las 4 pautas:** Implementa correctamente la relacion muchos a muchos entre `POLIZA` y `COBERTURA`. |
| **`ACCIDENTE`** | Cada fila es un siniestro vial reportado con la fecha, lugar y narracion opcional de los hechos. | **Cumple las 4 pautas:** Semantica clara; `descripcion_hechos` admite `NULL` unicamente cuando el reporte inicial aun no tiene narracion detallada, manteniendo pocos nulos. |
| **`VEHICULO`** | Cada fila es un vehiculo registrado en el sistema con su matricula, tipo, marca, modelo comercial y año de fabricacion. | **Falla Pauta 1 (Semantica clara) y Pauta 2 (Sin anomalias):** Mezcla los datos de la unidad fisica (`MATRICULA`, `anio`) con el catalogo comercial de fabricantes (`modelo` $\rightarrow$ `marca`). Si hay 50 vehiculos modelo *Versa*, la marca *Nissan* se repite 50 veces. Cumple Pautas 3 y 4. |
| **`VEHICULO_ACCIDENTE`** | Cada fila es la participacion de un vehiculo especifico dentro de un accidente vial registrado. | **Cumple las 4 pautas:** Tabla de interseccion pura sin atributos redundantes ni nulos. |
| **`AUTOMOVIL`** | Cada fila es la especializacion de un vehiculo de tipo automovil con su numero de puertas y tipo de transmision. | **Cumple las 4 pautas:** Al separar la especializacion de `VEHICULO`, evita dejar columnas nulas en motocicletas (cumple Pauta 3). |
| **`MOTOCICLETA`** | Cada fila es la especializacion de un vehiculo de tipo motocicleta con su cilindrada en centimetros cubicos y tipo de manillar. | **Cumple las 4 pautas:** Evita nulos en automoviles y mantiene semantica exclusiva de motocicletas. |
| **`TALLER`** | Cada fila es un taller mecanico autorizado por la aseguradora con su RFC unico, razon social y especialidad. | **Cumple las 4 pautas:** Cada columna depende exclusivamente de `RFC_TALLER`. |
| **`REPARACION`** | Cada fila es un concepto o catalogo de servicio de reparacion mecanica/hojalateria con su folio, descripcion y costo estimado. | **Cumple las 4 pautas:** Semantica clara y atomica sin anomalias. |
| **`REPARA`** | Cada fila es una orden de servicio ejecutada sobre un vehiculo especifico en un taller autorizado bajo un folio de reparacion y fecha de ingreso. | **Cumple las 4 pautas:** Relacion ternaria bien definida; no genera tuplas espurias al ser una asociacion ternaria indivisible. |
| **`RECLAMACION`** | Cada fila es una solicitud de indemnizacion asociada a un accidente y una poliza bajo un numero de tramite de pago y estado. | **Cumple las 4 pautas:** Todos sus atributos son obligatorios (`NOT NULL`) y describen el estado del tramite especifico. |
| **`PAGO_RECLAMACION`** | Cada fila es una exhibicion o abono monetario individual realizado para liquidar una reclamacion aprobada. | **Cumple las 4 pautas:** Registra cada movimiento financiero con monto exacto (`NUMERIC(12,2)`) y fecha de pago sin redundancias. |

---

## Ejercicio 1.2. Las dependencias funcionales

### 1. Conjunto $F$ de dependencias funcionales (derivadas de las reglas del negocio)

* **`CLIENTE`:**
  * $df_1: \text{ID\_CLIENTE} \to \{\text{rfc}, \text{nombre}, \text{codigo\_postal}, \text{ciudad}, \text{calle}, \text{numero\_exterior}, \text{colonia}\}$ — *Regla de negocio:* Cada cliente registrado recibe un identificador interno unico que determina sus datos fiscales y su domicilio registrado.
  * $df_2: \text{rfc} \to \{\text{ID\_CLIENTE}, \text{nombre}, \text{codigo\_postal}, \text{ciudad}, \text{calle}, \text{numero\_exterior}, \text{colonia}\}$ — *Regla de negocio:* Por legislacion fiscal mexicana (SAT), el RFC es unico por persona fisica o moral y no puede compartirse entre dos clientes (`uq_cliente_rfc`).
  * $df_3: \text{codigo\_postal} \to \text{ciudad}$ — *Regla de negocio:* De acuerdo con el catalogo oficial de SEPOMEX, cada codigo postal de 5 digitos pertenece a una unica ciudad o demarcacion territorial (nota: un codigo postal puede abarcar varias colonias, por lo que $\text{codigo\_postal} \not\to \text{colonia}$).

* **`CLIENTE_TELEFONO`:**
  * $df_4: \{\text{ID\_CLIENTE}, \text{telefono}\} \to \{\text{ID\_CLIENTE}, \text{telefono}\}$ (dependencia trivial; un cliente puede tener varios telefonos y un telefono familiar puede estar asociado a mas de un cliente).

* **`POLIZA`:**
  * $df_5: \text{NUM\_POLIZA} \to \{\text{ID\_CLIENTE}, \text{fecha\_inicio}, \text{fecha\_fin}, \text{prima\_total}\}$ — *Regla de negocio:* Cada numero de poliza es un contrato unico emitido a nombre de un solo titular con vigencia y prima definidas.

* **`COBERTURA`:**
  * $df_6: \text{ID\_COBERTURA} \to \{\text{descripcion}, \text{suma\_asegurada\_max}\}$ — *Regla de negocio:* Cada identificador de cobertura del catalogo corresponde a una unica descripcion de amparo y tope de suma asegurada.

* **`POLIZA_COBERTURA`:**
  * $df_7: \{\text{NUM\_POLIZA}, \text{ID\_COBERTURA}\} \to \{\text{NUM\_POLIZA}, \text{ID\_COBERTURA}\}$ (dependencia trivial; relacion muchos a muchos).

* **`ACCIDENTE`:**
  * $df_8: \text{ID\_ACCIDENTE} \to \{\text{fecha}, \text{lugar}, \text{descripcion\_hechos}\}$ — *Regla de negocio:* Cada folio de siniestro identifica un evento ocurrido en una fecha, lugar y circunstancia especificos.

* **`VEHICULO`:**
  * $df_9: \text{MATRICULA} \to \{\text{tipo\_vehiculo}, \text{marca}, \text{modelo}, \text{anio}\}$ — *Regla de negocio:* La placa o matricula vehicular identifica de manera unica a una unidad fisica con sus caracteristicas de fabricacion.
  * $df_{10}: \text{modelo} \to \text{marca}$ — *Regla de negocio:* En la industria automotriz, cada denominacion comercial de modelo es fabricada por una unica marca (por ejemplo, *Civic* corresponde exclusivamente a *Honda*, *Versa* a *Nissan*).

* **`VEHICULO_ACCIDENTE`:**
  * $df_{11}: \{\text{MATRICULA}, \text{ID\_ACCIDENTE}\} \to \{\text{MATRICULA}, \text{ID\_ACCIDENTE}\}$ (dependencia trivial; relacion muchos a muchos).

* **`AUTOMOVIL`:**
  * $df_{12}: \text{MATRICULA} \to \{\text{num\_puertas}, \text{tipo\_transmision}\}$ — *Regla de negocio:* Un vehiculo registrado como automovil tiene una unica configuracion fisica de puertas y transmision.

* **`MOTOCICLETA`:**
  * $df_{13}: \text{MATRICULA} \to \{\text{cilindrada\_cc}, \text{tipo\_manillar}\}$ — *Regla de negocio:* Una motocicleta registrada tiene una unica cilindrada y tipo de manillar de fabrica.

* **`TALLER`:**
  * $df_{14}: \text{RFC\_TALLER} \to \{\text{nombre}, \text{especialidad}\}$ — *Regla de negocio:* Cada taller en convenio se identifica fiscalmente por su RFC unico, el cual determina su razon social y especialidad tecnica.

* **`REPARACION`:**
  * $df_{15}: \text{FOLIO\_REPARACION} \to \{\text{descripcion}, \text{costo\_estimado}\}$ — *Regla de negocio:* Cada folio de catalogo de reparacion define un trabajo estandarizado con su costo tabulado.

* **`REPARA`:**
  * $df_{16}: \{\text{MATRICULA}, \text{RFC\_TALLER}, \text{FOLIO\_REPARACION}\} \to \text{fecha\_ingreso}$ — *Regla de negocio:* La asignacion de un trabajo de reparacion especifico sobre un vehiculo en un taller determinado ocurre en una fecha de ingreso unica.

* **`RECLAMACION`:**
  * $df_{17}: \{\text{ID\_ACCIDENTE}, \text{NUM\_POLIZA}, \text{NUM\_DE\_PAGO}\} \to \text{estado}$ — *Regla de negocio:* Cada tramite de reclamacion identificado por el siniestro, la poliza afectada y el numero de tramite tiene un unico estado operativo vigente (`PENDIENTE`, `APROBADA`, `PAGADA`, `RECHAZADA` o `CANCELADA`).

* **`PAGO_RECLAMACION`:**
  * $df_{18}: \{\text{ID\_ACCIDENTE}, \text{NUM\_POLIZA}, \text{NUM\_DE\_PAGO}, \text{ID\_PAGO\_REC}\} \to \{\text{monto}, \text{fecha\_pago}\}$ — *Regla de negocio:* Cada abono o exhibicion individual dentro de una reclamacion tiene un monto exacto y una fecha de liquidacion unicos.

---

### 2. Calculo paso a paso del cierre de atributos ($X^+$) y claves candidatas

* **Tabla `CLIENTE` ($R_{\text{CLIENTE}} = \{\text{ID\_CLIENTE}, \text{rfc}, \text{nombre}, \text{codigo\_postal}, \text{ciudad}, \text{calle}, \text{numero\_exterior}, \text{colonia}\}$):**
  1. Probamos $X = \{\text{ID\_CLIENTE}\}$:
     * Inicio: $\{\text{ID\_CLIENTE}\}^+ = \{\text{ID\_CLIENTE}\}$
     * Por $df_1$: $\{\text{ID\_CLIENTE}, \text{rfc}, \text{nombre}, \text{codigo\_postal}, \text{ciudad}, \text{calle}, \text{numero\_exterior}, \text{colonia}\} = R_{\text{CLIENTE}}$
     * Como ningun subconjunto propio lo determina, **$\{\text{ID\_CLIENTE}\}$ es clave candidata**.
  2. Probamos $X = \{\text{rfc}\}$:
     * Inicio: $\{\text{rfc}\}^+ = \{\text{rfc}\}$
     * Por $df_2$: $\{\text{rfc}, \text{ID\_CLIENTE}, \text{nombre}, \text{codigo\_postal}, \text{ciudad}, \text{calle}, \text{numero\_exterior}, \text{colonia}\} = R_{\text{CLIENTE}}$
     * **$\{\text{rfc}\}$ es clave candidata**.
  3. Probamos $X = \{\text{codigo\_postal}\}$:
     * $\{\text{codigo\_postal}\}^+ = \{\text{codigo\_postal}, \text{ciudad}\} \neq R_{\text{CLIENTE}}$ (no es clave).

* **Tabla `VEHICULO` ($R_{\text{VEHICULO}} = \{\text{MATRICULA}, \text{tipo\_vehiculo}, \text{marca}, \text{modelo}, \text{anio}\}$):**
  1. Probamos $X = \{\text{MATRICULA}\}$:
     * Inicio: $\{\text{MATRICULA}\}^+ = \{\text{MATRICULA}\}$
     * Por $df_9$: $\{\text{MATRICULA}, \text{tipo\_vehiculo}, \text{marca}, \text{modelo}, \text{anio}\} = R_{\text{VEHICULO}}$
     * **$\{\text{MATRICULA}\}$ es la unica clave candidata**.
  2. Probamos $X = \{\text{modelo}\}$:
     * $\{\text{modelo}\}^+ = \{\text{modelo}, \text{marca}\} \neq R_{\text{VEHICULO}}$ (no es clave).

* **Resto de las tablas (cierre directo por determinante unico):**
  * `CLIENTE_TELEFONO`: $\{\text{ID\_CLIENTE}, \text{telefono}\}^+ = \{\text{ID\_CLIENTE}, \text{telefono}\}$ $\implies$ Clave candidata: **$\{\text{ID\_CLIENTE}, \text{telefono}\}$**.
  * `POLIZA`: $\{\text{NUM\_POLIZA}\}^+ = \{\text{NUM\_POLIZA}, \text{ID\_CLIENTE}, \text{fecha\_inicio}, \text{fecha\_fin}, \text{prima\_total}\}$ $\implies$ Clave candidata: **$\{\text{NUM\_POLIZA}\}$**.
  * `COBERTURA`: $\{\text{ID\_COBERTURA}\}^+ = \{\text{ID\_COBERTURA}, \text{descripcion}, \text{suma\_asegurada\_max}\}$ $\implies$ Clave candidata: **$\{\text{ID\_COBERTURA}\}$**.
  * `POLIZA_COBERTURA`: $\{\text{NUM\_POLIZA}, \text{ID\_COBERTURA}\}^+ = \{\text{NUM\_POLIZA}, \text{ID\_COBERTURA}\}$ $\implies$ Clave candidata: **$\{\text{NUM\_POLIZA}, \text{ID\_COBERTURA}\}$**.
  * `ACCIDENTE`: $\{\text{ID\_ACCIDENTE}\}^+ = \{\text{ID\_ACCIDENTE}, \text{fecha}, \text{lugar}, \text{descripcion\_hechos}\}$ $\implies$ Clave candidata: **$\{\text{ID\_ACCIDENTE}\}$**.
  * `VEHICULO_ACCIDENTE`: $\{\text{MATRICULA}, \text{ID\_ACCIDENTE}\}^+ = \{\text{MATRICULA}, \text{ID\_ACCIDENTE}\}$ $\implies$ Clave candidata: **$\{\text{MATRICULA}, \text{ID\_ACCIDENTE}\}$**.
  * `AUTOMOVIL`: $\{\text{MATRICULA}\}^+ = \{\text{MATRICULA}, \text{num\_puertas}, \text{tipo\_transmision}\}$ $\implies$ Clave candidata: **$\{\text{MATRICULA}\}$**.
  * `MOTOCICLETA`: $\{\text{MATRICULA}\}^+ = \{\text{MATRICULA}, \text{cilindrada\_cc}, \text{tipo\_manillar}\}$ $\implies$ Clave candidata: **$\{\text{MATRICULA}\}$**.
  * `TALLER`: $\{\text{RFC\_TALLER}\}^+ = \{\text{RFC\_TALLER}, \text{nombre}, \text{especialidad}\}$ $\implies$ Clave candidata: **$\{\text{RFC\_TALLER}\}$**.
  * `REPARACION`: $\{\text{FOLIO\_REPARACION}\}^+ = \{\text{FOLIO\_REPARACION}, \text{descripcion}, \text{costo\_estimado}\}$ $\implies$ Clave candidata: **$\{\text{FOLIO\_REPARACION}\}$**.
  * `REPARA`: $\{\text{MATRICULA}, \text{RFC\_TALLER}, \text{FOLIO\_REPARACION}\}^+ = \{\text{MATRICULA}, \text{RFC\_TALLER}, \text{FOLIO\_REPARACION}, \text{fecha\_ingreso}\}$ $\implies$ Clave candidata: **$\{\text{MATRICULA}, \text{RFC\_TALLER}, \text{FOLIO\_REPARACION}\}$**.
  * `RECLAMACION`: $\{\text{ID\_ACCIDENTE}, \text{NUM\_POLIZA}, \text{NUM\_DE\_PAGO}\}^+ = \{\text{ID\_ACCIDENTE}, \text{NUM\_POLIZA}, \text{NUM\_DE\_PAGO}, \text{estado}\}$ $\implies$ Clave candidata: **$\{\text{ID\_ACCIDENTE}, \text{NUM\_POLIZA}, \text{NUM\_DE\_PAGO}\}$**.
  * `PAGO_RECLAMACION`: $\{\text{ID\_ACCIDENTE}, \text{NUM\_POLIZA}, \text{NUM\_DE\_PAGO}, \text{ID\_PAGO\_REC}\}^+ = \{\text{ID\_ACCIDENTE}, \text{NUM\_POLIZA}, \text{NUM\_DE\_PAGO}, \text{ID\_PAGO\_REC}, \text{monto}, \text{fecha\_pago}\}$ $\implies$ Clave candidata: **$\{\text{ID\_ACCIDENTE}, \text{NUM\_POLIZA}, \text{NUM\_DE\_PAGO}, \text{ID\_PAGO\_REC}\}$**.

---

### 3. Reduccion de $F$ a un conjunto minimo ($F_c$)

#### Paso 1: Lados derechos simples (descomposicion de implicados)
Se eliminan las dependencias triviales ($df_4, df_7, df_{11}$) y se separan todos los lados derechos compuestos en atributos atomicos:
* De $df_1$: $\text{ID\_CLIENTE} \to \text{rfc}$, $\text{ID\_CLIENTE} \to \text{nombre}$, $\text{ID\_CLIENTE} \to \text{codigo\_postal}$, $\text{ID\_CLIENTE} \to \text{ciudad}$, $\text{ID\_CLIENTE} \to \text{calle}$, $\text{ID\_CLIENTE} \to \text{numero\_exterior}$, $\text{ID\_CLIENTE} \to \text{colonia}$.
* De $df_2$: $\text{rfc} \to \text{ID\_CLIENTE}$, $\text{rfc} \to \text{nombre}$, $\text{rfc} \to \text{codigo\_postal}$, $\text{rfc} \to \text{ciudad}$, $\text{rfc} \to \text{calle}$, $\text{rfc} \to \text{numero\_exterior}$, $\text{rfc} \to \text{colonia}$.
* De $df_3$: $\text{codigo\_postal} \to \text{ciudad}$.
* De $df_5$: $\text{NUM\_POLIZA} \to \text{ID\_CLIENTE}$, $\text{NUM\_POLIZA} \to \text{fecha\_inicio}$, $\text{NUM\_POLIZA} \to \text{fecha\_fin}$, $\text{NUM\_POLIZA} \to \text{prima\_total}$.
* De $df_6$: $\text{ID\_COBERTURA} \to \text{descripcion}$, $\text{ID\_COBERTURA} \to \text{suma\_asegurada\_max}$.
* De $df_8$: $\text{ID\_ACCIDENTE} \to \text{fecha}$, $\text{ID\_ACCIDENTE} \to \text{lugar}$, $\text{ID\_ACCIDENTE} \to \text{descripcion\_hechos}$.
* De $df_9$: $\text{MATRICULA} \to \text{tipo\_vehiculo}$, $\text{MATRICULA} \to \text{marca}$, $\text{MATRICULA} \to \text{modelo}$, $\text{MATRICULA} \to \text{anio}$.
* De $df_{10}$: $\text{modelo} \to \text{marca}$.
* De $df_{12}$: $\text{MATRICULA} \to \text{num\_puertas}$, $\text{MATRICULA} \to \text{tipo\_transmision}$.
* De $df_{13}$: $\text{MATRICULA} \to \text{cilindrada\_cc}$, $\text{MATRICULA} \to \text{tipo\_manillar}$.
* De $df_{14}$: $\text{RFC\_TALLER} \to \text{nombre}$, $\text{RFC\_TALLER} \to \text{especialidad}$.
* De $df_{15}$: $\text{FOLIO\_REPARACION} \to \text{descripcion}$, $\text{FOLIO\_REPARACION} \to \text{costo\_estimado}$.
* De $df_{16}$: $\{\text{MATRICULA}, \text{RFC\_TALLER}, \text{FOLIO\_REPARACION}\} \to \text{fecha\_ingreso}$.
* De $df_{17}$: $\{\text{ID\_ACCIDENTE}, \text{NUM\_POLIZA}, \text{NUM\_DE\_PAGO}\} \to \text{estado}$.
* De $df_{18}$: $\{\text{ID\_ACCIDENTE}, \text{NUM\_POLIZA}, \text{NUM\_DE\_PAGO}, \text{ID\_PAGO\_REC}\} \to \text{monto}$, $\{\text{ID\_ACCIDENTE}, \text{NUM\_POLIZA}, \text{NUM\_DE\_PAGO}, \text{ID\_PAGO\_REC}\} \to \text{fecha\_pago}$.

#### Paso 2: Eliminacion de atributos sobrantes en el lado izquierdo
Se revisan todas las dependencias con determinante compuesto ($df_{16}, df_{17}, df_{18}$):
* En $\{\text{MATRICULA}, \text{RFC\_TALLER}, \text{FOLIO\_REPARACION}\} \to \text{fecha\_ingreso}$:
  * $\{\text{RFC\_TALLER}, \text{FOLIO\_REPARACION}\}^+ = \{\text{RFC\_TALLER}, \text{nombre}, \text{especialidad}, \text{FOLIO\_REPARACION}, \text{descripcion}, \text{costo\_estimado}\}$ (no contiene `fecha_ingreso` ni `MATRICULA`).
  * De forma analoga, quitar `RFC_TALLER` o `FOLIO_REPARACION` impide alcanzar `fecha_ingreso`. Ningun atributo sobra.
* En $\{\text{ID\_ACCIDENTE}, \text{NUM\_POLIZA}, \text{NUM\_DE\_PAGO}\} \to \text{estado}$:
  * Ningun subconjunto de 2 atributos determina `estado` segun las reglas del negocio. Ningun atributo sobra.
* En $\{\text{ID\_ACCIDENTE}, \text{NUM\_POLIZA}, \text{NUM\_DE\_PAGO}, \text{ID\_PAGO\_REC}\} \to \text{monto}$ (y `fecha_pago`):
  * Ningun subconjunto propio determina `monto` ni `fecha_pago`. Ningun atributo sobra.

#### Paso 3: Eliminacion de dependencias redundantes (justificadas con cierre)
1. **Eliminacion de $\text{ID\_CLIENTE} \to \text{ciudad}$:**
   * Sea $F' = F_1 - \{\text{ID\_CLIENTE} \to \text{ciudad}\}$.
   * Calculamos $\{\text{ID\_CLIENTE}\}^+_{F'}$:
     * Inicia en $\{\text{ID\_CLIENTE}\}$.
     * Por $\text{ID\_CLIENTE} \to \text{codigo\_postal}$, se agrega `codigo_postal`.
     * Por $\text{codigo\_postal} \to \text{ciudad}$, se agrega `ciudad`.
   * Como `ciudad` $\in \{\text{ID\_CLIENTE}\}^+_{F'}$, la dependencia $\text{ID\_CLIENTE} \to \text{ciudad}$ es **redundante y se elimina**.

2. **Eliminacion de $\text{rfc} \to \text{ciudad}$:**
   * Sea $F'' = F' - \{\text{rfc} \to \text{ciudad}\}$.
   * Calculamos $\{\text{rfc}\}^+_{F''}$:
     * Inicia en $\{\text{rfc}\}$.
     * Por $\text{rfc} \to \text{codigo\_postal}$, se agrega `codigo_postal`.
     * Por $\text{codigo\_postal} \to \text{ciudad}$, se agrega `ciudad`.
   * Como `ciudad` $\in \{\text{rfc}\}^+_{F''}$, la dependencia $\text{rfc} \to \text{ciudad}$ es **redundante y se elimina**.

3. **Eliminacion de implicados duplicados entre claves candidatas (`rfc` $\leftrightarrow$ `ID_CLIENTE`):**
   * Como tenemos $\text{rfc} \to \text{ID\_CLIENTE}$ y $\text{ID\_CLIENTE} \to \text{rfc}$, para cualquier atributo $A \in \{\text{nombre}, \text{codigo\_postal}, \text{calle}, \text{numero\_exterior}, \text{colonia}\}$, en $F''' = F'' - \{\text{rfc} \to A\}$ se cumple:
     * $\{\text{rfc}\}^+_{F'''} = \{\text{rfc}, \text{ID\_CLIENTE}, \text{nombre}, \text{codigo\_postal}, \text{ciudad}, \text{calle}, \text{numero\_exterior}, \text{colonia}\}$.
   * Por lo tanto, se eliminan las 5 dependencias redundantes $\text{rfc} \to \text{nombre}$, $\text{rfc} \to \text{codigo\_postal}$, $\text{rfc} \to \text{calle}$, $\text{rfc} \to \text{numero\_exterior}$ y $\text{rfc} \to \text{colonia}$, conservando $\text{rfc} \to \text{ID\_CLIENTE}$ y $\text{ID\_CLIENTE} \to \text{rfc}$.

4. **Eliminacion de $\text{MATRICULA} \to \text{marca}$:**
   * Sea $F^{(4)} = F''' - \{\text{MATRICULA} \to \text{marca}\}$.
   * Calculamos $\{\text{MATRICULA}\}^+_{F^{(4)}}$:
     * Inicia en $\{\text{MATRICULA}\}$.
     * Por $\text{MATRICULA} \to \text{modelo}$, se agrega `modelo`.
     * Por $\text{modelo} \to \text{marca}$, se agrega `marca`.
   * Como `marca` $\in \{\text{MATRICULA}\}^+_{F^{(4)}}$, la dependencia $\text{MATRICULA} \to \text{marca}$ es **redundante y se elimina**.

---

### 4. Equivalencia con el conjunto $F_{\text{otro}}$ de otro equipo del mismo dominio

Para demostrar equivalencia entre nuestro recubrimiento minimo $F_c$ y el conjunto $F_{\text{otro}}$ entregado por otro equipo que modela el mismo dominio de Seguros de Auto, se verifica la doble contencion de cierres ($F_c \equiv F_{\text{otro}} \iff F_c \subseteq F_{\text{otro}}^+ \land F_{\text{otro}} \subseteq F_c^+$):

* **Caso de intercambio documentado (Equipo par — Dominio Seguros de Auto):**
  * El equipo par modelo el cliente directamente por `rfc` como llave primaria unica (sin llave subrogada `ID_CLIENTE`) y mantuvo la relacion directa $\text{rfc} \to \text{ciudad}$ y $\text{MATRICULA} \to \text{marca}$ sin separar catalogos.
  * **Prueba 1 ($F_{\text{otro}} \subseteq F_c^+$):**
    * Para $(\text{rfc} \to \text{ciudad}) \in F_{\text{otro}}$: calculando $\{\text{rfc}\}^+_{F_c}$ obtenemos $\{\text{rfc}, \text{ID\_CLIENTE}, \text{codigo\_postal}, \text{ciudad}, \dots\}$, por lo que `ciudad` $\in \{\text{rfc}\}^+_{F_c}$.
    * Para $(\text{MATRICULA} \to \text{marca}) \in F_{\text{otro}}$: calculando $\{\text{MATRICULA}\}^+_{F_c}$ obtenemos $\{\text{MATRICULA}, \text{modelo}, \text{marca}, \dots\}$, por lo que `marca` $\in \{\text{MATRICULA}\}^+_{F_c}$.
  * **Prueba 2 ($F_c \subseteq F_{\text{otro}}^+$):**
    * Al incluir la correspondencia biunivoca de identidad del cliente ($\text{ID\_CLIENTE} \leftrightarrow \text{rfc}$), cada dependencia de $F_c$ se deriva por transitividad de $F_{\text{otro}}$.
  * **Conclusion:** Ambos conjuntos generan exactamente el mismo cierre $F_c^+ = F_{\text{otro}}^+$, demostrando que capturan las mismas reglas de negocio.

---

## Ejercicio 1.3. Las formas normales

### 1. Diagnostico de Forma Normal actual por tabla

| Tabla | Forma Normal Actual | Diagnostico formal |
| :--- | :---: | :--- |
| **`CLIENTE`** | **2FN** | Cumple 1FN (valores atomicos) y 2FN (claves candidatas simples `ID_CLIENTE` y `rfc`, sin dependencias parciales). **Viola 3FN y BCNF** por la dependencia transitiva $\text{ID\_CLIENTE} \to \text{codigo\_postal} \to \text{ciudad}$, donde `codigo_postal` no es superclave y `ciudad` no es atributo primo. |
| **`VEHICULO`** | **2FN** | Cumple 1FN y 2FN (clave candidata simple `MATRICULA`). **Viola 3FN y BCNF** por la dependencia transitiva $\text{MATRICULA} \to \text{modelo} \to \text{marca}$, donde `modelo` no es superclave y `marca` no es atributo primo. |
| `CLIENTE_TELEFONO` | **BCNF** | Todos sus atributos forman parte de la unica clave candidata $\{\text{ID\_CLIENTE}, \text{telefono}\}$. |
| `POLIZA` | **BCNF** | unico determinante es `NUM_POLIZA` (superclave). |
| `COBERTURA` | **BCNF** | unico determinante es `ID_COBERTURA` (superclave). |
| `POLIZA_COBERTURA` | **BCNF** | Todos los atributos son primos y forman la clave candidata $\{\text{NUM\_POLIZA}, \text{ID\_COBERTURA}\}$. |
| `ACCIDENTE` | **BCNF** | unico determinante es `ID_ACCIDENTE` (superclave). |
| `VEHICULO_ACCIDENTE` | **BCNF** | Todos los atributos son primos y forman la clave candidata $\{\text{MATRICULA}, \text{ID\_ACCIDENTE}\}$. |
| `AUTOMOVIL` | **BCNF** | unico determinante es `MATRICULA` (superclave). |
| `MOTOCICLETA` | **BCNF** | unico determinante es `MATRICULA` (superclave). |
| `TALLER` | **BCNF** | unico determinante es `RFC_TALLER` (superclave). |
| `REPARACION` | **BCNF** | unico determinante es `FOLIO_REPARACION` (superclave). |
| `REPARA` | **BCNF** | unico determinante no trivial es $\{\text{MATRICULA}, \text{RFC\_TALLER}, \text{FOLIO\_REPARACION}\}$ (superclave). |
| `RECLAMACION` | **BCNF** | unico determinante no trivial es $\{\text{ID\_ACCIDENTE}, \text{NUM\_POLIZA}, \text{NUM\_DE\_PAGO}\}$ (superclave). |
| `PAGO_RECLAMACION` | **BCNF** | unico determinante no trivial es $\{\text{ID\_ACCIDENTE}, \text{NUM\_POLIZA}, \text{NUM\_DE\_PAGO}, \text{ID\_PAGO\_REC}\}$ (superclave). |

---

### 2. Normalizacion a 3FN y comprobacion de BCNF

1. **Descomposicion de `CLIENTE` (eliminando $\text{codigo\_postal} \to \text{ciudad}$):**
   * $R_1 = \text{CODIGO\_POSTAL}(\underline{\text{codigo\_postal}}, \text{ciudad})$
     * Dependencia: $\text{codigo\_postal} \to \text{ciudad}$. El determinante `codigo_postal` es superclave $\implies$ **Cumple 3FN y BCNF**.
   * $R_2 = \text{CLIENTE}(\underline{\text{ID\_CLIENTE}}, \text{rfc}, \text{nombre}, \text{codigo\_postal}, \text{calle}, \text{numero\_exterior}, \text{colonia})$
     * Dependencias: $\text{ID\_CLIENTE} \to \{\text{rfc}, \text{nombre}, \text{codigo\_postal}, \text{calle}, \text{numero\_exterior}, \text{colonia}\}$ y $\text{rfc} \to \text{ID\_CLIENTE}$. Ambos determinantes (`ID_CLIENTE` y `rfc`) son claves candidatas (superclaves) $\implies$ **Cumple 3FN y BCNF**.

2. **Descomposicion de `VEHICULO` (eliminando $\text{modelo} \to \text{marca}$):**
   * $V_1 = \text{CATALOGO\_MODELO}(\underline{\text{modelo}}, \text{marca})$
     * Dependencia: $\text{modelo} \to \text{marca}$. El determinante `modelo` es superclave $\implies$ **Cumple 3FN y BCNF**.
   * $V_2 = \text{VEHICULO}(\underline{\text{MATRICULA}}, \text{tipo\_vehiculo}, \text{modelo}, \text{anio})$
     * Dependencia: $\text{MATRICULA} \to \{\text{tipo\_vehiculo}, \text{modelo}, \text{anio}\}$. El determinante `MATRICULA` es superclave $\implies$ **Cumple 3FN y BCNF**.

**Resultado global:** Las **17 tablas** del esquema normalizado alcanzan **BCNF** sin necesidad de sacrificar ninguna dependencia funcional.

---

### 3. Prueba de reunion sin perdida y preservacion de dependencias

* **Para `CLIENTE` $\to \{R_1(\text{CODIGO\_POSTAL}), R_2(\text{CLIENTE})\}$:**
  * **Reunion sin perdida (prueba de atributos comunes):**
    $$R_1 \cap R_2 = \{\text{codigo\_postal}\}$$
    $$\{\text{codigo\_postal}\}^+ = \{\text{codigo\_postal}, \text{ciudad}\} = R_1$$
    Dado que $(R_1 \cap R_2) \to R_1$, la interseccion es superclave de $R_1$, lo que garantiza matematicamente que $R_1 \bowtie R_2 = \text{CLIENTE}$ sin generar tuplas espurias.
  * **Preservacion de dependencias:**
    $$F_{R_1} = \{\text{codigo\_postal} \to \text{ciudad}\}$$
    $$F_{R_2} = \{\text{ID\_CLIENTE} \to \{\text{rfc}, \text{nombre}, \text{codigo\_postal}, \text{calle}, \text{numero\_exterior}, \text{colonia}\},\; \text{rfc} \to \text{ID\_CLIENTE}\}$$
    Se cumple $(F_{R_1} \cup F_{R_2})^+ = F_{\text{CLIENTE}}^+$; todas las dependencias se verifican localmente sin necesidad de hacer `JOIN`.

* **Para `VEHICULO` $\to \{V_1(\text{CATALOGO\_MODELO}), V_2(\text{VEHICULO})\}$:**
  * **Reunion sin perdida (prueba de atributos comunes):**
    $$V_1 \cap V_2 = \{\text{modelo}\}$$
    $$\{\text{modelo}\}^+ = \{\text{modelo}, \text{marca}\} = V_1$$
    Dado que $(V_1 \cap V_2) \to V_1$, la interseccion es superclave de $V_1$, garantizando que $V_1 \bowtie V_2 = \text{VEHICULO}$ sin perdida de informacion.
  * **Preservacion de dependencias:**
    $$F_{V_1} = \{\text{modelo} \to \text{marca}\}, \quad F_{V_2} = \{\text{MATRICULA} \to \{\text{tipo\_vehiculo}, \text{modelo}, \text{anio}\}\}$$
    Se cumple $(F_{V_1} \cup F_{V_2})^+ = F_{\text{VEHICULO}}^+$; todas las dependencias quedan preservadas.

---

### 4. Implementacion mediante migracion numerada

La descomposicion se aplico directamente sobre la base poblada mediante el archivo `practica6-8/migraciones/004-normalizacion.sql`, creando los catalogos `CODIGO_POSTAL` y `CATALOGO_MODELO`, transfiriendo los registros unicos existentes con `INSERT INTO ... SELECT DISTINCT ON`, enlazando las llaves foraneas y eliminando las columnas redundantes `ciudad` y `marca` sin perdida de registros.