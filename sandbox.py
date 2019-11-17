from urllib.parse import urlsplit

href = "https://dubai.dubizzle.com/motors/used-cars/audi/a6/2019/9/15/audi-a6-32l-qattro-v-6-sedan--2/"

parse_result = urlsplit(href)
query_s = parse_result.path
car_data = query_s.split("/")
title = car_data[8].replace("-"," ")
print(title)
car_data = car_data[3:8]
brand = str(car_data[0]).capitalize()
model = str(car_data[1])

if len(str(car_data[3])) == 1:
    month = "0" + str(car_data[3])
else:
    month = str(car_data[3])
if len(str(car_data[4])) == 1:
    date = "0" + str(car_data[4])
else:
    date = str(car_data[4])
ad_posted = str(car_data[2]) + "-" + month + "-" + date

parsed = []
parsed.append({

    'brand' : brand,
    'model' : model,
    'ad_posted' : ad_posted
})

print(parsed)
