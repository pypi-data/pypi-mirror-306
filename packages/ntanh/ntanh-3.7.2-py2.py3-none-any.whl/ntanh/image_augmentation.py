import pickle
import os, sys
import random
# import setuptools
import shutil
import cv2
from os.path import join, exists, dirname
from pprint import pprint as pp
# print(os.getcwd()) # Thư mục console đang chạy
# print(__file__) # Thư mục file code
codeDir=dirname(os.path.abspath(__file__))
sys.path.append(codeDir)

# pp(sys.path)

from ParamsBase import tactParametters
from tqdm import tqdm
from yolo_boxes import yolo_str_to_xyxy, xyxyn_to_xyxy
from PIL import Image


APP_NAME='Image_Augmentation'

class Parameters(tactParametters):
    def __init__(self, ModuleName="TACT"):
        super().__init__(saveParam_onlyThis_APP_NAME=True)
        self.AppName = APP_NAME
        self.Ready_to_run = False # Nếu bắt buộc phải config thì đặt cái này = False, khi nào user chỉnh sang True thì mới cho chạy
        self.HD = {
            "Brightness": "Adjust brightness (value: -255 to 255)",
            "Shadow_Brightness": "Adjust Shadow_Brightness (value: -255 to 255)",
            "Contrast": "Adjust contrast (alpha > 1 increases contrast, 0 < alpha < 1 decreases)",
            "Saturation": "Convert to HSV, adjust saturation, then back to BGR",
            "Hue": "Convert to HSV, adjust hue, then back to BGR",
            "cover_yolo_string": "'0 0.496094 0.772135 0.527344 0.453125' (ví dụ xâu), cái này nếu có giá trị, nó sẽ crop ảnh theo tọa độ trong này, TODO: tính lại tọa độ label theo cái này",
            "cover_yolo_string__resize_after_crop_HW": "Là 1 list, nếu không muốn resize, để thành list rỗng: []",
            "Max_random_image_to_Aug=x": "x==0: Aug tất cả các ảnh, x>0: chỉ Aug random x ảnh thôi, để test trong quá trình dò tim các tham số",
            "Cách dùng 1": "lệnh chạytrong CMD: 'ntanh_aug', khi hiển thị ảnh: bấm SPACE để tạm dừng/chạy tiếp, bấm ESC để thoát",
            "Cách dùng 2": "Muốn đưa tham số nào về mặc định thì xóa nó đi rồi chạy lại",
        }
        self.Intro="Chương trình này dành riêng cho việc augmentation ảnh nhằm tạo ra ảnh có các kiểu khác nhau phục vụ cho mục đích training model"

        self.cover_yolo_string = ""
        self.cover_yolo_string__expand_n_pixel = 20
        self.cover_yolo_string__resize_after_crop_WH=[]
        self.Random_varian_delta_in_percent = 20
        self.Brightness = 50
        self.Shadow_Brightness=0
        self.Contrast = 1.2 
        self.Saturation = 0
        self.Hue = 0
        self.image_folder__input = ""
        self.image_folder_output = ""
        self.Copy_label_when_save_augment_image=True

        self.Display_image=True
        self.Display_image_Stop_to_View_in___cv2_waitkey__ms=1000
        self.Display_image_max_height=800
        self.Max_random_image_to_Aug=10
        self.load_then_save_to_yaml(file_path=f"{APP_NAME}.yml", ModuleName=ModuleName)


mParams = Parameters("Augmentation_images")

def taImshow(title="image",image=None, wait=0):
    H,W=image.shape[:2]
    if H > mParams.Display_image_max_height:
        fxy = mParams.Display_image_max_height / H
        image = cv2.resize(image, None, fx=fxy, fy=fxy)
    cv2.imshow(title, image)
    if wait is not None:
        cv2.waitKey(wait)


