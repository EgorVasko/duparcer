array = [1,2,3,4,5,6,7,1,2]

array1 = []

array2 = [1,2,3]

array3 = 5

array4 = [6]


def arr_copy(x):
    if not x or not isinstance(x, list):
        print(str(x) + " - is empty / not a list / less than 1 item in list")
    else:
        testlist = []
        for i in x:
            if i not in testlist:
                testlist.append(i)
        if len(testlist) < len(x):
            print(str(x) + " have copy")
        else:
            print(str(x) + " have no copy")

arr_copy(array)
arr_copy(array1)
arr_copy(array2)
arr_copy(array3)
arr_copy(array4)
