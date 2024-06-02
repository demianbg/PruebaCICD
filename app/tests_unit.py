from django.test import TestCase
from app.models import Client, Pet, validate_pet, Vet, Speciality, validate_vet, Provider, validate_provider, validate_product, Medicine, validate_medicine, Product
import datetime


class ClientModelTest(TestCase):
    """
    Pruebas para la gestión de clientes en el sistema.
    """

    def test_can_create_and_get_client(self):
        """
        Verifica que se pueda crear y obtener un cliente correctamente.
        """

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
        """
        Verifica que se pueda actualizar un cliente correctamente.
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
        Verifica que al intentar actualizar un cliente con datos incorrectos, los datos anteriores se mantengan.
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
    """
    Pruebas para la validación de productos.
    """

    def test_valid_price(self):
        """
        Verifica que un precio válido no genere errores.
        """

        data = {
            "name": "ampicilina",
            "type": "antibiotico",
            "price": "100"
        }
        errors = validate_product(data)
        self.assertNotIn("price", errors)
    
    def test_price_equal_zero(self):
        """
        Verifica que un precio igual a cero genere un error adecuado.
        """

        data = {
            "name": "ampicilina",
            "type": "antibiotico",
            "price": "0"
        }
        errors = validate_product(data)
        self.assertIn("price", errors)
        self.assertEqual(errors["price"], "Por favor ingrese un precio mayor a cero")

    def test_price_missing(self):
        """
        Verifica que un precio faltante genere un error adecuado.
        """

        data = {
            "name": "ampicilina",
            "type": "antibiotico",
            "price": ""
        }
        errors = validate_product(data)
        self.assertIn("price", errors)
        self.assertEqual(errors["price"], "Por favor ingrese un precio")
    
    def test_negative_price(self):
        """
        Verifica que un precio negativo genere un error adecuado.
        """

        data = {
            "name": "ampicilina",
            "type": "antibiotico",
            "price": "-10"
        }
        errors = validate_product(data)
        self.assertIn("price", errors)
        self.assertEqual(errors["price"], "Por favor ingrese un precio mayor a cero")

    def test_can_update_valid_price(self):
        """
        Verifica que se pueda actualizar un producto con datos válidos.
        """

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
        """
        Verifica que al intentar actualizar un producto con datos incorrectos, los datos anteriores se mantengan.
        """

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
        """
        Verifica que al intentar actualizar un producto con un precio incorrecto, se genere un error adecuado.
        """

        data = {
                "name": "ampicilina",
                "type": "antibiotico",
                "price": "-10",
            }
        
        result = validate_product(data)
        self.assertIn("Por favor ingrese un precio mayor a cero", result.values())

    def test_validate_product_all_ok(self):
        """
        Verifica que la validación de un producto con datos válidos no genere errores.
        """

        data = {
                "name": "ampicilina",
                "type": "antibiotico",
                "price": "10",
            }
        
        result = validate_product(data)
        
        self.assertDictEqual(result,{})

    def test_validate_product_empty_data(self):
        """
        Verifica que la validación de un producto con datos faltantes genere errores adecuados.
        """

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
    """
    Pruebas para la gestión de mascotas en el sistema.
    """

    def test_can_create_and_get_pet(self):
        """
        Verifica que se pueda crear y obtener una mascota correctamente.
        """

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
        """
        Verifica que se pueda actualizar una mascota correctamente.
        """

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
        """
        Verifica que al intentar actualizar una mascota con datos incorrectos, los datos anteriores se mantengan.
        """

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
        """
        Verifica que los datos válidos pasen la validación sin errores.
        """

        data = {
                "name": "gatito",
                "breed": "orange",
                "birthday": "2024-05-18",
            }
        
        result = validate_pet(data)
        
        self.assertDictEqual(result,{})
    
    def test_validate_pet_empty_data(self):
        """
        Verifica que los datos vacíos generen los errores de validación apropiados.
        """

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
        """
        Verifica que una fecha de nacimiento igual a la fecha actual genere un error de validación.
        """

        date_now = datetime.date.today().strftime("%Y-%m-%d")
        data = {
            "name": "gatito",
                "breed": "orange",
                "birthday": date_now,
        }
        
        result = validate_pet(data)
        
        self.assertIn("Por favor ingrese una fecha de nacimiento valida y anterior a la de hoy",result.values())
    
    def test_validate_pet_invalid_birthday_date_later_than_today(self):
        """
        Verifica que una fecha de nacimiento posterior a la fecha actual genere un error de validación.
        """

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
    """
    Pruebas para la gestión de veterinarios en el sistema.
    """

    def test_can_create_and_get_vet(self):
        """
        Verifica que se pueda crear y obtener un veterinario correctamente.
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
        Verifica que se pueda actualizar un veterinario correctamente.
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
        Verifica que al intentar actualizar un veterinario con datos incorrectos, los datos anteriores se mantengan.
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
        Verifica que la especialidad proporcionada sea válida.
        """

        return speciality in [choice.value for choice in Speciality]
    
    def test_empty_speciality_error(self):
        """
        Verifica que al intentar crear un veterinario con una especialidad vacía, se genere un error de validación.
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
    """
    Pruebas para la gestión de proveedores en el sistema.
    """

    def test_can_create_and_get_provider(self):
        """
        Verifica que se pueda crear y obtener un proveedor correctamente.
        """

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
        """
        Verifica que se genere un error de validación al intentar crear un proveedor con una dirección vacía.
        """

        provider_data = {
                "name":"Demian",
                "email":"demian@utn.com",
                "address":""
            }

        result = validate_provider(provider_data)

        self.assertIn("Por favor ingrese una dirección", result.values())

    def test_validate_provider_with_everything_ok(self):
        """
        Verifica que un proveedor con datos correctos pase la validación.
        """

        provider_data = {
            "name":"Demian",
            "email":"demian@utn.com",
            "address":"Calle falsa 123"
        }

        result = validate_provider(provider_data)

        self.assertDictEqual(result, {})

    def test_validate_empty_data(self):
        """
        Verifica que se generen errores de validación al intentar crear un proveedor con todos los datos vacíos.
        """

        provider_data = {
            "name":"",
            "email":"",
            "address":""
        }

        result = validate_provider(provider_data)
        self.assertIn("Por favor ingrese un nombre", result.values())
        self.assertIn("Por favor ingrese un email", result.values())
        self.assertIn("Por favor ingrese una dirección", result.values())

    def test_can_update_provider(self):
        """
        Verifica que se pueda actualizar un proveedor correctamente.
        """

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
        """
        Verifica que al intentar actualizar un proveedor con una dirección vacía, los datos anteriores se mantengan.
        """

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
    """
    Pruebas para la gestión de medicamentos en el sistema.
    """

    def test_can_create_and_get_medicine(self):
        """
        Verifica que se pueda crear y obtener un medicamento correctamente.
        """

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
        """
        Verifica que se pueda actualizar un medicamento correctamente.
        """

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
        """
        Verifica que al intentar actualizar un medicamento con datos incorrectos, los datos anteriores se mantengan.
        """

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
        """
        Verifica que se genere un error de validación al ingresar una dosis fuera del rango permitido.
        """

        data = {
                "name": "Meloxicam",
                "description": "Antiinflamatorio y analgesico",
                "dose": "41",
            }
        
        result = validate_medicine(data)
        self.assertIn("La dosis debe estar entre 1 y 10", result.values())
        
    def test_validate_medicine_decimal_dose(self):
        """
        Verifica que se genere un error de validación al ingresar una dosis con decimales.
        """
        
        data = {
                "name": "Meloxicam",
                "description": "Antiinflamatorio y analgesico",
                "dose": "4.1",
            }
        
        result = validate_medicine(data)
        self.assertIn("La dosis debe ser un numero entero", result.values())