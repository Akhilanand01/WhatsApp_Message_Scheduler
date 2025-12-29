import streamlit as st
from twilio.rest import Client
from datetime import datetime
import time

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="WhatsApp Scheduler", page_icon="📲")

st.title("📲 WhatsApp Message Scheduler")
st.caption("Built using Python, Streamlit & Twilio WhatsApp API")

# ------------------ LOAD SECRETS ------------------
account_sid = st.secrets["TWILIO_ACCOUNT_SID"]
auth_token = st.secrets["TWILIO_AUTH_TOKEN"]

client = Client(account_sid, auth_token)

# ------------------ USER INPUT ------------------
name = st.text_input("Recipient Name")
recipient_number = st.text_input(
    "Recipient WhatsApp Number",
    placeholder="+919876543210"
)
message_body = st.text_area("Message")

date_input = st.date_input("Select Date")
time_input = st.time_input("Select Time")

# ------------------ SEND FUNCTION ------------------
def send_whatsapp_message(number, message):
    try:
        msg = client.messages.create(
            body=message,
            from_="whatsapp:+14155238886",  # Twilio Sandbox number
            to=f"whatsapp:{number}"
        )
        return True, msg.sid
    except Exception as e:
        return False, str(e)

# ------------------ BUTTON ------------------
if st.button("📤 Schedule Message"):

    # Input validation
    if not recipient_number or not message_body:
        st.error("❌ Please enter recipient number and message")
    else:
        scheduled_datetime = datetime.combine(date_input, time_input)
        delay_seconds = (scheduled_datetime - datetime.now()).total_seconds()

        if delay_seconds <= 0:
            st.error("❌ Please select a future date & time")
        else:
            st.success(
                f"✅ Message scheduled for {scheduled_datetime.strftime('%d %b %Y, %H:%M')}"
            )

            # Streamlit limitation note
            st.info("⏳ App will wait until scheduled time...")

            time.sleep(delay_seconds)

            success, result = send_whatsapp_message(
                recipient_number,
                f"Hi {name},\n\n{message_body}" if name else message_body
            )

            if success:
                st.success(f"🎉 Message sent successfully!\nSID: {result}")
            else:
                st.error(f"❌ Failed to send message\n{result}")
