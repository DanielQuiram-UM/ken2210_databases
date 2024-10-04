class CurrentCustomer:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CurrentCustomer, cls).__new__(cls)
            cls._instance.customer = None
        return cls._instance

    def set_customer(self, customer):
        """Set the current customer"""
        self.customer = customer
        print("set the customer singleton")

    def clear(self):
        self.customer = None
