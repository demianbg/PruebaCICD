from django.test import TestCase
from app.models import Client, Pet, validate_pet, Vet, Speciality, validate_vet, Provider, validate_provider, validate_product, Medicine, validate_medicine, Product
import datetime


class ClientModelTest(TestCase):
    def test_can_create_and_get_client(self):
        """Prueba que se pueda crear y obtener un cliente correctamente."""
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)

        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, "221555232")
        self.assertEqual(clients[0].address, "13 y 44")
        self.assertEqual(clients[0].email, "brujita75@hotmail.com")

    def test_can_update_client(self):
        """Prueba que se pueda actualizar la información de un cliente correctamente."""
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "221555232")

        client.update_client({
            "name": "Juan Sebastian Veron",
            "phone": "221555233",
            "address": "13 y 44",
            "email": "brujita75@hotmail.com",
            })

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "221555233")

    def test_update_client_with_error(self):
        """
    Prueba que el cliente no se actualice si se proporciona un número de teléfono vacío.

    Se crea un cliente con un número de teléfono válido. Luego se intenta
    actualizar el cliente con un número de teléfono vacío. Se verifica que
    el número de teléfono del cliente no cambie después de intentar la actualización.
        """
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "221555232")

        client.update_client({"phone": ""})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "221555232")


class TestValidateProduct(TestCase):
    """Pruebas para validar los productos."""

    def test_valid_price(self):
        """Prueba que verifica si el precio es válido."""
        data = {
            "name": "ampicilina",
            "type": "antibiotico",
            "price": "100"
        }
        errors = validate_product(data)
        self.assertNotIn("price", errors)
    
    def test_price_equal_zero(self):
        """Prueba que verifica si el precio es igual a cero."""
        data = {
            "name": "ampicilina",
            "type": "antibiotico",
            "price": "0"
        }
        errors = validate_product(data)
        self.assertIn("price", errors)
        self.assertEqual(errors["price"], "Por favor ingrese un precio mayor a cero")

    def test_price_missing(self):
        """Prueba que verifica si falta el precio."""
        data = {
            "name": "ampicilina",
            "type": "antibiotico",
            "price": ""
        }
        errors = validate_product(data)
        self.assertIn("price", errors)
        self.assertEqual(errors["price"], "Por favor ingrese un precio")
    
    def test_negative_price(self):
        """Prueba que verifica si se proporciona un precio negativo."""
        data = {
            "name": "ampicilina",
            "type": "antibiotico",
            "price": "-10"
        }
        errors = validate_product(data)
        self.assertIn("price", errors)
        self.assertEqual(errors["price"], "Por favor ingrese un precio mayor a cero")

    def test_can_update_valid_price(self):
        """Prueba que verifica si se puede actualizar un producto con un precio válido."""
        Product.save_product(
            {
                "name": "ampicilina",
                "type": "antibiotico",
                "price": "10",
            }
        )
        product = Product.objects.get(pk=1)
        self.assertEqual(product.name, "ampicilina")
        product.update_product({
            "name": "ampicilina",
            "type": "antibiotico",
            "birthday": "10",
        })
        product_updated = Product.objects.get(pk=1)
        self.assertEqual(product_updated.name, "ampicilina")

    def test_update_product_with_error(self):
        """Prueba que verifica si ocurre un error al intentar actualizar un producto con datos incorrectos.""" 
        Product.save_product(
            {
                "name": "ampicilina",
                "type": "antibiotico",
                "price": "10",
            }
        )
        product = Product.objects.get(pk=1)
        self.assertEqual(product.name, "ampicilina")
        product.update_product({"name": ""})
        product_updated = Product.objects.get(pk=1)
        self.assertEqual(product_updated.name, "ampicilina")

    def test_update_product_with_error_price(self):
        """Prueba que verifica si se produce un error al intentar actualizar un producto con un precio negativo.""" 
        data = {
                "name": "ampicilina",
                "type": "antibiotico",
                "price": "-10",
            }
        
        result = validate_product(data)
        self.assertIn("Por favor ingrese un precio mayor a cero", result.values())

    def test_validate_product_all_ok(self):
        """Prueba que verifica si la validación de datos del producto es exitosa cuando se proporcionan todos los datos necesarios."""
        data = {
                "name": "ampicilina",
                "type": "antibiotico",
                "price": "10",
            }
        result = validate_product(data)
        self.assertDictEqual(result,{})

    def test_validate_product_empty_data(self):
        """Prueba que verifica si se producen errores cuando no se proporcionan datos para el producto."""
        data = {
                "name": "",
                "type": "",
                "price": "",
            }
        result = validate_product(data)
        self.assertIn("Por favor ingrese un nombre",result.values())
        self.assertIn("Por favor ingrese un tipo",result.values())
        self.assertIn("Por favor ingrese un precio",result.values())

