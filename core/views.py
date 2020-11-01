from core.models import *
from core.forms import *

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail, send_mass_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.http import HttpResponse

from functools import reduce

def blog(request):
    tag = request.GET.get('tag')
    query = request.GET.get('query')
    if tag:
        entry_list = Entry.objects.filter(published=True, tags__name=tag).prefetch_related('tags')
        messages.success(request, 'Here are all articles tagged ' + tag)
    elif query:        
        #Remove extra spacing
        tquery = set(" ".join(query.lower().split()).split(' '))
        simple = set(['a', 'about', 'above', 'across', 'after', 'afterwards', 'again', 'against', 'all', 'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'am', 'among', 'amongst', 'amoungst', 'amount', 'an', 'and', 'another', 'any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere', 'are', 'around', 'as', 'at', 'back', 'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been', 'before', 'beforehand', 'behind', 'being', 'below', 'beside', 'besides', 'between', 'beyond', 'bill', 'both', 'bottom', 'but', 'by', 'call', 'can', 'cannot', 'cant', 'co', 'computer', 'con', 'could', 'couldnt', 'cry', 'de', 'describe', 'detail', 'did', 'do', 'done', 'down', 'due', 'during', 'each', 'eg', 'eight', 'either', 'eleven', 'else', 'elsewhere', 'empty', 'enough', 'etc', 'even', 'ever', 'every', 'everyone', 'everything', 'everywhere', 'except', 'few', 'fifteen', 'fifty', 'fill', 'find', 'fire', 'first', 'five', 'for', 'former', 'formerly', 'forty', 'found', 'four', 'from', 'front', 'full', 'further', 'get', 'give', 'go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her', 'here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'however', 'hundred', 'i', 'ie', 'if', 'in', 'inc', 'indeed', 'interest', 'into', 'is', 'it', 'its', 'itself', 'keep', 'last', 'latter', 'latterly', 'least', 'less', 'ltd', 'made', 'many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine', 'more', 'moreover', 'most', 'mostly', 'move', 'much', 'must', 'my', 'myself', 'name', 'namely', 'neither', 'never', 'nevertheless', 'next', 'nine', 'no', 'nobody', 'none', 'noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of', 'off', 'often', 'on', 'once', 'one', 'only', 'onto', 'or', 'other', 'others', 'otherwise', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'part', 'per', 'perhaps', 'please', 'put', 'rather', 're', 's', 'same', 'see', 'seem', 'seemed', 'seeming', 'seems', 'serious', 'several', 'she', 'should', 'show', 'side', 'since', 'sincere', 'six', 'sixty', 'so', 'some', 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhere', 'still', 'such', 'system', 'take', 'ten', 'than', 'that', 'the', 'their', 'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby', 'therefore', 'therein', 'thereupon', 'these', 'they', 'thick', 'thin', 'third', 'this', 'those', 'though', 'three', 'three', 'through', 'throughout', 'thru', 'thus', 'to', 'together', 'too', 'top', 'toward', 'towards', 'twelve', 'twenty', 'two', 'un', 'under', 'until', 'up', 'upon', 'us', 'very', 'via', 'was', 'we', 'well', 'were', 'what', 'whatever', 'when', 'whence', 'whenever', 'where', 'whereafter', 'whereas', 'whereby', 'wherein', 'whereupon', 'wherever', 'whether', 'which', 'while', 'whither', 'who', 'whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with', 'within', 'without', 'would', 'yet', 'you', 'your', 'yours', 'yourself', 'yourselves'])
        
        #Filter out simple words to prevent too many matches
        tquery = tquery.difference(simple)
        
        if tquery:
            #Create a complex query that does a like for each word
            tquery = reduce(Q.__or__, [Q(content__icontains=word) for word in tquery])
            entry_list = Entry.objects.filter(tquery, published=True).prefetch_related('tags')
            
            messages.success(request, 'Your search for ' + query + ' returned the following results')
        else:
            entry_list = []
            messages.success(request, 'Try a more specific query')
    else:
        entry_list = Entry.objects.filter(published=True).prefetch_related('tags')
    
    paginator = Paginator(entry_list, 5)
    
    page = request.GET.get('page')
    try:
        entries = paginator.page(page)
    except PageNotAnInteger:
        entries = paginator.page(1)
    except EmptyPage:
        entries = paginator.page(paginator.num_pages)

    return render(request, 'core/blog.html', locals())

def entry(request, slug=None):
    entry = get_object_or_404(Entry, slug=slug)    
    return render(request, 'core/entry.html', locals())

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            send_mail('Blog Contact Form', form['message'].value() + ' ' + form['email'].value(), form['email'].value(), [settings.EMAIL_HOST_USER, form['email'].value()] if form['cc_myself'].value() else [settings.EMAIL_HOST_USER], fail_silently=False)
            messages.success(request, 'Message sent successfully!')
            return redirect('core.views.contact')
    else:
        form = ContactForm() 

    return render(request, 'core/contact.html', locals())

#May reenable later but for now going to just use the search feature
def subscribe(request):
    email = request.GET.get('email')
    Subscriber.objects.get_or_create(email=email)
    if request.is_ajax():
        return HttpResponse('Thank you for subscribing!')
    referer = request.META.get('HTTP_REFERER', None)
    messages.success(request, 'Thank you for subscribing!')
    if referer:
        return redirect(referer)
    return redirect('core.views.blog')
    
def unsubscribe(request):
    email = request.GET.get('email')
    uuid = request.GET.get('key')
    if email and uuid:
        address = get_object_or_404(Subscriber, email=email, uuid=uuid)
        address.delete()
        messages.success(request, 'You have successfully been removed from my subscription list.')
    else:
        messages.error(request, 'Please click the unsubscribe link directly from your email.')
    return redirect('core.views.blog')

@user_passes_test(lambda u: u.is_superuser)    
def alert_the_press(request):
    '''List of entries that show if they've been posted to subscribers, facebook, and twitter. Allows me to send custom message to each service with a link to the entry'''
    if request.method == 'POST':
        form = Alert(request.POST)
        if form.is_valid():
            subject = form['subject'].value()
            message = form['message'].value()
            from_email = settings.EMAIL_HOST_USER
            if form['email'].value():
                subs = []
                for person in Subscriber.objects.all().values_list('email', flat=True):
                    subs.append((subject, message, from_email, [person]))
                send_mass_mail(subs)
                messages.success(request, 'Email successfully sent to all subscribers')
    else:
        form = Alert()
        FB_API_KEY = settings.FB_API_KEY
    return render(request, 'core/alert.html', locals())