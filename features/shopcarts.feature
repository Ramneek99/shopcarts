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