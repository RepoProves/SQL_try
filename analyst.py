import json
import os

INDEX_PATH = "index.json"
CHANGE_REQUEST_PATH = "change_request.json"
OUTPUT_MANIFEST = "impact_manifest.json"

# 1️⃣ Cargar Knowledge Layer
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    knowledge = json.load(f)

def load_change_request(path):
    if not os.path.exists(path):
        print(f"Error: {path} no encontrado.")
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def analyze_change(change):
    """
    Recibe dict con 'table' y opcional 'columns'
    """
    impacted_objects = []

    table = change.get("table", "").upper()
    if not table:
        print("No se especificó tabla en change_request.")
        return impacted_objects

    columns_to_check = [c.upper() for c in change.get("columns", [])]

    for obj_name, obj_data in knowledge["objects"].items():
        lineage = obj_data.get("lineage", {})
        if table in lineage:
            impacted_columns = []
            if columns_to_check:
                for col in columns_to_check:
                    if col in lineage[table]:
                        impacted_columns.append(col)
            else:
                impacted_columns = lineage[table]

            if impacted_columns:
                impacted_objects.append({
                    "object": obj_name,
                    "path": obj_data["path"],
                    "table": table,
                    "columns": impacted_columns,
                    "select_blocks": obj_data["select_blocks"]
                })

    return impacted_objects

def save_manifest(impacts):
    with open(OUTPUT_MANIFEST, "w", encoding="utf-8") as f:
        json.dump(impacts, f, indent=2)
    print(f"Manifest de impacto generado en {OUTPUT_MANIFEST}")

# 🟢 EJECUCIÓN
if __name__ == "__main__":
    change_request = load_change_request(CHANGE_REQUEST_PATH)
    if change_request:
        impacts = analyze_change(change_request)
        save_manifest(impacts)

        if impacts:
            print("Objetos impactados:")
            for obj in impacts:
                print(f"- {obj['object']} -> {obj['columns']}")
        else:
            print("No se detectaron objetos impactados.")