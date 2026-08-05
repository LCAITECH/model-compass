# Model Compass — Project Handoff Summary

Este documento es un resumen de contexto para retomar el proyecto en
modo implementación. La documentación completa y aprobada vive en los
7 archivos ya generados (`VISION.md`, `README.md`, `ROADMAP.md`,
`FEATURES.md`, `ARCHITECTURE.md`, `SCHEMA.md`, `CONTRIBUTING.md`) más
`LICENSE`. Este resumen no los reemplaza — es un mapa rápido para no
tener que releer todo antes de picar código.

---

## Qué es el proyecto

**Model Compass** es un motor de decisión open source que recomienda
qué modelo de IA usar para un caso de uso concreto. No es un
benchmark ni un comparador. Es un motor de reglas **determinístico**
que evalúa el contexto de un developer (caso de uso, presupuesto,
prioridades, idioma) contra un dataset curado, y devuelve una
recomendación **explicable** (modelo + razones + trade-offs +
alternativas). Nunca devuelve solo un nombre de modelo.

Tagline: *"Developers don't need more information. They need better
decisions."*

Licencia: MIT. Estado: Pre-MVP, fase documentation-first recién
cerrada, arranca implementación.

## Principios que NO se negocian

Estos son restricciones duras, no preferencias de estilo. Cualquier
código que los viole debe rechazarse, aunque funcione:

1. **Las interfaces dependen del Decision Engine. El Decision Engine
   nunca depende de las interfaces.** El core no conoce FastAPI,
   HTML, JSON, ni ningún mecanismo de acceso. Si se borran todas las
   interfaces, el core sigue funcionando igual.
2. **El Decision Engine nunca conoce nombres de modelos.** No sabe
   qué es "Gemini", "GPT" ni "Claude". Solo razona sobre atributos
   (`supports_spanish`, `cost_tier`, etc.), nunca sobre nombres
   (`if model == "gemini"` está prohibido, sin excepciones).
3. **Reglas son código. Datos son datos. Nunca se mezclan.** Todo
   conocimiento sobre modelos vive en el dataset (YAML), nunca
   hardcodeado en Python.
4. **Una única fuente de verdad**, aplicado en todos lados: un solo
   lugar por entidad de dominio, un solo archivo por modelo en el
   dataset, un solo lugar para cada tipo de dato compartido.
5. **Objective vs Editorial** (dentro del dataset): campos objetivos
   se verifican contra documentación pública del proveedor; campos
   editoriales son juicio curado por el proyecto, nunca basado en
   benchmarks propios o de terceros.

## Arquitectura (ver ARCHITECTURE.md para el detalle completo)

Flujo de datos, siempre en una sola dirección:

```
dataset/models/*.yaml
    → Loader      (lee YAML, produce objetos AIModel)
    → Evaluator    (aplica lógica de decisión: Context + AIModel[] → Candidate[])
    → Explainer    (Candidate[] → Recommendation, con razones y trade-offs)
    → Recommendation (objeto tipado, agnóstico de presentación)
    → interfaces/web/   (o api/, sdk/, cli/ en el futuro — cada uno presenta a su manera)
```

Estructura de carpetas objetivo:

```
model-compass/
├── dataset/
│   └── models/
│       └── *.yaml              (un archivo por modelo)
├── decision/                    ← el núcleo, sin conocer ninguna interfaz
│   ├── domain/
│   │   ├── ai_model.py
│   │   ├── context.py
│   │   ├── candidate.py
│   │   └── recommendation.py
│   ├── loader/
│   ├── evaluator/
│   └── explainer/
├── interfaces/
│   └── web/                     (única interfaz del MVP; api/sdk/cli vienen después)
├── docs/
│   ├── VISION.md
│   ├── ROADMAP.md
│   ├── FEATURES.md
│   ├── ARCHITECTURE.md
│   ├── SCHEMA.md
│   └── CONTRIBUTING.md
├── README.md
└── LICENSE
```

Decisiones de implementación **deliberadamente abiertas** (no
inventar, resolver cuando corresponda):
- Dónde vive la validación del dataset (¿dentro de `loader/`, o
  componente separado?)
