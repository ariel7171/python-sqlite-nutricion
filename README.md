# Sistema de Nutrición con SQLite

Este proyecto implementa un sistema simple para gestionar pacientes, alimentos y planes de comidas para una nutricionista, utilizando SQLite como base de datos.

## Características

- Gestión de pacientes (agregar, listar, actualizar, eliminar)
- Gestión de alimentos con su información nutricional
- Creación y seguimiento de planes de comida
- Cálculo de calorías consumidas por paciente
- Implementación de transacciones para mantener la integridad de los datos

## Estructura del proyecto

```
proyecto_nutricion/
│
├── app/
│   ├── models/        # Clases de modelo (Paciente, Alimento, PlanComida)
│   ├── repository/    # Capa de acceso a datos
│   └── utils/         # Funciones auxiliares
│
├── database/          # Directorio donde se almacena la base de datos
│
├── main.py            # Punto de entrada principal
└── README.md          # Esta documentación
```

## Requisitos

- Python 3.6+
- SQLite (incluido en la biblioteca estándar de Python)

## Instalación

1. Clonar el repositorio
2. No se requiere instalación adicional, SQLite ya está incluido en Python

## Uso

Ejecutar el archivo principal:
```
python main.py
```

## Ejemplo de uso

```python
from app.models import Paciente, Alimento, PlanComida
from app.repository import NutricionistaRepo

# Crear repositorio (conexión a BD)
repo = NutricionistaRepo()

# Crear un paciente
paciente = Paciente(nombre="Ana López", edad=35, peso_actual=68.5)
paciente_id = repo.crear_paciente(paciente)

# Crear un alimento
manzana = Alimento(nombre="Manzana", calorias=52)
manzana_id = repo.crear_alimento(manzana)

# Crear un plan de comida
plan = PlanComida(
    paciente_id=paciente_id,
    alimento_id=manzana_id,
    fecha="2023-06-15",
    cantidad=2.0  # 2 manzanas
)
plan_id = repo.crear_plan_comida(plan)

# Listar planes de comida
planes = repo.listar_planes_comida()
for plan in planes:
    print(f"Paciente: {plan['paciente_nombre']}, "
          f"Alimento: {plan['alimento_nombre']}, "
          f"Calorías totales: {plan['calorias_totales']}")

# Siempre cerrar la conexión al finalizar
repo.close()
```