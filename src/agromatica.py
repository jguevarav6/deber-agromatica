"""Consulta datos agrícolas de PostgreSQL y genera visualizaciones."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import psycopg2


@dataclass(frozen=True)
class DatabaseConfig:
    """Parámetros de conexión configurables mediante variables de entorno."""

    dbname: str = os.getenv("AGRO_DB_NAME", "agrobio_db")
    user: str = os.getenv("AGRO_DB_USER", "postgres")
    password: str = os.getenv("AGRO_DB_PASSWORD", "")
    host: str = os.getenv("AGRO_DB_HOST", "127.0.0.1")
    port: int = int(os.getenv("AGRO_DB_PORT", "5433"))


def conectar(config: DatabaseConfig | None = None):
    """Abre una sesión de PostgreSQL y devuelve la conexión."""

    cfg = config or DatabaseConfig()
    return psycopg2.connect(
        dbname=cfg.dbname,
        user=cfg.user,
        password=cfg.password,
        host=cfg.host,
        port=cfg.port,
    )


def consultar_resumen(conn) -> dict[str, float | int]:
    """Obtiene la cantidad de cultivos y su producción acumulada."""

    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT COUNT(*)::INT, COALESCE(SUM(produccion), 0) FROM cultivos"
        )
        cantidad, produccion_total = cursor.fetchone()
    return {"cantidad_cultivos": cantidad, "produccion_total": float(produccion_total)}


def consultar_cultivos(conn) -> pd.DataFrame:
    """Carga los cultivos ordenados cronológicamente en un DataFrame."""

    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT cultivo, anio, produccion::FLOAT, rendimiento::FLOAT
            FROM cultivos
            ORDER BY anio, cultivo
            """
        )
        registros = cursor.fetchall()
    return pd.DataFrame(
        registros, columns=["cultivo", "anio", "produccion", "rendimiento"]
    )


def cultivo_mas_eficiente(df: pd.DataFrame) -> pd.Series:
    """Devuelve el registro con mayor rendimiento por hectárea."""

    if df.empty:
        raise ValueError("No existen cultivos para analizar")
    return df.loc[df["rendimiento"].idxmax()]


def generar_graficos(df: pd.DataFrame, directorio: Path) -> tuple[Path, Path]:
    """Crea gráficos PNG de rendimiento por cultivo y producción por año."""

    directorio.mkdir(parents=True, exist_ok=True)
    estilo = {
        "axes.titleweight": "bold",
        "axes.titlesize": 14,
        "axes.labelsize": 11,
        "font.family": "DejaVu Sans",
    }
    plt.rcParams.update(estilo)

    barras = directorio / "rendimiento_por_cultivo.png"
    fig, ax = plt.subplots(figsize=(9, 5.2), layout="constrained")
    colores = ["#222222", "#555555", "#777777", "#999999", "#BBBBBB"]
    columnas = ax.bar(df["cultivo"], df["rendimiento"], color=colores)
    ax.bar_label(columnas, fmt="%.2f", padding=3)
    ax.set_title("Rendimiento agrícola por cultivo")
    ax.set_xlabel("Cultivo")
    ax.set_ylabel("Rendimiento (t/ha)")
    ax.grid(axis="y", alpha=0.25)
    fig.savefig(barras, dpi=180)
    plt.close(fig)

    linea = directorio / "produccion_por_anio.png"
    anual = df.groupby("anio", as_index=False)["produccion"].sum()
    fig, ax = plt.subplots(figsize=(9, 5.2), layout="constrained")
    ax.plot(
        anual["anio"],
        anual["produccion"],
        marker="o",
        linewidth=2.5,
        color="#111111",
    )
    for anio, produccion in zip(anual["anio"], anual["produccion"], strict=True):
        ax.annotate(
            f"{produccion / 1_000_000:.2f} M",
            (anio, produccion),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center",
        )
    ax.set_title("Producción agrícola registrada por año")
    ax.set_xlabel("Año")
    ax.set_ylabel("Producción (toneladas)")
    ax.ticklabel_format(style="plain", axis="y")
    ax.grid(alpha=0.25)
    fig.savefig(linea, dpi=180)
    plt.close(fig)
    return barras, linea


def main() -> None:
    """Ejecuta el flujo completo y presenta sus resultados."""

    salida = Path(__file__).resolve().parents[1] / "salida"
    with conectar() as conn:
        resumen = consultar_resumen(conn)
        cultivos = consultar_cultivos(conn)

    eficiente = cultivo_mas_eficiente(cultivos)
    graficos = generar_graficos(cultivos, salida)

    lineas = [
        "CONEXIÓN EXITOSA A POSTGRESQL",
        f"Cultivos registrados: {resumen['cantidad_cultivos']}",
        f"Producción total: {resumen['produccion_total']:,.2f} toneladas",
        "",
        "Datos consultados:",
        cultivos.to_string(index=False),
        "",
        f"\nCultivo más eficiente: {eficiente['cultivo']} "
        f"({eficiente['rendimiento']:.2f} t/ha)",
        "Gráficos generados:",
    ]
    for grafico in graficos:
        lineas.append(f"- {grafico}")
    salida_texto = "\n".join(lineas)
    print(salida_texto)
    (salida / "ejecucion_real.log").write_text(salida_texto + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
