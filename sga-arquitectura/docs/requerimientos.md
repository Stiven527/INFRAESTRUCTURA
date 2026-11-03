# Requerimientos del SGA

## Requerimientos funcionales

| ID | Requerimiento | Actor(es) | Módulo responsable | Prioridad |
|---|---|---|---|---|
| RF-01 | Autenticación: inicio y cierre de sesión con credenciales individuales | Todos | Autenticación | Alta |
| RF-02 | Roles y permisos: administrador, coordinador, docente y estudiante | Admin | Autorización (RBAC) | Alta |
| RF-03 | Gestión de estudiantes: registrar, consultar, actualizar, desactivar | Admin, Coord. | Gestión Académica | Alta |
| RF-04 | Gestión de docentes: registrar, consultar, actualizar, desactivar | Admin, Coord. | Gestión Académica | Alta |
| RF-05 | Programas, planes de estudio y asignaturas | Admin, Coord. | Gestión Académica | Alta |
| RF-06 | Periodos, grupos, cupos, docentes, horarios y aulas o enlaces | Coord. | Gestión Académica | Alta |
| RF-07 | Matrícula: validar cupos y evitar duplicados | Coord., Estudiante | Matrículas | Alta |
| RF-08 | Registro y actualización de calificaciones por el docente | Docente | Calificaciones | Alta |
| RF-09 | Consulta de asignaturas, horarios y notas publicadas | Estudiante | Matrículas / Calificaciones (lectura) | Alta |
| RF-10 | Reportes con filtros por periodo y programa | Admin, Coord., Docente | Reportes y Búsqueda | Media |
| RF-11 | Búsqueda y filtros | Usuarios autorizados | Reportes y Búsqueda | Media |
| RF-12 | Auditoría de eventos relevantes | Admin | Auditoría | Alta |

## Requerimientos no funcionales

| ID | Atributo | Criterio | Táctica principal |
|---|---|---|---|
| RNF-01 | Seguridad | HTTPS; contraseñas con hash; acceso por roles | TLS en proxy, hash Argon2/bcrypt, JWT + RBAC |
| RNF-02 | Rendimiento | 95 % de consultas comunes en 3 s o menos con 300 usuarios concurrentes | Índices, paginación, caché Redis, 2 nodos API |
| RNF-03 | Disponibilidad | 99,5 % mensual | Balanceo, réplica de BD, health checks |
| RNF-04 | Escalabilidad | Crecer sin rediseño | API sin estado, escalado horizontal |
| RNF-05 | Mantenibilidad | Bajo acoplamiento, alta cohesión | Monolito modular, interfaces, pruebas |
| RNF-06 | Usabilidad y accesibilidad | Responsive, contraste, teclado | Sistema de diseño, WCAG 2.2 AA |
| RNF-07 | Integridad y consistencia | Reglas de negocio y concurrencia | Transacciones ACID, bloqueo de fila, bloqueo optimista |
| RNF-08 | Interoperabilidad | Interfaces documentadas (REST) | API `/api/v1` con OpenAPI |
| RNF-09 | Respaldo y recuperación | Copias periódicas y restauración | Respaldo diario + WAL, copia externa cifrada |
| RNF-10 | Trazabilidad | Requisitos enlazados con componentes y evidencias | Matriz de trazabilidad, ADR |
| RNF-11 | Privacidad | Datos según necesidad del rol | Mínimo privilegio, cifrado en reposo |
| RNF-12 | Compatibilidad | Navegadores recientes y varias pantallas | SPA responsive |

## Reglas de negocio

- **RN-01.** Un estudiante no puede matricularse dos veces en el mismo grupo ni en dos grupos de la misma asignatura en el mismo periodo.
- **RN-02.** La matrícula requiere periodo abierto, cupo disponible y estudiante activo.
- **RN-03.** Solo el docente asignado al grupo puede registrar o modificar sus calificaciones.
- **RN-04.** El estudiante solo ve sus calificaciones publicadas.
- **RN-05.** Las entidades se desactivan (baja lógica); no se borran físicamente.
- **RN-06.** Toda matrícula, cambio de rol, inicio de sesión y modificación de nota genera un evento de auditoría inmutable.
