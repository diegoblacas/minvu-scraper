from flask import Flask, jsonify
import requests

app = Flask(__name__)

def scrape_minvu():
    administradores = []
    total = 0
    pagina = 1

    try:
        while True:
            url = f"https://condominios-api.minvu.cl/administradores?page={pagina}&limit=100"

            response = requests.get(url, timeout=10)
            data = response.json()

            resultados = data.get("data", [])

            if not resultados:
                break

            for item in resultados:
                nombre = f"{item.get('Nombres','')} {item.get('ApellidoUno','')} {item.get('ApellidoDos','')}".strip()
                
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

@app.route('/scrape', methods=['GET', 'POST'])
def scrape():
    return jsonify(scrape_minvu())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
