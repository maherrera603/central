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
    
    def get_cite_by_pk(self, pk):
        try:
            return self.get(pk=pk)
        except self.model.DoesNotExist:
            return False
        
        
    def update_cite(self, pk, data, doctor, statu):
        try:
            cite = self.get(pk=pk)
            cite.id_doctor = doctor
            cite.date_cite = data["date_cite"]
            cite.hour_cite = data["hour_cite"]
            cite.id_status = statu
            return cite
        except self.model.DoesNotExist:
            return False