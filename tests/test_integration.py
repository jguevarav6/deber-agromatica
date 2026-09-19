from src.agromatica import conectar, consultar_cultivos, consultar_resumen


def test_consultas_reales_en_postgresql():
    with conectar() as conn:
        resumen = consultar_resumen(conn)
        cultivos = consultar_cultivos(conn)

    assert resumen["cantidad_cultivos"] == 5
    assert resumen["produccion_total"] == 16_592_000.0
    assert len(cultivos) == 5
    assert set(cultivos.columns) == {"cultivo", "anio", "produccion", "rendimiento"}
