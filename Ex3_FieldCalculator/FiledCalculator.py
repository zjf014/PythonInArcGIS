# -*- coding: cp936 -*-

#1����ĳ���ֵ����˳�� ID �����֡�

#Code Block:
rec=0
def autoIncrement():
    global rec
    pStart = 1 #adjust start value, if req'd 
    pInterval = 1 #adjust interval value, if req'd
    if (rec == 0): 
        rec = pStart 
    else: 
        rec = rec + pInterval 
    return rec

#Expression:
autoIncrement()


#2������ֵ���ֶε��ۼ�ֵ��

#Code Block:
total = 0
def accumulate(increment):
    global total
    if total:
        total += increment
    else:
        total = increment
    return total

#Expression:
accumulate(!FieldA!)


#3������ֵ���ֶεİٷֱ�������

#Code Block:
lastValue = 0
def percentIncrease(newValue):
    global lastValue
    if lastValue:
        percentage = ((newValue - lastValue) / lastValue)  * 100
    else: 
        percentage = 0
    lastValue = newValue
    return percentage

#Expression:
percentIncrease(float(!FieldA!))


#4��������

#Code Block:
import arcpy 
rows = arcpy.UpdateCursor("Demo","","","","ORDER_ID")
i=2102130001
for row in rows:
     row.ORDER_ID=i
     i=i+1
     rows.updateRow(row)

del rows
del row

#Expression:
!FieldA!



#5����ĳҪ���е��۵�����

#Code Block:
def MySub(feat):    
    partnum = 0

    # Count the number of points in the current multipart feature
    partcount = feat.partCount
    pntcount = 0

    while partnum < partcount:
        part = feat.getPart(partnum)
        pnt = part.next()

        # Enter while loop for each vertex
        #
        while pnt:
            pntcount += 1   
            pnt = part.next()
   
            # If pnt is null, either the part is finished or there 
            # is an interior ring
            #
            if not pnt: 
                pnt = part.next()
        partnum += 1
    return pntcount


#Expression:
MySub(!shape!)



#6����Ҫ������ÿ����� x ����ƽ�� 100��

#Code Block:
def shiftXCoordinate(shape):
    shiftValue = 100
    point = shape.getPart(0)
    point.X += shiftValue
    return point

#Expression:
shiftXCoordinate(!SHAPE!)



