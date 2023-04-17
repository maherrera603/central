from django.db.models import Manager

class PattientManager(Manager):
    def create_pattient(self, data, user):
        pattient = self.create(
            name = data['name'],
            lastname = data['lastname'],
            type_document= data['type_document'],
            document = data['document'],
            phone = data['phone'],
            id_user= user
        )
        return pattient
    
    def get_user(self, account):
        return self.get(id_user=account)
        

class FamilyManager(Manager):
    pass