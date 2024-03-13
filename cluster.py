# coding: utf-8
"""
@author: xhb
"""

import sys
import os
import dlib
import glob
import cv2
import shutil 

# 指定路径
current_path = os.getcwd()
model_path = current_path + '/model/'
shape_predictor_model = model_path + '/shape_predictor_5_face_landmarks.dat'
face_rec_model = model_path + '/dlib_face_recognition_resnet_model_v1.dat'
face_folder = current_path + '/facetemp/'
output_folder = current_path + '/output/'

# 导入模型
detector = dlib.get_frontal_face_detector()
shape_detector = dlib.shape_predictor(shape_predictor_model)
face_recognizer = dlib.face_recognition_model_v1(face_rec_model)

# 为后面操作方便，建了几个列表
descriptors = []
images = []
#raw_pic = []
Max_Face_Image = ('',0)

# 遍历faces文件夹中所有的图片
for f in glob.glob(os.path.join(face_folder, "*.jpg")):
    print('Processing file：{}'.format(f))
    # 读取图片
    img = cv2.imread(f)
    # 转换到rgb颜色空间
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 检测人脸
    dets = detector(img2, 1)
    print("Number of faces detected: {}".format(len(dets)))

    # 寻找人脸数量最多的照片
    if (len(dets) > Max_Face_Image[1]):
        Max_Face_Image = (f,len(dets))

    # 遍历所有的人脸
    for index, face in enumerate(dets):
        # 检测人脸特征点
        shape = shape_detector(img2, face)
        # 投影到128D
        face_descriptor = face_recognizer.compute_face_descriptor(img2, shape)

        # 保存相关信息
        descriptors.append(face_descriptor)
        images.append((img2, shape))
        #raw_pic.append(f)
        

# 聚类
labels = dlib.chinese_whispers_clustering(descriptors, 1)
print("labels: {}".format(labels))
num_classes = len(set(labels))
print("Number of clusters: {}".format(num_classes))

# 为了方便操作，用字典类型保存
face_dict = {}
#raw_dict = {}

for i in range(num_classes):
    face_dict[i] = []
    #raw_dict[i] = []

    
# print face_dict  

for i in range(len(labels)):
    face_dict[labels[i]].append(images[i])
    #raw_dict[labels[i]].append(raw_pic[i])   #保存人脸

#输出单张照片
print(Max_Face_Image)
FinalPhoto = Max_Face_Image[0]

#命名调整
os.rename(FinalPhoto,FinalPhoto.rsplit('_',2)[0]+'.jpg')
shutil.move(FinalPhoto.rsplit('_',2)[0]+'.jpg',current_path)
for root, dirs, files in os.walk('./facetemp', topdown=False):
    for name in files:
        os.remove(os.path.join(root, name))