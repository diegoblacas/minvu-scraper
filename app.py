from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_minvu():
    administradores = []
    total_encontrados = 0
    paginas_procesadas = 0

    try:
        url = "https://condominios.minvu.cl/"
        
        while True:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            paginas_procesadas += 1

            table = soup.find("table")
            if not table:
                break

            rows = table.find_all("tr")

            for row in rows:
                cells = row.find_all("td")
                if len(cells) >= 3:
                    nombre = cells[0].get_text(strip=True)
                    correo = cells[1].get_text(strip=True)
                    region = cells[2].get_text(strip=True)

                    total_encontrados += 1

                    administradores.append({
                        "nombre": nombre,
                        "correo": correo,
                        "region": region
                    })

            # Buscar link "Siguiente"
            siguiente = soup.find("a", string=lambda x: x and "Siguiente" in x)

            if siguiente and siguiente.get("href"):
                url = "https://condominios.minvu.cl" + siguiente.get("href")
            else:
                break

    except Exception as e:
        return {
            "error": str(e),
            "administradores": administradores,
            "total_procesados": total_encontrados,
            "total_registros": len(administradores),
            "paginas_procesadas": paginas_procesadas,
            "success": False
        }

    return {
        "administradores": administradores,
        "total_procesados": total_encontrados,
        "total_registros": len(administradores),
        "paginas_procesadas": paginas_procesadas,
        "success": True
    }

@app.route('/scrape', methods=['GET', 'POST'])
def scrape():
    return jsonify(scrape_minvu())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
