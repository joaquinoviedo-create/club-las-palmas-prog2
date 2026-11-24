from datetime import date
from models.socio import Socio
from models.cuota_social import CuotaSocial
from models.acceso import Acceso
from models.club import ClubLasPalmas
from services.ordenamiento import selection_sort


class SistemaClubService:
    def __init__(self, club: ClubLasPalmas):
        self.club = club
        self._seq_socio = 1
        self._seq_cuota = 1
        self._seq_acceso = 1

    # ---------------------------------------------------------
    # CU01: Gestionar Socio (Alta, Baja, Modificación, Consulta)
    # ---------------------------------------------------------
    def cu01_alta_socio(self, nombre: str, apellido: str, dni: str,
                        email: str, telefono: str, categoria: str) -> Socio:
        if not nombre or not apellido or not dni:
            raise ValueError("Nombre, apellido y DNI son obligatorios.")
        if not dni.isdigit() or len(dni) not in (7, 8):
            raise ValueError("El DNI debe ser numérico de 7 u 8 dígitos.")
        if "@" not in email:
            raise ValueError("Formato de correo electrónico inválido.")
        if self.club.buscar_socio_por_dni(dni) is not None:
            raise ValueError(f"Ya existe un socio registrado con el DNI {dni}.")

        nuevo_socio = Socio(
            identificador_socio=self._seq_socio,
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            email=email,
            telefono=telefono,
            categoria=categoria,
            estado="Pendiente de Pago"
        )
        self._seq_socio += 1
        self.club.socios.append(nuevo_socio)
        return nuevo_socio

    def cu01_consultar_socio(self, dni: str) -> Socio:
        socio = self.club.buscar_socio_por_dni(dni)
        if not socio:
            raise LookupError(f"No se encontró ningún socio con DNI {dni}.")
        return socio

    def cu01_modificar_socio(self, dni: str, email: str = None,
                             telefono: str = None, categoria: str = None) -> Socio:
        socio = self.cu01_consultar_socio(dni)
        if email and "@" not in email:
            raise ValueError("Formato de correo electrónico inválido.")
        socio.modificar_datos(email=email, telefono=telefono, categoria=categoria)
        return socio

    def cu01_baja_socio(self, dni: str) -> Socio:
        socio = self.cu01_consultar_socio(dni)
        estado_cuenta = socio.consultar_estado_cuenta(self.club.cuotas)
        if estado_cuenta["deuda_total"] > 0:
            raise ValueError("No se puede dar de baja: el socio posee cuotas impagas.")
        socio.dar_de_baja()
        return socio

    # ---------------------------------------------------------
    # CU08: Actualizar Estado de Cuotas
    # ---------------------------------------------------------
    def cu08_actualizar_estado_cuotas(self, periodo: str, fecha_vencimiento: date,
                                      fecha_actual: date = None) -> dict:
        if fecha_actual is None:
            fecha_actual = date.today()

        emitidas = 0
        vencidas = 0

        for socio in self.club.socios:
            if socio.estado != "Inactivo":
                ya_existe = any(
                    c.id_socio == socio.identificador_socio and c.periodo == periodo
                    for c in self.club.cuotas
                )
                if not ya_existe:
                    monto = self.club.aranceles.get(socio.categoria, 15000.0)
                    estado_inicial = "Pagada" if monto == 0 else "Pendiente"
                    nueva_cuota = CuotaSocial(
                        identificador_cuota=self._seq_cuota,
                        id_socio=socio.identificador_socio,
                        periodo=periodo,
                        monto=monto,
                        fecha_vencimiento=fecha_vencimiento,
                        estado_pago=estado_inicial
                    )
                    self._seq_cuota += 1
                    self.club.cuotas.append(nueva_cuota)
                    emitidas += 1

                    if monto == 0 and socio.estado == "Pendiente de Pago":
                        socio.estado = "Habilitado"

        for cuota in self.club.cuotas:
            if cuota.actualizar_vencimiento(fecha_actual):
                vencidas += 1

        return {"emitidas": emitidas, "vencidas": vencidas}

    # ---------------------------------------------------------
    # CU02: Procesar Pago de Cuota Social
    # ---------------------------------------------------------
    def cu02_procesar_pago_cuota(self, dni: str, id_cuota: int, fecha_pago: date = None) -> CuotaSocial:
        if fecha_pago is None:
            fecha_pago = date.today()

        socio = self.cu01_consultar_socio(dni)
        cuota_objetivo = next(
            (c for c in self.club.cuotas if c.identificador_cuota == id_cuota and c.id_socio == socio.identificador_socio),
            None
        )
        if not cuota_objetivo:
            raise LookupError("Cuota no encontrada para el socio indicado.")

        cuota_objetivo.registrar_pago(fecha_pago)

        tiene_vencidas = any(
            c.id_socio == socio.identificador_socio and c.estado_pago == "Vencida"
            for c in self.club.cuotas
        )
        if not tiene_vencidas and socio.estado != "Inactivo":
            socio.estado = "Habilitado"

        return cuota_objetivo

    # ---------------------------------------------------------
    # CU04: Validar Acceso en Portería
    # ---------------------------------------------------------
    def cu04_validar_acceso_porteria(self, codigo_qr: str) -> Acceso:
        socio = self.club.buscar_socio_por_qr(codigo_qr)

        if not socio or socio.estado == "Inactivo":
            acceso = Acceso(
                identificador_acceso=self._seq_acceso,
                id_socio=socio.identificador_socio if socio else 0,
                codigo_qr_escaneado=codigo_qr,
                resultado_validacion="Rechazado",
                motivo_rechazo="Credencial Inválida o Inactiva"
            )
            self._seq_acceso += 1
            self.club.accesos.append(acceso)
            return acceso

        tiene_vencidas = any(
            c.id_socio == socio.identificador_socio and c.estado_pago == "Vencida"
            for c in self.club.cuotas
        )

        if socio.estado != "Habilitado" or tiene_vencidas:
            acceso = Acceso(
                identificador_acceso=self._seq_acceso,
                id_socio=socio.identificador_socio,
                codigo_qr_escaneado=codigo_qr,
                resultado_validacion="Rechazado",
                motivo_rechazo="Cuota Vencida o Pendiente de Pago"
            )
        else:
            acceso = Acceso(
                identificador_acceso=self._seq_acceso,
                id_socio=socio.identificador_socio,
                codigo_qr_escaneado=codigo_qr,
                resultado_validacion="Autorizado"
            )

        self._seq_acceso += 1
        self.club.accesos.append(acceso)
        return acceso

    # ---------------------------------------------------------
    # CU09: Generar Reportes (aplica algoritmo de ordenamiento)
    # ---------------------------------------------------------
    def cu09_reporte_padron_ordenado(self, criterio: str = "apellido") -> list:
        if criterio == "deuda":
            return selection_sort(
                self.club.socios,
                clave_func=lambda s: s.consultar_estado_cuenta(self.club.cuotas)["deuda_total"],
                reverso=True
            )
        return selection_sort(
            self.club.socios,
            clave_func=lambda s: s.apellido.lower(),
            reverso=False
        )

    def cu09_reporte_morosos_ordenado(self) -> list:
        morosos = []
        for s in self.club.socios:
            if s.estado != "Inactivo":
                info = s.consultar_estado_cuenta(self.club.cuotas)
                if info["deuda_total"] > 0:
                    morosos.append(info)

        return selection_sort(morosos, clave_func=lambda item: item["deuda_total"], reverso=True)