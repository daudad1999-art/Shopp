#!/usr/bin/env python3
"""Calculadora de margen por pedido para TikTok Shop España / Shopify.

Supone autónomo en recargo de equivalencia: coste y envío llevan
21 % IVA + 5,2 % recargo (×1,262) y el IVA no se deduce.
Cifras de nov 2026: verificar comisiones antes de decidir.

Ejemplos:
  python tools/margen.py --pvp 29.99 --coste 7 --envio 4
  python tools/margen.py --pvp 29.99 --coste 7 --envio 4 --afiliado 20 --comision 4
  python tools/margen.py --pvp 39 --coste 10 --envio 5 --canal shopify --cuota-mes 32 --pedidos-mes 30
"""
import argparse

RECARGO = 1.262  # 21 % IVA + 5,2 % recargo de equivalencia
IVA_PUBLICIDAD = 1.21  # IVA autoliquidado de anuncios, no recuperable


def calcular(pvp, coste, envio, canal="tiktok", comision=9.0, afiliado=0.0,
             devoluciones=5.0, cuota_mes=0.0, pedidos_mes=1):
    lineas = [("PVP (IVA incluido)", pvp),
              ("Producto (×1,262)", -coste * RECARGO),
              ("Envío (×1,262)", -envio * RECARGO)]
    if canal == "tiktok":
        lineas.append((f"Comisión TikTok ({comision:g} %)", -pvp * comision / 100))
        if afiliado:
            lineas.append((f"Afiliado ({afiliado:g} %)", -pvp * afiliado / 100))
    else:
        lineas.append(("Pasarela (2,1 % + 0,30 €)", -(pvp * 0.021 + 0.30)))
        if cuota_mes:
            lineas.append(("Cuota tienda prorrateada", -cuota_mes / max(pedidos_mes, 1)))
    lineas.append((f"Reserva devoluciones ({devoluciones:g} %)", -pvp * devoluciones / 100))
    neto = sum(v for _, v in lineas)
    return lineas, neto


def main():
    p = argparse.ArgumentParser(description="Margen por pedido")
    p.add_argument("--pvp", type=float, required=True, help="Precio de venta con IVA")
    p.add_argument("--coste", type=float, required=True, help="Coste del producto sin IVA")
    p.add_argument("--envio", type=float, required=True, help="Coste de envío sin IVA")
    p.add_argument("--canal", choices=["tiktok", "shopify"], default="tiktok")
    p.add_argument("--comision", type=float, default=9.0, help="Comisión TikTok en %% (4 en periodo de novedad)")
    p.add_argument("--afiliado", type=float, default=0.0, help="Comisión de afiliado en %%")
    p.add_argument("--devoluciones", type=float, default=5.0, help="Reserva de devoluciones en %%")
    p.add_argument("--cuota-mes", type=float, default=0.0, help="Cuota mensual Shopify")
    p.add_argument("--pedidos-mes", type=int, default=1)
    a = p.parse_args()

    lineas, neto = calcular(a.pvp, a.coste, a.envio, a.canal, a.comision,
                            a.afiliado, a.devoluciones, a.cuota_mes, a.pedidos_mes)
    for nombre, valor in lineas:
        print(f"{nombre:<34}{valor:>9.2f} €")
    print("-" * 43)
    print(f"{'Beneficio neto por pedido':<34}{neto:>9.2f} €  ({neto / a.pvp:.0%} del PVP)")
    print(f"{'CPA máximo con anuncios':<34}{max(neto, 0) / IVA_PUBLICIDAD:>9.2f} €")
    multiplicador = a.pvp / (a.coste + a.envio)
    ok = neto >= 6 and neto / a.pvp >= 0.20 and multiplicador >= 3
    print(f"PVP / (coste + envío) = {multiplicador:.1f}×")
    print("Criterio de margen: " + ("CUMPLE" if ok else "NO CUMPLE")
          + " (neto ≥ 6 €, ≥ 20 % del PVP y PVP ≥ 3× coste)")


if __name__ == "__main__":
    main()
