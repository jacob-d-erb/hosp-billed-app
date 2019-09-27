from django.db import models
import re
import datetime

class UserManager(models.Manager):
    
    def login_validator(self, postData):
        errors = {}

        if len(postData["admin_email_input"]) == 0:
            errors["email"] = "Please enter an email."
        
        if len(postData["admin_password_input"]) == 0:
            errors["password"] = "Please enter a password."
        try:
            test = User.objects.get(email=postData["admin_email_input"])
        except:
            errors["combination"] = "Email and password combination not valid."

        return errors


class HospitalManager(models.Manager):

    def hospital_validator(self, postData, csv_file):
        errors = {}

        if not csv_file.name.endswith('.csv'):
            errors["csv_file"] = "File is not CSV type."

        if len(postData["hosp_name_input"]) < 3:
            errors["hosp_name"] = "Please enter a hospital name."
        
        try:
            if float(postData["hosp_long_input"]) < -180 or float(postData["hosp_long_input"]) > 180:
                errors["hosp_long"] = "Please enter a valid longitude for the facility."
        except:
            errors["hosp_long"] = "Please enter a valid longitude for the facility."
        
        try: 
            if float(postData["hosp_lat_input"]) < -90 or float(postData["hosp_lat_input"]) > 90:
                errors["hosp_lat"] = "Please enter a valid latitude for the facility."
        except:
            errors["hosp_lat"] = "Please enter a valid latitude for the facility."

        if len(postData["hosp_source_input"]) < 3:
            errors["hosp_source"] = "Please enter a source."

        if len(postData["hosp_state_input"]) < 3:
            errors["hosp_region"] = "Please enter a region label for the hospital."

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class DRG(models.Model):
    ms_drg = models.CharField(max_length=3)
    drg_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Hospital(models.Model):
    name = models.CharField(max_length=255)
    drgs = models.ManyToManyField(DRG, through="HospitalDRG",related_name="coding_hospitals")
    longitude = models.FloatField()
    latitude = models.FloatField()
    source = models.CharField(max_length=255)
    state = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = HospitalManager()

class HospitalDRG(models.Model):
    hospital_id = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    drg_id = models.ForeignKey(DRG, on_delete=models.CASCADE)
    avg_allowed_charge = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)