from django.shortcuts import render, Http404

from .models import Pun

def valentines(request):

    puns = Pun.objects.order_by('?')


    if puns:
        pun = puns[0]
    else:
        raise Http404

    context = {'pun': pun}

    return render(request, 'projects/valentines.html', context)