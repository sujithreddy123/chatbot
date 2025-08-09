import streamlit as st
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# Symptom data with conditions, medicine suggestions, and disclaimers
symptom_medication_map = {
    "headache": {
        "conditions": ["Migraine", "Tension headache", "Dehydration", "High blood pressure"],
        "medicines": [
            "Over-the-counter painkillers like acetaminophen or ibuprofen may help.",
            "Stay hydrated and rest well."
        ],
        "disclaimer": "If the headache persists or worsens, consult a healthcare professional."
    },
    "fever": {
        "conditions": ["Infection", "Flu", "COVID-19", "Heat exhaustion"],
        "medicines": [
            "Acetaminophen or ibuprofen can help reduce fever.",
            "Drink plenty of fluids and rest."
        ],
        "disclaimer": "Seek medical help if fever lasts more than 3 days or is very high."
    },
    "cough": {
        "conditions": ["Common cold", "Bronchitis", "Pneumonia", "COVID-19"],
        "medicines": [
            "Cough syrups or lozenges may provide relief.",
            "Warm fluids and steam inhalation can help."
        ],
        "disclaimer": "If cough persists over 2 weeks or worsens, see a doctor."
    }
}

def extract_symptoms(user_input):
    found = []
    for symptom in symptom_medication_map:
        if symptom in user_input.lower():
            found.append(symptom)
    return found

def provide_medical_suggestions(symptoms):
    responses = []
    for symptom in symptoms:
        info = symptom_medication_map[symptom]
        response = (
            f"🩺 **Symptom:** {symptom.capitalize()}\n"
            f"Possible causes: {', '.join(info['conditions'])}\n\n"
            f"💊 **Suggestions:** {' '.join(info['medicines'])}\n\n"
            f"⚠ **Note:** {info['disclaimer']}"
        )
        responses.append(response)
    return "\n\n---\n\n".join(responses) if responses else "Sorry, I couldn't identify your symptoms."

# Setup chatbot for generic fallback replies
bot = ChatBot('MedicalBot')
trainer = ListTrainer(bot)
trainer.train([
    "Hello", "Hi! How can I help you with your health?",
    "Goodbye", "Take care and see a doctor for serious symptoms."
])

# Streamlit UI
st.title("🩺 Medical Chatbot with Suggestions")
st.write("Describe your symptoms, and I’ll suggest possible conditions and remedies. This is for informational purposes only.")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("💬 Your message:")

if st.button("Send") and user_input:
    symptoms = extract_symptoms(user_input)
    if symptoms:
        bot_reply = provide_medical_suggestions(symptoms)
    else:
        bot_reply = str(bot.get_response(user_input))

    st.session_state.history.append(("You", user_input))
    st.session_state.history.append(("Bot", bot_reply))

# Display conversation history
for sender, message in st.session_state.history:
    if sender == "You":
        st.markdown(f"**🧑 You:** {message}")
    else:
        st.markdown(f"**🤖 Bot:** {message}")

