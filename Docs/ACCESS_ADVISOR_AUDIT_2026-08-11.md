# Access Advisor — Auditoría multi-proveedor y especificación v1 (2026-08-11)

Este documento es un research log puntual, no uno de los 7 documentos
oficiales del proyecto. Producido en la rama
`research/access-advisor-audit-2026-08-11`, creada desde `main` en
`d2047b5` (limpio, 103/103 tests) y que existe **únicamente para
contener esta investigación** — no está pensada para mergearse a `main`
tal cual. No se tocó `dataset/`, `SCHEMA.md`, `decision/` ni
`interfaces/web/` durante su elaboración.

**Origen:** la auditoría de campo (secciones 1 y 2 de este documento) la
produjo Codex (OpenAI), operando como auditor/researcher externo del
proyecto en esta sesión, contra documentación oficial de cada
proveedor. Claude Code (este documento) la revisó, la verificó contra
las reglas ya existentes del proyecto (`AGENTS.md`, `SCHEMA.md`,
`ARCHITECTURE.md`) y la consolidó en la especificación de la Parte 3.
División de trabajo acordada explícitamente con el dueño del proyecto:
Codex audita/verifica fuentes, Claude Code decide y, si corresponde,
implementa.

**Alcance:** cerrar la brecha que dejó abierta
`research/access-model-research` (marco conceptual, sin casos
multi-proveedor) con evidencia oficial concreta de los cinco
proveedores ya representados en el dataset — Google, Anthropic, OpenAI,
NVIDIA (NIM) y AWS (Bedrock) — y proponer, recién en la Parte 3, un
modelo de datos y reglas v1 para un "Access Advisor" que se ejecute
**después** del `Recommendation` actual, sin modificar el scoring.

**Idioma:** documento interno, en español. Técnico en inglés — nombres
de modelo, nombres de campo, términos como API/token/GPU/Bedrock, y las
citas textuales de fuentes oficiales, nunca traducidas.

**Sobre la extensión:** documento único, mismo criterio que
`ACCESS_MODEL_RESEARCH_2026-08-10.md` — uso interno, nunca lo lee
`decision/` ni `interfaces/`, más fácil de navegar entero que partido.

## Índice

