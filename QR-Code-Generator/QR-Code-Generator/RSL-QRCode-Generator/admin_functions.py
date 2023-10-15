import os
import fnmatch
from PIL import Image


class AdminFunctions:
    """Comprised of a variety functions required for main to operate successfully."""

    def create_folder(self):
        """Create a folder on launch of the application."""
        folder_name = "QR_CODES"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

    def search_qr_image(self, serviceNumber):
        """The function searches and displays the corresponding image based on the input."""
        pattern = serviceNumber + ".png"
        folder_path = "QR_CODES/"

        # search for files that match the pattern
        matches = []
        for root, dirs, files in os.walk(folder_path):
            for filename in fnmatch.filter(files, pattern):
                matches.append(os.path.join(root, filename))

        if matches:
            # print the matched file paths
            for match in matches:
                print(match)

                # open and display the image
                image = Image.open(match)
                image.show()
        else:
            print(
                f"No QR code image found for service number {serviceNumber}. Please try again with a different service number.")

    def delete_qr_image(self, serviceNumber):
        """The function deletes the matching qrcode from the QR_CODES folder based on the input."""
        pattern = serviceNumber + ".png"
        folder_path = "QR_CODES/"

        # search for files that match the pattern
        matches = []
        for root, dirs, files in os.walk(folder_path):
            for filename in fnmatch.filter(files, pattern):
                matches.append(os.path.join(root, filename))

        if matches:
            # print the matched file paths
            for match in matches:
                print(f"Deleting QR code image: {match}")

                # delete the file
                os.remove(match)
        else:
            print(
                f"No QR code image found for service number {serviceNumber}. Please try again with a different service number.")