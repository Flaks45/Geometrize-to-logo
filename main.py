import json
import pyperclip


from logic import generate_image


if __name__ == "__main__":
    # Get image data from Geometrize json file
    file_path = input("Copy and paste the path to the Geometrize json file: ").replace('"', '')
    try:
        with open(file_path) as j_file:
            image_data_raw = j_file.read()
            image_data = json.loads(image_data_raw)
            print(f"File path was found. {file_path}")

    except FileNotFoundError:
        image_data = {}
        print(f"File path wasn't found. {file_path}")

    # Configuration
    displace = (0, 0)

    # Generates logo code
    final_code = generate_image(image_data, displace)

    pyperclip.copy(final_code)

    print("Code has been successfully copied to your clipboard.")
