import unittest
from dataclasses import dataclass

from peewee import *

from src.utils.database import class_to_peewee_model, db


class TestDataclassToPeeweeModel(unittest.TestCase):

    def setUp(self):
        # Use an in-memory SQLite database for testing
        db.init(':memory:')
        db.connect()

    def tearDown(self):
        db.close()

    def test_basic_dataclass_conversion(self):

        @dataclass
        class Person:
            name: str
            age: int
            is_active: bool

        PersonModel = class_to_peewee_model(Person)

        # Check if the model was created correctly
        self.assertTrue(issubclass(PersonModel, Model))
        self.assertEqual(PersonModel._meta.table_name, 'person')
        self.assertIsInstance(PersonModel.name, CharField)
        self.assertIsInstance(PersonModel.age, IntegerField)
        self.assertIsInstance(PersonModel.is_active, BooleanField)

    def test_foreign_key_relationship(self):

        @dataclass
        class Department:
            name: str

        @dataclass
        class Employee:
            name: str
            department: Department

        DepartmentModel = class_to_peewee_model(Department)
        EmployeeModel = class_to_peewee_model(Employee)

        # Check if the models were created correctly
        self.assertTrue(issubclass(DepartmentModel, Model))
        self.assertTrue(issubclass(EmployeeModel, Model))
        self.assertIsInstance(EmployeeModel.department, ForeignKeyField)
        self.assertEqual(EmployeeModel.department.rel_model, DepartmentModel)

    def test_model_creation_and_querying(self):

        @dataclass
        class Department:
            name: str

        @dataclass
        class Employee:
            name: str
            department: Department

        DepartmentModel = class_to_peewee_model(Department)
        EmployeeModel = class_to_peewee_model(Employee)

        # Create tables
        db.create_tables([DepartmentModel, EmployeeModel])

        # Create test data
        dept = DepartmentModel.create(name="Engineering")
        emp = EmployeeModel.create(name="Alice", department=dept)

        # Test querying
        retrieved_emp = EmployeeModel.get(EmployeeModel.name == "Alice")
        self.assertEqual(retrieved_emp.name, "Alice")
        self.assertEqual(retrieved_emp.department.name, "Engineering")

    def test_complex_datatype_defaults_to_textfield(self):

        @dataclass
        class ComplexData:
            data: dict

        ComplexModel = class_to_peewee_model(ComplexData)
        self.assertIsInstance(ComplexModel.data, TextField)


if __name__ == '__main__':
    unittest.main()
