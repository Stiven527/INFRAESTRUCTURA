# Matriz de trazabilidad

| ID | Componentes | Modelo / decisión | Método de verificación |
|---|---|---|---|
| RF-01 | Autenticación; SPA; Auditoría | CU01; componentes; despliegue; ADR-03 | Pruebas de login y logout; credenciales inválidas; revisión del hash |
| RF-02 | Autorización (RBAC); Capa API | CU02; componentes; ADR-03 | Matriz de pruebas rol-endpoint |
| RF-03 | Gestión Académica; Datos | CU03; datos (ESTUDIANTE) | Pruebas CRUD con baja lógica |
| RF-04 | Gestión Académica; Datos | CU04; datos (DOCENTE) | Pruebas CRUD con baja lógica |
| RF-05 | Gestión Académica; Datos | CU05; datos (PROGRAMA, ASIGNATURA) | Pruebas de alta y edición; unicidad del código |
| RF-06 | Gestión Académica; Datos | CU06; datos (PERIODO, GRUPO) | Pruebas de creación de grupos con cupo, docente, horario y aula |
| RF-07 | Matrículas; Gestión Académica; Datos | CU07; secuencia de matrícula; ADR-04; RN-01, RN-02 | Pruebas de cupo agotado, duplicado y concurrencia por el último cupo |
| RF-08 | Calificaciones; Matrículas; Autorización | CU08; secuencia de calificación; ADR-04; RN-03 | Un docente no califica grupos ajenos; prueba de rango de nota |
| RF-09 | Matrículas y Calificaciones (consulta); Autorización | CU09; RN-04 | El estudiante solo ve datos propios y notas publicadas |
| RF-10 | Reportes y Búsqueda | CU10; componentes | Comparar con consultas SQL de control; probar filtros |
| RF-11 | Reportes y Búsqueda; índices | CU11 | Pruebas de búsqueda por cada criterio, con paginación y rol |
| RF-12 | Auditoría; todos los módulos | CU12; datos (AUDITORIA); ADR-05; RN-06 | Ejecutar acciones y verificar el evento; intentar modificarlo |
| RNF-01 | Proxy TLS; Autenticación; Autorización | Despliegue; ADR-03 | Escaneo TLS; sin contraseñas en texto plano; pruebas por rol |
| RNF-02 | Caché Redis; índices; 2 nodos API | Despliegue; ADR-06 | Prueba de carga con 300 usuarios: percentil 95 menor o igual a 3 s |
| RNF-03 | Balanceador; 2 nodos; réplica de BD; monitoreo | Despliegue; escenario de disponibilidad | Prueba de caída de nodo; monitoreo mensual (99,5 %) |
| RNF-04 | API sin estado; réplicas; módulos extraíbles | ADR-01; ADR-03; despliegue | Prueba de carga al duplicar nodos |
| RNF-05 | Módulos con interfaces; capa de acceso a datos | Componentes; ADR-01 | Cobertura de pruebas; reglas automáticas de dependencia |
| RNF-06 | SPA; sistema de diseño | Prototipos; componentes | Auditoría WCAG 2.2 AA; prueba por teclado y móvil |
| RNF-07 | Matrículas; Calificaciones; PostgreSQL | Datos; ambas secuencias; ADR-04 | Pruebas de concurrencia y de unicidad |
| RNF-08 | Capa API; OpenAPI | Componentes | Revisar el contrato OpenAPI; probar con Postman |
| RNF-09 | Servicio de respaldos; réplica; almacén externo | Despliegue; escenario de recuperación | Simulacro trimestral de restauración |
| RNF-10 | Documentación (ADR, matriz); repositorio | Esta matriz; decisiones | Revisión en cada versión; cada requisito con una prueba |
| RNF-11 | Autorización; filtros por propiedad; cifrado | Despliegue; RN-03, RN-04; ADR-05 | Pruebas de acceso entre usuarios; revisión de logs |
| RNF-12 | SPA responsive | Componentes | Pruebas en Chrome, Firefox, Edge y Safari recientes |

Los métodos de verificación son propuestos; su ejecución corresponde a la fase de implementación.
