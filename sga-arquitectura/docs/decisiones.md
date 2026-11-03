# Decisiones arquitectónicas (ADR)

## ADR-01. Monolito modular con API REST y SPA
- **Justificación:** dominio acotado, equipo de 3 a 5 personas, 300 usuarios concurrentes y necesidad de transacciones ACID (RNF-02, 05, 07).
- **Descartado:** microservicios, por complejidad operativa y consistencia eventual sin beneficio a esta escala.
- **Consecuencia:** el escalado es por réplica completa; los límites modulares permiten extraer servicios si hace falta.

## ADR-02. Base de datos relacional PostgreSQL
- **Justificación:** datos relacionales, restricciones de integridad, transacciones, bloqueo de filas, replicación y respaldo continuo (RNF-03, 07, 09).
- **Descartado:** NoSQL, por la falta de integridad referencial y transacciones multi-entidad simples.
- **Consecuencia:** el escalado de escritura es vertical; se mitiga con réplicas de lectura e índices.

## ADR-03. API sin estado con JWT de corta duración, token de refresco y RBAC en el servidor
- **Justificación:** permite balanceo con varias instancias y escalado horizontal (RNF-01, 03, 04).
- **Descartado:** sesiones en memoria del servidor.
- **Consecuencia:** la revocación de tokens requiere una lista de revocación en Redis.

## ADR-04. Transacción con bloqueo de fila en matrícula y bloqueo optimista en notas
- **Justificación:** evita sobrecupo y pérdida de actualizaciones (RNF-07).
- **Descartado:** validar solo en la aplicación, por condiciones de carrera.
- **Consecuencia:** leve contención en picos de matrícula, aceptable al volumen esperado.

## ADR-05. Auditoría como módulo propio con tabla de solo inserción
- **Justificación:** trazabilidad e integridad de eventos (RF-12, RNF-10, RNF-11).
- **Descartado:** registrar solo en archivos de log.
- **Consecuencia:** más escrituras; se mitiga con índices y partición por fecha.

## ADR-06. Caché Redis para consultas de lectura frecuente
- **Justificación:** cumplir 95 % en 3 s en picos (RNF-02).
- **Descartado:** operar sin caché.
- **Consecuencia:** riesgo de datos desactualizados; se usa expiración corta e invalidación al escribir.
