class Socio:
    def __init__(self, identificador_socio: int, nombre: str, apellido: str, dni: str,
                 email: str, telefono: str, categoria: str, estado: str = "Pendiente de Pago"):
        self.identificador_socio = identificador_socio
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.email = email
        self.telefono = telefono
        self.categoria = categoria  # Activo, Cadete, Vitalicio
        self.estado = estado        # Pendiente de Pago, Habilitado, Inactivo
        self.codigo_qr = f"QR-LP-{identificador_socio:04d}-{dni}"

    def modificar_datos(self, email: str = None, telefono: str = None, categoria: str = None):
        if email:
            self.email = email
        if telefono:
            self.telefono = telefono
        if categoria:
            self.categoria = categoria

    def dar_de_baja(self):
        self.estado = "Inactivo"

    def consultar_estado_cuenta(self, cuotas: list) -> dict:
        pendientes = [c for c in cuotas if c.id_socio == self.identificador_socio and c.estado_pago in ("Pendiente", "Vencida")]
        deuda_total = sum(c.monto for c in pendientes)
        return {
            "socio": f"{self.apellido}, {self.nombre}",
            "estado": self.estado,
            "cuotas_adeudadas": len(pendientes),
            "deuda_total": deuda_total
        }

    def __str__(self):
        return f"[{self.identificador_socio}] {self.apellido}, {self.nombre} (DNI: {self.dni}) | Cat: {self.categoria} | Estado: {self.estado}"