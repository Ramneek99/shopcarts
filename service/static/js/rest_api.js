$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_product_form_data(res){
        $("#customer_id").val(res.shopcart_id);
        $("#product_id").val(res.id);
        $("#product_name").val(res.name);
        $("#product_quantity").val(res.quantity);
        $("#product_price").val(res.price);
    }
    function update_shopcart_form_data(res){
        $("#customer_id").val(res.customer_id);
    }
    /// Clears all form fields
    function clear_form_data() {
        $("#product_id").val("");
        $("#product_name").val("");
        $("#product_quantity").val("");
        $("#product_price").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create A Shop cart with product
    // ****************************************

    $("#create-btn").click(function () {

        let customer_id = $("#customer_id").val();

        let data = {
            "customer_id": customer_id,
            "products":[]
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: `/shopcarts/${customer_id}`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_shopcart_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Retrieve a Shop Cart
    // ****************************************

    $("#retrieve-btn").click(function () {

        let customer_id = $("#customer_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/shopcarts/${customer_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_shopcart_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });
    // ****************************************
    // List Products of a Shop Cart
    // ****************************************
 
    $("#list-btn").click(function () {

        let customer_id = $("#customer_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/shopcarts/${customer_id}/products`,
            contentType: "application/json",
            data: ''
        })
         
        ajax.done(function(res){
            //alert(res.toSource())
            $("#list_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Name</th>'
            table += '<th class="col-md-2">Quantity</th>'
            table += '<th class="col-md-2">Price</th>'
            table += '</tr></thead><tbody>'
            let firstProduct = "";
            for(let i = 0; i < res.length; i++) {
                let product = res[i];
                table +=  `<tr id="row_${i}"><td>${product.id}</td><td>${product.name}</td><td>${product.quantity}</td><td>${product.price}</td></tr>`;
                if (i == 0) {
                    firstProduct = product;
                }
            }
            table += '</tbody></table>';
            $("#list_results").append(table);

                    // copy the first result to the form
            if (firstPet != "") {
                update_form_data(firstPet)
            }
        
                flash_message("Success")
            });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });
    // ****************************************
    // Clear a Shop Cart
    // ****************************************

    $("#clear-btn").click(function () {

        let customer_id = $("#customer_id").val();
        let data = {
            "customer_id": customer_id,
            "products":[]
        };
        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/shopcarts/${customer_id}/clear`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_shopcart_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Shop Cart
    // ****************************************

    $("#delete-btn").click(function () {

        let customer_id = $("#customer_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/shopcarts/${customer_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_shopcart_form_data()
            flash_message("Shop Cart has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-form-btn").click(function () {
        $("#customer_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Add a Product
    // ****************************************
 
    $("#add-btn").click(function () {

        let customer_id = $("#customer_id").val();
        let product_id = $("#product_id").val();
        let price = $("#product_price").val();
        let quantity = $("#product_quantity").val();
        let name = $("#product_name").val();

        $("#flash_message").empty();

        let data = {
            "shopcart_id": customer_id,
            "name":name,
            "price":price,
            "quantity":quantity,
            "id":product_id
        };
        let ajax = $.ajax({
            type: "POST",
            url: `/shopcarts/${customer_id}/products`,
            contentType: "application/json",
            data: JSON.stringify(data),
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_product_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // delete a Product
    // ****************************************
 
    $("#delete-product-btn").click(function () {

        let customer_id = $("#customer_id").val();
        let product_id = $("#product_id").val();


        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/shopcarts/${customer_id}/products/${product_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Product has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });

    });

    // ****************************************
    // Update a Product
    // ****************************************
 
    $("#update-btn").click(function () {

        let customer_id = $("#customer_id").val();
        let product_id = $("#product_id").val();
        let price = $("#product_price").val();
        let quantity = $("#product_quantity").val();
        let name = $("#product_name").val();

        $("#flash_message").empty();

        let data = {
            "shopcart_id": customer_id,
            "name":name,
            "price":price,
            "quantity":quantity,
            "id":product_id
        };

        let ajax = $.ajax({
            type: "PUT",
            url: `/shopcarts/${customer_id}/products/${product_id}`,
            contentType: "application/json",
            data: JSON.stringify(data),
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_product_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Search for a Shop Cart based on a product
    // ****************************************

    $("#search-btn").click(function () {

        let name = $("#pet_name").val();
        let category = $("#pet_category").val();
        let available = $("#pet_available").val() == "true";

        let queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (category) {
            if (queryString.length > 0) {
                queryString += '&category=' + category
            } else {
                queryString += 'category=' + category
            }
        }
        if (available) {
            if (queryString.length > 0) {
                queryString += '&available=' + available
            } else {
                queryString += 'available=' + available
            }
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/pets?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Name</th>'
            table += '<th class="col-md-2">Category</th>'
            table += '<th class="col-md-2">Available</th>'
            table += '<th class="col-md-2">Gender</th>'
            table += '<th class="col-md-2">Birthday</th>'
            table += '</tr></thead><tbody>'
            let firstPet = "";
            for(let i = 0; i < res.length; i++) {
                let pet = res[i];
                table +=  `<tr id="row_${i}"><td>${pet.id}</td><td>${pet.name}</td><td>${pet.category}</td><td>${pet.available}</td><td>${pet.gender}</td><td>${pet.birthday}</td></tr>`;
                if (i == 0) {
                    firstPet = pet;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstPet != "") {
                update_form_data(firstPet)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
