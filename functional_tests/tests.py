import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright, expect, Browser

from django.urls import reverse

from app.models import Client, Pet, Vet, Speciality, Provider, Medicine, Product

import datetime

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
playwright = sync_playwright().start()
headless = os.environ.get("HEADLESS", 1) == 1
slow_mo = os.environ.get("SLOW_MO", 0)


class PlaywrightTestCase(StaticLiveServerTestCase):
    """
    Clase base para pruebas de integración utilizando Playwright y StaticLiveServerTestCase de Django.
    """

    @classmethod
    def setUpClass(cls):
        """
        Configuración inicial de la clase de prueba. Se ejecuta una vez antes de todas las pruebas.
        Inicializa el navegador Playwright en modo headless o visible según la configuración.
        """

        super().setUpClass()
        cls.browser: Browser = playwright.chromium.launch(
            headless=headless, slow_mo=int(slow_mo)
        )

    @classmethod
    def tearDownClass(cls):
        """
        Limpieza final de la clase de prueba. Se ejecuta una vez después de todas las pruebas.
        Cierra el navegador Playwright.
        """

        super().tearDownClass()
        cls.browser.close()

    def setUp(self):
        """
        Configuración inicial antes de cada prueba individual.
        Abre una nueva página del navegador para cada prueba.
        """

        super().setUp()
        self.page = self.browser.new_page()

    def tearDown(self):
        """
        Limpieza después de cada prueba individual.
        Cierra la página del navegador utilizada en la prueba.
        """

        super().tearDown()
        self.page.close()


class HomeTestCase(PlaywrightTestCase):
    """
    Pruebas para la página de inicio del sistema.
    """

    def test_should_have_navbar_with_links(self):
        """
        Verifica que la barra de navegación tenga los enlaces correctos.
        """

        self.page.goto(self.live_server_url)

        navbar_home_link = self.page.get_by_test_id("navbar-Home")

        expect(navbar_home_link).to_be_visible()
        expect(navbar_home_link).to_have_text("Home")
        expect(navbar_home_link).to_have_attribute("href", reverse("home"))

        navbar_clients_link = self.page.get_by_test_id("navbar-Clientes")

        expect(navbar_clients_link).to_be_visible()
        expect(navbar_clients_link).to_have_text("Clientes")
        expect(navbar_clients_link).to_have_attribute("href", reverse("clients_repo"))

    def test_should_have_home_cards_with_links(self): 
        """
        Verifica que las tarjetas de la página de inicio tengan los enlaces correctos.
        """

        self.page.goto(self.live_server_url)

        home_clients_link = self.page.get_by_test_id("home-Clientes")

        expect(home_clients_link).to_be_visible()
        expect(home_clients_link).to_have_text("Clientes")
        expect(home_clients_link).to_have_attribute("href", reverse("clients_repo"))


class ClientsRepoTestCase(PlaywrightTestCase):
    """
    Pruebas para la vista del repositorio de clientes.
    """

    def test_should_show_message_if_table_is_empty(self):
        """
        Verifica que se muestre un mensaje si la tabla está vacía.
        """

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("No existen clientes")).to_be_visible()

    def test_should_show_clients_data(self):
        """
        Verifica que se muestren los datos de los clientes correctamente.
        """
         
        Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        Client.objects.create(
            name="Guido Carrillo",
            address="1 y 57",
            phone="221232555",
            email="goleador@gmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("No existen clientes")).not_to_be_visible()

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("13 y 44")).to_be_visible()
        expect(self.page.get_by_text("221555232")).to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("1 y 57")).to_be_visible()
        expect(self.page.get_by_text("221232555")).to_be_visible()
        expect(self.page.get_by_text("goleador@gmail.com")).to_be_visible()

    def test_should_show_add_client_action(self):
        """
        Verifica que se muestre la acción de agregar cliente.
        """

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        add_client_action = self.page.get_by_role(
            "link", name="Nuevo cliente", exact=False
        )
        expect(add_client_action).to_have_attribute("href", reverse("clients_form"))

    def test_should_show_client_edit_action(self):
        """
        Verifica que se muestre la acción de editar cliente.
        """

        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("clients_edit", kwargs={"id": client.id})
        )

    def test_should_show_client_delete_action(self):
        """
        Verifica que se muestre la acción de eliminar cliente.
        """

        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        edit_form = self.page.get_by_role(
            "form", name="Formulario de eliminación de cliente"
        )
        client_id_input = edit_form.locator("input[name=client_id]")

        expect(edit_form).to_be_visible()
        expect(edit_form).to_have_attribute("action", reverse("clients_delete"))
        expect(client_id_input).not_to_be_visible()
        expect(client_id_input).to_have_value(str(client.id))
        expect(edit_form.get_by_role("button", name="Eliminar")).to_be_visible()

    def test_should_can_be_able_to_delete_a_client(self):
        """
        Verifica que se pueda eliminar un cliente.
        """

        Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()

        def is_delete_response(response):
            return response.url.find(reverse("clients_delete"))

        with self.page.expect_response(is_delete_response) as response_info:
            self.page.get_by_role("button", name="Eliminar").click()

        response = response_info.value
        self.assertTrue(response.status < 400)

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()


