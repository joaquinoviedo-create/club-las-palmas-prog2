class ClubLasPalmas:
    def __init__(self, identificador_club: int = 1, nombre: str = "Club Atlético Las Palmas",
                 direccion: str = "Juan García Martínez 323, Córdoba", telefono: str = "0351-4890000"):
        self.identificador_club = identificador_club
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.socios = []
        self.cuotas = []
        self.accesos = []
        self.aranceles = {
            "Activo": 15000.0,
            "Cadete": 10000.0,
            "Vitalicio": 0.0
        }

    def buscar_socio_por_dni(self, dni: str):
        for s in self.socios:
            if s.dni == dni:
                return s
        return None

    def buscar_socio_por_qr(self, codigo_qr: str):
        for s in self.socios:
            if s.codigo_qr == codigo_qr:
                return s
        return None

    def consultar_estadisticas(self) -> dict:
        activos = sum(1 for s in self.socios if s.estado != "Inactivo")
        recaudado = sum(c.monto for c in self.cuotas if c.estado_pago == "Pagada")
        return {
            "total_socios_activos": activos,
            "total_recaudado": recaudado,
            "total_accesos_registrados": len(self.accesos)
        }