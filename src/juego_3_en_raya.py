import pytest
import os

fichas = ['o', 'x']
n = 3  # Variable global necesaria para que los tests del boletín funcionen

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
    Método que permite determinar si los movimientos de un jugador le
    permiten ganar una partida.
    """
    for fila in movimientos_jugador:
        movimientos_columna = movimientos_jugador[fila]
        if len(movimientos_columna) == 3:
            return True
    return False

def mostrar_tablero(tablero):
    """
    Método que muestra el estado actual del tablero
    """
    for fila in tablero:
        for celda in fila:
            print(celda, end='')
        print('\n')

# --- TESTS UNITARIOS (Páginas 10-14) ---

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

def test_ganador():
    movimientos_jugador = {2: [1, 2, 3]}
    assert True == jugada_ganadora(movimientos_jugador)

# --- BUCLE PRINCIPAL DEL JUEGO (Páginas 15-16) ---
# Usamos "if __name__ == '__main__':" para que no se ejecute al lanzar los tests
if __name__ == '__main__':
    # Pedimos el tamaño del tablero
    n = int(input('Introduce el tamaño del tablero cuadrado: '))
    casillas_libres = n * n
    jugador_activo = 0
    movimientos_jugador_1 = {}
    movimientos_jugador_2 = {}
    movimientos_jugadores = [movimientos_jugador_1, movimientos_jugador_2]
    
    tablero = generar_tablero(n, movimientos_jugadores)
    mostrar_tablero(tablero)
    
    while casillas_libres > 0:
        casilla_jugador = input(f"JUGADOR {jugador_activo+1}: Introduce movimiento (x,y): ")
        casilla_jugador = casilla_jugador.strip()
        
        # Convertimos input "1,1" a índices 0,0
        x = int(casilla_jugador.split(',')[0]) - 1
        y = int(casilla_jugador.split(',')[1]) - 1
        
        print(casilla_jugador, x, y)
        
        movimientos_jugador_activo = movimientos_jugadores[jugador_activo]
        movimientos_otro_jugador = movimientos_jugadores[(jugador_activo+1)%2]
        
        if movimiento_valido(x, y, movimientos_otro_jugador):
            mov_col = movimientos_jugador_activo.get(x, [])
            mov_col.append(y)
            movimientos_jugador_activo[x] = mov_col
            
            # Limpiamos pantalla (comando para Windows)
            os.system('cls')
            
            tablero = generar_tablero(n, movimientos_jugadores)
            mostrar_tablero(tablero)
            
            if jugada_ganadora(movimientos_jugador_activo):
                print(f"ENHORABUENA EL JUGADOR {jugador_activo+1} HA GANADO")
                break
            
            casillas_libres = casillas_libres - 1
            jugador_activo = (jugador_activo + 1) % 2
        else:
            print('\a') # Sonido de alerta
            print("Movimiento invalido. Turno para el siguiente jugador")