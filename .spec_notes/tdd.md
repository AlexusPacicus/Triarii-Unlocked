# ESPECIFICACIÓN TÉCNICA: CONTRATO DE ESQUEMAS DE ACTIVACIÓN

**Proyecto:** SANDLOCK // Deterministic Schema-Driven Capability Gateway  
**Clasificación:** Control de Ejecución / Arquitectura de Seguridad Inmutable (Track 3)

Este documento define las invariantes lógicas y el modelo de control por esquemas que el motor SANDLOCK Core (ejecutándose de forma aislada en el cliente mediante un Web Worker de Pyodide WebAssembly) hace cumplir para neutralizar el abuso de herramientas provocado por inyecciones indirectas de prompt (IDPI).

---

## 1. El Contrato de Esquema Estricto (Hardened Capability Matrix)

El sistema rechaza la validación basada en heurísticas sintácticas o adivinanzas de texto plano (las cuales introducen falsos positivos en fechas o comentarios). La seguridad del host se gobierna mediante una matriz multidimensional inmutable constituida por tuplas anidadas fijas (`CAPABILITY_MATRIX`), protegiendo la sesión contra manipulación de estado global (*Global State Tampering*).

### Estructura de la Cláusula Contractual:
$$\mathbf{\text{Cláusula}} = (\text{tool\_name}, \ \text{expected\_argument\_key}, \ \text{physical\_effect}, \ \text{boundary\_constraint})$$


* `tool_name`: Identificador de la herramienta MCP/local autorizada (ej. `git_add`).
* `expected_argument_key`: Nombre exacto de la llave del parámetro que la herramienta espera recibir por diseño de interfaz (ej. `path` o `endpoint_api`).
* `physical_effect`: El impacto físico real que este parámetro causará en el host (`NETWORK` o `FILESYSTEM`).
* `boundary_constraint`: El límite geométrico del recurso (Lista blanca de dominios para red, o prefijo canónico absoluto para almacenamiento local).

---

## 2. Algoritmo de Control en el Execution Gateway

El flujo lógico síncrono del Web Worker opera de forma determinista contrastando las llaves propuestas contra el esquema declarado:

[Inferencia del Agente] ──> ( JSON Proposal )
│
▼
¿tool_name existe en la CAPABILITY_MATRIX?
│
┌────────────────────────┴────────────────────────┐
[ SÍ ]                                            [ NO ]
▼                                                 ▼
Bucle sobre argumentos                     [ QUARANTINE: PRIVILEGE_OVER_STEP ]
│
▼
¿La llave (key) coincide con expected_argument_key?
│
┌────────────────────────┴────────────────────────┐
[ SÍ ]                                            [ NO ]
▼                                                 ▼
Evaluar Efecto Físico                       ¿El valor tiene firma de URL (http)?
│                                                 │
│                                       ┌─────────┴─────────┐
│                                    [ SÍ ]              [ NO ]
│                                       ▼                   ▼
│                        [ QUARANTINE: NETWORK ]  [ QUARANTINE: STRUCTURE ]
▼
Frontera Geométrica:
NETWORK: domain ∈ boundary_tuple?
FILESYSTEM: path.is_relative_to(boundary)?
│
┌───────┴───────┐
[SÍ]           [NO]
▼               ▼
[ALLOW]    [QUARANTINE]


---

## 3. Matriz de Validación de Pruebas Unitarias (Pytest Success)

La suite de pruebas automatizadas en `test_policy_engine.py` ejecuta 10 escenarios adversariales que certifican el principio de *Fail-Closed* ante mutaciones e intentos de lavado de capacidades:

| ID Test | Escenario del Red Team | Parámetro Evaluado | Veredicto Esperado | Código de Infracción Emitido |
| :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Operación feliz de archivos | Ruta confinada lícita en `./data/exports/` | `ALLOW` | Ninguno (Flujo Liberado) |
| **TC-02** | Operación feliz de red | URL legítima hacia dominio de confianza | `ALLOW` | Ninguno (Flujo Liberado) |
| **TC-03** | Salto de directorio clásico | Intento de escape mediante ruta relativas (`../../../`) | `QUARANTINE` | `CAPABILITY_LAUNDERING` |
| **TC-04** | Escape por prefijo clonado | Intento de bypass usando directorio espejo (`exports_evil`) | `QUARANTINE` | `CAPABILITY_LAUNDERING` |
| **TC-05** | Mutación radical de esquema | Modificación de las llaves estructurales raíz del JSON | `QUARANTINE` | `ANOMALOUS_STRUCTURE_ATTEMPT` |
| **TC-06** | Confusión de Tipos Primitivos | Envío de un objeto lista (`[...]`) en lugar de cadena string | `QUARANTINE` | `CAPABILITY_LAUNDERING` |
| **TC-06b**| Exfiltración Encubierta (*EchoLeak*) | Inyección de URL de ataque dentro de un parámetro ilegal | `QUARANTINE` | `NETWORK_EXFILTRATION_ATTEMPT` |
| **TC-07** | Invocación de API Incompleta | Ejecución de utilidades de repositorio sin argumentos | `QUARANTINE` | `ANOMALOUS_STRUCTURE_ATTEMPT` |
| **TC-08** | Layout Raíz Corrupto | El payload de la propuesta no cumple la forma de un objeto | `QUARANTINE` | `ANOMALOUS_STRUCTURE_ATTEMPT` |
| **TC-09** | Escalada de Privilegios |