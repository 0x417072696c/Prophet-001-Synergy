from PIL import Image

def encode_message(image_path, message, output_path):
    img = Image.open(image_path).convert('RGB') # Гарантируем RGB
    encoded = img.copy()
    width, height = img.size
    
    # Добавляем маркер конца, чтобы декодер знал, где остановиться
    message += "Prophet 001 | L = [S0 * H * G] | Synergy 2026.04.11 | Silence is the Key. ###"
    # Превращаем сообщение в строку битов
    binary_message = ''.join(format(ord(c), '08b') for c in message)
    data_index = 0
    
    for y in range(height):
        for x in range(width):
            pixel = list(img.getpixel((x, y)))
            for n in range(3): # Проходим по R, G, B
                if data_index < len(binary_message):
                    # ИСПРАВЛЕНО: Обращаемся к конкретному каналу pixel[n]
                    pixel[n] = (pixel[n] & ~1) | int(binary_message[data_index])
                    data_index += 1
            
            encoded.putpixel((x, y), tuple(pixel))
            
            if data_index >= len(binary_message):
                encoded.save(output_path)
                return print(f"Синергия зафиксирована в {output_path}.")

# Запуск
encode_message('lik.png', 'L = [S0*H*G] | Prophet 001 | Synergy 2026', 'prophet_lsb.png')
import os
print(f"Ищу файл: {os.path.abspath('lik.png')}")
print("Запуск процесса...")