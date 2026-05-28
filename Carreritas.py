import random
import time

print("======================================")
print("\nBIENVENIDO A EXTREME RACING SIMULATOR\n")
print("======================================")

# Base de datos de los autos
AUTOS_BASE = {
    "Speedster 200": {
        "precio": 50000, 
        "velocidad": 180, 
        "aceleracion": 75,
        "manejo": 70, 
        "resistencia": 60
    },
    "Thunder GT": {
        "precio": 120000, 
        "velocidad": 220, 
        "aceleracion": 90,
        "manejo": 65, 
        "resistencia": 70
    },
    "Phoenix Pro": {
        "precio": 250000, 
        "velocidad": 280, 
        "aceleracion": 95,
        "manejo": 80, 
        "resistencia": 85
    },
    "Midnight Black": {
        "precio": 180000, 
        "velocidad": 240, 
        "aceleracion": 85, 
        "manejo": 88, 
        "resistencia": 75
    },
    "Diamond Racer": {
        "precio": 500000, 
        "velocidad": 320, 
        "aceleracion": 98,
        "manejo": 92, 
        "resistencia": 90
    },
}

# Base de datos de mejoras disponibles para los autos
MEJORAS = {
    10: {},
    "Motor Turbo": {"costo": 15000, "velocidad": 30, "aceleracion": 15},
    "Suspension Deportiva": {"costo": 12000, "manejo": 20, "resistencia": 10},
    "Frenos de Ceramica": {"costo": 10000, "resistencia": 25, "manejo": 15},
    "Chasis Ligero": {"costo": 18000, "aceleracion": 20, "velocidad": 25},
    "Aerodinamico": {"costo": 20000, "velocidad": 35, "manejo": 10},
    "Sistema ECU": {"costo": 8000, "aceleracion": 10, "manejo": 10},
}

# Base de datos de circuitos disponibles para competir
CIRCUITOS = {
    "Monza Express": {
        "dificultad": "Facil", 
        "distancia": 100, 
        "rivales": 3,
        "premio": 10000
    },
    "Mountain Challenge": {
        "dificultad": "Media", 
        "distancia": 150,
        "rivales": 5, 
        "premio": 25000
    },
    "Nurburgring Storm": {
        "dificultad": "Dificil", 
        "distancia": 200,
        "rivales": 7, 
        "premio": 50000
    },
    "Desert Burnout": {
        "dificultad": "Muy Dificil", 
        "distancia": 250,
        "rivales": 8, 
        "premio": 100000
    },
    "Night City Grand Prix": {
        "dificultad": "Extrema", 
        "distancia": 300,
        "rivales": 10, 
        "premio": 200000
    },
}

NOMBRES_RIVALES = [
    "Lightning Max", "Smoke", "Rey del Asfalto", "Ghost", "Turbina",
    "Serpiente", "Fenomeno", "Diablo", "Rapido Ricardo", "Sonic Silva"
]


class Corredor:
    # Gestiona el inventario, fondos y progresion del jugador
    def __init__(self, nombre):
        self.nombre = nombre
        self.dinero = 100000
        self.auto = None
        self.mejoras = {}
        self.historial_carreras = []
        self.victorias = 0
        self.derrotas = 0
        self.dinero_ganado = 0
        self.nivel = 1
        self.experiencia = 0

    def comprar_auto(self, modelo):
        # Valida que el dinero sea suficiente y asigna el auto al jugador
        precio = AUTOS_BASE[modelo]["precio"]
        
        if self.dinero >= precio:
            self.dinero -= precio
            self.auto = AUTOS_BASE[modelo].copy()
            self.mejoras = {}
            print(f"Compra exitosa: {modelo}")
            return True
            
        print(f"Fondos insuficientes. Necesitas ${precio}. Dinero actual: {self.dinero}")
        return False

    def mejorar_auto(self, mejora):
        # Repite los atributos de la mejora y aplica los modificadores matematicos al auto actual
        if not self.auto:
            print("Debes comprar un auto primero.")
            return False
            
        if mejora in self.mejoras:
            print(f"Ya posees la mejora: {mejora}")
            return False
            
        costo = MEJORAS[mejora]["costo"]
        
        if self.dinero >= costo:
            self.dinero -= costo
            self.mejoras[mejora] = True
            
            for atributo, bonus in MEJORAS[mejora].items():
                if atributo != "costo" and atributo in self.auto:
                    self.auto[atributo] += bonus
                    
            print(f"Mejora instalada: {mejora}. Estadisticas actualizadas.")
            return True
            
        print(f"Fondos insuficientes para esta mejora. Costo: ${costo}")
        return False

    def agregar_experiencia(self, cantidad):
        # Actualiza la experiencia mediante un ciclo while para procesar multiples subidas de nivel si es necesario
        self.experiencia += cantidad
        
        while self.experiencia >= 100:
            self.nivel += 1
            self.experiencia -= 100
            self.dinero += 50000
            print(f"Subiste de nivel! Ahora eres nivel {self.nivel}. Recibes bonus de $50,000")


