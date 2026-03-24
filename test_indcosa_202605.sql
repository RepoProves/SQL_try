-- Script de prueba para INDCOSA versión 202605
-- Insertar datos de prueba en LND con INDCOSA valores 1-20 aleatorios

-- Limpiar tablas LND
TRUNCATE TABLE LND_PERSONA;
TRUNCATE TABLE LND_CONTRATO;
TRUNCATE TABLE LND_CONTRATO_PERSONA;

-- Insertar personas
INSERT INTO LND_PERSONA (persona_id, nombre, apellido1, apellido2, nif, fecha_nacimiento, fec_carga, INDCOSA) VALUES (1, 'Juan', 'Perez', 'Garcia', '12345678A', DATE '1990-01-01', SYSDATE, 5);
INSERT INTO LND_PERSONA (persona_id, nombre, apellido1, apellido2, nif, fecha_nacimiento, fec_carga, INDCOSA) VALUES (2, 'Maria', 'Lopez', 'Martinez', '87654321B', DATE '1985-05-15', SYSDATE, 12);
INSERT INTO LND_PERSONA (persona_id, nombre, apellido1, apellido2, nif, fecha_nacimiento, fec_carga, INDCOSA) VALUES (3, 'Carlos', 'Sanchez', 'Rodriguez', '11223344C', DATE '1995-10-20', SYSDATE, 3);

-- Insertar contratos
INSERT INTO LND_CONTRATO (contrato_id, fecha_alta, importe_mensual, estado, tipo_producto, fec_carga, INDCOSA) VALUES (1001, DATE '2023-01-01', 100.00, 'ACTIVO', 'SEGURO', SYSDATE, 7);
INSERT INTO LND_CONTRATO (contrato_id, fecha_alta, importe_mensual, estado, tipo_producto, fec_carga, INDCOSA) VALUES (1002, DATE '2023-02-01', 200.00, 'ACTIVO', 'PRESTAMO', SYSDATE, 15);
INSERT INTO LND_CONTRATO (contrato_id, fecha_alta, importe_mensual, estado, tipo_producto, fec_carga, INDCOSA) VALUES (1003, DATE '2023-03-01', 150.00, 'INACTIVO', 'SEGURO', SYSDATE, 9);

-- Insertar relaciones contrato-persona
INSERT INTO LND_CONTRATO_PERSONA (contrato_id, persona_id, rol_persona, fec_carga, INDCOSA) VALUES (1001, 1, 'TITULAR', SYSDATE, 2);
INSERT INTO LND_CONTRATO_PERSONA (contrato_id, persona_id, rol_persona, fec_carga, INDCOSA) VALUES (1002, 2, 'TITULAR', SYSDATE, 18);
INSERT INTO LND_CONTRATO_PERSONA (contrato_id, persona_id, rol_persona, fec_carga, INDCOSA) VALUES (1003, 3, 'TITULAR', SYSDATE, 4);
INSERT INTO LND_CONTRATO_PERSONA (contrato_id, persona_id, rol_persona, fec_carga, INDCOSA) VALUES (1001, 2, 'BENEFICIARIO', SYSDATE, 11);

COMMIT;