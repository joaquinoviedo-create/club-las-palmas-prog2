import unittest
from datetime import date
from models.club import ClubLasPalmas
from services.casos_uso import SistemaClubService


class TestCasosUso(unittest.TestCase):

    def setUp(self):
        self.club = ClubLasPalmas()
        self.sistema = SistemaClubService(self.club)

    def test_cu01_gestionar_socio(self):
        socio = self.sistema.cu01_alta_socio("Lucas", "Martínez", "33222111", "lucas@mail.com", "351123456", "Activo")
        self.assertEqual(len(self.club.socios), 1)
        consultado = self.sistema.cu01_consultar_socio("33222111")
        self.assertEqual(consultado.identificador_socio, socio.identificador_socio)
        self.sistema.cu01_baja_socio("33222111")
        self.assertEqual(consultado.estado, "Inactivo")

    def test_cu08_actualizar_estado_cuotas(self):
        self.sistema.cu01_alta_socio("Lucas", "Martínez", "33222111", "lucas@mail.com", "351123456", "Activo")
        res = self.sistema.cu08_actualizar_estado_cuotas(
            periodo="2026-10",
            fecha_vencimiento=date(2026, 10, 10),
            fecha_actual=date(2026, 11, 1)
        )
        self.assertEqual(res["emitidas"], 1)
        self.assertEqual(res["vencidas"], 1)
        self.assertEqual(self.club.cuotas[0].estado_pago, "Vencida")

    def test_cu02_procesar_pago_cuota(self):
        socio = self.sistema.cu01_alta_socio("Lucas", "Martínez", "33222111", "lucas@mail.com", "351123456", "Activo")
        self.sistema.cu08_actualizar_estado_cuotas("2026-11", date(2026, 11, 10), date(2026, 11, 5))
        cuota = self.club.cuotas[0]
        self.sistema.cu02_procesar_pago_cuota("33222111", cuota.identificador_cuota)
        self.assertEqual(cuota.estado_pago, "Pagada")
        self.assertEqual(socio.estado, "Habilitado")

    def test_cu04_validar_acceso_porteria(self):
        socio = self.sistema.cu01_alta_socio("Lucas", "Martínez", "33222111", "lucas@mail.com", "351123456", "Activo")
        acceso_rechazado = self.sistema.cu04_validar_acceso_porteria(socio.codigo_qr)
        self.assertEqual(acceso_rechazado.resultado_validacion, "Rechazado")

        self.sistema.cu08_actualizar_estado_cuotas("2026-11", date(2026, 11, 10), date(2026, 11, 5))
        self.sistema.cu02_procesar_pago_cuota("33222111", self.club.cuotas[0].identificador_cuota)
        acceso_autorizado = self.sistema.cu04_validar_acceso_porteria(socio.codigo_qr)
        self.assertEqual(acceso_autorizado.resultado_validacion, "Autorizado")

    def test_cu09_generar_reportes_ordenados(self):
        self.sistema.cu01_alta_socio("Carlos", "Zavala", "30111111", "c@mail.com", "3511", "Activo")
        self.sistema.cu01_alta_socio("Ana", "Alonso", "30222222", "a@mail.com", "3512", "Cadete")
        ordenados = self.sistema.cu09_reporte_padron_ordenado(criterio="apellido")
        self.assertEqual([s.apellido for s in ordenados], ["Alonso", "Zavala"])


if __name__ == "__main__":
    unittest.main()