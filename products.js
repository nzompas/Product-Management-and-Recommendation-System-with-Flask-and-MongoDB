const api = "http://127.0.0.1:5000";

window.onload = () => {
    // BEGIN CODE HERE
    document.getElementById('search').addEventListener('click', searchButtonOnClick);
    document.getElementById('add-product-submit').addEventListener('click', productFormOnSubmit);

    // END CODE HERE
}

// Συνάρτηση για την εμφάνιση δεδομένων στον πίνακα
tableData = (products)=>{
    const tableBody = document.getElementById('table-body');
    htmlData = "";
    
    // Δημιουργούμε τις γραμμές του πίνακα με τα δεδομένα των προϊόντων
    products.forEach(product => {
        color ='';
        if (product.color==1){
            color='Κόκκινο';
        }
        else if (product.color==2){
            color='Κίτρινο';
        }
        else if (product.color==3){
            color='Μπλε';
        }
    
        size = '';
        if (product.size==1){
            size='Small';
        }
        else if (product.size==2){
            size='Medium';
        }
        else if (product.size==3){
            size='Large';
        }
        else if(product.size==4) {
            size='Extra large';
        }

        htmlData += `
        <tr>
            <td>${product._id}</td>
            <td>${product.name}</td>
            <td>${product.production_year}</td>
            <td>${product.price}</td>
            <td>${color}</td>
            <td>${size}</td>
        </tr>`;
    });

    // Εμφανίζουμε τα δεδομένα στον πίνακα
    tableBody.innerHTML = htmlData;

}

// Συνάρτηση για το κλικ στο κουμπί αναζήτησης
searchButtonOnClick = (event) => {
    // BEGIN CODE HERE

    event.preventDefault();

    // Λαμβάνουμε την τιμή της αναζήτησης από το input field
    var nameInput = document.getElementById('nameInput').value;
    
    // Κάνουμε αίτηση στο API για αναζήτηση προϊόντων με βάση το όνομα
    fetch(api+'/search?name=' + nameInput, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('Name received from server:', data);
        // Εμφανίζουμε τα δεδομένα στον πίνακα
        tableData(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
    
    // END CODE HERE
}

// Συνάρτηση για την υποβολή της φόρμας προσθήκης προϊόντος
productFormOnSubmit = (event) => {
    // BEGIN CODE HERE

    event.preventDefault();

    // Λαμβάνουμε τις τιμές από τη φόρμα
    const name = document.getElementById('productName').value;
    const production_year = parseInt(document.getElementById('productProductionYear').value);
    const price = parseFloat(document.getElementById('productPrice').value);
    const color = parseInt(document.getElementById('productColor').value);
    const size = parseInt(document.getElementById('productSize').value);

    // Έλεγχος εγκυρότητας των τιμών
    if (isNaN(production_year) || isNaN(price) || isNaN(color) || isNaN(size)) {
        alert("Παρακαλώ εισάγετε έγκυρους αριθμούς για το έτος παραγωγής, την τιμή, το χρώμα και το μέγεθος.");
        document.getElementById('productForm').reset();
        return;
    }

    // Δημιουργία JSON object
    const product = {
        "name": name,
        "production_year": production_year,
        "price": price,
        "color": color,
        "size": size
    };

    // Αποστολή του JSON object στο API για προσθήκη προϊόντος
    fetch(`${api}/add-product`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(product)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        document.getElementById('productForm').reset();// Επαναφορά της φόρμας
        alert("ΟΚ"); // Εμφάνιση μηνύματος επιτυχίας
    })
    .catch(error => {
        console.error('Error:', error);
    });

    // END CODE HERE
}