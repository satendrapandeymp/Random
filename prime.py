input = 10

check = []

def ways(num, arr2):
    
    temp = 0
    
    if num in [2,3]:
        return 0

    for pr in arr:

        temp1 = prime(num-pr)
        
        if num-pr in arr2:
            temp += 1         
        
        temp += ways(temp1 , num-pr, arr2)
        
    return temp

def prime(input):
    if input<2:
        return []
    arr = []    
    for i in range(2,input):
        flag = 0
        for j in range(2,int(i ** .5)):
            if i%j == 0:
                flag = 1
                break
        if flag != 1:
            arr.append(i)
    return arr


arr = prime(input)
arr2 = prime(input)

#num = ways(arr,input,arr2)
 
print arr
        