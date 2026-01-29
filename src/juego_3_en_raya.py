import pytest
import os

fichas = ['o', 'x']
n = 3

def generar_tablero(n, movimientos_jugadores):
    tablero = []
    for i in range(n):
        fila = ['_'] * n
        for j in range(n):
            for k in range(len(movimientos_jugadores)):
                if i in movimientos_jugadores[k] and j in movimientos_jugadores[k][i]:
                    fila[j] = fichas[k]
        tablero.append(fila)
    return tablero

def movimiento_valido(x, y, movimientos_otro_jugador):
    if x > n or y > n: return False
    if x in movimientos_otro_jugador and y in movimientos_otro_jugador[x]:
        return False
    return True

def jugada_ganadora(movimientos):
    # 1. Filas (si una fila tiene 'n' fichas)
    for fila in movimientos:
        if len(movimientos[fila]) == n: return True

    # 2. Columnas (contamos cuántas fichas hay en cada columna)
    for col in range(n):
        contador = 0
        for fila in movimientos:
            if col in movimientos[fila]: contador += 1
        if contador == n: return True

    # 3. Diagonales
    d1 = 0
    d2 = 0
    for i in range(n):
        if i in movimientos:
            if i in movimientos[i]: d1 += 1 
            if (n-1-i) in movimientos[i]: d2 += 1 
    
    if d1 == n or d2 == n: return True
    return False

def mostrar_tablero(tablero):
    for fila in tablero:
        print("".join(fila))

# --- TESTS ---
def test_tablero():
    assert len(generar_tablero(3, [{},{}])) == 3

def test_ganador():
    assert jugada_ganadora({0:[0], 1:[0], 2:[0]}) == True # Columna
    assert jugada_ganadora({0:[0], 1:[1], 2:[2]}) == True # Diagonal

# --- JUEGO ---
if __name__ == '__main__':
    try: n = int(input('Tamaño (Enter para 3): ') or 3)
    except: n = 3
    
    libres = n * n
    turno = 0
    movs = [{}, {}]
    
    mostrar_tablero(generar_tablero(n, movs))
    
    while libres > 0:
        try:
            txt = input(f"JUGADOR {turno+1} (x,y): ").strip()
            if not txt: break
            x, y = int(txt.split(',')[0])-1, int(txt.split(',')[1])-1
            
            rival = movs[(turno+1)%2]
            
            if movimiento_valido(x, y, rival):
                if x not in movs[turno]: movs[turno][x] = []
                movs[turno][x].append(y)
                
                os.system('cls' if os.name == 'nt' else 'clear')
                mostrar_tablero(generar_tablero(n, movs))
                
                if jugada_ganadora(movs[turno]):
                    print(f"¡GANA JUGADOR {turno+1}!")
                    break
                
                libres -= 1
                turno = (turno + 1) % 2
            else:
                print("Casilla ocupada.")
        except:
            print("Error. Usa: 1,1")