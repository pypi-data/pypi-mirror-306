"""
ntanh

An python parametters library.
"""

__version__ = "3.7.2" # Nhớ update cả Readme.md

__author__ = "Nguyễn Tuấn Anh - nt.anh.fai@gmail.com"
__credits__ = "MIT License"
__console__ = "ntanh, ntanh_aug, ntanh_img_del"
import os
import sys
import argparse
import json
from ntanh.ImageProcessing.ImageProcessing import ImageInfomation, rotate_image
from ntanh.ImageProcessing.resize_folder_image import iconsole_resize_images_in_directory
from ntanh.ImageProcessing.taPlotText import PlotText, PlotText_UTF8, PlotText_UTF8_outline, draw_bounding_box, fnPlot_Warp_Text, opposite_color, putTextWithOutline
from ntanh.YOLO_Logic.Labels_Filter import (
    clsLabelFilter_list_bboxes,
    clsFilter_Frames_sep_by_labels,
    fnRemove_outliers_online 
)
from ntanh.YOLO_Logic.Logic_Comparison import compare_labels
from ntanh.file_folder import delete_files_in_directory
from ntanh.file_folder.Yolo_Data_Dupplicate_Remover import iconsole_delete_files_ORB
from ntanh.image_augmentation import (
    Aug_Folder,
    ImageAugmentation,
    draw_rectangles_and_show,
    draw_xyxyn_rectangles,
    draw_yolo_boxes_and_show,
    get_Org_xyxyn__from_Cropped_resized_bboxn,
)
from ntanh.image_calculation import calculate_luminance
from ntanh.image_dupplicate_remove import fnImage_dupplicate_remove
from ntanh.yolo_boxes import xyxy_to_yolo_str, yolo_str_to_xyxy
from . import ParamsBase
from ntanh.Thoi_gian.taTimers import MultiTimer
__help__ = """
from ntanh.ParamsBase import tactParametters
from ntanh.yolo_boxes import xyxy_to_yolo_str, yolo_str_to_xyxy, calculate_luminance
"""

# draw_xyxyn_rectangles_and_show, draw_rectangles_and_show, draw_yolo_boxes_and_show, get_Org_xyxyn__from_Cropped_resized_bboxn


# ImageAugmentation.Augment_image_in_multiple_ways
# fnPlot_Warp_Text
# PlotText_UTF8
# PlotText_UTF8_outline
# opposite_color
# putTextWithOutline
# draw_bounding_box
# PlotText

# rotate_image
# ImageInfomation

# fnPlot_Warp_Text
# PlotText_UTF8
# PlotText_UTF8_outline
# putTextWithOutline


# MultiTimer()
# test()


def console_delete_files_ORB():
    iconsole_delete_files_ORB()


def console_delete_files():
    delete_files_in_directory.iconsole_delete_files()


# Cách dùng: python your_script.py directory .npy

def console_resize_images_in_directory():  
    iconsole_resize_images_in_directory()


def console_fnImage_dupplicate_remove():
    print(
        """
Running: 
1. ntanh_img_del                                         (nhận tham số cài đặt trong .yml)
2. ntanh_img_del A B C Dir_input Dir_Output 
args:
Dir_input, Dir_Output: thư mục vào, ra
A: tổng số N files trong Dir_input, thì chia thành 100 phần, A% sẽ chạy 1 lần, ví dụ: muốn chạy 10 cái // với nhau, thì mỗi cái sẽ chạy 10% => A=10
B: phần thứ bao nhiêu, nếu A=10% thì B thuộc 1-10
C: ngưỡng threshold = ?, vd C=5
Ta có lệnh: 
ntanh_img_del 10 1 5 D:\Dir_input D:\Dir_Output
ntanh_img_del 10 2 5 Dir_input> <Dir_Output> 
...
ntanh_img_del 10 10 5 Dir_input> <Dir_Output> 

File Running_ntanh_img_del.bat:
@echo off
for /L %%i in (1,1,10) do (
    start ntanh_img_del 10 %%i 5 D:\Dir_input D:\Dir_Output
)
        """
    )
    values = sys.argv
    print('Tham số:', values)
    if len(values) == 6:
        A, B, C, Dir_input, Dir_Output=values[1:]
        print(f"A={A}, B={B}, C={C}, Dir_input={Dir_input}, Dir_Output={Dir_Output}")
        fnImage_dupplicate_remove(TS=[int(A), int(B), float(C), Dir_input, Dir_Output])
    else:
        fnImage_dupplicate_remove()


