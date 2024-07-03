from django.contrib import admin
from .models import Question, Choice, Comment
#from django_comments.models import Comment

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2          # pari tyhjää valinta-riviä admin-käyttöön

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0          # kommentteja ei voi jättää adminin kautta, joten ei ekstrarivejä (pakko nollata, koska default näemmä on 3)

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline, CommentInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Comment)
