# Install ComfyUI for BCE (Linux)

This installs ComfyUI in an isolated folder without modifying your system shell.

---

## 1. Choose Install Location

Example:

```
/mnt/DATA/temp/genAI
```

```bash
mkdir -p /mnt/DATA/temp/genAI
cd /mnt/DATA/temp/genAI
```

---

## 2. Install Miniconda (local only)

Download Miniconda (Linux x86_64) from:

```
https://docs.conda.io/en/latest/miniconda.html
```

Install into:

```
/mnt/DATA/temp/genAI/miniconda3
```

Do NOT allow it to modify your .bashrc.

---

## 3. Create Comfy Environment

```bash
source miniconda3/bin/activate
conda create -n comfy python=3.12 -y
conda activate comfy
```

---

## 4. Install ComfyUI

```bash
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
pip install -r requirements.txt
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

---

## 5. Install ComfyUI Manager

```bash
cd custom_nodes
git clone https://github.com/ltdrdata/ComfyUI-Manager comfyui-manager
```

Restart ComfyUI after installing Manager.

---

## 6. Launch ComfyUI

```bash
cd /mnt/DATA/temp/genAI/ComfyUI
source ../miniconda3/bin/activate comfy
python main.py
```

Open:

http://127.0.0.1:8188