def update_labels(
    label_path, x_min_crop, y_min_crop, new_imW, new_imH, old_imW, old_imH
):
    # Cập nhật file nhãn dựa trên ảnh đã crop
    new_labels = []
    with open(label_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            # print(line)
            obj_class, x_center, y_center, width, height = map(float, line.split())

            # Tính tọa độ gốc của bounding box (theo ảnh ban đầu)
            old_x_min = (x_center - width / 2) * old_imW
            old_y_min = (y_center - height / 2) * old_imH
            old_x_max = (x_center + width / 2) * old_imW
            old_y_max = (y_center + height / 2) * old_imH

            # Điều chỉnh bounding box theo vùng đã crop
            new_x_min = max(0, old_x_min - x_min_crop)
            new_y_min = max(0, old_y_min - y_min_crop)
            new_x_max = min(new_imW, old_x_max - x_min_crop)
            new_y_max = min(new_imH, old_y_max - y_min_crop)

            # Bỏ qua các đối tượng không nằm trong vùng crop
            # if new_x_min < new_x_max and new_y_min < new_y_max:
            if 1:
                new_x_center = (new_x_min + new_x_max) / 2 / new_imW
                new_y_center = (new_y_min + new_y_max) / 2 / new_imH
                new_width = (new_x_max - new_x_min) / new_imW
                new_height = (new_y_max - new_y_min) / new_imH

                # Kiểm tra nếu tọa độ trung tâm nằm trong vùng hợp lệ
                # if 0 <= new_x_center <= 1 and 0 <= new_y_center <= 1:
                new_labels.append(
                    f"{int(obj_class)} {new_x_center:0.6f} {new_y_center:0.6f} {new_width:0.6f} {new_height:0.6f}"
                )

    s = "\n".join(new_labels)
    return s


class ImageAugmentation:
    def __init__(self):
        pass

    def Change_Brightness(self, image, value):
        # Adjust brightness
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        # Ensure brightness value is in the range of [-255, 255]
        if value > 0:
            lim = 255 - value
            v[v > lim] = 255
            v[v <= lim] += value
        else:
            lim = -value
            v[v < lim] = 0
            v[v >= lim] += value

        final_hsv = cv2.merge((h, s, v))
        result = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR) 
        return result

    def Change_Shadow_Brightness(self, image, value):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        # Create a mask for shadows (dark areas)
        shadow_mask = v < 128

        # Adjust brightness in shadow areas
        if value > 0:
            lim = 255 - value
            v[shadow_mask & (v > lim)] = 255
            v[shadow_mask & (v <= lim)] += value
        else:
            lim = -value
            v[shadow_mask & (v < lim)] = 0
            v[shadow_mask & (v >= lim)] += value

        final_hsv = cv2.merge((h, s, v))
        result = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

        return result

    def Change_Contrast(self, image, value):
        # Adjust contrast (alpha > 1 increases contrast, 0 < alpha < 1 decreases)
        return cv2.convertScaleAbs(image, alpha=value, beta=0)

    def Change_Saturation(self, image, value):
        # Convert to HSV, adjust saturation, then back to BGR
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hsv[:, :, 1] = cv2.add(hsv[:, :, 1], value)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    def Change_Hue(self, image, value):
        # Convert to HSV, adjust hue, then back to BGR
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hsv[:, :, 0] = cv2.add(hsv[:, :, 0], value)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    def Change_Vibrance(self, image, value):
        # Custom vibrance logic, placeholder here
        return image  # Vibrance adjustment not implemented for simplicity
    def restore_coordinates(self, img, restore_options): 
        # Các thông tin từ input
        org_image_hw = restore_options["orgImageHW"]  # (org_height, org_width)
        crop_image = restore_options["cropImage_xyxy"]     # (crop_x1, crop_y1, crop_x2, crop_y2)
        resize_image = restore_options["resizeImage"] # (resize_width, resize_height)
        xyxy = restore_options["xyxy"]              # bbox normalized coords in resizeImage (x_min, y_min, x_max, y_max)
        # xyxy = restore_options["xyxy"]              # bbox normalized coords in resizeImage (x_min, y_min, x_max, y_max)
        # draw_rectangles_and_show(img, [xyxy])
        # Kích thước của ảnh gốc
        org_height, org_width = org_image_hw

        # Tọa độ crop trên ảnh gốc
        crop_x1, crop_y1, crop_x2, crop_y2 = crop_image
        crop_width = crop_x2 - crop_x1
        crop_height = crop_y2 - crop_y1

        # Kích thước của ảnh đã resize
        resize_width, resize_height = resize_image

        # Tọa độ bbox trong resizeImage (chuẩn hóa lại để có tọa độ thực)
        x_min_resize = xyxy[0] # * resize_width
        y_min_resize = xyxy[1] # * resize_height
        x_max_resize = xyxy[2] # * resize_width
        y_max_resize = xyxy[3] # * resize_height
        # draw_rectangles_and_show(img, [xyxy])

        # Tính tỷ lệ chuyển từ resizeImage sang cropImage
        scale_x = crop_width / resize_width
        scale_y = crop_height / resize_height

        # Tọa độ bbox trong cropImage
        x_min_crop = x_min_resize * scale_x
        y_min_crop = y_min_resize * scale_y
        x_max_crop = x_max_resize * scale_x
        y_max_crop = y_max_resize * scale_y

        # Tọa độ bbox trong orgImage
        x_min_org = x_min_crop + crop_x1
        x_max_org = x_max_crop + crop_x1

        y_min_org = y_min_crop + crop_y1
        y_max_org = y_max_crop + crop_y1

        # Chuyển tọa độ về dạng chuẩn hóa (normalized) trên orgImage
        org_x1_normalized = x_min_org / org_width
        org_y1_normalized = y_min_org / org_height
        org_x2_normalized = x_max_org / org_width
        org_y2_normalized = y_max_org / org_height

        # Output dạng tọa độ chuẩn hóa trên orgImage
        org_xyxyn = [x_min_org,y_min_org,x_max_org,y_max_org]
        #
        org_normalized=[
            org_x1_normalized ,
            org_y1_normalized ,
            org_x2_normalized ,
            org_y2_normalized 
        ]
        return org_xyxyn

    def Augment_image_in_multiple_ways(self, image, options=None):
        """
        Python use:

        ```python
        options = {
            "cover_yolo_string": "0 0.496094 0.772135 0.527344 0.453125",  # or ''
            "cover_yolo_string__resize_after_crop_WH": [800, 600],  # or false
            "Brightness": 30,  # or 0
            "Shadow_Brightness": 0,  # or 0
            "Contrast": 1.2,  # or 0
            "Saturation": 0,  # or 0
            "Hue": 0,  # or 0
            "image_path": "",
            "Change_labels": False,
        }
        AUG = ImageAugmentation()
        image, retDict = AUG.Augment_image_in_multiple_ways(image, options=options)

        retDict['newLabel']
        retDict['orgImHW']
        retDict['orgXyxy']
        ```
        """
        if options is None:
            options = {
                "cover_yolo_string": "0 0.496094 0.772135 0.527344 0.453125",  # or ''
                "cover_yolo_string__resize_after_crop_WH": [800, 600],  # or false
                'Random_varian_delta_in_percent': 10,
                "Brightness": 30,  # or 0
                "Shadow_Brightness": 0,  # or 0
                "Contrast": 1.2,  # or 0
                "Saturation": 0,  # or 0
                "Hue": 0,  # or 0
                "image_path": "",
                "Change_labels": False,
            }
        Change_labels = options.get("Change_labels", False)

        retDict={}
        cover_yolo_string=options.get("cover_yolo_string", False)
        if cover_yolo_string:
            imH, imW = image.shape[:2]
            id, x1, y1, x2, y2 = yolo_str_to_xyxy( yolo_str=mParams.cover_yolo_string, imH=imH, imW=imW )

            d = mParams.cover_yolo_string__expand_n_pixel
            y1, y2, x1, x2 = y1 - d, y2 + d, x1 - d, x2 + d
            x1 = max(x1, 0)
            y1 = max(y1, 0)
            x2 = min(x2, imW)
            y2 = min(y2, imH)
            image = image[y1:y2, x1:x2]

            if Change_labels:
                image_path = options.get("image_path", '')
                label_path = image_path.replace(".jpg", ".txt")
                if exists(label_path):
                    x_min_crop, y_min_crop = x1, y1
                    new_imH, new_imW = image.shape[:2]
                    retDict['newLabel'] = update_labels( label_path, x_min_crop, y_min_crop, new_imW, new_imH, imW, imH, )
            retDict["orgImageHW"] = (imH, imW)
            # retDict["cropImage_xyxy"] = (x1, y1, x2, y2)
            retDict["cropImage_xyxyn"] = (x1/imW, y1/imH, x2/imW, y2/imH)

            cover_yolo_string__resize_after_crop_WH = options.get("cover_yolo_string__resize_after_crop_WH", False)
            if cover_yolo_string__resize_after_crop_WH:
                image = cv2.resize( image, tuple(cover_yolo_string__resize_after_crop_WH) )

        Delta = options.get( "Random_varian_delta_in_percent", 10 )
        Brightness= options.get("Brightness", 0)
        if Delta>0:
            Brightness = int((1.0 + (random.random() - 0.5) * Delta / 100) * Brightness)

        if Brightness:
            image = self.Change_Brightness(image, Brightness)

        Shadow_Brightness = options.get("Shadow_Brightness", 0)

        if Delta > 0: 
            Shadow_Brightness = int( (1.0 + (random.random() - 0.5) * Delta / 100) * Shadow_Brightness )

        if Shadow_Brightness:
            image = self.Change_Shadow_Brightness(image, Shadow_Brightness)

        Contrast = options.get("Contrast", 0)
        if Delta > 0: 
            Contrast = (1.0 + (random.random() - 0.5) * Delta / 100) * Contrast

        if Contrast:
            image = self.Change_Contrast(image, Contrast)

        Saturation = options.get("Saturation", 0)
        if Delta > 0: 
            Saturation = int((1.0 + (random.random() - 0.5) * Delta / 100) * Saturation)
        if Saturation:
            image = self.Change_Saturation(image, Saturation)

        Hue = options.get("Hue", 0)
        if Delta > 0:
            Hue = int((1.0 + (random.random() - 0.5) * Delta / 100) * Hue)
        if Hue:
            image = self.Change_Hue(image, Hue)

        return image, retDict

    def Change_image_multiple_ways(self, image,image_path, options):
        """
        console use
        """

        image, retDict = self.Augment_image_in_multiple_ways(image, options=options)
        if mParams.Display_image:
            taImshow(title="Augmented image", image=image, wait=None)
            keyPressed=cv2.waitKey(mParams.Display_image_Stop_to_View_in___cv2_waitkey__ms)
            if keyPressed==32:
                while True:
                    keyPressed = cv2.waitKey(
                        mParams.Display_image_Stop_to_View_in___cv2_waitkey__ms
                    )
                    if keyPressed==32:
                        break
                    if keyPressed==27:
                        os._exit(1)
        newLabel = retDict.get("newLabel", "")
        return image, newLabel

    def Augment_folder(self,TS=None, **options):
        fDau=0

        if TS is None:
            if mParams.image_folder__input == "":
                print("Hãy cấu hình giá trị cho file tham số trước, rồi chạy lại.")
                os.startfile("configs_ntanh_libs.yml")
                return
            image_folder_input = mParams.image_folder__input.replace("\\", "/")
            image_folder_output = mParams.image_folder_output.replace("\\", "/")

            FIS = mParams.fnFIS(image_folder_input, exts=(".jpg",))
            if mParams.Max_random_image_to_Aug > 0:
                FIS = [random.choice(FIS) for _ in range(mParams.Max_random_image_to_Aug)]
            nImg = len(FIS)
            nFiles = nImg
        else:
            A, B, options, Dir_input, Dir_Output = TS
            fis = mParams.fnFIS(Dir_input)
            Nfiles = len(fis)
            fDau = int((Nfiles * A/100) * (B - 1) ) # A: 10% B  # Đoạn mấy ?
            fCuoi =int( (Nfiles * A/100) * (B)  )

            image_folder_input = Dir_input.replace("\\", "/")
            image_folder_output = Dir_Output.replace("\\", "/")
            FIS = mParams.fnFIS(image_folder_input, exts=(".jpg",))
            nFiles=len(FIS)
            FIS = FIS[fDau:fCuoi]
            nImg = len(FIS)
        fCuoi=nImg
        print("Total files  :", nFiles)
        print("Working start:", fDau)
        print("Working End  :", fCuoi)

        if not exists(image_folder_output):
            os.makedirs(image_folder_output, exist_ok=True)

        for image_path in tqdm(FIS):
            image = cv2.imread(image_path)
            if image is None:
                print(f"Failed to read image: {image_path}")
                continue

            options ["image_path"]= image_path
            options ["Change_labels"]= True

            image_out, newLabel = self.Change_image_multiple_ways( image, image_path, options )
            fnOut = image_path.replace(image_folder_input, image_folder_output)
            label_inp = image_path.replace(".jpg", ".txt")
            label_out = fnOut.replace('.jpg', '.txt')

            os.makedirs(dirname(fnOut), exist_ok=True) 
            cv2.imwrite(fnOut, image_out)
            if mParams.Copy_label_when_save_augment_image:
                if newLabel:
                    with open(label_out, "w") as file:
                        file.write(newLabel)
                elif exists(label_inp):
                    if not exists(label_out):
                        shutil.copy(label_inp, label_out) 
            # print(".", end="", flush=True)

        print()
        print(f"Done augmenting {nImg} images to {image_folder_output}")

