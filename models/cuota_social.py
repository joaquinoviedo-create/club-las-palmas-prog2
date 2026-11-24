from datetime import date

class CuotaSocial:
    def __init__(self, identificador_cuota: int, id_socio: int, periodo: str,
                 monto: float, fecha_vencimiento: date, estado_pago: str = "Pendiente"):
        self.identificador_cuota = identificador_cuota
        self.id_socio = id_socio
        self.periodo = periodo
        self.monto = monto
        self.fecha_vencimiento = fecha_vencimiento
        self.fecha_pago = None
        self.estado_pago = estado_pago  # Pendiente, Pagada, Vencida, Anulada

    def actualizar_vencimiento(self, fecha_actual: date) -> bool:
        if self.estado_pago == "Pendiente" and fecha_actual > self.fecha_vencimiento:
            self.estado_pago = "Vencida"
            return True
        return False

    def registrar_pago(self, fecha_pago: date):
        if self.estado_pago == "Pagada":
            raise ValueError("La cuota ya se encuentra pagada.")
        self.fecha_pago = fecha_pago
        self.estado_pago = "Pagada"

    def anular_cuota(self):
        self.estado_pago = "Anulada"

    def __str__(self):
        return f"Cuota #{self.identificador_cuota} | Socio ID: {self.id_socio} | Período: {self.periodo} | ${self.monto:.2f} | Vto: {self.fecha_vencimiento} | {self.estado_pago}"