class PetModelTest(TestCase):
    def test_can_create_and_get_pet(self):
        """Prueba que verifica si se puede crear y obtener una mascota correctamente."""
        Pet.save_pet(
            {
                "name": "gatito",
                "breed": "orange",
                "birthday": "2024-05-18",
            }
        )
        pets = Pet.objects.all()
        self.assertEqual(len(pets), 1)
    def test_can_update_pet(self):
        """Prueba que verifica si se puede actualizar una mascota correctamente."""
        Pet.save_pet(
            {
                "name": "gatito",
                "breed": "orange",
                "birthday": "2024-05-18",
            }
        )
        pet = Pet.objects.get(pk=1)
        self.assertEqual(pet.name, "gatito")
        pet.update_pet({
            "name": "gato",
            "breed": "orange",
            "birthday": "2024-05-18",
        })
        pet_updated = Pet.objects.get(pk=1)
        self.assertEqual(pet_updated.name, "gato")
    def test_update_pet_with_error(self):
        """Prueba que verifica si se produce un error al intentar actualizar una mascota con un campo de nombre vacío.""" 
        Pet.save_pet(
            {
                "name": "gatito",
                "breed": "orange",
                "birthday": "2024-05-18",
            }
        )
        pet = Pet.objects.get(pk=1)
        self.assertEqual(pet.name, "gatito")
        pet.update_pet({"name": ""})
        pet_updated = Pet.objects.get(pk=1)
        self.assertEqual(pet_updated.name, "gatito")
    def test_validate_pet_all_ok(self):
        """Prueba que valida si todos los campos de una mascota están llenos correctamente."""
        data = {
                "name": "gatito",
                "breed": "orange",
                "birthday": "2024-05-18",
            }
        result = validate_pet(data)
        self.assertDictEqual(result,{})
    def test_validate_pet_empty_data(self):
        """Prueba que verifica si se detectan errores cuando todos los campos de una mascota están vacíos."""
        data = {
                "name": "",
                "breed": "",
                "birthday": "",
            }
        result = validate_pet(data)
        self.assertIn("Por favor ingrese una fecha de nacimiento valida y anterior a la de hoy",result.values())
        self.assertIn("Por favor ingrese un nombre",result.values())
        self.assertIn("Por favor ingrese una raza",result.values())
    def test_validate_pet_invalid_birthday_today(self):
        """Prueba que verifica si se detecta un error cuando la fecha de nacimiento de la mascota es la misma que la fecha actual."""
        date_now = datetime.date.today().strftime("%Y-%m-%d")
        data = {
            "name": "gatito",
                "breed": "orange",
                "birthday": date_now,
        }
        result = validate_pet(data)
        self.assertIn("Por favor ingrese una fecha de nacimiento valida y anterior a la de hoy",result.values())
    def test_validate_pet_invalid_birthday_date_later_than_today(self):
        """Prueba que verifica si se detecta un error cuando la fecha de nacimiento de la mascota es posterior a la fecha actual."""
        date_now = datetime.date.today()
        date_later = date_now + datetime.timedelta(days=1)
        date = date_later.strftime("%Y-%m-%d")
        data = {
            "name": "gatito",
            "breed": "orange",
            "birthday": date,
        }
        result = validate_pet(data)
        self.assertIn("Por favor ingrese una fecha de nacimiento valida y anterior a la de hoy",result.values())


