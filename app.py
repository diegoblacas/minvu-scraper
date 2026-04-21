from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

def scrape_minvu(max_paginas=3):
    administradores = []
    total = 0
    pagina = 1

    try:
        while pagina <= max_paginas:
            url = f"https://condominios-api.minvu.cl/administradores?page={pagina}&limit=100&select=Rut&select=Nombres&select=ApellidoUno&select=ApellidoDos&select=Tipo&select=Estado&select=RegionesPrestacionServicio"

            response = requests.get(url, timeout=10)
            print("🔥 PRIMEROS 1000 CARACTERES:")
            print(response.text[:1000])
            data = response.json()

            # 🔥 CLAVE: usar "content" en vez de "data"
            resultados = data.get("content", [])

            if not resultados:
                break

            for item in resultados:
                nombre = " ".join(filter(None, [
                    item.get("Nombres"),
                    item.get("ApellidoUno"),
                    item.get("ApellidoDos")
                ]))

                administradores.append({
                    "nombre": nombre,
                    "rut": item.get("Rut"),
                    "tipo": item.get("Tipo"),
                    "estado": item.get("Estado"),
                    "regiones": item.get("RegionesPrestacionServicio")
                })

                total += 1

            pagina += 1

    except Exception as e:
        return {
            "error": str(e),
            "administradores": administradores,
            "total_registros": total,
            "paginas_procesadas": pagina,
            "success": False
        }

    return {
        "administradores": administradores,
        "total_registros": total,
        "paginas_procesadas": pagina - 1,
        "success": True
    }

@app.route('/scrape', methods=['GET'])
def scrape():
    max_paginas = int(request.args.get("paginas", 3))
    return jsonify(scrape_minvu(max_paginas))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
