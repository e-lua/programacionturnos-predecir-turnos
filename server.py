from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.programacion_turnos import ProgramacionTurnosService
from pydantic import BaseModel
from typing import Optional

# Entrada original
datos = [
  {
    "Cedula": "1143385684",
    "ApellidoNombre": "RODRIGUEZ LORDUY ELKIN FRANCISCO",
    "TipoTurno":"",
    "SemanaAnteriorOriginal": "A (4 turnos),A (4 turnos),A (4 turnos - Sabado),A (4 turnos),A (4 turnos),A (4 turnos),ADM",
    "SemanaAnterior": "",
    "SemanaSiguiente": ""
  },
  {
    "Cedula": "1235044947",
    "ApellidoNombre": "AGAMEZ ALVAREZ PEDRO LUÍS",
    "TipoTurno":"",
    "SemanaAnteriorOriginal": "VACACIONES,C (4 turnos),C (4 turnos),DESCANSO,C (4 turnos),C (4 turnos),C (4 turnos)",
    "SemanaAnterior": "",
    "SemanaSiguiente": ""
  },
  {
    "Cedula": "73008313",
    "ApellidoNombre": "TATIS ALZUZAR JAMER YESIT",
    "TipoTurno":"",
    "SemanaAnteriorOriginal": "C (4 turnos),C (4 turnos - Sabado),C (4 turnos),C (4 turnos),C (4 turnos),C (4 turnos),DESCANSO",
    "SemanaAnterior": "",
    "SemanaSiguiente": ""
  },
  {
    "Cedula": "1047392733",
    "ApellidoNombre": "HUERTAS GUERRERO JHON ALEXANDER",
    "TipoTurno":"",
    "SemanaAnteriorOriginal": "DESCANSO,B (4 turnos),B (4 turnos),B (4 turnos),B (4 turnos),B (4 turnos),DESCANSO",
    "SemanaAnterior": "",
    "SemanaSiguiente": ""
  },
  {
    "Cedula": "2047392766",
    "ApellidoNombre": "LOPEZ LUA EDWARD",
    "TipoTurno":"",
    "SemanaAnteriorOriginal": "B (4 turnos),VACACIONES,VACACIONES,A (4 turnos),A (4 turnos),A (4 turnos),A (4 turnos)",
    "SemanaAnterior": "",
    "SemanaSiguiente": ""
  },
  {
    "Cedula": "2997392006",
    "ApellidoNombre": "PEREZ LOPEZ ANTONIO",
    "TipoTurno":"",
    "SemanaAnteriorOriginal": "A (3 turnos),A (3 turnos),A (3 turnos),A (3 turnos),A (3 turnos),A (3 turnos),C (3 turnos)",
    "SemanaAnterior": "",
    "SemanaSiguiente": ""
  }
]

# Definir el modelo
class Elemento(BaseModel):
    Cedula: str
    ApellidoNombre: str
    TipoTurno: Optional[str] = None
    SemanaAnteriorOriginal: str
    SemanaAnterior: Optional[str] = None
    SemanaSiguiente: Optional[str] = None

# Initialize FastAPI
app = FastAPI()

# Configurar CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "null",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"Unauthorized access"}

@app.post(
    "/v1/predecir-turnos-semana",
    name="Predecir turnos de la semana",
    description="Permite predecir los turnos de la semana",
)
async def predecir_turnos(datos:  list[Elemento]):

    # Actualizar el tipo de turno
    for elemento in datos:
        semana_anterior = elemento.SemanaAnteriorOriginal.split(",")
        
        tipo_turno = ""
        
        for turno in reversed(semana_anterior):
            
            if "3 turnos" in turno:
                tipo_turno="3 turnos"
                break
            
            elif "4 turnos" in turno:
                tipo_turno="4 turnos"
                break
        
        # Asignarlo al campo "TipoTuno"
        elemento.TipoTurno =tipo_turno
        
    # Actualizar el campo "SemanaAnterior"
    for elemento in datos:
        semana_original = elemento.SemanaAnteriorOriginal.split(",")  # Dividir por coma
        semana_actualizada = []

        for turno in semana_original:
            if "A (" in turno:
                semana_actualizada.append("A")
            elif "B (" in turno:
                semana_actualizada.append("B")
            elif "C (" in turno:
                semana_actualizada.append("C")
            else:
                semana_actualizada.append("X")  # Valor por defecto para no A, B, C

        # Unir la lista actualizada y asignarla al campo "SemanaAnterior"
        elemento.SemanaAnterior = ",".join(semana_actualizada)

    # Predecir turnos de la siguiente semana
    for elemento in datos:

        if elemento.TipoTurno == "4 turnos":
            semana_anterior = elemento.SemanaAnterior.split(",")
            semana_siguiente = ProgramacionTurnosService.predecir_siguiente_semana_4_turnos(semana_anterior)
            
            # Asignarlo al campo "SemanaSiguiente"
            elemento.SemanaSiguiente= ",".join(semana_siguiente)
        else:
            semana_anterior = elemento.SemanaAnterior.split(",")
            semana_siguiente = ProgramacionTurnosService.predecir_siguiente_semana_3_turnos(semana_anterior)
            
            # Asignarlo al campo "SemanaSiguiente"
            elemento.SemanaSiguiente= ",".join(semana_siguiente)
            
    return datos