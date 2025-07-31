# BEGIN CODE HERE
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
import numpy as np
from pymongo import TEXT
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json


# END CODE HERE

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/pspi"
CORS(app)
mongo = PyMongo(app)
mongo.db.products.create_index([("name", TEXT)])


@app.route("/search", methods=["GET"])
def search():
    # BEGIN CODE HERE

    name = request.args.get('name') # Λήψη της παραμέτρου "name" από το query string

    if not name:
        return jsonify([]) # Επιστροφή κενής λίστας αν δεν δόθηκε παράμετρος "name"

    # Φιλτράρισμα προϊόντων με βάση το όνομα, ταξινόμηση κατά τιμή
    filtered_products = list(mongo.db.products.find({'name': {'$regex': name, '$options': 'i'}}).sort("price", -1))


    for f in filtered_products:
        f["_id"] = str(f['_id']) # Μετατροπή ObjectID σε string για σωστή αποστολή στο JSON

    return jsonify(filtered_products)

    # END CODE HERE


@app.route("/add-product", methods=["POST"])
def add_product():
    # BEGIN CODE HERE
    product = request.get_json() # Λήψη δεδομένων JSON από το σώμα του αιτήματος

    # Έλεγχος εγκυρότητας τιμών
    production_year = int(product["production_year"])
    price = float(product["price"])
    color = int(product["color"])
    size = int(product["size"])

    # Έλεγχος αν το προϊόν υπάρχει ήδη στη βάση
    productExists=mongo.db.products.find_one({"name": product["name"]})

    if productExists:
        # Αν υπάρχει, ενημέρωση του προϊόντος
        mongo.db.products.update_one(
            {"name":product["name"]},
            {"$set": {
                "production_year": product["production_year"],
                "price": product["price"],
                "color": product["color"],
                "size": product["size"]
            }}
        )
        return jsonify({'res': "updated"})
    else:
        # Αν δεν υπάρχει, προσθήκη του προϊόντος
        mongo.db.products.insert_one({
            "name": product["name"],
            "production_year": production_year,
            "price": price,
            "color": color,
            "size": size
        })
        return jsonify({'res': "added"})

    # END CODE HERE


@app.route("/content-based-filtering", methods=["POST"])
def content_based_filtering():
    # BEGIN CODE HERE
    target_product = request.get_json() # Λήψη δεδομένων JSON από το σώμα του αιτήματος

    # Ελέγχουμε αν η τιμή του "size" είναι αριθμητική
    size = 0  # Προκαθορισμένη τιμή σε περίπτωση που η τιμή δεν είναι αριθμητική
    if isinstance(target_product["size"], str) and target_product["size"].isdigit():
        size = int(target_product["size"])
    elif isinstance(target_product["size"], int):
        size = target_product["size"]

   # Δημιουργία διανύσματος χαρακτηριστικών για το στοχείο προς αναζήτηση
    target_vector = np.array([
        int(target_product["production_year"]),
        float(target_product["price"]),
        target_product["color"],  
        size
    ])


    similar_products = []

    # Αναζήτηση παρόμοιων προϊόντων με βάση την ομοιότητα διανυσμάτων χαρακτηριστικών
    for product in mongo.db.products.find():
        product_size = 0
        # Έλεγχος αν η τιμή του "size" είναι αριθμητική
        if isinstance(product["size"], str) and product["size"].isdigit():
            product_size = int(product["size"])
        elif isinstance(product["size"], int):
            product_size=product["size"]

        vector = np.array([
            int(product["production_year"]),
            float(product["price"]),
            product["color"], 
            product_size
        ])
        similarity = np.dot(target_vector, vector) / (np.linalg.norm(target_vector) * np.linalg.norm(vector))
        if similarity > 0.7:
            similar_products.append(product['name'])

    return jsonify(similar_products)

    # END CODE HERE





@app.route("/crawler", methods=["GET"])
def crawler():
    # BEGIN CODE HERE
    semester = request.args.get('semester', type=int)

    url = f"https://qa.auth.gr/el/x/studyguide/600000438/current"

    # Ρυθμίσεις για το Selenium Chrome WebDriver
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    # Φόρτωση της σελίδας
    driver.get(url)

    # Εύρεση του πίνακα που περιέχει τα μαθήματα
    table_id = f"exam{semester}"
    table = driver.find_element(By.ID, table_id)

    # Λίστα για αποθήκευση των ονομάτων των μαθημάτων
    course_names = []

    # Εξαγωγή ονομάτων μαθημάτων από τον πίνακα
    for row in table.find_elements(By.CSS_SELECTOR, 'tr')[1:]:
        title_element = row.find_element(By.CSS_SELECTOR, '.title')
        course_names.append(title_element.text)
    

    driver.quit()

    return json.dumps(course_names, ensure_ascii=False)
    # END CODE HERE

if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)  