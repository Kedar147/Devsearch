import imp
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Projects,Tags
from .forms import projectForms,ReviewForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .utils import searchProjects, paginateProjects

def projects(request):
    projects, search_query = searchProjects(request)
    projectLists=Projects.objects.all()
    custom_range, projects = paginateProjects(request, projects, 6)
    context = {'projects': projects,
               'search_query': search_query, 'custom_range': custom_range}
    return render(request,'projects/projects.html',context)

def project(request, kd):
    Obj=Projects.objects.get(id=kd)
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.projects = Obj
        review.owner = request.user.profile
        
        review.save()

        Obj.getVoteCount

        messages.success(request, 'Your review was successfully submitted!')
        return redirect('project', kd=Obj.id)
            
        
    return render(request,'projects/single-project.html',{'project':Obj,'form': form})        

@login_required(login_url="login")
def projectforms(request):
    profile = request.user.profile
    form=projectForms()
    if request.method=='POST':
        newtags = request.POST.get('newtags').replace(',',  " ").split()
        form=projectForms(request.POST,request.FILES)

        if form.is_valid:
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            for tag in newtags:
                tag, created = Tags.objects.get_or_create(name=tag)
                project.Tags.add(tag)
            return redirect('account')

    context={'form':form}
    return render(request,'projects/project-forms.html',context)

@login_required(login_url="login")
def updateforms(request,pk):
    profile = request.user.profile
    project=profile.projects_set.get(id=pk)
    form=projectForms(instance=project)
    if request.method=='POST':
        newtags = request.POST.get('newtags').replace(',',  " ").split()
        form=projectForms(request.POST,request.FILES,instance=project)
        if form.is_valid:
            form.save()
            for tag in newtags:
                tag, created = Tags.objects.get_or_create(name=tag)
                project.Tags.add(tag)
            return redirect('account')

    context={'form':form}
    return render(request,'projects/project-forms.html',context)

@login_required(login_url="login")
def deleteForms(request,pk):
    profile = request.user.profile
    project=profile.projects_set.get(id=pk)
    if request.method=='POST':
        project.delete()
        return redirect('projectss')
    context={'object':project}
    return render(request,'projects/deleteproject.html',context)