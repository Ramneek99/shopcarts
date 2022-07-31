Feature: The shopcarts service back-end
    As a Shopcarts Manager 
    I need a RESTful catalog service
    So that I can keep track of all the shopcarts

Background:
    Given the following shopcarts 
        | customer_id | id | name           | quantity | price |
        | 1           | 1  | Apple Watch    | 1        | 100   |
        | 1           | 2  | Macbook Pro    | 15       | 520   |
        | 2           | 3  | iPhone13       | 14       | 250   |
        | 2           | 4  | Apple Watch    | 5        | 130   |
        | 3           | 5  | iPad           | 7        | 150   |
        | 3           | 6  | Apple Belt     | 9        | 12    |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Shop Cart Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Add a Product
    When I visit the "Home Page"
    And I set the "Product Name" to "Water"
    And I set the "Product Quantity" to "12"
    And I set the "Customer ID" to "1"
    And I set the "Product Price" to "2.75"
    And I press the "Add" button
    Then I should see the message "Success"
    When I copy the "Customer ID" field
    And I press the "Clear-Form" button
    Then the "Product ID" field should be empty 
    And the "Product Name" field should be empty
    And the "Product Price" field should be empty
    And the "Product Quantity" field should be empty
    And the "Customer ID" field should be empty
    When I paste the "Customer ID" field
    And I press the "List" button
    Then I should see the message "Success"
    And I should see "Water" in the results
    And I should see "Apple Watch" in the results
    And I should see "Macbook Pro" in the results

Scenario: Delete a Product
    When I visit the "Home Page"
    And I set the "Customer ID" to "1"
    And I press the "List" button
    Then I should see the message "Success"
    And I should see "Apple Watch" in the results
    And I should see "Macbook Pro" in the results
    When I copy the "Product ID" field
    And I press the "Clear-Form" button
    Then the "Product ID" field should be empty 
    And the "Product Name" field should be empty
    And the "Product Price" field should be empty
    And the "Product Quantity" field should be empty
    And the "Customer ID" field should be empty
    When I paste the "Product ID" field
    And I set the "Customer ID" to "1"
    And I press the "Delete-Product" button
    Then I should see the message "Product has been Deleted!"
    When I press the "Clear-Form" button
    Then the "Product ID" field should be empty 
    And the "Product Name" field should be empty
    And the "Product Price" field should be empty
    And the "Product Quantity" field should be empty
    And the "Customer ID" field should be empty
    When I set the "Customer ID" to "1"
    And I press the "List" button
    Then I should see the message "Success"
    And I should see "Macbook Pro" in the results

Scenario: Update a Product
    When I visit the "Home Page"
    And I set the "Customer ID" to "1"
    And I press the "List" button
    Then I should see the message "Success"
    And I should see "Apple Watch" in the results
    And I should see "Macbook Pro" in the results
    When I set the "Customer ID" to "1"
    And I set the "Product Name" to "Milk"
    And I press the "Update" button
    Then I should see the message "Success"
    When I press the "Clear-Form" button
    Then the "Product ID" field should be empty 
    And the "Product Name" field should be empty
    And the "Product Price" field should be empty
    And the "Product Quantity" field should be empty
    And the "Customer ID" field should be empty
    When I set the "Customer ID" to "1"
    And I press the "List" button
    Then I should see the message "Success"
    And I should see "Milk" in the results
    And I should see "Macbook Pro" in the results

Scenario: Create Shopcart
    When I visit the "Home Page"
    And I set the "Customer ID" to "1"
    And I press the "Create" button
    Then I should see the message "409 Conflict: Shopcart 1 already exists"
    When I press the "Clear-Form" button
    Then the "Product ID" field should be empty 
    And the "Product Name" field should be empty
    And the "Product Price" field should be empty
    And the "Product Quantity" field should be empty
    And the "Customer ID" field should be empty
    When I set the "Customer ID" to "4"
    And I press the "Create" button
    Then I should see the message "Success"
    When I press the "List-Shopcart" button
    Then I should see the message "Success"
    And I should see "4" in the results

Scenario: Clear Shopcart
    When I visit the "Home Page"
    And I set the "Customer ID" to "1"
    And I press the "List" button
    Then I should see "Apple Watch" in the results
    And I should see "Macbook Pro" in the results
    When I press the "Clear" button
    Then I should see the message "Success"
    When I press the "Clear-Form" button
    Then the "Product ID" field should be empty 
    And the "Product Name" field should be empty
    And the "Product Price" field should be empty
    And the "Product Quantity" field should be empty
    And the "Customer ID" field should be empty
    When I set the "Customer ID" to "1"
    And I press the "List" button
    Then I should see the message "Success"
    And I should not see "Apple Watch" in the results
    And I should not see "Macbook Pro" in the results

Scenario: List Shopcarts
    When I visit the "Home Page"
    And I press the "List-Shopcart" button
    Then I should see "1" in the results
    Then I should see "2" in the results
    Then I should see "3" in the results

Scenario: Read Shopcart
    When I visit the "Home Page"
    And I set the "Customer ID" to "1"
    And I press the "List" button
    Then I should see the message "Success"
    And I should see "Apple Watch" in the results
    And I should see "Macbook Pro" in the results

Scenario: Search by Product Name
    When I visit the "Home Page"
    And I set the "Product Name" to "Apple Watch"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "1" in the results
    And I should see "2" in the results

Scenario: Retrieve a Shop Cart
    When I set the "Customer ID" to "1"
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "1" in the "Customer ID" field