class VetModelTest(TestCase):
    def test_can_create_and_get_vet(self):
        """
        Prueba que verifica si se puede crear y obtener un veterinario correctamente.

        Se asegura de que el veterinario se crea correctamente y que todos los campos tienen los valores esperados.
        """
        speciality = "Urgencias"
        self.assertTrue(self.is_valid_speciality(speciality))
        
        Vet.save_vet(
            {
                "name": "Juan Sebastian Veron",
                "email": "brujita75@hotmail.com",
                "phone": "221555232",
                "speciality": speciality,
            }
        )
        
        vets = Vet.objects.all()
        self.assertEqual(len(vets), 1)
        
        self.assertEqual(vets[0].name, "Juan Sebastian Veron")
        self.assertEqual(vets[0].email, "brujita75@hotmail.com")
        self.assertEqual(vets[0].phone, "221555232")
        self.assertEqual(vets[0].speciality, "Urgencias")
    
    def test_can_update_vet(self):
        """
    Prueba que verifica si se puede actualizar un veterinario correctamente.

    Se asegura de que el veterinario se crea inicialmente con un número de teléfono,
    luego se actualiza el número de teléfono y se verifica que la actualización sea exitosa.
        """
        Vet.save_vet(
            {
                "name": "Juan Sebastian Veron",
                "email": "brujita75@hotmail.com",
                "phone": "221555232",
                "speciality": "Urgencias",
            }
        )
        
        vet = Vet.objects.get(pk=1)
        self.assertEqual(vet.phone, "221555232")
        
        vet.update_vet({
            "name": "Juan Sebastian Veron",
            "email": "brujita75@hotmail.com",
            "phone": "221555233",
            "speciality": "Urgencias",
            })
        
        vet_updated = Vet.objects.get(pk=1)
        
        self.assertEqual(vet_updated.phone, "221555233")
    
    def test_update_vet_with_error(self):
        """
    Prueba que verifica que un veterinario no se actualice si se proporcionan datos inválidos.

    Se asegura de que el veterinario se crea inicialmente con un número de teléfono válido.
    Luego, se intenta actualizar el veterinario con un número de teléfono vacío y se verifica
    que el número de teléfono no se haya actualizado.
        """
        Vet.save_vet(
            {
                "name": "Juan Sebastian Veron",
                "email": "brujita75@hotmail.com",
                "phone": "221555232",
                "speciality": "Urgencias",
            }
        )
        
        vet = Vet.objects.get(pk=1)
        self.assertEqual(vet.phone, "221555232")
        
        vet.update_vet({"phone": ""})
        vet_updated = Vet.objects.get(pk=1)
        
        self.assertEqual(vet_updated.phone, "221555232")

    def is_valid_speciality(self, speciality):
        """
        Verifica si una especialidad dada es válida
        """
        return speciality in [choice.value for choice in Speciality]
    
    def test_empty_speciality_error(self):
        """
    Prueba que verifica si se produce un error al intentar crear un veterinario con una especialidad vacía.

    Se crea un diccionario de datos que representa un veterinario con una especialidad vacía.
    Luego, se valida el diccionario de datos y se verifica que se encuentre el mensaje de error
    correspondiente en los errores generados.
        """
        data = {
            "name": "Juan Sebastian Veron",
            "email": "brujita75@hotmail.com",
            "phone": "221555232",
            "speciality": "",
        }

        errors = validate_vet(data)

        self.assertIn("Por favor seleccione una especialidad", errors.values())

