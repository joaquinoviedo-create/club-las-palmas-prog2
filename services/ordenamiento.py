def selection_sort(lista: list, clave_func, reverso: bool = False) -> list:
    """
    Implementación propia de Ordenamiento por Selección (Selection Sort).
    Devuelve una nueva lista ordenada sin mutar la original.
    """
    resultado = lista.copy()
    n = len(resultado)

    for i in range(n):
        idx_extremo = i
        for j in range(i + 1, n):
            val_j = clave_func(resultado[j])
            val_extremo = clave_func(resultado[idx_extremo])

            if reverso:
                if val_j > val_extremo:
                    idx_extremo = j
            else:
                if val_j < val_extremo:
                    idx_extremo = j

        resultado[i], resultado[idx_extremo] = resultado[idx_extremo], resultado[i]

    return resultado