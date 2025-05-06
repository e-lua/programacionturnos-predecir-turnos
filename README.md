## Código como Function

Codigo que representa el proyecto para que sea ejecutado mediante una Function

```python
from http.server import BaseHTTPRequestHandler
import json

class ProgramacionTurnosService:
    @staticmethod
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
    
    @staticmethod
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
    
    @staticmethod
    def predecir_siguiente_semana_adm_turnos(turnos_iniciales):
        """
        Predice los siguientes 7 días manteniendose las mimas fechas
        con descansos específicos
        """
        # Calculamos los siguientes 7 turnos
        siguientes_turnos = ["ADM","ADM","X","ADM","ADM","ADM","ADM"]
        
        return siguientes_turnos

def process_data(datos):
    """Process the input data and predict shifts"""
    # Diccionario de reemplazo
    reemplazos_3_turnos = {
        "X": "DESCANSO",
        "A": "A (3 turnos)",
        "B": "B (3 turnos)",
        "C": "C (3 turnos)"
    }
    reemplazos_4_turnos = {
        "X": "DESCANSO",
        "A": "A (4 turnos)",
        "B": "B (4 turnos)",
        "C": "C (4 turnos)"
    }
    reemplazos_adm_turnos = {
        "X": "DESCANSO",
        "ADM": "ADM"
    }
    
    # Actualizar el tipo de turno
    for elemento in datos:
        semana_anterior = elemento["SemanaAnteriorOriginal"].split(",")
        
        tipo_turno = ""
        
        for turno in reversed(semana_anterior):
            if "3 turnos" in turno:
                tipo_turno = "3 turnos"
                break
            elif "4 turnos" in turno:
                tipo_turno = "4 turnos"
                break
            elif "ADM" in turno:
                tipo_turno="ADM"
                break
        
        # Asignarlo al campo "TipoTuno"
        elemento["TipoTurno"] = tipo_turno
    
    # Actualizar el campo "SemanaAnterior"
    for elemento in datos:
        semana_original = elemento["SemanaAnteriorOriginal"].split(",")  # Dividir por coma
        semana_actualizada = []

        for turno in semana_original:
            if "A (" in turno:
                semana_actualizada.append("A")
            elif "B (" in turno:
                semana_actualizada.append("B")
            elif "C (" in turno:
                semana_actualizada.append("C")
            elif "ADM" in turno:
                semana_actualizada.append("ADM")
            else:
                semana_actualizada.append("X")  # Valor por defecto para no A, B, C, ADM

        # Unir la lista actualizada y asignarla al campo "SemanaAnterior"
        elemento["SemanaAnterior"] = ",".join(semana_actualizada)

    # Predecir turnos de la siguiente semana
    for elemento in datos:
        if elemento["TipoTurno"] == "4 turnos":
            semana_anterior = elemento["SemanaAnterior"].split(",")
            semana_siguiente = ProgramacionTurnosService.predecir_siguiente_semana_4_turnos(semana_anterior)
            
            # Asignarlo al campo "SemanaSiguiente"
            elemento["SemanaSiguiente"] = ",".join(semana_siguiente)
        elif elemento["TipoTurno"] == "3 turnos":
            semana_anterior = elemento["SemanaAnterior"].split(",")
            semana_siguiente = ProgramacionTurnosService.predecir_siguiente_semana_3_turnos(semana_anterior)
            
            # Asignarlo al campo "SemanaSiguiente"
            elemento["SemanaSiguiente"] = ",".join(semana_siguiente)
        elif elemento["TipoTurno"] == "ADM":
            semana_anterior = elemento["SemanaAnterior"].split(",")
            semana_siguiente = ProgramacionTurnosService.predecir_siguiente_semana_adm_turnos(semana_anterior)
            
            # Asignarlo al campo "SemanaSiguiente"
            elemento["SemanaSiguiente"]= ",".join(semana_siguiente)
    
    # Actualizar el campo "SemanaSiguienteOriginal"
    for elemento in datos:
        if elemento["TipoTurno"] == "3 turnos":
            # Reemplazar los nombres de los turnos
            semana_siguiente_original = ','.join([reemplazos_3_turnos.get(valor, valor) for valor in elemento["SemanaSiguiente"].split(',')])
            # Asignarla al campo "SemanaAnterior"
            elemento["SemanaSiguienteOriginal"] = semana_siguiente_original
          
        elif elemento["TipoTurno"] == "4 turnos":
            # Reemplazar los nombres de los turnos
            semana_siguiente_original = ','.join([reemplazos_4_turnos.get(valor, valor) for valor in elemento["SemanaSiguiente"].split(',')])
            # Asignarla al campo "SemanaAnterior"
            elemento["SemanaSiguienteOriginal"] = semana_siguiente_original         
        elif elemento["TipoTurno"] == "ADM":
            
            # Reemplazar los nombres de los turnos
            semana_siguiente_original = ','.join([reemplazos_adm_turnos.get(valor, valor) for valor in elemento["SemanaSiguiente"].split(',')])

            # Unir la lista actualizada y asignarla al campo "SemanaAnterior"
            elemento["SemanaSiguienteOriginal"] = semana_siguiente_original
              
    # Crear array para la respuesta
    elementos_respuesta = []
    for elemento in datos:
        fechas = elemento.get("Fechas", "").split(",")
        nombres_fechas = elemento.get("NombresFechas", "").split(",") if "NombresFechas" in elemento else [""] * 7
        
        for i in range(min(7, len(fechas))):
            # Clave única para buscar
            clave_unica = elemento["Cedula"] + fechas[i]
            
            # Tipo de turno
            tipo_turno = elemento["TipoTurno"]
            
            # Valor turno
            valor_turno = ""
            
            semana_siguiente = elemento.get("SemanaSiguiente", "").split(",")
            semana_siguiente_original = elemento.get("SemanaSiguienteOriginal", "").split(",")
            
            # Asegurarse de que hay suficientes elementos
            if i < len(semana_siguiente) and i < len(semana_siguiente_original):
                # Nombre del valor del turno
                if tipo_turno == "3 turnos" and i < len(nombres_fechas):
                    # Verificar si es sábado
                    if nombres_fechas[i] == "Saturday":
                        if semana_siguiente[i] == "A":
                            valor_turno = "A (3 turnos) - Sabado"
                        elif semana_siguiente[i] == "B":
                            valor_turno = "B (3 turnos) - Sabado"
                        else:
                            valor_turno = semana_siguiente_original[i]
                    else:       
                        # Asignar el valor del turno       
                        valor_turno = semana_siguiente_original[i]
                    
                elif tipo_turno == "4 turnos":
                    # Asignar el valor del turno
                    valor_turno = semana_siguiente_original[i]
                
                elif tipo_turno == "ADM":
                    
                    # Verificar si es viernes
                    if nombres_fechas[i] == "Friday":
                        valor_turno = "ADM - Viernes"
                    # Verificar si es sabado
                    elif nombres_fechas[i] == "Saturday":
                        valor_turno = "ADM - Sabado"
                    # Verificar si es lunes | martes | miercoles | jueves
                    elif nombres_fechas[i] == "Monday" or nombres_fechas[i] == "Tuesday" or nombres_fechas[i] == "Wednesday" or nombres_fechas[i] == "Thursday":
                        valor_turno = "ADM - Lun a Jue"
                    else:       
                        # Asignar el valor del turno       
                        valor_turno = semana_siguiente_original[i]
                                
            # Append al arreglo de los objetos
            elemento_respuesta = {
                "ClaveParaBuscar": clave_unica,
                "TipoTurno": tipo_turno,
                "ValorTurno": valor_turno
            }
            elementos_respuesta.append(elemento_respuesta)
    
    return {"detalle": datos, "respuesta": elementos_respuesta}

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Get the content length
        content_length = int(self.headers['Content-Length'])
        # Read the post data
        post_data = self.rfile.read(content_length)
        # Parse the JSON data
        datos = json.loads(post_data)
        
        # Process the data
        result = process_data(datos)
        
        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        # Send the result
        self.wfile.write(json.dumps(result).encode())
        return

# Main function for DigitalOcean Functions
def main(args):
    """Entry point for DigitalOcean Function"""
    try:
        # If the request is via HTTP
        if "http" in args and "body" in args["http"]:
            # Get the body content
            body = args["http"]["body"]
            # Parse the JSON data
            if isinstance(body, str):
                datos = json.loads(body)
            else:
                datos = body
                
            # Process the data
            result = process_data(datos)
            
            # Return the result
            return {
                "body": result,
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json"
                }
            }
        else:
            # Direct invocation with JSON data
            result = process_data(args)
            return result
            
    except Exception as e:
        # Return error message
        return {
            "body": {"error": str(e)},
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            }
        }