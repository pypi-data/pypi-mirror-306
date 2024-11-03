import torch
import argparse
import os
from PIL import Image
from transformers import AutoTokenizer
from .weights import load_from_safetensors
from .vision import encode_image
from .text import text_encoder, text_decoder, lm_head
from .rope import precompute_freqs_cis

def run_inference(image_path: str, prompt: str, model_path: str, max_tokens: int = 200, sampler: str = "greedy"):
    """
    Run inference on an image with a given prompt.
    
    Args:
        image_path (str): Path to the image file
        prompt (str): Question to ask about the image
        model_path (str): Path to the model weights
        max_tokens (int, optional): Maximum number of tokens to generate. Defaults to 200.
        sampler (str, optional): Sampling strategy ("greedy" or "multinomial"). Defaults to "greedy".
    
    Returns:
        str: Generated answer
    """
    if torch.cuda.is_available():
        torch.set_default_device("cuda")
    elif torch.backends.mps.is_available():
        torch.set_default_device("mps")

    # Load model
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}")
    model = load_from_safetensors(model_path)

    # Your existing inference code here...
    # [Rest of your original code from sample.py goes here, 
    #  wrapped in the function with appropriate returns]
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found at {image_path}")
    image = Image.open(image_path)
    image = image.resize((378, 378))
    image_tensor = encode_image(image, model.vision)

    # Encode text, and create inputs_embeds.
    tokenizer = AutoTokenizer.from_pretrained("vikhyatk/moondream2")
    prompt = f"\n\nQuestion: {prompt}\n\nAnswer:"
    input_ids = tokenizer(prompt, return_tensors="pt")["input_ids"]
    input_ids = torch.cat([torch.tensor([[tokenizer.eos_token_id]]), input_ids], dim=1)
    inputs_embeds = text_encoder(input_ids, model.text)
    inputs_embeds = torch.cat(
        [
            inputs_embeds[:, 0:1, :],
            image_tensor.unsqueeze(0),
            inputs_embeds[:, 1:, :],
        ],
        dim=1,
    )

    kv_cache = torch.empty(24, 2, 1, 32, 0, 64, dtype=torch.float16)
    freqs_cis = precompute_freqs_cis(32, 2048)

    for _ in range(max_tokens):
        with torch.no_grad():
            hidden, kv_cache = text_decoder(
                inputs_embeds, model.text, kv_cache, freqs_cis
            )
            logits = lm_head(hidden, model.text)

            if sampler == "multinomial":
                next_token = torch.multinomial(
                    torch.softmax(logits, dim=-1), num_samples=1
                ).squeeze(0)
            elif sampler == "greedy":
                next_token = torch.argmax(logits, dim=-1)
            else:
                raise ValueError(f"Invalid sampler: {sampler}")

            if next_token == tokenizer.eos_token_id:
                print()
                break

            input_ids = next_token.unsqueeze(0)
            inputs_embeds = text_encoder(input_ids, model.text)

            output_text = tokenizer.batch_decode(input_ids)[0]
            
            print(output_text, end="", flush=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", "-i", type=str, required=True)
    parser.add_argument("--prompt", "-p", type=str, required=True)
    parser.add_argument("--model", "-m", type=str, required=True)
    parser.add_argument("--max-tokens", "-t", type=int, default=200)
    parser.add_argument("--sampler", "-s", type=str, default="greedy")
    args = parser.parse_args()
    
    result = run_inference(
        args.image,
        args.prompt,
        args.model,
        max_tokens=args.max_tokens,
        sampler=args.sampler
    )
    print(result)

if __name__ == "__main__":
    main()