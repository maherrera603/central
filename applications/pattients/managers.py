from django.db.models import Manager

class PattientManager(Manager):
    def create_pattient(self, data, user):
        pattient = self.create(
            name = data["name"],
            lastname = data["lastname"],
            type_document= data["type_document"],
            document = data["document"],
            phone = data["phone"],
            id_user= user
        )
        return pattient
    
    def get_user(self, account):
        return self.get(id_user=account)
    
    def get_pattient(self, document):
        return self.get(document=document)
    
    def update_pattient(self, document, data):
        pattient = self.get(document=document)
        pattient.name = data["name"]
        pattient.lastname = data["lastname"]
        pattient.type_document = data["type_document"]
        pattient.document = data["document"]
        pattient.phone = data["phone"]
        return pattient
    
    def get_pattient_by_id(self, pk):
        return self.get(pk=pk)
    
    def get_pattient_by_id_user(self, id_user):
        return self.get(id_user=id_user)
        

class FamilyManager(Manager):
    def obtain_familys(self, pk_pattient):
        return self.filter(id_pattient= pk_pattient)
    
    def create_family(self, data, pattient):
        family = self.model()
        family.name = data["name"]
        family.lastname = data["lastname"]
        family.type_document = data["type_document"]
        family.document = data["document"]
        family.phone = data["phone"]
        family.id_pattient = pattient
        return family
    
    def get_family_by_id(self, pk):
        data = {}
        try:
            data["family"] = self.get(pk=pk)
            data["exists"] = True
        except self.model.DoesNotExist:
            data["exists"] = False
        return data