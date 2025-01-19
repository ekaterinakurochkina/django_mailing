from config.settings import CACHE_ENABLED
from mailing.models import MailingRecipient, Message, Sending, MailingAttempt
from django.core.cache import cache


def get_object_from_cache():
    """Функция низкоуровневого кеширования для списка рассылок"""
    if not CACHE_ENABLED:
        return Sending.objects.all() # проверяем, используется ли кеширование в проекте
    key = "sending_list"        # задаем ключ
    sendings = cache.get(key)   # обращаемся в кеш по этому ключу
    if sendings is not None:
        return sendings         # если кеш пуст
    sendings = Sending.objects.all()    # забираем список рассылок из БД
    cache.set(key, sendings)    # записываем этот список в кеш
    return sendings             # и выдаем пользователю