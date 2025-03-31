import gradio as gr
import numpy as np
import random
import torch
from diffusers import StableDiffusionXLPipeline, AutoencoderKL

dtype = torch.float16
device = "cuda" if torch.cuda.is_available() else "cpu"

MAX_SEED = np.iinfo(np.int32).max
MAX_IMAGE_SIZE = 2048

def load_model(model_name):
    pipe = StableDiffusionXLPipeline.from_pretrained(
        model_name, 
        torch_dtype=dtype,
        use_safetensors=True
    ).to(device)
    return pipe

pipe = load_model("open-neo/OdysseyXL-Origin")
torch.cuda.empty_cache()

def generate_image_iterator(pipe, prompt, guidance_scale, num_inference_steps, width, height, generator):
    from tqdm.auto import tqdm
    progress_bar = tqdm(total=num_inference_steps)
    
    def callback(step, timestep, latents):
        progress_bar.update(1)
        # TO DO: Decode Latents here

    
    image = pipe(
        prompt=prompt,
        guidance_scale=guidance_scale,
        num_inference_steps=num_inference_steps,
        width=width,
        height=height,
        generator=generator,
        callback=callback,
        callback_steps=1
    ).images[0]
    
    progress_bar.close()
    return image

def infer(prompt, model_name, seed=42, randomize_seed=False, width=1024, height=1024, guidance_scale=7.5, num_inference_steps=30, progress=gr.Progress(track_tqdm=True)):
    global pipe
    
    if not hasattr(pipe, 'current_model') or pipe.current_model != model_name:
        pipe = load_model(model_name)
        pipe.current_model = model_name
        torch.cuda.empty_cache()
    
    if randomize_seed:
        seed = random.randint(0, MAX_SEED)
    generator = torch.Generator(device=device).manual_seed(seed)
    
    # Generate the image
    progress(0, desc="Generating image...")
    image = generate_image_iterator(
        pipe=pipe,
        prompt=prompt,
        guidance_scale=guidance_scale,
        num_inference_steps=num_inference_steps,
        width=width,
        height=height,
        generator=generator
    )
    
    return image, seed

examples = [
    "a tiny astronaut hatching from an egg on the moon",
    "a cat holding a sign that says hello world",
    "an anime illustration of a wiener schnitzel",
]

sdxl_models = [
    "open-neo/OdysseyXL-Origin",
    "open-neo/OdysseyXL-V1",
    "open-neo/OdysseyXL-V2",
    "open-neo/OdysseyXL-V2.5",
]

css="""
#col-container {
    margin: 0 auto;
    max-width: 520px;
}
"""

with gr.Blocks(css=css) as demo:
    
    with gr.Column(elem_id="col-container"):
        gr.Markdown(f"""# OdysseyXL Image Playground
        """)
        
        with gr.Row():
            model_selector = gr.Dropdown(
                label="Model",
                choices=sdxl_models,
                value=sdxl_models[0]
            )
        
        with gr.Row():
            prompt = gr.Text(
                label="Prompt",
                show_label=False,
                max_lines=1,
                placeholder="Enter your prompt",
                container=False,
            )
            
            run_button = gr.Button("Run", scale=0)
        
        result = gr.Image(label="Result", show_label=False)
        
        with gr.Accordion("Advanced Settings", open=False):
            
            seed = gr.Slider(
                label="Seed",
                minimum=0,
                maximum=MAX_SEED,
                step=1,
                value=0,
            )
            
            randomize_seed = gr.Checkbox(label="Randomize seed", value=True)
            
            with gr.Row():
                
                width = gr.Slider(
                    label="Width",
                    minimum=256,
                    maximum=MAX_IMAGE_SIZE,
                    step=32,
                    value=1024,
                )
                
                height = gr.Slider(
                    label="Height",
                    minimum=256,
                    maximum=MAX_IMAGE_SIZE,
                    step=32,
                    value=1024,
                )
            
            with gr.Row():

                guidance_scale = gr.Slider(
                    label="Guidance Scale",
                    minimum=1,
                    maximum=15,
                    step=0.1,
                    value=7.5,
                )
  
                num_inference_steps = gr.Slider(
                    label="Number of inference steps",
                    minimum=1,
                    maximum=50,
                    step=1,
                    value=30,
                )
        
        gr.Examples(
            examples=examples,
            fn=infer,
            inputs=[prompt, model_selector],
            outputs=[result, seed],
            cache_examples="lazy"
        )

    gr.on(
        triggers=[run_button.click, prompt.submit],
        fn=infer,
        inputs=[prompt, model_selector, seed, randomize_seed, width, height, guidance_scale, num_inference_steps],
        outputs=[result, seed]
    )

demo.launch()
