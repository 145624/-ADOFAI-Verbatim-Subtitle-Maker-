#选择并读取文件

from importlib import import_module
import operator
from re import L
from tkinter import *
from tkinter import filedialog
from adobase import *
root=Tk()
root.withdraw()
filepath=filedialog.askopenfilename(title="选择.adofai文件",filetypes=[("ADOFAI关卡文件", "*.adofai")])
if filepath:
    with open(filepath,"r",encoding="utf-8") as file:
        level=ADOFAILevel.load(filepath)

#基本参数&装饰物创建
#轨道数
floor=int(input("请输入轨道数:"))
#装饰物标签
tag=input("请输入装饰物标签:")
accept=input("装饰物标签将设为："+tag+"_1,"+tag+"_2 ......可以吗？[y/n]")
if accept=="y":
    pass
else:
    print("已取消")
    exit()
#字体
font=input("""请输入字体:
           1.默认
           2.Arial
           3.Comic Sans MS
           4.Courier New
           5.Georgia
           6.Helvetica
           7.Times New Roman
           """)
if font=="1":
    font="Default"
elif font=="2":
    font="Arial"
elif font=="3":
    font="ComicSansMS"  
elif font=="4":
    font="CourierNew"
elif font=="5":
    font="Georgia"
elif font=="6":
    font="Helvetica"
elif font=="7":
    font="TimesNewRoman"
else:
    print("已取消")
    exit()
#坐标
x=float(str(input("请输入x位置偏移:")))
y=float(str(input("请输入y位置偏移:")))

#旋转角度
rotation=float(str(input("请输入旋转角度:")))
#大小
scale1=float(str(input("请输入x大小:")))
scale2=float(str(input("请输入y大小:")))

#锁定
lockRotation=input("锁定旋转吗？[y/n]")
if lockRotation=="y":
    lockRotation=True
else:
    lockRotation=False
lockScale=input("锁定大小吗？[y/n]")
if lockScale=="y":
    lockScale=True
else:
    lockScale=False
#颜色
color=input("请输入颜色代码（六位，默认ffffff）:")
if color=="":
    color="ffffff"
#深度
depth=input("请输入深度:")
#平行
parallax1=float(str(input("请输入x平行:")))
parallax2=float(str(input("请输入y平行:")))

#视差偏移
if parallax1 !=0 and parallax2 !=0:
    parallaxOffset1=float(str(input("请输入x视差偏移:")))
    parallaxOffset2=float(str(input("请输入y视差偏移:")))
else:
    parallaxOffset1=0
    parallaxOffset2=0
#文字
text=input("请输入文字:")
animathion=input("是否需要制作动画？[y/n]")