def Aug_Folder(TS=None):
    aug = ImageAugmentation()
    if TS is None:
        print("Working dir:", mParams.get_Home_Dir())
        if not mParams.Ready_to_run:
            print('Thay đổi tham số config trong file:', mParams.get_Home_Dir())
            return

        print("cover_yolo_string:", mParams.get("cover_yolo_string", False))
        print("Brightness:", mParams.get("Brightness", False))
        print("Shadow_Brightness:", mParams.get("Shadow_Brightness", False))
        print("Contrast:", mParams.get("Contrast", False))
        print("Saturation:", mParams.get("Saturation", False))
        print("Hue:", mParams.get("Hue", False))
        print( "Random_varian_delta_in_percent:", mParams.get("Random_varian_delta_in_percent", 10), )
        aug.Augment_folder(
            TS=None,
            cover_yolo_string=mParams.get("cover_yolo_string", False),
            cover_yolo_string__resize_after_crop_WH=mParams.get("cover_yolo_string__resize_after_crop_WH", False),
            Brightness=mParams.get("Brightness", False),
            Shadow_Brightness=mParams.get("Shadow_Brightness", False),
            Contrast=mParams.get("Contrast", False),
            Saturation=mParams.get("Saturation", False),
            Hue=mParams.get("Hue", False),
            Vibrance=mParams.get("Vibrance", False),
            Random_varian_delta_in_percent= mParams.get("Random_varian_delta_in_percent", 10),
        )
    else:
        aug.Augment_folder(TS=TS)