- Tooling del proyecto: gestor de dependencias, estructura de tests,
  `pyproject.toml`, etc. — nada de esto está definido todavía.

Preferencia declarada: Python + FastAPI (para cuando llegue la Web
app / API), tipado fuerte, código desacoplado. Pero esto se decidió
**después** de la arquitectura, no antes — la arquitectura no depende
del stack.

## El dataset (ver SCHEMA.md para el detalle completo)

Un YAML por modelo en `dataset/models/{id}.yaml`. Principio rector:

> "Un modelo no entra al dataset porque existe. Entra cuando está
> completamente caracterizado."

Todos los campos del schema son obligatorios en v1 — si un modelo no
está completamente evaluado, no entra, punto.

Categorías del schema: Identity, Functional Capabilities (visión,
audio, tool calling, etc. — objetivos), Quality (reasoning, coding,
creative_writing, instruction_following — editoriales, escala
`low/medium/high/very_high`), Languages + language_quality
(objetivo + editorial), Operational Characteristics (context_window,
max_output — objetivos; **latency queda deliberadamente fuera**,
porque es propiedad del servicio, no del modelo), Cost (precios
objetivos; `cost_tier` NO se guarda, se deriva en el Evaluator),
Ecosystem (integration_ease, maturity — editoriales).

Campos explícitamente descartados y por qué (no reintroducir sin
discusión): `cost_tier` (se deriva, no se almacena), `latency_class`
(no es propiedad del modelo), `popularity` (sin fuente objetiva
confiable todavía), `multilingual` como campo único (reemplazado por
`language_quality`, que es más preciso).

## Roadmap (fases, sin fechas — ver ROADMAP.md)

1. **Foundation** — identidad, docs, dataset inicial. *(Estado actual)*
2. **Decision Engine** — el core, sin UI.
3. **Web Platform** — primera interfaz, MVP visible.
4. **Developer Platform** — API → SDK → CLI.
5. **Community & Governance** — maduración de procesos, no apertura
   (la comunidad ya está "adentro" desde Foundation).

## Cómo arrancar la implementación (orden acordado)

**No empezar por código.** Orden decidido explícitamente:

1. Cargar **5 modelos reales** en `dataset/models/*.yaml` a mano,
   siguiendo `SCHEMA.md` estrictamente (ej. Gemini 2.5 Flash, GPT-5
   Mini, Claude Sonnet 5, DeepSeek V3, Mistral Large). El objetivo es
   que estos 5 modelos reales le hagan fricción al schema *antes* de
   que exista una línea de código — es mucho más barato descubrir un
   problema de schema con 5 YAML que con medio Evaluator ya escrito.
2. Anotar cualquier fricción (campo que falta, enum que no alcanza,
   campo que sobra) sin tocar el schema todavía. Solo ajustar el
   schema si el mismo problema aparece 2-3 veces — nunca reaccionar
   al primer caso.
3. Recién ahí, escribir el `Loader` — contra datos reales, no mocks.
4. Después `Evaluator`, después `Explainer`, en ese orden.
5. Recién al final, `interfaces/web/`.

## Ideas anotadas pero explícitamente NO comprometidas todavía

Estas existen como dirección futura, no como tareas — no implementar
sin retomar la conversación:
- Pipeline de actualización automática del dataset (scrapers por
  proveedor, normalizador, campos como `last_verified`/`source_url`).
- `Recommendation Confidence` (score de confianza en la recomendación).
- `Recommendation History` (cómo cambió una recomendación en el tiempo).
- `Custom Recommendation Profiles` (perfiles de ponderación reusables).
- `.github/` con `ISSUE_TEMPLATE`, `PULL_REQUEST_TEMPLATE.md`,
  `CODE_OF_CONDUCT.md` — para cuando el repo reciba PRs reales.

## Tono y criterio general del proyecto

Minimalista pero bien explicado — estilo Stripe/Vercel/FastAPI/Docker.
Cero emojis de humo (🚀🔥✨) en la documentación oficial. Simplicidad
por sobre complejidad, mantenibilidad por sobre velocidad, todo
cambio modular, evitar sobreingeniería, MVP chico y sólido antes que
una solución grande difícil de mantener. Cualquier decisión que
afecte arquitectura se discute antes de implementarse, no se asume.