class ClientCreateEditTestCase(PlaywrightTestCase):
    """
    Pruebas para la creación y edición de clientes.
    """

    def test_should_be_able_to_create_a_new_client(self):
        """
        Verifica que se pueda crear un nuevo cliente.
        """

        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("221555232")
        self.page.get_by_label("Email").fill("brujita75@hotmail.com")
        self.page.get_by_label("Dirección").fill("13 y 44")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("221555232")).to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).to_be_visible()
        expect(self.page.get_by_text("13 y 44")).to_be_visible()

    def test_should_view_errors_if_form_is_invalid(self):
        """
        Verifica que se muestren errores si el formulario es inválido.
        """

        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un teléfono")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("221555232")
        self.page.get_by_label("Email").fill("brujita75")
        self.page.get_by_label("Dirección").fill("13 y 44")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(
            self.page.get_by_text("Por favor ingrese un teléfono")
        ).not_to_be_visible()

        expect(
            self.page.get_by_text("Por favor ingrese un email valido")
        ).to_be_visible()

    def test_should_be_able_to_edit_a_client(self):
        """
        Verifica que se pueda editar un cliente existente.
        """

        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        path = reverse("clients_edit", kwargs={"id": client.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Guido Carrillo")
        self.page.get_by_label("Teléfono").fill("221232555")
        self.page.get_by_label("Email").fill("goleador@gmail.com")
        self.page.get_by_label("Dirección").fill("1 y 57")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()
        expect(self.page.get_by_text("13 y 44")).not_to_be_visible()
        expect(self.page.get_by_text("221555232")).not_to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).not_to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("1 y 57")).to_be_visible()
        expect(self.page.get_by_text("221232555")).to_be_visible()
        expect(self.page.get_by_text("goleador@gmail.com")).to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("clients_edit", kwargs={"id": client.id})
        )


