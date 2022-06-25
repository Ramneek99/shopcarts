'''class ShopCart(db.Model):
    """
    Class that represents a ShopCart
    """

    app = None

    # Table Schema
    # customer_id
    # product_id
    # product_name
    # quantity
    # price
    customer_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(300), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return "<ShopCart customer_id=[%s]>" % (self.customer_id)

    def create(self, customer_id, product_id, product_name, quantity, price):
        """
        Creates a ShopCart to the database
        """
        logger.info("Creating %d", self.customer_id)
        self.customer_id = customer_id  # id must be user id to generate next primary key
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.price = price
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a ShopCart to the database
        """
        logger.info("Saving %d", self.customer_id)
        db.session.commit()

    def delete(self):
        """Removes a ShopCart from the data store"""
        logger.info("Deleting %d", self.customer_id)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Serializes a ShopCart into a dictionary"""
        shopcart = {
            "id": self.customer_id,
            "products": [],
        }
        for product in self.addresses:
            account["addresses"].append(address.serialize())
        return account

    def deserialize(self, data):
        """
        Deserializes a ShopCart from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.customer_id = data["customer_id"]
        except KeyError as error:
            raise DataValidationError("Invalid ShopCart: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid ShopCart: body of request contained bad or no data - "
                "Error message: " + error
            )
        return self

    @classmethod
    def init_db(cls, app):
        """Initializes the database session"""
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """Returns all of the ShopCarts in the database"""
        logger.info("Processing all ShopCarts")
        return cls.query.all()

    @classmethod
    def find(cls, customer_id, product_id):
        """Finds a ShopCart by it's user id"""
        logger.info("Processing lookup for customer_id: %d and product_id: %d ...", customer_id, product_id)
        return cls.query.get({"customer_id": customer_id, "product_id": product_id})

    @classmethod
    def find_by_product_name(cls, product_name):
        """Returns all ShopCarts with the given name

        Args:
            product_name (string): the name of the product you want to match
        """
        logger.info("Processing name query for %s ...", product_name)
        return cls.query.filter(cls.product_name == product_name)

    @classmethod
    def addItem(cls, customer_id, product_id, quantity):
        """Add a new item info to items list"""
        logger.info("Processing update query for %d ...", customer_id)
        shopCart = ShopCart.find(customer_id=customer_id, product_id=product_id)
        shopCart.quantity += quantity
        db.session.commit()'''
