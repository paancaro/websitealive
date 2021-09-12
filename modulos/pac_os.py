import toml

# Leer un archivo de configuracion tipo TOML (lo importa en diccionario python (Parecido a JSON))
def toml_leer_archivo(data):
    parsed = (toml.load(data))
    return parsed
