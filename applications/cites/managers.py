from django.db.models import Manager

class CiteManager(Manager):
    def get_cites_by_pattient(self, pattient):
        return self.filter(id_pattient=pattient)
    
    def created_cite(self, data, speciality, status, pattient):
        cite = self.model()
        cite.name = data["name"]
        cite.lastname = data["lastname"]
        cite.type_document = data["type_document"]
        cite.document = data["document"]
        cite.phone = data["phone"]
        cite.eps = data["eps"]
        cite.id_speciality = speciality
        cite.id_status = status
        cite.id_pattient = pattient
        return cite