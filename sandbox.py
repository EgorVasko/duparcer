parsed = [{"href":'href1',"price": "10000"},{"href":'href2',"price": "10000"},{"href":'href3',"price": "15000"},{"href":'href4',"price": "20000"},{"href":'href5',"price": "15000"}]
dictred = [{"href":'href2',"price": "15000"},{"href":'href5',"price": "15000"}]
dictold = [{"href":'href3',"price": "20000"},{"href":'href4',"price": "20000"}]



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
                continue
            if i['price'] >= x['price']:
                dict_red_nochanges.append(i)
                continue

parsed1 = []
for i in dict_disc_again:
    for x in parsed:
        if i != x:
            parsed1.append(x)
parsed = []
for i in dict_red_nochanges:
    for x in parsed1:
        if i != x:
            parsed.append(x)

for i in parsed:
    for z in dictold:
        if i['href'] == z['href']:
            if i['price'] < z['price']:
                dict_disc.append(i)
                continue
            if i['price'] >= z['price']:
                dict_nochanges.append(i)
                continue

parsed1 = []
for i in dict_disc:
    for x in parsed:
        if i != x:
            parsed1.append(x)
parsed = []
for i in dict_nochanges:
    for x in parsed1:
        if i != x:
            dict_new.append(x)

out_new = dict_nochanges + dict_new
out_disc = dict_disc+dict_disc_again + dict_red_nochanges


def load_to_html():
    with open('output.html', 'w+') as out_file:
        if not dict_new:
            line = "<center><h2> No new cars " + "</center></h2>"
            out_file.write(line)
        if dict_new:
            line = "<center><h2> New cars " + "</center></h2>"
            out_file.write(line)
            for i in dict_new:
                line = 'Link is : <a href="' + i['href'] + '">' + i['href'] + '</a>' + "&nbsp;&nbsp;&nbsp;&nbsp;Price is: " + i['price'] + "<br />"
                out_file.write(line)

        if not dict_disc_again:
            line = ""
        else:
            line = "<center><h2>  Price reduced AGAIN! </center></h2>"
            out_file.write(line)
            for i in dict_disc_again:
                for x in dictred:
                    if i['href'] == x['href']:
                        oldprice = x['price']
                line = 'Link is : <a href="' + i['href'] + '">' + i['href'] + '</a>' + "&nbsp;&nbsp;&nbsp;&nbsp;Price is: " + i['price'] + "&nbsp;&nbsp;&nbsp;&nbsp;Old price is: " + oldprice + "<br />"
                out_file.write(line)

        if not dict_disc:
            line = ""
        else:
            line = "<center><h2>  Price reduced </center></h2> "
            out_file.write(line)
            for i in dict_disc:
                line = 'Link is : <a href="' + i['href'] + '">' + i['href'] + '</a>' + "&nbsp;&nbsp;&nbsp;&nbsp;Price is: " + i['price'] + "<br />"
                out_file.write(line)

        if not dict_nochanges:
            line = ""
        else:
            line = "<center><h2>  Old Cars </center></h2>"
            out_file.write(line)
            for i in dict_nochanges:
                line = 'Link is : <a href="' + i['href'] + '">' + i['href'] + '</a>' + "&nbsp;&nbsp;&nbsp;&nbsp;Price is: " + i['price'] + "<br />"
                out_file.write(line)

        if not dict_red_nochanges:
            line = ""
        else:
            for i in dict_red_nochanges:
                line = 'Link is : <a href="' + i['href'] + '">' + i['href'] + '</a>' + "&nbsp;&nbsp;&nbsp;&nbsp;Price is: " + i['price'] + "<br />"
                out_file.write(line)


load_to_html()

def cli_output():
    for i in dict_new:
        print("NEW                  Key = " + i['href'] + "    Price =     " + i['price'])

    for i in dict_disc_again:
        print("PRICE REDUCED AGAIN! Key = " + i['href'] + "    New price = " + i['price'] + "    Old price is = " + i['price'])

    for i in dict_disc:
        print("PRICE REDUCED!       Key = " + i['href'] + "    New price = " + i['price'] + "    Old price is = " + i['price'])

    for i in dict_nochanges:
        print("OLD                  Key = " + i['href'] + "    Value =     " + i['price'])

    for i in dict_red_nochanges:
        print("OLD                  Key = " + i['href'] + "    Value =     " + i['price'])

print(dict_new)
print(dict_red_nochanges)
print(dict_disc_again)
print(dict_disc)
print(dict_nochanges)