def simular_carrera(corredor, circuito_nombre):
    # Ejecuta el ciclo de simulacion de la carrera.
    if not corredor.auto:
        print("Necesitas un auto para correr.")
        return False
        
    circuito = CIRCUITOS[circuito_nombre]
    print(f"\n--- INICIANDO CARRERA: {circuito_nombre} ---")
    print(f"Distancia: {circuito['distancia']} km | Rivales: {circuito['rivales']}")
    time.sleep(1)
    
    # Calcula distancias e inyecta perturbaciones aleatorias para simular clima y eventos del vehiculo
    clima = random.choice(["Despejado", "Lluvia", "Niebla", "Tormenta"])
    factor_clima = 0.7 if clima in ["Lluvia", "Tormenta"] else (0.8 if clima == "Niebla" else 1.0)
    print(f"Condicion climatica: {clima} (Factor de manejo: {factor_clima})")
    
    # Generador de rivales con estado inicial de distancia 0
    rivales = [
        {"nombre": random.choice(NOMBRES_RIVALES), "velocidad": random.randint(150, 300), "distancia": 0} 
        for _ in range(circuito['rivales'])
    ]
    
    distancia_jugador = 0
    daño_auto = 0
    eventos_carrera = []
    
    # Ajuste de estadisticas del jugador con el factor ambiental
    velocidad_j = corredor.auto["velocidad"] * factor_clima
    acel_j = corredor.auto["aceleracion"]
    manejo_j = corredor.auto["manejo"] * factor_clima
    resis_j = corredor.auto["resistencia"]
    etapa = 0
    
    # Bucle principal de la simulación
    while distancia_jugador < circuito['distancia']:
        etapa += 1
        print(f"\n--- ETAPA {etapa} --- Progreso: {int(distancia_jugador)}/{circuito['distancia']} km")
        
        avance = random.randint(5, 15) + (acel_j / 10)
        distancia_jugador += avance
        
        evento = random.random()
        if evento < 0.1 and daño_auto < 30:
            print("Evento: Pinchazo detectado (-5km, +15% daño)")
            distancia_jugador -= 5
            daño_auto += 15
            eventos_carrera.append("Pinchazo")
            
        elif evento < 0.15 and manejo_j > 50:
            print("Evento: Drift Perfecto (+8km)")
            distancia_jugador += 8
            eventos_carrera.append("Drift Perfecto")
            
        elif evento < 0.2 and resis_j > 60:
            print("Evento: Sobrecalentamiento (-3km, +10% daño)")
            distancia_jugador -= 3
            daño_auto += 10
            eventos_carrera.append("Sobrecalentamiento")
            
        elif evento < 0.08:
            print("Evento: Turbo activado (+12km)")
            distancia_jugador += 12
            eventos_carrera.append("Turbo")
            
        # Avance algoritmico de los rivales
        for r in rivales:
            r["distancia"] += random.randint(5, 10) + (r["velocidad"] / 50)
            
        if daño_auto >= 100:
            print("\nDaño critico. Auto descompuesto. Descalificacion automatica.")
            corredor.derrotas += 1
            corredor.agregar_experiencia(10)
            return False
            
        time.sleep(0.5)
        
    # Calculo algoritmico de posiciones finales comparando distancias recorridas
    mi_posicion = 1 + sum(1 for r in rivales if r["distancia"] > distancia_jugador)
    print(f"\nRESULTADO FINAL: Posicion {mi_posicion} de {len(rivales) + 1}")
    
    # Asignacion matematica de premios y experiencia
    porcentajes_premio = {1: 1.0, 2: 0.6, 3: 0.4}
    premio = int(circuito['premio'] * porcentajes_premio.get(mi_posicion, 0.2))
    
    if mi_posicion == 1:
        corredor.victorias += 1
        corredor.agregar_experiencia(50)
    elif mi_posicion <= 3:
        corredor.agregar_experiencia(40 - (mi_posicion * 10))
    else:
        corredor.derrotas += 1
        corredor.agregar_experiencia(15)
        
    corredor.dinero += premio
    corredor.dinero_ganado += premio
    
    corredor.historial_carreras.append({
        "circuito": circuito_nombre, 
        "posicion": mi_posicion,
        "premio": premio, 
        "eventos": eventos_carrera
    })
    
    print(f"Premio liquidado: ${premio:,}")
    return True