- [Parte 1 — Caso profundo: Google Gemini API / AI Studio](#parte-1--caso-profundo-google-gemini-api--ai-studio)
- [Parte 2 — Auditoría cruzada: los cinco proveedores](#parte-2--auditoría-cruzada-los-cinco-proveedores)
- [Parte 3 — Especificación v1 del Access Advisor](#parte-3--especificación-v1-del-access-advisor)
- [Parte 4 — Validación, caveats abiertos y orden de entrega](#parte-4--validación-caveats-abiertos-y-orden-de-entrega)
- [Parte 5 — Decisiones de arquitectura pendientes, en 4 bloques](#parte-5--decisiones-de-arquitectura-pendientes-en-4-bloques)
- [Fuentes](#fuentes)

---

## Parte 1 — Caso profundo: Google Gemini API / AI Studio

Producido primero, como caso piloto (mismo criterio que pide
`PLAN.md`: "Google será el caso piloto"), antes de la auditoría
cruzada de la Parte 2.

**Hallazgos centrales, confirmados contra fuente oficial:**

1. **Google AI Pro/Ultra no son los tiers de Gemini API.** Los tiers de
   API son Gratis, Nivel 1, 2 y 3, determinados por proyecto + cuenta
   de Cloud Billing + pago acumulado + antigüedad
   ([Billing](https://ai.google.dev/gemini-api/docs/billing?hl=es-419)).
   Una suscripción Google AI es un plan de Google One, con límites
   propios por producto.
2. **Ninguna fuente documenta que una suscripción mejore RPM/TPM/RPD de
   la API ni pague sus tokens.** Eso exige vincular Cloud Billing y,
   habitualmente, un prepago mínimo de USD 10.
3. **AI Studio sí es un beneficio de Pro/Ultra en el estado actual de
   Google One** — la página de restricciones dice que hoy sólo está
   disponible para Pro/Ultra
   ([restricciones](https://support.google.com/googleone/answer/16105039?hl=en-en)).
   Esto convive con documentación de Gemini API que sigue hablando de
   "Free Tier" y mencionando AI Studio — tratado explícitamente como
   posible deriva regional/temporal, no como contradicción a resolver
   por inferencia.
4. **Acceso a un modelo no implica consumo incluido.** Una key pagada
   usada desde AI Studio genera cobro; compartir una app de Build hace
   que las llamadas de los usuarios de esa app cuenten contra la
   cuota/costo de la key del creador.
5. **Conclusión de diseño (llevada a la Parte 3):** recomendar dos
   decisiones separadas — modelo/API de ejecución, y superficie de
   trabajo personal. Pro/Ultra puede ser la respuesta correcta para AI
   Studio, Gemini Apps, Antigravity o Flow; nunca se debe presentar
   como alternativa económica al uso intensivo de Gemini API sin una
   excepción documentada para ese producto puntual.

**Tabla resumen de modalidades** (detalle completo, con cada fuente
citada, en el documento original de Codex — preservado aquí por ser la
evidencia primaria de esta sesión):

| Modalidad | Qué es | Relación confirmada | Unidad de acceso/costo relevante |
|---|---|---|---|
| Gemini API | Interfaz developer para integrar Gemini/Veo/Nano Banana/agentes. | AI Studio puede crear/gestionar las keys que usa; no es una tarifa distinta. | Proyecto + API key + Cloud Billing; tokenizado/por media. |
| Google AI Studio | Producto web de prompt testing, gestión de keys/uso, prototipado (Build/Playground Agents). | No es un modelo ni una tarifa distinta; una key pagada vinculada cobra como uso de API. | Acceso personal Pro/Ultra según Google One vigente; la key decide el tier de API. |
| Google AI Pro | Suscripción Google One. | Incluye AI Studio, límites mayores en Gemini Apps, Antigravity, Flow. No es tier de Gemini API. | Límite por producto/suscripción. |
| Google AI Ultra | Plan Google One de máximo acceso. | Incluye Pro + mayor cuota Gemini Apps/Antigravity, Deep Think, AI Studio. No es tier de Gemini API. | Límite por producto/suscripción. |
| Vertex AI / Google Cloud | Plataforma enterprise/cloud. | Usa Gemini vía Vertex, plano de API/facturación/cuotas distinto (DSQ o throughput reservado). | Proyecto/región Cloud; Cloud Billing. |
| Gemini Apps | App de consumo (web/móvil). | Pro/Ultra eleva límites; refresco cada 5 h hasta tope semanal. | Cuenta/plan Google AI. |
| Google Antigravity | IDE agéntico sobre Gemini 3 Pro y Model Garden. | Pro/Ultra da mayor cuota/prioridad; AI credits aplican acá. El **Antigravity Agent** de Gemini API es un acceso distinto (managed agent por API). | Suscripción+credits para la plataforma; API key/tokens+tools para el Agent API. |

**Free Tier de API vs. Paid Tier vs. Pro/Ultra — no intercambiables:**
free tier de API es acceso gratuito y limitado por modelo/proyecto,
paid tier exige Cloud Billing vinculado, y Pro/Ultra es nomenclatura de
producto de consumo — ninguna fuente equipara las tres escalas. Los
rate limits documentados (RPM, TPM de input, RPD) se miden **por
proyecto, no por API key**
([rate limits](https://ai.google.dev/gemini-api/docs/rate-limits?hl=es-419)).

**Pregunta de producto ("tengo USD 25, ¿API o suscripción?"):** no
respondible con precisión sin mezcla de input/output, modalidad,
contexto, herramientas, región/precio de suscripción y necesidad de
API desde una app. Como aproximación de tokens puros: USD 25 en Gemini
2.5 Flash ($0.30 in / $2.50 out) da ~8,9M tokens si input=output; en
3.5 Flash ($1.50/$9.00) da ~2,38M pares — sin cache, grounding, media
ni impuestos. Para uso humano en Gemini Apps/AI Studio/Antigravity/Flow,
Pro/Ultra puede ser la mejor vía porque da el acceso a esos productos —
eso no hace el costo marginal de una llamada API igual a cero.

**Ambigüedades explícitamente no resueltas por las fuentes** (no deben
inferirse en el Advisor):

1. No hay tabla oficial "sin suscripción / Pro / Ultra" por modelo,
   precio o cuota de API.
2. Elegibilidad de AI Studio (Google One) vs. "Free Tier" (docs de API)
   puede ser una deriva regional/temporal — verificar por cuenta/país
   antes de cualquier UX concluyente.
3. RPM/TPM/RPD exactos viven en el dashboard del proyecto, cambian por
   modelo/nivel — no hardcodear una tabla universal.
4. Precio local de Pro/Ultra, disponibilidad exacta por país/cuenta,
   cuotas numéricas de AI Studio, y equivalencia AI credits↔tokens
   Gemini API: no determinado.
5. Google AI Studio ≠ Vertex AI Studio ≠ Gemini App — superficies
   distintas aunque compartan tecnología.

---

## Parte 2 — Auditoría cruzada: los cinco proveedores

**Snapshot:** 2026-08-11, America/Argentina/Buenos_Aires. Fuentes:
documentación oficial de cada proveedor únicamente.

### 2.1 Patrón dominante por proveedor

| Proveedor | Patrón dominante | Conclusión para Access Advisor |
|---|---|---|
| Google | API por proyecto/Cloud Billing; AI Studio y planes Google AI son superficies separadas. | Una suscripción puede dar AI Studio/Gemini Apps, pero **no documenta** créditos ni mejores cuotas de Gemini API. |
| Anthropic | API first-party por organización; Console/Workbench para probar; Claude consumer es otra superficie. | Para integrar/automatizar, API con organización y límites propios; el plan Claude no se trata como saldo API. |
| OpenAI | API por organización/proyecto y tier de uso; ChatGPT es facturación/uso separado. | Separación confirmada explícitamente por el propio soporte de OpenAI: la suscripción ChatGPT no migra ni cubre consumo API. |
| NVIDIA NIM | API catalog gratuita para prototipado + NIM descargable; producción self-hosted requiere AI Enterprise. | El costo principal puede ser licencia por GPU + infraestructura, no tokens — no comparable como API pay-per-token. |
| Amazon Bedrock | Plataforma cloud AWS: catálogo de terceros, consola/playground y APIs; IAM, Marketplace, región y cuotas AWS. | El acceso es de cuenta AWS/rol/región. Bedrock es vía de consumo, no suscripción al modelo ni self-hosting. |

**Regla de oro de esta auditoría, y del Advisor:** disponibilidad de
modelo ≠ elegibilidad del usuario ≠ unidad de facturación ≠ derecho a
automatizar/producción.

### 2.2 Taxonomía de superficies y estados

| Superficie | Significado |
|---|---|
| `direct_api` | API gestionada por el proveedor del modelo. |
| `playground_or_studio` | Entorno visual de prueba/prototipado. |
| `consumer_subscription` | App/web/IDE de uso humano sujeto a un plan. |
| `cloud_hosted` | Modelo invocado desde cloud de un tercero (p. ej. Bedrock/Vertex). |
| `enterprise` | Contrato, gobierno, soporte o capacidad empresarial. |
| `self_hosted` | El usuario despliega software/pesos/infraestructura propia. |

| Estado | Significado |
|---|---|
| `confirmed` | La fuente oficial afirma el hecho. |
| `not_determined` | La documentación consultada no permite afirmarlo. |
| `account_dependent` | Depende de organización, proyecto, billing, dashboard o historial de cuenta. |
| `region_dependent` | Depende de país, región cloud o geografía de procesamiento. |
| `deprecated` | La fuente marca el modelo/superficie como deprecated/retired, o da fecha de fin. |

Este vocabulario de 6 superficies × 5 estados es el que adopta la Parte
3 como vocabulario de campo — no `if provider == "..."` en ningún
lado, sólo estos atributos.

### 2.3 Catálogo: qué cuenta como "modelo disponible"

No existe una lista estable copiable como inventario de largo plazo —
cada proveedor publica catálogos vivos, aliases y modelos en preview.
Antes de recomendar un ID concreto, el Advisor debe resolverlo contra
el catálogo vigente del proveedor y la región/cuenta aplicable, nunca
contra una copia local.

| Proveedor | Catálogo primario (autoridad) | Estado/caveat |
|---|---|---|
| Google | [Gemini API Models](https://ai.google.dev/gemini-api/docs/models?hl=es-419) | `confirmed`; disponibilidad gratuita/paga y preview se determina por modelo. |
| Anthropic | [Claude Platform home](https://platform.claude.com/docs/en/home), [pricing](https://platform.claude.com/docs/en/about-claude/pricing) | `confirmed`; lifecycle puede diferir entre API first-party, Bedrock y Google Cloud. |
| OpenAI | [OpenAI model catalog](https://developers.openai.com/api/docs/models) | `confirmed`; cada ficha trae endpoints, capacidades, precios, snapshots y límites. |
| NVIDIA | [API Catalog](https://build.nvidia.com/explore/discover), [NIM support matrix](https://docs.nvidia.com/nim/large-language-models/2.0.2/reference/support-matrix.html) | `account_dependent`; catálogo y perfiles/hardware dinámicos, no todo modelo alojado es NIM certificado. |
| AWS Bedrock | [Model availability & compatibility](https://docs.aws.amazon.com/bedrock/latest/userguide/models.html) | `region_dependent`; el propio catálogo es la tabla canónica por modelo/endpoint/región. |

**Consecuencia directa:** "Claude existe en Bedrock", "Llama existe en
NIM" o "GPT existe en ChatGPT" no permite concluir que el mismo ID,
versión, cuota, privacidad ni facturación estén disponibles para el
usuario concreto.

### 2.4 Matriz cruzada de superficies por familia

| Proveedor / familia | API | Playground | Suscripción/app | Cloud | Enterprise | Self-host | Free | Billing separado |
|---|---|---|---|---|---|---|---|---|
| Google / Gemini | `confirmed` | `confirmed` (AI Studio) | `confirmed` (Google AI Pro/Ultra, según elegibilidad) | `confirmed` (Vertex AI) | `confirmed` (Gemini Enterprise Agent Platform/Vertex) | — | `confirmed` (modelos/cuotas seleccionados de API) | `confirmed` (plan Google AI no es tier de API) |
| Anthropic / Claude | `confirmed` (Messages/Managed Agents) | `confirmed` (Workbench/Console) | `confirmed` (Claude consumer/Enterprise, cuotas propias) | `confirmed` (Bedrock, Google Cloud, Microsoft Foundry) | `confirmed` (enterprise/custom terms/admin) | — | `confirmed` (crédito de prueba chico; no free tier continuo) | `confirmed` (Platform AWS vía Marketplace, distinto de créditos Anthropic) |
| OpenAI / GPT | `confirmed` | `confirmed` (enlaces por modelo; requiere cuenta/API) | `confirmed` (planes ChatGPT) | `confirmed` (Bedrock como integración; verificar modelo/región) | `confirmed` (Business/Enterprise/Edu) | `confirmed` sólo para familias open-weight publicadas | `confirmed` (API Free no cubre estos modelos; ChatGPT free es otra superficie) | `confirmed` (API y ChatGPT se gestionan/facturan por separado, explícito) |
| NVIDIA / NIM | `confirmed` (endpoints alojados) | `confirmed` (API Catalog) | — | `confirmed` (clouds propios/partners) | `confirmed` (NIM Certified/AI Enterprise) | `confirmed` (Docker/K8s/air-gap/model-free) | `confirmed` (Developer Program, sólo prototipo) | `confirmed` (producción = licencia AI Enterprise + infraestructura) |
| AWS / Bedrock | `confirmed` (InvokeModel/Converse) | `confirmed` (Console playgrounds) | — | `confirmed` (es la definición del producto) | `confirmed` (IAM, SCP, VPC/PrivateLink, provisioned throughput) | — | `not_determined` (sin free tier general documentado) | `confirmed` (factura AWS; modelos 3P pueden exigir Marketplace/EULA) |

### 2.5 Facturación y suscripción — qué sí y qué no permite afirmar la evidencia

**Confirmado:**

1. Google: paid tier vía Cloud Billing/proyecto, cuota por proyecto;
   Pro/Ultra son planes Google One, documentados aparte del billing de
   API.
2. Anthropic: API facturada por uso mensual; créditos de prueba
   pequeños sin importe público; Claude Platform on AWS factura vía
   AWS Marketplace, no créditos Anthropic.
3. OpenAI: la API está *"billed and managed separately to ChatGPT"*
   (cita textual de soporte oficial); paga con método de pago propio
   del billing de API.
4. NIM: Developer Program permite prototipo/desarrollo/test;
   producción exige NVIDIA AI Enterprise, desde USD 4.500/GPU/año o
   ~USD 1/GPU/h cloud, independiente de la cantidad de NIMs.
5. Bedrock: AWS factura uso/capacidad aprovisionada; modelos de
   terceros exigen aceptar EULA vía AWS Marketplace/IAM.

**No determinado por las fuentes consultadas:**

- Que un plan consumer de Claude incluya un volumen equivalente a una
  API concreta.
- Que Google AI Pro/Ultra mejore RPM/TPM/RPD o pague tokens de Gemini
  API.
- Que créditos de ChatGPT Enterprise/Business habiliten cualquier
  endpoint de la API de OpenAI.
- Una tabla pública global de RPM de NVIDIA API Catalog.
- Un free tier general y permanente de Bedrock.

### 2.6 Rate limits y cómo debe expresarlos el Advisor (nunca como promesa)

| Proveedor | Scope confirmado | Cómo debe expresarlo el Advisor |
|---|---|---|
| Google API | Proyecto y modelo, no API key. | "Quota depends on project/model/tier; verify in AI Studio." |
| Anthropic API | Organización, por modelo/tier. | "Organization limits apply; current values are readable in Console/Rate Limits API." |
| OpenAI API | Usage tier y modelo. | "API tier required; check model-specific rate-limit table." |
| NVIDIA API Catalog | Sin tabla pública universal documentada. | "Do not promise an RPM; check account/catalog terms." |
| NIM self-host | GPU, modelo, profile, despliegue. | "Estimate from validated GPU profile; not a provider API quota." |
| Bedrock | Cuenta + endpoint + modelo + región. | "Check AWS Service Quotas in the target region/endpoint." |

### 2.7 Deprecaciones y migración (relevante para no recomendar una ruta muerta)

- Anthropic define `active`/`legacy`/`deprecated`/`retired`, con ≥60
  días de aviso para modelos públicamente publicados en plataformas
  operadas por Anthropic; Bedrock/Google Cloud pueden tener fechas
  distintas.
- OpenAI publica snapshots y IDs deprecados por ficha de modelo.
- Google marca previews/deprecados con fechas de sunset por familia
  cuando corresponde (p. ej. Imagen/Veo).
- Bedrock publica lifecycle y guía de migración por modelo — puede
  seguir activo en Bedrock aunque el proveedor lo retire, o viceversa.
- NIM distingue Day 0 (sin garantías de lifecycle) de NIM Certified
  (lifecycle/mantenimiento empresarial documentado).

---

## Parte 3 — Especificación v1 del Access Advisor

Esta parte es la síntesis de Claude Code sobre la evidencia de las
Partes 1 y 2, verificada contra `AGENTS.md`/`ARCHITECTURE.md`/
`SCHEMA.md` — no es transcripción directa de Codex.

### 3.1 Separar tres preguntas, no una

```text
Model availability
  "¿La plataforma publica este modelo/ID en esta superficie?"

Access route
  "¿Qué necesita una persona/organización para invocarlo aquí?"

User eligibility
  "¿Este usuario, con región, plan, billing e intención concretos,
   cumple hoy?"
```

`Recommendation` (el motor actual) responde una cuarta pregunta
distinta de las tres de arriba — "¿qué modelo es el más indicado para
tu contexto de calidad/costo?" — y no se toca. El Access Advisor se
ejecuta **después**, nunca vuelve a puntuar calidad, y nunca cambia el
ganador.

**Revisión (2026-08-11, segunda pasada, a pedido explícito del dueño
del proyecto):** la primera versión de este documento aterrizaba las
tres preguntas de arriba en una sola fila plana de `access_routes`
(ver 3.2), mezclando en los mismos campos "¿existe esta ruta?" con
"¿cuánto cuesta?" y, parcialmente, "¿quién califica?". Es la misma
fusión de conceptos que el proyecto ya había decidido evitar para
`subscriptions/` — corregida acá antes de cerrar la decisión. La
auditoría de las Partes 1 y 2 sostiene, en los cinco proveedores, que
son **tres ejes independientes** que pueden variar por separado para
el mismo modelo:

```text
Modelo: X

  Access (¿existe la ruta?)
    API directa       ✓
    Cloud hosted       ✓
    Subscription        ✗
    Self-hosted         ✓

  Eligibility (¿este usuario puede usarla?)
    billing API         ✓
    AWS account          ✗
    GPU propia           ✓
    región                ✓

  Economics (¿cuánto cuesta usarla?)
    api_token (Access API)
    cloud_paygo (Access Cloud)
    gpu_license (Access Self-hosted)
```

El modelo está disponible por varias rutas, pero no todas esas rutas
están disponibles para *este* usuario, y cada una que sí lo está tiene
una unidad de costo distinta — un GPU-hora no es comparable contra un
USD/millón de tokens sin convertir la pregunta. Esta es la potencia
real del Advisor: cruzar las tres tablas, no aplanarlas en una.
`SCHEMA.md`/`dataset/models/` no representa ninguna de las tres — las
tres viven en el catálogo nuevo de la sección 3.2, con la separación
de ejes preservada dentro del propio formato del archivo, no solo en
la prosa de este documento.

### 3.2 Por qué esto no es un cambio de `SCHEMA.md`

`AGENTS.md` es explícito: `SCHEMA.md` no se modifica reactivamente, y
"cómo se paga esto" es justo el riesgo que
`research/access-model-research` ya había marcado para
`access.has_free_access`. La evidencia de las Partes 1 y 2 confirma por
qué: rutas de acceso, planes y cuotas son datos que **cambian rápido y
dependen de cuenta/región** (`account_dependent`/`region_dependent` en
la mayoría de las filas de la matriz), mientras que `dataset/models/`
está diseñado para hechos objetivos relativamente estables del modelo
en sí. Meter una tabla de rate limits o de elegibilidad de suscripción
en el YAML de un modelo lo dejaría stale en semanas, y violaría
"nunca fabricar precisión" apenas el dashboard de una cuenta cambie.

**Propuesta: catálogo nuevo, separado, fuera de `dataset/models/`, con
Access/Eligibility/Economics como tres bloques explícitos dentro de
cada ruta — no tres campos sueltos entre otros diez.**

```text
dataset/access_routes/{provider}/{route_id}.yaml
  provider: string
  model_id: string                # id exacto y existente de dataset/models/ —
                                  # nunca family/agregado (cerrado en 5.1)

  access:                        # eje 1 — ¿existe esta ruta?
    surface: direct_api | playground_or_studio | consumer_subscription |
             cloud_hosted | enterprise | self_hosted
    access_method: string        # "API key", "AI Studio", "Workbench", etc.
    capabilities: [prototype, build, deploy, managed_agent,
                   enterprise_governance, automation]
    guide_ref: string            # id de sección en docs/access-guides/{provider}.md
                                  # (ver 5.4) — data-driven, la UI nunca adivina
                                  # qué guía corresponde a qué ruta

  eligibility:                   # eje 2 — ¿quién califica, y con qué?
    requirements:                # lista tipada, NO string libre — cerrado
                                  # en 5.2.1, kind = enum validado por el
                                  # loader, value depende del kind:
      - kind: api_billing_linked
      - kind: cloud_account
        value: aws               # aws | gcp | azure
      - kind: consumer_subscription
        value: [google-ai-pro, google-ai-ultra]   # any-of, plan_id de
                                                    # subscriptions/*.yaml
      - kind: program_membership
        value: nvidia_developer_program
      - kind: gpu_infrastructure
    region_scope: account_dependent | region_dependent | global | not_determined

  economics:                     # eje 3 — ¿cuánto cuesta usarla?
    billing_owner: string        # quién factura (proveedor del modelo,
                                  # AWS, NVIDIA AI Enterprise, ...)
    billing_scheme: subscription_quota | api_token | media_unit |
                    cloud_paygo | gpu_license | provisioned
    quota_scope: product | project | organization | billing_account |
                 region | account
    production_allowed: boolean | not_determined

  evidence:                      # trazabilidad, igual disciplina que dataset/models/
    source_url: string
    consulted_at: date
    status: confirmed | not_determined | account_dependent |
            region_dependent | deprecated
    caveat: string                # texto libre, la salvedad real de la fila

dataset/subscriptions/{provider}/{plan_id}.yaml
  provider: string
  plan_name: string               # "Google AI Pro", "ChatGPT Plus", ...
  surface_entitlements: [surface, ...]   # informativo — qué superficies
                                          # habilita en general (para mostrar
                                          # "qué te da este plan", nunca
                                          # usado para matching de
                                          # elegibilidad — eso vive
                                          # enteramente en
                                          # access_routes.eligibility.
                                          # requirements[kind=consumer_
                                          # subscription].value, ver 5.4)
  documented_exclusions: [string, ...]   # informativo — qué NO cubre, en
                                          # prosa, ej. "no API billing"
  region_scope: string
  source_url: string
  consulted_at: date
  status: confirmed | not_determined | account_dependent | region_dependent
```

**Por qué esto evita la cadena `Claude → Claude Pro → Sonnet → API`:**
`subscriptions/*.yaml` nunca referencia un `model_id` ni un
`route_id` — sólo declara qué *superficies* habilita en general
(`surface_entitlements`, informativo). `access_routes/*.yaml` nunca
referencia un plan por nombre en prosa — solo por `plan_id` dentro de
`consumer_subscription.value` (cerrado en 5.4: `satisfies_requirements`
se eliminó, era redundante con esto). El cruce entre ambos catálogos
(¿el plan que declaró el usuario resuelve los requisitos de esta ruta,
para este modelo?) lo hace el Advisor **en tiempo de consulta**, leyendo
el contexto de acceso (3.3), nunca
hardcodeado en el dato. Un mismo plan (p. ej. Google AI Pro) puede así
satisfacer la elegibilidad de rutas de N modelos distintos sin que
ningún archivo mencione esos modelos por nombre — mismo principio que
el hard constraint de `AGENTS.md` de no razonar por identidad en
`decision/`, aplicado ahora también a este catálogo nuevo.

Ambos catálogos son datos versionados en el repo (igual disciplina de
sourcing que `dataset/models/`: URL + fecha + estado, nunca
aggregators), pero **fuera** del schema que valida `loader.py` hoy —
necesitan su propio loader/validador cuando se implementen, no una
extensión de `SCHEMA.md`.

### 3.3 Contexto de acceso (input del usuario, separado de las prioridades de calidad)

| Campo | Valores v1 | Uso |
|---|---|---|
| `use_mode` | `manual`, `prototype`, `api_integration`, `automation` | Distingue consumo humano de llamada programática. |
| `workload_type` | `exploratory`, `interactive`, `batch`, `agentic` | Distingue latencia/operación, sin estimar tokens. |
| `intensity` | `occasional`, `frequent`, `intensive` | Selecciona advertencia/ruta, nunca promete cuota. |
| `subscriptions` | conjunto declarado por el usuario | Sólo aplica si `subscriptions/*.yaml` conecta ese plan a una superficie concreta. |
| `has_api_billing` | boolean/unknown | Determina elegibilidad de API paga, no capacidad. |
| `cloud_accounts` | AWS/GCP/etc. declarados | Determina si corresponde sugerir una ruta cloud. |
| `country` | ISO 3166-1 alpha-2 / unknown | **Cerrado en 5.1 — un solo campo, sin `cloud_region`. Actualizado en la pasada final: no participa en matching todavía** (ver 5.1 — ni `AccessRoute` ni `SubscriptionPlan` tienen hoy una lista de países comparable). Se recolecta y se muestra junto al `caveat` de la ruta, nunca decide `requires_onboarding`/`not_available` por sí solo. Compatibilidad de región cloud específica (¿está este modelo en `eu-west-1`?) queda deliberadamente fuera del matching — no hay fuente estable/determinística para eso (mismo problema que rate limits: tablas dinámicas por dashboard, no un dato objetivo estable). Puerta abierta, no diseñada preventivamente: matching real por país o por `cloud_region` se agrega el día que exista evidencia estructurada y estable para eso, con esa evidencia como justificación. |
| `has_gpu_infrastructure` | boolean/unknown | **No** "tiene alguna GPU" — significa infraestructura GPU compatible/disponible para correr NIM específicamente. Definición deliberadamente angosta (ver Bloque 2.1, 5.2); no intenta capturar modelo de GPU, VRAM ni cantidad — esa granularidad solo se agrega si la evidencia la exige. |
| `program_memberships` | conjunto declarado por el usuario | Programas de desarrollador declarados (ej. NVIDIA Developer Program). Vacío por default; ningún proveedor nuevo asume membership sin que el usuario la declare. |

Este bloque vive en el contexto de la consulta (análogo a `Priorities`/
`Budget` hoy), nunca dentro de `dataset/models/`. Los dos últimos
campos se agregaron en el cierre del Bloque 2.1 (5.2) — sin ellos,
`gpu_infrastructure` y `program_membership` no tendrían con qué
matchear.

### 3.4 Reglas v1 — revisadas (ver 5.2.2/5.2.3 para el porqué del recorte)

**Superadas por la simplificación de la Parte 5 (2026-08-11):** las 5
reglas de priorización que vivían acá (preferir
playground para manual, API directa para integración, etc.) asumían
que Access Advisor elegía una "ruta principal" por criterio editorial.
Esa elección se eliminó — ver 5.2.2. Lo único que sobrevive de estas
reglas, reformulado sin ranking:

1. **`intensity: intensive`:** el `caveat` de la ruta debe mencionar
   controles de gasto/observabilidad si la evidencia los documenta.
   Nunca declarar que una suscripción cubre intensidad alta — eso ya
   estaba bien y sigue igual.
2. **Enterprise/compliance:** rutas con `access.capabilities:
   enterprise_governance` no entran a la lista de acceso por default
   — se muestran solo si el usuario pide explícitamente ver rutas
   enterprise. Ya estaba decidido así (5.0/5.2.1), sin cambios acá.
3. **NIM/self-host:** nunca comparar su costo contra "USD por 1M
   tokens" — unidades incompatibles (GPU-hora/licencia vs. token). Se
   muestra como una ruta más de la lista, con su propio `caveat` de
   costo real, igual que cualquier otra.

Lo que se elimina explícitamente: cualquier regla que decida qué
`use_mode` prefiere qué superficie. La lista completa de rutas ya le
da esa información al usuario sin que Access Advisor tenga que
adivinar su preferencia.

### 3.5 UI — resumen corto + lista expandible (reemplaza la versión anterior de esta sección)

**Decisión final de esta sesión, después de revisar la complejidad que
había acumulado el diseño:** no hay una card de "Best way to access" +
"Alternative" elegidas por ranking. En su lugar, dos niveles:

**Nivel 1 — resumen corto, siempre visible, después del
`Recommendation` actual:**

```text
Acceso recomendado
──────────────────
Anthropic API
Disponible ahora

[Ver todas las opciones de acceso]
```

Regla de selección del resumen — **deliberadamente simple, no un
ranking**: entre las rutas `currently_eligible` **con
`evidence.status: confirmed`** del modelo ganador, si exactamente una
tiene `surface: direct_api`, esa es la que se muestra. No es una
preferencia editorial entre proveedores — es que la API propia del
proveedor del modelo no tiene ningún par comparable (no hay otro
`direct_api` compitiendo por el mismo modelo), a diferencia de
Bedrock/Vertex/Foundry, que sí son pares entre sí y por eso nunca se
eligen uno sobre otro acá. **Cierre de la pasada final — requisito de
`status: confirmed` agregado:** sin esto, una ruta con evidencia
`account_dependent`/`region_dependent`/`not_determined` podía terminar
ocupando `highlighted_route` con la redacción anterior, contradiciendo
directamente lo que 5.2.2 ya dice sobre `not_determined` ("se muestra
igual, pero nunca ocupa el resumen corto"). Transparencia total sigue
intacta — la ruta con evidencia más débil sigue apareciendo en la
lista completa (Nivel 2), simplemente no se destaca como si fuera la
recomendación segura. Si no hay un `direct_api` confirmado únicamente
elegible, o si hay más de una ruta `currently_eligible`+`confirmed` sin
que `direct_api` desempate (ej. un modelo sin API propia), el resumen
**no elige una** — muestra un conteo neutro:

```text
Acceso recomendado
──────────────────
3 formas de acceso disponibles

[Ver todas las opciones de acceso]
```

Si no hay ninguna ruta `currently_eligible`, se repite la misma lógica
(incluido el requisito de `status: confirmed`) sobre el bucket
`requires_onboarding` (una sola `direct_api` confirmada → se nombra con
su caveat de onboarding; si no, conteo neutro). Si tampoco hay rutas en
`requires_onboarding` (todo quedó `not_available`), estado explícito —
ver 5.4.

**Nivel 2 — lista expandible, "Ver todas las opciones de acceso":**

```text
Todas las opciones de acceso

✓ Anthropic API
  Disponible ahora
  [Cómo acceder]

→ AWS Bedrock
  Requiere cuenta AWS
  [Cómo acceder]

→ Google Cloud
  Requiere proyecto + billing
  [Cómo acceder]

→ Microsoft Foundry
  Requiere Azure
  [Cómo acceder]
```

Todas las rutas no-`not_available` del modelo ganador, agrupadas por
estado de elegibilidad (`currently_eligible` primero, luego
`requires_onboarding`), en orden estable dentro de cada grupo (mismo
mecanismo alfabético por `route_id` que ya se documentó como
presentation-order only — sigue siendo válido para *ordenar una lista
completa*, ya no para *elegir un ganador*, que es la diferencia real
que corrigió esta revisión). Cada fila linkea a `access.guide_ref`
(ver 5.4) — nunca a evidencia cruda sin explicación.

Mismo patrón visual que ya usa el proyecto para "Also strong options" /
"Outranked": transparencia completa de las opciones reales, sin
esconder ninguna, sin fingir que la lista completa es ruido.

### 3.6 Qué no implementar ni afirmar todavía

- No convertir Plus/Pro/Ultra/Claude/ChatGPT/AI credits en "X tokens
  de API".
- No usar `has_free_access` como sinónimo de producción, automatización
  o cuota garantizada — sigue siendo lo angosto que ya es.
- No presentar valores de rate limit de un dashboard de cuenta como
  documentación universal.
- No afirmar que un modelo disponible en ChatGPT/Claude App/AI Studio
  esté disponible por API, Bedrock, Vertex o NIM sin fuente propia por
  superficie.
- No afirmar que Bedrock soporta hoy todo modelo de Anthropic/OpenAI/
  Meta sólo porque exista una entrada histórica de blog.
- No estimar costo de NIM self-hosted desde una tabla de precios
  tokenizada de otro proveedor.
- No volver a aplanar Access/Eligibility/Economics en un solo campo o
  un solo booleano de conveniencia — son tres ejes independientes (3.1),
  y la especificación de 3.2 los mantiene en bloques separados a
  propósito. Si una implementación futura los junta "para simplificar",
  eso es exactamente la regresión que esta revisión corrigió.
- **No cambiar el ganador del motor por la suscripción declarada en
  v1.** La suscripción sólo cambia qué rutas se muestran y sus
  caveats — nunca el `Recommendation` de calidad/costo.
- **No reintroducir un ranking o desempate editorial entre rutas.**
  Fue diseñado (5.2.2, versión anterior de este documento), discutido
  a fondo, y **revertido deliberadamente** en esta misma sesión — no
  por falta de rigor, sino porque el proyecto ya tiene un mecanismo
  mejor para este problema (mostrar la lista completa, sin elegir un
  ganador) y no hacía falta inventar uno nuevo. Si alguien reabre esto,
  que lea primero por qué se sacó, no solo que se sacó.

---

## Parte 4 — Validación, caveats abiertos y orden de entrega

### 4.1 Fuente OpenAI — re-verificada y cerrada

La primera entrega de Codex citaba esta fuente con un sufijo de query
string corrupto (`%2525...` repetido decenas de veces). El dueño del
proyecto aportó la URL limpia
(`https://help.openai.com/en/articles/8156019-is-api-usage-included-in-chatgpt-subscriptions-even-if-i-have-a-paid-chatgpt-account`)
en la entrega editada de Codex, y Claude Code la verificó por su
cuenta, en vivo, contra el HTML real de la página (no contra el
snapshot de Codex): título de página *"How can I move my ChatGPT
subscription to the API?"*, con la cita textual exacta —

> "Our API service is billed and managed separately to ChatGPT. You'll
> be able to upgrade your API service to pay-as-you-go by adding a
> payment method in your API account billing settings."

Confirma directamente la fila 3.6/sección 4 ("no convertir Plus/Pro/
Ultra/ChatGPT en tokens de API") y el punto 3 del resumen ejecutivo de
la Parte 2 ("La separación está confirmada explícitamente"). Estado
final: `confirmed`, fuente cerrada — sin pendientes de re-verificación
en esta auditoría.

### 4.2 Escenarios a probar cuando exista implementación (de `PLAN.md`, sin resolver acá)

- Sin suscripción + prototipo.
- Pro/Ultra + prototipo.
- Suscripción + automatización.
- API con billing + carga intensiva.
- Claude/OpenAI con plan personal.
- NIM y Bedrock.

Verificar en cada uno que el ranking de `Recommendation` no cambie, y
que ningún claim de costo/uso quede sin respaldo — mismo criterio que
ya aplica el proyecto a "Also strong options" y al Budget redesign.

### 4.3 Orden de entrega (de `PLAN.md`, confirmado como todavía vigente)

1. Auditoría + evidencia — **completa con este documento** (5
   proveedores, taxonomía consistente, matriz cruzada).
2. Especificación de datos/reglas/UI — **completa con la Parte 3** de
   este documento.
3. Implementación — explícitamente pendiente. `PLAN.md` la condiciona
   a que la rama actual esté estabilizada y validada manualmente; según
   `HANDOFF.md` (`main` @ `d2047b5`, 103/103 tests, merge+push
   confirmados) esa condición ya se cumple. **No se implementó nada de
   código en esta sesión** — queda para que el dueño del proyecto decida
   explícitamente arrancarla, en una sesión/branch propia, siguiendo el
   mismo patrón de las sesiones de research previas (`Implementation`
   branch, o uno nuevo desde `main`).

---

## Parte 5 — Decisiones de arquitectura pendientes, en 4 bloques

Tras revisar la especificación de la Parte 3 contra el código real de
`decision/` e `interfaces/web/`, quedaron 10 decisiones concretas sin
cerrar. El dueño del proyecto las agrupó en 4 bloques, en orden de
dependencia (cada bloque necesita las decisiones del anterior para ser
resoluble) — **implementación explícitamente en pausa** hasta cerrar
los 4.

### 5.0 Confirmado: Access Advisor es un subsistema que se enchufa, no una reforma del motor

```text
Context
   ↓
Decision Evaluator      (sin cambios)
   ↓
Modelo ganador
   ↓
Explainer                (sin cambios)
   ↓
Recommendation           (objeto existente, sin cambios)
   │
   │   interfaces/web/app.py orquesta el llamado siguiente —
   │   Explainer nunca invoca a Access Advisor directamente
   ↓
┌───────────────────────────┐
│      ACCESS ADVISOR       │  ← subsistema nuevo, decision/access/
│                           │
│ routes + subscriptions    │
│ eligibility + billing     │
│ mode + workload + region  │
│ eligibility grouping      │  ← nunca ranking entre rutas (5.2.2)
└─────────────┬─────────────┘
              ↓
       Access Recommendation
              ↓
             UI
```

`Decision Evaluator` sigue respondiendo "¿qué modelo es el mejor para
este usuario?"; Access Advisor responde una pregunta distinta, "¿cuál
es la mejor manera de acceder a ese modelo, para este usuario?" —
mismo principio que ya sostiene la separación `Recommendation` (calidad)
vs. `also_strong_options`/`Outranked` (transparencia de ranking): dos
preguntas, dos objetos, un solo flujo de datos, sin retroalimentación
del segundo hacia el primero.

**Restricción estructural nueva, que responde directamente la pregunta
"¿cómo garantizamos que no toca `evaluator`?" del Bloque 3 sin depender
de disciplina humana:** `decision/access/` puede importar
`decision/domain/` (el `AIModel`, y los tipos propios de Access
Advisor) pero **nunca** `decision/evaluator/` ni los internals de
scoring. Igual que el hard constraint ya existente
"`decision/` nunca importa de `interfaces/`", pero aplicado como un
límite interno nuevo dentro de `decision/` mismo. Si `decision/access/`
alguna vez necesita algo de `Candidate` o del cálculo de score, es una
señal de que se está filtrando la pregunta equivocada hacia el
subsistema equivocado — no una razón para relajar el límite. **Nota de
la pasada final (2026-08-11):** el cierre de 5.3 terminó siendo más
estricto todavía que este párrafo original — `recommend_access` recibe
`AIModel` directamente, ni siquiera `Recommendation` — corregido acá
para que 5.0 no quede prometiendo un acceso más amplio del que 5.3
finalmente cerró.

### 5.1 Bloque 1 — Identidad y datos

**Cerrado en esta revisión: matching modelo↔ruta = ID exacto, no `family`.**

`access_routes/{provider}/{route_id}.yaml` debe referenciar siempre un
`model_id` que sea un `id` real y existente de `dataset/models/` —
nunca un nombre de familia agregado ("Claude family", "Gemini API
models"). Decisión tomada explícitamente en contra de agregar un campo
`family` a `SCHEMA.md`, por la misma razón de fondo que ya gobierna el
resto del proyecto: family-matching es una capa de inferencia implícita
(“esta fila aplica mágicamente a estos cinco modelos”), exactamente lo
que "nunca fabricar precisión" y la política de sourcing de
`dataset/models/` existen para evitar. El nombre del campo (`model_id`,
no `model_or_family`) se corrigió en el cierre del Bloque 3 (5.3) para
que el contrato no arrastre una opción que ya se descartó — nada de
"family" escondido esperando volver. Consecuencias concretas, aceptadas
a propósito:

- Más filas por proveedor (una por modelo, no una por familia) — costo
  de mantenimiento asumido conscientemente, no un descuido.
- El loader nuevo de `access_routes/` gana una regla de integridad
  referencial mecánica: `model_id` debe matchear un `id`
  existente en `dataset/models/`, mismo espíritu que la regla ya
  existente "`id` debe ser único y matchear el nombre del archivo".
- **Vía de escape ya acordada, no abierta a discusión ad-hoc:** si en
  la práctica mantener una fila por modelo resulta insostenible, eso
  sería evidencia real y repetida (el mismo criterio del "2-3 veces
  antes de proponer un cambio a `SCHEMA.md`" que ya rige el resto del
  proyecto) — recién ahí se reconsidera `family` como evolución de
  schema, con los datos de esa fricción como justificación, no antes.

**Cerrado — región: un solo campo, `country`, sin `cloud_region` en
v1.** Ver la fila `country` en 3.3 para la definición completa y el
razonamiento (mismo problema que ya se rechazó para rate limits: sin
fuente estable/determinística para matching de región cloud
específica, ese dato queda en `caveat`, nunca en un campo que el
sistema pretenda "verificar").

**Hueco encontrado en la pasada final (2026-08-11) y cerrado acá —
`country` no tiene, hoy, contra qué matchear.** `AccessRoute` no tiene
ningún campo tipo `supported_countries`/`excluded_countries` —
`eligibility.region_scope` es una clasificación gruesa
(`account_dependent`/`region_dependent`/`global`/`not_determined`), no
una lista comparable contra el `country` del usuario. Mismo problema en
`SubscriptionPlan.region_scope`, que es un string libre, no una lista.
Dos caminos posibles, evaluados:

- **(A, elegido para v1):** no inventar un campo nuevo. `country` sigue
  existiendo en `AccessContext` — se recolecta y se muestra junto al
  `caveat` de la ruta cuando corresponde — pero **no participa en
  matching de elegibilidad todavía**. Ninguna ruta pasa a
  `requires_onboarding` ni a `not_available` por el `country`
  declarado; la incertidumbre de región queda comunicada en texto
  (`caveat`), nunca decidida por el sistema. Se agrega matching real el
  día que una ruta concreta incorpore evidencia estructurada y estable
  por país — con esa evidencia como justificación, no antes.
- **(B, descartado):** agregar `supported_countries`/`excluded_countries`
  a `AccessRoute` ahora. Rechazado por la misma razón que ya se aplicó
  a `cloud_region`: no agregar estructura "por si algún día hace
  falta" sin evidencia concreta que lo exija.

**Consecuencia directa, que corrige también la definición de
`not_available` en 5.2.1:** "región no cubierta" **no es, en v1, un
mecanismo computable** — el Advisor no tiene con qué decidirlo
mecánicamente. El único disparador real y estructural de
`not_available` en v1 es `enterprise_governance` sin opt-in explícito
del usuario. Cualquier incertidumbre de región/país se comunica
siempre como `caveat`, nunca mueve una ruta a `requires_onboarding` ni
a `not_available`.

**Cerrado en 5.4 — `satisfies_requirements` eliminado de
`subscriptions/*.yaml`.** La relación es unidireccional: la ruta
declara qué `plan_id` la resuelven (`consumer_subscription.value`), el
plan nunca declara qué rutas resuelve. Ver 5.4 para el detalle
completo. Con esto, **Bloque 1 queda 100% cerrado, sin pendientes.**

### 5.2 Bloque 2 — Motor de decisión

#### 5.2.1 Cerrado: vocabulario de `requirements` + elegibilidad de tres estados

**El vocabulario cerrado.** `eligibility.requirements` deja de ser
string libre — pasa a ser una lista de objetos tipados, `kind` de un
enum cerrado (validado por el loader) + `value` opcional según el
`kind`:

```text
RequirementKind (enum cerrado):

  api_billing_linked
    Sin valor. Google Cloud Billing, OpenAI "API billing settings" +
    payment method, Anthropic billing por uso.
    Contexto: has_api_billing: boolean/unknown

  cloud_account
    Valor: aws | gcp | azure.
    Bedrock (cuenta AWS), Vertex (proyecto GCP), Claude Platform on
    AWS/Google Cloud/Microsoft Foundry.
    Contexto: cloud_accounts (membership)

  consumer_subscription
    Valor: lista de plan_id de subscriptions/*.yaml (any-of) —
    lista porque el único caso confirmado (Google, AI Studio) es
    "Pro O Ultra", no un plan único.
    Contexto: subscriptions (intersección)

  program_membership
    Valor: string (ej. "nvidia_developer_program").
    Único caso confirmado hoy: NVIDIA Developer Program. Regla de
    disciplina: un proveedor nuevo no suma un `value` a este kind sin
    evidencia propia de que esa membership es real — mismo estándar
    de sourcing que el resto del proyecto, no se generaliza por
    analogía con NVIDIA.
    Contexto: program_memberships (NUEVO campo en 3.3)

  gpu_infrastructure
    Sin valor. Único caso confirmado: NIM self-hosted.
    Contexto: has_gpu_infrastructure (NUEVO campo en 3.3) — definido
    angosto a propósito: "infraestructura compatible/disponible para
    correr NIM", no "tiene alguna GPU". No intenta capturar modelo/
    VRAM/cantidad; esa granularidad se agrega solo si la evidencia lo
    exige, mismo criterio que ya gobierna todo lo demás en este
    documento.
```

**Deliberadamente afuera del vocabulario**, con la razón puntual:
enterprise/contract-only ya se representa vía
`access.capabilities: enterprise_governance` (3.2), no necesita un
`RequirementKind`; Marketplace EULA (Bedrock) es procedural, no
gating (ver el corte de abajo); API usage tier (OpenAI 1-5, "cuentas
nuevas por debajo del standard tier" en Anthropic) es dinámico/
`account_dependent`, se muestra como caveat informativo, nunca como
gate; región se representa mediante el eje `country`, cerrado en 5.1 —
no participa en matching de elegibilidad en v1 (ver el hueco encontrado
y cerrado en la pasada final, misma sección), nunca un `RequirementKind`.

**La corrección de diseño real de esta sesión — de binario a tres
estados.** La primera versión de este vocabulario asumía que un
`requirement` no cumplido descartaba la ruta. El dueño del proyecto (y
una segunda opinión externa, GPT, consultada por él) señalaron
correctamente que esto es un error de modelado, no un detalle: "no
tener cuenta AWS" y "no tener infraestructura GPU propia" son
fricciones de clase completamente distinta para el público real de
Model Compass (developers/entusiastas — ver `VISION.md`, sección
"Users") — la primera es un signup self-serve de minutos, la segunda
es una decisión de infraestructura/capital. Tratarlas igual habría
sacado a Bedrock del radar solo por asumir pereza que la evidencia no
sostiene.

**Reencuadre final, cerrado en la pasada de consistencia (2026-08-11)
— "access state", no examen de elegibilidad.** El mismo razonamiento
que salvó a Bedrock aplica igual de limpio al caso más común de todos:
una API key. Si `Claude API` requiere `api_billing_linked` y el
usuario no lo declaró, la ruta no es "el usuario no calificó" — es
"esta ruta existe, y para usarla hace falta esto". La pregunta que
responde `RouteEligibilityState` no es *"¿puede usarlo ahora mismo?"*
sino *"¿puede acceder directo, o primero necesita completar algún
paso?"* — la misma distinción, dicho distinto, pero vale la pena
dejarlo explícito porque cambia el tono de la UI: nunca "no calificás
para esto", siempre "esto es lo que necesitás y por dónde conseguirlo".
Ejemplo, el mismo patrón para cualquier `requirement`:

```text
Claude API
🔑 Requiere una API key.
Podés obtenerla desde la plataforma de Anthropic.
[Cómo obtener tu API key →]
```

No cambia ninguna mecánica ya cerrada (siguen siendo los mismos dos
estados vivos + `not_available`, el mismo vocabulario de 5.2.1) — es la
forma de comunicarlo, y la razón por la que `requires_onboarding` es el
nombre correcto y no algo como `ineligible`.

**La corrección, generalizada, no parcheada por proveedor:** ningún
`requirement` descarta una ruta por sí solo. En cambio, cada ruta
recibe un estado de elegibilidad de tres valores, evaluado contra el
contexto del usuario:

```text
route_eligibility(route, user_context):

  currently_eligible    el usuario cumple el 100% de los requirements
                         de la ruta ahora mismo

  requires_onboarding    falta uno o más requirements, pero son
                          self-serve (crear cuenta, sumar billing,
                          sumar GPU, unirse a un programa) — la ruta
                          SIGUE viva, nunca se oculta

  not_available          en v1, un único disparador real y
                          computable: ruta `enterprise_governance`
                          sin que el usuario pida explícitamente ver
                          rutas enterprise — depende de un proceso de
                          ventas del proveedor, no de un signup
                          determinístico, categóricamente distinto de
                          "no lo intentó todavía". "Región no
                          cubierta" NO es, en v1, un mecanismo
                          computable — ni `AccessRoute` ni
                          `SubscriptionPlan` tienen una lista de países
                          comparable contra `country` (hueco
                          encontrado y cerrado en la pasada final,
                          ver 5.1); toda incertidumbre de región queda
                          en `caveat`, nunca decide este estado.
```

Ningún `requirement` individual decide "más difícil" que otro —
eso sería inventar un friction score sin fuente, lo mismo que ya
rechazó el proyecto para rate limits y para RPM/TPM. Lo que sí hay,
cuando la evidencia lo da (como el precio real de NVIDIA AI Enterprise,
~USD 4.500/GPU/año), es texto concreto en `caveat` — nunca un booleano
de "esto es más pesado".

**Regla operacional cerrada en la pasada final — qué hace `None`
("unknown") en `AccessContext`.** `has_api_billing`/
`has_gpu_infrastructure` son `bool | None` (3.3, 5.3); faltaba decir
qué pasa cuando un `requirement` necesita uno de esos campos y el
usuario no lo declaró. Regla, deliberadamente la más simple posible:
**`None` nunca equivale a `True`.** Si un `requirement` no puede
confirmarse como cumplido por falta de dato del usuario, la ruta queda
en `requires_onboarding`, con ese `requirement` incluido en
`unmet_requirements` — igual que si el usuario hubiera declarado
explícitamente que no lo tiene. Nunca se infiere que sí lo tiene por
default, y la ruta tampoco desaparece por la falta de dato — mismo
principio de "no inventar, no ocultar" que ya gobierna el resto de
5.2.1.

**Consecuencia directa para la presentación (no para un ranking — ver
5.2.2, revertido):** `currently_eligible` se agrupa y se muestra antes
que `requires_onboarding` en la lista de 3.5; `not_available` queda
excluido del conjunto por completo, nunca se muestra ni se compara.

#### 5.2.2 Revertido: ranking/desempate entre rutas — reemplazado por lista completa sin ganador

**Historial, a propósito no borrado — ver por qué se sacó, no solo que
se sacó.** La primera versión de esta sección diseñó un desempate de 4
criterios (match contra datos declarados, cobertura de `capabilities`
por `use_mode`, cobertura por `workload_type`, fuerza de
`evidence.status`) más un campo `also_equivalent_routes` para los
empates que sobrevivían a los 4. El diseño era correcto en su momento
— cada criterio tenía justificación observable, nunca un ranking de
proveedores — pero resolvía un problema que existía únicamente porque
el propio diseño insistía en elegir **una** ruta como "Best way to
access" entre pares estructuralmente equivalentes (AWS Marketplace vs.
Google Cloud vs. Microsoft Foundry, mismo modelo, mismo `surface`).

**La corrección real de esta sesión: dejar de insistir en elegir una.**
El dueño del proyecto (con una segunda opinión externa) notó que el
proyecto ya tiene un mecanismo mejor para este problema exacto —
transparencia total en vez de un ganador forzado, el mismo principio
que ya sostiene `Outranked`/`also_strong_options` para el ranking de
modelos. Aplicado acá: Access Advisor **no rankea rutas entre sí**.
Muestra el conjunto completo (agrupado solo por el estado de 5.2.1,
nunca ordenado por preferencia dentro de un grupo más allá del orden
estable de presentación), y dejar que el usuario elija según lo que
ya sabe de sí mismo (qué cuenta tiene, qué le resulta más cómodo) —
que Access Advisor no tiene forma de adivinar sin inventar criterio.

**Qué se elimina, explícitamente, de este documento:**

- Los 4 criterios de desempate entre rutas.
- `also_equivalent_routes` como campo de `AccessRecommendation` — ya
  no hace falta, no hay "ganador" del que algo sea "también
  equivalente".
- La tabla de mapeo `use_mode` ↔ `capabilities` **como mecanismo para
  elegir una ruta** — ver el punto siguiente, sigue existiendo un uso
  para `capabilities`, pero es informativo, no decisorio.

**Qué se conserva:** la regla de aislamiento por estado de
elegibilidad (nunca comparar/mezclar `currently_eligible` con
`requires_onboarding` — siguen siendo grupos separados, ver 3.5 Nivel
2), el orden estable por `route_id` dentro de cada grupo (para que la
lista no cambie de orden entre corridas sin motivo — presentación
únicamente, nunca aparece como criterio en ningún texto explicativo),
y el criterio 4 original (`evidence.status`) reaparece en 3.5 como
regla simple: rutas `not_determined` se muestran igual (transparencia),
pero nunca ocupan el resumen corto de Nivel 1.

#### 5.2.3 `capabilities` pasa de criterio de ranking a metadata informativa — sin tabla de mapeo pendiente

Con el ranking eliminado, la tabla `use_mode` ↔ `capabilities` que
figuraba como el ítem más importante de este bloque **deja de ser
necesaria para v1**. `access.capabilities` (por ruta, ya sourceado en
3.2) se muestra tal cual en la lista expandida de 3.5 — el usuario que
declaró `use_mode: automation` puede leer directamente qué rutas
listan `automation` entre sus capabilities, sin que el sistema decida
por él. Si en el futuro hay evidencia real de que los usuarios
necesitan filtrado automático (no solo lectura), ahí se construye la
tabla — con evidencia de uso real, mismo criterio de "2-3 veces antes
de construir" que rige el resto del proyecto.

**Alcance de ejecución, sin cambios respecto a la versión anterior:**
el Advisor corre **solo sobre el modelo ganador**
(`Recommendation.recommended`), no sobre `alternatives` ni
`also_strong_options` en v1 — consistente con la nueva UX de 3.5 (un
resumen + una lista, por modelo, no por cada alternativa de modelo).

### 5.3 Cerrado: contrato de `decision/access/` — layout, firma, límites, loader

Derivado del código real (`decision/domain/context.py`, `ai_model.py`,
`candidate.py`, `recommendation.py`, los `errors.py` de loader/
explainer, `interfaces/web/context_form.py`, `interfaces/web/app.py`),
no diseñado en el vacío. Diseño de contrato — **nada de esto se
implementó, es la especificación que va a guiar la implementación
cuando arranque**.

**Layout, mismo patrón que `decision/domain/`/`decision/loader/`:**

```text
decision/domain/access_context.py        # AccessContext + UseMode/WorkloadType/
                                          # Intensity/CloudProvider
decision/domain/access_route.py          # AccessRoute + Access/Eligibility/
                                          # Economics/Evidence, RequirementKind,
                                          # AccessRequirement
decision/domain/access_recommendation.py # RouteEligibilityState, RouteEntry,
                                          # AccessSummary, AccessRecommendation
decision/domain/subscription.py          # SubscriptionPlan

decision/access/__init__.py              # re-exporta recommend_access
decision/access/advisor.py               # recommend_access(...)

decision/loader/access_loader.py         # load_access_routes(), load_subscriptions(),
                                          # validate_route_references() —
                                          # reusa DatasetValidationError tal cual
```

Todos frozen `@dataclass`, enums `str, Enum` — mismo estilo que
`ai_model.py`/`context.py`, cero convención nueva.

**`AccessContext`** (`decision/domain/access_context.py`):

```python
class UseMode(str, Enum):
    MANUAL = "manual"
    PROTOTYPE = "prototype"
    API_INTEGRATION = "api_integration"
    AUTOMATION = "automation"

class WorkloadType(str, Enum):
    EXPLORATORY = "exploratory"
    INTERACTIVE = "interactive"
    BATCH = "batch"
    AGENTIC = "agentic"

class Intensity(str, Enum):
    OCCASIONAL = "occasional"
    FREQUENT = "frequent"
    INTENSIVE = "intensive"

class CloudProvider(str, Enum):
    AWS = "aws"
    GCP = "gcp"
    AZURE = "azure"

@dataclass(frozen=True)
class AccessContext:
    use_mode: UseMode
    workload_type: WorkloadType
    intensity: Intensity
    country: str | None                      # ISO 3166-1 alpha-2, None = unknown
    subscriptions: tuple[str, ...]            # plan_id de subscriptions/*.yaml
    has_api_billing: bool | None              # None = unknown, no False
    cloud_accounts: tuple[CloudProvider, ...]
    program_memberships: tuple[str, ...]
    has_gpu_infrastructure: bool | None       # None = unknown
```

`bool | None` para "unknown" — mismo patrón que `Context.budget:
BudgetLevel | None` con `BudgetMode.CUSTOM`, no un tercer estado
inventado.

**`AccessRecommendation`** (`decision/domain/access_recommendation.py`):

```python
class RouteEligibilityState(str, Enum):
    CURRENTLY_ELIGIBLE = "currently_eligible"
    REQUIRES_ONBOARDING = "requires_onboarding"
    # NOT_AVAILABLE no aparece acá -- se descarta en el advisor (5.2.1),
    # nunca llega a un RouteEntry

@dataclass(frozen=True)
class RouteEntry:
    route: AccessRoute
    state: RouteEligibilityState
    unmet_requirements: tuple[AccessRequirement, ...]  # vacío si currently_eligible

@dataclass(frozen=True)
class AccessSummary:
    """Lo que muestra el 'Acceso recomendado' corto -- ver 3.5."""
    highlighted_route: AccessRoute | None       # None = sin match único, mostrar conteo --
                                                 # solo candidata si evidence.status ==
                                                 # confirmed (cerrado en la pasada final)
    bucket_state: RouteEligibilityState | None  # de qué bucket sale; None = sin rutas
    bucket_size: int

@dataclass(frozen=True)
class AccessRecommendation:
    model: AIModel
    routes: tuple[RouteEntry, ...]  # not_available ya excluidas; currently_eligible
                                     # primero, luego requires_onboarding; orden
                                     # alfabético por route_id dentro de cada grupo
    summary: AccessSummary
```

Sin excepción tipo `NoQualifyingModelsError` — a diferencia del
Explainer, "cero rutas para este modelo" es un estado esperado y
frecuente mientras el catálogo crece, no una salida excepcional. Se
representa como `AccessRecommendation(routes=(), summary.bucket_state=None)`,
nunca una excepción — mismo estado explícito que ya define 5.4.

**La firma:**

```python
def recommend_access(
    model: AIModel,
    context: AccessContext,
    routes: list[AccessRoute],
    subscriptions: list[SubscriptionPlan],
) -> AccessRecommendation:
```

Deliberadamente más estricta que el mínimo fijado en 5.0: recibe
`AIModel`, **no** `Recommendation` — `decision/access/` ni necesita
saber que `decision/domain/recommendation.py` existe. `routes`/
`subscriptions` son los catálogos **completos**; el advisor filtra por
`route.model_id == model.id` internamente, mismo patrón que
`evaluate(context, models)` recibe todo el dataset y filtra/puntúa
adentro.

**Límite de importación, con archivos concretos:** `decision/access/`
puede importar `access_context.py`, `access_route.py`,
`access_recommendation.py`, `subscription.py`, y `ai_model.py` (por el
tipo `AIModel`). **Nunca** `decision/evaluator/`, `decision/explainer/`,
ni `candidate.py`/`recommendation.py` (no hacen falta, ver arriba). Dato
verificado contra el repo real: **hoy no existe ningún test
automatizado** para el límite ya existente `decision/` ↔ `interfaces/`
— se sostiene solo por disciplina/code review. Cuando se implemente,
sumar un test de arquitectura chico (chequeo de imports por AST o grep
sobre `decision/access/*.py`) — protección estructural, no algo que
Access Advisor necesite funcionalmente para andar. Sería el primer test
de este tipo en el proyecto, precedente reusable para el límite
`decision/`↔`interfaces/` también, si se quiere extender después.

**El loader — contrato, con la responsabilidad separada del advisor
(segundo ajuste de esta revisión):**

```python
def load_access_routes(directory: Path) -> list[AccessRoute]: ...
def load_subscriptions(directory: Path) -> list[SubscriptionPlan]: ...
def validate_route_references(routes: list[AccessRoute], models: list[AIModel]) -> None: ...
    # raise DatasetValidationError si algún route.model_id no existe
    # en {m.id for m in models}
```

`load_access_routes`/`load_subscriptions` validan estructura (mismo
rigor que `load_model_file`: campos requeridos, enums válidos,
`raise DatasetValidationError(path, issues)` reusado tal cual de
`decision/loader/errors.py`, sin excepción nueva). La integridad
referencial cruzada (¿existe `claude-opus-4-8` en `dataset/models/`?)
es una responsabilidad separada, explícita, del loader/boot —
**nunca** del advisor:

```text
loader (boot)
  ├── valida estructura YAML de cada catálogo
  └── valida referencias cruzadas (validate_route_references)

advisor (por request)
  └── consume datos ya validados — no verifica que un model_id exista,
      lo asume
```

`recommend_access()` queda deliberadamente "tonto" — no le preocupa si
`claude-opus-4-8` existe, eso ya se garantizó antes de que el catálogo
llegara a sus manos. Carga en boot, no por request — mismo patrón que
`models = load_dataset(DATASET_DIR)` en `app.py:41`.

**Orquestación en `app.py` — el punto exacto, una línea nueva:**

```python
candidates = evaluate(context, models)          # sin cambios
recommendation = explain(context, candidates)    # sin cambios
access = (
    recommend_access(recommendation.recommended, access_context, access_routes, subscriptions)
    if recommendation else None
)
```

Tres preguntas, tres responsabilidades, ninguna invade a la otra:
Evaluator decide qué modelo, Explainer explica por qué, Access Advisor
explica cómo acceder. `evaluate()`/`explain()` quedan literalmente
intactos — confirmado contra el código real, no solo el diagrama de 5.0.

### 5.4 Cerrado: subscriptions data-driven + freshness de evidencia

#### 5.4.1 `SubscriptionPlan` — estructura final y relación con `AccessRoute`

Ya escrita en 3.2 tras esta revisión (`satisfies_requirements`
eliminado). Resumen de la relación, la pregunta central del bloque:

```text
subscriptions/*.yaml
        ↓ load_subscriptions()
SubscriptionPlan[]
        ↓
   interfaces/web/  (form: opciones data-driven, ver 5.4.2)
        ↓
   AccessContext.subscriptions  (plan_id declarados por el usuario)
        ↓
recommend_access(model, context, routes, subscriptions)
        ↓ matching contra access_routes.eligibility.requirements
          [kind=consumer_subscription].value  (lista de plan_id)
   AccessRecommendation
```

**La duplicación se elimina — veredicto sobre el punto 4:** la
relación queda **unidireccional**. `access_routes` declara qué
`plan_id` resuelven cada requisito (`consumer_subscription.value`, ya
existía); `subscriptions/*.yaml` **no** vuelve a declarar qué rutas
resuelve. `SubscriptionPlan.surface_entitlements`/`documented_exclusions`
quedan, pero se degradan de "mecanismo de matching" a **informativo
puro** — texto para mostrar "qué te da este plan en general" (útil
para "What your subscription does/does not cover" en 3.5), nunca
consultado por `recommend_access()` para decidir estado de
elegibilidad. Esa decisión la toma enteramente el lado de la ruta. No
hay necesidad concreta detectada para mantenerla en los dos catálogos
a la vez — se sacó.

**Validación referencial, extiende lo ya cerrado en Bloque 3:**
`validate_route_references()` (5.3) gana un segundo chequeo — todo
`plan_id` listado en cualquier `consumer_subscription.value` debe
existir en el catálogo de `SubscriptionPlan` cargado, mismo mecanismo
que ya valida `model_id` contra `dataset/models/`. Sigue siendo
responsabilidad del loader/boot, nunca del advisor.

#### 5.4.2 De dónde salen las opciones del formulario

**Cerrado: 100% data-driven, cero hardcodeo.** Mismo patrón que ya usa
el proyecto — `providers = sorted({model.provider for model in
models})` en `app.py:43`, `USE_CASES` en `use_cases.py`. Un
`subscriptions = load_subscriptions(SUBSCRIPTIONS_DIR)` a nivel módulo
en `app.py` (boot, junto a `access_routes`, ya cerrado en 5.3), y las
opciones del formulario (agrupadas por `provider`, etiquetadas por
`plan_name`) se derivan de esa lista en el momento de armar el
contexto — nunca una lista escrita a mano en una plantilla o en
`interfaces/web/`. Si mañana aparece un plan nuevo de cualquier
proveedor, es un YAML nuevo en `dataset/subscriptions/` — cero cambios
de código o de UI.

#### 5.4.3 Freshness de `evidence.consulted_at` — comportamiento concreto

**Lo que SÍ hace la UI:** muestra `consulted_at` tal cual, junto a
`source_url`, en cada ruta de la lista expandida (3.5) — un dato
real, no interpretado. El usuario decide por sí mismo si una fecha le
resulta vieja, con la misma disciplina de transparencia que ya aplica
`docs/models/{id}.md`. Sumado a esto, un **disclaimer fijo, no
condicional a la edad del dato**, visible una sola vez en la sección
de Access Advisor (no por ruta): algo del orden de *"El acceso y la
elegibilidad pueden cambiar — confirmá los términos vigentes en la
fuente oficial antes de depender de esto en producción."* Aparece
siempre, independientemente de qué tan reciente sea `consulted_at` —
resuelve la advertencia sin necesitar ningún umbral.

**Lo que NO hace freshness — explícito, punto 6:**

- **No hay downgrade automático de `status` por edad.** Nunca
  `if consulted_at < N days: status = not_determined` ni nada
  parecido — eso inventaría un umbral de significancia temporal sin
  evidencia de que N días sea el número correcto para ningún
  proveedor, mismo tipo de fabricación que "nunca fabricar precisión"
  ya prohíbe para rate limits.
- **No hay score ni porcentaje de frescura.** Nada de "85% fresh" —
  mismo rechazo ya aplicado a "Recommendation Confidence" en
  `FEATURES.md` (una escala continua inventada sobre un dato que no la
  sostiene).
- **Ninguna ruta se oculta ni se degrada de estado por tener evidencia
  vieja.** El estado de elegibilidad (5.2.1) depende de si el usuario
  cumple los requisitos, no de cuándo se verificó la fila — son ejes
  independientes, mezclarlos sería repetir el error que ya corregimos
  una vez (Access/Eligibility/Economics, sesión anterior).
- **No se define un umbral universal de "viejo".** Si algún día hay
  evidencia real de que cierto tipo de dato (ej. pricing) queda
  obsoleto en un plazo predecible para un proveedor específico, esa
  señal se agrega con ese sourcing puntual — nunca como una regla
  genérica de "N días" aplicada a todo el catálogo.
- **Re-auditar el catálogo es proceso editorial, no una feature de
  producto.** Mismo tipo de disciplina que ya mantiene
  `docs/models/{id}.md` actualizado manualmente cuando aparece
  evidencia nueva — no hay mecanismo de expiración automática que
  reemplace ese trabajo humano, ni debería haberlo.

#### 5.4.4 El resto de Bloque 4, sin cambios de esta revisión

- Estado explícito de "sin ruta confirmada" cuando el conjunto de rutas
  del modelo ganador queda vacío (todo `not_available`, o el catálogo
  todavía no tiene filas para ese modelo) — mismo patrón ya usado para
  "No fair lower-cost swap" en el Lower-cost Alternative rediseñado
  (`HANDOFF.md`, sesión 8): nunca una card vacía ni una ruta dudosa
  mostrada como si fuera segura, un mensaje honesto de "no documentado
  todavía".
- **Nuevo, agregado en esta revisión — catálogo de guías de acceso:**

  ```text
  docs/access-guides/
      openai.md
      anthropic.md
      google.md
      aws-bedrock.md
      nvidia-nim.md
  ```

  Mismo patrón que `docs/models/{id}.md` — contenido curado, sourceado,
  con fecha, no un link externo suelto. Cada fila de `access_routes`
  referencia la sección exacta vía `access.guide_ref` (agregado a la
  Parte 3.2 en esta revisión) — la UI nunca adivina qué guía
  corresponde a qué ruta, ni linkea a evidencia cruda sin explicación.
  Falta decidir: ¿una guía por proveedor (como en el árbol de arriba)
  o una por superficie cuando un proveedor tiene varias rutas muy
  distintas (ej. Anthropic direct API vs. Claude Platform on AWS)?
  Probablemente lo segundo, dado que ya vimos que esas rutas piden
  cosas distintas — pero queda para cuando se escriba la primera guía
  real, no antes.

  **Profundidad cerrada en esta revisión — puntero curado, no tutorial
  paso a paso.** `VISION.md` ya lo dice, sin que Access Advisor tuviera
  que inventar la regla: *"Does not replace official provider
  documentation"* (línea 65) y *"Does not make the final decision for
  the user — it informs it"* (línea 69). Una guía dice **qué hace
  falta y por dónde entrar**, no reproduce cada click de la consola de
  cada proveedor — eso queda desactualizado apenas el proveedor
  rediseña su UI, y con 5+ proveedores es mantenimiento infinito para
  un dato que ya no sería "nunca fabricar precisión" sino "nunca dejar
  de mantener precisión". Forma esperada de una entrada:

  ```text
  Cómo acceder a Llama 3 mediante AWS Bedrock

  1. Crear/usar una cuenta AWS.
  2. Revisar disponibilidad del modelo en tu región — la
     disponibilidad varía por país, región y cuenta.
  3. Configurar los requisitos de Bedrock (IAM, Marketplace/EULA si
     corresponde).
  4. Seguir la documentación oficial: [enlaces sourceados].
  ```

  Y en la UI, el texto por ruta se queda corto a propósito:

  ```text
  Meta Llama 3
  Podés acceder mediante AWS Bedrock.
  Requiere una cuenta de AWS y configuración inicial.
  La disponibilidad puede variar según país, región y cuenta.
  [Cómo acceder →]
  ```

  Nada de "ahora hacé click acá, después esperá esto" — ese nivel de
  detalle, si alguna vez se justifica, es contenido de la guía citando
  la doc oficial, nunca texto que Model Compass mantiene como si fuera
  propio.

**Estado de esta revisión — los 4 bloques cerrados:**

- **Bloque 1** — matching por `id` exacto (`model_id`), vocabulario
  tipado de `requirements`, región como un solo campo `country` sin
  `cloud_region`. Sin pendientes.
- **Bloque 2** — elegibilidad de tres estados (5.2.1) firme; ranking/
  desempate entre rutas (5.2.2 original) diseñado, discutido y
  **revertido** deliberadamente a favor de mostrar la lista completa
  sin ganador forzado; `use_mode`↔`capabilities` bajado de criterio de
  ranking a metadata informativa (5.2.3). `PLAN.md` reconciliado con
  esta dirección (4 ediciones puntuales, `Downloads/PLAN.md`, no
  versionado en git).
- **Bloque 3** — layout de archivos, `AccessContext`/
  `AccessRecommendation` derivados del código real, firma de
  `recommend_access` (recibe `AIModel`, no `Recommendation`), límite de
  importación con archivos concretos, contrato del loader con
  validación referencial separada del advisor.
- **Bloque 4** — `SubscriptionPlan` sin `satisfies_requirements`
  (relación unidireccional, la ruta apunta al plan, nunca al revés),
  catálogo de suscripciones 100% data-driven en el formulario, guías de
  acceso (catálogo + profundidad de puntero curado), y freshness de
  evidencia resuelta sin ningún umbral inventado — se muestra la fecha
  real más un disclaimer fijo, nunca un downgrade automático de estado
  ni un score de "qué tan vieja" es la evidencia.

Con los 4 bloques cerrados, se hicieron **dos pasadas de auditoría de
consistencia** (2026-08-11) sobre el documento completo, ambas de
cierre — no de diseño nuevo:

- **Primera pasada:** encontró y corrigió 2 contradicciones reales en
  5.0 (el diagrama todavía decía `deterministic ranking`, y el límite
  de importación todavía permitía leer `Recommendation`) que quedaron
  stale después de que 5.2.2 revirtiera el ranking y 5.3 cerrara la
  firma final, más un ajuste chico de wording en 3.4.
- **Segunda pasada:** encontró y cerró 4 puntos más — dos frases
  muertas en 5.2.1 (región marcada como "pendiente" cuando ya estaba
  cerrada en 5.1; el ranking de 5.2.2 citado como "todavía abierto"
  cuando ya estaba revertido), un hueco técnico real (`country` no
  tenía, hasta esta pasada, ningún campo contra el cual matchear —
  resuelto con la Opción A: se recolecta pero no gatea nada en v1,
  toda incertidumbre de región queda en `caveat`, y esto además
  redefinió `not_available` para dejar un solo disparador real:
  `enterprise_governance` sin opt-in), la regla operacional de
  `None`/"unknown" en `has_api_billing`/`has_gpu_infrastructure`
  (nunca equivale a `True`, siempre `requires_onboarding`), la
  contradicción entre `highlighted_route` y la regla de 5.2.2 sobre
  `not_determined` (resuelta exigiendo `evidence.status: confirmed`
  para poder destacarse en el resumen corto), y el reencuadre final de
  "eligibility" como "access state" (misma mecánica, comunicación más
  honesta — nunca "no calificás", siempre "esto es lo que necesitás").

**Con esto, la especificación queda cerrada.** Próximo paso: crear una
rama de implementación desde `main`. Nada de código todavía.

**Nota de proceso, explícita:** esta revisión reemplaza contenido de
las Partes 3.4/3.5 escrito en sesiones anteriores de este mismo
documento (no de `PLAN.md`, que sigue intacto — ver Parte 4.3 para
cuándo se actualiza formalmente). El historial de qué se diseñó y por
qué se revirtió se conservó a propósito (5.2.2) en vez de borrarse,
mismo criterio que ya rige `INCIDENT_LOG.md`: no reescribir
retroactivamente sin dejar rastro de lo que realmente pasó.

---

## Fuentes

Todas consultadas 2026-08-11.

### Google

- https://ai.google.dev/gemini-api/docs?hl=es-419
- https://ai.google.dev/gemini-api/docs/models?hl=es-419
- https://ai.google.dev/gemini-api/docs/pricing?hl=es-419
- https://ai.google.dev/gemini-api/docs/billing?hl=es-419
- https://ai.google.dev/gemini-api/docs/rate-limits?hl=es-419
- https://ai.google.dev/gemini-api/docs/aistudio-agents
- https://ai.google.dev/gemini-api/docs/aistudio-build-mode
- https://ai.google.dev/gemini-api/docs/aistudio-deploying?hl=en
- https://ai.google.dev/gemini-api/docs/antigravity-agent
- https://support.google.com/googleone/answer/16105039?hl=en-en
- https://support.google.com/googleone/answer/14534406
- https://support.google.com/googleone/answer/16286513
- https://support.google.com/gemini/answer/16275805?hl=en
- https://support.google.com/gemini/thread/379168629 (secundaria — respuesta de Product Expert, no reemplaza términos de producto)
- https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models
- https://cloud.google.com/vertex-ai/generative-ai/docs/quotas
- https://cloud.google.com/vertex-ai/generative-ai/docs/resources/throughput-quota

### Anthropic

- https://platform.claude.com/docs/en/home
- https://platform.claude.com/docs/en/manage-claude/authentication
- https://platform.claude.com/docs/en/api/rate-limits
- https://platform.claude.com/docs/en/manage-claude/rate-limits-api
- https://platform.claude.com/docs/en/about-claude/pricing
- https://platform.claude.com/docs/en/manage-claude/api-and-data-retention
- https://platform.claude.com/docs/en/manage-claude/data-residency
- https://platform.claude.com/docs/en/docs/about-claude/model-deprecations
- https://platform.claude.com/docs/en/manage-claude/usage-cost-api

### OpenAI

- https://developers.openai.com/api/docs
- https://developers.openai.com/api/docs/models
- https://developers.openai.com/api/docs/models/compare
- https://help.openai.com/en/articles/11487671-flexible-pricing-for-chatgpt-enterprise-plans
- https://help.openai.com/en/articles/8156019-is-api-usage-included-in-chatgpt-subscriptions-even-if-i-have-a-paid-chatgpt-account (verificada en vivo, ver 4.1 — `confirmed`)

### NVIDIA

- https://docs.api.nvidia.com/
- https://docs.api.nvidia.com/nim/docs/product
- https://docs.nvidia.com/nim/large-language-models/latest/introduction.html
- https://docs.nvidia.com/nim/large-language-models/latest/deployment/model-free-nim.html
- https://docs.nvidia.com/nim/large-language-models/2.0.2/reference/support-matrix.html
- https://docs.nvidia.com/nim-operator/latest/install.html
- https://docs.nvidia.com/nim-operator/latest/platform-support.html

### AWS

- https://aws.amazon.com/es/bedrock/faqs/
- https://docs.aws.amazon.com/bedrock/latest/userguide/models.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/foundation-models-reference.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/quotas.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/models-region-compatibility.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/scaling-throughput-best-practices.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/data-retention.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/usingVPC.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/data-encryption.html
- https://aws.amazon.com/es/blogs/aws/metas-llama-3-models-are-now-available-in-amazon-bedrock/ (histórica; no usable como catálogo vigente)
