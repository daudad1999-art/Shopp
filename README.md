# Shopp

Dropshipping en **TikTok Shop España** con productos para hombre, guiado por un "director de e-commerce" de IA (Claude) y un radar de tendencias (Grok).

## Qué hay aquí
| Ruta | Para qué |
|---|---|
| `docs/estrategia.md` | Estrategia acordada, datos de TikTok Shop, plan por fases y riesgos |
| `.claude/skills/director-ecommerce/SKILL.md` | El director: matriz Go/No-Go, márgenes, proveedores, contenido, revisión semanal |
| `prompts/grok-radar.md` | Prompt semanal para Grok y ciclo de trabajo Grok → director |
| `tools/margen.py` | Calculadora de beneficio por pedido (TikTok Shop o Shopify) |

## Uso rápido
```bash
# Beneficio de un pedido en TikTok Shop vendido por un creador al 15 %
python tools/margen.py --pvp 29.99 --coste 7 --envio 4 --afiliado 15
```

## Ciclo semanal
1. Grok busca qué se vende ahora (`prompts/grok-radar.md`).
2. Le pasas el resultado al director.
3. El director verifica, calcula y da veredicto GO / NO-GO.
4. Se prueba un producto cada vez, con criterio de corte fijado antes.

> Las cifras de comisiones y normativa son de noviembre de 2026. Verifícalas antes de decidir.
