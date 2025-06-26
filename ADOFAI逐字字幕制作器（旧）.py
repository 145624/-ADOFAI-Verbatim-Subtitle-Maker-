print("请先调试好文字装饰及其标签！")
print("请全屏使用，建议备份后多次尝试")
b=0 #循环次数
c=0 #字符
#基本信息
floor=int(input("请输入目标轨道："))
d=int(input("请输入初始轨道偏移："))
angleOffset=int(input("请输入轨道偏移（每个字符）："))

a=d-angleOffset 
tag=input("请输入目标装饰物标签:")
text=input("请输入一句话：")
#循环
while 1:
    print("""		                { "floor": """+str(floor)+""", "eventType": "SetText", "decText": " """+text[0:c]+""" ", "tag": " """+tag+""" ", "angleOffset": """+str(a)+""", "eventTag": ""},""") #事件
    a=a+angleOffset #轨道偏移增加
    b=b+1 #循环次数增加
    c=c+1 #字符数增加
    if b == len(text)+1:
        break
print("使用时删去第一行")
input("删去第一行并复制后输入2继续")
print("使用方法:复制进.adofai文件")
print("""例如：
                { "floor": 目标格数的上一格, "eventType": "Hold", "duration": 8, "distanceMultiplier": 100, "landingAnimation": true},
                { "floor": 目标格数, "eventType": "SetText", "decText": " m ", "tag": " p1_title ", "angleOffset": 0, "eventTag": ""},
                { "floor": 目标格数, "eventType": "SetText", "decText": " ma ", "tag": " p1_title ", "angleOffset": 5, "eventTag": ""},
                { "floor": 目标格数, "eventType": "SetText", "decText": " man ", "tag": " p1_title ", "angleOffset": 10, "eventTag": ""},
                { "floor": 目标格数, "eventType": "SetText", "decText": " man! ", "tag": " p1_title ", "angleOffset": 15, "eventTag": ""},
                { "floor": 目标格数, "eventType": "SetText", "decText": " man!  ", "tag": " p1_title ", "angleOffset": 20, "eventTag": ""},
                { "floor": 目标格数, "eventType": "SetText", "decText": " man! w ", "tag": " p1_title ", "angleOffset": 25, "eventTag": ""},
                { "floor": 目标格数, "eventType": "SetText", "decText": " man! wh ", "tag": " p1_title ", "angleOffset": 30, "eventTag": ""},        
                { "floor": 目标格数, "eventType": "SetText", "decText": " man! wha ", "tag": " p1_title ", "angleOffset": 35, "eventTag": ""},       
                { "floor": 目标格数, "eventType": "SetText", "decText": " man! what ", "tag": " p1_title ", "angleOffset": 40, "eventTag": ""},      
                { "floor": 目标格数, "eventType": "SetText", "decText": " man! what  ", "tag": " p1_title ", "angleOffset": 45, "eventTag": ""},     
                { "floor": 目标格数, "eventType": "SetText", "decText": " man! what c ", "tag": " p1_title ", "angleOffset": 50, "eventTag": ""},    
                { "floor": 目标格数, "eventType": "SetText", "decText": " man! what ca ", "tag": " p1_title ", "angleOffset": 55, "eventTag": ""},   
                { "floor": 目标格数, "eventType": "SetText", "decText": " man! what can ", "tag": " p1_title ", "angleOffset": 60, "eventTag": ""},  
                { "floor": 目标格数, "eventType": "SetText", "decText": " man! what can  ", "tag": " p1_title ", "angleOffset": 65, "eventTag": ""}, 
                { "floor": 目标格数, "eventType": "SetText", "decText": " man! what can i ", "tag": " p1_title ", "angleOffset": 70, "eventTag": ""},
                { "floor": 目标格数, "eventType": "SetText", "decText": " man! what can i  ", "tag": " p1_title ", "angleOffset": 75, "eventTag": ""},
                { "floor": 目标格数, "eventType": "SetText", "decText": " man! what can i s ", "tag": " p1_title ", "angleOffset": 80, "eventTag": ""},
                { "floor": 目标格数, "eventType": "SetText", "decText": " man! what can i sa ", "tag": " p1_title ", "angleOffset": 85, "eventTag": ""},
                { "floor": 目标格数, "eventType": "SetText", "decText": " man! what can i say ", "tag": " p1_title ", "angleOffset": 90, "eventTag": ""},
                { "floor": 目标格数, "eventType": "SetText", "decText": " man! what can i say! ", "tag": " p1_title ", "angleOffset": 95, "eventTag": ""},
                { "floor": 目标格数下一格, "eventType": "AnimateTrack", "trackAnimation": "Fade", "beatsAhead": 1, "beatsBehind": 2},""")
print("一定不要覆盖其他事件！！！")
exib=input("输入1退出程序")
if exit==1:
    exit()