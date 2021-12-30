import os
import cv2
import numpy as np

import torch

from yolov5.models.yolo import Model
from yolov5.models.experimental import attempt_load

from yolov5.utils.datasets import LoadImages
from yolov5.utils.general import check_img_size, non_max_suppression, scale_coords
from yolov5.utils.plots import Annotator, colors

src_path_root = "/home/user/yuri/ai-term-project/waste_data/images/"

print(os.listdir(src_path_root))
file_name = input("Insert File Name : ")

imgsz = 640
conf_thres = 0.25
iou_thres = 0.45
classes = None
agnostic_nms = False
max_det = 1000
line_thickness = 3

src = src_path_root + file_name
model = attempt_load("/home/user/yuri/ai-term-project/yolov5/runs/train/exp97/weights/best.pt", map_location='cpu')
print(src)

stride = int(model.stride.max())
names = model.names

dataset = LoadImages(src, img_size=imgsz, stride=stride, auto=True)

for path, img, im0s, vid_cap in dataset:

    img = torch.from_numpy(img).to('cpu')
    img = img.float()
    img /= 255.0
    
    if len(img.shape) == 3:
        img = img[None]  
    pred = model(img, False, False)[0]
    pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)

    print("---------------------------")
    print(pred)
    print("---------------------------")

    for i, det in enumerate(pred):
        
        p, s, im0, frame = path[i], f'{i}: ', im0s.copy(), dataset.count

        annotator = Annotator(im0, line_width=line_thickness, example=str(names))
        im0 = annotator.result()

        if len(det):
            
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
            
            for cl in det[:, -1].unique():
                n = (det[:, -1] == cl).sum()
                s += f"{n} {names[int(cl)]}{'s' * (n > 1)}, "
                name = s.split(' ')[2].split(',')[0]
            print(name)
            
            for *xyxy, conf, cls in reversed(det):

                c = int(cls) 
                label = f'{names[c]} {conf:.2f}'
                annotator.box_label(xyxy, label, color=colors(c, True))
                
            # Predict price
            price_dict = {'bag':[2000, 3000], 'bed':[5000, 8000, 19000, 22000, 28000], 'chair':[2000], 'diningtable':[2000, 3000], 'refir':[4000, 6000, 8000], 'sofa':[3000, 5000, 7000, 9000]} 
            name = s.split(' ')[2].split(',')[0]
            
            print('-----------------------------')
            if len(price_dict[name]) == 1:
                print('Predict price : {}'.format(price_dict[name][0]))
            else:
                print('Predict price : {} ~ {}'.format(price_dict[name][0], price_dict[name][-1]))
            print('-----------------------------')
            
            h, w, c = im0.shape
            im0 = cv2.resize(im0, (int(w/3), int(h/3)))
            cv2.imshow('waste', im0)

while True:

    key = cv2.waitKey(100)   
    
    if key == 27:
        break    
    
cv2.destroyAllWindows()