import pandas as pd
import pytest

from src.agromatica import DatabaseConfig, cultivo_mas_eficiente


def test_configuracion_predeterminada():
    config = DatabaseConfig()
    assert config.dbname == "agrobio_db"
    assert config.host == "127.0.0.1"
    assert config.port == 5433


def test_identifica_cultivo_mas_eficiente():
    datos = pd.DataFrame(
        {"cultivo": ["Cacao", "Banano"], "rendimiento": [0.74, 41.80]}
    )
    assert cultivo_mas_eficiente(datos)["cultivo"] == "Banano"


def test_rechaza_dataframe_vacio():
    with pytest.raises(ValueError, match="No existen cultivos"):
        cultivo_mas_eficiente(pd.DataFrame(columns=["rendimiento"]))
