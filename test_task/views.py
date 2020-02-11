from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from test_task import vk_api

vk = vk_api.VkAPI(redirect_uri='')  # https://vk.com/dev/authcode_flow_user?f=3.%20Получение%20code


def index(request):
    user = request.session.get('user_id', False)

    warnings = False
    msgs = messages.get_messages(request)
    for msg in msgs:
        if msg.level == 30:
            warnings = True

    if user:
        friends = vk.get_friends(user, request.session['access_token'])
        me = vk.get_me(request.session['access_token'])
        return render(request, 'test_task/friends.html', {'friends': friends, 'me': me})
    else:
        href = vk.get_auth_url(scope='friends')
        request.session.set_test_cookie()
        return render(request, 'test_task/index.html', {'href': href, 'warnings': warnings})


def auth(request):
    """Обработка ответа VK"""
    items_dict = vk.get_access_token(request.GET['code'])
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        for key in items_dict:
            request.session[key] = items_dict[key]

        messages.add_message(request, messages.SUCCESS, 'Успешная авторизация.')
        return HttpResponseRedirect(reverse('index_url'))
    else:
        messages.add_message(request, messages.WARNING, 'У Вас отключены cookies!')
        return HttpResponseRedirect(reverse('index_url'))


def logout(request):
    """Удаление сессии пользователя"""
    request.session.flush()

    messages.add_message(request, messages.SUCCESS, 'Вы вышли из аккаунта.')

    return HttpResponseRedirect(reverse('index_url'))
