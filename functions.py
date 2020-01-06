#!/usr/bin/env python3
import json


def dump_data(dict1, dict2, path):
    if dict1 != dict2:
        with open(path, "w+", encoding="utf-8") as write_file:
            json.dump(dict2, write_file)


def sort_by_parametr(list_to_sort, parametr):
    for x in range(len(list_to_sort) - 1, 0, -1):
        for y in range(x):
            if list_to_sort[y].get(parametr) < list_to_sort[y + 1].get(parametr):
                list_to_sort[y], list_to_sort[y + 1] = list_to_sort[y + 1], list_to_sort[y]


def combine(main, dict0, dict1, dict2):
    for i in range(len(main), 0, -1):
        for z in range(len(dict0), 0, -1):
            if main[i - 1].get('href') == dict0[z - 1].get('href'):
                if int(main[i - 1].get('price')) < int(dict0[z - 1].get('price')):
                    main[i - 1]['oldprice'] = dict0[z - 1].get('price')  # adding old price
                    dict1.append(main[i - 1])
                    main.pop(i - 1)
                    dict0.pop(z - 1)
                    break
                if int(main[i - 1].get('price')) >= int(dict0[z - 1].get('price')):
                    main[i - 1]['oldprice'] = dict0[z - 1].get('oldprice')
                    dict2.append(main[i - 1])
                    main.pop(i - 1)
                    dict0.pop(z - 1)
                    break


def openbase(file, text):
    dict_var = []
    try:
        with open(file, "r", encoding="utf-8") as old_file:
            dict_var = json.load(old_file)
        print("{} results are available: {} cars".format(text, len(dict_var)))
        return dict_var
    except FileNotFoundError:
        print("No " + text + " results")
        return dict_var


def osis():  # define path to Desktop folder
    if platform.system() == "Windows":
        return "C:\\Users\\" + getpass.getuser() + '\Desktop\\'  # try os.path.expanduser('~')
    elif platform.system() == "Linux":
        return os.path.expanduser('~') + "/Desktop/"
    else:
        return ''


def exitmessage(tim, dict):
    if (len(dict)) > 0:
        print('Completed:', tim, "seconds\n", len(dict), "New cars found")
        # print("Press ESC key to exit")
        # keyboard.wait('esc','space')
    else:
        print('Completed:', tim, "seconds\nNo new cars")


