# Uso de Google AI Studio

> Completar con los prompts reales usados, las respuestas relevantes y las capturas (carpeta `capturas/`). No incluir datos personales reales ni credenciales.

## Prompts propuestos

1. **Clasificar requerimientos.** Actúa como arquitecto de software. Te entrego 12 RF y 12 RNF de un sistema de gestión académica. Clasifica cada uno, identifica actores, supuestos, restricciones y reglas de negocio, y señala ambigüedades.
2. **Comparar estilos.** Compara arquitectura en capas, monolito modular y microservicios para este sistema (300 usuarios concurrentes, equipo de 3 a 5 personas, matrícula con alta concurrencia). Usa una tabla con los atributos de calidad de los RNF y recomienda uno con argumentos.
3. **Casos de uso.** Genera la lista de casos de uso para los 4 actores, con precondición, flujo principal y excepciones, alineados con RF-01 a RF-12. Entrega también el código PlantUML.
4. **Componentes.** Propón los módulos del backend con responsabilidades, interfaces y dependencias, de modo que autenticación, gestión académica, matrículas, calificaciones, reportes y auditoría queden claramente separados.
5. **Despliegue.** Describe un despliegue con proxy inverso, dos nodos de API, base de datos con réplica, respaldos y monitoreo. Indica canales de comunicación y controles de seguridad.
6. **Datos.** Propón el modelo conceptual con Usuario, Rol, Estudiante, Docente, Programa, Asignatura, PeriodoAcadémico, Grupo, Matrícula, Calificación y Auditoría, con cardinalidades y restricciones de integridad.
7. **Secuencia.** Describe la secuencia de matrícula de un estudiante garantizando que no se supere el cupo con solicitudes simultáneas.
8. **Crítica.** Revisa esta arquitectura: lista riesgos, puntos únicos de falla, problemas de seguridad y límites de escalabilidad, y señala qué requerimientos no están cubiertos.

## Registro de validación

| Prompt | Sugerencia de la IA | Decisión (aceptado / modificado / descartado) | Justificación | Captura |
|---|---|---|---|---|
| 1 | [completar] | | | `capturas/01.png` |
| 2 | [completar] | | | `capturas/02.png` |
| 3 | [completar] | | | `capturas/03.png` |
| 4 | [completar] | | | `capturas/04.png` |
| 5 | [completar] | | | `capturas/05.png` |
| 6 | [completar] | | | `capturas/06.png` |
| 7 | [completar] | | | `capturas/07.png` |
| 8 | [completar] | | | `capturas/08.png` |