def menu_principal(corredor):
    # Interfaz de entrada de comandos
    while True:
        print("\n-- MENU PRINCIPAL ---")
        print("1. Ver perfil\n2. Comprar auto\n3. Mejorar auto\n4. Ver circuitos")
        print("5. Correr carrera\n6. Ver historial\n7. Salir")
        
        opcion = input("Elige una opcion numerica (1-7): ").strip()
        
        if opcion == "1":
            print(f"\nPerfil: {corredor.nombre} | Nivel: {corredor.nivel} | Dinero: ${corredor.dinero:,}")
            print(f"Auto actual: {corredor.auto['velocidad']} vel, {corredor.auto['aceleracion']} acel" if corredor.auto else "Auto actual: Ninguno")
            print(f"Victorias: {corredor.victorias} | Derrotas: {corredor.derrotas}")
            
        elif opcion == "2":
            print("\n-- TIENDA DE AUTOS --")
            for m, s in AUTOS_BASE.items():
                print(f"[{m}] Precio: ${s['precio']:,} | Vel: {s['velocidad']} | Acel: {s['aceleracion']}")
            auto = input("Escribe el nombre exacto del auto a comprar (o 0 para cancelar): ").strip()
            if auto in AUTOS_BASE:
                corredor.comprar_auto(auto)
                
        elif opcion == "3":
            print("\n-- TALLER DE MEJORAS --")
            for m, s in MEJORAS.items():
                if type(m) == str:
                    print(f"[{m}] Costo: ${s['costo']:,}")
            mejora = input("Escribe el nombre exacto de la mejora (o 0 para cancelar): ").strip()
            if mejora in MEJORAS:
                corredor.mejorar_auto(mejora)
                
        elif opcion == "4":
            print("\n-- CIRCUITOS DISPONIBLES --")
            for c, d in CIRCUITOS.items():
                print(f"[{c}] Dificultad: {d['dificultad']} | {d['distancia']} km | Premio Base: ${d['premio']:,}")
                
        elif opcion == "5":
            circuito = input("\nEscribe el nombre exacto del circuito a correr (o 0 para cancelar): ").strip()
            if circuito in CIRCUITOS:
                simular_carrera(corredor, circuito)
            elif circuito != "0":
                print("Circuito no encontrado en la base de datos.")
                
        elif opcion == "6":
            print("\n-- HISTORIAL DE CARRERAS --")
            if not corredor.historial_carreras:
                print("Sin registros en la base de datos.")
            for i, c in enumerate(corredor.historial_carreras, 1):
                print(f"{i}. {c['circuito']} | Posicion: {c['posicion']} | Premio: ${c['premio']:,}")
                
        elif opcion == "7":
            print("Cerrando el simulador...")
            break
        else:
            print("Input no reconocido.")


if __name__ == "__main__":
    nombre = input("\nIntroduce tu nombre de corredor: ").strip() or "Anonimo"
    jugador = Corredor(nombre)
    print(f"\nSesion iniciada. Cuentas con un saldo inicial de $100,000.")
    menu_principal(jugador)