def load_to_variable(dict_new, dict_disc_again, dict_disc, dict_nochanges, dict_red_nochanges, out_sold, time_of_parse):
    counter = 1
    # line = """{% extends 'base.html' %}
    #       {% block body %}
    #          """
    '''<!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
    <title>Dubizzle scraper by 2rbo</title>
    </head>
    <body>
    <script>
        document.write('<a href="' + document.referrer + '">Go Back</a>');
    </script>
    '''

    if not dict_new:
        line = "<center><h2> No new cars " + time_of_parse + "</center></h2>"
    if dict_new:
        line = "<center><h2> New cars " + time_of_parse + "</center></h2>"
        line += """
        <table class="new">
            <tr>
                <th>#</th>
                <th>Posted</th>
                <th>Model</th>
                <th>Price</th>
                <th>Year</th>
                <th>Mileage</th>
                <th>Link</th>
            </tr>
        """

        for i in dict_new:
            line += """
                <tr>
                <td width="5%">""" + str(counter) + """</td>
                    <td width="10%">""" + i['ad_posted'] + """</td>
                    <td class="textfield" width="20%">""" + i['brand'] + " " + i['model'] + """</td>
                    <td width="8%">""" + i['price'] + """</td>
                    <td width="7%">""" + i['year'] + """</td>
                    <td width="10%">""" + i['mileage'] + """</td>
                    <td class="textfield" width="40%"><a href='""" + i['href'] + """'>""" + i['title_test'] + """</a><br/></td>
                </tr>

            """

            counter += 1
        line += """
                  </table>
                    """

    if not dict_disc_again:
        pass  # line = ""
    else:
        line += "<center><h2>  Price reduced AGAIN! </center></h2>"
        line += """
            <table>
                <tr>
                    <th>#</th>
                    <th>Posted</th>
                    <th>Model</th>
                    <th>Price</th>
                    <th>Old price</th>
                    <th>Year</th>
                    <th>Mileage</th>
                    <th>Link</th>
                </tr>
        """
        for i in dict_disc_again:
            line += """
                <tr>
                    <td width="4%"><center>""" + str(counter) + """</td>
                    <td width="9%">""" + str(i['ad_posted']) + """</td>
                    <td class="textfield" width="19%">""" + i['brand'] + " " + i['model'] + """</td>
                    <td width="8%">""" + str(i['price']) + """</td>
                    <td width="8%">""" + str(i['oldprice']) + """</td>
                    <td width="6%">""" + str(i['year']) + """</td>
                    <td width="9%">""" + str(i['mileage']) + """</td>
                    <td class="textfield" width="39%"><a href='""" + i['href'] + """'>""" + i['title_test'] + """</a><br/></td>
                </tr>

            """
            counter += 1
        line += """
                  </table>
                    """

    if not dict_disc:
        pass  # line = ""
    else:
        line += "<center><h2>  Price reduced </center></h2> "
        line += """
        <table>
            <tr>
                <th>#</th>
                <th>Posted</th>
                <th>Model</th>
                <th>Price</th>
                <th>Old price</th>
                <th>Year</th>
                <th>Mileage</th>
                <th>Link</th>
            </tr>
        """
        for i in dict_disc:
            line += """
                <tr>
                    <td width="4%"><center>""" + str(counter) + """</td>
                    <td width="9%">""" + str(i['ad_posted']) + """</td>
                    <td class="textfield" width="19%">""" + i['brand'] + " " + i['model'] + """</td>
                    <td width="8%">""" + str(i['price']) + """</td>
                    <td width="8%">""" + str(i['oldprice']) + """</td>
                    <td width="6%">""" + str(i['year']) + """</td>
                    <td width="9%">""" + str(i['mileage']) + """</td>
                    <td class="textfield" width="39%"><a href='""" + i['href'] + """'>""" + i['title_test'] + """</a><br/></td>
                </tr>

            """
            counter += 1
        line += """
                  </table>
                    """

    if not dict_nochanges:
        pass  # line = ""
    else:
        line += "<center><h2>  Old Cars </center></h2>"
        line += """
        <table>
            <tr>
                <th>#</th>
                <th>Posted</th>
                <th>Model</th>
                <th>Price</th>
                <th>Year</th>
                <th>Mileage</th>
                <th>Link</th>
            </tr>
        """
        for i in dict_nochanges:
            line += """
                <tr>
                    <td width="5%">""" + str(counter) + """</td>
                    <td width="10%">""" + i['ad_posted'] + """</td>
                    <td class="textfield" width="20%">""" + i['brand'] + " " + i['model'] + """</td>
                    <td width="8%">""" + i['price'] + """</td>
                    <td width="7%">""" + i['year'] + """</td>
                    <td width="10%">""" + i['mileage'] + """</td>
                    <td class="textfield" width="40%"><a href='""" + i['href'] + """'>""" + i['title_test'] + """</a><br/></td>
                </tr>
            """
            counter += 1
        line += """
              </table>
                """
    if not dict_red_nochanges:
        pass  # line = ""
    else:
        line += """
        <br>
        <table>
        <tr>
            <th>#</th>
            <th>Posted</th>
            <th>Model</th>
            <th>Price</th>
            <th>Old price</th>
            <th>Year</th>
            <th>Mileage</th>
            <th>Link</th>
        </tr>
        """
        for i in dict_red_nochanges:
            #  =================  output in a format => because of no old price only
            line += """<tr><td width="4%"><center> {} </td><td width="11%"> {} </td><td class="textfield" width="19%"> {} {} </td><td width="7%"> {}</td>
            <td width="7%"> {} </td><td width="6%"> {} </td><td width="9%"> {} </td><td class="textfield" width="39%"><a href='{}'>{}</a><br/></td>
            </tr>""".format(str(counter), i['ad_posted'], i['brand'], i['model'], i['price'], i['oldprice'], i['year'],
                            i['mileage'], i['href'], i['title_test'])
            '''line = """
                <tr>
                    <td width="4%"><center>""" + str(counter) + """</td>
                    <td width="9%">""" + i['ad_posted'] + """</td>
                    <td class="textfield" width="19%">""" + i['brand'] + " " + i['model'] + """</td>
                    <td width="9%">""" + i['price'] + """</td>
                    <td width="9%">""" + i['oldprice'] + """</td>
                    <td width="6%">""" + i['year'] + """</td>
                    <td width="9%">""" + i['mileage'] + """</td>
                    <td class="textfield" width="37%"><a href='""" + i['href'] + """'>""" + i['title_test'] + """</a><br/></td>
                </tr>
            """'''
            counter += 1
        line += """
            </table>
            """
    if not out_sold:
        pass  # instead of line = ""
    else:
        line += "<center><h2>  Sold Cars </center></h2>"
        line += """
        <table>
            <tr>
                <th>#</th>
                <th>Posted</th>
                <th>Model</th>
                <th>Price</th>
                <th>Year</th>
                <th>Mileage</th>
                <th>Link</th>
            </tr>
        """
        for i in out_sold:
            line += """
                <tr>
                    <td width="3%">""" + str(counter) + """</td>
                    <td width="11%">""" + str(i['ad_posted']) + """</td>
                    <td class="textfield" width="21%">""" + i['brand'] + " " + i['model'] + """</td>
                    <td width="7%">""" + str(i['price']) + """</td>
                    <td width="7%">""" + str(i['year']) + """</td>
                    <td width="10%">""" + str(i['mileage']) + """</td>
                    <td class="textfield" width="41%"><a href='""" + i['href'] + """'>""" + i['title_test'] + """</a><br/></td>
                </tr>
                    """
            counter += 1
        line += """
            </table>
            """

    # line += "{% endblock %}"
    # </body></html>
    return line
