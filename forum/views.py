from django.shortcuts import render
from django.views.generic.base import TemplateResponseMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, View
from django.views.generic.edit import FormMixin
from .models import CityProblem, SolutionProposal, Vote, Category, Poll, Answer
from .forms import SolutionProposalForm, VoteForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.views.generic import ListView


from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegistrationForm

from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('forum:forum_list')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

class ForumListView(TemplateResponseMixin, View):
    template_name = 'forum.html'

    def get(self, request, *args, **kwargs):
        category_id = self.kwargs.get('category_id', None)
        сategories = Category.objects.all()
        polls = Poll.objects.all()
        if category_id:
            problems = CityProblem.objects.filter(category=category_id)
            return self.render_to_response({'problems': problems, 'сategories': сategories, 'polls': polls})
        problems = CityProblem.objects.all()
        return self.render_to_response({'problems': problems, 'сategories': сategories, 'polls': polls})

    def post(self, request, *args, **kwargs):
        answer_id = request.POST.get('answer')
        if answer_id:
            answer = Answer.objects.get(id=answer_id)
            answer.votes += 1
            answer.save()
        return redirect('forum:forum_list')

from .forms import DonationForm
class CityProblemDetailView(LoginRequiredMixin, DetailView, FormMixin):
    model = CityProblem
    template_name = 'forum_detail.html'
    form_class = SolutionProposalForm
    context_object_name = 'problem'

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['solution_form'] = self.get_form()
        context['vote_form'] = VoteForm()
        context['donation_form'] = DonationForm()
        problem_id = self.kwargs.get('pk')
        problem = get_object_or_404(CityProblem, pk=problem_id)
        solutions = problem.solutions.annotate(total_votes=Sum('vote_set__value'))
        context['solutions'] = solutions
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'submit_solution' in request.POST:
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
        elif 'vote' in request.POST:
            return self.vote(request)
        elif 'submit_donation' in request.POST:
            donation_form = DonationForm(request.POST)
            if donation_form.is_valid():
                return self.donation_form_valid(donation_form)
        return self.form_invalid(form)

    def form_valid(self, form):
        solution = form.save(commit=False)
        solution.problem = self.object
        solution.author = self.request.user
        solution.save()
        return super().form_valid(form)

    def vote(self, request):
        solution_id = request.POST.get('solution_id')
        solution = get_object_or_404(SolutionProposal, id=solution_id)
        vote_type = request.POST.get('vote', 'up')
        existing_vote = Vote.objects.filter(voter=request.user, solution=solution)

        if existing_vote.exists():
            existing_vote = existing_vote.first()
            if vote_type == 'up' and existing_vote.value == -1 or vote_type == 'down' and existing_vote.value == 1:
                existing_vote.value *= -1
                existing_vote.save()
            else:
                existing_vote.delete()
        else:
            Vote.objects.create(solution=solution, voter=request.user, value=1 if vote_type == 'up' else -1)

        return redirect(self.get_success_url())

    def donation_form_valid(self, form):
        donation = form.save(commit=False)
        donation.city_problem = self.object
        donation.save()
        return redirect(self.get_success_url())


class CityProblemListView(ListView):
    model = CityProblem
    template_name = 'cityproblem_list.html'
    context_object_name = 'problems'

    def get_queryset(self):
        return CityProblem.objects.filter(author=self.request.user).order_by('-created_at')

from .forms import CityProblemForm

class CityProblemCreateView(LoginRequiredMixin, CreateView):
    model = CityProblem
    form_class = CityProblemForm
    template_name = 'cityproblem_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('forum:city_problem_detail', kwargs={'pk': self.object.pk})

class CityProblemUpdateView(LoginRequiredMixin, UpdateView):
    model = CityProblem
    form_class = CityProblemForm
    template_name = 'cityproblem_form.html'

    def get_queryset(self):
        return CityProblem.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('forum:city_problem_detail', kwargs={'pk': self.object.pk})


class CityProblemDeleteView(LoginRequiredMixin, DeleteView):
    model = CityProblem
    template_name = 'cityproblem_confirm_delete.html'

    def get_queryset(self):
        return CityProblem.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('forum:cityproblem_list')



