from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

def scrape_minvu(max_paginas=3):
    administradores = []
    total = 0
    pagina = 1

    try:
        while pagina <= max_paginas:
            url = f"https://condominios-api.minvu.cl/administradores?page={pagina}&limit=100"

            headers = {
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json"
            }

            response = requests.get(url, headers=headers, timeout=10)
            data = response.json()

            # ✅ CLAVE REAL
            resultados = data.get("data", [])

            if not resultados:
                break

            for item in resultados:
                administradores.append({
                    "nombre": item.get("nombre_completo"),
                    "rut": item.get("rut"),
                    "tipo": item.get("tipo"),
                    "estado": item.get("estado_vigencia"),
                    "regiones": item.get("regiones_prestacion_servicio"),
                    "email": item.get("email")
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
