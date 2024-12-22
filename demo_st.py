import streamlit as st
from diffusers import DiffusionPipeline
from PIL import Image

# Load the models
@st.cache_resource
def load_pipeline(version):
    model_name = f"Spestly/OdysseyXL-{version}"
    try:
        return DiffusionPipeline.from_pretrained(model_name)
    except Exception as e:
        st.error(f"Failed to load model: {e}")
        return None

# Streamlit app
def main():
    st.title("OdysseyXL Image Generator")
    st.write("Generate images using the OdysseyXL model family. Select the model version, enter your prompt, and generate an image.")

    # Sidebar for model version selection
    st.sidebar.header("Model Selection")
    model_version = st.sidebar.selectbox(
        "Select OdysseyXL Version",
        ("3.0", "2.0", "1.0"),
        index=0
    )

    # Text input for the prompt
    prompt = st.text_input(
        "Enter your text prompt:",
        value="Astronaut in a jungle, cold color palette, muted colors, detailed, 8k"
    )

    # Generate button
    if st.button("Generate Image"):
        with st.spinner("Loading the model and generating the image..."):
            # Load the selected pipeline
            pipe = load_pipeline(model_version)
            if pipe:
                try:
                    # Generate the image
                    image = pipe(prompt).images[0]
                    # Display the image
                    st.image(image, caption=f"Generated with OdysseyXL-{model_version}", use_column_width=True)

                    # Download option
                    st.download_button(
                        label="Download Image",
                        data=image.tobytes(),
                        file_name="generated_image.png",
                        mime="image/png"
                    )
                except Exception as e:
                    st.error(f"Failed to generate image: {e}")

if __name__ == "__main__":
    main()
