from datetime import date
from models.club import ClubLasPalmas
from services.casos_uso import SistemaClubService


def precargar_datos(sistema: SistemaClubService):
    s1 = sistema.cu01_alta_socio("Juan", "Pérez", "35111222", "juan@mail.com", "351500001", "Activo")
    s2 = sistema.cu01_alta_socio("María", "Álvarez", "38444555", "maria@mail.com", "351500002", "Cadete")
    s3 = sistema.cu01_alta_socio("Carlos", "Gómez", "20999888", "carlos@mail.com", "351500003", "Vitalicio")

    # Emitimos cuota vencida de octubre y cuota vigente de noviembre
    sistema.cu08_actualizar_estado_cuotas("2026-10", date(2026, 10, 10), fecha_actual=date(2026, 11, 24))
    sistema.cu08_actualizar_estado_cuotas("2026-11", date(2026, 12, 10), fecha_actual=date(2026, 11, 24))

    # María paga todas sus cuotas y queda habilitada
    for c in sistema.club.cuotas:
        if c.id_socio == s2.identificador_socio and c.estado_pago != "Pagada":
            sistema.cu02_procesar_pago_cuota(s2.dni, c.identificador_cuota)


def menu():
    club = ClubLasPalmas()
    sistema = SistemaClubService(club)
    precargar_datos(sistema)

    while True:
        print("\n" + "=" * 55)
        print("  CLUB ATLÉTICO LAS PALMAS - SISTEMA DE GESTIÓN")
        print("=" * 55)
        print("1. [CU01] Alta de Socio")
        print("2. [CU01] Consultar / Dar de Baja Socio")
        print("3. [CU08] Generar Cuotas Mensuales y Actualizar Mora")
        print("4. [CU02] Procesar Pago de Cuota Social")
        print("5. [CU04] Validar Acceso en Portería (Lector QR)")
        print("6. [CU09] Reporte: Padrón Ordenado por Apellido (Selection Sort)")
        print("7. [CU09] Reporte: Socios Morosos Ordenados por Deuda (Selection Sort)")
        print("0. Salir")

        opcion = input("\nSeleccioná una opción: ").strip()

        try:
            if opcion == "1":
                nombre = input("Nombre: ")
                apellido = input("Apellido: ")
                dni = input("DNI (7 u 8 dígitos): ")
                email = input("Email: ")
                tel = input("Teléfono: ")
                cat = input("Categoría (Activo / Cadete / Vitalicio): ")
                socio = sistema.cu01_alta_socio(nombre, apellido, dni, email, tel, cat)
                print(f"\n[OK] Socio registrado: {socio} | QR: {socio.codigo_qr}")

            elif opcion == "2":
                dni = input("Ingresá DNI del socio: ")
                socio = sistema.cu01_consultar_socio(dni)
                print(f"\nFicha: {socio} | QR: {socio.codigo_qr}")
                baja = input("¿Desea darlo de baja? (s/n): ").lower()
                if baja == "s":
                    sistema.cu01_baja_socio(dni)
                    print("[OK] Socio dado de baja correctamente.")

            elif opcion == "3":
                periodo = input("Período a liquidar (ej. 2026-12): ")
                res = sistema.cu08_actualizar_estado_cuotas(periodo, date(2026, 12, 10))
                print(f"\n[OK] Cuotas emitidas: {res['emitidas']} | Cuotas pasadas a Vencida: {res['vencidas']}")

            elif opcion == "4":
                dni = input("DNI del socio: ")
                socio = sistema.cu01_consultar_socio(dni)
                cuotas_socio = [c for c in club.cuotas if c.id_socio == socio.identificador_socio]
                for c in cuotas_socio:
                    print("  ", c)
                id_c = int(input("Ingresá el ID de cuota a abonar: "))
                cuota_paga = sistema.cu02_procesar_pago_cuota(dni, id_c)
                print(f"\n[OK] Pago acreditado: {cuota_paga} | Nuevo estado socio: {socio.estado}")

            elif opcion == "5":
                print("\nCódigos QR disponibles para probar:")
                for s in club.socios:
                    print(f"  - {s.apellido}, {s.nombre} ({s.estado}): {s.codigo_qr}")
                qr = input("\nEscaneá o pegá el código QR: ").strip()
                acceso = sistema.cu04_validar_acceso_porteria(qr)
                print(f"\n>>> RESULTADO PORTERÍA: {acceso}")

            elif opcion == "6":
                ordenados = sistema.cu09_reporte_padron_ordenado(criterio="apellido")
                print("\n--- PADRÓN ORDENADO ALFABÉTICAMENTE ---")
                for s in ordenados:
                    print("  ", s)

            elif opcion == "7":
                morosos = sistema.cu09_reporte_morosos_ordenado()
                print("\n--- REPORTE DE MOROSOS (MAYOR A MENOR DEUDA) ---")
                for m in morosos:
                    print(f"  {m['socio']} | Cuotas adeudadas: {m['cuotas_adeudadas']} | Deuda: ${m['deuda_total']:.2f}")

            elif opcion == "0":
                print("Saliendo del sistema...")
                break
            else:
                print("Opción inválida.")
        except Exception as e:
            print(f"\n[ERROR] {e}")


if __name__ == "__main__":
    menu()