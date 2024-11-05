import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import KillStory

logger = logging.getLogger('aa_killstory')

@login_required
def index(request):
    logger.info('Killstory index view accessed by user %s', request.user)
    stories = KillStory.objects.all()
    return render(request, 'aa_killstory/index.html', {'stories': stories})
