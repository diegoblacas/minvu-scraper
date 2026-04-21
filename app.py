from flask import Flask, jsonify
from playwright.async_api import async_playwright
import asyncio
import re

app = Flask(__name__)

async def scrape_minvu():
    administradores_santiago = []
    total_encontrados = 0
    paginas_procesadas = 0
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
    headless=True,
    args=["--no-sandbox", "--disable-setuid-sandbox"]
)
            page = await browser.new_page()
            await page.goto("https://condominios.minvu.cl/", wait_until="networkidle", timeout=30000)
            paginas_procesadas = 1
            
            # Espera tabla
            await page.wait_for_selector("table", timeout=10000)
            content = await page.content()
            
            # Extrae datos del HTML
            rows = re.findall(r'<tr[^>]*>(.*?)</tr>', content, re.DOTALL)
            
            for row in rows:
                cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
                if len(cells) >= 3:
                    nombre = re.sub(r'<[^>]+>', '', cells[0]).strip()
                    correo = re.sub(r'<[^>]+>', '', cells[1]).strip()
                    region = re.sub(r'<[^>]+>', '', cells[2]).strip()
                    
                    total_encontrados += 1
                    
                    if "SANTIAGO" in region.upper():
                        administradores_santiago.append({
                            "nombre": nombre,
                            "correo": correo,
                            "region": region
                        })
            
            await browser.close()
    except Exception as e:
        return {"error": str(e), "success": False}
    
    return {
        "administradores_santiago": administradores_santiago,
        "total_encontrados": total_encontrados,
        "total_filtrados": len(administradores_santiago),
        "paginas_procesadas": paginas_procesadas,
        "success": True
    }

@app.route('/scrape', methods=['GET'])
def scrape():
    resultado = asyncio.run(scrape_minvu())
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
