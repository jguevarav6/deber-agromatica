BEGIN;

DROP TABLE IF EXISTS genes;
DROP TABLE IF EXISTS cultivos;

CREATE TABLE genes (
    id SERIAL PRIMARY KEY,
    especie TEXT NOT NULL,
    nombre TEXT NOT NULL,
    longitud INT NOT NULL CHECK (longitud > 0)
);

CREATE TABLE cultivos (
    id SERIAL PRIMARY KEY,
    cultivo TEXT NOT NULL,
    anio INT NOT NULL CHECK (anio BETWEEN 2000 AND 2100),
    produccion NUMERIC(12, 2) NOT NULL CHECK (produccion >= 0),
    rendimiento NUMERIC(8, 2) NOT NULL CHECK (rendimiento >= 0)
);

INSERT INTO genes (especie, nombre, longitud) VALUES
    ('Theobroma cacao', 'rbcL', 1428),
    ('Musa acuminata', 'matK', 1512),
    ('Oryza sativa', 'Wx', 6098),
    ('Zea mays', 'adh1', 3560),
    ('Saccharum officinarum', 'SPS', 3204);

INSERT INTO cultivos (cultivo, anio, produccion, rendimiento) VALUES
    ('Cacao', 2022, 412000.00, 0.74),
    ('Banano', 2023, 7020000.00, 41.80),
    ('Arroz', 2024, 1570000.00, 5.21),
    ('Maíz', 2025, 1490000.00, 4.63),
    ('Caña de azúcar', 2026, 6100000.00, 78.40);

COMMIT;