class ProductCreateEditTestCase(PlaywrightTestCase):
    """
    Pruebas para la creación y edición de productos.
    """

    def test_should_be_able_to_create_a_new_product(self):
        """
        Verifica que se pueda crear un nuevo producto.
        """

        self.page.goto(f"{self.live_server_url}{reverse('products_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Ampicilina")
        self.page.get_by_label("Tipo").fill("Antibiotico")
        self.page.get_by_label("Precio").fill("10")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Ampicilina")).to_be_visible()
        expect(self.page.get_by_text("Antibiotico")).to_be_visible()
        expect(self.page.get_by_text("10")).to_be_visible()

    def test_should_view_errors_if_price_is_zero(self):
        """
        Verifica que se muestren errores si el precio del producto es cero.
        """

        self.page.goto(f"{self.live_server_url}{reverse('products_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()
        
        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un tipo")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un precio")).to_be_visible()
        
        self.page.get_by_label("Nombre").fill("ampicilina")
        self.page.get_by_label("Tipo").fill("antibiotico")
        self.page.get_by_label("Precio").fill("0")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un tipo")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un precio mayor a cero")).to_be_visible()

    
    def test_should_view_errors_if_price_is_negative(self):
        """
        Verifica que se muestren errores si el precio del producto es negativo.
        """

        self.page.goto(f"{self.live_server_url}{reverse('products_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()
        self.page.get_by_role("button", name="Guardar").click()
        
        self.page.get_by_label("Nombre").fill("ampicilina")
        self.page.get_by_label("Tipo").fill("antibiotico")
        self.page.get_by_label("Precio").fill("-10")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un tipo")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un precio")).to_be_visible()


    def test_should_view_errors_if_price_is_empty(self):
        """
        Verifica que se muestren errores si el precio del producto está vacío.
        """

        self.page.goto(f"{self.live_server_url}{reverse('products_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Ampicilina")
        self.page.get_by_label("Tipo").fill("Antibiotico")
        self.page.get_by_label("Precio").fill("")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un precio")).to_be_visible()
    

    def test_should_not_allow_editing_product_with_empty_or_zero_price(self):
        """
        Verifica que no se permita editar un producto con precio cero o vacío.
        """
    
        product = Product.objects.create(
            name="ampicilina",
            type="antibiotico",
            price=10
        )

        path = reverse("products_edit", kwargs={"id": product.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Producto Editado")
        self.page.get_by_label("Tipo").fill("Tipo Editado")
        self.page.get_by_label("Precio").fill("")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un precio")).to_be_visible()

        self.page.get_by_label("Precio").fill("0")
        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un precio mayor a cero")).to_be_visible()

    def test_should_not_allow_editing_product_with_negative_price(self):
        """
        Verifica que no se permita editar un producto con precio negativo.
        """

        product = Product.objects.create(
            name="ampicilina",
            type="antibiotico",
            price=10
        )

        path = reverse("products_edit", kwargs={"id": product.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Producto Editado")
        self.page.get_by_label("Tipo").fill("Tipo Editado")
        self.page.get_by_label("Precio").fill("-10")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un precio mayor a cero")).to_be_visible()


class PetsRepoTestCase(PlaywrightTestCase):
    """
    Pruebas para el repositorio de mascotas.
    """

    def test_should_show_message_if_table_is_empty(self):
        """
        Verifica que se muestre un mensaje si la tabla de mascotas está vacía.
        """

        self.page.goto(f"{self.live_server_url}{reverse('pets_repo')}")
        expect(self.page.get_by_text("No existen mascotas")).to_be_visible()
   
    def test_should_show_pets_data(self):
        """
        Verifica que se muestren los datos de las mascotas.
        """

        Pet.objects.create(
            name="gatito",
            breed="orange",
            birthday="2024-05-18",
        )
        Pet.objects.create(
            name="mishu",
            breed="mestizo",
            birthday="2024-04-10",
        )
        
        self.page.goto(f"{self.live_server_url}{reverse('pets_repo')}")
        
        expect(self.page.get_by_text("No existen mascotas")).not_to_be_visible()
        expect(self.page.get_by_text("gatito")).to_be_visible()
        expect(self.page.get_by_text("orange")).to_be_visible()
        expect(self.page.get_by_text("May 18, 2024")).to_be_visible()
        expect(self.page.get_by_text("mishu")).to_be_visible()
        expect(self.page.get_by_text("mestizo")).to_be_visible()
        expect(self.page.get_by_text("April 10, 2024")).to_be_visible()
    
    def test_should_show_add_pet_action(self):
        """
        Verifica que se muestre la acción para agregar una nueva mascota.
        """

        self.page.goto(f"{self.live_server_url}{reverse('pets_repo')}")
        add_client_action = self.page.get_by_role(
            "link", name="Nueva Mascota", exact=False
        )
        
        expect(add_client_action).to_have_attribute("href", reverse("pets_form"))
    
    def test_should_show_pet_edit_action(self):
        """
        Verifica que se muestre la acción para editar una mascota.
        """

        pet = Pet.objects.create(
            name="gatito",
            breed="orange",
            birthday="2024-05-18",
        )
        
        self.page.goto(f"{self.live_server_url}{reverse('pets_repo')}")
        
        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("pets_edit", kwargs={"id": pet.id})
        )
    
    def test_should_show_pet_delete_action(self):
        """
        Verifica que se muestre la acción para eliminar una mascota.
        """

        pet = Pet.objects.create(
            name="gatito",
            breed="orange",
            birthday="2024-05-18",
        )
        
        self.page.goto(f"{self.live_server_url}{reverse('pets_repo')}")
        
        edit_form = self.page.get_by_role(
            "form", name="Formulario de eliminación de mascotas" 
        
        )
        pet_id_input = edit_form.locator("input[name=pet_id]")
        
        expect(edit_form).to_be_visible()
        expect(edit_form).to_have_attribute("action", reverse("pets_delete"))
        expect(pet_id_input).not_to_be_visible()
        expect(pet_id_input).to_have_value(str(pet.id))
        expect(edit_form.get_by_role("button", name="Eliminar")).to_be_visible()
    
    def test_should_be_able_to_delete_a_pet(self):
        """
        Verifica que se pueda eliminar una mascota.
        """

        Pet.objects.create(
            name="gatito",
            breed="orange",
            birthday="2024-05-18",
        )
        
        self.page.goto(f"{self.live_server_url}{reverse('pets_repo')}")
        
        expect(self.page.get_by_text("gatito")).to_be_visible()
        
        def is_delete_response(response):
            return response.url.find(reverse("pets_delete"))
        
        with self.page.expect_response(is_delete_response) as response_info:
            self.page.get_by_role("button", name="Eliminar").click()
        
        response = response_info.value
        self.assertTrue(response.status < 400) #si es menor es exitoso
        
        expect(self.page.get_by_text("gatito")).not_to_be_visible()


class PetCreateEditTestCase(PlaywrightTestCase):
    """
    Pruebas para crear y editar mascotas.
    """

    def test_should_be_able_to_create_a_new_pet(self):
        """
        Verifica que se pueda crear una nueva mascota.
        """

        self.page.goto(f"{self.live_server_url}{reverse('pets_form')}")
        
        expect(self.page.get_by_role("form")).to_be_visible()
        
        self.page.get_by_label("Nombre").fill("gatito")
        self.page.get_by_label("Raza").fill("orange")
        self.page.get_by_label("Fecha de Nacimiento").fill("2024-05-18")
        self.page.get_by_role("button", name="Guardar").click()
        
        expect(self.page.get_by_text("gatito")).to_be_visible()
        expect(self.page.get_by_text("orange")).to_be_visible()
        expect(self.page.get_by_text("May 18, 2024")).to_be_visible()
    
    def test_should_view_errors_if_form_is_invalid(self):
        """
        Verifica que se muestren errores si el formulario es inválido.
        """

        self.page.goto(f"{self.live_server_url}{reverse('pets_form')}")
        
        expect(self.page.get_by_role("form")).to_be_visible()
        
        self.page.get_by_role("button", name="Guardar").click()
        
        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una raza")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una fecha de nacimiento valida y anterior a la de hoy")).to_be_visible()
        
        self.page.get_by_label("Nombre").fill("gatito")
        self.page.get_by_label("Raza").fill("orange")
        self.page.get_by_label("Fecha de Nacimiento").fill("2024-05-18")
        self.page.get_by_role("button", name="Guardar").click()
        
        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una raza")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una fecha de nacimiento valida y anterior a la de hoy")).not_to_be_visible()
    
    def test_should_view_error_if_birthday_is_today(self):
        """
        Verifica que se muestre un error si la fecha de nacimiento es hoy.
        """

        date_now = datetime.date.today().strftime("%Y-%m-%d")
        
        self.page.goto(f"{self.live_server_url}{reverse('pets_form')}")
        
        expect(self.page.get_by_role("form")).to_be_visible()
        
        self.page.get_by_label("Nombre").fill("gatito")
        self.page.get_by_label("Raza").fill("orange")
        self.page.get_by_label("Fecha de Nacimiento").fill(date_now)
        self.page.get_by_role("button", name="Guardar").click()
        
        expect(self.page.get_by_text("Por favor ingrese una fecha de nacimiento valida y anterior a la de hoy")).to_be_visible()
        
        self.page.get_by_label("Nombre").fill("gatito")
        self.page.get_by_label("Raza").fill("orange")
        self.page.get_by_label("Fecha de Nacimiento").fill("2024-05-18")
        self.page.get_by_role("button", name="Guardar").click()
        
        expect(self.page.get_by_text("Por favor ingrese una fecha de nacimiento valida y anterior a la de hoy")).not_to_be_visible()
    
    def test_should_view_error_if_birthday_is_later_than_today(self): 
        """
        Verifica que se muestre un error si la fecha de nacimiento es posterior a hoy.
        """

        date_now = datetime.date.today()
        date_later = date_now + datetime.timedelta(days=1)
        date = date_later.strftime("%Y-%m-%d")
        
        self.page.goto(f"{self.live_server_url}{reverse('pets_form')}")
        
        expect(self.page.get_by_role("form")).to_be_visible()
        
        self.page.get_by_label("Nombre").fill("gatito")
        self.page.get_by_label("Raza").fill("orange")
        self.page.get_by_label("Fecha de Nacimiento").fill(date)
        self.page.get_by_role("button", name="Guardar").click()
        
        expect(self.page.get_by_text("Por favor ingrese una fecha de nacimiento valida y anterior a la de hoy")).to_be_visible()
        
        self.page.get_by_label("Nombre").fill("gatito")
        self.page.get_by_label("Raza").fill("orange")
        self.page.get_by_label("Fecha de Nacimiento").fill("2024-05-18")
        self.page.get_by_role("button", name="Guardar").click()
        
        expect(self.page.get_by_text("Por favor ingrese una fecha de nacimiento valida y anterior a la de hoy")).not_to_be_visible()
    
    def test_should_be_able_to_edit_a_pet(self):
        """
        Verifica que se pueda editar una mascota.
        """

        pet = Pet.objects.create(
            name="gatito",
            breed="orange",
            birthday="2024-05-18",
        )
        
        path = reverse("pets_edit", kwargs={"id": pet.id})
        
        self.page.goto(f"{self.live_server_url}{path}")
        self.page.get_by_label("Nombre").fill("mishu")
        self.page.get_by_label("Raza").fill("mestizo")
        self.page.get_by_label("Fecha de Nacimiento").fill("2024-04-10")
        self.page.get_by_role("button", name="Guardar").click()
        
        expect(self.page.get_by_text("gatito")).not_to_be_visible()
        expect(self.page.get_by_text("orange")).not_to_be_visible()
        expect(self.page.get_by_text("May 18, 2024")).not_to_be_visible()
        expect(self.page.get_by_text("mishu")).to_be_visible()
        expect(self.page.get_by_text("mestizo")).to_be_visible()
        expect(self.page.get_by_text("April 10, 2024")).to_be_visible()
        
        edit_action = self.page.get_by_role("link", name="Editar")
        
        expect(edit_action).to_have_attribute(
            "href", reverse("pets_edit", kwargs={"id": pet.id})
        )
    
    def test_should_not_be_able_to_edit_pet_if_form_is_invalid(self):
        """
        Verifica que no se pueda editar una mascota si el formulario es inválido.
        """

        pet = Pet.objects.create(
            name="gatito",
            breed="orange",
            birthday="2024-05-18",
        )
        
        path = reverse("pets_edit", kwargs={"id": pet.id})
        
        self.page.goto(f"{self.live_server_url}{path}")
        self.page.get_by_label("Nombre").fill("")
        self.page.get_by_label("Raza").fill("")
        self.page.get_by_label("Fecha de Nacimiento").fill("")
        self.page.get_by_role("button", name="Guardar").click()
        
        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una raza")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una fecha de nacimiento valida y anterior a la de hoy")).to_be_visible()
        
        self.page.get_by_label("Nombre").fill("mishu")
        self.page.get_by_label("Raza").fill("mestizo")
        self.page.get_by_label("Fecha de Nacimiento").fill("2024-04-10")
        self.page.get_by_role("button", name="Guardar").click()
        
        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una raza")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una fecha de nacimiento valida y anterior a la de hoy")).not_to_be_visible()
        
        expect(self.page.get_by_text("gatito")).not_to_be_visible()
        expect(self.page.get_by_text("orange")).not_to_be_visible()
        expect(self.page.get_by_text("May 18, 2024")).not_to_be_visible()
        
        expect(self.page.get_by_text("mishu")).to_be_visible()
        expect(self.page.get_by_text("mestizo")).to_be_visible()
        expect(self.page.get_by_text("April 10, 2024")).to_be_visible()
        
        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("pets_edit", kwargs={"id": pet.id})
        )
    
    def test_should_not_be_able_to_edit_pet_if_birthday_is_today(self):
        """
        Verifica que no se pueda editar una mascota si la fecha de nacimiento es hoy.
        """

        pet = Pet.objects.create(
            name="gatito",
            breed="orange",
            birthday="2024-05-18",
        )
        
        path = reverse("pets_edit", kwargs={"id": pet.id})
        
        self.page.goto(f"{self.live_server_url}{path}")
        
        date_now = datetime.date.today().strftime("%Y-%m-%d")
        
        self.page.get_by_label("Nombre").fill("gatito")
        self.page.get_by_label("Raza").fill("orange")
        self.page.get_by_label("Fecha de Nacimiento").fill(date_now)
        self.page.get_by_role("button", name="Guardar").click()
        
        expect(self.page.get_by_text("Por favor ingrese una fecha de nacimiento valida y anterior a la de hoy")).to_be_visible()
        
        self.page.get_by_label("Nombre").fill("gatito")
        self.page.get_by_label("Raza").fill("orange")
        self.page.get_by_label("Fecha de Nacimiento").fill("2024-04-10")
        self.page.get_by_role("button", name="Guardar").click()
        
        expect(self.page.get_by_text("Por favor ingrese una fecha de nacimiento valida y anterior a la de hoy")).not_to_be_visible()
        expect(self.page.get_by_text("gatito")).to_be_visible()
        expect(self.page.get_by_text("orange")).to_be_visible()
        expect(self.page.get_by_text("April 10, 2024")).to_be_visible()
        
        expect(self.page.get_by_text("May 18, 2024")).not_to_be_visible()
        
        edit_action = self.page.get_by_role("link", name="Editar")
        
        expect(edit_action).to_have_attribute(
            "href", reverse("pets_edit", kwargs={"id": pet.id})
        )
    
    def test_should_not_be_able_to_edit_pet_if_birthday_is_later_than_today(self):
        """
        Verifica que no se pueda editar una mascota si la fecha de nacimiento es posterior a hoy.
        """

        pet = Pet.objects.create(
            name="gatito",
            breed="orange",
            birthday="2024-05-18",
        )
        
        path = reverse("pets_edit", kwargs={"id": pet.id})
        
        self.page.goto(f"{self.live_server_url}{path}")
        
        date_now = datetime.date.today()
        date_later = date_now + datetime.timedelta(days=1)
        date = date_later.strftime("%Y-%m-%d")
        
        self.page.get_by_label("Nombre").fill("gatito")
        self.page.get_by_label("Raza").fill("orange")
        self.page.get_by_label("Fecha de Nacimiento").fill(date)
        
        self.page.get_by_role("button", name="Guardar").click()
        
        expect(self.page.get_by_text("Por favor ingrese una fecha de nacimiento valida y anterior a la de hoy")).to_be_visible()
        
        self.page.get_by_label("Nombre").fill("gatito")
        self.page.get_by_label("Raza").fill("orange")
        self.page.get_by_label("Fecha de Nacimiento").fill("2024-04-10")
        
        self.page.get_by_role("button", name="Guardar").click()
        
        expect(self.page.get_by_text("Por favor ingrese una fecha de nacimiento valida y anterior a la de hoy")).not_to_be_visible()
        expect(self.page.get_by_text("gatito")).to_be_visible()
        expect(self.page.get_by_text("orange")).to_be_visible()
        expect(self.page.get_by_text("April 10, 2024")).to_be_visible()
        
        expect(self.page.get_by_text("May 18, 2024")).not_to_be_visible()
        
        edit_action = self.page.get_by_role("link", name="Editar")
        
        expect(edit_action).to_have_attribute(
            "href", reverse("pets_edit", kwargs={"id": pet.id})
        )


