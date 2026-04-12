class PetItem:
    def __init__(self, name, breed, info, qty, srp, img):
        self.name = name
        self.breed = breed
        self.info = info
        self.qty = int(qty)
        self.srp = float(srp)
        self.img = img

class ThePetShop:
    def __init__(self):
        self.users = []
        self.catalog = []
        self.load_all()

    def load_all(self):

       
