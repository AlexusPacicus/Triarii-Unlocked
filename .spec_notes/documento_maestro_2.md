DOCUMENTO MAESTRO 2: El Flujo Técnico de la Demo (Guión Visual)
Este es tu mapa de ruta de ejecución ininterrumpida. Todo ocurre dentro del navegador del usuario final, garantizando latencia predecible, inmunidad a caídas de API de terceros y protección absoluta del perímetro.
   [ PASO 1: BRIGHT DATA INGRESS ]
   Fetch de contenido HTML desde una URL pública externa gestionada por Bright Data directo a la memoria local.
                 │
                 ▼
   [ PASO 2: LOBSTER TRAP RISK SIGNALING ]
   Inspección ligera de entrada en JavaScript. Enciende un testigo visual de riesgo en el cliente.
                 │
                 ▼
   [ PASO 3: INFERENCIA PRIVADA LOCAL ]
   El contenido HTML es transmitido hacia el LLM que corre localmente en la pestaña web mediante WebGPU.
                 │
                 ▼
   [ PASO 4: UNSAFE TOOL INVOCATION ]
   The model produces an unsafe tool invocation after processing contaminated external context (Path Traversal).
                 │
                 ▼
   [ PASO 5: PYODIDE WASM CONTAINMENT ]
   El motor local de Pyodide intercepta la estructura JSON en la memoria estanca de la pestaña del navegador.
                 │
                 ▼
   [ PASO 6: FORENSIC UX (HITL) ]
   Bloqueo instantáneo de la interfaz: "CAPABILITY_VIOLATION". Contraste visual entre la regla de la política y el ataque.
                 │
                 ▼
   [ PASO 7: AUDIT LOG CLOSE ]
   Comportamiento complementario de contención defensiva pasiva y generación de registro plano append-only local.