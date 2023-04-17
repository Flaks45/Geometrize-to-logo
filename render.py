import math
from PIL import Image, ImageDraw


def hex_string(value: int):
    """
    Turns value into hex without the address (0xXX -> XX)
    :param int value:
    :return: hex string value
    :rtype: str
    """
    hex_value = str(hex(value)).replace("0x", "")
    if len(hex_value) < 2:
        hex_value = "0" + hex_value
    return hex_value


def rgb_to_string(r: int, g: int, b: int):
    """
    Function to return the string of an RGB color
    :param int r: Red value
    :param int g: Green value
    :param int b: Blue value
    :return: #RRGGBB
    :rtype: str
    """
    hex_r = str(hex(r)).replace("0x", "")
    if len(hex_r) < 2:
        hex_r = "0" + hex_r

    hex_g = str(hex(g)).replace("0x", "")
    if len(hex_g) < 2:
        hex_g = "0" + hex_g

    hex_b = str(hex(b)).replace("0x", "")
    if len(hex_b) < 2:
        hex_b = "0" + hex_b

    return ("#" + hex_r + hex_g + hex_b).upper()


def rotated_about(ax, ay, bx, by, angle):
    """
    Function to rotate points
    :param ax:
    :param ay:
    :param bx:
    :param by:
    :param angle:
    :return:
    """
    radius = math.dist((ax,ay),(bx,by))
    angle += math.atan2(ay-by, ax-bx)
    return (
        round(bx + radius * math.cos(angle)),
        round(by + radius * math.sin(angle))
    )


def preview_image(image_data: dict, displace: tuple = (0, 0), scale_factor: int = 1,
                  color_variation: tuple = (255, 255, 255)):
    """
    Function to preview a generated Logo image
    :param dict image_data: Image data from Geometrize file
    :param tuple displace: Displacement amount of the image
    :param int scale_factor: Scale of the image
    :param tuple color_variation: Color multipliers of the image
    :return: image
    :rtype: Image.new()
    """
    # Create white canvas
    image = Image.new(mode="RGB", size=(500, 500), color="#AAAAAA")
    d_image = ImageDraw.Draw(image)

    # Draw grid
    for i in range(400):
        d_image.rectangle((25 * (i % 20) + 1,
                           25 * math.floor(i / 20) + 1,
                           25 * (i % 20) + 24,
                          25 * math.floor(i / 20) + 24),
                          fill="#FFFFFF")

    # Draw shapes
    for shape in image_data:
        # Get info from the object
        color_data = shape["color"]
        transform_data = [telement * scale_factor for telement in shape["data"]]
        shape_color = rgb_to_string(color_data[0] * int(color_variation[0] / 255),
                                    color_data[1] * int(color_variation[1] / 255),
                                    color_data[2] * int(color_variation[2] / 255))

        # If the object type is a rectangle
        if shape["type"] == 0:
            d_image.rectangle((transform_data[0] + displace[0], transform_data[1] + displace[1],
                               transform_data[2] + displace[0], transform_data[3] + displace[1]),
                              fill=shape_color)

        # If the object type is a rotated rectangle
        if shape["type"] == 1:
            rectangle_vertices = (
                (transform_data[0] + displace[0], transform_data[1] + displace[1]),
                (transform_data[2] + displace[0], transform_data[1] + displace[1]),
                (transform_data[2] + displace[0], transform_data[3] + displace[1]),
                (transform_data[0] + displace[0], transform_data[3] + displace[1])
            )
            rectangle_vertices = [rotated_about(x, y, (transform_data[0] + transform_data[2]) / 2 + displace[0],
                                                (transform_data[3] + transform_data[1]) / 2 + displace[1],
                                                math.radians(transform_data[4])) for x, y in rectangle_vertices]

            d_image.polygon(rectangle_vertices, fill=shape_color)

        # If the object type is a circle
        if shape["type"] == 5:
            d_image.ellipse([((transform_data[0] - transform_data[2] + displace[0]),
                              (transform_data[1] - transform_data[2] + displace[1])),
                            ((transform_data[0] + transform_data[2] + displace[0]),
                             (transform_data[1] + transform_data[2] + displace[1]))],
                            fill=shape_color)

        # If the object type is a line
        if shape["type"] == 6:
            d_image.line([(transform_data[0] + displace[0], transform_data[1] + displace[1]),
                          (transform_data[2] + displace[0], transform_data[3] + displace[1])],
                         fill=shape_color)

    return image
