import os
import re
import json
from collections import defaultdict

REPO_PATH = "./SQLs"   # Ajusta a tu repo
OUTPUT_PATH = "index.json"  

def find_latest_versions(repo_path):
    objects = defaultdict(list)

    for root, _, files in os.walk(repo_path):
        for file in files:
            if ".sql_" in file:
                base, version = file.split(".sql_")
                objects[base].append((version, os.path.join(root, file)))

    latest = {}
    for obj, versions in objects.items():
        latest_version = sorted(versions, key=lambda x: x[0], reverse=True)[0]
        latest[obj] = {
            "version": latest_version[0],
            "path": latest_version[1]
        }

    return latest

def extract_metadata(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1️⃣ Eliminar comentarios
    content = re.sub(r"--.*?\n", " ", content)
    content = re.sub(r"/\*.*?\*/", " ", content, flags=re.DOTALL)

    tables = set()
    columns = set()
    select_blocks = []
    lineage = dict()

    # 2️⃣ Detectar tablas en INSERT / FROM / JOIN
    table_patterns = re.findall(r"(?:FROM|JOIN|INTO)\s+([A-Z0-9_]+)", content, re.IGNORECASE)
    for table in table_patterns:
        tables.add(table.upper())

    # 3️⃣ Detectar SELECT blocks robustos
    select_pattern = re.compile(
        r"SELECT\s+(.*?)\s+FROM\s+([A-Z0-9_,\s]+)",
        re.IGNORECASE | re.DOTALL
    )

    for match in select_pattern.finditer(content):
        cols_str = match.group(1)
        tables_in_select = [t.strip().upper() for t in match.group(2).split(",")]
        snippet = match.group(0).strip()[:400]

        col_list = []
        for col in cols_str.split(","):
            col = col.strip()
            col = re.sub(r"[\(\)]", "", col)              # eliminar paréntesis
            col = re.sub(r"(?i)\s+AS\s+\w+", "", col)    # eliminar alias
            col = col.split()[-1]                         # tomar último token
            if col:
                columns.add(col.upper())
                col_list.append(col.upper())

        # Guardamos el select block
        select_blocks.append({
            "tables": tables_in_select,
            "columns": col_list,
            "snippet": snippet
        })

        # Construimos lineage parcial
        for t in tables_in_select:
            if t not in lineage:
                lineage[t] = set()
            for c in col_list:
                lineage[t].add(c.upper())

    # 4️⃣ Intentar detectar columnas usadas en INSERT
    insert_pattern = re.compile(
        r"INSERT\s+INTO\s+([A-Z0-9_]+)\s*\((.*?)\)", re.IGNORECASE | re.DOTALL
    )
    for match in insert_pattern.finditer(content):
        table_name = match.group(1).upper()
        cols = match.group(2).split(",")
        for col in cols:
            col_name = col.strip().upper()
            if col_name:
                columns.add(col_name)
                if table_name not in lineage:
                    lineage[table_name] = set()
                lineage[table_name].add(col_name)

    # convertir lineage sets a listas
    lineage = {k: list(v) for k, v in lineage.items()}

    return {
        "tables": list(tables),
        "columns": list(columns),
        "select_blocks": select_blocks,
        "lineage": lineage
    }


def build_knowledge():
    latest_versions = find_latest_versions(REPO_PATH)

    knowledge = {
        "objects": {},
        "table_usage": defaultdict(list)
    }

    for obj, data in latest_versions.items():
        metadata = extract_metadata(data["path"])

        knowledge["objects"][obj] = {
            "type": "procedure",
            "latest_version": data["version"],
            "path": data["path"],
            "tables": metadata["tables"],
            "columns": metadata["columns"],
            "select_blocks": metadata["select_blocks"]
        }

        for table in metadata["tables"]:
            knowledge["table_usage"][table].append(obj)

    # convertir defaultdict
    knowledge["table_usage"] = dict(knowledge["table_usage"])

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(knowledge, f, indent=2)

    print("Knowledge index construido correctamente.")


if __name__ == "__main__":
    build_knowledge()
