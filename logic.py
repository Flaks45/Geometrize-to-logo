import math


def get_circle_function():
    """Logo function to generate a circle. Returns string."""
    return "to generate_circle :x :y :radius :r :g :b\nsetxy :x :y" \
           "\nsetpensize :radius\ncolor (:r :g :b)\ncircle :radius/2\nend"


def get_line_function():
    """Logo function to generate a line. Returns string."""
    return "to generate_line :x :y :length :angle :r :g :b\nsetxy :x :y" \
           "\nsetpensize 1\ncolor (:r :g :b)\nrt :angle\nfd :length\nlt :angle\nend"


def get_rectangle_function():
    """Logo function to generate a rectangle. Returns string."""
    return "to generate_rectangle :x :y :length :width :r :g :b\nsetxy :x :y" \
           "\nsetpensize :width\ncolor (:r :g :b)\nfd :length\nend"


def get_functions():
    """All logo functions. Returns string."""
    functions = ""
    functions += get_circle_function() + "\n\n"
    functions += get_line_function() + "\n\n"
    functions += get_rectangle_function() + "\n"
    return functions


def circle_string(position: tuple, radius: int, color: tuple):
    """Logo code to generate one circle. Requires position (tuple), radius (int) and color (tuple).
    Returns string."""
    return f"generate_circle {position[0]} {position[1]} {radius} {color[0]} {color[1]} {color[2]}"


def line_string(position: tuple, length: int, angle: int, color: tuple):
    """Logo code to generate one circle. Requires position (tuple), radius (int), angle (int) and color (tuple).
    Returns string."""
    return f"generate_line {position[0]} {position[1]} {length} {angle} {color[0]} {color[1]} {color[2]}"


def rectangle_string(position: tuple, length: int, width: int, color: tuple):
    """Logo code to generate one rectangle. Requires position (tuple), length (int), width (int) and color (tuple).
    Returns string."""
    return f"generate_rectangle {position[0]} {position[1]} {length} {width} {color[0]} {color[1]} {color[2]}"


def finish_string():
    """Logo code to move turtle out of the way at the end of drawing. Returns string."""
    return f"\nsetxy 0 0"


def generate_image(image_data: dict, displace: tuple = (0, 0), scale_factor: int = 1,
                   color_variation: tuple = (255, 255, 255)):
    """Logo code to generate the final image. Requires image data (dict), displace (tuple) and color variation (tuple).
    Returns string."""
    code = ""
    for shape in image_data:
        # Get info from the object
        color_data = shape["color"]
        transform_data = [telement * scale_factor for telement in shape["data"]]
        shape_color = (color_data[0] * int(color_variation[0] / 255),
                       color_data[1] * int(color_variation[1] / 255),
                       color_data[2] * int(color_variation[2] / 255))

        if shape["type"] == 0:  # If the object type is a rectangle
            rectangle_position = (int((transform_data[0] + transform_data[2]) / 2), transform_data[3])
            rectangle_width = transform_data[2] - transform_data[0]
            rectangle_length = transform_data[3] - transform_data[1]

            code += "\n" + rectangle_string(rectangle_position, rectangle_length, rectangle_width, shape_color)

        if shape["type"] == 5:  # If the object type is a circle
            circle_position = (transform_data[0] + displace[0], transform_data[1] + displace[1])
            circle_radius = transform_data[2]

            code += "\n" + circle_string(circle_position, circle_radius, shape_color)

        if shape["type"] == 6:  # If the object type is a line
            line_x1, line_x2 = (transform_data[0], transform_data[2])
            line_y1, line_y2 = (transform_data[1], transform_data[3])

            line_position = (line_x1 + displace[0], line_y1 + displace[1])
            line_angle = 360 + 90 + int(math.degrees(
                math.atan2((line_y2 - line_y1), line_x2 - line_x1)))
            line_length = int(math.dist([line_x1, line_y1], [line_x2, line_y2]))

            code += "\n" + line_string(line_position, line_length, line_angle, shape_color)

    return get_functions() + code + finish_string()
