from django.contrib import admin
from .models import CityProblem, SolutionProposal, Vote, Finalist, Category, Donation

admin.site.register(Category)

class SolutionProposalInline(admin.TabularInline):
    model = SolutionProposal
    extra = 1  # Количество форм для добавления новых решений

class VoteInline(admin.TabularInline):
    model = Vote
    extra = 1

class FinalistInline(admin.TabularInline):
    model = Finalist
    extra = 1

class CityProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    inlines = [SolutionProposalInline]

class SolutionProposalAdmin(admin.ModelAdmin):
    list_display = ('description', 'problem', 'author', 'votes', 'created_at')
    search_fields = ('description', 'problem__title')
    inlines = [VoteInline, FinalistInline]

class VoteAdmin(admin.ModelAdmin):
    list_display = ('voter', 'solution', 'created_at')
    search_fields = ('voter__username', 'solution__description')

class FinalistAdmin(admin.ModelAdmin):
    list_display = ('solution', 'votes_in_final')
    search_fields = ('solution__description',)

admin.site.register(CityProblem, CityProblemAdmin)
admin.site.register(SolutionProposal, SolutionProposalAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Finalist, FinalistAdmin)

from .models import Poll, Answer

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('question',)
    inlines = [AnswerInline]

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer_text', 'votes', 'poll')
    list_filter = ('poll',)

admin.site.register(Donation)

