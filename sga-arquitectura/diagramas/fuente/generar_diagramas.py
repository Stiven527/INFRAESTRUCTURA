import subprocess, textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def dot(name, src):
    open(f"img/{name}.dot","w").write(src)
    subprocess.run(["dot","-Tpng","-Gdpi=170",f"img/{name}.dot","-o",f"img/{name}.png"],check=True)

FONT='fontname="DejaVu Sans"'
# ---------- 6.1 Casos de uso ----------
ucs = {
 "CU01":"Iniciar / cerrar sesión","CU02":"Gestionar roles y permisos","CU03":"Gestionar estudiantes",
 "CU04":"Gestionar docentes","CU05":"Gestionar programas,\\nplanes y asignaturas","CU06":"Configurar periodos,\\ngrupos y horarios",
 "CU07":"Matricular estudiante","CU08":"Registrar / actualizar\\ncalificaciones","CU09":"Consultar asignaturas,\\nhorarios y notas",
 "CU10":"Generar reportes","CU11":"Buscar y filtrar registros","CU12":"Consultar auditoría"}
s=f'digraph G {{ rankdir=LR; splines=line; nodesep=0.3; ranksep=3.2; node[{FONT}, fontsize=11]; edge[arrowhead=none,color="#555555"];\n'
for a,l in [("ADM","Administrador"),("COO","Coordinador\\nacadémico"),("DOC","Docente"),("EST","Estudiante")]:
    s+=f'{a}[label="{l}",shape=box,style="filled",fillcolor="#E8EEF7",color="#1F3A5F",penwidth=1.6];\n'
s+='subgraph cluster_sga{label="Sistema de Gestión Académica (SGA)";fontsize=13;style="rounded";color="#1F3A5F";\n'
for k,v in ucs.items():
    s+=f'{k}[label="{k}\\n{v}",shape=ellipse,style=filled,fillcolor="#FFF8E1",color="#B8860B"];\n'
s+='}\n'
rel={"ADM":["CU01","CU02","CU03","CU04","CU05","CU06","CU10","CU11","CU12"],
"COO":["CU01","CU03","CU04","CU05","CU06","CU07","CU10","CU11"],
"DOC":["CU01","CU08","CU10","CU11"],
"EST":["CU01","CU09"]}
for a,l in rel.items():
    for c in l: s+=f'{a}->{c};\n'
s+='}'
dot("uc",s)

# ---------- 6.2 Componentes ----------
s=f'''digraph G{{ rankdir=TB; compound=true; nodesep=0.35; ranksep=0.55; node[{FONT},shape=box,style="rounded,filled",fontsize=10,fillcolor="#FFFFFF"]; edge[{FONT},fontsize=8,color="#444444"];
subgraph cluster_fe{{label="Capa de presentación";style="rounded,filled";fillcolor="#E8EEF7";color="#1F3A5F";
 SPA[label="Aplicación web SPA\\n(React, responsive, WCAG)"];}}
subgraph cluster_api{{label="Backend: monolito modular (API REST /api/v1)";style="rounded,filled";fillcolor="#F4F7EC";color="#4C6B22";
 GW[label="Capa API\\nControladores REST + validación + OpenAPI"];
 AUTH[label="Módulo Autenticación\\ny Autorización (RBAC)"];
 ACAD[label="Módulo Gestión Académica\\n(estudiantes, docentes, programas,\\nasignaturas, periodos, grupos)"];
 MAT[label="Módulo Matrículas"];
 CAL[label="Módulo Calificaciones"];
 REP[label="Módulo Reportes\\ny Búsqueda"];
 AUD[label="Módulo Auditoría"];
 INFRA[label="Capa de acceso a datos (ORM / repositorios)\\n+ transacciones"];}}
subgraph cluster_data{{label="Capa de datos y servicios";style="rounded,filled";fillcolor="#FDF1E7";color="#9C4A00";
 DB[label="PostgreSQL\\n(datos académicos + auditoría)",shape=cylinder];
 CACHE[label="Caché (Redis)\\nsesiones/consultas",shape=cylinder];
 BK[label="Servicio de respaldos"];}}
SPA->GW[label="HTTPS / JSON (IAPI)"];
GW->AUTH[label="verifica token y rol"];
GW->ACAD;GW->MAT;GW->CAL;GW->REP;
MAT->ACAD[label="valida grupo/cupo"];
CAL->MAT[label="valida matrícula"];
REP->ACAD;REP->MAT;REP->CAL;
MAT->AUD[label="evento"];CAL->AUD[label="evento"];AUTH->AUD[label="evento"];
ACAD->INFRA;MAT->INFRA;CAL->INFRA;REP->INFRA;AUD->INFRA;AUTH->INFRA;
INFRA->DB[label="SQL (TLS)"];
AUTH->CACHE[style=dashed];REP->CACHE[style=dashed];
BK->DB[label="pg_dump / WAL"];
}}'''
s=s.replace("(IAPI)","")
dot("comp",s)