import cv2
import numpy as np


def draw_rectangles_and_show(
    iframe_org, bbox_list, title="Rectangles", waitkey=0, destroyWindows=True, Linewidth=2
):
    """
    Draw rectangles on image and display resized version

    Parameters:
    iframe_org: numpy array - Original input image
    bbox_list: list of [x1,y1,x2,y2] coordinates for rectangles
    """
    # Make a copy of original image to avoid modifying it
    image = iframe_org.copy()

    # Draw all rectangles on original size image
    for bbox in bbox_list:
        x1, y1, x2, y2 = [int(coord) for coord in bbox]
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), Linewidth)

    # Resize image for display
    display_image = cv2.resize(image, (800, 600))

    # Show image
    cv2.imshow(title, display_image)
    cv2.waitKey(waitkey)
    if destroyWindows:cv2.destroyAllWindows()

    return image, display_image


def draw_xyxyn_rectangles( iframe_org, bbox_list, resizeWH=None,COLOR=(0, 255, 0), Linewidth=2):
    """
    Draw rectangles on image and display resized version

    Parameters:
    iframe_org: numpy array - Original input image
    bbox_list: list of [x1,y1,x2,y2] coordinates for rectangles
    """
    # Make a copy of original image to avoid modifying it
    image = iframe_org
    H,W=image.shape[:2]
    # Draw all rectangles on original size image
    for bbox in bbox_list:
        x1, y1, x2, y2 = bbox  
        x1, x2=int(x1*W), int(x2*W) 
        y1, y2=int(y1*H), int(y2*H)
        cv2.rectangle(image, (x1, y1), (x2, y2), COLOR, Linewidth)
    if resizeWH is not None:
        image = cv2.resize(image, resizeWH)
    return image


