def ShiftHorizontal(List, ShiftAmount):
    temp=List.copy()

    lenX=len(List)
    for x in range(5):
        if ShiftAmount<0:
            if x- ShiftAmount < len(temp):
                temp[x]=List[x-ShiftAmount]
            else:
                temp[x]=['z','z','z','z','z']
        else:
            if lenX-1-x-ShiftAmount >=0:
                temp[lenX-1-x]=List[lenX-1-x-ShiftAmount]
            else:
                temp[lenX-1-x]=['z','z','z','z','z']
    return temp

def shiftVertical(List, ShiftAmount):
    lenX=len(List)
    lenY=len(List[0])
    lastIndex=lenY-1
    temp=List.copy()
    for i in range(lenY):
        column=temp[i]
        for j in range(lenX):
            if ShiftAmount < 0:
                if j - ShiftAmount < lenY:
                    column[j] = List[i][j - ShiftAmount]
                else:
                    column[j] = 'z'
            else:
                if lenY - 1 - j - ShiftAmount >= 0:
                    column[lenY - 1 - j] = List[i][lenY - 1 - j - ShiftAmount]
                else:
                    column[lenX - 1 - j] = 'z'
    return temp