# ---------- 6.3 Despliegue ----------
s=f'''digraph G{{ rankdir=TB; compound=true; nodesep=0.4; ranksep=0.6; node[{FONT},shape=box3d,style=filled,fillcolor="#FFFFFF",fontsize=10]; edge[{FONT},fontsize=9,color="#444444"];
U[label="Navegador web\\n(PC / móvil)",shape=box,style="rounded,filled",fillcolor="#E8EEF7"];
subgraph cluster_dmz{{label="Zona pública (DMZ)";style="rounded,filled";fillcolor="#FDECEA";color="#B03A2E";
 WAF[label="Reverse proxy / Balanceador\\nNginx + TLS 1.2+ (HTTPS)\\nWAF, rate limiting"];
 STA[label="Servidor de estáticos / CDN\\n(SPA compilada)"];}}
subgraph cluster_app{{label="Zona de aplicación (red privada)";style="rounded,filled";fillcolor="#F4F7EC";color="#4C6B22";
 A1[label="Nodo API 1\\nContenedor Docker\\nMonolito modular"];
 A2[label="Nodo API 2\\nContenedor Docker\\nMonolito modular"];
 RD[label="Redis\\n(caché/sesiones)",shape=cylinder];}}
subgraph cluster_db{{label="Zona de datos (sin acceso público)";style="rounded,filled";fillcolor="#FDF1E7";color="#9C4A00";
 DBP[label="PostgreSQL primario\\ncifrado en reposo",shape=cylinder];
 DBR[label="PostgreSQL réplica\\n(lectura / failover)",shape=cylinder];
 BKP[label="Almacén de respaldos\\n(diario + WAL, copia externa cifrada)",shape=folder];}}
MON[label="Monitoreo y logs\\n(Prometheus / Grafana / ELK)"];
U->WAF[label="HTTPS 443"];
WAF->STA[label="HTTP interno"];
WAF->A1[label="HTTP/TLS interno\\n/api"];WAF->A2;
A1->DBP[label="TCP 5432 TLS"];A2->DBP;
A1->RD[style=dashed];A2->RD[style=dashed];
DBP->DBR[label="replicación"];
DBP->BKP[label="respaldo cifrado"];
A1->MON[style=dashed];A2->MON[style=dashed];
}}'''
dot("deploy",s)

# ---------- 6.4 Datos ----------
ents={
"USUARIO":["PK id_usuario","email (único)","hash_contraseña","estado","id_rol (FK)"],
"ROL":["PK id_rol","nombre","descripción"],
"ESTUDIANTE":["PK id_estudiante","FK id_usuario","código","nombres/apellidos","FK id_programa","estado"],
"DOCENTE":["PK id_docente","FK id_usuario","documento","nombres/apellidos","estado"],
"PROGRAMA":["PK id_programa","código","nombre","nivel"],
"ASIGNATURA":["PK id_asignatura","FK id_programa","código","nombre","créditos","semestre"],
"PERIODO_ACADEMICO":["PK id_periodo","nombre (2026-1)","fecha_inicio","fecha_fin","estado"],
"GRUPO":["PK id_grupo","FK id_asignatura","FK id_periodo","FK id_docente","cupo","horario","aula/enlace"],
"MATRICULA":["PK id_matricula","FK id_estudiante","FK id_grupo","fecha","estado","UQ(estudiante,grupo)"],
"CALIFICACION":["PK id_calificacion","FK id_matricula","corte/tipo","nota","publicada","fecha"],
"AUDITORIA":["PK id_evento","FK id_usuario","fecha","acción","entidad","id_registro"],
}
s=f'digraph G{{ rankdir=LR; nodesep=0.45; ranksep=1.0; node[{FONT},shape=plain,fontsize=9]; edge[{FONT},fontsize=10,color="#333333",arrowhead=none,labeldistance=1.8];\n'
for n,at in ents.items():
    rows=''.join(f'<TR><TD ALIGN="LEFT">{a}</TD></TR>' for a in at)
    s+=f'{n}[label=<<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="3"><TR><TD BGCOLOR="#1F3A5F"><FONT COLOR="white"><B>{n}</B></FONT></TD></TR>{rows}</TABLE>>];\n'
def r(a,b,ta,tb,l=""):
    return f'{a}->{b}[taillabel="{ta}",headlabel="{tb}",label="{l}"];\n'
