from django.urls import reverse

links = [
    {"label": "Home", "href": reverse("home"), "icon": "bi bi-house-door"},
    {"label": "Clientes", "href": reverse("clients_repo"), "icon": "bi bi-people"},
    {"label": "Proveedores", "href": reverse("providers_repo"), "icon": "bi bi-people"},
    {"label": "Productos", "href": reverse("products_repo"), "icon": "bi bi-basket3"},
    {"label": "Medicinas", "href": reverse("medicine_repo"), "icon": "bi bi-capsule"},
    {"label": "Mascotas", "href": reverse("pets_repo"), "icon": "bi bi-github"},
    {"label": "Veterinarios", "href": reverse("vets_repo"), "icon": "bi bi-people"},
]


def navbar(request):
    """
    Generate a dictionary with links and their active status based on the request path.

    This function takes a Django HttpRequest object and generates a dictionary
    where each link in `links` is checked against the request path to determine
    if it should be marked as active. The active status is added to the link's
    dictionary.

    :param request: The HttpRequest object containing metadata about the request.
    :return: A dictionary containing the links with their active status.
    """
    def add_active(link):
        """
        Add an 'active' key to the link dictionary based on the request path.

        This helper function creates a copy of the link dictionary and determines
        if the link should be marked as active based on whether the request path
        matches or starts with the link's href.

        :param link: A dictionary representing a link with at least an 'href' key.
        :return: A copy of the link dictionary with an added 'active' key.
        """
        copy = link.copy()

        if copy["href"] == "/":
            copy["active"] = request.path == "/"
        else:
            copy["active"] = request.path.startswith(copy.get("href", ""))

        return copy

    return {"links": map(add_active, links)}