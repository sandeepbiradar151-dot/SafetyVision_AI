import torch
print(f"--- GPU DIAGNOSTIC ---")
try:
    print(f"PyTorch Version: {torch.__version__}")
    if torch.cuda.is_available():
        print(f"✅ SUCCESS: Found {torch.cuda.get_device_name(0)}")
        print(f"   VRAM Available: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
    else:
        print("❌ FAILURE: Python is using CPU. GPU not found.")
except Exception as e:
    print(f"❌ Error: {e}")