# Create a new file called download_fix.py and run it
from huggingface_hub import hf_hub_download

# This pulls the exact file ChromaDB was struggling with
print("Downloading the ONNX model... please wait.")
hf_hub_download(
    repo_id="sentence-transformers/all-MiniLM-L6-v2",
    filename="onnx/model.onnx",
    cache_dir="/home/nehtrm/.cache/chroma/onnx_models/all-MiniLM-L6-v2"
)
print("Download complete! You can run Lyra-san now.")
