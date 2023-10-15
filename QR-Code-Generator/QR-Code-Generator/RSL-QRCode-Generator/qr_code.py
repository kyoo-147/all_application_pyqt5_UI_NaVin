import qrcode
from PIL import Image
from servicemen import Serviceman



class QrCode():
    """Class required for generating the QR Codes"""

    def __init__(self, url, imageName):
        """Initalize QrCode Class"""
        self.url = url
        self.imageName = imageName

    def get_url(self):
        return self.url

    def get_imageName(self):
        return  self.imageName

    def set_imageName(self, imageName):
        self.imageName = imageName

    def set_url(self, url):
        self.url = url

    def generate_qr_code(self):
        url = self.url
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="transparent")
        imageName = self.imageName
        img.save(f"QR_codes/{imageName}.png")


url = "https://github.com/Billy4896/QR-Code-Generator"
imageName = "githubPurple"
a = QrCode(url, imageName)
a.generate_qr_code()