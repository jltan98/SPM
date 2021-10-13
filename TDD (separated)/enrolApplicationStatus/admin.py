class Admin:
    def __init__(self,
                 adminName="",
                 adminID="",
                 adminContact="",):
        self.adminName = adminName
        self.adminID = adminID
        self.adminContact = adminContact

    def get_name(self):
        return self.adminName

    def get_id(self):
        return self.adminID
        
    def get_contact(self):
        return self.adminContact


admin1 = Admin('HR', "Admin001", "hr@smu.edu.sg")

