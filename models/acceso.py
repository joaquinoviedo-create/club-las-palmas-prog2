from datetime import datetime

class Acceso:
    def __init__(self, identificador_acceso: int, id_socio: int, codigo_qr_escaneado: str,
                 resultado_validacion: str, motivo_rechazo: str = ""):
        self.identificador_acceso = identificador_acceso
        self.id_socio = id_socio
        self.fecha_hora_ingreso = datetime.now()
        self.codigo_qr_escaneado = codigo_qr_escaneado
        self.resultado_validacion = resultado_validacion  # Autorizado / Rechazado
        self.motivo_rechazo = motivo_rechazo

    def __str__(self):
        fecha_str = self.fecha_hora_ingreso.strftime("%Y-%m-%d %H:%M:%S")
        motivo = f" ({self.motivo_rechazo})" if self.motivo_rechazo else ""
        return f"Acceso #{self.identificador_acceso} | {fecha_str} | QR: {self.codigo_qr_escaneado} -> {self.resultado_validacion}{motivo}"