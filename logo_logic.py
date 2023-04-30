import math


def get_circle_function():
    """Custom logo function to generate a circle.
    :return: circle custom function
    :rtype: str
    """
    return "to generate_circle :x :y :radius :r :g :b\nsetxy :x :y" \
           "\nsetpensize :radius\ncolor (:r :g :b)\ncircle :radius/2\nend\n\n"


def get_line_function():
    """Custom logo function to generate a line.
    :return: line custom function
    :rtype: str
    """
    return "to generate_line :x :y :length :angle :r :g :b\nsetxy :x :y" \
           "\nsetpensize 1\ncolor (:r :g :b)\nrt :angle\nfd :length\nlt :angle\nend\n\n"


def get_rectangle_function():
    """Custom logo function to generate a rectangle.
    :return: rectangle custom function
    :rtype: str
    """
    return "to generate_rectangle :x :y :height :width :r :g :b\nsetxy :x :y" \
           "\nsetpensize :width\ncolor (:r :g :b)\nfd :height\nend\n\n"


def get_rotated_rectangle_function():
    """Custom logo function to generate a rotated rectangle.
    :return: rotated rectangle custom function
    :rtype: str
    """
    return "to generate_rotated_rectangle :x :y :height :width :rotation :r :g :b\nsetxy :x :y" \
           "\nsetpensize :width\ncolor (:r :g :b)\nrt :rotation\npu\nbk :height / 2\npd\nfd :height\nlt :rotation\n" \
           "end\n\n"


def get_functions():
    """
    Get all custom logo functions for future use.
    :return: all custom functions
    :rtype: str
    """
    functions = [get_circle_function(), get_line_function(), get_rectangle_function(), get_rotated_rectangle_function()]
    return "".join(functions)


def circle_string(position: tuple, radius: int, color: tuple):
    """
    Logo code to generate one circle.
    :param tuple position: Position of the circle
    :param int radius: Radius of the circle
    :param tuple color: Color of the circle
    :return: generate circle
    :rtype: str
    """
    return f"generate_circle {position[0]} {position[1]} {radius} {color[0]} {color[1]} {color[2]}"


def line_string(position: tuple, length: int, angle: int, color: tuple):
    """
    Logo code to generate one line.
    :param tuple position: Position of the line
    :param int length: Length of the line
    :param int angle: Angle of the line
    :param tuple color: Color of the line
    :return: generate line
    :rtype: str
    """
    return f"generate_line {position[0]} {position[1]} {length} {angle} {color[0]} {color[1]} {color[2]}"


def rectangle_string(position: tuple, height: int, width: int, color: tuple):
    """
    Logo code to generate one rectangle.
    :param tuple position: Position of the rectangle
    :param int height: Height of the rectangle
    :param int width: Width of the rectangle
    :param tuple color: Color of the rectangle
    :return: generate rectangle
    :rtype: str
    """
    return f"generate_rectangle {position[0]} {position[1]} {height} {width} {color[0]} {color[1]} {color[2]}"


def rotated_rectangle_string(position: tuple, height: int, width: int, rotation: int, color: tuple):
    """
    Logo code to generate one rotated rectangle.
    :param tuple position: Position of the rectangle
    :param int height: Height of the rectangle
    :param int width: Width of the rectangle
    :param int rotation: Angle of rotation of the rectangle
    :param tuple color: Color of the rectangle
    :return: generate rectangle
    :rtype: str
    """
    return f"generate_rotated_rectangle {position[0]} {position[1]} {height} {width} {rotation} " \
           f"{color[0]} {color[1]} {color[2]}"


def finish_string():
    """
    Logo code to move turtle out of the way at the end of drawing.
    :return: move turtle away
    :rtype: str
    """
    return f"\nsetxy 0 0"


