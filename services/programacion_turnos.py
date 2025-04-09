
class ProgramacionTurnosService:
            
    def predecir_siguiente_semana_4_turnos(turnos_iniciales):
        """
        Predice los siguientes 7 días basándose en la secuencia A → C → B
        con descansos específicos
        """
        # Definimos el patrón completo
        patron = ['A']*6 + ['X']*2 + ['C']*6 + ['X']*2 + ['B']*6 + ['X']*2
        ciclo_completo = len(patron)  # 24 turnos en total
        
        # Contar cuántos de cada tipo tenemos
        conteo = {'A': 0, 'B': 0, 'C': 0, 'X': 0}
        for turno in turnos_iniciales:
            if turno in conteo:
                conteo[turno] += 1
        
        # Determinar en qué parte del ciclo estamos
        posicion_actual = 0
        
        # Si hay más de un tipo de letra, tenemos que analizar la secuencia
        tipos_en_entrada = sum(1 for letra, cantidad in conteo.items() if cantidad > 0)
        
        if tipos_en_entrada > 1:
            # Examinar cada posible posición de inicio
            for inicio in range(ciclo_completo):
                coincide = True
                for i, turno in enumerate(turnos_iniciales):
                    if patron[(inicio + i) % ciclo_completo] != turno:
                        coincide = False
                        break
                if coincide:
                    posicion_actual = (inicio + len(turnos_iniciales)) % ciclo_completo
                    break
            
            # Si no encontramos una coincidencia exacta, tratamos de inferir por el contexto
            if posicion_actual == 0:
                # Buscar transiciones características (por ejemplo, de A->X, X->C, etc.)
                for i in range(len(turnos_iniciales) - 1):
                    if turnos_iniciales[i] != turnos_iniciales[i+1]:
                        # Encontramos un cambio, verificar qué tipo de cambio es
                        if turnos_iniciales[i] == 'A' and turnos_iniciales[i+1] == 'X':
                            posicion_actual = 6 + (len(turnos_iniciales) - i - 1)
                            break
                        elif turnos_iniciales[i] == 'X' and turnos_iniciales[i+1] == 'C':
                            posicion_actual = 8 + (len(turnos_iniciales) - i - 1)
                            break
                        elif turnos_iniciales[i] == 'C' and turnos_iniciales[i+1] == 'X':
                            posicion_actual = 14 + (len(turnos_iniciales) - i - 1)
                            break
                        elif turnos_iniciales[i] == 'X' and turnos_iniciales[i+1] == 'B':
                            posicion_actual = 16 + (len(turnos_iniciales) - i - 1)
                            break
                        elif turnos_iniciales[i] == 'B' and turnos_iniciales[i+1] == 'X':
                            posicion_actual = 22 + (len(turnos_iniciales) - i - 1)
                            break
                        elif turnos_iniciales[i] == 'X' and turnos_iniciales[i+1] == 'A':
                            posicion_actual = 0 + (len(turnos_iniciales) - i - 1)
                            break
        
        # Si no pudimos determinar la posición, usamos el último turno para inferir
        if posicion_actual == 0:
            ultimo_turno = turnos_iniciales[-1]
            if ultimo_turno == 'A':
                # Asumimos que estamos en la secuencia de A's
                conteo_a = sum(1 for t in reversed(turnos_iniciales) if t == 'A')
                posicion_actual = conteo_a % 6
                if posicion_actual == 0:
                    posicion_actual = 6
            elif ultimo_turno == 'X':
                # Asumimos que estamos en la secuencia de X's
                # Verificamos qué letra viene antes del X
                for i in range(len(turnos_iniciales)-2, -1, -1):
                    if turnos_iniciales[i] != 'X':
                        letra_anterior = turnos_iniciales[i]
                        if letra_anterior == 'A':
                            posicion_actual = 7  # Después del primer X que sigue a A
                        elif letra_anterior == 'C':
                            posicion_actual = 15  # Después del primer X que sigue a C
                        elif letra_anterior == 'B':
                            posicion_actual = 23  # Después del primer X que sigue a B
                        break
            elif ultimo_turno == 'C':
                # Asumimos que estamos en la secuencia de C's
                conteo_c = sum(1 for t in reversed(turnos_iniciales) if t == 'C')
                posicion_actual = 8 + (conteo_c % 6)
                if posicion_actual == 8:
                    posicion_actual = 14
            elif ultimo_turno == 'B':
                # Asumimos que estamos en la secuencia de B's
                conteo_b = sum(1 for t in reversed(turnos_iniciales) if t == 'B')
                posicion_actual = 16 + (conteo_b % 6)
                if posicion_actual == 16:
                    posicion_actual = 22
        
        # Calculamos los siguientes 7 turnos
        siguientes_turnos = []
        for i in range(7):
            indice = (posicion_actual + i) % ciclo_completo
            siguientes_turnos.append(patron[indice])
        
        return siguientes_turnos
        
    def predecir_siguiente_semana_3_turnos(turnos_iniciales):
        """
        Predice los siguientes 7 días basándose en la secuencia A → C → B
        con descansos específicos
        """
        # Definimos el nuevo patrón completo
        patron = ['A']*6 + ['C']*6 + ['X']*2 + ['B']*6 + ['X']*1
        ciclo_completo = len(patron)  # 21 turnos en total
        
        # Buscar la posición en el patrón
        posicion_actual = -1
        
        # Examinar cada posible posición de inicio
        for inicio in range(ciclo_completo):
            coincide = True
            for i, turno in enumerate(turnos_iniciales):
                if i < len(turnos_iniciales) and patron[(inicio + i) % ciclo_completo] != turno:
                    coincide = False
                    break
            if coincide:
                posicion_actual = (inicio + len(turnos_iniciales)) % ciclo_completo
                break
        
        # Si no encontramos una coincidencia exacta, buscamos patrones parciales
        if posicion_actual == -1:
            # Buscar patrones de transición característica
            for i in range(len(turnos_iniciales) - 1):
                if turnos_iniciales[i] != turnos_iniciales[i+1]:
                    # Encontramos un cambio, verificar qué tipo de cambio es
                    if turnos_iniciales[i] == 'A' and turnos_iniciales[i+1] == 'C':
                        posicion_actual = 6 + (len(turnos_iniciales) - i - 1)
                        break
                    elif turnos_iniciales[i] == 'C' and turnos_iniciales[i+1] == 'X':
                        posicion_actual = 12 + (len(turnos_iniciales) - i - 1)
                        break
                    elif turnos_iniciales[i] == 'X' and turnos_iniciales[i+1] == 'B':
                        posicion_actual = 14 + (len(turnos_iniciales) - i - 1)
                        break
                    elif turnos_iniciales[i] == 'B' and turnos_iniciales[i+1] == 'X':
                        posicion_actual = 20 + (len(turnos_iniciales) - i - 1)
                        break
                    elif turnos_iniciales[i] == 'X' and turnos_iniciales[i+1] == 'A':
                        posicion_actual = 0 + (len(turnos_iniciales) - i - 1)
                        break
        
        # Si todavía no hemos podido determinar la posición
        if posicion_actual == -1:
            # Contar cuántos del mismo tipo tenemos al final
            ultimo_turno = turnos_iniciales[-1]
            contador = 0
            
            for i in range(len(turnos_iniciales)-1, -1, -1):
                if turnos_iniciales[i] == ultimo_turno:
                    contador += 1
                else:
                    break
            
            # Inferir posición basada en el último turno y su cantidad
            if ultimo_turno == 'A':
                posicion_actual = contador % 6
            elif ultimo_turno == 'C':
                posicion_actual = 6 + (contador % 6)
            elif ultimo_turno == 'X':
                # Si es X, necesitamos saber si es después de C o después de B
                if len(turnos_iniciales) > 1 and turnos_iniciales[-2] == 'C':
                    posicion_actual = 12 + (contador % 2)
                else:
                    posicion_actual = 20  # Solo hay un X después de B
            elif ultimo_turno == 'B':
                posicion_actual = 14 + (contador % 6)
        
        # Si posicion_actual es -1 (no pudimos determinar la posición), usamos 0 como predeterminado
        if posicion_actual == -1:
            posicion_actual = 0
        
        # Calculamos los siguientes 7 turnos
        siguientes_turnos = []
        for i in range(7):
            indice = (posicion_actual + i) % ciclo_completo
            siguientes_turnos.append(patron[indice])
        
        return siguientes_turnos
