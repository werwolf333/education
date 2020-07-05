from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Client(models.Model):
    user = models.OneToOneField(User, related_name='users', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Teacher(models.Model):
    client = models.OneToOneField(Client, related_name='teacher', on_delete=models.CASCADE)
    teacherName = models.CharField(max_length=200, verbose_name="teacherName")

    def __str__(self):
        return self.teacherName


class Student(models.Model):
    client = models.OneToOneField(Client, related_name='student', on_delete=models.CASCADE)
    studentName = models.CharField(max_length=200, verbose_name="studentName")

    def __str__(self):
        return self.studentName


class ListGroup(models.Model):
    groupName = models.CharField(max_length=200, verbose_name="groupName")

    def __str__(self):
        return self.groupName


class GroupStudent(models.Model):
    group = models.ForeignKey(ListGroup, related_name='GroupStudent', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='GroupStudent', on_delete=models.CASCADE)

    def __str__(self):
        return self.student.studentName


class GroupTeacher(models.Model):
    group = models.ForeignKey(ListGroup, related_name='GroupTeacher', on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, related_name='GroupTeacher', on_delete=models.CASCADE)

    def __str__(self):
        return self.teacher.teacherName + ' ' +self.group.groupName + ' ' +self.teacher.client.user.username


class MyTask(models.Model):
    group = models.ForeignKey(ListGroup, related_name='task', on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey(Teacher, related_name='task', on_delete=models.DO_NOTHING)
    text = models.TextField(verbose_name="текст")

    def __str__(self):
        return self.text


class MyDecision(models.Model):
    task = models.ForeignKey(MyTask, related_name='decision', on_delete=models.DO_NOTHING)
    student = models.ForeignKey(Student, related_name='decision', on_delete=models.DO_NOTHING)
    text = models.TextField(verbose_name="текст")
    file = models.FileField(blank=True,  upload_to='uploads/')
    def __str__(self):
        return self.text

