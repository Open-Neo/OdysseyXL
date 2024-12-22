import gradio as gr
from diffusers import DiffusionPipeline
from PIL import Image

# Load the models
def load_pipeline(version):
    model_name = f"Spestly/OdysseyXL-{version}"
    return DiffusionPipeline.from_pretrained(model_name)

# Function to generate an image
def generate_image(version, prompt):
    # Load the selected pipeline
    pipe = load_pipeline(version)
    
    # Generate the image
    image = pipe(prompt).images[0]
    
    # Return the generated image
    return image
    
css="""
#col-container {
    margin: 0 auto;
    max-width: 520px;
}
"""

# Define the Gradio interface with custom design
with gr.Blocks(css=css) as demo:
    with gr.Row():
        gr.Markdown("<h1>✨ OdysseyXL Image Generator ✨</h1>")
    
    gr.Markdown(
        """
        <h2>🎨 Create stunning AI-generated images!</h2>
        <p style='text-align:center;'>
            Select a model version, enter a descriptive text prompt, and let OdysseyXL bring your imagination to life.
        </p>
        """
    )
    
    with gr.Row():
        with gr.Column(scale=1):
            version = gr.Dropdown(
                ["3.0", "2.0", "1.0"], 
                value="3.0", 
                label="🛠 Select Model Version", 
                interactive=True
            )
        with gr.Column(scale=2):
            prompt = gr.Textbox(
                value="Astronaut in a jungle, cold color palette, muted colors, detailed, 8k", 
                label="💡 Enter Your Prompt", 
                lines=2, 
                placeholder="Describe the image you want to generate..."
            )
    
    with gr.Row():
        generate_button = gr.Button("🚀 Generate Image", elem_id="generate-button")
    
    with gr.Row():
        image_output = gr.Image(label="Generated Image", type="numpy", elem_id="output-image")
    
    generate_button.click(
        fn=generate_image, 
        inputs=[version, prompt], 
        outputs=image_output
    )

    gr.Markdown(
        """
        <div class="footer">
            <p>Developed with ❤️ by <a href="https://github.com/Aayan-Mishra" target="_blank">Spestly</a></p>
        </div>
        """
    )

# Run the app
if __name__ == "__main__":
    demo.launch()
