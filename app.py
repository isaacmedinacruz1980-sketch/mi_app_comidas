import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- Configuración de la página ---
st.set_page_config(page_title="Mi negocio de comidas", layout="centered")

# --- Título y descripción ---
st.title("🍽️ Mi negocio de comidas")
st.subheader("Desayunos, comidas y cenas caseras")

# --- Menú (cambia los precios aquí si quieres) ---
st.header("📋 Menú del día")

menu = {
    "🥐 Desayuno (café + tostada o bollería)": 4.50,
    "🥗 Comida (primer + segundo + postre + bebida)": 9.90,
    "🍲 Cena menú ligero (crema + pescado o pollo + fruta)": 8.50
}

for producto, precio in menu.items():
    st.write(f"**{producto}** - {precio:.2f} €")

# --- Formulario de pedido ---
st.header("🛍️ Hacer un pedido")

with st.form("pedido_form"):
    nombre = st.text_input("Tu nombre")
    direccion = st.text_input("Dirección de entrega")
    telefono = st.text_input("Teléfono (para confirmar el pedido)")
    
    opcion = st.selectbox("¿Qué quieres pedir?", list(menu.keys()))
    cantidad = st.number_input("Cantidad", min_value=1, max_value=10, value=1)
    
    fecha_entrega = st.date_input("¿Para qué día lo quieres?")
    hora_entrega = st.selectbox("Franja horaria", ["Desayuno (8-10h)", "Comida (13-15h)", "Cena (20-22h)"])
    
    enviado = st.form_submit_button("📞 Hacer pedido")

# --- Guardar el pedido cuando se envía ---
if enviado:
    if nombre and direccion and telefono:
        total = menu[opcion] * cantidad
        
        pedido = {
            "fecha_pedido": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nombre": nombre,
            "direccion": direccion,
            "telefono": telefono,
            "producto": opcion,
            "cantidad": cantidad,
            "total": total,
            "fecha_entrega": fecha_entrega.strftime("%Y-%m-%d"),
            "hora_entrega": hora_entrega
        }
        
        archivo_pedidos = "pedidos.csv"
        df_nuevo = pd.DataFrame([pedido])
        
        if os.path.exists(archivo_pedidos):
            df_existente = pd.read_csv(archivo_pedidos)
            df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)
        else:
            df_final = df_nuevo
        
        df_final.to_csv(archivo_pedidos, index=False)
        
        st.success(f"✅ ¡Pedido recibido! Total: {total:.2f} €")
        st.info("Te llamaré en los próximos minutos para confirmar y darte las instrucciones de pago.")
    else:
        st.error("❌ Por favor, rellena todos los campos (nombre, dirección y teléfono)")

# --- Panel secreto solo para ti ---
st.header("🔒 Panel de pedidos (solo para mí)")
contrasena = st.text_input("Contraseña", type="password")

if contrasena == "tupassword123":
    if os.path.exists("pedidos.csv"):
        pedidos_df = pd.read_csv("pedidos.csv")
        st.write(f"**Total de pedidos:** {len(pedidos_df)}")
        st.dataframe(pedidos_df)
        
        with open("pedidos.csv", "rb") as file:
            st.download_button(
                label="📥 Descargar todos los pedidos",
                data=file,
                file_name="mis_pedidos.csv",
                mime="text/csv"
            )
    else:
        st.info("Todavía no hay pedidos. ¡A promocionar!")
else:
    if contrasena:
        st.warning("Contraseña incorrecta")