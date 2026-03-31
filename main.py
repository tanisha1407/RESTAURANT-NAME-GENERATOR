import streamlit as st
import google.generativeai as genai

# --- Streamlit UI ---
st.set_page_config(page_title="Restaurant Generator 🍽️", page_icon="🍕")

st.title("🍴 Restaurant Name & Menu Generator")

# 🔑 API KEY INPUT (NEW)
api_key = st.text_input("Enter your Gemini API Key:", type="password")

# Inputs
cuisine = st.selectbox(
    "Choose cuisine type:",
    ["Italian", "Indian", "Mexican", "Chinese", "Japanese", "French", "Thai"]
)

style = st.text_input("Enter restaurant style (e.g., modern, cozy):")

number = st.slider("How many ideas?", 1, 5, 3)

# Button
if st.button("COOK IDEA"):
    if not api_key:
        st.warning("⚠️ Please enter your Gemini API key")
    elif not style.strip():
        st.warning("⚠️ Please enter restaurant style")
    else:
        try:
            # Configure Gemini
            genai.configure(api_key=api_key)

            model = genai.GenerativeModel("gemini-1.5-flash")

            prompt = f"""
            Generate {number} creative restaurant names for a {style} restaurant serving {cuisine} cuisine.
            For each restaurant, also suggest a short sample menu as a comma-separated list of 5 dishes.

            Format:
            Restaurant Name: <name>
            Menu: item1, item2, item3, item4, item5
            """

            response = model.generate_content(prompt)

            result = response.text

            st.success("Here are your ideas:")

            # Format output nicely
            lines = [line for line in result.split("\n") if line.strip()]
            current_name = None

            for line in lines:
                if line.lower().startswith("restaurant name"):
                    current_name = line.split(":", 1)[1].strip()
                    st.markdown(f"### 🍽️ {current_name}")
                elif line.lower().startswith("menu"):
                    menu_items = line.split(":", 1)[1].strip()
                    st.write(f"👉 {menu_items}")

        except Exception as e:
            st.error(f"Error: {str(e)}")
