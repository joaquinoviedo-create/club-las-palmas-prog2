import unittest
from datetime import date
from models.socio import Socio
from models.cuota_social import CuotaSocial
from models.acceso import Acceso
from models.club import ClubLasPalmas


class TestModels(unittest.TestCase):

    def test_clase_socio(self):
        socio = Socio(1, "Juan", "Pérez", "35111222", "juan@mail.com", "351500001", "Activo")
        self.assertEqual(socio.estado, "Pendiente de Pago")
        self.assertEqual(socio.codigo_qr, "QR-LP-0001-35111222")
        socio.modificar_datos(telefono="351999999")
        self.assertEqual(socio.telefono, "351999999")
        socio.dar_de_baja()
        self.assertEqual(socio.estado, "Inactivo")

    def test_clase_cuota_social(self):
        cuota = CuotaSocial(1, 1, "2026-10", 15000.0, date(2026, 10, 10))
        vencio = cuota.actualizar_vencimiento(date(2026, 10, 15))
        self.assertTrue(vencio)
        self.assertEqual(cuota.estado_pago, "Vencida")
        cuota.registrar_pago(date(2026, 10, 20))
        self.assertEqual(cuota.estado_pago, "Pagada")

    def test_clase_acceso(self):
        acceso = Acceso(1, 1, "QR-LP-0001-35111222", "Autorizado")
        self.assertEqual(acceso.resultado_validacion, "Autorizado")
        self.assertEqual(acceso.motivo_rechazo, "")

    def test_clase_club_las_palmas(self):
        club = ClubLasPalmas()
        socio = Socio(1, "Ana", "López", "40123456", "ana@mail.com", "351000000", "Cadete")
        club.socios.append(socio)
        encontrado = club.buscar_socio_por_dni("40123456")
        self.assertIsNotNone(encontrado)
        self.assertEqual(encontrado.nombre, "Ana")


if __name__ == "__main__":
    unittest.main()