import streamlit as st
import pandas as pd
from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ============================================
# 🔧 CONFIGURACIÓN - CAMBIA ESTOS 4 VALORES
# ============================================

# 1. Tu correo electrónico (el que enviará las notificaciones)
EMAIL_REMITENTE = "tuemail@gmail.com"

# 2. Tu contraseña (si es Gmail, necesitas una "Contraseña de aplicación")
EMAIL_CONTRASENA = "tucontraseña"

# 3. Tu correo de destino (donde quieres recibir las alertas)
EMAIL_DESTINO = "tucorreo@ejemplo.com"

# 4. Cambia la contraseña del panel de admin si quieres
CONTRASENA_ADMIN = "tupassword123"

# ============================================
# 📧 FUNCIÓN PARA ENVIAR EMAIL
# ============================================

def enviar_email(asunto, mensaje_html):
    """Envía un correo electrónico con el pedido"""
    try:
        # Crear el mensaje
        msg = MIMEMultipart()
        msg["From"] = EMAIL_REMITENTE
        msg["To"] = EMAIL_DESTINO
        msg["Subject"] = asunto
        
        # Cuerpo del mensaje en HTML
        msg.attach(MIMEText(mensaje_html, "html"))
        
        # Conectar al servidor de Gmail
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_REMITENTE, EMAIL_CONTRASENA)
        
        # Enviar
        server.send_message(msg)
        server.quit()
        return True
        
    except Exception as e:
        print(f"Error al enviar email: {e}")
        return False

# ============================================
# 🎨 INTERFAZ DE LA APP
# ============================================

# Configuración de la página
st.set_page_config(page_title="Mi negocio de comidas", layout="centered")

# Título
st.title("🍽️ Mi negocio de comidas")
st.subheader("Desayunos, comidas y cenas caseras")

# --- Menú (cambia los platos y precios aquí) ---
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
    hora_entrega = st.selectbox("Franja horaria", [
        "Desayuno (8-10h)", 
        "Comida (13-15h)", 
        "Cena (20-22h)"
    ])
    
    enviado = st.form_submit_button("📞 Hacer pedido")

# ============================================
# 💾 GUARDAR PEDIDO Y ENVIAR NOTIFICACIÓN
# ============================================

if enviado:
    if nombre and direccion and telefono:
        # Calcular total
        total = menu[opcion] * cantidad
        
        # Crear diccionario con el pedido
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
        
        # Guardar en archivo CSV
        archivo_pedidos = "pedidos.csv"
        df_nuevo = pd.DataFrame([pedido])
        
        if os.path.exists(archivo_pedidos):
            df_existente = pd.read_csv(archivo_pedidos)
            df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)
        else:
            df_final = df_nuevo
        
        df_final.to_csv(archivo_pedidos, index=False)
        
        # ========================================
        # 📧 ENVIAR NOTIFICACIÓN POR EMAIL
        # ========================================
        
        # Crear mensaje HTML bonito
        mensaje_html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .pedido {{ background-color: #f9f9f9; padding: 15px; border-radius: 10px; }}
                h2 {{ color: #FF6B35; }}
                .total {{ font-size: 18px; font-weight: bold; color: #2E7D32; }}
            </style>
        </head>
        <body>
            <h2>🍽️ ¡NUEVO PEDIDO!</h2>
            <div class="pedido">
                <p><strong>👤 Cliente:</strong> {nombre}</p>
                <p><strong>📍 Dirección:</strong> {direccion}</p>
                <p><strong>📞 Teléfono:</strong> {telefono}</p>
                <p><strong>🍲 Producto:</strong> {opcion}</p>
                <p><strong>🔢 Cantidad:</strong> {cantidad}</p>
                <p class="total"><strong>💰 Total:</strong> {total:.2f} €</p>
                <p><strong>📅 Fecha de entrega:</strong> {fecha_entrega.strftime('%d/%m/%Y')}</p>
                <p><strong>⏰ Franja horaria:</strong> {hora_entrega}</p>
                <hr>
                <p><strong>🕐 Pedido realizado:</strong> {datetime.now().strftime('%H:%M:%S')}</p>
            </div>
            <p><em>Este pedido se ha guardado automáticamente. Revisa tu panel de administración.</em></p>
        </body>
        </html>
        """
        
        asunto = f"🍽️ NUEVO PEDIDO - {nombre} - {total:.2f}€"
        
        # Enviar el email
        email_enviado = enviar_email(asunto, mensaje_html)
        
        # Mostrar mensaje de éxito en la app
        if email_enviado:
            st.success(f"✅ ¡Pedido recibido! Total: {total:.2f} €")
            st.info("📧 Se ha enviado una notificación a tu correo. Te llamaré en los próximos minutos para confirmar.")
        else:
            st.success(f"✅ ¡Pedido recibido! Total: {total:.2f} €")
            st.warning("⚠️ No se pudo enviar la notificación por email, pero el pedido quedó guardado. Revisa tu panel de admin.")
            
    else:
        st.error("❌ Por favor, rellena todos los campos (nombre, dirección y teléfono)")

# ============================================
# 🔒 PANEL DE ADMINISTRACIÓN (SOLO PARA TI)
# ============================================

st.header("🔒 Panel de administración")
contrasena = st.text_input("Contraseña", type="password")

if contrasena == CONTRASENA_ADMIN:
    st.subheader("📊 Gestión de pedidos")
    
    if os.path.exists("pedidos.csv"):
        pedidos_df = pd.read_csv("pedidos.csv")
        
        # Mostrar estadísticas
        col1, col2, col3 = st.columns(3)
        col1.metric("Total de pedidos", len(pedidos_df))
        col2.metric("Ingresos totales", f"{pedidos_df['total'].sum():.2f} €")
        col3.metric("Pedido promedio", f"{pedidos_df['total'].mean():.2f} €")
        
        st.divider()
        
        # Mostrar tabla de pedidos
        st.write("### 📋 Lista de pedidos")
        st.dataframe(pedidos_df, use_container_width=True)
        
        # Botón para descargar
        with open("pedidos.csv", "rb") as file:
            st.download_button(
                label="📥 Descargar todos los pedidos (CSV)",
                data=file,
                file_name=f"pedidos_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
            
        # Opción para eliminar pedidos antiguos
        st.divider()
        with st.expander("🗑️ Eliminar pedidos antiguos"):
            dias = st.number_input("Eliminar pedidos de hace más de X días", min_value=1, max_value=365, value=30)
            if st.button("Eliminar pedidos antiguos"):
                fecha_limite = datetime.now() - pd.Timedelta(days=dias)
                pedidos_df['fecha_pedido'] = pd.to_datetime(pedidos_df['fecha_pedido'])
                pedidos_nuevos = pedidos_df[pedidos_df['fecha_pedido'] > fecha_limite]
                pedidos_nuevos.to_csv("pedidos.csv", index=False)
                st.success(f"Se eliminaron {len(pedidos_df) - len(pedidos_nuevos)} pedidos antiguos")
                st.rerun()
                
    else:
        st.info("📭 Todavía no hay pedidos. ¡Comparte tu app para empezar a recibir!")
        
elif contrasena:
    st.warning("🔑 Contraseña incorrecta")