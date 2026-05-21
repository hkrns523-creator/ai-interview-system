import qrcode

url = "https://reformist-symptom-unusual.ngrok-free.dev"

qr = qrcode.make(url)

qr.save("project_qr.png")

print("QR Code Generated")