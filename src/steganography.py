from stegano import lsb
from PIL import Image

class Steganography:
    @staticmethod
    def encode_message(image_path, message, password, output_path):
        """Hide message in image with password protection"""
        try:
            # Simple password "encryption" by prepending to message
            secured_message = f"{password}|||{message}"
            
            # Encode the message in the image
            secret = lsb.hide(image_path, secured_message)
            secret.save(output_path)
            return True, "Message encoded successfully!"
        except Exception as e:
            return False, f"Encoding failed: {str(e)}"

    @staticmethod
    def decode_message(image_path, password):
        """Extract message from image with password verification"""
        try:
            extracted = lsb.reveal(image_path)
            if extracted is None:
                return False, "No hidden message found"
            
            parts = extracted.split("|||", 1)
            if len(parts) != 2:
                return False, "Invalid message format or no password found"
                
            extracted_password, message = parts
            if extracted_password != password:
                return False, "Incorrect password"
                
            return True, message
        except Exception as e:
            return False, f"Decoding failed: {str(e)}"

    @staticmethod
    def is_image_file(filepath):
        """Check if file is a valid image"""
        try:
            Image.open(filepath)
            return True
        except:
            return False
