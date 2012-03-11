from core.models import *
from core.forms import *

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail, send_mass_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from django.http import HttpResponse

from recaptcha.client import captcha
import socket

def blog(request):
    tag = request.GET.get('tag')
    if tag:
        entry_list = Entry.objects.filter(published=True, tags__name=tag).extra(select={'ccount':'SELECT COUNT(*) FROM core_comment WHERE core_entry.id = core_comment.entry_id AND core_comment.spam = FALSE AND core_comment.deleted = FALSE'})
        if len(entry_list) > 0:
            messages.success(request, 'Here are all articles tagged ' + tag)
        else:
            messages.success(request, 'Sorry there are currently no articles tagged ' + tag)
    else:
        entry_list = Entry.objects.filter(published=True).extra(select={'ccount':'SELECT COUNT(*) FROM core_comment WHERE core_entry.id = core_comment.entry_id AND core_comment.spam = FALSE AND core_comment.deleted = FALSE'})
    
    paginator = Paginator(entry_list, 2)
    
    page = request.GET.get('page')
    try:
        entries = paginator.page(page)
    except PageNotAnInteger:
        entries = paginator.page(1)
    except EmptyPage:
        entries = paginator.page(paginator.num_pages)

    return render(request, 'core/blog.html', locals())

def entry(request, slug=None):
    entry = get_object_or_404(Entry, slug=slug, published=True)
    form = CommentForm(request.POST or None)
    #Initializing this so I can figure out later in the form if I want to generate a form with or without captcha error
    pass_captcha = True
    if request.method == 'POST':
        
        if request.user.is_anonymous() and settings.RECAPTCHA_ENABLED:
            check_captcha = captcha.submit(request.POST['recaptcha_challenge_field'], request.POST['recaptcha_response_field'], settings.RECAPTCHA_PRIVATE_KEY, request.META['REMOTE_ADDR'])
            if check_captcha.is_valid == False:
                pass_captcha = False
                html_captcha = captcha.displayhtml(settings.RECAPTCHA_PUBLIC_KEY, error=check_captcha.error_code)
        if form.is_valid() and pass_captcha:
            form2 = form.save(commit=False)
            if form2.name == '':
                form2.name = 'Anonymous'
            if form['ancestor'].value() == '':
                form2.user = request.user if request.user.is_authenticated() else None
                form2.path = []
                form2.entry = entry
            else:
                try:
                    parent = Comment.objects.get(id=int(form['ancestor'].value()))
                    form2.parent = parent
                    form2.user = request.user if request.user.is_authenticated() else None
                    form2.depth = parent.depth + 1
                    temp_path = parent.path
                    temp_path.append(parent.id)
                    form2.path = temp_path
                    form2.entry = entry
                    form2.save()
                    temp_path.append(form2.id)
                    form2.path = temp_path
                except:
                    messages.error(request, 'The comment you are replying to does not exist.')
            
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')

            if settings.HTTPBL_KEY and settings.HTTPBL_ADDRESS:
                try:
                    iplist = ip.split('.')
                    iplist.reverse()
                    
                    query = settings.HTTPBL_KEY + '.' + '.'.join(iplist) + '.' + settings.HTTPBL_ADDRESS

                    httpbl_result = socket.gethostbyname(query)
                    httpbl_resultlist = httpbl_result.split('.')
                    
                    #Check if response is proper
                    if httpbl_resultlist[0] == "127":
                        #DO SOME MORE CHECKING OF ALL THE VALUES RETURNED
                        if httpbl_resultlist[2] > settings.HTTPBL_TL:
                            form2.spam = True
                        else:
                            form2.spam = False
                    else:
                        form2.spam = True
                except:
                    form2.spam = False
            else:
                form2.spam = True
            form2.save()
            messages.success(request, 'Thanks for commenting!')
            return redirect('core.views.entry', slug=slug)
        else:
            messages.error(request, 'There was a problem submitting your comment. Please try agian.')
            
    #Users don't need to pass a captcha and checking that this is the initial value so there will be no error codes
    if request.user.is_anonymous() and pass_captcha and settings.RECAPTCHA_ENABLED:
        html_captcha = captcha.displayhtml(settings.RECAPTCHA_PUBLIC_KEY)
    comments = Comment.objects.select_related('user').filter(entry=entry.id, deleted=False).order_by('path')
    comment_tree = []
    com_counter = len(comments) #total number of comments
    counter = 0 #total number of parent comments
    for i in range(com_counter):
        if comments[i].path == []:
            comment_tree.append([comments[i]])
            counter += 1
        else:
            break
    
    #Code in for loop could be more efficient but is fine for now
    comments = comments[counter::]
    if comments:
        for parent in xrange(0, counter):
            commentid = comment_tree[parent][0].id
            comment_tree[parent].extend([item for item in comments if item.path[0] == commentid])    
    
    return render(request, 'core/entry.html', locals())
    
'''Implement in python for comments Line 371: https://github.com/EllisLab/CodeIgniter/blob/develop/system/helpers/url_helper.php

Or consider moving to textile https://docs.djangoproject.com/en/dev/ref/contrib/markup/'''

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            send_mail('Blog Contact Form', form['message'].value(), form['email'].value(), ['joesmoe@teamtol.com', form['email'].value()] if form['cc_myself'].value() else ['joesmoe@teamtol.com'], fail_silently=False)
            messages.success(request, 'Message sent successfully!')
            return redirect('core.views.contact')
    else:
        form = ContactForm() 

    return render(request, 'core/contact.html', locals())

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
            from_email = 'mburst91@gmail.com'
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