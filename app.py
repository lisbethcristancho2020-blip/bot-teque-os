import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Configuración de Whapi
WHAPI_TOKEN = "AtjlYXTeoEBseb4bVfuiAw0CdVa3D013"
WHAPI_URL = "https://gate.whapi.cloud/"

# Inventario y Precios de Tequeños
inventario = {
    "grande_queso": {"cantidad": 0, "precio": 20000, "nombre": "Grandes de Queso"},
    "grande_bocadillo": {"cantidad": 0, "precio": 20000, "nombre": "Grandes Queso c/ Bocadillo"},
    "grande_oregano": {"cantidad": 0, "precio": 20000, "nombre": "Grandes Queso c/ Orégano"},
    "grande_jamon": {"cantidad": 0, "precio": 22000, "nombre": "Grandes Jamón c/ Queso"},
    "grande_salchicha": {"cantidad": 0, "precio": 22000, "nombre": "Grandes Salchicha c/ Queso"},
    "grande_tocineta": {"cantidad": 0, "precio": 22000, "nombre": "Grandes Tocineta c/ Queso"},
    "mediano": {"cantidad": 0, "precio": 15000, "nombre": "Medianos (Cualquier sabor)"},
    "pasapalo_crudo": {"cantidad": 0, "precio": 70000, "nombre": "Pasapalos Crudos"},
    "pasapalo_frito": {"cantidad": 0, "precio": 75000, "nombre": "Pasapalos Fritos"}
}

def procesar_comando(texto):
    texto = texto.strip().lower()
    partes = texto.split()

    if not partes:
        return "Por favor envía un comando válido."

    comando = partes[0]

    # Consultar inventario y menú
    if comando == "inventario" or comando == "menu":
        respuesta = "📋 *MENÚ Y DISPONIBILIDAD DE TEQUEÑOS* 📋\n\n"
        
        respuesta += "🧀 *TEQUEÑOS GRANDES*\n"
        for key in ["grande_queso", "grande_bocadillo", "grande_oregano"]:
            respuesta += f"• {inventario[key]['nombre']}: {inventario[key]['precio']} Bs (Disp: {inventario[key]['cantidad']})\n"
            
        respuesta += "\n🥓 *TEQUEÑOS GRANDES ESPECIALES*\n"
        for key in ["grande_jamon", "grande_salchicha", "grande_tocineta"]:
            respuesta += f"• {inventario[key]['nombre']}: {inventario[key]['precio']} Bs (Disp: {inventario[key]['cantidad']})\n"
            
        respuesta += "\n🍘 *TEQUEÑOS MEDIANOS*\n"
        respuesta += f"• {inventario['mediano']['nombre']}: {inventario['mediano']['precio']} Bs (Disp: {inventario['mediano']['cantidad']})\n"
        
        respuesta += "\n🎉 *PASAPALOS (FIESTA)*\n"
        for key in ["pasapalo_crudo", "pasapalo_frito"]:
            respuesta += f"• {inventario[key]['nombre']}: {inventario[key]['precio']} Bs (Disp: {inventario[key]['cantidad']})\n"
            
        return respuesta

    # Modificar inventario (+ o -)
    elif comando in ["+", "-"] and len(partes) >= 3:
        try:
            cantidad = int(partes[1])
            codigo_sabor = partes[2]

            if codigo_sabor in inventario:
                if comando == "+":
                    inventario[codigo_sabor]["cantidad"] += cantidad
                    return f"✅ ¡Agregado! Ahora hay {inventario[codigo_sabor]['cantidad']} de {inventario[codigo_sabor]['nombre']}."
                elif comando == "-":
                    if inventario[codigo_sabor]["cantidad"] >= cantidad:
                        inventario[codigo_sabor]["cantidad"] -= cantidad
                        return f"🔻 Salida registrada. Quedan {inventario[codigo_sabor]['cantidad']} de {inventario[codigo_sabor]['nombre']}."
                    else:
                        return f"⚠️ Alerta: Solo quedan {inventario[codigo_sabor]['cantidad']} de {inventario[codigo_sabor]['nombre']}."
            else:
                return f"❌ El código '{codigo_sabor}' no existe. Revisa el menú para ver los códigos válidos."
        except ValueError:
            return "❌ La cantidad debe ser un número entero."

    else:
        return "🤖 *Comandos disponibles:*\n• `menu` o `inventario`\n• `+ [cant] [codigo]` (Ej: + 5 grande_queso)\n• `- [cant] [codigo]` (Ej: - 2 pasapalo_frito)"

@app.route('/', methods=['GET'])
def home():
    return "Bot de Inventario de Tequeños Activo"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if data and 'messages' in data:
        for message in data['messages']:
            if not message.get('from_me'):
                chat_id = message.get('chat_id')
                texto_recibido = message.get('text', {}).get('body', '')

                if texto_recibido:
                    respuesta = procesar_comando(texto_recibido)
                    enviar_mensaje_whapi(chat_id, respuesta)

    return jsonify({"status": "ok"}), 200

def enviar_mensaje_whapi(chat_id, texto):
    headers = {
        "Authorization": f"Bearer {WHAPI_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "to": chat_id,
        "body": texto
    }
    requests.post(WHAPI_URL, json=payload, headers=headers)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
