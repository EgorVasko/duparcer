from urllib.parse import urlsplit

parse_result = urlsplit("https://dubai.dubizzle.com/motors/used-cars/infiniti/gseries/2019/10/28/%D9%88%D8%B1%D8%B3%D8%A7%D9%86-2/")
query_s = parse_result.path
car_data = query_s.split("/")
car_data = car_data[3:8]

for i in car_data:
    print(i)

DICT = []
DICT.append({
    'brand' : car_data[0],
    'model' : car_data[1],
    'ad_posted' : str(car_data[2]) + "-" + str(car_data[3]) + "-" + str(car_data[4])
#    'title': title,
#    'href': href,
#    'price': price,
#    'year': year,
#    'mileage': mileage
    
})

print(DICT)
