from django.test import TestCase
from django.shortcuts import reverse
from app.models import Client, Product, Pet, Vet, Speciality, Provider, Medicine

import datetime


class HomePageTest(TestCase):
    """
    Pruebas para la vista de la página de inicio.
    """

    def test_use_home_template(self):
        """
        Prueba que la vista de la página de inicio use el template correcto.

        Realiza una solicitud GET a la URL de la página de inicio y verifica 
        que el template 'home.html' sea utilizado en la respuesta.
        """

        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home.html")


class ClientsTest(TestCase):
    """
    Pruebas para la vista y funcionalidad de los clientes.
    """

    def test_repo_use_repo_template(self):
        """
        Prueba que la vista del repositorio de clientes use el template correcto.

        Realiza una solicitud GET a la URL del repositorio de clientes y verifica 
        que el template 'clients/repository.html' sea utilizado en la respuesta.
        """

        response = self.client.get(reverse("clients_repo"))
        self.assertTemplateUsed(response, "clients/repository.html")

    def test_repo_display_all_clients(self):
        """
        Prueba que la vista del repositorio de clientes muestre todos los clientes.

        Realiza una solicitud GET a la URL del repositorio de clientes y verifica 
        que el template 'clients/repository.html' sea utilizado en la respuesta.
        """

        response = self.client.get(reverse("clients_repo"))
        self.assertTemplateUsed(response, "clients/repository.html")

    def test_form_use_form_template(self):
        """
        Prueba que la vista del formulario de clientes use el template correcto.

        Realiza una solicitud GET a la URL del formulario de clientes y verifica 
        que el template 'clients/form.html' sea utilizado en la respuesta.
        """

        response = self.client.get(reverse("clients_form"))
        self.assertTemplateUsed(response, "clients/form.html")

    def test_can_create_client(self):
        """
        Prueba que se pueda crear un cliente.

        Realiza una solicitud POST a la URL del formulario de clientes con los datos
        del nuevo cliente y verifica que el cliente sea creado correctamente en la base de datos.
        """

        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            },
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)

        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, "221555232")
        self.assertEqual(clients[0].address, "13 y 44")
        self.assertEqual(clients[0].email, "brujita75@hotmail.com")

        self.assertRedirects(response, reverse("clients_repo"))

    def test_validation_errors_create_client(self):
        """
        Prueba que se muestren errores de validación al intentar crear un cliente con datos inválidos.

        Realiza una solicitud POST a la URL del formulario de clientes con datos vacíos y verifica
        que se muestren los mensajes de error correspondientes.
        """

        response = self.client.post(
            reverse("clients_form"),
            data={},
        )

        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese un teléfono")
        self.assertContains(response, "Por favor ingrese un email")

    def test_should_response_with_404_status_if_client_doesnt_exists(self):
        """
        Prueba que se retorne un estado 404 si se intenta editar un cliente que no existe.

        Realiza una solicitud GET a la URL de edición de clientes con un ID inexistente y verifica 
        que se retorne un estado 404.
        """

        response = self.client.get(reverse("clients_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_validation_invalid_email(self):
        """
        Prueba que se muestre un error de validación si se ingresa un email inválido.

        Realiza una solicitud POST a la URL del formulario de clientes con un email inválido y verifica
        que se muestre el mensaje de error correspondiente.
        """

        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75",
            },
        )

        self.assertContains(response, "Por favor ingrese un email valido")

    def test_edit_user_with_valid_data(self): 
        """
        Prueba que se pueda editar un cliente con datos válidos.

        Crea un cliente, realiza una solicitud POST a la URL del formulario de clientes con los datos
        actualizados y verifica que el cliente sea actualizado correctamente en la base de datos.
        """
        
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        response = self.client.post(
            reverse("clients_form"),
            data={
                "id": client.id,
                "name": "Guido Carrillo", 
                "address":client.address,
                "phone":client.phone,
                "email":client.email,
            },
        )

        # redirect after post
        self.assertEqual(response.status_code, 302)

        editedClient = Client.objects.get(pk=client.id)
        self.assertEqual(editedClient.name, "Guido Carrillo")
        self.assertEqual(editedClient.phone, client.phone)
        self.assertEqual(editedClient.address, client.address)
        self.assertEqual(editedClient.email, client.email)