class VetsRepoTestCase(PlaywrightTestCase):
    """
    Pruebas para la vista del repositorio de veterinarios.
    """

    def test_should_show_message_if_table_is_empty(self):
        """
        Verifica que se muestre un mensaje si la tabla está vacía.
        """

        self.page.goto(f"{self.live_server_url}{reverse('vets_repo')}")
        expect(self.page.get_by_text("No existen veterinarios")).to_be_visible()
    
    def test_should_show_vets_data(self):
        """
        Verifica que se muestren los datos de los veterinarios correctamente.
        """

        Vet.objects.create(
            name="Juan Sebastián Veron",
            email="brujita75@hotmail.com",
            phone="221555232",
            speciality="Urgencias",
        )
        
        Vet.objects.create(
            name="Guido Carrillo",
            email="goleador@gmail.com",
            phone="221232555",
            speciality="Oftalmologia"
        )
        
        self.page.goto(f"{self.live_server_url}{reverse('vets_repo')}")
        
        expect(self.page.get_by_text("No existen veterinarios")).not_to_be_visible()
        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).to_be_visible()
        expect(self.page.get_by_text("221555232")).to_be_visible()
        expect(self.page.get_by_text("Urgencias")).to_be_visible()
        
        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("goleador@gmail.com")).to_be_visible()
        expect(self.page.get_by_text("221232555")).to_be_visible()
        expect(self.page.get_by_text("Oftalmologia")).to_be_visible()
    
    def test_should_show_add_vet_action(self):
        """
        Verifica que se muestre la acción de agregar veterinario.
        """

        self.page.goto(f"{self.live_server_url}{reverse('vets_repo')}")
        
        add_vet_action = self.page.get_by_role(
            "link", name="Nuevo Veterinario", exact=False
        )
        
        expect(add_vet_action).to_have_attribute("href", reverse("vets_form"))
    
    def test_should_show_vet_edit_action(self):
        """
        Verifica que se muestre la acción de editar veterinario.
        """

        vet = Vet.objects.create(
            name="Juan Sebastián Veron",
            email="brujita75@hotmail.com",
            phone="221555232",
            speciality="Urgencias",
        )
        
        self.page.goto(f"{self.live_server_url}{reverse('vets_repo')}")
        
        edit_action = self.page.get_by_role("link", name="Editar")
        
        expect(edit_action).to_have_attribute(
            "href", reverse("vets_edit", kwargs={"id": vet.id})
        )
    
    def test_should_show_vet_delete_action(self):
        """
        Verifica que se muestre la acción de eliminar veterinario.
        """

        vet = Vet.objects.create(
            name="Juan Sebastián Veron",
            email="brujita75@hotmail.com",
            phone="221555232",
            speciality="Urgencias",
        )
        
        self.page.goto(f"{self.live_server_url}{reverse('vets_repo')}")
        
        edit_form = self.page.get_by_role(
            "form", name="Formulario de eliminación de veterinario"
        )
        
        vet_id_input = edit_form.locator("input[name=vet_id]")
        
        expect(edit_form).to_be_visible()
        
        expect(edit_form).to_have_attribute("action", reverse("vets_delete"))
        
        expect(vet_id_input).not_to_be_visible()
        expect(vet_id_input).to_have_value(str(vet.id))
        
        expect(edit_form.get_by_role("button", name="Eliminar")).to_be_visible()
    
    def test_should_can_be_able_to_delete_a_vet(self):
        """
        Verifica que se pueda eliminar un veterinario.
        """

        Vet.objects.create(
            name="Juan Sebastián Veron",
            email="brujita75@hotmail.com",
            phone="221555232",
            speciality="Urgencias",
        )
        
        self.page.goto(f"{self.live_server_url}{reverse('vets_repo')}")
        
        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        
        def is_delete_response(response):
            return response.url.find(reverse("vets_delete"))
        
        with self.page.expect_response(is_delete_response) as response_info:
            self.page.get_by_role("button", name="Eliminar").click()
        
        response = response_info.value
        
        self.assertTrue(response.status < 400)
        
        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()


