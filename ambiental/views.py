from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from ambiental.forms import RatingElementForm, ProjectForm, UserProfileForm, LoginForm
from .models import RatingElement, CD, Project, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.generic.base import ContextMixin

A = [
    'Cost Estimate',
    'Cost Risk/Contingency Analysis',
    'Funding Requirements/Profile',
    'Independent Cost Estimate/Schedule Review',
    'Life Cycle Cost',
    'Forecast of Cost at Completion',
    'Cost Estimate for Next Phase Work Scope']
B = [
    'Project Schedule',
    'Major Milestones',
    'Resource Loading',
    'Critical Path Management',
    'Schedule Risk/Contingency Analysis',
    'Forecast of Schedule Completion',
    'Schedule for Next Phase Work Scope'] # 'B' Schedule Rating Element Options
C = [
    'Systems Engineering',
    'Alternatives Analysis',
    'Functional & Performance Requirements (What)',
    'Site Location',
    'Design Basis (How)',
    'Design Criteria (How To)',
    'Technology Needs Identifies',
    'Technology Needs Demonstrated',
    'Trade-Off/Optimization Studies',
    'Plot Plan',
    'Process Flow Diagrams (PDFs)',
    'Layout Drawings and Equipment List',
    'Piping & Instrumentation Diagrams (P&ID)',
    'Site Characterization (Including Surveys and Soil Tests)',
    'Waste Characterization/Assess Current Situation',
    'Waste Acceptance Criteria (WAC) and Waste Packaging',
    'Hazard Analysis',
    'Hazard Classification',
    'Safety Documentation',
    'Safeguards & Security',
    'ES&H Management Planning (including ISMS)',
    'Emergency Preparedness',
    'NEPA Documentation',
    'Civil, Structural and Architectural',
    'Mechanical (PipIng)',
    'Instrumental & Electrical',
    'Long Lead/Critical Equipment & Materials List',
    'Desing Completion',
    'Design Reviews for Current Phase',
    'Interface Planning and Control',
    'Operating, Maintenance, and Reliability Concepts',
    'Reliability, Availability and Maintainability (RAM) Analysis',
    'Transition and Startup Planning',
    'Pollution Prevention and Waste Minimization',
    'Transportation Requirements',
    'Loading/Unloading/Storage FAcility Requirements',
    'Training Requirements',
    'Processing/Production Plan/Schedule',
    'Operations Plans and Procedures']
D = [
    'Mission Need Statement',
    'Acquisition Strategy/Plan',
    'Conceptual Design Report (CDR)',
    'Project Charter',
    'Key Project Assumptions',
    'Project Execution Plan (PEP)',
    'Integrated Project Team/Project Organization',
    'Baseline Change Control',
    'Project Control',
    'Project Work Breakdown Strcture (WBS)',
    'Resources Required (People/Material) for Next Phase',
    'Project Risk Management Plan/Assessment',
    'Quality Assurance Program',
    'Configuration Management',
    'Value Engineering',
    'Procurement Packages',
    'Project Arquisition Process',
    'Funds Management',
    'Reviews/Assessments']
E = [
    'Integrated Regulatory Oversight Program',
    'Inter-Site Issues',
    'On-Site Issues',
    'Permits, Licenses, and Regulatory Approvals',
    'StakeholderProgram']
TJ = {
    'A': 1,
    'B': 2,
    'C': 3,
    'D': 4,
    'E': 5,}
T = {
    '1': 'A',
    '2': 'B',
    '3': 'C',
    '4': 'D',
    '5': 'E',}
TA ={
    '1': 10,
    '2': 10,
    '3': 200,
    '4': 60,
    '5': 20,}
TB = {
    '1': 70,
    '2': 70,
    '3': 320,
    '4': 120,
    '5': 20}
TC = {
    '1': 130,
    '2': 130,
    '3': 380,
    '4': 180,
    '5': 80}
TD = {
    '1': 150,
    '2': 150,
    '3': 400,
    '4': 200,
    '5': 100}