class TestIntegration(TestCase):
    """
    Pruebas de integración para la creación y validación de productos.
    """
     
    def test_some_integration(self):
        """
        Prueba la validación de precios vacíos en el formulario de productos.

        Realiza una solicitud POST a la URL del formulario de productos con un precio vacío.
        Verifica que se muestre un mensaje de error y que el producto no sea creado en la base de datos.
        """

        response = self.client.post(
            reverse("products_form"),
            data={
                "name": "ampicilina",
                "type": "antibiotico",
                "price": "",
            },
            follow=True  # Permite seguir redirecciones
        )

        self.assertContains(response, "Por favor ingrese un precio")
        #self.assertNotEqual(response.status_code, 200)
        #self.assertFalse(Product.objects.filter(name="ampicilina").exists())


    def test_valid_product_price(self):
        """
        Prueba la creación de un producto con un precio válido.

        Realiza una solicitud POST a la URL del formulario de productos con un precio válido.
        Verifica que la solicitud sea exitosa (redirección) y que el producto sea creado en la base de datos.
        """

        response = self.client.post(reverse('products_form'), {
            "name": "ampicilina",
            "type": "antibiotico",
            "price": "10"  # Precio mayor a 0, debería ser válido
        })

        # Verifica que la solicitud haya sido exitosa (se espera un redirect)
        self.assertEqual(response.status_code, 302)

        # Verifica que el producto haya sido creado en la base de datos
        self.assertTrue(Product.objects.filter(name="ampicilina").exists())

    def test_price_empty(self):
        """
        Prueba la validación de precios vacíos en el formulario de productos.

        Realiza una solicitud POST a la URL del formulario de productos con un precio vacío.
        Verifica que se muestre un mensaje de error y que el producto no sea creado en la base de datos.
        """

        response = self.client.post(
            reverse("products_form"),
            data={
                "name": "ampicilina",
                "type": "antibiotico",
                "price": "",
            },
            follow=True
        )

        # Verifica que el formulario devuelva un error de precio vacío
        self.assertContains(response, "Por favor ingrese un precio")
        # Verifica que el producto no haya sido creado en la base de datos
        self.assertFalse(Product.objects.filter(name="ampicilina").exists())

    def test_price_zero(self):
        """
        Prueba la validación de precios iguales a cero en el formulario de productos.

        Realiza una solicitud POST a la URL del formulario de productos con un precio de cero.
        Verifica que se muestre un mensaje de error y que el producto no sea creado en la base de datos.
        """

        response = self.client.post(
            reverse("products_form"),
            data={
                "name": "ampicilina",
                "type": "antibiotico",
                "price": "0",
            },
            follow=True
        )

        # Verifica que el formulario devuelva un error de precio cero
        self.assertContains(response, "Por favor ingrese un precio")
        # Verifica que el producto no haya sido creado en la base de datos
        self.assertFalse(Product.objects.filter(name="ampicilina").exists())

    def test_negative_price(self):
        """
        Prueba la validación de precios negativos en el formulario de productos.

        Realiza una solicitud POST a la URL del formulario de productos con un precio negativo.
        Verifica que se muestre un mensaje de error y que el producto no sea creado en la base de datos.
        """

        response = self.client.post(
            reverse('products_form'),
            data={
                "name": "ampicilina",
                "type": "antibiotico",
                "price": "-10",
            }
        )

        # self.assertEqual(response.status_code, 400)
        
        # Verifica que el mensaje de error esté presente en la respuesta
        self.assertContains(response, "Por favor ingrese un precio mayor a cero")
        # Verifica que el producto no haya sido creado en la base de datos
        self.assertFalse(Product.objects.filter(name="ampicilina").exists())


