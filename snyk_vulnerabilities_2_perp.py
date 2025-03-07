import requests
import json

# Configuración
snyk_api_token = ""
org_id = ""
snyk_api_url = "https://snyk.io/api/v1"  # Ajusta según la documentación de Snyk

# Encabezados para la autenticación
headers = {
    "Authorization": f"token {snyk_api_token}",
    "Content-Type": "application/json"
}

def obtener_proyectos(org_id):
    """Obtiene todos los proyectos de una organización."""
    # Ajusta el endpoint según la documentación de la API
    url = f"{snyk_api_url}/org/{org_id}/projects"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener proyectos: {response.text}")
        return []

def obtener_vulnerabilidades(proyecto_id):
    """Obtiene las vulnerabilidades de un proyecto."""
    # Ajusta el endpoint según la documentación de la API
    url = f"{snyk_api_url}/v1/reporting/issues?projectIds={proyecto_id}&groupBy=issue"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener vulnerabilidades: {response.text}")
        return []

def guardar_vulnerabilidades(proyecto_nombre, vulnerabilidades):
    """Guarda las vulnerabilidades en un archivo JSON."""
    with open(f"{proyecto_nombre}.json", "w") as archivo:
        json.dump(vulnerabilidades, archivo, indent=4)

def main():
    proyectos = obtener_proyectos(org_id)
    
    for proyecto in proyectos:
        proyecto_id = proyecto['id']
        proyecto_nombre = proyecto['name']
        
        vulnerabilidades = obtener_vulnerabilidades(proyecto_id)
        guardar_vulnerabilidades(proyecto_nombre, vulnerabilidades)
        
        print(f"Vulnerabilidades guardadas para {proyecto_nombre}")

if __name__ == "__main__":
    main()