from src.agromatica import conectar, consultar_cultivos, generar_graficos


def test_flujo_genera_los_dos_graficos(tmp_path):
    with conectar() as conn:
        cultivos = consultar_cultivos(conn)

    archivos = generar_graficos(cultivos, tmp_path)
    assert all(archivo.exists() for archivo in archivos)
    assert all(archivo.stat().st_size > 10_000 for archivo in archivos)