class VetCreateEditTestCase(PlaywrightTestCase):
    """
    Pruebas para la creación y edición de veterinarios.
    """

    def test_should_be_able_to_create_a_new_vet(self):
        """
        Verifica que se pueda crear un nuevo veterinario.
        """
        
        self.page.goto(f"{self.live_server_url}{reverse('vets_form')}")
        
        expect(self.page.get_by_role("form")).to_be_visible()
        
        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Email").fill("brujita75@hotmail.com")
        self.page.get_by_label("Teléfono").fill("221555232")
        self.page.select_option("select[name=speciality]", value="Urgencias")
        
        self.page.get_by_role("button", name="Guardar").click()
        
        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).to_be_visible()
        expect(self.page.get_by_text("221555232")).to_be_visible()
        expect(self.page.get_by_text("Urgencias")).to_be_visible()
    
    def test_should_view_errors_if_form_is_invalid(self):
        """
        Verifica que se muestren errores si el formulario es inválido.
        """

        self.page.goto(f"{self.live_server_url}{reverse('vets_form')}")
        
        expect(self.page.get_by_role("form")).to_be_visible()
        
        self.page.get_by_role("button", name="Guardar").click()
        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un teléfono")).to_be_visible()
        expect(self.page.get_by_text("Por favor seleccione una especialidad")).to_be_visible()
        
        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Email").fill("brujita75")
        self.page.get_by_label("Teléfono").fill("221555232")
        self.page.select_option("select[name=speciality]", value="Urgencias")
        
        self.page.get_by_role("button", name="Guardar").click()
        
        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email valido")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un teléfono")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor seleccione una especialidad")).not_to_be_visible()
    
    def test_should_be_able_to_edit_a_vet(self):
        """
        Verifica que se pueda editar un veterinario.
        """

        vet = Vet.objects.create(
            name="Juan Sebastián Veron",
            email="brujita75@hotmail.com",
            phone="221555232",
            speciality="Urgencias",
        )
        
        path = reverse("vets_edit", kwargs={"id": vet.id})
        
        self.page.goto(f"{self.live_server_url}{path}")
        
        self.page.get_by_label("Nombre").fill("Guido Carrillo")
        self.page.get_by_label("Email").fill("goleador@gmail.com")
        self.page.get_by_label("Teléfono").fill("221232555")
        self.page.select_option("select[name=speciality]", value="Oftalmologia")
        
        self.page.get_by_role("button", name="Guardar").click()
        
        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).not_to_be_visible()
        expect(self.page.get_by_text("221555232")).not_to_be_visible()
        expect(self.page.get_by_text("Urgencias")).not_to_be_visible()
        
        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("goleador@gmail.com")).to_be_visible()
        expect(self.page.get_by_text("221232555")).to_be_visible()
        expect(self.page.get_by_text("Oftalmologia")).to_be_visible()
        
        edit_action = self.page.get_by_role("link", name="Editar")
        
        expect(edit_action).to_have_attribute(
            "href", reverse("vets_edit", kwargs={"id": vet.id})
        )
    
    def test_should_be_able_to_create_a_new_vet_with_valid_speciality(self):
        """
        Verifica que se pueda crear un nuevo veterinario con una especialidad válida.
        """

        self.page.goto(f"{self.live_server_url}{reverse('vets_form')}")
        
        expect(self.page.get_by_role("form")).to_be_visible()
        
        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Email").fill("brujita75@hotmail.com")
        self.page.get_by_label("Teléfono").fill("221555232")
        
        valid_specialities = [speciality.value for speciality in Speciality]
        self.page.select_option("select[name=speciality]", value=valid_specialities[0])
        
        self.page.get_by_role("button", name="Guardar").click()
        
        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).to_be_visible()
        expect(self.page.get_by_text("221555232")).to_be_visible()
        expect(self.page.get_by_text(valid_specialities[0])).to_be_visible() 


