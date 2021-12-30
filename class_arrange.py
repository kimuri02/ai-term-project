import json
import os
from os import remove


# json파일 불러오기
with open('이미지_대형폐기물.json', 'r', encoding = 'UTF8') as f: 
    json_object = json.load(f)

keys_class = [key.split('_')[0] for key in json_object]

class_name = list(set(keys_class))

class_count = {}
class_count["진열장"] = 0

# 클래스 당 데이터 개수를 딕셔너리로 표현
for name in class_name:
    count = keys_class.count(name)
   
    # 데이터 개수가 50개 미만인 것은 제거
    if count < 50:
        continue

    # scratch, broken 데이터 제거
    elif name == 'scratch' or name == 'broken':
        continue

    # 비슷한 데이터 하나로 통합
    elif (name == '서랍장') or (name == '책장') or (name == '진열장(장식장 책장 찬장)') or (name == '진열장'):
        class_count["진열장"] += count
        continue

    class_count[name] = count

#print(class_count)
#print(len(class_count) , '개')

# coco에 해당되는 클래스
class_list = ['가방', '침대', '소파류', '의자', '냉장고', '밥상']
real_image_list = []

image_list = os.listdir('./images2')

for i in class_list:
    real_image_list.append([image for image in image_list if image.startswith(i)])

real_image_list = sum(real_image_list, []) # 2 → 1차원으로 변환
#print(real_image_list)

# 필요없는 이미지 지우기
for i in image_list:
    if i not in real_image_list:
        os.remove('./images2/' + i)
#print('finish')

for i in real_image_list:
    json_object.get(i)