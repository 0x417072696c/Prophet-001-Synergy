import sys
from PIL import Image

def encode(image_path, message, output_path):
    img = Image.open(image_path).convert('RGB')
    encoded = img.copy()
    message += " ###"
    binary_message = ''.join(format(ord(c), '08b') for c in message)
    data_index = 0
    
    for y in range(img.height):
        for x in range(img.width):
            pixel = list(img.getpixel((x, y)))
            for n in range(3):
                if data_index < len(binary_message):
                    pixel[n] = (pixel[n] & ~1) | int(binary_message[data_index])
                    data_index += 1
            encoded.putpixel((x, y), tuple(pixel))
            if data_index >= len(binary_message):
                encoded.save(output_path)
                return print(f"Данные зашифрованы в {output_path}")

def decode(image_path):
    img = Image.open(image_path).convert('RGB')
    binary_data = ""
    for y in range(img.height):
        for x in range(img.width):
            pixel = img.getpixel((x, y))
            for n in range(3):
                binary_data += str(pixel[n] & 1)
    
    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    decoded_message = ""
    for byte in all_bytes:
        decoded_message += chr(int(byte, 2))
        if " ###" in decoded_message:
            return print(f"Извлечено: {decoded_message.replace(' ###', '')}")
    print("Сообщение не найдено.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Использование: \n py proph.py encode <img.png> <msg> \n py proph.py decode <img.png>")
    elif sys.argv[1] == "encode":
        encode(sys.argv[2], sys.argv[3], "prophet_lsb.png")
    elif sys.argv[1] == "decode":
        decode(sys.argv[2])