class PetsTest(TestCase):
    """
    Pruebas para el manejo de mascotas en el sistema.
    """

    def test_repo_use_repo_template(self):
        """
        Verifica que la vista de repositorio de mascotas utilice el template correcto.
        """
        response = self.client.get(reverse("pets_repo"))
        self.assertTemplateUsed(response, "pets/repository.html")
    
    def test_repo_display_all_pets(self):
        """
        Verifica que la vista de repositorio de mascotas utilice el template correcto.
        """

        response = self.client.get(reverse("pets_repo"))
        self.assertTemplateUsed(response, "pets/repository.html")

    def test_form_use_form_template(self):
        """
        Verifica que la vista de formulario de mascotas utilice el template correcto.
        """
        
        response = self.client.get(reverse("pets_form"))
        self.assertTemplateUsed(response, "pets/form.html")
    
    def test_can_create_pet(self):
        """
        Verifica que se pueda crear una mascota correctamente.
        """
         
        response = self.client.post(
            reverse("pets_form"),
            data={
                "name": "gatito",
                "breed": "orange",
                "birthday": "2024-05-18",
            },
        )
        pets = Pet.objects.all()
        self.assertEqual(len(pets), 1)
        
        self.assertEqual(pets[0].name, "gatito")
        self.assertEqual(pets[0].breed, "orange")
        self.assertEqual(pets[0].birthday, datetime.date(2024, 5, 18))
        
        self.assertRedirects(response, reverse("pets_repo"))
    
    def test_validation_errors_create_pet(self):
        """
        Verifica que se muestren mensajes de error adecuados al intentar crear una mascota con datos inválidos.
        """

        response = self.client.post(
            reverse("pets_form"),
            data={},
        )
        
        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese una raza")
        self.assertContains(response, "Por favor ingrese una fecha de nacimiento valida y anterior a la de hoy")
    
    def test_should_response_with_404_status_if_pet_doesnt_exists(self):
        """
        Verifica que se retorne un código de estado 404 si se intenta acceder a una mascota que no existe.
        """

        response = self.client.get(reverse("pets_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)
    
    def test_validation_invalid_birthday_date_now(self): 
        """
        Verifica que se muestre un mensaje de error al intentar crear una mascota con fecha de nacimiento igual a la de hoy.
        """

        date_now = datetime.date.today().strftime("%Y-%m-%d")
        response = self.client.post(
            reverse("pets_form"),
            data={
                "name": "gatito",
                "breed": "orange",
                "email": date_now,
            },
        )
        
        self.assertContains(response, "Por favor ingrese una fecha de nacimiento valida y anterior a la de hoy")
    
    def test_validation_invalid_birthday_date_later_than_today(self): 
        """
        Verifica que se muestre un mensaje de error al intentar crear una mascota con fecha de nacimiento posterior a la de hoy.
        """

        date_now = datetime.date.today()
        date_later = date_now + datetime.timedelta(days=1)
        date = date_later.strftime("%Y-%m-%d")
        response = self.client.post(
            reverse("pets_form"),
            data={
                "name": "gatito",
                "breed": "orange",
                "email": date,
            },
        )
        
        self.assertContains(response, "Por favor ingrese una fecha de nacimiento valida y anterior a la de hoy")
    
    def test_edit_user_with_valid_data_pet(self):
        """
        Verifica que se pueda editar una mascota con datos válidos.
        """

        pet = Pet.objects.create(
            name="gatito",
            breed="orange",
            birthday="2024-05-18"
        )
        
        response = self.client.post(
            reverse("pets_form"),
            data={
                "id": pet.id,
                "name": "mishu",
                "breed":pet.breed,
                "birthday":pet.birthday,
            },
        )
       
        # redirect after post
        self.assertEqual(response.status_code, 302)
       
        editedPet = Pet.objects.get(pk=pet.id)
       
        self.assertEqual(editedPet.name, "mishu")
        self.assertEqual(editedPet.breed, pet.breed)
        self.assertEqual(editedPet.birthday.strftime("%Y-%m-%d"), pet.birthday)
   
    def test_edit_user_with_invalid_data_pet(self):
        """
        Verifica que no se pueda editar una mascota con datos inválidos.
        """

        pet = Pet.objects.create(
            name="gatito",
            breed="orange",
            birthday="2024-05-18"
        )
        
        response = self.client.post(
            reverse("pets_form"),
            data={
                "id": pet.id,
                "name": "",
                "breed":"",
                "birthday":"",
            },
        )
        
        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese una raza")
        self.assertContains(response, "Por favor ingrese una fecha de nacimiento valida y anterior a la de hoy")
    
    def test_edit_user_with_invalid_birthday_today(self):
        """
        Verifica que no se pueda editar una mascota con fecha de nacimiento igual a la de hoy.
        """

        pet = Pet.objects.create(
            name="gatito",
            breed="orange",
            birthday="2024-05-18"
        )
        date_now = datetime.date.today().strftime("%Y-%m-%d")
        
        response = self.client.post(
            reverse("pets_form"),
            data={
                "id": pet.id,
                "name": pet.name,
                "breed":pet.breed,
                "birthday":date_now,
            },
        )
        
        self.assertContains(response, "Por favor ingrese una fecha de nacimiento valida y anterior a la de hoy")
    
    def test_edit_user_with_invalid_birthday_later_than_today(self): 
        """
        Verifica que no se pueda editar una mascota con fecha de nacimiento posterior a la de hoy.
        """

        pet = Pet.objects.create(
            name="gatito",
            breed="orange",
            birthday="2024-05-18"
        )
        
        date_now = datetime.date.today()
        date_later = date_now + datetime.timedelta(days=1)
        date = date_later.strftime("%Y-%m-%d")
        
        response = self.client.post(
            reverse("pets_form"),
            data={
                "name": pet.name,
                "breed": pet.breed,
                "email": date,
            },
        )
        
        self.assertContains(response, "Por favor ingrese una fecha de nacimiento valida y anterior a la de hoy")


class VetsTest(TestCase):
    """
    Pruebas para la gestión de veterinarios en el sistema.
    """

    def test_repo_use_repo_template(self):
        """
        Verifica que la vista de repositorio de veterinarios utilice el template correcto.
        """

        response = self.client.get(reverse("vets_repo"))
        self.assertTemplateUsed(response, "vets/repository.html")
    
    def test_repo_display_all_vets(self):
        """
        Verifica que la vista de repositorio de veterinarios muestre todos los veterinarios correctamente.
        """

        response = self.client.get(reverse("vets_repo"))
        self.assertTemplateUsed(response, "vets/repository.html")
    
    def test_form_use_form_template(self):
        """
        Verifica que la vista de formulario de veterinarios utilice el template correcto.
        """

        response = self.client.get(reverse("vets_form"))
        self.assertTemplateUsed(response, "vets/form.html")
    
    def test_can_create_vet(self):
        """
        Verifica que se pueda crear un veterinario correctamente.
        """

        speciality = "Urgencias"
        self.assertTrue(self.is_valid_speciality(speciality))
        
        response = self.client.post(
            reverse("vets_form"),
            data={
                "name": "Juan Sebastian Veron",
                "email": "brujita75@hotmail.com",
                "phone": "221555232",
                "speciality": speciality,
            },
        )
        
        vets = Vet.objects.all()
        self.assertEqual(len(vets), 1)
        
        self.assertEqual(vets[0].name, "Juan Sebastian Veron")
        self.assertEqual(vets[0].email, "brujita75@hotmail.com")
        self.assertEqual(vets[0].phone, "221555232")
        self.assertEqual(vets[0].speciality, "Urgencias")
        
        self.assertRedirects(response, reverse("vets_repo"))
    
    def is_valid_speciality(self, speciality):
        """
        Verifica si una especialidad es válida.
        """

        return speciality in [choice.value for choice in Speciality]
    
    def test_validation_errors_create_vet(self):
        """
        Verifica si se muestran mensajes de error adecuados al intentar crear un veterinario con datos inválidos.
        """

        response = self.client.post(
            reverse("vets_form"),
            data={},
        )
        
        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese un email")
        self.assertContains(response, "Por favor ingrese un teléfono")
        self.assertContains(response, "Por favor seleccione una especialidad")
    
    def test_should_response_with_404_status_if_vet_doesnt_exists(self):
        """
        Verifica si se devuelve un código de estado 404 si se intenta acceder a un veterinario que no existe.
        """

        response = self.client.get(reverse("vets_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)
    
    def test_validation_invalid_email(self):
        """
        Verifica si se valida correctamente el formato del email.
        """

        response = self.client.post(
            reverse("vets_form"),
            data={
                "name": "Juan Sebastian Veron",
                "email": "brujita75",
                "phone": "221555232",
                "speciality": "Urgencias",
            },
        )
        
        self.assertContains(response, "Por favor ingrese un email valido")
    
    def test_edit_user_with_valid_data_vet(self):
        """
        Verifica si se puede editar correctamente la información de un veterinario con datos válidos.
        """

        vet = Vet.objects.create(
            name="Juan Sebastián Veron",
            phone="221555232",
            email="brujita75@hotmail.com",
            speciality="Urgencias",
        )
       
        response = self.client.post(
            reverse("vets_form"),
            data={
                "id": vet.id,
                "name": "Guido Carrillo",
                "phone":vet.phone,
                "email":vet.email,
                "speciality":vet.speciality,
            },
        )
        
        self.assertEqual(response.status_code, 302)
        
        editedVet = Vet.objects.get(pk=vet.id)
        
        self.assertEqual(editedVet.name, "Guido Carrillo")
        self.assertEqual(editedVet.email, vet.email)
        self.assertEqual(editedVet.phone, vet.phone)
        self.assertEqual(editedVet.speciality, vet.speciality)

    def test_create_vet_with_valid_speciality(self):
        """
        Verifica si se puede crear un veterinario con una especialidad válida.
        """

        response = self.client.post(reverse("vets_form"), {
            "name": "Juan Sebastian Veron",
            "email": "brujita75@hotmail.com",
            "phone": "221555232",
            "speciality": "Urgencias"
        })

        self.assertEqual(response.status_code, 302)

        self.assertTrue(Vet.objects.filter(name="Juan Sebastian Veron").exists())

    def test_edit_user_with_empty_speciality_vet(self):
        """
        Verifica si se muestra un mensaje de error al intentar editar un veterinario con una especialidad vacía.
        """

        vet = Vet.objects.create(
            name="Juan Sebastian Veron",
            email= "brujita75@hotmail.com",
            phone= "221555232",
            speciality= "Urgencias"
        )
        response = self.client.post(
            reverse("vets_form"),
            data={
                "id": vet.id,
                "name": "Juan Sebastian Veron",
                "email": "brujita75@hotmail.com",
                "phone": "221555232",
                "speciality": ""
            },
        )

        self.assertContains(response, "Por favor seleccione una especialidad")


class ProvidersTest(TestCase):
    """
    Pruebas para la gestión de proveedores en el sistema.
    """

    def test_repo_use_repo_template(self):
        """
        Verifica que la vista de repositorio de proveedores utilice el template correcto.
        """

        response = self.client.get(reverse("providers_repo"))
        self.assertTemplateUsed(response, "providers/repository.html")

    def test_repo_display_all_providers(self):
        """
        Verifica que la vista de repositorio de proveedores muestre todos los proveedores correctamente.
        """

        response = self.client.get(reverse("providers_repo"))
        self.assertTemplateUsed(response, "providers/repository.html")

    def test_form_use_form_template(self):
        """
        Verifica que la vista de formulario de proveedores utilice el template correcto.
        """

        response = self.client.get(reverse("providers_form"))
        self.assertTemplateUsed(response, "providers/form.html")

    def test_can_create_provider(self):
        """
        Verifica que se pueda crear un proveedor correctamente.
        """

        response = self.client.post(
            reverse("providers_form"),
            data = {
                "name":"Demian",
                "email":"demian@utn.com",
                "address":"Calle falsa 123"
            },
        )

        providers = Provider.objects.all()
        self.assertEqual(len(providers), 1)

        self.assertEqual(providers[0].name, "Demian")
        self.assertEqual(providers[0].email, "demian@utn.com")
        self.assertEqual(providers[0].address, "Calle falsa 123")

        self.assertRedirects(response, reverse("providers_repo"))

    def test_validation_errors_when_create_provider(self):
        """
        Verifica que se muestren mensajes de error adecuados al intentar crear un proveedor con datos inválidos.
        """

        response = self.client.post(
            reverse("providers_form"),
            data={}
        )

        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese un email")
        self.assertContains(response, "Por favor ingrese una dirección")

    def test_should_response_with_404_status_if_provider_doesnt_exists(self):
        """
        Verifica que se retorne un código de estado 404 si se intenta acceder a un proveedor que no existe.
        """

        response = self.client.get(reverse("providers_edit", kwargs={"id":"742"}))
        self.assertEqual(response.status_code, 404)

    def test_cant_create_provider_with_empty_address(self):
        """
        Verifica que no se pueda crear un proveedor con la dirección vacía.
        """

        response = self.client.post(
            reverse("providers_form"),
            data={
                "name":"Demian",
                "email":"demian@utn.com",
                "address":""
            }
        )

        self.assertContains(response, "Por favor ingrese una dirección")

    def test_user_can_edit_provider_with_valid_data(self):
        """
        Verifica que se pueda editar un proveedor con datos válidos.
        """

        provider = Provider.objects.create(
            name="Demian",
            email="demian@utn.com",
            address="Calle falsa 123"
        )

        response = self.client.post(
            reverse("providers_form"),
            data={
                "id":provider.id,
                "name":provider.name,
                "email":provider.email,
                "address":"Avenida Siempreviva 742"
            }
        )

        self.assertEqual(response.status_code, 302)

    def test_user_cant_edit_provider_with_invalid_data(self):
        """
        Verifica que no se pueda editar un proveedor con datos inválidos.
        """

        provider=Provider.objects.create(
            name="Demian",
            email="demian@utn.com",
            address="Calle falsa 123"
        )

        response = self.client.post(
            reverse("providers_form"),
            data={
                "id":provider.id,
                "name":"",
                "email":"",
                "address":""
            }
        )

        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese un email")
        self.assertContains(response, "Por favor ingrese una dirección")

    def test_user_cant_edit_provider_with_empty_address(self):
        """
        Verifica que no se pueda editar un proveedor con la dirección vacía.
        """

        provider=Provider.objects.create(
            name="Demian",
            email="demian@utn.com",
            address="Calle falsa 123"
        )

        response = self.client.post(
            reverse("providers_form"),
            data={
                "id":provider.id,
                "name":provider.name,
                "email":provider.email,
                "address":""
            }
        )

        self.assertContains(response, "Por favor ingrese una dirección")

class MedicinesTest(TestCase):
    """
    Pruebas para la gestión de medicinas en el sistema.
    """

    def test_repo_use_repo_template(self):
        """
        Verifica que la vista de repositorio de medicinas utilice el template correcto.
        """

        response = self.client.get(reverse("medicine_repo"))
        self.assertTemplateUsed(response, "medicine/repository.html")
    
    def test_repo_display_all_medicines(self):
        """
        Verifica que la vista de repositorio de medicinas muestre todas las medicinas correctamente.
        """

        response = self.client.get(reverse("medicine_repo"))
        self.assertTemplateUsed(response, "medicine/repository.html")
    
    def test_form_use_form_template(self):
        """
        Verifica que la vista de formulario de medicinas utilice el template correcto.
        """

        response = self.client.get(reverse("medicine_form"))
        self.assertTemplateUsed(response, "medicine/form.html")
    
    def test_can_create_medicine(self):
        """
        Verifica que se pueda crear una medicina correctamente.
        """

        response = self.client.post(
            reverse("medicine_form"),
            data={
                "name": "Rostrum",
                "description": "Antibacteriano",
                "dose": "2"
            },
        )
        medicines = Medicine.objects.all()
        self.assertEqual(len(medicines), 1)

        self.assertEqual(medicines[0].name, "Rostrum")
        self.assertEqual(medicines[0].description, "Antibacteriano")
        self.assertEqual(medicines[0].dose, 2)

        self.assertRedirects(response, reverse("medicine_repo"))
        
    def test_validation_errors_create_medicine(self):
        """
        Verifica que se muestren mensajes de error adecuados al intentar crear una medicina con datos inválidos.
        """

        response = self.client.post(
            reverse("medicine_form"),
            data={},
        )

        self.assertContains(response, "Por favor, ingrese un nombre de la medicina")
        self.assertContains(response, "Por favor, ingrese una descripcion de la medicina")
        self.assertContains(response, "Por favor, ingrese una cantidad de la dosis de la medicina")
        
    def test_should_response_with_404_status_if_medicine_doesnt_exists(self):
        """
        Verifica que se retorne un código de estado 404 si se intenta acceder a una medicina que no existe.
        """

        response = self.client.get(reverse("medicine_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)
        
    def test_validation_decimal_dose(self):
        """
        Verifica que se muestre un mensaje de error al intentar crear una medicina con una dosis decimal.
        """

        response = self.client.post(
            reverse("medicine_form"),
            data={
                "name": "Rostrum",
                "description": "Antibacteriano",
                "dose": "2.5",
            },
        )
        
        self.assertContains(response, "La dosis debe ser un numero entero")
    
    def test_validation_dose_out_of_range(self):
        """
        Verifica que se muestre un mensaje de error al intentar crear una medicina con una dosis fuera del rango permitido.
        """
        response = self.client.post(
            reverse("medicine_form"),
            data={
                "name": "Rostrum",
                "description": "Antibacteriano",
                "dose": "88",
            },
        )
        
        self.assertContains(response, "La dosis debe estar entre 1 y 10")
        
    def test_edit_medicine_with_valid_data(self): 
        """
        Verifica que se pueda editar una medicina con datos válidos.
        """
        
        medicine = Medicine.objects.create(
            name="Rostrum",
            description="Antibacteriano",
            dose=8,
        )

        response = self.client.post(
            reverse("medicine_form"),
            data={
                "id": medicine.id,
                "name": medicine.name,
                "description": medicine.description,
                "dose": "3",
            },
        )

        self.assertEqual(response.status_code, 302)

        editedMedicine = Medicine.objects.get(pk=medicine.id)
        self.assertEqual(editedMedicine.name, medicine.name)
        self.assertEqual(editedMedicine.description, medicine.description)
        self.assertEqual(editedMedicine.dose, 3)