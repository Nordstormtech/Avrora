from django.shortcuts import render
from .models import People
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from static.bitrix import B24 as bitrix
clas = bitrix()

def index(request):
    return HttpResponse('Главная страница')


def avrora(request, pk, vv):
    alfa = (clas.bitrix_check_task(pk))['tasks']

    a = len(alfa)
    worker = []
    for i in People.objects.all():
        worker.append(i.name)
    names = []
    for i in alfa:
        if i['groupId'] == '0':
            group_name = ''
        else:
            try:
                group_name = (clas.sonet_group_get(i['groupId']))[0]['name']
            except:
                group_name = ''
        names.append(f"{group_name}.{i['title']}")

    context = {'numbers': range(a), 'names': names, 'worker': worker, 'vv': vv}
    return render(request, 'avrora_leave.html', context=context)


@csrf_exempt
def new_avrora(request):
    if 'people' in request.GET:
        message = 'Спасибо, ваш лист замещения отправлен на согласование'
        info = dict(request.GET)
        tasks = (info['id'])[0].split("'")
        a = ''
        people = ''
        i = 0
        while i < len(tasks):
            if tasks[i] == '[' or tasks[i] == ']' or tasks[i] == ', ':
                del tasks[i]
            else:
                i += 1
        for task in range(len(tasks)):
            b = f'\n {tasks[task]}: {(info["people"])[task]}'
            c = f'\n{(info["people"])[task]}'
            a = a+b
            people = people+c
        id_string = (info['vv'])[0]
        clas.bizproc_workflow_start(a, id_string)
    else:
        message = 'Вы не заполнили лист замещения'
    return HttpResponse(message)


def avrora_check(request):
    pass
