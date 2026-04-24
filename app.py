import streamlit as st
import pandas as pd
from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ============================================
# 🔧 CONFIGURACIÓN - ¡CAMBIAME ESTOS VALORES!
# ============================================

# ----- TUS DATOS BANCARIOS (para que te paguen) -----
TU_NOMBRE = "Isaac Medina Cruz"                    # Tu nombre completo
TU_IBAN = "ES16 0182 5342 7702 0133 2852"        # Tu número de cuenta (IBAN)
TU_BANCO = "BBVA"                                 # Tu banco: BBVA, Santander, CaixaBank, etc.

# ----- CONFIGURACIÓN DE EMAIL (para recibir notificaciones) -----
EMAIL_REMITENTE = "isaacmedinacruz1980@gmail.com"           # Tu correo (el que envía las alertas)
EMAIL_CONTRASENA = "skoj rvjb xdrf aymi"                 # Contraseña (si es Gmail, usa contraseña de app)
EMAIL_DESTINO = "isaacmedinacruz1980@gmail.com"            # Dónde quieres recibir los avisos (puede ser el mismo)

# ----- CONTRASEÑA PARA VER EL PANEL DE ADMIN -----
CONTRASENA_ADMIN = "admin123"                     # Cámbiala por una que recuerdes

# ----- INFORMACIÓN DE TU NEGOCIO -----
NOMBRE_NEGOCIO = "Comidas BA GANDO"
TELEFONO_CONTACTO = "640765025"
HORARIO_ENTREGA = "De lunes a viernes de 9:00 a 21:00"

# ============================================
# 📧 FUNCIÓN PARA ENVIAR CORREOS
# ============================================

def enviar_email(asunto, mensaje_html, destinatario=None):
    """Envía un correo electrónico"""
    try:
        para = destinatario if destinatario else EMAIL_DESTINO
        
        msg = MIMEMultipart()
        msg["From"] = EMAIL_REMITENTE
        msg["To"] = para
        msg["Subject"] = asunto
        msg.attach(MIMEText(mensaje_html, "html"))
        
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_REMITENTE, EMAIL_CONTRASENA)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Error al enviar email: {e}")
        return False

# ============================================
# 🎨 INTERFAZ PRINCIPAL DE LA APP
# ============================================

st.set_page_config(page_title=NOMBRE_NEGOCIO, layout="centered")

# Barra lateral con información
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1046/1046784.png", width=80)
    st.markdown(f"## {NOMBRE_NEGOCIO}")
    st.markdown(f"📞 {TELEFONO_CONTACTO}")
    st.markdown(f"⏰ {HORARIO_ENTREGA}")
    st.divider()
    st.caption("Pagos por transferencia bancaria")
    st.caption("Sin comisiones para ti")

# Título principal
st.title("🍽️ " + NOMBRE_NEGOCIO)
st.subheader("Desayunos, comidas y cenas caseras")
st.markdown("💚 **Hecho con ingredientes frescos y mucho cariño**")

# --- MENÚ DE COMIDAS ---
st.header("📋 Nuestro menú de hoy")

menu = {
    "🥐 Desayuno (café + tostada o bollería)": 4.50,
    "🥗 Comida (primer plato + segundo + postre + bebida)": 9.90,
    "🍲 Cena menú ligero (crema + pescado/pollo + fruta)": 8.50,
    "🥪 Bocadillo para llevar": 5.50,
    "🍝 Plato combinado (ensalada + pasta o arroz)": 7.90
}

for producto, precio in menu.items():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**{producto}**")
    with col2:
        st.markdown(f"**{precio:.2f} €**")

st.divider()

# --- FORMULARIO DE PEDIDO ---
st.header("🛍️ Hacer un pedido")

with st.form("formulario_pedido"):
    nombre = st.text_input("Tu nombre completo *")
    direccion = st.text_input("Dirección de entrega *")
    telefono = st.text_input("Teléfono de contacto *")
    email_cliente = st.text_input("Correo electrónico (opcional, para confirmación)")
    
    col1, col2 = st.columns(2)
    with col1:
        opcion = st.selectbox("¿Qué quieres comer?", list(menu.keys()))
    with col2:
        cantidad = st.number_input("Cantidad", min_value=1, max_value=10, value=1)
    
    col1, col2 = st.columns(2)
    with col1:
        fecha_entrega = st.date_input("¿Para qué día lo quieres?")
    with col2:
        hora_entrega = st.selectbox("Franja horaria", [
            "Desayuno (8:00 - 10:00)", 
            "Comida (13:00 - 15:00)", 
            "Cena (20:00 - 22:00)"
        ])
    
    instrucciones = st.text_area("Instrucciones especiales (alergias, timbre, etc.)", placeholder="Ej: sin cebolla, tocar el timbre 2 veces...")
    
    enviado = st.form_submit_button("📞 Continuar con el pedido", use_container_width=True)

