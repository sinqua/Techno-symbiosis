import easyocr

reader = easyocr.Reader(['ko', 'en'], gpu=True)

# image = 'IMG_1979.jpeg'
image = 'korean.jpg'

result = reader.readtext(image, detail=0)
print(result)
user_input = ' '.join(result)

print(user_input)