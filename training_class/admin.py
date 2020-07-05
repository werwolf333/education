from django.contrib import admin
from .models import Client, Teacher, Student,GroupTeacher, GroupStudent, ListGroup,  MyTask, MyDecision


class ClientAdmin(admin.ModelAdmin):
    fields = []


admin.site.register(Client,  ClientAdmin)
admin.site.register(Teacher,  ClientAdmin)
admin.site.register(Student, ClientAdmin)
admin.site.register(GroupStudent, ClientAdmin)
admin.site.register(GroupTeacher, ClientAdmin)
admin.site.register(ListGroup, ClientAdmin)
admin.site.register(MyTask, ClientAdmin)
admin.site.register(MyDecision, ClientAdmin)
