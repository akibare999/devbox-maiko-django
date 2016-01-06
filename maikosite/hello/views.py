from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import View, FormView, TemplateView
from django.views.decorators.cache import cache_control

import logging
import datetime

_LOGGER = logging.getLogger(__name__)

# Create your views here.

class HelloBaseView(View):
    '''
    Generic view class for all of our views to inherit from.
    Can override "dispatch" in here to do some logging or whatever.

    Can put the "am I allowed to be here" redirect stuff, also mucking
    with back links, etc, in the overridden dispatch routine.
    '''

    def dispatch(self, *args, **kwargs):
        '''
        Add pre-code that happens on every access to the view.
        We'll just write a log message.
        '''
        login = self.request.session.get('login','UNKNOWN USER')
        viewname = self.__class__.__name__
        namespace = self.request.resolver_match.namespace
        current_url = self.request.resolver_match.url_name
        _LOGGER.debug("User %s visited view %s (URL %s:%s) at %s)" % (login,
                      viewname,
                      namespace,
                      current_url,
                      datetime.datetime.now()))

        # Continue to dispatch from the parent
        return super(HelloBaseView, self).dispatch(*args, **kwargs)

class HelloView(TemplateView):
    template_name = 'hello/index.html'

class ClearView(HelloBaseView):
    @cache_control(no_cache=True, no_store=True)
    def dispatch(self, request, *args, **kwargs):
        super(ClearView, self).dispatch(request, *args, **kwargs)
        request.session.flush()
        return HttpResponseRedirect(reverse('hello:hello')) #FIXME


class LogoutView(View):
    @cache_control(no_cache=True, no_store=True)
    def dispatch(self, request, *args, **kwargs):
        super(LogoutView, self).dispatch(request, *args, **kwargs)

        # Clear the local session
        request.session.flush()

        # Logout from the Shibboleth IDP (clear remote cookies)
        # via standard redirect to /Shibboleth.sso/Logout
        return redirect('/Shibboleth.sso/Logout')

