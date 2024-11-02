import textwrap
import cv2
from PIL import ImageFont, Image, ImageDraw
import numpy as np

def fnPlot_Warp_Text(img, lstlines, x1, y1, twidth=35, font_size=0.7, font_thickness=1, lineSpacing=10, color=(0, 0, 0), bg_Width=4):
    font = cv2.FONT_HERSHEY_SIMPLEX
    if type(lstlines) == str:
        # Tách các dòng trong xâu text bằng ký tự xuống dòng (\n)
        lstlines = lstlines.splitlines()
    
    # Khởi tạo tọa độ y ban đầu cho dòng đầu tiên
    y = y1
    textsize = None
    # Lặp qua từng dòng và in trên ảnh
    for i, line in enumerate(lstlines):
        wrapped_text = textwrap.wrap(line, width=twidth)
        if len(line) == 0:
            wrapped_text = ['']
        for j, wrapped_line in enumerate(wrapped_text):
            if textsize is None:
                textsize = cv2.getTextSize(wrapped_line, font, font_size, font_thickness)[0]
            # gap = textsize[1] + lineSpacing
            
            # Cập nhật tọa độ y cho dòng mới
            y += textsize[1] + lineSpacing
            
            x = int(x1)
            cv2.putText(img, wrapped_line, (x, int(y)), font, font_size,  # (128, 128, 128),
                        (255, 255, 255),
                        bg_Width,
                        lineType=cv2.LINE_AA
                        )
            cv2.putText(img, wrapped_line, (int(x), int(y)), font, font_size, color, font_thickness, lineType=cv2.LINE_AA)
    return img


def PlotText_UTF8(image, text, x=50, y=50, font="C:/Windows/Fonts/arial.ttf", font_size=35, color=(255, 0, 0, 255), change_color_position=False):
    """
    Plot text using UTF-8 (vietnamese)
    """
    if len(color) == 3:
        color = tuple(list(color) + [255])
    if change_color_position:
        b = color
        b = (b[2], b[1], b[0], b[3])
        color = b
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image)
    # Draw non-ascii text onto image
    font = ImageFont.truetype(font, font_size)
    draw = ImageDraw.Draw(pil_image)
    draw.text((x, y), text, font=font, fill=color)
    # Convert back to Numpy array and switch back from RGB to BGR
    image = np.asarray(pil_image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image


def PlotText_UTF8_outline(image, text, x=50, y=50, font="C:/Windows/Fonts/arial.ttf", font_size=30, color=(255, 0, 0, 255), outline_color=(255, 255, 255, 128), outline_width=1):
    """
    Plot text using UTF-8 (vietnamese) with an outline
    """
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image)
    
    # Draw non-ascii text onto image with outline
    font = ImageFont.truetype(font, font_size)
    draw = ImageDraw.Draw(pil_image)
    
    # Draw the outline
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            draw.text((x + dx, y + dy), text, font=font, fill=outline_color)
    
    # Draw the main text
    draw.text((x, y), text, font=font, fill=color)
    
    # Convert back to Numpy array and switch back from RGB to BGR
    image = np.asarray(pil_image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image


def opposite_color(color):
    return tuple(255 - value for value in color)


def putTextWithOutline(image, text, position, font, font_scale, color, thickness):
    # outline_color = (128, 128, 128)
    outline_color = opposite_color(color)
    img = cv2.putText( image, text, position, font, font_scale, outline_color, thickness + 3, cv2.LINE_AA, )
    img = cv2.putText( img, text, position, font, font_scale, color, thickness, cv2.LINE_AA )
    return img


def draw_bounding_box( image, list_x1y1x2y2, label_text="", font_scale=None, thickness=None, TopOnly=False, colour=(0, 255, 0), hesoFont=1.0, hesoLine=1.0, ):
    # Calculate thickness and font scale based on image width
    h, w = image.shape[:2]
    if not thickness:
        thickness = int(max(1, hesoLine * h / 420))
    if not font_scale:
        font_scale = max(0.5, hesoFont * h / 1200.0)
    # Draw the bounding box
    x1, y1, x2, y2 = list_x1y1x2y2
    if TopOnly:
        y2 = y1 + thickness
    cv2.rectangle(image, (x1, y1), (x2, y2), (188, 188, 188), thickness + 1)
    cv2.rectangle(image, (x1, y1), (x2, y2), colour, thickness)
    # Put the label and confidence

    cv2.putText( image, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, font_scale, (120, 120, 120), thickness + 1, )
    cv2.putText( image, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, font_scale, colour, thickness, )
    return image


def PlotText(image, label_text, x1, y1, font_scale, thickness, colour=(0, 255, 0)):
    cv2.putText( image, label_text, (x1, y1), cv2.FONT_HERSHEY_DUPLEX, font_scale, (120, 120, 120), thickness + 1, )
    cv2.putText( image, label_text, (x1, y1), cv2.FONT_HERSHEY_DUPLEX, font_scale, colour, thickness, )
