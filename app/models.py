from django.db import models
from enum import Enum
import datetime

def validate_client(data):
    """
    Validate client data and return a dictionary of errors for missing or invalid fields.

    This function checks for the presence of 'name', 'phone', and 'email' fields in the input data.
    It ensures that each field is not empty, and additionally checks that the 'email' field contains
    an '@' symbol to verify its validity.

    :param data: A dictionary containing client data with keys 'name', 'phone', and 'email'.
    :return: A dictionary containing error messages for each field that is missing or invalid.
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
    Valida que los datos del formulario para crear o editar proveedores no queden vacíos. Además de validar que el mail contenga el símbolo @.
    Retorna un diccionario con mensajes para los errores (o uno vacío si no hubiera).
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
    Valida que los datos del formulario para crear o editar medicamentos no queden vacíos. Además de validar que la dosis quede dentro del rango 1 - 10.
    Retorna un diccionario con mensajes para los errores (o uno vacío si no hubiera).
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
    elif not isinstance(dose, str) or not dose.isdigit():
        errors["dose"] = "La dosis debe ser un numero entero"
    elif not (num > 0 and num < 11):
        errors["dose"] = "La dosis debe estar entre 1 y 10"

    return errors
    
def validate_product(data):
    """
    Valida que los campos no queden vacíos y que el precio sea siempre positivo.
    Retorna un diccionario con mensajes para los errores (o uno vacío si no hubiera).
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
    Valida que los campos no queden vacíos y que la fecha sea menor a la fecha de hoy.
    Retorna un diccionario con mensajes para los errores (o uno vacío si no hubiera).
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
    Valida que los campos no queden vacíos y que el email contenga el @
    Retorna un diccionario con mensajes para los errores (o uno vacío si no hubiera).
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
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def save_client(cls, client_data):
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
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=200)

    def __str__(self):
            return self.name
    
    @classmethod
    def save_provider(cls, provider_data):
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
        return self.name

    @classmethod
    def save_medicine(cls, medicine_data):
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
        return self.name
    
    @classmethod
    def save_product(cls, product_data):
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
        return self.name
    
    @classmethod
    def save_pet(cls, pet_data):
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
        return [(key.name, key.value) for key in cls]

class Vet(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    speciality = models.CharField(max_length=100, choices=Speciality.choices(), default=Speciality.Urgencias)

    def __str__(self):
        return self.name

    @classmethod
    def save_vet(cls, vet_data):
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
        errors = validate_vet(vet_data)

        if len(errors.keys()) > 0:
            return False, errors
        
        self.name = vet_data.get("name", "") or self.name
        self.email = vet_data.get("email", "") or self.email
        self.phone = vet_data.get("phone", "") or self.phone
        self.speciality = vet_data.get("speciality", "") or self.speciality
        self.save()
        return True, None
    