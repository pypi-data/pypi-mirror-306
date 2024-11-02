import cv2
import os
import argparse
import shutil
from tqdm import tqdm

def resize_images_in_directory(input_dir, fx=1.0, fy=1.0, output_dir=None, min_size=0, imgz=None):
    if not os.path.exists(input_dir):
        print(f"Đường dẫn không tồn tại: {input_dir}")
        return

    output_dir = output_dir or input_dir

    # Đếm tổng số lượng ảnh trong toàn bộ thư mục
    total_images = sum(
        len([file for file in files if file.lower().endswith(('.jpg', '.jpeg', '.png'))])
        for _, _, files in os.walk(input_dir)
    )

    # Sử dụng tqdm cho tiến trình tổng thể
    with tqdm(total=total_images, desc="Resizing images", unit="image") as total_progress:
        for root, dirs, files in os.walk(input_dir):
            # Chỉ lấy các file ảnh
            image_files = [file for file in files if file.lower().endswith(('.jpg', '.jpeg', '.png'))]
            
            # Tạo tqdm cho tiến trình của thư mục hiện tại
            with tqdm(total=len(image_files), desc=f"Processing {root}", leave=False) as folder_progress:
                for file in image_files:
                    image_path = os.path.join(root, file)
                    image = cv2.imread(image_path)

                    if image is None:
                        print(f"Lỗi khi đọc ảnh: {image_path}")
                        folder_progress.update(1)
                        total_progress.update(1)
                        continue

                    # Kiểm tra kích thước ảnh so với min_size
                    height, width = image.shape[:2]
                    if max(width, height) <= min_size:
                        print(f"Bỏ qua ảnh {image_path} vì kích thước nhỏ hơn hoặc bằng {min_size}px")
                        folder_progress.update(1)
                        total_progress.update(1)
                        continue
                    
                    # Resize cạnh lớn nhất về tham số imgz nếu có
                    if imgz is not None:
                        if width > height:
                            scale = imgz / width
                        else:
                            scale = imgz / height
                        fx = fy = scale  # Thiết lập tỷ lệ resize cho cả hai chiều

                    # Thay đổi kích thước ảnh
                    resized_image = cv2.resize(image, None, fx=fx, fy=fy, interpolation=cv2.INTER_LINEAR)

                    # Tạo đường dẫn lưu giữ cấu trúc thư mục con
                    save_path = os.path.join(output_dir, os.path.relpath(image_path, input_dir))
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)

                    # Lưu ảnh đã thay đổi kích thước
                    cv2.imwrite(save_path, resized_image)

                    # Kiểm tra và sao chép file .txt nếu tồn tại
                    txt_file_path = os.path.splitext(image_path)[0] + ".txt"
                    if os.path.exists(txt_file_path):
                        txt_save_path = os.path.join(output_dir, os.path.relpath(txt_file_path, input_dir))
                        if not os.path.exists(txt_save_path):
                            shutil.copy2(txt_file_path, txt_save_path)

                    # Cập nhật tiến trình của thư mục và tổng thể
                    folder_progress.update(1)
                    total_progress.update(1)

def iconsole_resize_images_in_directory():
    parser = argparse.ArgumentParser( description="Resize images in a directory and copy associated .txt files if present. Ví dụ: " )
    parser.add_argument("--imgz", type=int, default=None, help="Kích thước cạnh lớn nhất để resize ảnh, nếu có giá trị, nó sẽ bỏ qua fx, fy, ví dụ: 1200")
    parser.add_argument("--fx", type=float, default=1.0, help="Tỷ lệ chiều rộng (fx) để resize ảnh, mặc đinh=1.0, phóng to: >1, thu nhỏ: <1")
    parser.add_argument("--fy", type=float, default=1.0, help="Tỷ lệ chiều cao (fy) để resize ảnh, mặc đinh=1.0, phóng to: >1, thu nhỏ: <1")
    parser.add_argument("--inputDir", type=str, required=True, help="Đường dẫn đến thư mục chứa ảnh, bắt buộc")
    parser.add_argument("--min_size", type=int, default=1200, help="Kích thước tối thiểu (cả W và H) để resize ảnh, mặc định =1200")
    parser.add_argument("--outputDir", type=str, help="Đường dẫn đến thư mục xuất ảnh sau khi resize, tùy chọn, mặc định = inputDir (resize bản gốc)")

    args = parser.parse_args()

    # Kiểm tra tham số đầu vào
    if not args.inputDir:
        print("Vui lòng cung cấp tham số inputDir")
        return

    # Kiểm tra các tham số fx, fy không âm
    if args.fx < 0 or args.fy < 0:
        print("fx và fy phải là giá trị không âm.")
        return
    
    # Nếu imgz được cung cấp, đặt fx, fy về 1.0
    if args.imgz is not None:
        args.fx = 1.0
        args.fy = 1.0

    print("Đang xử lý với các tham số sau:")
    print("inputDir:", args.inputDir)
    print("fx:", args.fx)
    print("fy:", args.fy)
    print("outputDir:", args.outputDir or "Sử dụng thư mục đầu vào")
    print("min_size:", args.min_size)
    print("imgz:", args.imgz)

    resize_images_in_directory(args.inputDir, args.fx, args.fy, args.outputDir, args.min_size, args.imgz)


if __name__ == "__main__":
    iconsole_resize_images_in_directory()
