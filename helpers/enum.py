class Roles():
    def __init__(self):
        self.switcher_by_name = {
            'admin': 1,
            'reseller': 2
        }

        self.switcher_by_number = {
            1: 'admin',
            2: 'reseller'
        }

    def enum_to_name(self, enum):
        return self.switcher_by_number.get(enum, 'Invalid Number')

    def name_to_enum(self, name):
        return self.switcher_by_name.get(name, 'Invalid Name')