def generate_image(image_data: dict = None, displace: tuple = None, scale_factor: int = None,
                   color_variation: tuple = None, bg_activated: bool = False, margin_activated: bool = False):
    """
    Logo code to generate the final image.
    :param bool bg_activated: Whether a plain background is generated or not
    :param bool margin_activated: Whether the image is generated with margins or not
    :param dict image_data: Image data from Geometrize file
    :param tuple displace: Displacement amount of the image
    :param int scale_factor: Scale of the image
    :param tuple color_variation: Color multipliers of the image
    :return: finished code
    :rtype: str
    """
    # If no image needs to be drawn
    if scale_factor == 0:
        return "No code has been generated since scale is equal to 0"

    # Default values
    if image_data is None:
        image_data = {}

    if displace is None:
        displace = (0, 0)

    if scale_factor is None:
        scale_factor = 1

    if color_variation is None:
        color_variation = (255, 255, 255)

    code = ""

    if bg_activated and len(image_data) > 0:
        bg_color = (int(image_data[0]["color"][0] * color_variation[0] / 255),
                    int(image_data[0]["color"][1] * color_variation[1] / 255),
                    int(image_data[0]["color"][2] * color_variation[2] / 255))

        code += f"setxy 250 500 setpensize 500 color ({bg_color[0]} {bg_color[1]} {bg_color[2]}) fd 500\n\n"

    for shape in image_data:
        # Get info from the object
        color_data = shape["color"]
        transform_data = [int(telement * scale_factor) for telement in shape["data"]]
        shape_color = (int(color_data[0] * color_variation[0] / 255),
                       int(color_data[1] * color_variation[1] / 255),
                       int(color_data[2] * color_variation[2] / 255))

        # If the object type is a rectangle
        if shape["type"] == 0:
            rectangle_position = (int((transform_data[0] + transform_data[2]) / 2) + displace[0],
                                  transform_data[3] + displace[1])
            rectangle_width = transform_data[2] - transform_data[0]
            if rectangle_width == 0:
                rectangle_width = 1
            rectangle_height = transform_data[3] - transform_data[1]

            code += "\n" + rectangle_string(rectangle_position, rectangle_height, rectangle_width, shape_color)

        # If the object type is a rotated rectangle
        if shape["type"] == 1:
            rotated_rectangle_position = (int((transform_data[0] + transform_data[2]) / 2 + displace[0]),
                                          int((transform_data[1] + transform_data[3]) / 2 + displace[1]))
            rotated_rectangle_width = transform_data[2] - transform_data[0]
            if rotated_rectangle_width == 0:
                rotated_rectangle_width = 1
            rotated_rectangle_height = transform_data[3] - transform_data[1]
            rotated_rectangle_rotation = int(transform_data[4] / scale_factor)

            code += "\n" + rotated_rectangle_string(rotated_rectangle_position, rotated_rectangle_height,
                                                    rotated_rectangle_width, rotated_rectangle_rotation, shape_color)

        # If the object type is a circle
        if shape["type"] == 5:
            circle_position = (transform_data[0] + displace[0], transform_data[1] + displace[1])
            circle_radius = transform_data[2]

            code += "\n" + circle_string(circle_position, circle_radius, shape_color)

        # If the object type is a line
        if shape["type"] == 6:
            line_x1, line_x2 = (transform_data[0], transform_data[2])
            line_y1, line_y2 = (transform_data[1], transform_data[3])

            line_position = (line_x1 + displace[0], line_y1 + displace[1])
            line_angle = 360 + 90 + int(math.degrees(
                math.atan2((line_y2 - line_y1), line_x2 - line_x1)))
            line_length = int(math.dist([line_x1, line_y1], [line_x2, line_y2]))

            code += "\n" + line_string(line_position, line_length, line_angle, shape_color)

    # Draw margins
    if margin_activated and len(image_data) > 0:
        margin_corners = [image_data[0]["data"][0] * scale_factor + displace[0],
                          image_data[0]["data"][1] * scale_factor + displace[1],
                          image_data[0]["data"][2] * scale_factor + displace[0],
                          image_data[0]["data"][3] * scale_factor + displace[1]]
        (0, 0, int(margin_corners[0]), 500)
        code += "\n" + rectangle_string((int(margin_corners[0] / 2), 500), 500, int(margin_corners[0]), (0, 0, 0))
        code += "\n" + rectangle_string((250, int(margin_corners[1])), int(margin_corners[1]), 500, (0, 0, 0))
        code += "\n" + rectangle_string((int(margin_corners[2]) + int((500 - int(margin_corners[2])) / 2), 500), 500,
                                        500 - int(margin_corners[2]), (0, 0, 0))
        code += "\n" + rectangle_string((250, 500), 500 - int(margin_corners[3]), 500, (0, 0, 0))

    return get_functions() + code + finish_string()
