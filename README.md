# 🖼 Steganography Tool - Hide Secrets in Plain Sight  

A Python tool to hide and extract secret messages inside images using LSB (Least Significant Bit) steganography.  

![Demo](assets/demo.gif) (Add a GIF/screenshot showing encoding/decoding in action)  

## ✨ Features  
- *Hide Text in Images*: Encode secret messages into PNG/BMP files without visible changes.  
- *Extract Hidden Data*: Decode messages from steganographic images.  
- *Password Protection*: Optional AES-256 encryption for secure encoding/decoding.  
- *Multiple Modes*: Supports CLI (command-line) and GUI (Tkinter/PyQt) interfaces.  
- *Metadata Support*: (Optional) Hide data in EXIF/metadata fields.  

## 🚀 Quick Start  

### Installation  
```bash
git clone https://github.com/shivangi0502/steganography_with_encryption.git  
cd steganography_with_encryption
pip install -r requirements.txt  # Pillow, cryptography, numpy
