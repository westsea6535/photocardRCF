import os
import cv2
import numpy as np



# 폴더 경로 설정
base_folder = './image_processing/augmentation/photocard'
data_folder = f'{base_folder}/data'
gt_folder = f'{base_folder}/gt'
aug_data_folder = f'{base_folder}/aug_data'
aug_data_scale_05_folder = f'{base_folder}/aug_data_scale_0.5'
aug_data_scale_15_folder = f'{base_folder}/aug_data_scale_1.5'
aug_gt_folder = f'{base_folder}/aug_gt'
aug_gt_scale_05_folder = f'{base_folder}/aug_gt_scale_0.5'
aug_gt_scale_15_folder = f'{base_folder}/aug_gt_scale_1.5'

# 회전 각도 설정
angles = [i * 90 for i in range(4)]

# 폴더 생성 함수
def create_folder_structure(base_folder, angles):
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)
    for angle in angles:
        os.makedirs(os.path.join(base_folder, f'{int(angle)}_1_1'), exist_ok=True)
        os.makedirs(os.path.join(base_folder, f'{int(angle)}_1_0'), exist_ok=True)

# 폴더 구조 생성
create_folder_structure(aug_data_folder, angles)
create_folder_structure(aug_data_scale_05_folder, angles)
create_folder_structure(aug_data_scale_15_folder, angles)
create_folder_structure(aug_gt_folder, angles)
create_folder_structure(aug_gt_scale_05_folder, angles)
create_folder_structure(aug_gt_scale_15_folder, angles)

# 이미지 증강 함수
def augment_image(image, gt_image, base_name, angle, flip_code, scale, output_folder_image, output_folder_gt):
    # 회전
    h, w = image.shape[:2]
    if angle in [90, 270]:
        new_w, new_h = h, w
    else:
        new_w, new_h = w, h
    center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, angle, 1)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # Compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # Adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - center[0]
    M[1, 2] += (nH / 2) - center[1]

    rotated_image = cv2.warpAffine(image, M, (nW, nH))
    rotated_gt_image = cv2.warpAffine(gt_image, M, (nW, nH))

    # 플립
    if flip_code != -1:
        flipped_image = cv2.flip(rotated_image, flip_code)
        flipped_gt_image = cv2.flip(rotated_gt_image, flip_code)
    else:
        flipped_image = rotated_image
        flipped_gt_image = rotated_gt_image

    # 스케일링
    scaled_image = cv2.resize(flipped_image, (0, 0), fx=scale, fy=scale)
    scaled_gt_image = cv2.resize(flipped_gt_image, (0, 0), fx=scale, fy=scale)

    # 파일명 설정
    flip_suffix = f'1_{1 if flip_code == 1 else 0}'
    angle_str = f'{int(angle)}_{flip_suffix}'
    image_output_path = os.path.join(output_folder_image, angle_str, base_name)
    gt_output_path = os.path.join(output_folder_gt, angle_str, f"{os.path.splitext(base_name)[0]}.png")

    # 저장
    cv2.imwrite(image_output_path, scaled_image)
    cv2.imwrite(gt_output_path, scaled_gt_image)


# 데이터 증강 수행
for filename in os.listdir(data_folder):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        base_name = os.path.basename(filename)
        image_path = os.path.join(data_folder, filename)
        gt_filename = f"{os.path.splitext(base_name)[0]}_2px.png"
        gt_path = os.path.join(gt_folder, gt_filename)
        
        image = cv2.imread(image_path)
        gt_image = cv2.imread(gt_path)  # gt는 흑백 이미지로 가정
        
        for angle in angles:
            for flip_code in [-1, 1]:  # -1: no flip, 0: x-axis flip
                # 원본 스케일
                augment_image(image, gt_image, base_name, angle, flip_code, 1.0, aug_data_folder, aug_gt_folder)
                # 0.5배 스케일
                augment_image(image, gt_image, base_name, angle, flip_code, 0.5, aug_data_scale_05_folder, aug_gt_scale_05_folder)
                # 1.5배 스케일
                augment_image(image, gt_image, base_name, angle, flip_code, 1.5, aug_data_scale_15_folder, aug_gt_scale_15_folder)
