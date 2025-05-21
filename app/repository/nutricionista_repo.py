import sqlite3
import os
from typing import List, Optional, Dict, Tuple
from app.models import Paciente, Alimento, PlanComida

class NutricionistaRepo:
    def __init__(self, db_path: str = "database/nutricion.db"):
        # Asegurarse que la carpeta database existe
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._crear_tablas()
    
    def _crear_tablas(self) -> None:
        with self.conn:
            self.conn.execute('''
            CREATE TABLE IF NOT EXISTS pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                edad INTEGER NOT NULL,
                peso_actual REAL NOT NULL
            )
            ''')
            
            self.conn.execute('''
            CREATE TABLE IF NOT EXISTS alimentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                calorias INTEGER NOT NULL
            )
            ''')
            
            self.conn.execute('''
            CREATE TABLE IF NOT EXISTS plan_comidas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                alimento_id INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                cantidad REAL NOT NULL,
                FOREIGN KEY(paciente_id) REFERENCES pacientes(id),
                FOREIGN KEY(alimento_id) REFERENCES alimentos(id)
            )
            ''')
    
    def close(self) -> None:
        if self.conn:
            self.conn.close()
    
    # --- Métodos para Pacientes ---
    
    def crear_paciente(self, paciente: Paciente) -> int:
        with self.conn:
            cursor = self.conn.execute(
                'INSERT INTO pacientes (nombre, edad, peso_actual) VALUES (?, ?, ?)',
                (paciente.nombre, paciente.edad, paciente.peso_actual)
            )
            return cursor.lastrowid
    
    def obtener_paciente(self, paciente_id: int) -> Optional[Paciente]:
        cursor = self.conn.execute('SELECT * FROM pacientes WHERE id = ?', (paciente_id,))
        row = cursor.fetchone()
        if row:
            return Paciente(
                id=row['id'],
                nombre=row['nombre'],
                edad=row['edad'],
                peso_actual=row['peso_actual']
            )
        return None
    
    def listar_pacientes(self) -> List[Paciente]:
        cursor = self.conn.execute('SELECT * FROM pacientes')
        return [Paciente(
            id=row['id'],
            nombre=row['nombre'],
            edad=row['edad'],
            peso_actual=row['peso_actual']
        ) for row in cursor.fetchall()]
    
    def actualizar_paciente(self, paciente: Paciente) -> bool:
        with self.conn:
            cursor = self.conn.execute(
                'UPDATE pacientes SET nombre = ?, edad = ?, peso_actual = ? WHERE id = ?',
                (paciente.nombre, paciente.edad, paciente.peso_actual, paciente.id)
            )
            return cursor.rowcount > 0
    
    def eliminar_paciente(self, paciente_id: int) -> bool:
        with self.conn:
            cursor = self.conn.execute('DELETE FROM pacientes WHERE id = ?', (paciente_id,))
            return cursor.rowcount > 0
    
    # --- Métodos para Alimentos ---
    
    def crear_alimento(self, alimento: Alimento) -> int:
        with self.conn:
            cursor = self.conn.execute(
                'INSERT INTO alimentos (nombre, calorias) VALUES (?, ?)',
                (alimento.nombre, alimento.calorias)
            )
            return cursor.lastrowid
    
    def obtener_alimento(self, alimento_id: int) -> Optional[Alimento]:
        cursor = self.conn.execute('SELECT * FROM alimentos WHERE id = ?', (alimento_id,))
        row = cursor.fetchone()
        if row:
            return Alimento(
                id=row['id'],
                nombre=row['nombre'],
                calorias=row['calorias']
            )
        return None
    
    def listar_alimentos(self) -> List[Alimento]:
        cursor = self.conn.execute('SELECT * FROM alimentos')
        return [Alimento(
            id=row['id'],
            nombre=row['nombre'],
            calorias=row['calorias']
        ) for row in cursor.fetchall()]
    
    def actualizar_alimento(self, alimento: Alimento) -> bool:
        with self.conn:
            cursor = self.conn.execute(
                'UPDATE alimentos SET nombre = ?, calorias = ? WHERE id = ?',
                (alimento.nombre, alimento.calorias, alimento.id)
            )
            return cursor.rowcount > 0
    
    def eliminar_alimento(self, alimento_id: int) -> bool:
        with self.conn:
            cursor = self.conn.execute('DELETE FROM alimentos WHERE id = ?', (alimento_id,))
            return cursor.rowcount > 0
    
    # --- Metodos para Planes de Comida ---
    
    def crear_plan_comida(self, plan: PlanComida) -> int:
        with self.conn:
            cursor = self.conn.execute(
                'INSERT INTO plan_comidas (paciente_id, alimento_id, fecha, cantidad) VALUES (?, ?, ?, ?)',
                (plan.paciente_id, plan.alimento_id, plan.fecha, plan.cantidad)
            )
            return cursor.lastrowid
    
    def obtener_plan_comida(self, plan_id: int) -> Optional[PlanComida]:
        cursor = self.conn.execute('SELECT * FROM plan_comidas WHERE id = ?', (plan_id,))
        row = cursor.fetchone()
        if row:
            return PlanComida(
                id=row['id'],
                paciente_id=row['paciente_id'],
                alimento_id=row['alimento_id'],
                fecha=row['fecha'],
                cantidad=row['cantidad']
            )
        return None
    
    def listar_planes_comida(self) -> List[Dict]:
        cursor = self.conn.execute('''
            SELECT 
                pc.id, 
                p.nombre AS paciente_nombre, 
                a.nombre AS alimento_nombre,
                pc.fecha, 
                pc.cantidad,
                a.calorias * pc.cantidad AS calorias_totales
            FROM plan_comidas pc
            JOIN pacientes p ON pc.paciente_id = p.id
            JOIN alimentos a ON pc.alimento_id = a.id
        ''')
        return [dict(row) for row in cursor.fetchall()]
    
    def actualizar_plan_comida(self, plan: PlanComida) -> bool:
        with self.conn:
            cursor = self.conn.execute(
                'UPDATE plan_comidas SET paciente_id = ?, alimento_id = ?, fecha = ?, cantidad = ? WHERE id = ?',
                (plan.paciente_id, plan.alimento_id, plan.fecha, plan.cantidad, plan.id)
            )
            return cursor.rowcount > 0
    
    def eliminar_plan_comida(self, plan_id: int) -> bool:
        with self.conn:
            cursor = self.conn.execute('DELETE FROM plan_comidas WHERE id = ?', (plan_id,))
            return cursor.rowcount > 0
    
    def actualizar_peso_paciente(self, paciente_id: int, nuevo_peso: float) -> bool:
        with self.conn:
            cursor = self.conn.execute(
                'UPDATE pacientes SET peso_actual = ? WHERE id = ?',
                (nuevo_peso, paciente_id)
            )
            return cursor.rowcount > 0
    
    def crear_todo_nuevo(self, paciente: Paciente, alimento: Alimento, plan: PlanComida) -> Tuple[int, int, int]:
        try:
            self.conn.execute("BEGIN TRANSACTION")
            
            # Crear paciente
            cursor = self.conn.execute(
                'INSERT INTO pacientes (nombre, edad, peso_actual) VALUES (?, ?, ?)',
                (paciente.nombre, paciente.edad, paciente.peso_actual)
            )
            paciente_id = cursor.lastrowid
            
            # Crear alimento
            cursor = self.conn.execute(
                'INSERT INTO alimentos (nombre, calorias) VALUES (?, ?)',
                (alimento.nombre, alimento.calorias)
            )
            alimento_id = cursor.lastrowid
            
            # Crear plan de comida
            plan.paciente_id = paciente_id
            plan.alimento_id = alimento_id
            cursor = self.conn.execute(
                'INSERT INTO plan_comidas (paciente_id, alimento_id, fecha, cantidad) VALUES (?, ?, ?, ?)',
                (plan.paciente_id, plan.alimento_id, plan.fecha, plan.cantidad)
            )
            plan_id = cursor.lastrowid
            
            self.conn.commit()
            return paciente_id, alimento_id, plan_id
        
        except Exception as e:
            self.conn.rollback()
            print(f"Error en la transacción: {e}")
            raise