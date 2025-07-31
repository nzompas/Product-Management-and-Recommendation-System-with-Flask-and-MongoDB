# Product Management and Recommendation System with Flask and MongoDB

This project is a full-stack web application that enables users to manage and search products stored in a MongoDB database. It also includes a content-based recommendation system using vector similarity and a course crawler for university subjects.

## 🔧 Technologies Used

- **Backend**: Python, Flask, Flask-PyMongo, NumPy, Selenium
- **Frontend**: JavaScript, HTML/CSS
- **Database**: MongoDB
- **Others**: Flask-CORS, Chrome WebDriver

## 🚀 Features

- Add or update products with attributes such as name, year, price, color, and size
- Search products by name using MongoDB's text indexing
- Display results in a dynamic HTML table
- Recommend similar products based on content-based filtering (cosine similarity)
- Crawl university courses from a public site using Selenium

## 📁 API Endpoints

### `GET /search?name=product_name`
Returns a list of products whose names match the search query.

### `POST /add-product`
Adds a new product or updates an existing one based on its name.

### `POST /content-based-filtering`
Receives a product's attributes and returns a list of similar products based on feature vectors.

### `GET /crawler?semester=n`
Returns a list of university course names for a given semester using web scraping.
