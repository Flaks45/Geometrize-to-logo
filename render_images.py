import math
from PIL import Image, ImageDraw


def hex_string(value: int):
    """
    Turns value into hex without the address (0xXX -> XX).
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
    Function to return the string of an RGB color.
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
    Function to rotate points.
    :param ax: point A x
    :param ay: point A y
    :param bx: point B x
    :param by: point B y
    :param angle: angle to rotate
    :return: New position (x, y)
    :rtype: tuple[float, float]
    """
    radius = math.dist((ax, ay), (bx, by))
    angle += math.atan2(ay - by, ax - bx)
    return (
        round(bx + radius * math.cos(angle)),
        round(by + radius * math.sin(angle))
    )


def preview_image(image_data: dict = None, displace: tuple = None, scale_factor: int = None,
                  color_variation: tuple = None, bg_activated: bool = False, margin_activated: bool = False):
    """
    Function to preview a generated Logo image.
    :param bool bg_activated: Whether a plain background is generated or not
    :param bool margin_activated: Whether the image is generated with margins or not
    :param dict image_data: Image data from Geometrize file
    :param tuple displace: Displacement amount of the image
    :param int scale_factor: Scale of the image
    :param tuple color_variation: Color multipliers of the image
    :return: Image file
    :rtype: Image.new()
    """
    # Default values
    if image_data is None:
        image_data = {}

    if displace is None:
        displace = (0, 0)

    if scale_factor is None:
        scale_factor = 1

    if color_variation is None:
        color_variation = (255, 255, 255)

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

    # If no image needs to be drawn
    if scale_factor == 0:
        return image

    # Draw background
    if bg_activated and len(image_data) > 0:
        bg_color = (int(image_data[0]["color"][0] * color_variation[0] / 255),
                    int(image_data[0]["color"][1] * color_variation[1] / 255),
                    int(image_data[0]["color"][2] * color_variation[2] / 255))
        d_image.rectangle((0, 0, 500, 500), fill=rgb_to_string(bg_color[0], bg_color[1], bg_color[2]))

    # Draw shapes
    for shape in image_data:
        # Get info from the object
        color_data = shape["color"]
        transform_data = [int(telement * scale_factor) for telement in shape["data"]]
        shape_color = rgb_to_string(int(color_data[0] * color_variation[0] / 255),
                                    int(color_data[1] * color_variation[1] / 255),
                                    int(color_data[2] * color_variation[2] / 255))

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
                                                math.radians(transform_data[4] / scale_factor))
                                  for x, y in rectangle_vertices]

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

    # Draw margins
    if margin_activated and len(image_data) > 0:
        margin_corners = [image_data[0]["data"][0] * scale_factor + displace[0],
                          image_data[0]["data"][1] * scale_factor + displace[1],
                          image_data[0]["data"][2] * scale_factor + displace[0],
                          image_data[0]["data"][3] * scale_factor + displace[1]]
        d_image.rectangle((0, 0, int(margin_corners[0]), 500), fill="#000000")
        d_image.rectangle((0, 0, 500, int(margin_corners[1])), fill="#000000")
        d_image.rectangle((int(margin_corners[2]), 0, 500, 500), fill="#000000")
        d_image.rectangle((0, int(margin_corners[3]), 500, 500), fill="#000000")

    return image
