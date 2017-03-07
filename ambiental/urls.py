from django.conf.urls import url
from django.views import generic
from .views import FinalReportDetailView, LoginView, RegistrationView, CdReportDetailView, RatingElementView, FormBase, CreateProject, search, ProjectDetailView, CdDetailView
urlpatterns = [
    url(r'^$', LoginView.as_view(), name='login'),
    url(r'^create/$', CreateProject.as_view(), name='create-project'),
    url(r'^search/$', search, name='search'),
    url(r'^registration/$', RegistrationView.as_view(), name='registration'),
    url(r'^index/$', FormBase.as_view(), name='index'),
    url(r'^login/(?P<failed>[a-z]+)$', LoginView.as_view(), name='login'),
    url(r'^project/(?P<slug>[-\w]+)/$', ProjectDetailView.as_view(), name='project'),
    url(r'^project/(?P<slug>[-\w]+)/(?P<pk>[0-9]+)/cd-(?P<type>[0-9])$', CdDetailView.as_view(), name='cd'),
    url(r'^project/(?P<slug>[-\w]+)/(?P<pk>[0-9]+)/cd-report$', CdReportDetailView.as_view(), name='cd-report'),
    url(r'^project/(?P<slug>[-\w]+)/final-report$', FinalReportDetailView.as_view(), name='final-report'),
    url(r'^project/(?P<slug>[-\w]+)/(?P<pk>[0-9]+)/(?P<re_pk>[0-9]+)/$', RatingElementView.as_view(), name='ratingElement')

]
