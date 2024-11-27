class EmptyDraftOrder(ValueError):
    def __init__(self):
        super().__init__("The list of products from the draft order is empty!")