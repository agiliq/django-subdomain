import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages

setup(
    name="django-subdomain",
    version="0.1",
    packages=['subdomains'],
    package_data={'subdomains': ['templates/*.html', 
                                 'templates/subdomains/*.html'],
                 },
    zip_safe=False,
    author="Agiliq Solutions",
    author_email="hello@agiliq.com",
    description="app to provide subdomain functionality in django project",
    url="http://agiliq.com/",
)
