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
        pattient.last_name = data["last_name"]
        pattient.type_document = data["type_document"]
        pattient.document = data["document"]
        pattient.phone = data["phone"]
        pattient.user = user
        return pattient
    
    def get_user(self, user):
        try:
            return self.get(user=user)
        except self.model.DoesNotExist:
            return False
        

class FamilyManager(Manager):
    def get_families_by_pattient(self, pattient):
        return self.filter(pattient=pattient)
    
    def get_family_by_document(self, document):
        try:
            return self.get(document=document)
        except self.model.DoesNotExist:
            return False
    
    def create_family(self, data, pattient):
        family = self.model()
        family.name = data["name"]
        family.last_name = data["last_name"]
        family.type_document = data["type_document"]
        family.document = data["document"]
        family.phone = data["phone"]
        family.pattient = pattient
        return family
    
    def search_family(self, search, pattient):
        return self.filter(
            Q(name__icontains=search) | Q(last_name__icontains=search) | Q(document__icontains=search) 
        ).filter(pattient=pattient)
    