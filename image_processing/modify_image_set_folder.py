import os
import shutil
from PIL import Image


# 폴더 이름 설정
source_folder = os.path.abspath("./imagesWithEdge/png")
px2 = os.path.join(source_folder, '2px')
px3 = os.path.join(source_folder, '3px')

# 폴더 생성
os.makedirs(px2, exist_ok=True)
os.makedirs(px3, exist_ok=True)

# 파일 이동 및 처리
for filename in os.listdir(source_folder):
    file_path = os.path.join(source_folder, filename)
    
    if os.path.isfile(file_path):
        if filename.lower().endswith('2px.png'):
            shutil.move(file_path, px2)
        if filename.lower().endswith('3px.png'):
            shutil.move(file_path, px3)


print("파일 처리가 완료되었습니다.")