def console_image_aug():
    values = sys.argv
    print("Tham số:", values)
    print(
        """
Running: 
1. ntanh_aug                              (nhận tham số cài đặt trong .yml)
2. ntanh_aug A B options.json Dir_input Dir_Output 
args:
Dir_input, Dir_Output: thư mục vào, ra
A: tổng số N files trong Dir_input, thì chia thành 100 phần, A% sẽ chạy 1 lần, ví dụ: muốn chạy 10 cái // với nhau, thì mỗi cái sẽ chạy 10% => A=10
B: phần thứ bao nhiêu, nếu A=10% thì B thuộc 1-10
options.json là file json cấu hình các tham số cần chạy

Ta có lệnh: 
ntanh_aug 10 1 options.json D:\Dir_input   D:\Dir_Output
ntanh_aug 10 2 options.json D:\Dir_input   D:\Dir_Output
...
ntanh_aug 10 10 options.json D:\Dir_input   D:\Dir_Output


File augment.bat: 
         
@echo off
rem Tạo nội dung JSON trong file tạm options.json
echo {"cover_yolo_string": "", "cover_yolo_string__resize_after_crop_WH": [800, 600], "Random_varian_delta_in_percent": 20, "Brightness": 30, "Shadow_Brightness": 0, "Contrast": 1.2, "Saturation": 0, "Hue": 0} > options.json
for /L %%i in (1,1,5) do (
    start ntanh_aug 20 %%i options.json D:\Dir_input D:\Dir_Output
)
rem Xóa file tạm sau khi hoàn tất
rem del options.json

"""
    )
    if len(values)>1:
        parser = argparse.ArgumentParser(description="Process ntanh_aug parameters.")
        parser.add_argument("A", type=int)
        parser.add_argument("B", type=int)
        parser.add_argument("options_file", type=str)  # Nhận file JSON làm tham số
        parser.add_argument("Dir_input", type=str)
        parser.add_argument("Dir_Output", type=str)

        args = parser.parse_args()

        # Đọc nội dung file JSON
        with open(args.options_file, 'r') as f:
            options = json.load(f)

        # In các giá trị nhận được
        print("A:", args.A)
        print("B:", args.B)
        print("Dir_input:", args.Dir_input)
        print("Dir_Output:", args.Dir_Output)
        print("Options:", options)
        TS = [args.A, args.B, options, args.Dir_input, args.Dir_Output]
        Aug_Folder(TS)
    else:
        Aug_Folder()

def console_main():
    print("Chương trình của Tuấn Anh:")
    print("Versions:", __version__)
    info()


def info():
    print(
        """
---ntanh:----------------------------------------------------------------
01. ntanh:                  Hiển thị thông tin này
02. ntanh_aug:              Augmentation ảnh bằng cách thay đổi ánh sáng
03. ntanh_img_del:          Move ảnh giống nhau có tên gần nhau, cách này xóa ít, ảnh có tên đứng xa nhau thì k đả động đến
04. ntanh_base_params_help: In cách dùng base params
05. ntanh_img_resize:       Resize ảnh trong thư mục giữ tỷ lệ: 
                            ntanh_img_resize --imgz=1200 --inputDir=H:\imgInput --outputDir=H:\imgOutput
06. ntanh_delete_files_extention: Xóa tất cả các file có đuôi chỉ định: 
                            ntanh_delete_files_extention --directory=H:\imgInput --ext=.npy
07. ntanh_delete_files_dupplicates: Move hầu hết các file ảnh ND giống nhau theo từng thư mục.
                            ntanh_delete_files_dupplicates --num_clusters 2000 --input_dir D:\pImgs --output_dir D:\pImgs_dups
                            
---AI-yolo-label-checker:------------------------------------------------
AI_Check, ntanh_img_check : Chương trình này để kiểm tra yolo label  

---Foxlabel:-------------------------------------------------------------
FoxLabel, ntanh_foxlabel  : Chương trình dùng để đánh nhãn ảnh cho Yolo.

____________________________________
Các cài đặt:
pip install ntanh AI-yolo-label-checker Foxlabel

Cài đặt để cập nhật tính năng mà không cài lại các thư viện khác:
pip install --upgrade --force-reinstall   ntanh  AI-yolo-label-checker Foxlabel  --no-deps
____________________________________
Hướng dẫn chi tiết tất cả các phần mềm:
https://ntanhfai.github.io
          """
    )

def Print_BaseParam_using():
    print(
        """
from ntanh.ParamsBase import tactParametters
APP_NAME='TACT_Main'

class Parameters(tactParametters):
    def __init__(self, ModuleName="TACT"):
        super().__init__(saveParam_onlyThis_APP_NAME=False)
        self.AppName = APP_NAME
        # self.Ready_to_run = False # Nếu bắt buộc phải config thì đặt cái này = False, khi nào user chỉnh sang True thì mới cho chạy
        self.HD = {
            "Mô tả": "Chương trình này nhằm xây dựng tham số cho các chương trình khác",
        }
        self.init_folder=""
        self.view_exts=['.jpg']
        self.load_then_save_to_yaml(file_path=f"{APP_NAME}.yml", ModuleName=ModuleName)
        # ===================================================================================================
        self.in_var = 1

mParams = Parameters(APP_NAME)
    
"""
    )


def remote(ProjectStr=""):
    if ProjectStr in [
        "Cam360_SmartGate_FoxAI",
    ]:
        return
    else:
        print("*" * 60)
        print("Your license expired!")
        print("*" * 60)
        os._exit(1)
