import sqlite3
from typing import List, Optional, Callable
class Libro:
    def __init__(self, titulo: str, autor: str, anio: int, libro_id: Optional[int] = None):
        self.id = libro_id
        self.titulo = titulo
        self.autor = autor
        self.anio = anio
    #Constructor alternativo que permite crear instancias de Libro a partir de un registro SQLite
    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "Libro":
        return cls(
            titulo=row["titulo"],
            autor=row["autor"],
            anio=row["anio"],
            libro_id=row["id"]
        )

    def __repr__(self):
        return f"Libro(id={self.id!r}, titulo={self.titulo!r}, autor={self.autor!r}, año={self.anio!r})"
        #return f"Libro(id={repr(self.id)}, titulo={repr(self.titulo)}, autor={repr(self.autor)}, año={repr(self.anio)})"


class RepositorioLibros:
    def __init__(self, db_path: str = "libros.db"):
        # Por defecto sqlite3 abre en modo transactions#
        self.conn = sqlite3.connect(db_path)       #conn es de tipo Connection
        self.conn.row_factory = sqlite3.Row        #configura el cursor para indexar por nombre de columna
        self._create_table()

    def _create_table(self):                       #protegido por convención- uso interno
        sql = """
        CREATE TABLE IF NOT EXISTS libros (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo   TEXT NOT NULL,
            autor  TEXT NOT NULL,
            anio    INTEGER NOT NULL
        ) STRICT;                                  
        """
        with self.conn:
            self.conn.execute(sql)

    def add_libro(self, libro: Libro) -> int:
        """
        Inserta un libro; si falla, se revierte automáticamente.
        """
        with self.conn:
            cursor = self.conn.execute(
                "INSERT INTO libros (titulo, autor, anio) VALUES (?, ?, ?);",
                (libro.titulo, libro.autor, libro.anio)
            )
            libro.id = cursor.lastrowid     #devuelve el id autogenerado por la última inserción.
            return libro.id



    def get_libro(self, libro_id: int) -> Optional[Libro]:    #devuelve un Libro o None
        cursor = self.conn.execute(
            "SELECT * FROM libros WHERE id = ?;",
            (libro_id,)
        )
        row = cursor.fetchone()
        return Libro.from_row(row) if row else None    #usamos el constructor alternativo de la clase libro

    def list_libros(self) -> List[Libro]:
        cursor = self.conn.execute("SELECT * FROM libros;")
        return [Libro.from_row(row) for row in cursor.fetchall()]  #lista por convencion de filas de la tabla libros

    def buscar_por_autor(self, autor: str) -> List[Libro]:
        cursor = self.conn.execute(
            "SELECT * FROM libros WHERE autor LIKE ?;",
            (f"%{autor}%",)
        )
        return [Libro.from_row(row) for row in cursor.fetchall()]

    def buscar_por_titulo(self, titulo: str) -> List[Libro]:
        cursor = self.conn.execute(
            "SELECT * FROM libros WHERE titulo LIKE ?;",
            (f"%{titulo}%",)
        )
        return [Libro.from_row(row) for row in cursor.fetchall()]

    def update_libro(self, libro: Libro) -> bool:
        with self.conn:
            cursor = self.conn.execute(
                "UPDATE libros SET titulo = ?, autor = ?, anio = ? WHERE id = ?;",
                (libro.titulo, libro.autor, libro.anio, libro.id)
            )
            return cursor.rowcount > 0         #cantidad de filas afectadas por un UPDATE > 0

    def delete_libro(self, libro_id: int) -> bool:
        with self.conn:
            cursor = self.conn.execute(
                "DELETE FROM libros WHERE id = ?;",
                (libro_id,)
            )
            return cursor.rowcount > 0       #cantidad de filas afectadas por un DELETE > 0

    def ejecutar_transaccion(self, operaciones: Callable[["RepositorioLibros"], None]) -> bool:
        """
        El parametro operaciones es una función que espera un argumento de tipo RepositorioLibros y no retorna nada.
        Esta funcion permite agrupar múltiples operaciones en una única transacción:
        si alguna falla se revierteó
        """
        try:
            with self.conn:
                operaciones(self)
            return True
        except sqlite3.Error as e:
            print("Transacción abortada por error:", e)
            return False

    def __del__(self):
        self.conn.close()         #No olvidar cerrar la conexion

if __name__ == "__main__":
    repo = RepositorioLibros()
    #Transacción exitosa
    def lote_exitoso(r: RepositorioLibros):
        b_ok1 = Libro("El Martín Fierro", "El gaucho Martin Fierro", 1872)
        r.add_libro(b_ok1)
        b_ok2 = Libro("El Principito", "Antoine de Saint-Exupéry", 1943)
        r.add_libro(b_ok2)
        b_ok3 = Libro("Cuentos de la selva", "Horacio Quiroga", 1918)
        r.add_libro(b_ok3)
    ok = repo.ejecutar_transaccion(lote_exitoso)
    print(f"Transacción exitosa (sin error): {ok}")

    print("Después de transacción exitosa:", [b.titulo for b in repo.list_libros()])
    todos=repo.list_libros()
    if todos:
        primero = todos[0]                #Actualizar el primer libro de la lista
        print(f"\nAntes de actualizar: {primero}")
        primero.anio += 10
        actualizado = repo.update_libro(primero)
        print(f"¿Actualización exitosa? {actualizado}")
        print("Después de actualizar:", repo.get_libro(primero.id))
    todos = repo.list_libros()
    if todos:
        ultimo = todos[-1]                  #Borrar el último de la lista
        borrado = repo.delete_libro(ultimo.id)
        print(f"\n¿Borrado de '{ultimo.titulo}' exitoso? {borrado}")
        print("Listado final tras borrado:", [b.titulo for b in repo.list_libros()])

    #Transacción con error forzado → rollback
    def lote_con_error(r: RepositorioLibros):
        # Forzamos excepción para probar rollback
        r.conn.execute("INSERT INTO libros (titulo, autor, anio) VALUES (?, ?, ?);",
                   ("Libro con error", "Autor", "texto"))  # anio debería ser entero

    ok_err = repo.ejecutar_transaccion(lote_con_error)
    print(f"\nTransacción con error forzado: {ok_err}")
    print("Después de transacción fallida:", [b.titulo for b in repo.list_libros()])  # lista sin Libro con error


