import qrcode

data = input("Enter a URL:")

try:
    img = qrcode.make(data)

    name = input("Enter file name:")

    img.save(name)

    print("QR code generated!")

except Exception as e:
    print(f"Error occurred {e}")