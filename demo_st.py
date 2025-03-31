import os
import re
import time
from glob import iglob
from io import BytesIO

import streamlit as st
import torch
from einops import rearrange
from fire import Fire
from PIL import ExifTags, Image
from torchvision import transforms
from transformers import pipeline
from diffusers import DiffusionPipeline

NSFW_THRESHOLD = 0.85

def st_keyup(label, value="", key=None, debounce=0):
    input_value = st.text_input(label, value=value, key=key)
    
    if key not in st.session_state:
        st.session_state[key] = value
        
    return input_value

@st.cache_resource()
def get_pipeline(model_name: str, device: torch.device):
    pipe = DiffusionPipeline.from_pretrained(model_name)
    pipe.to(device)
    return pipe

def get_image() -> torch.Tensor | None:
    image = st.file_uploader("Input", type=["jpg", "JPEG", "png"])
    if image is None:
        return None
    image = Image.open(image).convert("RGB")

    transform = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Lambda(lambda x: 2.0 * x - 1.0),
        ]
    )
    img: torch.Tensor = transform(image)
    return img[None, ...]

@torch.inference_mode()
def main(
        device: str = "cuda" if torch.cuda.is_available() else "cpu",
        output_dir: str = "output",
        debug: bool = False,
):
    st.set_page_config(page_title="OdysseyXL", layout="wide")
    st.title("Text-to-Image by Open-Neo")
    
    torch_device = torch.device(device)
    if debug:
        st.info(f"Using device: {torch_device}")
        
    model_names = ["open-neo/OdysseyXL-V2.5", "open-neo/OdysseyXL-V2", "open-neo/OdysseyXL-V1", "open-neo/OdysseyXL-Origin"]
    model_name = st.selectbox("Which model to load?", model_names)
    
    if model_name is None or not st.checkbox("Load model", False):
        st.warning("Please select a model and check 'Load model' to continue.")
        return

    with st.spinner(f"Loading {model_name}..."):
        pipe = get_pipeline(model_name, torch_device)
    
    st.success(f"Model {model_name} loaded successfully!")

    prompt = st_keyup("Enter a prompt", value="", debounce=300, key="interactive_text")
    
    with st.expander("Advanced Options"):
        guidance_scale = st.slider("Guidance Scale", min_value=1.0, max_value=20.0, value=7.5, step=0.5)
        num_inference_steps = st.slider("Inference Steps", min_value=1, max_value=100, value=50, step=1)
        
    output_name = os.path.join(output_dir, "img_{idx}.jpg")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        idx = 0
    else:
        fns = [fn for fn in iglob(output_name.format(idx="*")) if re.search(r"img_[0-9]+\.jpg$", fn)]
        if len(fns) > 0:
            idx = max(int(fn.split("_")[-1].split(".")[0]) for fn in fns) + 1
        else:
            idx = 0

    if st.button("Generate"):
        if not prompt:
            st.error("Please enter a prompt")
            return
            
        with st.spinner(f"Generating '{prompt}'"):
            if debug:
                st.write(f"Generating '{prompt}'")
            t0 = time.perf_counter()

            image = pipe(
                prompt, 
                guidance_scale=guidance_scale, 
                num_inference_steps=num_inference_steps
            ).images[0]

            t1 = time.perf_counter()

            fn = output_name.format(idx=idx)
            if debug:
                st.write(f"Done in {t1 - t0:.1f}s.")

            buffer = BytesIO()
            exif_data = Image.Exif()
            exif_data[ExifTags.Base.Software] = "AI generated;txt2img;flux"
            exif_data[ExifTags.Base.Make] = "Black Forest Labs"
            exif_data[ExifTags.Base.Model] = model_name

            image.save(buffer, format="jpeg", exif=exif_data, quality=95, subsampling=0)
            img_bytes = buffer.getvalue()

            if debug:
                st.write(f"Saving {fn}")
            with open(fn, "wb") as file:
                file.write(img_bytes)
            idx += 1

            st.session_state["samples"] = {
                "prompt": prompt,
                "img": image,
                "bytes": img_bytes,
            }
            
            st.success("Image generated successfully!")

    samples = st.session_state.get("samples", None)
    if samples is not None:
        st.image(samples["img"], caption=samples["prompt"])
        st.download_button(
            "Download full-resolution",
            samples["bytes"],
            file_name="generated.jpg",
            mime="image/jpg",
        )

def app():
    Fire(main)

if __name__ == "__main__":
    app()
