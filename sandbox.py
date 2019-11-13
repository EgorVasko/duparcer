parsed = [{"href":'href1',"price": "20000"},{"href":'href2',"price": "20000"},{"href":'href3',"price": "20000"},{"href":'href4',"price": "20000"}]
dictred = [{"href":'href1',"price": "20000"},{"href":'href2',"price": "20000"},{"href":'href3',"price": "20000"},{"href":'href4',"price": "20000"}]
dictold = [{"href":'href2',"price": "20000"},{"href":'href3',"price": "20000"},{"href":'href4',"price": "20000"}]



dict_disc_again = []
dict_red_nochanges = []
dict_disc = []
dict_nochanges = []
dict_new = []

for i in parsed:
    for x in dictred:
        if i['href'] == x['href']:
            if i['price'] < x['price']:
                dict_disc_again.append(i)        # add to again discounted
                print(i)
                continue
            if i['price'] >= x['price']:
                dict_red_nochanges.append(i)
                print(i)
                continue
        for z in dictold:
            if i['price'] < z['price']:
                dict_disc.append(i)
                continue
            if i['price'] >= z['price']:
                dict_nochanges.append(i)
                continue
            else:
                dict_new.append(i)
