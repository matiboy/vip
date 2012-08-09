"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.utils import unittest
import cms.models
import students.models
import django.contrib.auth
from django.test.client import Client
import VIP.tests
from django.core.urlresolvers import reverse, reverse_lazy
import json

class CMSTest:
    def login(self, client):
        # Login
        client.login(username="mat", password="m1x3r.")
        
    def json_response(self, payload):
        return json.loads(payload)
    
    def is_successful_json(self, payload):
        decoded = self.json_response(payload)
        self.assertEqual(decoded["success"], True)

class StudentCreateTest(unittest.TestCase,CMSTest):
    def try_create_student(self, data=None):
        if data is None:
            return
        
        else:
            return c.post(reverse("students.student.create"),data)
        
    def test_logged_in_correct_data(self):
        c = Client()
        
        self.login(c)
        
        # Attempt to create
        username = "back.to@thefuture.com"
        data = {"first_name":"Emett",
                "last_name":"Brown",
                "email":username,
                "facebook_id":"456465465",
                "date_of_birth":"1985-11-05"
                }
        
        response = self.try_create_student(data)
        
        # 200 response
        self.assertEqual(response.status_code, 200)
        
        # Reload from db and check that object was saved
        try:
            after_save = students.models.Student.objects.get(user__username=username)
        except:
            after_save = None
        
        self.assertEqual(after_save, False)
        self.assertIsNotNone(after_save, "Student object not saved to db")
        
