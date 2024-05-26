from django.test import TestCase
from app.models import Client, Pet, validate_pet, Vet, Speciality, Provider, validate_provider, validate_product, Medicine, validate_medicine
import datetime


class ClientModelTest(TestCase):
    def test_can_create_and_get_client(self):
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

    def test_valid_price(self):
        data = {
            "name": "ampicilina",
            "type": "antibiotico",
            "price": "100"
        }
        errors = validate_product(data)
        self.assertNotIn("price", errors)
    
    def test_price_equal_zero(self):
        data = {
            "name": "ampicilina",
            "type": "antibiotico",
            "price": "0"
        }
        errors = validate_product(data)
        self.assertIn("price", errors)
        self.assertEqual(errors["price"], "Por favor ingrese un precio mayor a cero")

    def test_price_missing(self):
        data = {
            "name": "ampicilina",
            "type": "antibiotico",
            "price": ""
        }
        errors = validate_product(data)
        self.assertIn("price", errors)
        self.assertEqual(errors["price"], "Por favor ingrese un precio")

class PetModelTest(TestCase):
    def test_can_create_and_get_pet(self):
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
        data = {
                "name": "gatito",
                "breed": "orange",
                "birthday": "2024-05-18",
            }
        result = validate_pet(data)
        self.assertDictEqual(result,{})
    def test_validate_pet_empty_data(self):
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
        date_now = datetime.date.today().strftime("%Y-%m-%d")
        data = {
            "name": "gatito",
                "breed": "orange",
                "birthday": date_now,
        }
        result = validate_pet(data)
        self.assertIn("Por favor ingrese una fecha de nacimiento valida y anterior a la de hoy",result.values())
    def test_validate_pet_invalid_birthday_date_later_than_today(self):
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
        return speciality in [choice.value for choice in Speciality]

class ProviderModelTest(TestCase):
    # TESTS para el alta de proveedores
    def test_can_create_and_get_provider(self):
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
        provider_data = {
                "name":"Demian",
                "email":"demian@utn.com",
                "address":""
            }

        result = validate_provider(provider_data)

        self.assertIn("Por favor ingrese una dirección", result.values())

    def test_validate_provider_with_everything_ok(self):
        provider_data = {
            "name":"Demian",
            "email":"demian@utn.com",
            "address":"Calle falsa 123"
        }

        result = validate_provider(provider_data)

        self.assertDictEqual(result, {})

    def test_validate_empty_data(self):
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
        data = {
                "name": "Meloxicam",
                "description": "Antiinflamatorio y analgesico",
                "dose": "41",
            }
        
        result = validate_medicine(data)
        self.assertIn("La dosis debe estar entre 1 y 10", result.values())
        
    def test_validate_medicine_decimal_dose(self):
        data = {
                "name": "Meloxicam",
                "description": "Antiinflamatorio y analgesico",
                "dose": "4.1",
            }
        
        result = validate_medicine(data)
        self.assertIn("La dosis debe ser un numero entero", result.values())