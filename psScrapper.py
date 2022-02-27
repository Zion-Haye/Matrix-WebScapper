from bs4 import BeautifulSoup
import requests

import xlsxwriter

workbook = xlsxwriter.Workbook('PriceSmart-Prices.xlsx')
worksheet = workbook.add_worksheet()


urlpart1 = 'https://www.pricesmart.com/site/tt/en/category/groceries?cat=G10D03&r119_r1_r3_r1:page='
urlpart2 = '&r119_r1_r3_r1:_sps=12'

row = 0
worksheet.write(row , 0 , "Product Name")
worksheet.write(row , 1 , "Price")
worksheet.write(row , 2 , "Availability")
worksheet.write(row , 3 , "Image URL")
row =  row + 1

for x in range(1 , 123):

    fullurl = urlpart1 + str(x) + urlpart2
    html_text = requests.get(fullurl).text
    #html_text = requests.get('https://www.pricesmart.com/site/tt/en/category/groceries?cat=G10D03&r119_r1_r3_r1:page=1&r119_r1_r3_r1:_sps=12').text
    #print(html_text)

    soup = BeautifulSoup(html_text, 'lxml')

    products = soup.find_all('div', class_ ='col-xs-12 col-sm-6 col-md-6 col-lg-3 px-3 px-sm-2 px-md-2 px-lg-2')

    for product in products:

        product_name = product.find('p', class_ = 'search-product-description')
        if(product_name != None):
            product_name = product.find('p', class_ = 'search-product-description').text.replace('\n','')
        else:
            product_name = "Unknown"

        product_price = product.find('strong', class_ ='currency')
        if(product_price != None):
            product_price = product.find('strong', class_ ='currency').text.replace('\n','')
        else:
            product_price = "Unknown"

        product_availability_false = product.find('i' ,class_ ='far fa-times-circle')
        if (product_availability_false != None):
            product_availability_false = product.find('i' ,class_ ='far fa-times-circle').text.replace('\n','')

        product_availability_true = product.find('i' ,class_ ='far fa-check-circle')
        if(product_availability_true != None):
            product_availability_true = product.find('i' ,class_ ='far fa-check-circle').text.replace('\n','')

        product_image_container = product.find('div', class_="search-product-image")
        image_link = "Unknown"
        if(product_image_container!= None):
            image = product_image_container.find('img')
            if(image!=None):
                image_link = image.attrs.get("src")
            #print(image_link)


        if(product_availability_true!=None):
           
            product_information = product_name + product_price + product_availability_true + image_link

            worksheet.write(row , 0 , product_name)
            worksheet.write(row , 1 , product_price)
            worksheet.write(row , 2 , product_availability_true)
            worksheet.write(row , 3 , image_link)

        else:
      
            product_information = product_name + product_price + product_availability_false + image_link

            worksheet.write(row , 0 , product_name)
            worksheet.write(row , 1 , product_price)
            worksheet.write(row , 2 , product_availability_false)
            worksheet.write(row , 3 , image_link)

        print(product_information)

        row =  row + 1

workbook.close()

#print(product_name)
#print(product_price)
#print(product_availability)