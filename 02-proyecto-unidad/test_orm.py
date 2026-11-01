import tempfile
import unittest
from pathlib import Path
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from orm import Base, Cliente, conectar, alta, listar, resumen_sql

class Pruebas(unittest.TestCase):
    def test_persistencia_y_rollback(self):
        with tempfile.TemporaryDirectory() as carpeta:
            engine=conectar(Path(carpeta)/'prueba.sqlite')
            Base.metadata.create_all(engine)
            alta(engine,'Empresa ficticia','demo@example.test')
            self.assertEqual(listar(engine)[0][3],1)
            with self.assertRaises(IntegrityError):
                alta(engine,'Duplicado','demo@example.test')
            self.assertEqual(len(listar(engine)),1)
            with Session(engine) as s, s.begin():
                s.get(Cliente,1).estado='activo'
            self.assertEqual(resumen_sql(engine),[('activo',1)])
            engine.dispose()
if __name__=='__main__': unittest.main()
