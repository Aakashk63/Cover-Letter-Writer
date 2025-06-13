import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable
import os

# ----------------------------
# 1. Set your Gemini API key
# ----------------------------
# You can also use environment variable: os.environ["GOOGLE_API_KEY"] = "AIzaSyDuswxRiX6aX4Wv3-YsWhlz_lPVa6mbA0A"
GOOGLE_API_KEY = "AIzaSyDuswxRiX6aX4Wv3-YsWhlz_lPVa6mbA0A"  # 🔁 Replace with your actual key
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# ----------------------------
# 2. Setup Gemini LLM via LangChain
# ----------------------------
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# ----------------------------
# 3. Create a ChatPromptTemplate
# ----------------------------
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a translator that converts English to French."),
    ("user", "Translate this sentence to French: {sentence}")
])

# ----------------------------
# 4. Create a simple LangChain chain
# ----------------------------
chain: Runnable = prompt | llm

# ----------------------------
# 5. Build the Streamlit UI
# ----------------------------
st.set_page_config(page_title="English to French Translator", page_icon="🌍")

st.title("🌍 English to French Translator")
st.write("Enter an English sentence below and click **Translate** to see the French version.")

# Text input
user_input = st.text_input("Enter your sentence in English:", placeholder="e.g., How are you today?")

# Button to trigger translation
if st.button("Translate"):
    if user_input.strip() == "":
        st.warning("Please enter a sentence to translate.")
    else:
        try:
            # Run the chain
            result = chain.invoke({"sentence": user_input})
            # Extract content if it's an AIMessage
            output = result.content if hasattr(result, "content") else str(result)

            st.success("✅ Translation successful!")
            st.markdown(f"**French Translation:**\n\n> {output}")
        except Exception as e:
            st.error(f"❌ An error occurred during translation:\n\n{e}")
