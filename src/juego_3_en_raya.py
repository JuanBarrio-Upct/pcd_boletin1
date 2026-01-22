import pytest
import os

fichas = ['o', 'x']
n = 3 

def generar_tablero(n, movimientos_jugadores):
    tablero = []
    for i in range(n):
        fila = ['_' for i in range(n)]
        for j in range(n):
            casilla_vacia = True
            for k in range(len(movimientos_jugadores)):
                movimientos_jugador = movimientos_jugadores[k]
                if i in movimientos_jugador:
                    if j in movimientos_jugador[i]:
                        fila[j] = fichas[k]
        tablero.append(fila)
    return tablero

def movimiento_valido(x, y, movimientos_otro_jugador):
    if x > n or y > n:
        return False
    if x in movimientos_otro_jugador:
        movimientos_en_columna = movimientos_otro_jugador[x]
        if y in movimientos_en_columna:
            return False
    return True

def jugada_ganadora(movimientos_jugador):
    """
    Método COMPLETO que comprueba filas, columnas y diagonales.
    """
    # 1. Comprobamos FILAS (ya lo tenías)
    for fila in movimientos_jugador:
        if len(movimientos_jugador[fila]) == n:
            return True

    # 2. Comprobamos COLUMNAS
    # Contamos cuántas fichas hay en cada columna (0, 1, 2)
    conteo_columnas = {0: 0, 1: 0, 2: 0}
    for fila in movimientos_jugador:
        for col in movimientos_jugador[fila]:
            if col in conteo_columnas:
                conteo_columnas[col] += 1
    
    if n in conteo_columnas.values():
        return True

    # 3. Comprobamos DIAGONALES
    diag_principal = 0 # (0,0), (1,1), (2,2)
    diag_inversa = 0   # (0,2), (1,1), (2,0)

    for fila in movimientos_jugador:
        for col in movimientos_jugador[fila]:
            # Diagonal principal: fila es igual a columna
            if fila == col:
                diag_principal += 1
            # Diagonal inversa: fila + columna suman n-1 (ej: 0+2, 1+1, 2+0)
            if fila + col == (n - 1):
                diag_inversa += 1
    
    if diag_principal == n or diag_inversa == n:
        return True

    return False

def mostrar_tablero(tablero):
    for fila in tablero:
        for celda in fila:
            print(celda, end='')
        print('\n')

# --- TESTS UNITARIOS ---

def test_generar_tablero():
    mov_jugador_1 = {}
    mov_jugador_2 = {}
    movimientos_jugadores = [mov_jugador_1, mov_jugador_2]
    n = 3
    t = generar_tablero(n, movimientos_jugadores)
    assert len(t) == n
    for f in t:
        assert len(f) == n

def test_movimiento_columna_fuera_tablero():
    movimientos_otro_jugador = {}
    x = 1
    y = n + 1
    assert False == movimiento_valido(x, y, movimientos_otro_jugador)

def test_movimiento_fila_y_columna_fuera_tablero():
    movimientos_otro_jugador = {}
    x = n + 1
    y = n + 1
    assert False == movimiento_valido(x, y, movimientos_otro_jugador)

def test_movimiento_incorrecto():
    movimientos_otro_jugador = {2: [3]}
    x = 2
    y = 3
    assert False == movimiento_valido(x, y, movimientos_otro_jugador)

def test_no_ganador():
    movimientos_jugador = {2: [2, 3]}
    assert False == jugada_ganadora(movimientos_jugador)

def test_ganador_fila():
    movimientos_jugador = {2: [1, 2, 3]} # Fila llena
    # Nota: Ajustado indices para que coincida con lógica interna (0,1,2 si se usa directo o input-1)
    # En los tests previos usabamos indices directos, mantenemos coherencia.
    # Si tus tests anteriores pasaban con {2:[1,2,3]} asumimos n=4 o indices base 1. 
    # Para asegurar con n=3 (indices 0,1,2):
    movimientos_jugador_fix = {1: [0, 1, 2]} 
    assert True == jugada_ganadora(movimientos_jugador_fix)

def test_ganador_columna():
    # Gana columna 0 (fila 0, 1 y 2 tienen la col 0)
    movimientos = {0:[0], 1:[0], 2:[0]}
    assert True == jugada_ganadora(movimientos)

def test_ganador_diagonal():
    # Gana diagonal (0,0), (1,1), (2,2)
    movimientos = {0:[0], 1:[1], 2:[2]}
    assert True == jugada_ganadora(movimientos)


# --- BUCLE PRINCIPAL DEL JUEGO ---
if __name__ == '__main__':
    try:
        entrada = input('Introduce el tamaño del tablero cuadrado (por defecto 3): ')
        n = int(entrada) if entrada else 3
    except:
        n = 3
        
    casillas_libres = n * n
    jugador_activo = 0
    movimientos_jugador_1 = {}
    movimientos_jugador_2 = {}
    movimientos_jugadores = [movimientos_jugador_1, movimientos_jugador_2]
    
    tablero = generar_tablero(n, movimientos_jugadores)
    mostrar_tablero(tablero)
    
    while casillas_libres > 0:
        casilla_jugador = input(f"JUGADOR {jugador_activo+1}: Introduce movimiento (x,y): ")
        try:
            casilla_jugador = casilla_jugador.strip()
            if not casilla_jugador: break
            
            x = int(casilla_jugador.split(',')[0]) - 1
            y = int(casilla_jugador.split(',')[1]) - 1
            
            movimientos_jugador_activo = movimientos_jugadores[jugador_activo]
            movimientos_otro_jugador = movimientos_jugadores[(jugador_activo+1)%2]
            
            if movimiento_valido(x, y, movimientos_otro_jugador):
                mov_col = movimientos_jugador_activo.get(x, [])
                mov_col.append(y)
                movimientos_jugador_activo[x] = mov_col
                
                os.system('cls' if os.name == 'nt' else 'clear')
                
                tablero = generar_tablero(n, movimientos_jugadores)
                mostrar_tablero(tablero)
                
                if jugada_ganadora(movimientos_jugador_activo):
                    print(f"¡ENHORABUENA EL JUGADOR {jugador_activo+1} HA GANADO!")
                    break
                
                casillas_libres = casillas_libres - 1
                jugador_activo = (jugador_activo + 1) % 2
            else:
                print("Movimiento inválido (casilla ocupada o fuera de rango).")
        except:
            print("Error en el formato. Usa x,y (ej: 1,1)")