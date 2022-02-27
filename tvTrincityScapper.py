from bs4 import BeautifulSoup
import requests

import xlsxwriter

workbook = xlsxwriter.Workbook('TruValu-Trincity-Prices.xlsx')
worksheet = workbook.add_worksheet()

urlpart1 = 'https://shop.doortodoortt.com/trincity/shop/'
urlpart2 = 'page/'
urlpart3 = '/'

row = 0
worksheet.write(row , 0 , "Category")
worksheet.write(row , 1 , "Name")
worksheet.write(row , 2 , "Price")
worksheet.write(row , 3 , "Image_URL")
row =  row + 1

for x in range(1 , 651):

    if(x==1):
        fullurl = urlpart1
    else:
        fullurl = urlpart1 + urlpart2 + str(x) + urlpart3

    html_text = requests.get(fullurl).text

    soup = BeautifulSoup(html_text, 'lxml')

    products = soup.find_all('li', class_ ='ast-col-sm-12')

    for product in products:

        product_category = product.find('span', class_ ='ast-woo-product-category')
        if(product_category != None):
            product_category = product.find('span', class_ ='ast-woo-product-category').text.replace('\n','')
        else:
            product_category = "Unknown"

        product_name = product.find('h2', class_ = 'woocommerce-loop-product__title')
        if(product_name != None):
            product_name = product.find('h2', class_ = 'woocommerce-loop-product__title').text.replace('\n','')
        else:
            product_name = "Unknown"

        product_price = product.find('bdi')
        if(product_price != None):
            product_price = product.find('bdi').text.replace('\n','')
        else:
            product_price = "Unknown"
        
        product_image_container = product.find('div' , class_='astra-shop-thumbnail-wrap')
        image_link = "Unknown"
        if(product_image_container!=None):
            image =  product_image_container.find('img')
            if(image!=None):
                image_link = image.attrs.get("src")

        product_information = product_category + "\t" + product_name + "\t" + product_price + "\t" + image_link

        worksheet.write(row , 0 , product_category)
        worksheet.write(row , 1 , product_name)
        worksheet.write(row , 2 , product_price)
        worksheet.write(row , 3 , image_link)

        print(product_information)

        row =  row + 1

workbook.close()

#print(product_name)
#print(product_price)
#print(product_availability)