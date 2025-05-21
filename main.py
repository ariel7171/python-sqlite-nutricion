from app.models import Paciente, Alimento, PlanComida
from app.repository import NutricionistaRepo
from app.utils import validar_fecha

def demo():
    """Función de demostración para probar todas las funcionalidades del sistema."""
    # Crear instancia del repositorio
    repo = NutricionistaRepo()
    
    try:
        # 1. Agregar algunos pacientes
        paciente1 = Paciente(nombre="Ana López", edad=35, peso_actual=68.5)
        paciente2 = Paciente(nombre="Carlos Martínez", edad=42, peso_actual=81.2)
        
        paciente1_id = repo.crear_paciente(paciente1)
        paciente2_id = repo.crear_paciente(paciente2)
        
        print(f"Pacientes creados con IDs: {paciente1_id}, {paciente2_id}")
        
        # 2. Agregar algunos alimentos
        alimento1 = Alimento(nombre="Manzana", calorias=52)
        alimento2 = Alimento(nombre="Yogur natural", calorias=59)
        alimento3 = Alimento(nombre="Pollo a la plancha", calorias=165)
        
        alimento1_id = repo.crear_alimento(alimento1)
        alimento2_id = repo.crear_alimento(alimento2)
        alimento3_id = repo.crear_alimento(alimento3)
        
        print(f"Alimentos creados con IDs: {alimento1_id}, {alimento2_id}, {alimento3_id}")
        
        # 3. Agregar planes de comida
        fecha = "2023-06-15"
        if validar_fecha(fecha):  # Uso de la función helper
            plan1 = PlanComida(
                paciente_id=paciente1_id,
                alimento_id=alimento1_id,
                fecha=fecha,
                cantidad=2.0  # 2 manzanas
            )
            
            plan2 = PlanComida(
                paciente_id=paciente1_id,
                alimento_id=alimento3_id,
                fecha=fecha,
                cantidad=0.3  # 300g de pollo
            )
            
            plan3 = PlanComida(
                paciente_id=paciente2_id,
                alimento_id=alimento2_id,
                fecha=fecha,
                cantidad=1.0  # 1 yogur
            )
            
            plan1_id = repo.crear_plan_comida(plan1)
            plan2_id = repo.crear_plan_comida(plan2)
            plan3_id = repo.crear_plan_comida(plan3)
            
            print(f"Planes de comida creados con IDs: {plan1_id}, {plan2_id}, {plan3_id}")
        
        # 4. Listar todos los pacientes
        print("\n--- Listado de Pacientes ---")
        for paciente in repo.listar_pacientes():
            print(paciente)
        
        # 5. Listar todos los alimentos
        print("\n--- Listado de Alimentos ---")
        for alimento in repo.listar_alimentos():
            print(alimento)
        
        # 6. Listar planes de comida con detalles
        print("\n--- Listado de Planes de Comida ---")
        planes = repo.listar_planes_comida()
        for plan in planes:
            print(f"ID: {plan['id']}, Paciente: {plan['paciente_nombre']}, "
                  f"Alimento: {plan['alimento_nombre']}, Fecha: {plan['fecha']}, "
                  f"Cantidad: {plan['cantidad']}, Calorías totales: {plan['calorias_totales']}")
        
        # 7. Actualizar el peso de un paciente
        print("\n--- Actualización de Peso ---")
        nuevo_peso = 67.8
        exito = repo.actualizar_peso_paciente(paciente1_id, nuevo_peso)
        if exito:
            paciente_actualizado = repo.obtener_paciente(paciente1_id)
            print(f"Peso actualizado: {paciente_actualizado}")
        
        # 8. Eliminar un plan de comida
        print("\n--- Eliminación de Plan de Comida ---")
        exito = repo.eliminar_plan_comida(plan3_id)
        print(f"Plan de comida eliminado: {exito}")
        
        # 9. Verificar que se eliminó (listamos de nuevo)
        print("\n--- Listado actualizado de Planes de Comida ---")
        planes = repo.listar_planes_comida()
        for plan in planes:
            print(f"ID: {plan['id']}, Paciente: {plan['paciente_nombre']}, "
                  f"Alimento: {plan['alimento_nombre']}")
        
        # 10. Eliminar un paciente
        print("\n--- Eliminación de Paciente ---")
        exito = repo.eliminar_paciente(paciente2_id)
        print(f"Paciente eliminado: {exito}")
        
        # 11. Crear todo nuevo en una transacción
        print("\n--- Creación en Transacción ---")
        nuevo_paciente = Paciente(nombre="Laura García", edad=28, peso_actual=65.7)
        nuevo_alimento = Alimento(nombre="Ensalada mixta", calorias=45)
        nuevo_plan = PlanComida(fecha="2023-06-16", cantidad=1.5)  # IDs se asignarán automáticamente
        
        paciente_id, alimento_id, plan_id = repo.crear_todo_nuevo(nuevo_paciente, nuevo_alimento, nuevo_plan)
        print(f"Creados en transacción - Paciente ID: {paciente_id}, Alimento ID: {alimento_id}, Plan ID: {plan_id}")
        
        # 12. Provocar un error en transacción para demostrar rollback
        try:
            print("\n--- Provocando Error en Transacción ---")
            paciente_invalido = Paciente(nombre="", edad=-5, peso_actual=-10)  # Datos inválidos
            alimento_valido = Alimento(nombre="Chocolate", calorias=546)
            plan_valido = PlanComida(fecha="2023-06-17", cantidad=0.2)
            
            repo.crear_todo_nuevo(paciente_invalido, alimento_valido, plan_valido)
        except Exception as e:
            print(f"Error capturado como se esperaba: {e}")
            
        # 13. Verificar el estado final de la base de datos
        print("\n--- Estado Final de Pacientes ---")
        for paciente in repo.listar_pacientes():
            print(paciente)
            
    finally:
        # Siempre cerrar la conexión
        repo.close()


if __name__ == "__main__":
    demo()