#动画
if animathion=="y":

    random=input("是否需要随机字符位置？[y/n]")
    #随机字符
    if random=="y":
        import random
        random1=int(str(input("请输入随机范围1(整数)：")))
        random2=int(str(input("请输入随机范围2(整数)：")))
        x2=float(str(input("请输入文字间隔：")))
        rotationOffset_input = input("请输入旋转偏移(不填默认回正)：")
        rotationOffset = -rotation if rotationOffset_input == '' else float(str(rotationOffset_input))
        duration=float(str(input("请输入每个字符出现时间（拍子）：")))
        a=float(str(input("请输入初始角度偏移：")))
        angleOffset=float(str(input("请输入每个字符角度偏移：")))
        randomease=input("是否需要随机缓动函数(不含linear，flash，Bounce等)？[y/n]")
        d=1#标签数
        c1=0
        c=1#字符数
        b=0#循环次数
        #随机字符并随机缓速
        if randomease=="y":
            randomrange = input("在哪些函数中随机？：\n1.in函数\n2.out函数\n3.inout函数")
            while True:
                if randomrange == "1":
                    ease_num = random.randint(1, 8)
                    if ease_num == 1:
                        ease = "InSine"
                    elif ease_num == 2:
                        ease = "InCubic"
                    elif ease_num == 3:
                        ease = "InQuart"
                    elif ease_num == 4:
                        ease = "InQuint"
                    elif ease_num == 5:
                        ease = "InExpo"
                    elif ease_num == 6:
                        ease = "InCirc"
                    elif ease_num == 7:
                        ease = "InBack"
                    elif ease_num == 8:
                        ease = "InQuad"
                elif randomrange == "2":
                    ease_num = random.randint(1, 8)
                    if ease_num == 1:
                        ease = "OutSine"
                    elif ease_num == 2:
                        ease = "OutCubic"
                    elif ease_num == 3:
                        ease = "OutQuart"
                    elif ease_num == 4:
                        ease = "OutQuint"
                    elif ease_num == 5:
                        ease = "OutExpo"
                    elif ease_num == 6:
                        ease = "OutCirc"
                    elif ease_num == 7:
                        ease = "OutBack"
                    elif ease_num == 8:
                        ease = "OutQuad"
                elif randomrange == "3":
                    ease_num = random.randint(1, 8)
                    if ease_num == 1:
                        ease = "InOutSine"
                    elif ease_num == 2:
                        ease = "InOutCubic"
                    elif ease_num == 3:
                        ease = "InOutQuart"
                    elif ease_num == 4:
                        ease = "InOutQuint"
                    elif ease_num == 5:
                        ease = "InOutExpo"
                    elif ease_num == 6:
                        ease = "InOutCirc"
                    elif ease_num == 7:
                        ease = "InOutBack"
                    elif ease_num == 8:
                        ease = "InOutQuad"
                x1=random.randint(random1, random2)
                y1=random.randint(random1, random2)
                tag1=tag+"_"+str(d)
                if parallax1!=0 or parallax2!=0:
                    parallaxOffset1=parallaxOffset1+x2
                    level.add_decoration(floor, "AddText", decText=text[c1:c], tag=tag1,font=font,position=[x+x1,y+y1],relativeTo="Tile",pivotOffset=[0,0],    rotation=rotation,  lockRotation=lockRotation, scale=[scale1,scale2], lockScale=lockScale, color=color, opacity=0, depth=depth, parallax=[parallax1,parallax2], parallaxOffset=[parallaxOffset1+x1,parallaxOffset2+y1])
                else:
                    x=x+x2
                    level.add_decoration(floor, "AddText", decText=text[c1:c], tag=tag1,font=font,position=[x+x1,y+y1],relativeTo="Tile",pivotOffset=[0,0],    rotation=rotation,  lockRotation=lockRotation, scale=[scale1,scale2], lockScale=lockScale, color=color, opacity=0, depth=depth, parallax=[parallax1,parallax2], parallaxOffset=[parallaxOffset1,parallaxOffset2])
                level.add_event(floor, "MoveDecorations", duration=duration,positionOffset=[-x1,-y1],tag=tag1, rotationOffset=rotationOffset,opacity=100,angleOffset=a,ease=ease,parallaxOffset=[parallaxOffset1,parallaxOffset2])
                d=d+1
                c1=c1+1#字符数增加
                a=a+angleOffset
                c=c+1#字符数增加
                b=b+1#循环次数增加
                if b == len(text)+1:
                    break
        #随机字符但不随机缓速
        else:
            import random
            ease=input("""请输入缓动函数：
                1.Linear
                2.InSine
                3.OutSine
                4.InOutSine
                5.InQuad
                6.InCubic
                7.InQuart
                8.InQuint
                9.InExpo
                10.InCirc
                11.InBack
                12.OutQuad
                13.OutCubic
                14.OutQuart
                15.OutQuint
                16.OutExpo
                17.OutCirc
                18.OutBack
                19.InBounce
                20.InElastic
                21.Flash
                22.InFlash
                23.OutBounce
                24.OutElastic
                25.OutFlash
                26.InOutQuad
                27.InOutCubic
                28.InOutQuart
                29.InOutQuint
                30.InOutExpo
                31.InOutCirc
                32.InOutBack
                33.InOutElastic
                34.InOutFlash


                """)
            if ease=="1":
                ease="Linear"
            elif ease=="2":
                ease="InSine"
            elif ease=="3":
                ease="OutSine"
            elif ease=="4":
                ease="InOutSine"
            elif ease=="5":
                ease="InQuad"
            elif ease=="6":
                ease="InCubic"
            elif ease=="7":
                ease="InQuart"
            elif ease=="8":
                ease="InQuint"
            elif ease=="9":
                ease="InExpo"
            elif ease=="10":
                ease="InCirc"
            elif ease=="11":
                ease="InBack"
            elif ease=="12":
                ease="OutQuad"
            elif ease=="13":
                ease="OutCubic"
            elif ease=="14":
                ease="OutQuart"
            elif ease=="15":
                ease="OutQuint"
            elif ease=="16":
                ease="OutExpo"
            elif ease=="17":
                ease="OutCirc"
            elif ease=="18":
                ease="OutBack"
            elif ease=="19":
                ease="InBounce"
            elif ease=="20":
                ease="InElastic"
            elif ease=="21":
                ease="Flash"
            elif ease=="22":
                ease="InFlash"
            elif ease=="23":
                ease="OutBounce"
            elif ease=="24":
                ease="OutElastic"
            elif ease=="25":
                ease="OutFlash"
            elif ease=="26":
                ease="InOutQuad"
            elif ease=="27":
                ease="InOutCubic"
            elif ease=="28":
                ease="InOutQuart"
            elif ease=="29":
                ease="InOutQuint"
            elif ease=="30":
                ease="InOutExpo"
            elif ease=="31":
                ease="InOutCirc"
            elif ease=="32":
                ease="InOutBack"
            elif ease=="33":
                ease="InOutElastic"
            elif ease=="34":
                ease="InOutFlash"
            while True:
                x1=random.randint(random1, random2)
                y1=random.randint(random1, random2)
                tag1=tag+"_"+str(d)
                if parallax1!=0 or parallax2!=0:
                    parallaxOffset1=parallaxOffset1+x2
                    level.add_decoration(floor, "AddText", decText=text[c1:c], tag=tag1,font=font,position=[x+x1,y+y1],relativeTo="Tile",pivotOffset=[0,0],    rotation=rotation,  lockRotation=lockRotation, scale=[scale1,scale2], lockScale=lockScale, color=color, opacity=0, depth=depth, parallax=[parallax1,parallax2], parallaxOffset=[parallaxOffset1+x1,parallaxOffset2+y1])
                else:
                    x=x+x2
                    level.add_decoration(floor, "AddText", decText=text[c1:c], tag=tag1,font=font,position=[x+x1,y+y1],relativeTo="Tile",pivotOffset=[0,0],    rotation=rotation,  lockRotation=lockRotation, scale=[scale1,scale2], lockScale=lockScale, color=color, opacity=0, depth=depth, parallax=[parallax1,parallax2], parallaxOffset=[parallaxOffset1,parallaxOffset2])
                level.add_event(floor, "MoveDecorations", duration=duration,positionOffset=[-x1,-y1],tag=tag1, rotationOffset=rotationOffset,opacity=100,angleOffset=a,ease=ease,parallaxOffset=[parallaxOffset1,parallaxOffset2])
                d=d+1
                c1=c1+1#字符数增加
                a=a+angleOffset
                c=c+1#字符数增加
                b=b+1#循环次数增加
                if b == len(text)+1:
                    break
    #不随机字符
    else:
        import random
        y1=float(str(input("请输入文字起始向上+/下-偏移量：")))
        x1=float(str(input("请输入文字起始向左-/右+偏移量：")))
        x2=float(str(input("请输入文字间隔：")))
        rotationOffset = input("请输入旋转偏移(不填默认回正)：")
        if rotationOffset == '':
            rotationOffset = -rotation
        else:
            rotationOffset = float(str(rotationOffset))
        duration=float(str(input("请输入每个字符出现时间（拍子）：")))
        a=float(str(input("请输入初始角度偏移：")))
        angleOffset=float(str(input("请输入每个字符角度偏移：")))
        randomease=input("是否需要随机缓动函数？[y/n]")
        d=1#标签数
        c1=0
        c=1#字符数
        b=0#循环次数
        #不随机字符但随机缓速
        if randomease=="y":
            randomrange=input("""在哪些函数中随机？：
            1.in函数
            2.out函数
            3.inout函数""")
            while True:
                if randomrange == "1":
                    ease_num = random.randint(1, 8)
                    if ease_num == 1:
                        ease = "InSine"
                    elif ease_num == 2:
                        ease = "InCubic"
                    elif ease_num == 3:
                        ease = "InQuart"
                    elif ease_num == 4:
                        ease = "InQuint"
                    elif ease_num == 5:
                        ease = "InExpo"
                    elif ease_num == 6:
                        ease = "InCirc"
                    elif ease_num == 7:
                        ease = "InBack"
                    elif ease_num == 8:
                        ease = "InQuad"
                elif randomrange == "2":
                    ease_num = random.randint(1, 8)
                    if ease_num == 1:
                        ease = "OutSine"
                    elif ease_num == 2:
                        ease = "OutCubic"
                    elif ease_num == 3:
                        ease = "OutQuart"
                    elif ease_num == 4:
                        ease = "OutQuint"
                    elif ease_num == 5:
                        ease = "OutExpo"
                    elif ease_num == 6:
                        ease = "OutCirc"
                    elif ease_num == 7:
                        ease = "OutBack"
                    elif ease_num == 8:
                        ease = "OutQuad"
                elif randomrange == "3":
                    ease_num = random.randint(1, 8)
                    if ease_num == 1:
                        ease = "InOutSine"
                    elif ease_num == 2:
                        ease = "InOutCubic"
                    elif ease_num == 3:
                        ease = "InOutQuart"
                    elif ease_num == 4:
                        ease = "InOutQuint"
                    elif ease_num == 5:
                        ease = "InOutExpo"
                    elif ease_num == 6:
                        ease = "InOutCirc"
                    elif ease_num == 7:
                        ease = "InOutBack"
                    elif ease_num == 8:
                        ease = "InOutQuad"

                tag1=tag+"_"+str(d)
                if parallax1!=0 or parallax2!=0:
                    parallaxOffset1=parallaxOffset1+x2
                    level.add_decoration(floor, "AddText", decText=text[c1:c], tag=tag1,font=font,position=[x+x1,y+y1],relativeTo="Tile",pivotOffset=[0,0],    rotation=rotation,  lockRotation=lockRotation, scale=[scale1,scale2], lockScale=lockScale, color=color, opacity=0, depth=depth, parallax=[parallax1,parallax2], parallaxOffset=[parallaxOffset1+x1,parallaxOffset2+y1])
                else:
                    x=x+x2
                    level.add_decoration(floor, "AddText", decText=text[c1:c], tag=tag1,font=font,position=[x+x1,y+y1],relativeTo="Tile",pivotOffset=[0,0],    rotation=rotation,  lockRotation=lockRotation, scale=[scale1,scale2], lockScale=lockScale, color=color, opacity=0, depth=depth, parallax=[parallax1,parallax2], parallaxOffset=[parallaxOffset1,parallaxOffset2])
                level.add_event(floor, "MoveDecorations", duration=duration,positionOffset=[-x1,-y1],tag=tag1, rotationOffset=rotationOffset,opacity=100,angleOffset=a,ease=ease,parallaxOffset=[parallaxOffset1,parallaxOffset2])
                d=d+1
                c1=c1+1#字符数增加
                a=a+angleOffset
                c=c+1#字符数增加
                b=b+1#循环次数增加
                if b == len(text)+1:
                    break
                
        #不随机字符也不随机缓速
        else:
            ease=input("""请输入缓动函数：
                1.Linear
                2.InSine
                3.OutSine
                4.InOutSine
                5.InQuad
                6.InCubic
                7.InQuart
                8.InQuint
                9.InExpo
                10.InCirc
                11.InBack
                12.OutQuad
                13.OutCubic
                14.OutQuart
                15.OutQuint
                16.OutExpo
                17.OutCirc
                18.OutBack
                19.InBounce
                20.InElastic
                21.Flash
                22.InFlash
                23.OutBounce
                24.OutElastic
                25.OutFlash
                26.InOutQuad
                27.InOutCubic
                28.InOutQuart
                29.InOutQuint
                30.InOutExpo
                31.InOutCirc
                32.InOutBack
                33.InOutElastic
                34.InOutFlash


                """)
            if ease=="1":
                ease="Linear"
            elif ease=="2":
                ease="InSine"
            elif ease=="3":
                ease="OutSine"
            elif ease=="4":
                ease="InOutSine"
            elif ease=="5":
                ease="InQuad"
            elif ease=="6":
                ease="InCubic"
            elif ease=="7":
                ease="InQuart"
            elif ease=="8":
                ease="InQuint"
            elif ease=="9":
                ease="InExpo"
            elif ease=="10":
                ease="InCirc"
            elif ease=="11":
                ease="InBack"
            elif ease=="12":
                ease="OutQuad"
            elif ease=="13":
                ease="OutCubic"
            elif ease=="14":
                ease="OutQuart"
            elif ease=="15":
                ease="OutQuint"
            elif ease=="16":
                ease="OutExpo"
            elif ease=="17":
                ease="OutCirc"
            elif ease=="18":
                ease="OutBack"
            elif ease=="19":
                ease="InBounce"
            elif ease=="20":
                ease="InElastic"
            elif ease=="21":
                ease="Flash"
            elif ease=="22":
                ease="InFlash"
            elif ease=="23":
                ease="OutBounce"
            elif ease=="24":
                ease="OutElastic"
            elif ease=="25":
                ease="OutFlash"
            elif ease=="26":
                ease="InOutQuad"
            elif ease=="27":
                ease="InOutCubic"
            elif ease=="28":
                ease="InOutQuart"
            elif ease=="29":
                ease="InOutQuint"
            elif ease=="30":
                ease="InOutExpo"
            elif ease=="31":
                ease="InOutCirc"
            elif ease=="32":
                ease="InOutBack"
            elif ease=="33":
                ease="InOutElastic"
            elif ease=="34":
                ease="InOutFlash"
            while True:

                tag1=tag+"_"+str(d)
                if parallax1!=0 or parallax2!=0:
                    parallaxOffset1=parallaxOffset1+x2
                    level.add_decoration(floor, "AddText", decText=text[c1:c], tag=tag1,font=font,position=[x+x1,y+y1],relativeTo="Tile",pivotOffset=[0,0],    rotation=rotation,  lockRotation=lockRotation, scale=[scale1,scale2], lockScale=lockScale, color=color, opacity=0, depth=depth, parallax=[parallax1,parallax2], parallaxOffset=[parallaxOffset1+x1,parallaxOffset2+y1])
                else:
                    x=x+x2
                    level.add_decoration(floor, "AddText", decText=text[c1:c], tag=tag1,font=font,position=[x+x1,y+y1],relativeTo="Tile",pivotOffset=[0,0],    rotation=rotation,  lockRotation=lockRotation, scale=[scale1,scale2], lockScale=lockScale, color=color, opacity=0, depth=depth, parallax=[parallax1,parallax2], parallaxOffset=[parallaxOffset1,parallaxOffset2])
                level.add_event(floor, "MoveDecorations", duration=duration,positionOffset=[-x1,-y1],tag=tag1, rotationOffset=rotationOffset,opacity=100,angleOffset=a,ease=ease,parallaxOffset=[parallaxOffset1,parallaxOffset2])
                d=d+1
                c1=c1+1#字符数增加
                a=a+angleOffset
                c=c+1#字符数增加
                b=b+1#循环次数增加
                if b == len(text)+1:
                    break

#仅逐字
else:

    level.add_decoration(floor, "AddText", dectext="",tag=tag,font=font,position=[x,y],relativeTo="Tile",pivotOffset=[0,0],    rotation=rotation,  lockRotation=lockRotation, scale=[scale1,scale2], lockScale=lockScale, color=color, opacity=0, depth=depth, parallax=[parallax1,parallax2], parallaxOffset=[parallaxOffset1,parallaxOffset2])
    b=0 #循环次数
    c=1 #字符
    #基本信息
    d=float(input("请输入初始角度偏移："))
    angleOffset=float(input("请输入角度偏移（每个字符）："))
    level.add_event(floor, "MoveDecorations", tag=tag,duration=0,opacity=100 ,angleOffset=0)

    #循环
    while 1:

        level.add_event(floor,"SetText",decText=text[0:c],tag=tag,angleOffset=d)
        d=d+angleOffset #角度偏移增加
        b=b+1 #循环次数增加
        c=c+1 #字符数增加
        if b == len(text)+1:
            break
level.export(filepath, as_original=True)
        



















