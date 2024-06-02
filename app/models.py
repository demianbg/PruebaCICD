from django.db import models
from enum import Enum
import datetime

def validate_client(data):
    """
    Valida los datos de un cliente.

    Args:
        data (dict): Un diccionario que contiene los datos del cliente.

    Returns:
        dict: Un diccionario que contiene los errores encontrados durante la validación.
    """
    errors = {}

    name = data.get("name", "")
    phone = data.get("phone", "")
    email = data.get("email", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if phone == "":
        errors["phone"] = "Por favor ingrese un teléfono"

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    return errors


def validate_provider(data):
    """
    Valida los datos de un proveedor.

    Args:
        data (dict): Un diccionario que contiene los datos del proveedor.

    Returns:
        dict: Un diccionario que contiene los errores encontrados durante la validación.
    """
    errors = {}
    
    name = data.get("name", "")
    email = data.get("email", "")
    address = data.get("address", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    if address == "":
        errors["address"] = "Por favor ingrese una dirección"

    return errors

def validate_medicine(data):
    """
    Valida los datos de un medicamento.

    Args:
        data (dict): Un diccionario que contiene los datos del medicamento.

    Returns:
        dict: Un diccionario que contiene los errores encontrados durante la validación.
    """
    errors = {}

    name = data.get("name", "")
    description = data.get("description", "")
    dose = data.get("dose")
    if dose is not None:
        try:
            num = int(dose)
        except ValueError:
            num = None     

    if name == "":
        errors["name"] = "Por favor, ingrese un nombre de la medicina"
    
    if description == "":
        errors["description"] = "Por favor, ingrese una descripcion de la medicina"
    
    if dose is None or dose == "":
        errors["dose"] = "Por favor, ingrese una cantidad de la dosis de la medicina"
    elif not (isinstance(dose, str) and dose.isdigit()):
        errors["dose"] = "La dosis debe ser un numero entero"
    elif not (num > 0 and num < 11):
        errors["dose"] = "La dosis debe estar entre 1 y 10"
    return errors
    
def validate_product(data):
    """
    Valida los datos de un producto.

    Args:
        data (dict): Un diccionario que contiene los datos del producto.

    Returns:
        dict: Un diccionario que contiene los errores encontrados durante la validación.
    """
    errors={}

    name = data.get("name","")
    type = data.get("type","")
    price = data.get("price","")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"
    
    if type == "":
        errors["type"] = "Por favor ingrese un tipo"

    if price == "":
        errors["price"] = "Por favor ingrese un precio"
    else:
        try:
            price_value = float(price)
            if price_value <= 0.0:
                errors["price"] = "Por favor ingrese un precio mayor a cero"
        except ValueError:
            errors["price"] = "Por favor ingrese un precio válido"

    return errors


def validate_pet(data):
    """
    Valida los datos de una mascota.

    Args:
        data (dict): Un diccionario que contiene los datos de la mascota.

    Returns:
        dict: Un diccionario que contiene los errores encontrados durante la validación.
    """
    errors={}

    name = data.get("name","")
    breed = data.get("breed","")
    birthday = data.get("birthday","")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"
    
    if breed == "":
        errors["breed"] = "Por favor ingrese una raza"

    date_now = datetime.date.today().strftime("%Y-%m-%d")

    if birthday == "" or birthday >= date_now: 
        errors["birthday"] = "Por favor ingrese una fecha de nacimiento valida y anterior a la de hoy"

    return errors

def validate_vet(data):
    """
    Valida los datos de un veterinario.

    Args:
        data (dict): Un diccionario que contiene los datos del veterinario.

    Returns:
        dict: Un diccionario que contiene los errores encontrados durante la validación.
    """
    errors = {}

    name = data.get("name", "")
    email = data.get("email", "")
    phone = data.get("phone", "")
    speciality = data.get("speciality", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    if phone == "":
        errors["phone"] = "Por favor ingrese un teléfono"

    if speciality == "":
        errors["speciality"] = "Por favor seleccione una especialidad"

    return errors

class Client(models.Model):
    """
    Modelo para un cliente.

    Atributos:
        name (CharField): Nombre del cliente.
        phone (CharField): Teléfono del cliente.
        email (EmailField): Correo electrónico del cliente.
        address (CharField): Dirección del cliente.
    """
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        """
        Retorna una representación en string del cliente, que es su nombre.
        """
        return self.name

    @classmethod
    def save_client(cls, client_data):
        """
        Guarda un nuevo cliente en la base de datos.

        Args:
            client_data (dict): Un diccionario con los datos del cliente.

        Returns:
            tuple: Una tupla indicando si se guardó correctamente el cliente y, en caso de errores, los mensajes de error.
        """
        errors = validate_client(client_data)

        if len(errors.keys()) > 0:
            return False, errors

        Client.objects.create(
            name=client_data.get("name"),
            phone=client_data.get("phone"),
            email=client_data.get("email"),
            address=client_data.get("address"),
        )

        return True, None

    def update_client(self, client_data):
        """
        Actualiza los datos de un cliente existente en la base de datos.

        Args:
            client_data (dict): Un diccionario con los datos actualizados del cliente.

        Returns:
            tuple: Una tupla indicando si se actualizó correctamente el cliente y, en caso de errores, los mensajes de error.
        """
        errors = validate_client(client_data)

        if len(errors.keys()) > 0:
            return False, errors

        self.name = client_data.get("name", "") or self.name
        self.email = client_data.get("email", "") or self.email
        self.phone = client_data.get("phone", "") or self.phone
        self.address = client_data.get("address", "") or self.address

        self.save()
        return True, None


class Provider (models.Model):
    """
    Modelo para un proveedor.

    Atributos:
        name (CharField): Nombre del proveedor.
        email (EmailField): Correo electrónico del proveedor.
        address (CharField): Dirección del proveedor.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=200)

    def __str__(self):
        """
        Retorna una representación en string del proveedor, que es su nombre.
        """
        return self.name
    
    @classmethod
    def save_provider(cls, provider_data):
        """
        Guarda un nuevo proveedor en la base de datos.

        Args:
            provider_data (dict): Un diccionario con los datos del proveedor.

        Returns:
            tuple: Una tupla indicando si se guardó correctamente el proveedor y, en caso de errores, los mensajes de error.
        """
        errors = validate_provider(provider_data)

        if len(errors.keys()) > 0:
            return False, errors

        Provider.objects.create(
            name=provider_data.get("name"),
            email=provider_data.get("email"),
            address=provider_data.get("address")
        )

        return True, None

    def update_provider(self, provider_data):
        """
        Actualiza los datos de un proveedor existente en la base de datos.

        Args:
            provider_data (dict): Un diccionario con los datos actualizados del proveedor.

        Returns:
            tuple: Una tupla indicando si se actualizó correctamente el proveedor y, en caso de errores, los mensajes de error.
        """
        errors = validate_provider(provider_data)

        if len(errors.keys()) > 0:
            return False, errors
        
        self.name = provider_data.get("name", "") or self.name
        self.email = provider_data.get("email", "") or self.email
        self.address = provider_data.get("address", "") or self.address

        self.save()
        return True, None

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    dose = models.IntegerField()

    def __str__(self):
        """
        Retorna una representación en string del medicamento, que es su nombre.
        """
        return self.name

    @classmethod
    def save_medicine(cls, medicine_data):
        """
        Guarda un nuevo medicamento en la base de datos.

        Args:
            medicine_data (dict): Un diccionario con los datos del medicamento.

        Returns:
            tuple: Una tupla indicando si se guardó correctamente el medicamento y, en caso de errores, los mensajes de error.
        """
        errors = validate_medicine(medicine_data)

        if len(errors.keys()) > 0:
            return False, errors

        Medicine.objects.create(
            name=medicine_data.get("name"),
            description=medicine_data.get("description"),
            dose=medicine_data.get("dose"),
        )
        return True, None

    def update_medicine(self, medicine_data):
        """
        Actualiza los datos de un medicamento existente en la base de datos.

        Args:
            medicine_data (dict): Un diccionario con los datos actualizados del medicamento.

        Returns:
            tuple: Una tupla indicando si se actualizó correctamente el medicamento y, en caso de errores, los mensajes de error.
        """
        errors = validate_medicine(medicine_data)
        
        if len(errors.keys()) > 0:
            return False, errors
        
        self.name = medicine_data.get("name", "") or self.name
        self.description = medicine_data.get("description", "") or self.description
        self.dose = medicine_data.get("dose", None) or self.dose

        self.save()
        return True, None

class Product (models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    price = models.FloatField()

    def __str__(self):
        """
        Retorna una representación en string del producto, que es su nombre.
        """
        return self.name
    
    @classmethod
    def save_product(cls, product_data):
        """
        Guarda un nuevo producto en la base de datos.

        Args:
            product_data (dict): Un diccionario con los datos del producto.

        Returns:
            tuple: Una tupla indicando si se guardó correctamente el producto y, en caso de errores, los mensajes de error.
        """
        errors = validate_product(product_data)

        if len(errors.keys()) > 0:
            return False, errors
        
        Product.objects.create(
            name=product_data.get("name"),
            type=product_data.get("type"),
            price=product_data.get("price"),
        )

        return True, None
    
    def update_product(self, product_data):
        """
        Actualiza los datos de un producto existente en la base de datos.

        Args:
            product_data (dict): Un diccionario con los datos actualizados del producto.

        Returns:
            tuple: Una tupla indicando si se actualizó correctamente el producto y, en caso de errores, los mensajes de error.
        """
        errors = validate_product(product_data)

        if len(errors.keys()) > 0:
            return False, errors
    
        self.name=product_data.get("name", "") or self.name
        self.type=product_data.get("type", "") or self.type
        self.price=product_data.get("price","") or self.price

        self.save()
        return True, None
        
class Pet (models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    birthday = models.DateField()

    def __str__(self):
        """
        Retorna una representación en string de la mascota, que es su nombre.
        """
        return self.name
    
    @classmethod
    def save_pet(cls, pet_data):
        """
        Guarda una nueva mascota en la base de datos.

        Args:
            pet_data (dict): Un diccionario con los datos de la mascota.

        Returns:
            tuple: Una tupla indicando si se guardó correctamente la mascota y, en caso de errores, los mensajes de error.
        """
        errors = validate_pet(pet_data)

        if len(errors.keys()) > 0:
            return False, errors
        
        Pet.objects.create(
            name=pet_data.get("name"),
            breed=pet_data.get("breed"),
            birthday=pet_data.get("birthday"),
        )

        return True, None
    
    def update_pet(self, pet_data):
        """
        Actualiza los datos de una mascota existente en la base de datos.

        Args:
            pet_data (dict): Un diccionario con los datos actualizados de la mascota.

        Returns:
            tuple: Una tupla indicando si se actualizó correctamente la mascota y, en caso de errores, los mensajes de error.
        """
        errors = validate_pet(pet_data)

        if len(errors.keys()) > 0:
            return False, errors

        self.name=pet_data.get("name", "") or self.name
        self.breed=pet_data.get("breed", "") or self.breed
        self.birthday=pet_data.get("birthday","") or self.birthday

        self.save()
        return True, None

class Speciality(Enum):
    Oftalmologia = "Oftalmologia"
    Quimioterapia = "Quimioterapia"
    Radiologia = "Radiologia"
    Ecocardiografias = "Ecocardiografias"
    Traumatologia = "Traumatologia"
    Ecografias = "Ecografias"
    Urgencias = "Urgencias"
    
    @classmethod
    def choices(cls):
        """
        Retorna una lista de tuplas con las opciones de especialidad.
        
        Returns:
            list: Una lista de tuplas con los nombres y valores de las especialidades.
        """
        return [(key.name, key.value) for key in cls]

class Vet(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    speciality = models.CharField(max_length=100, choices=Speciality.choices(), default=Speciality.Urgencias)

    def __str__(self):
        """
        Retorna una representación en string del veterinario, que es su nombre.
        """
        return self.name

    @classmethod
    def save_vet(cls, vet_data):
        """
        Guarda un nuevo veterinario en la base de datos.

        Args:
            vet_data (dict): Un diccionario con los datos del veterinario.

        Returns:
            tuple: Una tupla indicando si se guardó correctamente el veterinario y, en caso de errores, los mensajes de error.
        """
        errors = validate_vet(vet_data)

        if len(errors.keys()) > 0:
            return False, errors

        Vet.objects.create(
            name=vet_data.get("name"),
            email=vet_data.get("email"),
            phone=vet_data.get("phone"),
            speciality=vet_data.get("speciality", Speciality.Urgencias),
        )

        return True, None

    def update_vet(self, vet_data):
        """
        Actualiza los datos de un veterinario existente en la base de datos.

        Args:
            vet_data (dict): Un diccionario con los datos actualizados del veterinario.

        Returns:
            tuple: Una tupla indicando si se actualizó correctamente el veterinario y, en caso de errores, los mensajes de error.
        """
        errors = validate_vet(vet_data)

        if len(errors.keys()) > 0:
            return False, errors
        
        self.name = vet_data.get("name", "") or self.name
        self.email = vet_data.get("email", "") or self.email
        self.phone = vet_data.get("phone", "") or self.phone
        self.speciality = vet_data.get("speciality", "") or self.speciality
        self.save()
        return True, None
    