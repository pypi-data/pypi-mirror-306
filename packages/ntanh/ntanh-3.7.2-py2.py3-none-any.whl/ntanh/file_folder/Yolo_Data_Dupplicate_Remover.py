import os
import cv2
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from tqdm import tqdm
from collections import defaultdict
import shutil


def extract_orb_features(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    orb = cv2.ORB_create()
    keypoints, descriptors = orb.detectAndCompute(image, None)
    return descriptors


def cluster_images(image_paths, num_clusters=10):
    descriptors_list = []
    descriptors_map = {}

    for img_path in tqdm(image_paths, desc="Extracting ORB features", leave=False):
        descriptors = extract_orb_features(img_path)
        if descriptors is not None:
            descriptors_list.extend(descriptors)
            descriptors_map[img_path] = descriptors

    if not descriptors_list:
        print("No descriptors found in the current folder. Skipping...")
        return {}

    print("Clustering features...")
    
    # Kiểm tra số lượng mẫu và điều chỉnh num_clusters nếu cần
    n_samples = len(descriptors_list)
    if n_samples < num_clusters:
        print(f"Number of samples ({n_samples}) is less than num_clusters ({num_clusters}). Adjusting num_clusters.")
        num_clusters = n_samples  # Điều chỉnh num_clusters về số lượng mẫu

    batch_size = num_clusters * 2
    if n_samples <= batch_size:
        batch_size = n_samples

    kmeans = MiniBatchKMeans(n_clusters=num_clusters, random_state=0, batch_size=batch_size)

    num_batches = n_samples // batch_size + 1

    for i in tqdm(range(num_batches), desc="Clustering with MiniBatchKMeans", leave=False):
        batch_data = descriptors_list[i * batch_size: (i + 1) * batch_size]
        if batch_data:
            kmeans.partial_fit(batch_data)

    # Nhóm các ảnh theo nhãn của cụm
    clusters = defaultdict(list)
    for img_path, descriptor in tqdm(descriptors_map.items(), desc="Assigning images to clusters", leave=False):
        label = kmeans.predict([descriptor[0]])[0]
        clusters[label].append(img_path)

    return clusters


def move_duplicates(clusters, dir_out, image_folder):
    MovedFiles = 0
    for cluster_label, image_paths in tqdm(clusters.items(), desc="Moving duplicates"):
        if len(image_paths) > 1:
            for duplicate_image in image_paths[1:]:
                relative_path = os.path.relpath(duplicate_image, image_folder)
                destination_path = os.path.join(dir_out, relative_path)

                os.makedirs(os.path.dirname(destination_path), exist_ok=True)

                try:
                    shutil.move(duplicate_image, destination_path)

                    # Di chuyển file nhãn (nếu có)
                    label_path = os.path.splitext(duplicate_image)[0] + ".txt"
                    destination_label = os.path.splitext(destination_path)[0] + ".txt"
                    if os.path.exists(label_path):
                        shutil.move(label_path, destination_label)
                    MovedFiles += 1
                except Exception as e:
                    print(f"Move error: {e}")
    print(f"{MovedFiles} files moved")


def process_folder(image_folder, dir_out, num_clusters=500):
    # Lấy tất cả đường dẫn ảnh trong thư mục
    image_paths = [
        os.path.join(image_folder, f)
        for f in os.listdir(image_folder)
        if f.endswith((".jpg", ".png", ".jpeg"))
    ]

    if len(image_paths) == 0:
        print(f"No images found in folder {image_folder}. Skipping...")
        return

    # Phân cụm ảnh dựa trên đặc trưng ORB và phân cụm MiniBatchKMeans
    clusters = cluster_images(image_paths, num_clusters=num_clusters)

    print(f"Moving duplicates for folder: {image_folder}")
    move_duplicates(clusters, dir_out, image_folder)


def main_Yolo_Data_Dupplicate_Remover(input_dir, output_dir, num_clusters=500):
    for root, dirs, files in os.walk(input_dir):
        # Chỉ xử lý các thư mục con chứa ít nhất một ảnh
        image_files = [f for f in files if f.endswith((".jpg", ".png", ".jpeg"))]
        if image_files:
            print(f"Processing folder: {root}")
            corresponding_output_dir = root.replace(input_dir, output_dir)
            process_folder(root, corresponding_output_dir, num_clusters=num_clusters)
        print()


def iconsole_delete_files_ORB():
    import argparse

    parser = argparse.ArgumentParser( description="Tính toán độ trùng lặp của nội dung ảnh chung trong 1 thư mục, lặp lại cho các thư mục con.")
    parser.add_argument( "--num_clusters", type=int, default=2000, help="Số lớp tối đa sẽ phân cụm theo ORB" )
    parser.add_argument( "--input_dir", type=str, help="Đường dẫn đến thư mục cần di chuyển các file đi" )
    parser.add_argument( "--output_dir", type=str, help="Đường dẫn đến thư mục cần di chuyển file đến" )

    args = parser.parse_args()

    print("Thực hiện di chuyển các file giống nhau với tham số:")
    print("num_clusters:", args.num_clusters)
    print("input_dir:", args.input_dir)
    print("output_dir:", args.output_dir)

    main_Yolo_Data_Dupplicate_Remover(args.input_dir, args.output_dir, args.num_clusters)


if __name__ == "__main__":
    # input_dir = r"E:\TA_training\26_09"
    # output_dir = r"E:\TA_training\26_09_Dupp"

    # main_Yolo_Data_Dupplicate_Remover(input_dir, output_dir, num_clusters=2000)
    iconsole_delete_files_ORB()
