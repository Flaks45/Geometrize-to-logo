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
            print(f"File path was found. {file_path}\n")

    except FileNotFoundError:
        image_data = {}
        print(f"File path wasn't found. {file_path}\n")

    # Configuration
    try:
        displace = tuple(map(int, input(
            "Tip! For 500x500 images displace will be (0, 0), since logo's drawing space is 500 pixels by 500 pixels \n"
            "Enter displace amount | Follow format -> (x, y): ").replace('(', '').replace(')', '').split(',')))
        if len(displace) != 2:
            raise ValueError
    except ValueError:
        print("Invalid displace format, set to default: (0, 0)")
        displace = (0, 0)

    print(f"Displace amount set to {displace}\n")

    try:
        color_variation = tuple(map(int, input("For color variation keep in mind that (255, 255, 255) will result in "
                                               "the original image \nEnter color variation | Follow format -> "
                                               "(r, g, b): ").replace('(', '').replace(')', '').split(',')))
        if len(color_variation) != 3:
            raise ValueError
    except ValueError:
        print("Invalid color variation format, set to default: (255, 255, 255)")
        color_variation = (255, 255, 255)

    print(f"Color variation set to {color_variation}\n")

    # Generates logo code
    final_code = generate_image(image_data, displace, color_variation)

    pyperclip.copy(final_code)

    print("Code successfully copied to your clipboard.")
