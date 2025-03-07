import requests
import json
import os

# Configuración
SNYK_API_TOKEN = ""  # Reemplaza con tu token de Snyk
ORG_ID = ""  # Reemplaza con el ID de tu organización en Snyk
BASE_URL = "https://api.snyk.io/rest"

HEADERS = {
    "Authorization": f"token {SNYK_API_TOKEN}",
    "Content-Type": "application/json"
}
# Carpeta para guardar JSON
OUTPUT_FOLDER = "snyk_vulnerabilities"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# 1️⃣ Obtener la lista de proyectos de la organización
def get_projects():
    url = f"{BASE_URL}/org/{ORG_ID}/projects"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json().get("projects", [])
    elif response.status_code == 404:
        print("🚨 Error 404: La organización no existe o el endpoint es incorrecto.")
    elif response.status_code == 401:
        print("🚨 Error 401: Token inválido o sin permisos.")
    else:
        print(f"Error al obtener proyectos: {response.status_code} - {response.text}")
    
    return []

# 2️⃣ Obtener las vulnerabilidades de un proyecto
def get_project_vulnerabilities(project_id):
    url = f"{BASE_URL}/org/{ORG_ID}/project/{project_id}/issues"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        print(f"🚨 Proyecto {project_id} no encontrado.")
    elif response.status_code == 401:
        print("🚨 Error 401: Token inválido o sin permisos.")
    else:
        print(f"Error {response.status_code} al obtener vulnerabilidades: {response.text}")
    
    return {}

# 3️⃣ Procesar proyectos y guardar resultados
def main():
    projects = get_projects()

    if not projects:
        print("❌ No se encontraron proyectos. Verifica el ORG_ID y el token.")
        return

    for project in projects:
        project_id = project.get("id")
        project_name = project.get("name", "unknown_project").replace(" ", "_")
        print(f"🔍 Obteniendo vulnerabilidades para: {project_name} ({project_id})")

        vulnerabilities = get_project_vulnerabilities(project_id)

        # Guardar JSON
        output_file = os.path.join(OUTPUT_FOLDER, f"{project_name}.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(vulnerabilities, f, indent=4)

        print(f"✅ Guardado: {output_file}")

if __name__ == "__main__":
    main()