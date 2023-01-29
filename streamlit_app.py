import streamlit as st
import yaml

def main():
    st.set_page_config(page_title="YAML Parser", page_icon=":guardsman:", layout="wide")
    st.title("YAML Parser")

    uploaded_file = st.file_uploader("Upload your YAML file", type=["yml", "yaml"])

    if uploaded_file:
        with open(uploaded_file) as file:
            yaml_data = yaml.safe_load(file)
            st.write("Here is the contents of your YAML file:")
            st.json(yaml_data)

if __name__ == '__main__':
    main()
