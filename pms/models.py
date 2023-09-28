from django.db import models

# Create your models here.
class Sensor(models.Model):
    name = models.CharField(
        max_length=1000, default=None, null=True, blank=True)
    

    def __str__(self):
        return str(self.name)
    


from django.db import models

class Device(models.Model):
    username = models.CharField(max_length=150) 
    uname=models.CharField(
        max_length=1000, default=None, null=True, blank=True)
    passw=models.CharField(
        max_length=1000, default=None, null=True, blank=True)

    def __str__(self):
        return str(self.uname)


class Data(models.Model):
    sensor=models.ForeignKey(Sensor, on_delete=models.SET_NULL, null=True)
    device=models.ForeignKey(Device, on_delete=models.SET_NULL, null=True)
    data = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True)
    
    def __str__(self):
        name = str(self.sensor) + " " + str(self.device) + " " + str(self.data) + " " + str(self.created_at)
        return str(name) # type: ignore