def show_image(image, title="Image", waitkey=1, destroyWindows=False):
    cv2.imshow(title, image)
    cv2.waitKey(waitkey)
    if destroyWindows:
        cv2.destroyAllWindows()


import cv2
import numpy as np


def draw_yolo_boxes_and_show(iframe_org, bbox_list, waitkey=0, destroyWindows=True, Linewidth=2):
    """
    Draw rectangles from YOLO format coordinates and display resized version

    Parameters:
    iframe_org: numpy array - Original input image
    bbox_list: list of [x_center, y_center, width, height] YOLO format coordinates (normalized 0-1)
    """
    # Make a copy of original image to avoid modifying it
    image = iframe_org.copy()

    # Get image dimensions
    height, width = image.shape[:2]

    # Draw all rectangles on original size image
    for bbox in bbox_list:
        # Convert YOLO format to pixel coordinates
        x_center, y_center, w, h = bbox

        # Convert normalized coordinates to pixel values
        x_center = int(x_center * width)
        y_center = int(y_center * height)
        w = int(w * width)
        h = int(h * height)

        # Calculate corner points
        x1 = int(x_center - w / 2)
        y1 = int(y_center - h / 2)
        x2 = int(x_center + w / 2)
        y2 = int(y_center + h / 2)

        # Ensure coordinates are within image bounds
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(width, x2)
        y2 = min(height, y2)

        # Draw rectangle
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), Linewidth)

    # Resize image for display
    display_image = cv2.resize(image.copy(), (800, 600))

    cv2.imshow("Rectangles", display_image)
    cv2.waitKey(waitkey)
    if destroyWindows:
        cv2.destroyAllWindows()

    return image, display_image


