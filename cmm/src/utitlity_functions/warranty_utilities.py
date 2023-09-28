from cmm.models import Cmm_Warranty, Cmm_Warranty_New

class CmmUtilitie:
    """ UTILITY FUNCTIONS FOR CMM """
    
    def get_data(type):
        """ Get data from cmm data table 
            usage example : get_data('train_number')
            types: train_number, coach_number, coach_type, owning_rly, vehicle_type, department, workshop 
        """
        data = list(Cmm_Warranty.objects.all().values_list(type, flat=True))
        data_set = set(data)
        return list(data_set)


class CmmUtilitie_new:
    """ UTILITY FUNCTIONS FOR CMM """
    
    def get_data(type):
        """ Get data from cmm data table 
            usage example : get_data('train_number')
            types: train_number, coach_number, coach_type, owning_rly, vehicle_type, department, workshop 
        """
        data = list(Cmm_Warranty_New.objects.all().values_list(type, flat=True))
        data_set = set(data)
        return list(data_set)