class ProviderModelTest(TestCase):
    # TESTS para el alta de proveedores
    def test_can_create_and_get_provider(self):
        """Prueba que verifica si se puede crear y obtener un proveedor."""
        Provider.save_provider(
            {
                "name":"Demian",
                "email":"demian@utn.com",
                "address":"Calle falsa 123"
            }
        )

        providers = Provider.objects.all()
        self.assertEqual(len(providers), 1)

    def test_validate_empty_address_when_create_provider(self):
        """Prueba que valida una dirección vacía al crear un proveedor."""
        provider_data = {
                "name":"Demian",
                "email":"demian@utn.com",
                "address":""
            }

        result = validate_provider(provider_data)

        self.assertIn("Por favor ingrese una dirección", result.values())

    def test_validate_provider_with_everything_ok(self):
        """Prueba la validación de un proveedor con todos los campos válidos."""
        provider_data = {
            "name":"Demian",
            "email":"demian@utn.com",
            "address":"Calle falsa 123"
        }

        result = validate_provider(provider_data)

        self.assertDictEqual(result, {})

    def test_validate_empty_data(self):
        """Prueba la validación de un proveedor con datos vacíos."""
        provider_data = {
            "name":"",
            "email":"",
            "address":""
        }

        result = validate_provider(provider_data)
        self.assertIn("Por favor ingrese un nombre", result.values())
        self.assertIn("Por favor ingrese un email", result.values())
        self.assertIn("Por favor ingrese una dirección", result.values())

    # TESTS para modificar proveedores
    def test_can_update_provider(self):
        """Prueba que verifica si se puede actualizar un proveedor."""
        Provider.save_provider(
            {
                "name":"Demian",
                "email":"demian@utn.com",
                "address":"Calle falsa 123"
            }
        )

        provider = Provider.objects.get(pk=1)

        self.assertEqual(provider.name, "Demian")

        provider.update_provider({
            "name":provider.name,
            "email":provider.email,
            "address":"Avenida Siempreviva 742"
        })

        updated_provider = Provider.objects.get(pk=1)

        self.assertEqual(updated_provider.address, "Avenida Siempreviva 742")

    def test_cant_update_with_empty_address(self):
        """Prueba que verifica que no se puede actualizar con una dirección vacía."""
        Provider.save_provider(
            {
                "name":"Demian",
                "email":"demian@utn.com",
                "address":"Calle falsa 123"
            }
        )

        provider = Provider.objects.get(pk=1)

        provider.update_provider({
            "name":provider.name,
            "email":provider.email,
            "address":""
        })

        updated_provider = Provider.objects.get(pk=1)

        self.assertEqual(updated_provider.address, "Calle falsa 123")
        
class MedicineModelTest(TestCase):
    def test_can_create_and_get_medicine(self):
        """Prueba que verifica si se puede crear y obtener un medicamento."""
        Medicine.save_medicine(
            {
                "name": "Meloxicam",
                "description": "Antiinflamatorio y analgesico",
                "dose": "2",
            }
        )
        medicines = Medicine.objects.all()
        self.assertEqual(len(medicines), 1)
        
        self.assertEqual(medicines[0].name, "Meloxicam")
        self.assertEqual(medicines[0].description, "Antiinflamatorio y analgesico")
        self.assertEqual(medicines[0].dose, 2)
        
    def test_can_update_medicine(self):
        """Prueba que verifica si se puede actualizar un medicamento."""
        Medicine.save_medicine(
            {
                "name": "Meloxicam",
                "description": "Antiinflamatorio y analgesico",
                "dose": "2",
            }
        )
        medicine = Medicine.objects.get(pk=1)
        
        self.assertEqual(medicine.dose, 2)
        
        medicine.update_medicine(
            {
            "name": "Meloxicam",
                "description": "Antiinflamatorio y analgesico",
                "dose": "8",
            }
        )
        
        medicine_updated = Medicine.objects.get(pk=1)
        
        self.assertEqual(medicine_updated.dose, 8)
        
    def test_update_medicine_with_error(self):
        """Prueba que verifica que no se puede actualizar un medicamento con un nombre vacío."""
        Medicine.save_medicine(
            {
                "name": "Meloxicam",
                "description": "Antiinflamatorio y analgesico",
                "dose": "2",
            }
        )
        medicine = Medicine.objects.get(pk=1)
        
        self.assertEqual(medicine.name, "Meloxicam")
        
        medicine.update_medicine({"name": ""})
        
        medicine_updated = Medicine.objects.get(pk=1)
        
        self.assertEqual(medicine_updated.name, "Meloxicam")
    
    def test_validate_medicine_invalid_dose(self):
        """Prueba la validación de un medicamento con dosis inválida."""
        data = {
                "name": "Meloxicam",
                "description": "Antiinflamatorio y analgesico",
                "dose": "41",
            }
        
        result = validate_medicine(data)
        self.assertIn("La dosis debe estar entre 1 y 10", result.values())
        
    def test_validate_medicine_decimal_dose(self):
        """Prueba la validación de un medicamento con dosis decimal."""
        data = {
                "name": "Meloxicam",
                "description": "Antiinflamatorio y analgesico",
                "dose": "4.1",
            }
        
        result = validate_medicine(data)
        self.assertIn("La dosis debe ser un numero entero", result.values())