def convert_xyxyn_coordinates_to_new_image(xyxyn, cropImage_xyxy, HW=None):
    """Chuyển đổi hệ trục tọa độ,
    Chúng ta có:
    - ảnh Im1 là ảnh gốc, ảnh to
    - ảnh Im2 là ảnh được crop từ ảnh Im1, là 1 phần của ảnh Im1, có vùng crop là: xr1, yr1, xr2, yr2 (size: cropH, cropW)) tọa độ này thuộc tọa độ ảnh Im1
    - ảnh Im3 là ảnh được resize (nhiều lần) từ ảnh Im2 => ta có ảnh cuối cùng là Im3, mang đi predict, có box: xyxyn (tọa độ xyxy nhưng tỷ lệ 0..1)

    Hàm này chuyển xyxyn (trên ảnh Im3) về tọa độ xyxy trên ảnh Im1.

    Nếu có HW thì sẽ chuyển về tọa độ xyxyn trên ảnh Im1. Lợi ích của việc dùng xyxyn là nó không bị ảnh hưởng khi resize.

    Args:
        xyxyn: x1, y1, x2, y2 của bbox thuộc khoảng 0..1
        cropImage_xyxy: x1, y1, x2, y2 của tọa độ khi crop ảnh từ ảnh gốc.

    Returns:
        xyxy hoặc xyxyn nếu HW != None
    """
    xr1, yr1, xr2, yr2 = cropImage_xyxy # Tọa độ crop trên ảnh Im1
    cropH = yr2-yr1 
    cropW = xr2-xr1
    xn1, yn1, xn2, yn2 = xyxyn
    x1, x2 =  cropW * xn1, cropW * xn2
    y1, y2 =  cropH * yn1, cropH * yn2
    x1 = x1 + xr1
    x2 = x2 + xr1
    y1 = y1 + yr1
    y2 = y2 + yr1
    if HW is not None:
        x1, x2 = x1 / HW[1], x2 / HW[1]
        y1, y2 = y1 / HW[0], y2 / HW[0]
    return x1, y1, x2, y2


def get_Org_xyxyn__from_Cropped_resized_bboxn(xyxyn, cropImage_xyxyn):
    """Chuyển đổi hệ trục tọa độ,
    
    Quy ước: xyxyn (tọa độ xyxy nhưng tỷ lệ 0..1)
     
    Chúng ta có:
    - ảnh Im1 là ảnh gốc, ảnh to
    - ảnh Im2 là ảnh được crop từ ảnh Im1, là 1 phần của ảnh Im1, có vùng crop là: `xr1, yr1, xr2, yr2` (size: `cropH, cropW`)) tọa độ này thuộc tọa độ ảnh Im1.
      Tọa độ này được convert vể xyxyn, đặt tên là `cropImage_xyxyn` .
    - ảnh Im3 là ảnh được resize (nhiều lần) từ ảnh Im2 => ta có ảnh cuối cùng là Im3, mang đi predict, có box: xyxyn  

    Hàm này chuyển xyxyn (trên ảnh Im3) về tọa độ xyxyn trên ảnh Im1. Lợi ích của việc dùng xyxyn là nó không bị ảnh hưởng khi resize.

    Args:
        xyxyn: x1, y1, x2, y2 của bbox (thuộc khoảng 0..1)
        cropImage_xyxyn: x1, y1, x2, y2 của tọa độ khi crop ảnh từ ảnh gốc (thuộc khoảng 0..1).

    Returns:
        xyxyn 
    """
    xr1, yr1, xr2, yr2 = cropImage_xyxyn  # Tọa độ crop trên ảnh Im1
    x1, y1, x2, y2 = xyxyn
    x1 = x1 * (xr2 - xr1) + xr1
    x2 = x2 * (xr2 - xr1) + xr1
    y1 = y1 * (yr2 - yr1) + yr1
    y2 = y2 * (yr2 - yr1) + yr1
    xyxyn = (x1, y1, x2, y2)
    return xyxyn


