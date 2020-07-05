from django.shortcuts import render, redirect
from django.views import View
from django.contrib import auth
from training_class.models import Client, Teacher, Student, MyTask, MyDecision, GroupTeacher,  GroupStudent, ListGroup
from django.core.exceptions import ObjectDoesNotExist


def this_groups(request):
    status = status_determination(request)
    if status == 'student':
        groups = GroupStudent.objects.filter(student_id=Student.objects.get(client_id=this_client_id(request)).id)
    elif status == 'teacher':
        groups = GroupTeacher.objects.filter(teacher_id=Teacher.objects.get(client_id=this_client_id(request)).id)
    else:
        groups = ""
    return groups


def status_determination(request):
    context = ""
    client_id = this_client_id(request)
    try:
        if Teacher.objects.get(client_id=client_id):
            context = 'teacher'
    except ObjectDoesNotExist:
        pass
    try:
        if Student.objects.get(client_id=client_id):
            context = 'student'
    except ObjectDoesNotExist:
        pass
    return context


def this_client_id(request):
    client_id = Client.objects.get(user_id=auth.get_user(request).id).id
    return client_id


class TrainingClass(View):
    def get(self, request):
        context = {}
        context['username'] = auth.get_user(request).username
        context['status'] = status_determination(request)
        context['groups'] = this_groups(request)
        return render(request, 'training_class/trainingClass.html', context)


class TeacherTask(View):
    def get(self, request, group):
        context = {}
        context['status'] = status_determination(request)
        if context['status']=='teacher':
            context['username'] = auth.get_user(request).username
            context['tasks'] = MyTask.objects.filter(group_id=ListGroup.objects.get(groupName=group).id)
            context['group'] = group
            return render(request, 'training_class/task.html', context)
        else:
            return redirect('/education/')


class TeacherTaskAdd(View):
    def get(self, request, group):
        context = {}
        context['status'] = status_determination(request)
        if context['status'] == 'teacher':
            context['username'] = auth.get_user(request).username
            context['group'] = group
            return render(request, 'training_class/taskAdd.html', context)
        else:
            return redirect('/education/')

    def post(self, request, group):
        context = {}
        context['username'] = auth.get_user(request).username
        context['status'] = status_determination(request)
        task = MyTask(
            group=ListGroup.objects.get(groupName=group),
            teacher=Teacher.objects.get(client_id=this_client_id(request)),
            text=request.POST['text']
        )
        task.save()
        return redirect('/education/%s/task'%group)


class TeacherTaskEdit(View):
    def get(self, request, id, group):
        context = {}
        context['status'] = status_determination(request)
        if context['status'] == 'teacher':
            context['username'] = auth.get_user(request).username
            context['this_group'] = ListGroup.objects.get(groupName=group)
            context['other_groups'] = this_groups(request).filter().exclude(group_id=ListGroup.objects.get(groupName=group))
            context['group'] = group
            context['text'] = MyTask.objects.get(id=id)
            return render(request, 'training_class/taskEdit.html', context)
        else:
            return redirect('/education/')

    def post(self, request, id, group):
        context = {}
        context['username'] = auth.get_user(request).username
        task = MyTask.objects.get(id=id)
        task.group = ListGroup.objects.get(groupName=request.POST['group'])
        task.text = request.POST['text']
        task.save()
        return redirect('/education/%s/task'%group)


class TeacherTaskDelete(View):
    def get(self, request, id, group):
        MyTask.objects.filter(id=id).delete()
        return redirect('/education/%s/task'%group)


class TeacherTaskDecision(View):
    def get(self, request, id, group):
        context = {}
        context['status'] = status_determination(request)
        if context['status'] == 'teacher':
            context['group'] = group
            context['username'] = auth.get_user(request).username
            context['task_id'] = id
            context['decisions'] = MyDecision.objects.filter(task_id=id)
            return render(request, 'training_class/taskDecision.html', context)
        else:
            return redirect('/education/')


class TeacherTaskDecisionEdit(View):
    def get(self, request, id, group, id_dec):
        context = {}
        context['status'] = status_determination(request)
        if context['status'] == 'teacher':
            context['group'] = group
            context['username'] = auth.get_user(request).username
            context['task_id'] = id
            context['decision'] = MyDecision.objects.get(id=id_dec)
            return render(request, 'training_class/taskDecisionEdit.html', context)
        else:
            return redirect('/education/')

    def post(self, request, id, group, id_dec):
        context = {}
        context['username'] = auth.get_user(request).username
        decision = MyDecision.objects.get(id=id_dec)
        decision.text = request.POST['text']
        decision.save()
        return redirect('/education/%s/task/%s/decision'%(group, id))


class Decision(View):
    def get(self, request, group):
        context = {}
        context['status'] = status_determination(request)
        if context['status'] == 'student':
            context['group'] = group
            context['username'] = auth.get_user(request).username
            context['tasks'] = MyTask.objects.filter(group_id=ListGroup.objects.get(groupName=group).id)
            return render(request, 'training_class/decision.html', context)
        else:
            return redirect('/education/')


class DecisionAdd(View):
    def get(self, request, group, id):
        context = {}
        context['status'] = status_determination(request)
        if context['status'] == 'student':
            context['group'] = group
            context['username'] = auth.get_user(request).username
            return render(request, 'training_class/decisionAdd.html', context)
        else:
            return redirect('/education/')

    def post(self, request, group, id):
        context = {}
        context['status'] = status_determination(request)
        context['username'] = auth.get_user(request).username
        decision = MyDecision(
            task=MyTask.objects.get(id=id),
            student=Student.objects.get(client_id=this_client_id(request)),
            text=request.POST['text'],
            file=request.FILES.get('file', None)
        )
        decision.save()
        return redirect('/education/%s/decision'%group)


class DecisionList(View):
    def get(self, request, id, group):
        context = {}
        context['status'] = status_determination(request)
        if context['status'] == 'student':
            context['group'] = group
            context['username'] = auth.get_user(request).username
            context['decisions'] = MyDecision.objects.filter(task_id=id, student_id=Student.objects.get(client_id=this_client_id(request)))
            return render(request, 'training_class/DecisionList.html', context)
        else:
            return redirect('/education/')






