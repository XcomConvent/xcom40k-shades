from django.test import TestCase

# Create your tests here.

import datetime

from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth import views, logout
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseServerError
import logging
from django.utils import timezone
from .forms import *
from .models import *
from xcom40k.settings import BUILD_NAME, BUILD_VERSION
from . import models,views,forms,urls

class QuestionViewTests(TestCase):
	# a following sample IS TO BE FOLLOWED STRICTLY:
	# 					#####						
	#def test_<some verbose name> (self):
	#''' COMPONENTS: <name of components being tested>
	#	 ABOUT: <a broad explanation of the test's purpose>
	#	 EXPECTED: <an expected result>
	#'''
	#	<code>
	# 					#####						
	# The following example should be self-explanatory:
    def test_try_to_ping(self):
        """ COMPONENT: app:*
        	ABOUT: Tries to ping up the server.
        	EXPECTED: A '200 OK' response should be received from the server
        """
        self.assertEqual(self.client.get(reverse('app:index')).status_code,    200)
