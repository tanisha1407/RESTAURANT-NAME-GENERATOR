import streamlit as st
from google import genai

st.set_page_config(page_title="Restaurant Generator 🍽️")

st.title("🍴 Restaurant Name & Menu Generator")

# API Key input
api_key = st.text_input("Enter Gemini API Key:", type="password")

# Inputs
cuisine = st.selectbox(
    "Choose cuisine:",
    ["Italian", "Indian", "Mexican", "Chinese", "Japanese"]
)

style = st.text_input("Restaurant style:")

number = st.slider("Number of ideas:", 1, 5, 3)

if st.button("COOK IDEA"):
    if not api_key:
        st.warning("Enter API key")
    elif not style:
        st.warning("Enter style")
    else:
        try:
            # Initialize Gemini
            client = genai.Client(api_key=api_key)

            prompt = f"""
            Generate {number} creative restaurant names for a {style} restaurant serving {cuisine} cuisine.
            Also provide 5 menu items.

            Format:
            Restaurant Name: <name>
            Menu: item1, item2, item3, item4, item5
            """

            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )

            result = response.text

            st.success("Here are your ideas:")

            lines = [line for line in result.split("\n") if line.strip()]

            for line in lines:
                if line.lower().startswith("restaurant name"):
                    name = line.split(":", 1)[1].strip()
                    st.markdown(f"### 🍽️ {name}")
                elif line.lower().startswith("menu"):
                    menu = line.split(":", 1)[1].strip()
                    st.write(f"👉 {menu}")

        except Exception as e:
            st.error(str(e))
