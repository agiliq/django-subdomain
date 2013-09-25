from django.shortcuts import render_to_response
from django.template import RequestContext

from subdomains.forms import SubdomainForm

def subdomainform(request):
	form = SubdomainForm()
	return render_to_response('project/subdomainform.html', {'form':form}, \
		context_instance=RequestContext(request))