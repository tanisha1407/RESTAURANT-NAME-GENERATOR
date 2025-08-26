import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# LangChain LLM with GPT-4o-mini
llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=OPENAI_API_KEY,
    temperature=0.7
)

# Define prompt template
prompt_template = PromptTemplate(
    input_variables=["cuisine", "style", "number"],
    template="""
    Generate {number} creative restaurant names for a {style} restaurant serving {cuisine} cuisine.
    For each restaurant, also suggest a short sample menu as a comma-separated list of 5 signature dishes.
    Format output clearly as:
    Restaurant Name: <name>
    Menu: item1, item2, item3, item4, item5
    """
)

chain = LLMChain(llm=llm, prompt=prompt_template)

# Streamlit UI
st.set_page_config(page_title="Restaurant Name & Menu Generator 🍽️", page_icon="🍕", layout="centered")
st.title("🍴 Restaurant Name & Menu Generator")
st.write("Generate restaurant names and menus")

# Cuisine dropdown
cuisine = st.selectbox(
    "Choose cuisine type:",
    ["Italian", "Indian", "Mexican", "Chinese", "Japanese", "French", "Thai", "Mediterranean", "American"]
)

# Style input
style = st.text_input("Enter restaurant style (e.g., modern, cozy, luxurious):", "")

# Number of ideas
number = st.slider("How many restaurant ideas do you want?", 1, 5, 3)

if st.button("COOK IDEA"):
    if style.strip() == "":
        st.warning("⚠️ Please enter the restaurant style.")
    else:
        with st.spinner("✨ Cooking up restaurant names and menus..."):
            try:
                result = chain.run(cuisine=cuisine, style=style, number=number)

                st.success("Here are your restaurant name & menu ideas:")

                # Format output as list
                lines = [line for line in result.strip().split("\n") if line.strip()]
                current_name = None
                for line in lines:
                    if line.lower().startswith("restaurant name"):
                        current_name = line.split(":", 1)[1].strip()
                        st.markdown(f"**🍽️ {current_name}**")
                    elif line.lower().startswith("menu"):
                        menu_items = line.split(":", 1)[1].strip()
                        st.write(f"   - {menu_items}")

            except Exception as e:
                st.error(f"Error: {str(e)}")