class ProvidersRepoTestCase(PlaywrightTestCase):
    """
    Pruebas para la vista del repositorio de proveedores.
    """
     
    def test_should_show_message_if_table_is_empty(self):
        """
        Verifica que se muestre un mensaje si la tabla está vacía.
        """

        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        expect(self.page.get_by_text("No existen proveedores")).to_be_visible()

    def test_should_show_providers_data(self):
        """
        Verifica que se muestren los datos de los proveedores correctamente.
        """

        Provider.objects.create(
            name = "Bogado",
            email = "demian@utn.com",
            address = "Calle falsa 123",
        )

        Provider.objects.create(
            name = "Luciana",
            email = "lu@utn.com",
            address = "Avenida Siempreviva 742",
        )

        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        expect(self.page.get_by_text("No existen proveedores")).not_to_be_visible()

        expect(self.page.get_by_text("Bogado")).to_be_visible()
        expect(self.page.get_by_text("demian@utn.com")).to_be_visible()
        expect(self.page.get_by_text("Calle falsa 123")).to_be_visible()

        expect(self.page.get_by_text("Luciana")).to_be_visible()
        expect(self.page.get_by_text("lu@utn.com")).to_be_visible()
        expect(self.page.get_by_text("Avenida Siempreviva 742")).to_be_visible()

    def test_should_show_add_provider_action(self):
        """
        Verifica que se muestre la acción de agregar proveedor.
        """

        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        add_provider_action = self.page.get_by_role(
            "link", name="Nuevo Proveedor", exact=False
        )

        expect(add_provider_action).to_have_attribute("href", reverse("providers_form"))

    def test_should_show_provider_edit_action(self):
        """
        Verifica que se muestre la acción de editar proveedor.
        """

        provider = Provider.objects.create(
            name="Demian",
            email="demian@utn.com",
            address="Calle falsa 123",
        )

        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("providers_edit", kwargs={"id":provider.id})
        )

    def test_should_show_provider_delete_action(self):
        """
        Verifica que se muestre la acción de eliminar proveedor.
        """

        provider = Provider.objects.create(
            name="Demian",
            email="demian@utn.com",
            address="Calle falsa 123",
        )

        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        delete_form = self.page.get_by_role(
            "form", name="Formulario de eliminación de proveedor"
        )
        provider_id_input = delete_form.locator("input[name=provider_id]")

        expect(delete_form).to_be_visible()
        expect(delete_form).to_have_attribute("action", reverse("providers_delete"))
        expect(provider_id_input).not_to_be_visible()
        expect(provider_id_input).to_have_value(str(provider.id))
        expect(delete_form.get_by_role("button", name="Eliminar")).to_be_visible()

    def test_should_be_able_to_delete_a_provider(self):
        """
        Verifica que se pueda eliminar un proveedor.
        """

        Provider.objects.create(
            name="Bogado",
            email="demian@utn.com",
            address="Calle falsa 123",
        )

        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        expect(self.page.get_by_text("Bogado")).to_be_visible()

        def is_delete_response(response):
            return response.url.find(reverse("providers_delete"))

        with self.page.expect_response(is_delete_response) as response_info:
            self.page.get_by_role("button", name="Eliminar").click()

        response = response_info.value
        self.assertTrue(response.status < 400)

        expect(self.page.get_by_text("Bogado")).not_to_be_visible()


