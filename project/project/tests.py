"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse



class SubdomainAppTestcase(TestCase):

    def setUp(self):
        self.c = Client()

    def Indextestview(self):
        response = self.c.get(reverse("index"))    	
        self.assertEqual(200, response.status_code)

    def Submittestview(self):
        response = self.c.get(reverse("subdomain_form"))    	
        self.assertEqual(200, response.status_code)