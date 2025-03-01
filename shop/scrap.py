"""
1. Enter link to be extracted
2. get content from the link
3. Extract relevant information from the link
4. Download images in a folder
5. upload image to the products folder(By django)
6. save the product.
7. Got to step 1.
"""



import requests
from bs4 import BeautifulSoup
import uuid
from shop.models import other_products
from django.core.files.base import ContentFile
from django.core.files import File as DjangoFile

def spider_writer(link, file_name):
	"""
	"links" parameter should be in a list format
	- Stores all urls in a database.
	"""
	database = open(f"C:/Users/lenovo/Desktop/{file_name}.txt", "a")
	database.write(link+"\n")
	database.close()
#spider_writer(["he","oekfoek","fmofe","foekfo","fiejfie","fjeiojeo"], "new_links")



def spider_checker(checked_link, file_name):
	"""
	Checks if a link exits in the specified file
	"""
	file = open(f"C:/Users/lenovo/Desktop/{file_name}.txt", "r")
	links = file.readlines()
	print(links)
	for link in links:
		if link == checked_link+"\n":
			file.close()
			return True
		else:
			continue
	file.close()
	return False

#print(spider_checker("he", "new_links"))


"""
Save the image saved from a given url.
Saves the image using a randon uuid
- Saves an image on the machine and then deletes it
"""
def save_image(pic_url):
	image_uuid = uuid.uuid4()
	save_dir = "/images/"#save_dir = "C:/Users/lenovo/Desktop/images/"
	with open(f'{save_dir}{image_uuid}.jpg', 'wb') as handle:
	    response = requests.get(pic_url.replace("150x150", "500x500"), stream=True)

	    if not response.ok:
	        print(response)

	    for block in response.iter_content(1024):
	        if not block:
	            break

	        handle.write(block)

	handle.close()
	# Return the image URL
	return f"{save_dir}{image_uuid}.jpg"

"""
Saves the contents of the page
- Name
- Images
- Price
- Category
- Brand
- Description
- Key Features
- Other Related Product Urls
"""

# Fetches and returns page content
def get_content(page_url):
	#page_content = ""
	try:
		page_content = requests.get(page_url)
	except:
		exit(0)
	return page_content.text

# Return a list of images
def get_image_links(list_of_images):
	links = []
	for image_link in list_of_images:
		link = image_link.get('data-src')
		links.append(str(link))
	return links


# Extract page content
def soup_page(page_content):
	soup = BeautifulSoup(page_content, 'html.parser')
	
	props = soup.find('a', {'id':'wishlist'})
	sbt = BeautifulSoup(str(props), 'html.parser')
	p_name = str(sbt.a['data-ga4-item_name'])
	p_brand = str(sbt.a['data-ga4-item_brand'])
	single_image = soup.find('img', {'class':'-fw -fh'})

	try:
		p_discount = str(sbt.a['data-ga4-discount'])
	except:
		p_discount = "0"
	try:
		p_category = str(sbt.a['data-ga4-item_category'])
	except:
		p_category = "NONE"
	try:
		p_category2 = str(sbt.a['data-ga4-item_category2'])
	except:
		p_category2 = "NONE"
	try:
		p_category3 = str(sbt.a['data-ga4-item_category3'])
	except:
		p_category3 = "NONE"
	try:
		p_category4 = str(sbt.a['data-ga4-item_category4'])
	except:
		p_category4 = "NONE"
	try:
		p_category5 = str(sbt.a['data-ga4-item_category5'])
	except:
		p_category5 = "NONE"
	p_price = str(float(sbt.a['data-ga4-price'])*3950)
	#print(sbt.a['data-moengage-product_image'])
	images = get_image_links(soup.find_all("img", class_="-fw _ni"))

	try:
		image = images[0]
		i0 = open(save_image(str(images[0])), 'rb')
	except:
		image = single_image.get('data-src')
		i0 = open(save_image(str(image)), 'rb')

	try:
		image1 = images[1]
		i1 = open(save_image(str(images[1])), 'rb')
	except:
		pass
	try:
		image2 = images[2]
		i2 = open(save_image(str(images[2])), 'rb')
	except:
		pass
	try:
		image3 = images[3]
		i3 = open(save_image(str(images[3])), 'rb')
	except:
		pass

	desc = str(soup.find("div", class_="markup -mhm -pvl -oxa -sc").get_text())
	specs = str(soup.find("div", class_="markup -pam").get_text())
	product = other_products.objects.create(
		name = p_name,
		brand=p_brand,
		discount=p_discount,
		category=p_category,
		category2=p_category2,
		category3=p_category3,
		category4 = p_category4,
		category5 = p_category5,
		price=p_price,
		description = desc,
		specifications = specs,
		#image = DjangoFile(i0, name=str(uuid.uuid4())),
		#image1 = i1,
		#image2 = i2,
		#image3 = i3
		)
	image_name = uuid.uuid4()
	image_name_1 = uuid.uuid4()
	image_name_2 = uuid.uuid4()
	image_name_3 = uuid.uuid4()
	product.image.save(str(f"{image_name}.jpg"), DjangoFile(i0, name=str(f"{image_name}.jpg")))
	try:
		product.image1.save(str(f"{image_name_1}.jpg"), DjangoFile(i1, name=str(f"{image_name_1}.jpg")))
	except:
		pass
	try:
		product.image2.save(str(f"{image_name_2}.jpg"), DjangoFile(i2, name=str(f"{image_name_2}.jpg")))
	except:
		pass
	try:
		product.image3.save(str(f"{image_name_3}.jpg"), DjangoFile(i3, name=str(f"{image_name_3}.jpg")))
	except:
		pass
	product.save()


	# close open files
	i0.close()
	try:
		i1.close()
	except:
		pass
	try:
		i2.close()
	except:
		pass
	try:
		i3.close()
	except:
		pass

#soup_page(get_content("https://www.jumia.ug/lg-20-litres-microwave-solo-with-glass-door-ms2043db-black-lg-mpg2698.html"))

def get_links_from_page(page_content):
	soup = BeautifulSoup(page_content, 'html.parser')
	links = soup.find_all('a')
	for link in links:
		print(link.get('href'))