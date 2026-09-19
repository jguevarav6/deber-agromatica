"""Registra un log durable con el resultado real de pytest."""

from pathlib import Path


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    reportes = terminalreporter.stats.get("passed", [])
    lineas = [
        "EJECUCIÓN REAL DE PYTEST",
        f"Código de salida: {exitstatus}",
        "",
    ]
    lineas.extend(f"PASSED  {reporte.nodeid}" for reporte in reportes)
    lineas.extend(["", f"Resultado: {len(reportes)} pruebas aprobadas"])
    salida = Path(__file__).resolve().parents[1] / "salida" / "pruebas_reales.log"
    salida.parent.mkdir(exist_ok=True)
    salida.write_text("\n".join(lineas) + "\n", encoding="utf-8")
