import json
import subprocess
import os

# Requerimientos: openai (pip install openai) o cualquier GPT API
import openai

# Paths
CHANGE_REQUEST_PATH = "change_request.json"
ANALYST_SCRIPT = "analyst.py"
INDEX_PATH = "index.json"

# Configurar tu API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_user_for_description():
    print("==== Boss Agent ====")
    description = input("Describe el cambio funcional (en lenguaje natural): ").strip()
    return description

def suggest_change_request(description):
    """
    Usa IA generativa para sugerir tabla y columnas afectadas
    """
    prompt = f"""
Tienes un Knowledge Layer con las tablas y columnas de un proyecto Data Oracle.
A partir de esta descripción funcional:
\"\"\"{description}\"\"\"
Sugiere la tabla y columnas afectadas en el siguiente formato JSON:
{{"table": "...", "columns": ["...", "..."]}}
Usa mayúsculas exactas para los nombres.
Si no puedes inferir columnas exactas, deja la lista vacía.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    # Extraer el JSON de la respuesta de GPT
    try:
        text = response['choices'][0]['message']['content']
        # intentar cargar JSON directamente
        change_request = json.loads(text)
    except Exception as e:
        print("No se pudo parsear la respuesta de GPT, usando fallback vacío:", e)
        change_request = {"table": "", "columns": []}

    return change_request

def save_change_request(change_request):
    with open(CHANGE_REQUEST_PATH, "w", encoding="utf-8") as f:
        json.dump(change_request, f, indent=2)
    print(f"Change request guardado en {CHANGE_REQUEST_PATH}")

def run_analyst():
    if not os.path.exists(ANALYST_SCRIPT):
        print(f"Error: {ANALYST_SCRIPT} no encontrado.")
        return False
    result = subprocess.run(["python", ANALYST_SCRIPT], capture_output=True, text=True)
    print(result.stdout)
    return result.returncode == 0

def main():
    description = ask_user_for_description()
    change_request = suggest_change_request(description)

    if not change_request.get("table"):
        print("No se pudo inferir la tabla afectada. Por favor verifica manualmente.")
        return

    save_change_request(change_request)
    print("\nEjecutando Analyst Agent para analizar impactos...\n")
    success = run_analyst()

    if success:
        print("\n=== Manifest de impacto listo ===")
        manifest_path = "impact_manifest.json"
        if os.path.exists(manifest_path):
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = json.load(f)
            if not manifest:
                print("No se detectaron objetos impactados.")
            else:
                for obj in manifest:
                    print(f"- Procedimiento: {obj['object']}")
                    print(f"  Tabla: {obj['table']}")
                    print(f"  Columnas: {', '.join(obj['columns'])}")
                    print("  ---")
        else:
            print("No se encontró el manifest generado.")
    else:
        print("Hubo un problema ejecutando el Analyst.")

if __name__ == "__main__":
    main()
