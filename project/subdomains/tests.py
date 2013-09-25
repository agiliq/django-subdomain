from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.test.client import RequestFactory

import unittest

from subdomains.models import Subdomain, SubdomainSettingsNotAvailable
from subdomains.middleware import GetSubdomainMiddleware
from subdomains.context_processors import populate_subdomain
from subdomains.decorators import ensure_has_subdomain, ensure_is_main_subdomain

class TestSubdomainSettings(unittest.TestCase):
    def testget_settings(self):
        "Test get settings work"
        user = User.objects.create_user(username = 'Test3', password = 'Tset', email = 'test@example.com')
        
        subdomain = Subdomain.objects.register_new_subdomain(subdomain_text = 'foo3', name='Foo, the subdomain', description = 'Foo has not description', user = user)
        subdomain_settings = subdomain.get_settings()
        
class TestMiddleware(unittest.TestCase):
    def testGetSubdomainMiddleware1(self):
        "Test GetSubdomainMiddleware.process_request succeds without exceptions on a request."
        rf = RequestFactory(subdomain = 'foo')
        request = rf.request()
        middleware = GetSubdomainMiddleware()
        middleware.process_request(request)
    
    def testGetSubdomainMiddleware2(self):
        "Test GetSubdomainMiddleware.process_request populates the variables we need correctly"
        rf = RequestFactory(subdomain = 'www')
        request = rf.request()
        middleware = GetSubdomainMiddleware()
        middleware.process_request(request)
        self.assertEqual(request.META['subdomain'], 'www')
        self.assertEqual(request.subdomain, None)
    
        
    def testGetSubdomainMiddleware3(self):
        "Test GetSubdomainMiddleware.process_request populates the variables we need correctly"
        user = User.objects.create_user(username = 'Test4', password = 'Tset', email = 'test@example.com')
        subdomain = Subdomain.objects.register_new_subdomain(subdomain_text = 'foo4', name='Foo, the subdomain', description = 'Foo has not description', user = user)
        rf = RequestFactory(subdomain = 'foo4')
        request = rf.request()
        middleware = GetSubdomainMiddleware()
        middleware.process_request(request)
        self.assertEqual(request.META['subdomain'], 'foo4')
    
    def testGetSubdomainMiddleware4(self):
        "Test GetSubdomainMiddleware.process_request populates the variables we need correctly"
        user = User.objects.create_user(username = 'Testa1', password = 'Tset', email = 'test@example.com')
        subdomain = Subdomain.objects.register_new_subdomain(subdomain_text = 'fooa1', name='Foo, the subdomain', description = 'Foo has not description', user = user)
        subdomain.domain = 'bax.notfoo.tld'
        subdomain.save()
        rf = RequestFactory(domain = 'bax.notfoo.tld')
        request = rf.request()
        middleware = GetSubdomainMiddleware()
        middleware.process_request(request)
        self.assertEqual(request.META['domain'], 'bax.notfoo.tld')
    
    def testGetSubdomainMiddleware5(self):
        "Test GetSubdomainMiddleware.process_request populates the variables we need correctly"
        rf = RequestFactory(domain = 'boox.notfoo.tld')
        request = rf.request()
        middleware = GetSubdomainMiddleware()
        middleware.process_request(request)
        self.assertEqual(request.META['domain'], 'boox.notfoo.tld')

class TestContextProcessors(unittest.TestCase):
    def testpopulate_subdomain(self):
        user = User.objects.create_user(username = 'Test5', password = 'Tset', email = 'test@example.com')
        subdomain = Subdomain.objects.register_new_subdomain(subdomain_text = 'foo5', name='Foo, the subdomain', description = 'Foo has not description', user = user)
        rf = RequestFactory(subdomain = 'foo5', main_site = False)
        request = rf.request()
        middleware = GetSubdomainMiddleware()
        middleware.process_request(request)
        context = populate_subdomain(request)
        self.assertEqual(context['subdomain_text'], 'testserver')
        self.assertEqual(context['main_site'], False)
        self.assertEqual(context['subdomain'], None)
      
class TestDecorators(unittest.TestCase):
    def testensure_has_subdomain(self):
        def view_func(request):
            "Dummy view function to decorate"
            return HttpResponse('hello')
        view_func = ensure_has_subdomain(view_func)
        user = User.objects.create_user(username = 'Test6', password = 'Tset', email = 'test@example.com')
        subdomain = Subdomain.objects.register_new_subdomain(subdomain_text = 'foo6', name='Foo, the subdomain', description = 'Foo has not description', user = user)
        rf = RequestFactory(subdomain = 'foo6')
        request = rf.request()
        middleware = GetSubdomainMiddleware()
        middleware.process_request(request)
        response = view_func(request)
        self.assertEqual(HttpResponseRedirect, response.__class__)
        
    def testensure_has_subdomain2(self):
        def view_func(request):
            "Dummy view function to decorate"
            return HttpResponse('hello')
        view_func = ensure_has_subdomain(view_func)
        user = User.objects.create_user(username = 'Test7', password = 'Tset', email = 'test@example.com')
        subdomain = Subdomain.objects.register_new_subdomain(subdomain_text = 'foo7', name='Foo, the subdomain', description = 'Foo has not description', user = user)
        rf = RequestFactory(subdomain = 'doesnotexistxx')
        request = rf.request()
        middleware = GetSubdomainMiddleware()
        middleware.process_request(request)
        response = view_func(request)
        self.assertEqual(HttpResponseRedirect, response.__class__)
        
    def testensure_is_main_subdomain1(self):
        def view_func(request):
            "Dummy view function to decorate"
            return HttpResponse('hello')
        view_func = ensure_is_main_subdomain(view_func)
        rf = RequestFactory(subdomain = 'www')
        request = rf.request()
        middleware = GetSubdomainMiddleware()
        middleware.process_request(request)
        response = view_func(request)
        self.assertEqual(HttpResponseRedirect, response.__class__)
        
    def testensure_is_main_subdomain2(self):
        def view_func(request):
            "Dummy view function to decorate"
            return HttpResponse('hello')
        view_func = ensure_is_main_subdomain(view_func)
        rf = RequestFactory(subdomain = 'bar')
        request = rf.request()
        middleware = GetSubdomainMiddleware()
        middleware.process_request(request)
        response = view_func(request)
        self.assertEqual(HttpResponseRedirect, response.__class__)
        
        
        
# def create_subdomain_settings(subdomain):
#     from subdomains.models import SubdomainSettings
#     subdomain_settings = SubdomainSettings(subdomain = subdomain, foo = 'Foo', bar = 'Bar')
#     subdomain_settings.save()