# ============================================
# 💰 PROCESAR EL PEDIDO
# ============================================

if enviado:
    if not nombre or not direccion or not telefono:
        st.error("❌ Por favor, rellena los campos obligatorios: nombre, dirección y teléfono")
    else:
        # Calcular total
        total = menu[opcion] * cantidad
        
        # Generar número de pedido único
        num_pedido = f"PED-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Guardar pedido en session_state
        st.session_state["pedido_actual"] = {
            "num_pedido": num_pedido,
            "nombre": nombre,
            "direccion": direccion,
            "telefono": telefono,
            "email": email_cliente,
            "producto": opcion,
            "cantidad": cantidad,
            "total": total,
            "fecha_entrega": fecha_entrega,
            "hora_entrega": hora_entrega,
            "instrucciones": instrucciones,
            "estado": "pendiente_pago"
        }
        
        # Mostrar resumen
        st.success(f"✅ Pedido #{num_pedido} creado correctamente", icon="✅")
        
        st.subheader("📝 Resumen de tu pedido")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Producto:** {opcion}")
            st.markdown(f"**Cantidad:** {cantidad}")
            st.markdown(f"**Total:** {total:.2f} €")
        with col2:
            st.markdown(f"**Entrega:** {fecha_entrega.strftime('%d/%m/%Y')}")
            st.markdown(f"**Hora:** {hora_entrega}")
            st.markdown(f"**Pedido #:** {num_pedido}")
        
        if instrucciones:
            st.info(f"📝 Notas: {instrucciones}")
        
        st.divider()
        
        # ========================================
        # 💳 DATOS BANCARIOS PARA EL PAGO
        # ========================================
        
        st.subheader("💰 Datos para realizar la transferencia")
        
        # Mostrar los datos bancarios de forma clara
        st.markdown(f"""
        <div style="background-color: #e8f4e8; padding: 15px; border-radius: 10px; margin: 10px 0;">
            <h4 style="color: #2E7D32; margin: 0;">🏦 Realiza una transferencia con estos datos:</h4>
            <table style="width: 100%; margin-top: 10px;">
                <tr><td><strong>Beneficiario:</strong></td><td>{TU_NOMBRE}</td></tr>
                <tr><td><strong>IBAN:</strong></td><td><code style="font-size: 16px;">{TU_IBAN}</code></td></tr>
                <tr><td><strong>Banco:</strong></td><td>{TU_BANCO}</td></tr>
                <tr><td><strong>Importe:</strong></td><td><strong style="color: #2E7D32;">{total:.2f} €</strong></td></tr>
                <tr><td><strong>Concepto (IMPORTANTE):</strong></td><td><code style="background: yellow; padding: 2px 5px;">{num_pedido}</code></td></tr>
            </table>
            <p style="margin-top: 10px; font-size: 14px; color: #555;">
                ⚠️ <strong>IMPORTANTE:</strong> Usa el concepto <strong>{num_pedido}</strong> para que podamos identificar tu pago.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Botón para confirmar que ya pagó
        st.markdown("---")
        st.markdown("### ✅ ¿Ya hiciste la transferencia?")
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            confirmar_pago = st.button("📲 Ya hice la transferencia", use_container_width=True)
        
        if confirmar_pago:
            # Guardar el pedido en el archivo CSV
            pedido_guardado = {
                "num_pedido": num_pedido,
                "fecha_pedido": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "nombre": nombre,
                "direccion": direccion,
                "telefono": telefono,
                "email": email_cliente,
                "producto": opcion,
                "cantidad": cantidad,
                "total": total,
                "fecha_entrega": fecha_entrega.strftime("%Y-%m-%d"),
                "hora_entrega": hora_entrega,
                "instrucciones": instrucciones,
                "estado": "pendiente_verificar"
            }
            
            archivo_pedidos = "pedidos.csv"
            df_nuevo = pd.DataFrame([pedido_guardado])
            
            if os.path.exists(archivo_pedidos):
                df_existente = pd.read_csv(archivo_pedidos)
                df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)
            else:
                df_final = df_nuevo
            
            df_final.to_csv(archivo_pedidos, index=False)
            
            # Enviar email al administrador (TÚ)
            email_admin = f"""
            <html>
            <body style="font-family: Arial, sans-serif;">
                <h2 style="color: #FF6B35;">🍽️ ¡NUEVO PEDIDO!</h2>
                <div style="background-color: #f5f5f5; padding: 15px; border-radius: 10px;">
                    <p><strong>📦 Pedido #:</strong> {num_pedido}</p>
                    <p><strong>👤 Cliente:</strong> {nombre}</p>
                    <p><strong>📍 Dirección:</strong> {direccion}</p>
                    <p><strong>📞 Teléfono:</strong> {telefono}</p>
                    <p><strong>🍲 Producto:</strong> {opcion} x{cantidad}</p>
                    <p><strong>💰 Total:</strong> {total:.2f} €</p>
                    <p><strong>📅 Entrega:</strong> {fecha_entrega.strftime('%d/%m/%Y')} - {hora_entrega}</p>
                    <p><strong>📝 Instrucciones:</strong> {instrucciones or "Ninguna"}</p>
                    <hr>
                    <p><strong>⚠️ EL CLIENTE HA INDICADO QUE YA HIZO LA TRANSFERENCIA</strong></p>
                    <p><strong>Concepto para buscar en tu banco:</strong> <code>{num_pedido}</code></p>
                </div>
                <p style="margin-top: 15px;">Revisa tu cuenta bancaria y confirma el pago en el panel de administración antes de entregar.</p>
            </body>
            </html>
            """
            enviar_email(f"📦 NUEVO PEDIDO #{num_pedido} - {nombre} - {total:.2f}€", email_admin)
            
            # Enviar email de confirmación al cliente
            if email_cliente:
                email_cliente_html = f"""
                <html>
                <body style="font-family: Arial, sans-serif;">
                    <h2 style="color: #2E7D32;">✅ ¡Pedido recibido!</h2>
                    <p>Hemos recibido correctamente tu pedido #{num_pedido}.</p>
                    
                    <h3>🧾 Resumen:</h3>
                    <p><strong>Producto:</strong> {opcion} x{cantidad}</p>
                    <p><strong>Total:</strong> {total:.2f} €</p>
                    <p><strong>Entrega:</strong> {fecha_entrega.strftime('%d/%m/%Y')} - {hora_entrega}</p>
                    
                    <h3>🏦 Datos para la transferencia:</h3>
                    <p><strong>Beneficiario:</strong> {TU_NOMBRE}</p>
                    <p><strong>IBAN:</strong> {TU_IBAN}</p>
                    <p><strong>Concepto:</strong> <code>{num_pedido}</code></p>
                    
                    <hr>
                    <p>📞 Si tienes alguna duda, llámanos al {TELEFONO_CONTACTO}</p>
                    <p>🍽️ ¡Gracias por confiar en nosotros!</p>
                </body>
                </html>
                """
                enviar_email(f"✅ Tu pedido #{num_pedido} está confirmado", email_cliente_html, email_cliente)
            
            st.success(f"✅ ¡Gracias, {nombre}! Tu pedido #{num_pedido} ha sido registrado.")
            st.info(f"💰 Realiza la transferencia de **{total:.2f} €** usando el concepto **{num_pedido}**.\n\n📌 Te avisaremos por WhatsApp cuando confirmemos el pago.")
            st.balloons()
            
            # Limpiar el pedido actual
            st.session_state["pedido_actual"] = None
            st.rerun()

# ============================================
# 🔒 PANEL DE ADMINISTRACIÓN
# ============================================

st.divider()
st.header("🔒 Panel de administración")

with st.expander("Acceso al panel (solo para el dueño del negocio)"):
    contrasena = st.text_input("Contraseña", type="password")
    
    if contrasena == CONTRASENA_ADMIN:
        st.success("🔓 Acceso concedido")
        
        if os.path.exists("pedidos.csv"):
            pedidos_df = pd.read_csv("pedidos.csv")
            
            # Estadísticas
            st.subheader("📊 Estadísticas")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total pedidos", len(pedidos_df))
            with col2:
                pendientes = len(pedidos_df[pedidos_df['estado'] == 'pendiente_verificar'])
                st.metric("Pendientes de pago", pendientes, delta="👀 Revisar" if pendientes > 0 else None)
            with col3:
                st.metric("Ingresos totales", f"{pedidos_df['total'].sum():.2f} €")
            with col4:
                st.metric("Ticket medio", f"{pedidos_df['total'].mean():.2f} €")
            
            st.divider()
            
            # Filtros
            st.subheader("🔍 Filtrar pedidos")
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                estado_filtro = st.selectbox("Estado", ["Todos", "pendiente_verificar", "pagado", "entregado"])
            with col_f2:
                orden = st.selectbox("Ordenar por", ["fecha_pedido (reciente)", "fecha_pedido (antiguo)", "total (mayor)", "total (menor)"])
            
            # Aplicar filtros
            df_filtrado = pedidos_df.copy()
            if estado_filtro != "Todos":
                df_filtrado = df_filtrado[df_filtrado['estado'] == estado_filtro]
            
            if orden == "fecha_pedido (reciente)":
                df_filtrado = df_filtrado.sort_values('fecha_pedido', ascending=False)
            elif orden == "fecha_pedido (antiguo)":
                df_filtrado = df_filtrado.sort_values('fecha_pedido', ascending=True)
            elif orden == "total (mayor)":
                df_filtrado = df_filtrado.sort_values('total', ascending=False)
            elif orden == "total (menor)":
                df_filtrado = df_filtrado.sort_values('total', ascending=True)
            
            st.write(f"**Mostrando {len(df_filtrado)} pedidos**")
            st.dataframe(df_filtrado, use_container_width=True)
            
            # Gestión de pedidos
            st.divider()
            st.subheader("✅ Gestionar pedidos")
            
            pedidos_pendientes = df_filtrado[df_filtrado['estado'] == 'pendiente_verificar']
            if len(pedidos_pendientes) > 0:
                pedido_seleccionado = st.selectbox(
                    "Selecciona un pedido para actualizar",
                    pedidos_pendientes['num_pedido'].tolist()
                )
                
                pedido_data = pedidos_pendientes[pedidos_pendientes['num_pedido'] == pedido_seleccionado].iloc[0]
                
                st.markdown(f"""
                <div style="background-color: #fff3e0; padding: 10px; border-radius: 10px;">
                    <p><strong>👤 Cliente:</strong> {pedido_data['nombre']}</p>
                    <p><strong>💰 Total:</strong> {pedido_data['total']:.2f} €</p>
                    <p><strong>📞 Teléfono:</strong> {pedido_data['telefono']}</p>
                    <p><strong>📍 Dirección:</strong> {pedido_data['direccion']}</p>
                    <p><strong>📅 Entrega:</strong> {pedido_data['fecha_entrega']} - {pedido_data['hora_entrega']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    if st.button("💰 Marcar como pagado"):
                        pedidos_df.loc[pedidos_df['num_pedido'] == pedido_seleccionado, 'estado'] = 'pagado'
                        pedidos_df.to_csv("pedidos.csv", index=False)
                        st.success(f"✅ Pedido {pedido_seleccionado} marcado como PAGADO")
                        st.rerun()
                
                with col_b2:
                    if st.button("🚚 Marcar como entregado"):
                        pedidos_df.loc[pedidos_df['num_pedido'] == pedido_seleccionado, 'estado'] = 'entregado'
                        pedidos_df.to_csv("pedidos.csv", index=False)
                        st.success(f"✅ Pedido {pedido_seleccionado} marcado como ENTREGADO")
                        st.rerun()
            else:
                st.info("No hay pedidos pendientes de verificar")
            
            # Descargar pedidos
            st.divider()
            with open("pedidos.csv", "rb") as file:
                st.download_button(
                    label="📥 Descargar todos los pedidos (CSV)",
                    data=file,
                    file_name=f"pedidos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        else:
            st.info("📭 Todavía no hay pedidos. ¡Comparte tu app para empezar a recibir!")
    
    elif contrasena:
        st.error("❌ Contraseña incorrecta")

# ============================================
# PIE DE PÁGINA
# ============================================

st.divider()
st.markdown(f"""
<div style="text-align: center; color: #666; font-size: 12px;">
    <p>{NOMBRE_NEGOCIO} - Comidas caseras con amor 💚</p>
    <p>📞 {TELEFONO_CONTACTO} | 📧 {EMAIL_REMITENTE}</p>
</div>
""", unsafe_allow_html=True)