class FormBase(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('login')
    redirect_field_name = 'redirect_to'
    template_name = 'ambiental/index.html'
    form_class = RatingElementForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = {}
        print self.request.user
        context['projects'] = Project.objects.filter(creator=self.request.user.userprofile)


        return context



class CreateProject(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('login')
    redirect_field_name = 'redirect_to'
    template_name = 'ambiental/create_project.html'
    form_class = ProjectForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):

        project = Project.objects.create(creator=self.request.user.userprofile, name=form.cleaned_data['name'], description=form.cleaned_data['description'])

        for j in range(4):
            cd = CD.objects.create(project=project, name='CD-{0}'.format(j))
            for i in range(39):
                if i < 7:
                    RatingElement.objects.create(cd=cd, group='COST',index='A{0}'.format(i+1), name=A[i])
                    RatingElement.objects.create(cd=cd, group='SCHEDULE', index='B{0}'.format(i+1), name=B[i])
                    if i < 5:
                        RatingElement.objects.create(cd=cd, group='EXTERNAL FACTORS', index='E{0}'.format(i+1), name=E[i])
                if i < 19:
                    RatingElement.objects.create(cd=cd, group='MANAGEMENT PLANNING AND CONTROL', index='D{0}'.format(i+1), name=D[i])
                RatingElement.objects.create(cd=cd, group='SCOPE/TECHNICAL', index='C{0}'.format(i+1), name=C[i])

        return super(CreateProject, self).form_valid(form)

@login_required(login_url=reverse_lazy('login'))
def search(request):
    login_url = reverse_lazy('login')
    redirect_field_name = 'redirect_to'
    result = None
    if request.method == 'POST':
        query = request.POST['query']
        if request.user.username == 'admin':
            project = Project.objects.filter()
        elif query:
            project = Project.objects.filter(creator=request.user.userprofile, name__icontains=query)
            if project:
                result = project

    return render(request, 'ambiental/search.html', {'result': result})


class ProjectDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    redirect_field_name = 'redirect_to'
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        cd = CD.objects.filter(project_id=context['object'].id)
        context['cd'] = cd
        index = ['a', 'b', 'c', 'd']
        i = 0
        total = 0.00
        for critical in context['cd']:
            if critical.name == 'CD-0' and critical.total_score >= 240:
                total = total + 25
            if critical.name == 'CD-1' and critical.total_score >= 480:
                total = total + 25
            if critical.name == 'CD-2' and critical.total_score >= 720:
                total = total + 25
            if critical.name == 'CD-3' and critical.total_score >= 800:
                total = total + 25
            context[index[i]] = critical.total_score
            i = i + 1

        context['progress'] = total
        context['missing'] = 100 - total
        return context


class CdDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    redirect_field_name = 'redirect_to'
    model = CD
    template_name = 'ambiental/cd_detail.html'

    def get_context_data(self, **kwargs):
        context = {}
        global T, TA, TB, TC ,TD
        total = 0
        context['cd'] = super(CdDetailView, self).get_context_data(**kwargs)
        context['project'] = Project.objects.get(id=context['cd']['object'].project.id)
        print T[self.kwargs['type']]
        context['re'] = RatingElement.objects.filter(cd_id=context['cd']['object'].id, index__icontains=T[self.kwargs['type']])
        for score in context['re']:
            total = total + score.score
        context['highScore'] = total
        if context['cd']['object'].name == 'CD-0':
            context['limit'] = TA[self.kwargs['type']]
        elif context['cd']['object'].name == 'CD-1':
            context['limit'] = TB[self.kwargs['type']]
        elif context['cd']['object'].name == 'CD-2':
            context['limit'] = TC[self.kwargs['type']]
        else:
            context['limit'] = TD[self.kwargs['type']]
        print context['limit']

        if self.kwargs['type'] == '1':
            context['cd']['object'].score_a = total
            context['cd']['object'].save()
        elif self.kwargs['type'] == '2':
            context['cd']['object'].score_b = total
            context['cd']['object'].save()
        elif self.kwargs['type'] == '3':
            context['cd']['object'].score_c = total
            context['cd']['object'].save()
        elif self.kwargs['type'] == '4':
            context['cd']['object'].score_d = total
            context['cd']['object'].save()
        else:
            context['cd']['object'].score_e = total
            context['cd']['object'].save()
        print context['cd']['object'].total_score
        return context

class RatingElementView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('login')
    redirect_field_name = 'redirect_to'
    form_class = RatingElementForm
    template_name = 'ambiental/rating_element_detail.html'

    def get_context_data(self, **kwargs):
        global TJ
        context = super(RatingElementView, self).get_context_data(**kwargs)
        project = Project.objects.get(slug=self.kwargs['slug'])
        cd = CD.objects.get(id=self.kwargs['pk'])
        re = RatingElement.objects.get(id=self.kwargs['re_pk'])
        context['slug'] = project.slug
        context['pk'] = cd.pk
        print TJ[re.index[0]]
        context['type'] = TJ[re.index[0]]
        return context

    def get_success_url(self, **kwargs):
        global TJ
        re = RatingElement.objects.get(id=self.kwargs['re_pk'])
        return reverse_lazy('cd', kwargs={'slug': self.kwargs['slug'], 'pk': self.kwargs['pk'],'type': TJ[re.index[0]]})

    def get_initial(self):
        re = RatingElement.objects.get(id=self.kwargs['re_pk'])
        fields = {
            'index': re.index,
            'name': re.name,
            'wd': re.wd,
            'wf': re.wf,
            'mv': re.mv,
            'score': re.score,
            'comment': re.comment
        }
        return fields

    def form_valid(self, form):
        re = RatingElement.objects.get(id=self.kwargs['re_pk'])
        print re
        re.wd = form.cleaned_data['wd']
        re.wf = form.cleaned_data['wf']
        re.mv = form.cleaned_data['mv']
        re.score = form.cleaned_data['score']
        re.comment = form.cleaned_data['comment']
        re.save()
        return super(RatingElementView, self).form_valid(form)

class CdReportDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    redirect_field_name = 'redirect_to'
    model = CD
    template_name = 'ambiental/cd_report_detail.html'

    def get_context_data(self, **kwargs):
        context = {}
        total = 0
        context['cd'] = super(CdReportDetailView, self).get_context_data(**kwargs)
        context['project'] = Project.objects.get(id=context['cd']['object'].project.id)
        context['rea'] = RatingElement.objects.filter(cd_id=context['cd']['object'].id, group='COST')
        context['reb'] = RatingElement.objects.filter(cd_id=context['cd']['object'].id, group='SCHEDULE')
        context['rec'] = RatingElement.objects.filter(cd_id=context['cd']['object'].id, group='SCOPE/TECHNICAL')
        context['red'] = RatingElement.objects.filter(cd_id=context['cd']['object'].id, group='MANAGEMENT PLANNING AND CONTROL')
        context['ree'] = RatingElement.objects.filter(cd_id=context['cd']['object'].id, group='EXTERNAL FACTORS')
        return context

class RegistrationView(FormView):
    form_class = UserProfileForm
    template_name = 'ambiental/registration.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user, createu = User.objects.get_or_create(username=form.cleaned_data['username'])
        if user:
            profile, create = UserProfile.objects.get_or_create(user=user)
            print create
            user.set_password(form.cleaned_data['password'])
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            profile.company = form.cleaned_data['company']
            profile.save()
            return super(RegistrationView, self).form_valid(form)
        else:
            return HttpResponseRedirect(reverse_lazy('registration'))

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'ambiental/login.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        print username
        print password
        user = authenticate(username=username, password=password)
        print user
        print reverse_lazy('login') + 'failed=True'
        if user:
            if user.is_active:
                login(self.request, user)
                return super(LoginView, self).form_valid(form)
        else:
            return HttpResponseRedirect(reverse_lazy('login') + 'failed')

    def get_context_data(self, **kwargs):
        logout(self.request)
        context = {}
        context = super(LoginView, self).get_context_data(**kwargs)
        if self.kwargs:
            context['failed'] = self.kwargs['failed']
        return context
