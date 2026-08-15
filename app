# Diccionario con los productos y sus precios en pesos colombianos (COP)
precios_tequenos = {
    # Medianos (15.000)
    "mediano_queso": 15000,
    "mediano_jamon": 15000,
    
    # Grandes Grupo A (20.000)
    "grande_queso": 20000,
    "grande_bocadillo": 20000,
    "grande_oregano": 20000,
    
    # Grandes Grupo B (22.000)
    "grande_salchicha": 22000,
    "grande_tocineta": 22000,
    "grande_jamon": 22000,
}
from flask import Flask, request, jsonify

app = Flask(__name__)

# 1. Tu inventario inicial (en ceros para que lo vayan llenando)
inventario_tequenos = {
    "mediano_queso": 0,
    "mediano_jamon": 0,
    "grande_queso": 0,
    "grande_bocadillo": 0,
    "grande_oregano": 0,
    "grande_salchicha": 0,
    "grande_tocineta": 0,
    "grande_jamon": 0,
}

# 2. Función que procesa los comandos que llegan por WhatsApp
def procesar_comando(mensaje):
    mensaje = mensaje.lower().strip()
    partes = mensaje.split()
    
    if not partes:
        return "Escribe un comando válido."
    
    comando = partes[0]
    
    # Ver inventario
    if comando in ["inventario", "ver"]:
        respuesta = "📦 *Inventario Actual de Tequeños*:\n"
        for sabor, cantidad in inventario_tequenos.items():
            respuesta += f"- {sabor}: {cantidad}\n"
        return respuesta
    
    # Modificar inventario (+ o -)
    elif comando in ["+", "-"] and len(partes) >= 3:
        try:
            cantidad = int(partes[1])
            sabor = partes[2]
            
            if sabor in inventario_tequenos:
                if comando == "+":
                    inventario_tequenos[sabor] += cantidad
                    return f"✅ ¡Agregado! Ahora hay {inventario_tequenos[sabor]} bandejas de {sabor}."
                elif comando == "-":
                    if inventario_tequenos[sabor] >= cantidad:
                        inventario_tequenos[sabor] -= cantidad
                        return f"🔻 Salida registrada. Quedan {inventario_tequenos[sabor]} bandejas de {sabor}."
                    else:
                        return f"⚠️ Alerta: Solo quedan {inventario_tequenos[sabor]} bandejas de {sabor}."
            else:
                return f"❌ El sabor '{sabor}' no existe. Revisa el nombre."
        except ValueError:
            return "❌ La cantidad debe ser un número."
            
    else:
        return "🤖 Comandos disponibles:\n- `inventario`\n- `+ [cant] [sabor]`\n- `- [cant] [sabor]`"

# 3. La ruta (Webhook) que recibe los mensajes que manda Green API
@app.route("/webhook", methods=["POST"])
def webhook_whatsapp():
    data = request.json
    
    # Verificamos si es un mensaje de texto entrante de WhatsApp
    try:
        if data.get("typeWebhook") == "incomingMessageReceived":
            mensaje_texto = data["messageData"]["textMessageData"]["textMessage"]
            chat_id = data["senderData"]["chatId"]
            
            # Procesamos el mensaje con nuestra lógica
            respuesta_texto = procesar_comando(mensaje_texto)
            
            # Aquí es donde Green API mandaría la respuesta de vuelta al chat de tu mamá
            # (Más adelante configuramos la llamada para enviar el mensaje de respuesta)
            print(f"Mensaje de {chat_id}: {mensaje_texto}")
            print(f"Respuesta generada: {respuesta_texto}")
            
    except Exception as e:
        print("Error procesando webhook:", e)
        
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(port=5000)
