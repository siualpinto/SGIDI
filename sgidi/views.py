
from django.views import generic
# Create your views here.


class IndexView(generic.ListView):
    template_name = "sgidi/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return