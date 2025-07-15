import mysql.connector
import sql


ARRAY = [
         [19,"OG Bareform Jacket","An original Bareform Jacket, made by OG founders, perfect for them frosty winters","Jacket","Grey","35.00",10,"jacket.png"],
         [20,"OG Bareform Hoodie","An original Bareform Hoodie, made by OG founders, designed for comfort and a warm appeal","Hoodie","Grey","55.00",10,"hoodie.png"],
         [21,"OG Bareform Joggers","The first created Bareform clothing, made by the OG founders, and designed for the best feel and comfort","Joggers","Grey","39.99",10,"jogger.png"]
         ]
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="root",
    database="shopdb"
)

cursor = db.cursor()

for i in ARRAY:
    Code = "INSERT INTO products (product_id,product_name,description,type,colour,price,stock_quantity,image_url) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    print(i[7])
    Data = (i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7])

    cursor.execute(Code,Data)
    db.commit()

cursor.close()
db.close()



ARRAY = [["Classic Denim Jacket", "A timeless denim jacket with a relaxed fit, perfect for casual outings.", "Jacket", "Blue", "59.99", "120"],
         ["Slim Fit Black Jeans", "Sleek, slim-fit jeans with a black finish, ideal for evening wear or casual events.", "Jeans", "Black", "49.99", "150"],
         ["V-Neck Linen Shirt", "A light, breathable shirt made from linen, with a stylish V-neckline.", "Shirt", "White", "39.99", "80"],
         ["Grey Sweatpants", "Comfortable and casual sweatpants with an adjustable waistband.", "Pants", "Grey", "34.99", "200"],
         ["Red Puffer Jacket", "A lightweight yet warm puffer jacket, perfect for winter walks.", "Jacket", "Red", "99.99", "50"],
         ["Black Leather Boots", "Durable leather boots with a sleek finish, ideal for both work and play.", "Footwear", "Black", "129.99", "60"],
         ["White Cotton Tank Top", "A simple, comfortable cotton tank top for layering or solo wear.", "Top", "White", "19.99", "250"],
         ["Plaid Flannel Shirt", "A cozy, plaid-patterned flannel shirt with button-down closure.", "Shirt", "Red/Black", "39.99", "100"],
         ["Navy Blue Blazer", "A sophisticated navy blue blazer with a tailored fit, perfect for formal occasions.", "Blazer", "Navy Blue", "89.99", "75"],
         ["Charcoal Grey Hoodie", "A soft and cozy hoodie with a front pocket and adjustable hood.", "Hoodie", "Charcoal Grey", "49.99", "180"],
         ["Floral Summer Dress", "A flowy, lightweight summer dress with a vibrant floral pattern.", "Dress", "Multi-color", "69.99", "120"],
         ["Olive Green Cargo Shorts", "Casual cargo shorts with multiple pockets and a relaxed fit.", "Shorts", "Olive Green", "29.99", "200"],
         ["Black Midi Skirt", "A stylish midi skirt with a flattering silhouette and subtle pleats.", "Skirt", "Black", "39.99", "90"],
         ["Striped Polo Shirt", "A classic polo shirt featuring horizontal stripes and a comfortable fit.", "Shirt", "Navy/White Stripes", "34.99", "150"],
         ["Brown Chelsea Boots", "A sleek pair of Chelsea boots, made from premium leather with elastic side panels.", "Footwear", "Brown", "109.99", "45"],
         ["Cream Knit Sweater", "A soft, cream-colored knit sweater with a crew neck and relaxed fit.", "Sweater", "Cream", "59.99", "100"],
         ["Black Leather Belt", "A stylish black leather belt with a sleek metal buckle.", "Accessory", "Black", "24.99", "300"],
         ["Pink Knit Beanie", "A cozy knit beanie in a soft pink color, perfect for chilly days.", "Accessory", "Pink", "14.99", "500"]]