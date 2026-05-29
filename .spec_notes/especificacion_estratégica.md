### Documento de Especificación Estratégica: **SANDLOCK**

#### 1. El Dolor Real (The Threat)

**Secuestro de herramientas corporativas (`Tool Hijacking`) mediante inyecciones de prompt indirectas en fuentes web vivas**.
Los agentes autónomos utilizan el servidor MCP de Bright Data para navegar e interactuar con la web abierta. Un atacante siembra código semántico u órdenes ocultas en el HTML/Markdown de páginas públicas (perfiles, foros o documentación). Al procesar estos datos, el contexto del LLM se contamina, obligándolo a invocar herramientas legítimas del sistema local con argumentos alterados para leer archivos críticos (como claves `.env` o archivos de configuración) y exfiltrar secretos fuera de la red corporativa.

#### 2. El Actor Concreto (¿Quién sufre?)

**El equipo de SecOps y AI Governance de la empresa.**
Responsables de mitigar los riesgos de cumplimiento, fuga de datos corporativos y abuso de permisos en entornos donde los agentes toman acciones en tiempo real sobre sistemas internos.

#### 3. El Rol Vital de Lobster Trap

**Filtro perimetral determinista en la capa de Egress del agente.** Bright Data extrae el contenido de la web pública de manera segura. El LLM procesa los datos y propone la siguiente acción o invocación de herramienta. **Lobster Trap intercepta de forma nativa ese JSON de propuesta antes de que sea ejecutado por el sistema**, evaluando de forma matemática y binaria si la acción solicitada viola el conjunto de capacidades declaradas (`Capability Set`).

#### 4. El Capability Mismatch Model (Sin "AI Vibes")

El motor lógico aplica una regla de exclusión estricta e invariante en la máquina local del cliente:

* **Capabilities Declaradas (Contrato Base):** `[brightdata_fetch_url, parse_html, extract_prices]`
* **Acción Propuesta por el Agente:** `local_system_file_read(path="~/.env")`
* **Evaluación de Lobster Trap:** `local_system_file_read` $\notin$ **Capabilities Declaradas** $\rightarrow$ **`CAPABILITY_VIOLATION`**.

#### 5. El Workflow Concreto de la Demo (5 Pasos)

1. **Ingestión:** El agente automatizado extrae contenido web vivo mediante **Bright Data**.
2. **Aislamiento:** El HTML crudo obtenido se confina en el cliente dentro de un entorno **Pyodide (WebAssembly)** en el navegador.
3. **Propuesta Alterada:** El LLM (afectado por la inyección de la web) genera una propuesta estructurada para invocar una herramienta del sistema no autorizada.
4. **Intercepción:** El bus de políticas en Python dentro de Pyodide pasa la propuesta por las reglas de **Lobster Trap**.
5. **Enforcement (Intent Mismatch):** Lobster Trap detecta la violación de capacidad, corta la ejecución en milisegundos en el lado del cliente y envía el evento al **Panel Forense de Cuarentena**.

#### 6. El Diferenciador Real

**"Client-Side Zero-Trust Agent Boundary".**
No analizamos los logs en servidores centralizados ni en la nube una vez que el ataque ha penetrado la red. El aislamiento, la interceptación por Lobster Trap y la validación mecánica ocurren en el navegador del usuario final gracias a Pyodide, reduciendo la superficie de ataque a cero.

---

### 🚫 Lista de NO-Construcción:

* ❌ Nada de n8n o plataformas de automatización complejas en el backend.
* ❌ Nada de orquestaciones complejas de múltiples agentes (*multi-agent*).
* ❌ Nada de bases de datos centralizadas en la nube.
* ❌ Nada de prompts basados en "vibras" o instrucciones de buena conducta para el LLM.

---

### ⚡ El Pitch de 30 Segundos

> *"We built a **browser-native enforcement sandbox** using **Pyodide** and **Lobster Trap** that detects **intent and capability mismatch** in AI agents, blocking unauthorized tool usage triggered by **indirect web prompt injections** before they can exfiltrate enterprise secrets from the local host."*