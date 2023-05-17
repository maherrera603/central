from django.db.models import Manager
from django.db.models import Q

class PattientManager(Manager):
    def get_pattient_by_document(self, document):
        try:
            return self.get(document=document)
        except self.model.DoesNotExist:
            return False

    def create_pattient(self, data, user):
        pattient = self.model()
        pattient.name = data["name"]
        pattient.lastname = data["lastname"]
        pattient.type_document = data["type_document"]
        pattient.document = data["document"]
        pattient.phone = data["phone"]
        pattient.id_user = user
        return pattient
    
    def get_user(self, user):
        try:
            return self.get(id_user=user)
        except self.model.DoesNotExist:
            return False
        

class FamilyManager(Manager):
    def get_families_by_pattient(self, pattient):
        return self.filter(id_pattient=pattient)
    
    def get_family_by_document(self, document):
        try:
            return self.get(document=document)
        except self.model.DoesNotExist:
            return False
    
    def create_family(self, data, pattient):
        family = self.model()
        family.name = data["name"]
        family.lastname = data["lastname"]
        family.type_document = data["type_document"]
        family.document = data["document"]
        family.phone = data["phone"]
        family.id_pattient = pattient
        return family
    
    def search_family(self, search, pattient):
        return self.filter(
            Q(name__icontains=search) | Q(lastname__icontains=search) | Q(document__icontains=search) 
        ).filter(id_pattient=pattient)
    