![Header](https://raw.githubusercontent.com/Aayan-Mishra/Images/refs/heads/main/API%20(1).png)

# OdysseyXL Family

Welcome to the **OdysseyXL** family! This repository showcases the cutting-edge advancements in the **OdysseyXL** series, a collection of finetuned **Stable Diffusion XL** models designed to push the boundaries of creativity and realism in generative AI. Whether you're an artist, researcher, or developer, OdysseyXL has something for you.

---

## 🚀 Models in the OdysseyXL Family

![4.0-Grid](https://raw.githubusercontent.com/Aayan-Mishra/Images/refs/heads/main/4.0-Grid.png)

### **OdysseyXL 4.0**
The most advanced SOTA generative model in the OdysseyXL Family, OdysseyXL 4.0 is perfect for:
- Ultra realism
- Full potential of OdysseyXL
- Cinematic and photographic images

### **OdysseyXL 3.0**
Optimized for ultra-realism and vibrant creativity, OdysseyXL 3.0 is perfect for:
- High-detail art generation
- Photorealistic renders
- Excellent prompt adherence

### **OdysseyXL 2.0**
A balanced model combining realism with stylistic flexibility. Ideal for:
- Concept art
- Digital painting
- Experimenting with styles

### **OdysseyXL 1.0**
The original model that started it all. Great for:
- General-purpose image generation
- Prototyping creative ideas

---

## 🛠️ Usage
### Option 1:
To get started with any OdysseyXL model, install the `diffusers` library and load the model using the following example:

```bash
pip install diffusers
```

Now we can the generation script. For this example we will use OdysseyXL-3.0

```bash
git clone https://github.com/Aayan-Mishra/OdysseyXL.git
cd OdysseyXL
python3 download-and-infrence.py
```
### Option 2:
In this option you can use the new OdysseyXL API (Part of spestly package. Only supports 3.0+)!

```bash
pip install spestly
```

Now that we have the API system installed, we can now use it! A demo is shown below:

```python
from spestly import OdysseyXL

odysseyxl = OdysseyXL()

# Define the prompt and negative prompt
prompt = (
    "An amateur cellphone photography of a black Ferrari. "
    "f8.0, Samsung Galaxy, noise, jpeg artefacts, poor lighting, low light, "
    "underexposed, high contrast"
)
negative_prompt = (
    "(octane render, render, drawing, anime, bad photo, bad photography:1.3), "
    "(worst quality, low quality, blurry:1.2), "
    "(bad teeth, deformed teeth, deformed lips), "
    "(bad anatomy, bad proportions:1.1), "
    "(deformed iris, deformed pupils), "
    "(deformed eyes, bad eyes), "
    "(deformed face, ugly face, bad face), "
    "(deformed hands, bad hands, fused fingers), "
    "morbid, mutilated, mutation, disfigured"
)

# Generate the image using the OdysseyXL model version 3.0
image = odysseyxl.generate(
    model_version="3.0",
    prompt=prompt,
    negative_prompt=negative_prompt,
)

image.save("output.png")
image.show()
```

---

## 🌟 Features

- **Ultra-Realism**: OdysseyXL 3.0 excels in generating images that blur the lines between reality and imagination.
- **Fine Detail**: Tailored for intricate and high-resolution artwork.
- **Creative Flexibility**: Adaptable to a wide range of artistic and technical applications.

---

## 📂 Available Models

| Model          | Size       | API Access               | Hardware |
|----------------|------------|--------------------------|---------------|
|OdysseyXL 4.0   | Large      | [HuggingFace](https://huggingface.co/Spestly/OdysseyXL-4.0), [DiffuseCraftMod](https://huggingface.co/spaces/John6666/DiffuseCraftMod), OdysseyXL API | 1xA100
| OdysseyXL 3.0 | Large      | [Civitai](https://civitai.com/models/1055457/odysseyxl), [HuggingFace](https://huggingface.co/Spestly/OdysseyXL-3.0), [DiffuseCraft](https://huggingface.co/spaces/r3gm/DiffuseCraft), OdysseyXL API     | 1xA100     |
| OdysseyXL 2.0 | Medium     | [Civitai](https://civitai.com/models/1055457?modelVersionId=1187743), [HuggingFace](https://huggingface.co/Spestly/OdysseyXL-2.0)  | 1xL40S  |
| OdysseyXL 1.0 | Small      | [Civitai](https://civitai.com/models/1055457?modelVersionId=1187335), [HuggingFace](https://huggingface.co/Spestly/OdysseyXL-1.0)  | 1xP100  |

---

## 📖 License

All models in the OdysseyXL family are shared under the **Stability.ai Community license**. Please ensure you adhere to the terms and conditions outlined in the license.

---

## 📢 Community and Support

Join the OdysseyXL community to share your creations, report issues, and stay updated:

- **Discord**: Coming Soon
- **Twitter**: [@Spestly](https://twitter.com/Spestly)
- **Submit your generated images!**: [Submit](https://tally.so/r/mZPblv)

For any questions or support, feel free to reach out via email at [aayan.mishra@proton.me](mailto:aayan.mishra@proton.me).

