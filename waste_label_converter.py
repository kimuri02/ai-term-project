import os
import json
import cv2


# row data class
# translate_dict = {
#     "고무통" : "rubber", "차탁자" : "teatable",
#     "옥매트" : "jademat", "텔레비젼" : "tv",
#     "쓰레기통" : "bin", "정수기" : "coway",
#     "텐트" : "tent", "돗자리" : "mat",
#     "피아노" : "piano", "거울" : "mirror",
#     "골프가방" : "golfbag", "파티션" : "partition",
#     "캐비닛류" : "cabinet", "침대" : "bed",
#     "에어콘" : "aircon", "커튼" : "curtain",
#     "베개" : "pillow", "타이어" : "tire",
#     "선풍기" : "fan", "개수대류" : "sink",
#     "옷걸이류" : "hanger", "전기담요" : "electromat",
#     "아이스박스" : "icebox", "유모차" : "babycar",
#     "세탁기" : "washmachine", "입간판" : "standbanner",
#     "조명기구" : "light", "러닝머신" : "runningmachine",
#     "난로" : "stove", "다리미판" : "irontable",
#     "프린트기" : "printer", "액자" : "angle",
#     "변기통" : "toilet", "가스오븐레인지" : "gasrange",
#     "블라인드" : "blind", "병풍" : "foldingscreen",
#     "청소기" : "vacuum", "장우산류" : "umbrella",
#     "오디오장식장" : "audiocabinet", "히터류" : "heater",
#     "장롱" : "closet", "카펫" : "carpet",
#     "욕조" : "bath", "항아리류" : "pot",
#     "헬스자전거" : "cycle", "전축(오디오)" : "audio",
#     "가방" : "bag", "의자" : "chair",
#     "화장대" : "cosmetictable", "화장품함" : "cosmeticbox",
#     "스피커" : "speaker", "복사기" : "printer",
#     "장식장" : "display", "텔레비전대" : "tvtable",
#     "방석" : "sheet", "신발장" : "shoescloset",
#     "장판" : "longmat", "협탁" : "sidetable",
#     "진열장(장식장 책장 찬장)" : "display", "빨래건조대" : "dryhanger",
#     "이불등" : "corver", "문짝" : "door",
#     "비데" : "bidet", "식기건조기" : "dishdryer",
#     "도마" : "coatingboard", "벽걸이시계" : "clock",
#     "소파류" : "sofa", "밥상" : "diningtable",
#     "자전거" : "bike", "책상" : "desk",
#     "책꽂이" : "bookshelves", "보행기" : "babywalker",
#     "쌀통" : "ricebox", "김치냉장고" : "refri",
#     "식탁" : "table", "책장" : "bookshelves",
#     "냉장고" : "refri", "서랍장" : "drawer",
#     "완구류" : "toy"
# }

# class arrange
translate_dict = {'가방':'bag','침대':'bed', '의자':'chair', '밥상':'diningtable', '냉장고':'refri', '소파류':'sofa'}


class_list = list(translate_dict.keys())

with open('./이미지_대형폐기물.json', 'r') as j:
    json_file = json.load(j)    
    
    img_list = os.listdir('./waste_data/images4')
    count = 0
    
    for img in img_list:
        count += 1
        image = cv2.imread('./waste_data/images4/' + img)
        h, w, c = image.shape
        
        name = img.split('.')[0]
        name_kor = name.split('_')[0]
        serial_number = name.split('_')[1]
        
        os.rename('./waste_data/images4/{}'.format(img), './waste_data/images4/{}_{}.jpg'.format(translate_dict.get(name_kor), serial_number))
        
        crd = json_file.get(img)
        
        # make label data (txt file)
        with open('./waste_data/labels4/{}_{}.txt'.format(translate_dict.get(name_kor), serial_number), 'w') as f:
            
            xmin = crd[0][0] / w
            ymin = crd[0][1] / h
            xmax = crd[1][0] / w
            ymax = crd[1][1] / h
        
            f.write("{} {} {} {} {}".format(class_list.index(name_kor), (xmin+xmax)/2, (ymin+ymax)/2, (xmax-xmin), (ymax-ymin))) # (x,y,x2,y2) >> (x,y,w,h)