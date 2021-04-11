def getAverageValue(size,data,actualIndex):
    elementsSum = 0    
    if size+actualIndex < len(data):
        for k in range(1, size+1):
            elementsSum += data[actualIndex+k]
            elementsSum += data[actualIndex-k]
    else:
        overflow = size+actualIndex - len(data)
        for j in range(1, size-overflow):
            elementsSum += data[actualIndex+j]
            elementsSum += data[actualIndex-j]

    return elementsSum/(size*2)


def filterByConfidence(x,y,conf,threshold):
    ran = range(len(conf))
    filteredX= []
    filteredY= []
    for i in ran:
        if conf[i] > threshold:
            filteredX.append(x[i])
            filteredY.append(y[i])
        else:
            newValueX = getAverageValue(size=5,data=x,actualIndex=i)
            newValueY = getAverageValue(size=5,data=y,actualIndex=i)
            filteredX.append(newValueX)
            filteredY.append(newValueY)
    return filteredX,filteredY

def average(x,f):
    avg = 0
    suma = 0
    for element in x[f:f+60]:
        suma += element
    avg = suma/60
    return avg    

def averagePerSecond(list):
    avgX= []
    iter = 0
    for f in range(len(list)):
        if iter==60:
            avg = average(list,f)
            avgX.append(avg)
            iter=0
        iter+=1
    return avgX

def differentiation(list):
    diff = []
    for i in range(len(list)-1):
        diff.append(list[i+1]-list[i])

    return diff