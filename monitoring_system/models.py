from django.db import models


class User(models.Model):
    """Пользователи с уровнями доступов"""
    first_name = models.CharField(max_length=255, verbose_name="Имя")
    second_name = models.CharField(max_length=255, verbose_name="Фамилия")
    path_photo = models.ImageField(upload_to='static/photo', verbose_name="Загруженное фото") # Спросить на счет автокропа

    def __str__(self):
        return f'{self.first_name} {self.second_name} photo: {self.path_photo}'

    class Meta:
        verbose_name = "Работники"
        db_table = "Работники"


class Journal(models.Model):
    """Журнал учитывающий срабатывание системы на вход и на выход"""
    status = models.BooleanField(verbose_name="Статус")
    userid = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name="ID пользователя")
    status_recoding_time = models.DateTimeField(auto_now_add=True, verbose_name="Дата внесения в журнал")
    path_on_video = models.ImageField(upload_to="static/video", blank=True, verbose_name="Ссылка на видео")

    def __str__(self):
        return f'{self.userid.first_name} {self.userid.second_name} ' \
               f'Время {self.status_recoding_time.strftime("%d-%m-%Y %H:%M:%S")}Статус: {self.status}'

    class Meta:
        db_table = "Журнал времени"
        verbose_name = "Журнал времени"