s+=r("ROL","USUARIO","1","N","tiene")
s+=r("USUARIO","ESTUDIANTE","1","0..1","es")
s+=r("USUARIO","DOCENTE","1","0..1","es")
s+=r("PROGRAMA","ESTUDIANTE","1","N","admite")
s+=r("PROGRAMA","ASIGNATURA","1","N","contiene")
s+=r("ASIGNATURA","GRUPO","1","N","se ofrece en")
s+=r("PERIODO_ACADEMICO","GRUPO","1","N","agrupa")
s+=r("DOCENTE","GRUPO","1","N","dicta")
s+=r("ESTUDIANTE","MATRICULA","1","N","realiza")
s+=r("GRUPO","MATRICULA","1","N","recibe")
s+=r("MATRICULA","CALIFICACION","1","N","genera")
s+=r("USUARIO","AUDITORIA","1","N","origina")
s+='}'
dot("er",s)

# ---------- 6.5 Secuencia ----------
def seq(name,title,parts,msgs):
    n=len(parts); W=1.9*n; H=0.55*len(msgs)+2.0
    fig,ax=plt.subplots(figsize=(W,H)); ax.set_xlim(0,n); ax.set_ylim(0,len(msgs)+2.2); ax.axis("off")
    top=len(msgs)+1.9
    xs=[i+0.5 for i in range(n)]
    for x,p in zip(xs,parts):
        ax.text(x,top,p,ha="center",va="center",fontsize=11,fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.35",fc="#E8EEF7",ec="#1F3A5F"))
        ax.plot([x,x],[0.2,top-0.3],color="#888",ls="--",lw=0.8,zorder=0)
    y=top-0.85
    for i,(a,b,t,kind) in enumerate(msgs):
        xa,xb=xs[a],xs[b]
        if a==b:
            ax.annotate("",xy=(xa,y-0.3),xytext=(xa,y),arrowprops=dict(arrowstyle="-|>",color="#9C4A00",connectionstyle="arc3,rad=-1.4",lw=1))
            ax.text(xa+0.08,y-0.15,f"{i+1}. {t}",fontsize=11.5,va="center",ha="left",color="#9C4A00")
            y-=1; continue
        ls="--" if kind=="r" else "-"
        col="#555" if kind=="r" else "#1F3A5F"
        ax.annotate("",xy=(xb,y),xytext=(xa,y),arrowprops=dict(arrowstyle="-|>",color=col,ls=ls,lw=1.1))
        ax.text((xa+xb)/2,y+0.12,f"{i+1}. {t}",fontsize=11.5,ha="center",va="bottom",color="#111")
        y-=1
    pass
    plt.tight_layout(); plt.savefig(f"img/{name}.png",dpi=170); plt.close()

P=["Estudiante","SPA web","Capa API","Módulo\nAutorización","Módulo\nMatrículas","Módulo\nAcadémico","PostgreSQL","Módulo\nAuditoría"]
M=[(0,1,"Selecciona grupo y confirma matrícula","m"),
(1,2,"POST /api/v1/matriculas {id_grupo} + JWT (HTTPS)","m"),
(2,3,"Validar token y permiso (rol ESTUDIANTE/COORD.)","m"),
(3,2,"Autorizado / 403","r"),
(2,4,"registrarMatricula(estudiante, grupo)","m"),
(4,5,"Verificar periodo abierto y grupo existente","m"),
(4,6,"BEGIN; SELECT grupo FOR UPDATE (bloqueo de cupo)","m"),
(4,4,"Reglas: cupo > 0, sin duplicado, estudiante activo","m"),
(4,6,"INSERT matrícula; UPDATE cupo; COMMIT","m"),
(4,7,"Registrar evento MATRICULA (usuario, fecha, acción)","m"),
(4,2,"Matrícula creada (201) o error 409/422","r"),
(2,1,"Respuesta JSON","r"),
(1,0,"Muestra confirmación o mensaje de error","r")]
seq("seq_mat","Figura 6.5-A. Secuencia: matrícula de un estudiante",P,M)

P2=["Docente","SPA web","Capa API","Módulo\nAutorización","Módulo\nCalificaciones","Módulo\nMatrículas","PostgreSQL","Módulo\nAuditoría"]
M2=[(0,1,"Ingresa nota del estudiante","m"),
(1,2,"PUT /api/v1/calificaciones/{id} {nota} + JWT","m"),
(2,3,"Validar token, rol DOCENTE","m"),
(3,2,"Autorizado","r"),
(2,4,"registrarNota(matrícula, nota)","m"),
(4,5,"¿Matrícula activa y grupo asignado a este docente?","m"),
(5,4,"Sí / No (403)","r"),
(4,4,"Validar rango de nota (0.0 a 5.0) y periodo abierto","m"),
(4,6,"UPDATE calificación (control de versión optimista)","m"),
(4,7,"Evento NOTA_MODIFICADA (valor anterior/nuevo)","m"),
(4,2,"200 OK / 409 conflicto de versión","r"),
(2,1,"Respuesta JSON","r"),
(1,0,"Confirma guardado","r")]
seq("seq_cal","Figura 6.5-B. Secuencia: registro de una calificación",P2,M2)
print("ok")