class ProviderCreateEditTestCase(PlaywrightTestCase):
    """
    Pruebas para la creación y edición de proveedores.
    """

    def test_should_be_able_to_create_a_new_provider(self):
        """
        Verifica que se pueda crear un nuevo proveedor correctamente.
        """

        self.page.goto(f"{self.live_server_url}{reverse('providers_form')}")

        expect(self.page.get_by_role("form")).to_be_visible

        self.page.get_by_label("Nombre").fill("Bogado")
        self.page.get_by_label("Email").fill("demian@utn.com")
        self.page.get_by_label("Dirección").fill("Calle falsa 123")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Bogado")).to_be_visible()
        expect(self.page.get_by_text("demian@utn.com")).to_be_visible()
        expect(self.page.get_by_text("Calle falsa 123")).to_be_visible()

    def test_should_view_errors_if_form_is_invalid(self):
        """
        Verifica que se muestren los errores si el formulario es inválido.
        """

        self.page.goto(f"{self.live_server_url}{reverse('providers_form')}")

        expect(self.page.get_by_role("form")).to_be_visible

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una dirección")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Bogado")
        self.page.get_by_label("Email").fill("demian@utn.com")
        self.page.get_by_label("Dirección").fill("Calle falsa 123")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una dirección")).not_to_be_visible()

    def test_should_view_error_if_address_is_empty(self):
        """
        Verifica que se muestre un error si la dirección está vacía.
        """

        self.page.goto(f"{self.live_server_url}{reverse('providers_form')}")

        expect(self.page.get_by_role("form")).to_be_visible

        self.page.get_by_label("Nombre").fill("Bogado")
        self.page.get_by_label("Email").fill("demian@utn.com")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese una dirección")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Bogado")
        self.page.get_by_label("Email").fill("demian@utn.com")
        self.page.get_by_label("Dirección").fill("Calle falsa 123")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese una dirección")).not_to_be_visible()

    def test_should_be_able_to_edit_a_provider(self):
        """
        Verifica que se pueda editar un proveedor correctamente.
        """
        
        provider = Provider.objects.create(
            name = "Bogado",
            email = "demian@utn.com",
            address = "Calle falsa 123",
        )

        path = reverse("providers_edit", kwargs={"id": provider.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Luciana")
        self.page.get_by_label("Email").fill("lu@utn.com")
        self.page.get_by_label("Dirección").fill("Avenida Siempreviva 742")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Bogado")).not_to_be_visible()
        expect(self.page.get_by_text("demian@utn.com")).not_to_be_visible()
        expect(self.page.get_by_text("Calle falsa 123")).not_to_be_visible()

        expect(self.page.get_by_text("Luciana")).to_be_visible()
        expect(self.page.get_by_text("lu@utn.com")).to_be_visible()
        expect(self.page.get_by_text("Avenida Siempreviva 742")).to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("providers_edit", kwargs={"id":provider.id})
        )

    def test_should_not_be_able_to_edit_provider_if_form_is_invalid(self):
        """
        Verifica que no se pueda editar un proveedor si el formulario es inválido.
        """

        provider = Provider.objects.create(
            name = "Bogado",
            email = "demian@utn.com",
            address = "Calle falsa 123",
        )

        path = reverse("providers_edit", kwargs={"id": provider.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("")
        self.page.get_by_label("Email").fill("")
        self.page.get_by_label("Dirección").fill("")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una dirección")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Luciana")
        self.page.get_by_label("Email").fill("lu@utn.com")
        self.page.get_by_label("Dirección").fill("Avenida Siempreviva 742")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una dirección")).not_to_be_visible()

        expect(self.page.get_by_text("Bogado")).not_to_be_visible()
        expect(self.page.get_by_text("demian@utn.com")).not_to_be_visible()
        expect(self.page.get_by_text("Calle falsa 123")).not_to_be_visible()

        expect(self.page.get_by_text("Luciana")).to_be_visible()
        expect(self.page.get_by_text("lu@utn.com")).to_be_visible()
        expect(self.page.get_by_text("Avenida Siempreviva 742")).to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("providers_edit", kwargs={"id":provider.id})
        )

    def test_should_not_be_able_to_edit_a_provider_if_address_is_empty(self):
        """
        Verifica que no se pueda editar un proveedor si la dirección está vacía.
        """

        provider = Provider.objects.create(
            name = "Bogado",
            email = "demian@utn.com",
            address = "Calle falsa 123",
        )

        path = reverse("providers_edit", kwargs={"id": provider.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill(provider.name)
        self.page.get_by_label("Email").fill(provider.email)
        self.page.get_by_label("Dirección").fill("")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese una dirección")).to_be_visible()

        self.page.get_by_label("Nombre").fill(provider.name)
        self.page.get_by_label("Email").fill(provider.email)
        self.page.get_by_label("Dirección").fill("Avenida Siempreviva 742")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese una dirección")).not_to_be_visible()

        expect(self.page.get_by_text("Bogado")).to_be_visible()
        expect(self.page.get_by_text("demian@utn.com")).to_be_visible()
        expect(self.page.get_by_text("Avenida Siempreviva 742")).to_be_visible()

        expect(self.page.get_by_text("Calle falsa 123")).not_to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("providers_edit", kwargs={"id":provider.id})
        )
        

class MedicineCreateEditTestCase(PlaywrightTestCase):
    """
    Pruebas para la creación y edición de medicinas.
    """

    def test_should_be_able_to_create_a_new_medicine(self):
        """
        Verifica que se pueda crear una nueva medicina.
        """

        self.page.goto(f"{self.live_server_url}{reverse('medicine_form')}")

        expect(self.page.get_by_role("form")).to_be_visible

        self.page.get_by_label("Nombre").fill("Bravecto")
        self.page.get_by_label("Descripción").fill("Previene y elimina parasitos externos")
        self.page.get_by_label("Dosis").fill("1")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Bravecto")).to_be_visible()
        expect(self.page.get_by_text("Previene y elimina parasitos externos")).to_be_visible()
        expect(self.page.get_by_text("1")).to_be_visible()
    
    def test_should_view_errors_if_form_is_invalid(self):
        """
        Verifica que se muestren errores si el formulario es inválido.
        """

        self.page.goto(f"{self.live_server_url}{reverse('medicine_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor, ingrese un nombre de la medicina")).to_be_visible()
        expect(self.page.get_by_text("Por favor, ingrese una descripcion de la medicina")).to_be_visible()
        expect(self.page.get_by_text("Por favor, ingrese una cantidad de la dosis de la medicina")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Bravecto")
        self.page.get_by_label("Descripción").fill("")
        self.page.get_by_label("Dosis").fill("1")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor, ingrese un nombre de la medicina")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor, ingrese una descripcion de la medicina")).to_be_visible()
        expect(self.page.get_by_text("Por favor, ingrese una cantidad de la dosis de la medicina")).not_to_be_visible()
        
    def test_should_be_able_to_edit_a_medicine(self):
        """
        Verifica que se pueda editar una medicina.
        """

        medicine = Medicine.objects.create(
            name="Bravecto",
            description="Previene y elimina parasitos externos",
            dose=2,
        )

        path = reverse("medicine_edit", kwargs={"id": medicine.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Meloxicam")
        self.page.get_by_label("Descripción").fill("Antiinflamatorio")
        self.page.get_by_label("Dosis").fill("6")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Bravecto")).not_to_be_visible()
        expect(self.page.get_by_text("Previene y elimina parasitos externos")).not_to_be_visible()
        expect(self.page.get_by_text("2")).not_to_be_visible()

        expect(self.page.get_by_text("Meloxicam")).to_be_visible()
        expect(self.page.get_by_text("Antiinflamatorio")).to_be_visible()
        expect(self.page.get_by_text("6")).to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("medicine_edit", kwargs={"id": medicine.id})
        )    
    
    def test_should_not_be_able_to_create_a_new_medicine_if_dose_is_empty(self):
        """
        Verifica que no se pueda crear una nueva medicina si la dosis está vacía.
        """

        self.page.goto(f"{self.live_server_url}{reverse('medicine_form')}")

        expect(self.page.get_by_role("form")).to_be_visible

        self.page.get_by_label("Nombre").fill("Bravecto")
        self.page.get_by_label("Descripción").fill("Previene y elimina parasitos externos")
        self.page.get_by_label("Dosis").fill("")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor, ingrese un nombre de la medicina")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor, ingrese una descripcion de la medicina")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor, ingrese una cantidad de la dosis de la medicina")).to_be_visible()
    
    def test_should_not_be_able_to_create_a_new_medicine_if_dose_is_decimal(self):
        """
        Verifica que no se pueda crear una nueva medicina si la dosis es un número decimal.
        """

        self.page.goto(f"{self.live_server_url}{reverse('medicine_form')}")

        expect(self.page.get_by_role("form")).to_be_visible

        self.page.get_by_label("Nombre").fill("Bravecto")
        self.page.get_by_label("Descripción").fill("Previene y elimina parasitos externos")
        self.page.get_by_label("Dosis").fill("1.5")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor, ingrese un nombre de la medicina")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor, ingrese una descripcion de la medicina")).not_to_be_visible()
        expect(self.page.get_by_text("La dosis debe ser un numero entero")).to_be_visible()
        
    def test_should_not_be_able_to_create_a_new_medicine_if_dose_is_out_of_range(self):
        """
        Verifica que no se pueda crear una nueva medicina si la dosis está fuera de rango.
        """
        
        self.page.goto(f"{self.live_server_url}{reverse('medicine_form')}")

        expect(self.page.get_by_role("form")).to_be_visible

        self.page.get_by_label("Nombre").fill("Bravecto")
        self.page.get_by_label("Descripción").fill("Previene y elimina parasitos externos")
        self.page.get_by_label("Dosis").fill("15")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor, ingrese un nombre de la medicina")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor, ingrese una descripcion de la medicina")).not_to_be_visible()
        expect(self.page.get_by_text("La dosis debe estar entre 1 y 10")).to_be_visible()
        