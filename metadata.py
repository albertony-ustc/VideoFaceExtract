## 照片元数据处理程序

PicName = ''  #照片-视频文件名称

def TimeToUTC(Time):
    # 日期UTC化
    date_string = Time
    # 分割字符串，获取时区和日期
    timezone_str, date_str = date_string.split(' ', 1)
    # 创建时区对象
    timezone = pytz.timezone(timezone_str)
    # 解析日期字符串
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    # 将日期转换为UTC时区
    dt = timezone.localize(dt)
    dt = str(dt.astimezone(pytz.UTC)).split('+')[0]

    return datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")

# 视频元数据提取
from pymediainfo import MediaInfo

media_info = MediaInfo.parse(f'{PicName}.mp4')
data = eval(media_info.to_json())

GPS = data['tracks'][0]['xyz'][1:-1].split('+') ; GPS = [float(GPS[0]),float(GPS[1])]
Time = data['tracks'][0]['tagged_date']
TimeLastMod = data['tracks'][0]['file_last_modification_date']
TimeLastModLocal = datetime.strptime(data['tracks'][0]['file_last_modification_date__local'],"%Y-%m-%d %H:%M:%S")

# ========================
# 照片GPS信息写入
from GPSPhoto import gpsphoto
# 创建一个GPSPhoto对象
photo = gpsphoto.GPSPhoto(f"{PicName}.jpg")
# 创建GPSInfo数据对象
info = gpsphoto.GPSInfo(GPS)
# 修改GPS数据
photo.modGPSData(info, f'{PicName}.jpg')

#时间处理
from datetime import datetime
import pytz

#计算时区
# 解析日期字符串
Time = TimeToUTC(Time)
TimeLastMod = TimeToUTC(TimeLastMod)

# =================
# 照片时间信息写入

## 时区提取
from datetime import datetime
import pytz
# 定义两个时间
#time1 = datetime.strptime(TimeLastModLocal, '%Y-%m-%d %H:%M:%S')
#time2 = datetime.strptime(TimeLastMod, '%Y:%m:%d %H:%M:%S')
# 计算时间差
time_diff = TimeLastModLocal - TimeLastMod
# 将时间差转换成小时
hours_diff = time_diff.total_seconds() / 3600
# 将小时差转换成时区格式
if hours_diff >= 0:
    timezone_format = f"+{int(hours_diff):02d}:00"
else:
    timezone_format = f"{int(hours_diff):03d}:00"

Time += time_diff  #UTC时间转为时区时间

## 写入拍摄时间
from pyexiv2 import Image  # 只支持64位的python环境

# 元信息
i = Image(f"{PicName}.jpg")
_dict = {"Exif.Photo.DateTimeOriginal": Time.strftime('%Y:%m:%d %H:%M:%S'),
         "Exif.Photo.OffsetTime": timezone_format}

i.modify_exif(_dict)  # 执行修改
