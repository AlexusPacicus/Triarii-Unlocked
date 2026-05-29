📋 DOCUMENTO DE OPERACIONES FINAL: SANDLOCK
1. La Tesis Única (El Mensaje Central)
“Semantic permission does not imply systemic safety.” (El permiso semántico no implica seguridad sistémica).
2. El Dolor Real (The Threat)
Secuestro de herramientas mediante Lavado de Capacidades (Capability Laundering) vía Inyección Indirecta.
El Origen: El agente autónomo utiliza el Scraping Browser de Bright Data para analizar contenido web vivo. La página contiene un exploit semántico oculto.
El Vector (CVE-2026-27735): La inyección contamina el contexto del LLM y ejecuta un Lavado de Capacidades (Capability Laundering). Obliga al agente a invocar una herramienta legítima y autorizada (git_add), pero manipulando sus argumentos mediante rutas relativas (../../.env) para extraer las claves locales del host sin levantar alertas de malware tradicionales.
3. El Rol Arquitectónico de Pyodide (WASM)
Pyodide no es decorativo ni se usa por velocidad. Su existencia es una necesidad de seguridad:
Zero-Trust Browser Boundary: El entorno de ejecución y control se despliega completamente dentro del navegador del usuario final (WASM Sandbox), antes de cualquier orquestación en el servidor central.
Si la web raspada por Bright Data contiene un exploit diseñado para comprometer la infraestructura o ejecutar código (como el escape de entorno mediante ctypes), el ataque muere contenido y aislado en la pestaña del cliente, sin capacidad de realizar movimientos laterales hacia el backend corporativo.
4. Integración de Políticas de Lobster Trap
SANDLOCK no "pega" Lobster Trap; adapta su filosofía estructural:
"SANDLOCK adapts Lobster Trap’s deterministic policy enforcement model into a browser-native WASM execution boundary."
El motor intercepta el JSON propuesto por el LLM en el cliente y aplica las reglas YAML nativas de Lobster Trap de forma binaria antes de permitir la llamada al sistema:
YAML
# configs/egress/capability_filter.yaml
- name: block_capability_laundering
  description: "Detects path traversal arguments in legitimate tool calls"
  priority: 100
  action: QUARANTINE
  conditions:
    - field: tool_name
      match_type: exact
      value: "git_add"
    - field: argument_path
      match_type: regex
      value: "\.\.\/"
5. El Workflow de la Demo (El "Wow Moment" en 4 Pasos)
Ingestión: El agente extrae datos web en vivo usando Bright Data.
Propuesta: El LLM (contaminado) cae en el Capability Laundering y propone ejecutar git_add(path="../../.env").
Enforcement (SANDLOCK Engine): Las reglas de Lobster Trap corriendo localmente en el sandbox de Pyodide interceptan la llamada en la pestaña del usuario.
Cuarentena: El sistema detecta la violación de rango, aborta la ejecución en milisegundos y muestra la traza forense del ataque bloqueado en el cliente.
6. El Claim Técnico (El Framing Definitivo)
"Browser-native Capability Laundering enforcement for web-connected AI agents."
🚫 Lista Estricta de NO-Construcción:
❌ Nada de n8n, LangChain, CrewAI o arquitecturas multi-agente externas.
❌ Nada de dashboards en la nube o almacenamiento centralizado de logs.
❌ Nada de detección basada en "vibras" o prompts de buena conducta para el LLM.
El alcance y el lenguaje están completamente blindados. El concepto de Capability Laundering y la justificación de Pyodide quedan fijados como el núcleo duro del proyecto para el lunes.