if __name__ == "__main__":
    RUN=1
    if RUN==1:
        Aug_Folder()
    if RUN==2:
        import numpy as np
        aug = ImageAugmentation()
        iframe_org = cv2.imread("d:/iframe_org.jpg")
        with open("d:/retDict.pkl", "rb") as handle:
            retDict = pickle.load(handle)

        with open("d:/results.pkl", "rb") as handle:
            results = pickle.load(handle)

        # =========================================
        for k, box in enumerate(results.boxes):
            # x1, y1, x2, y2 = np.array(box.xyxy.cpu(), dtype=np.dtype(np.int_)).squeeze()
            xyxyn = list( tuple(np.array(box.xyxyn.cpu(), dtype=np.dtype(np.float_)).squeeze()) )
            xyxy = list( tuple(np.array(box.xyxy.cpu(), dtype=np.dtype(np.float_)).squeeze()) )

            confidence = float(box.conf.cpu())

            img = results[k].plot()  # This plots the detections on the image
            print("{}".format(img.shape,))
            # Convert BGR to RGB (OpenCV uses BGR by default)
            # img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            x1, y1, x2, y2=xyxy
            draw_rectangles_and_show(img, [[x1, y1, x2, y2]], title='aaa111', waitkey=1, destroyWindows=False, Linewidth=2)
            # cv2.imshow('Detection Results', img)
            # cv2.waitKey(1)

            x1,y1,x2,y2 = retDict["cropImage_xyxy"]
            H,W=retDict["orgImageHW"]
            x1, x2 = x1/W, x2/W
            y1, y2 = y1/H, y2/H
            retDict["cropImage_xyxyn"] =(x1,y1,x2,y2)
            restore_options = {
                "orgImageHW": retDict["orgImageHW"],
                # "cropImage_xyxy": retDict["cropImage_xyxy"], 
                "cropImage_xyxyn": retDict["cropImage_xyxyn"], 
                "resizeImageHW": retDict["resizeImage"],
                "xyxyn": xyxyn,
                # "xyxy": xyxy,
            }
            print(restore_options)
            # ret = aug.restore_coordinates(iframe_org, restore_options)
            H_predict, W_predict = results.orig_shape
            H, W = restore_options["orgImageHW"]
            # x_center, y_center, box_width, box_height = xyxyn
            # x1, y1, x2, y2 = retDict["cropImage_xyxy"]
            # draw_rectangles_and_show(iframe_org, [[x1, y1, x2, y2]], title='aaa', waitkey=1, destroyWindows=False, Linewidth=4)
            # draw_rectangles_and_show(
            #     img, [xyxy], title="bbbb", waitkey=1, destroyWindows=False
            # )

            # ret = convert_xyxyn_coordinates_to_new_image( xyxyn=xyxyn, cropImage_xyxy=retDict["cropImage_xyxy"], HW=restore_options["orgImageHW"] )

            # print(ret)
            # print()
            # bbox_list = [ret]
            # # draw_rectangles_and_show(iframe_org, bbox_list)
            # draw_rectangles_and_show(iframe_org, bbox_list, Linewidth=5,waitkey=1,)
            cropImage_xyxyn = retDict["cropImage_xyxyn"]
            ret1 = get_Org_xyxyn__from_Cropped_resized_bboxn(xyxyn, cropImage_xyxyn)
            pp(ret1)
            iframe_org=draw_xyxyn_rectangles(iframe_org, [ret1], COLOR=(0,0,255), Linewidth=3)
            taImshow(image=iframe_org,)

        # print(ret)
# cv2.imshow("img", iframe[70:106,0:5]);cv2.waitKey(0)
