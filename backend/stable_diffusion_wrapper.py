from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
import torch

torch.cuda.empty_cache()

class StableDiffusionWrapper:
    def __init__(self) -> None:
        repo_id = "stabilityai/stable-diffusion-2-base"
        pipe = DiffusionPipeline.from_pretrained(
            repo_id, revision="fp16",
            torch_dtype=torch.float16
        )

        pipe.scheduler = DPMSolverMultistepScheduler.from_config(
            pipe.scheduler.config)
        self.pipe = pipe.to("cuda")

            
    def generate_images(self, text_prompt: str):
        prompt = [text_prompt]
        images = self.pipe(prompt, num_inference_steps=10).images
        return images
