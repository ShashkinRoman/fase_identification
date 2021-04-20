from monitoring_system.models import Journal, User
from datetime import datetime, timedelta
from sys import argv
import calendar
import pandas as pd
import numpy as np


if argv[1] == '1':
    start_day = (7, 30)
    end_day = (16, 00)
if argv[1] == '2':
    start_day = (16, 00)
    end_day = (00, 30)
if argv[1] == '3':
    start_day = (00, 30)
    end_day = (7, 30)


def create_dates(yearnumber: str, mount_number: str):
    start_month = datetime(int('20' + yearnumber), int(mount_number), 1, 0, 0, 0)
    end_month = datetime(int('20' + yearnumber), int(mount_number),
                         calendar.monthrange(int('20' + yearnumber), int(mount_number))[0], 0, 0, 0)
    pass


def day_reports(start_day, end_day):
    """ Отчет по количеству учтенного времени
    {date: 1, name_1: time_inside: 7:23, time_outside: 0:37, coming: 7:30, leave: 16:00
    timetable: ((7:23, True), (8:53, False), ...), video_path: ((7:30, /static/qweq), (...))"""
    journal = Journal.objects.values_list('status', 'userid', 'userid_id__first_name', 'userid_id__second_name',
                                          'status_recoding_time', 'path_on_video').\
        filter(status_recoding_time__range=(start_day, end_day))
    df = pd.DataFrame(journal, columns = ['status', 'userid', 'first_name', 'second_name',
                                         'status_recoding_time', 'path_on_video'])
    df['status_recoding_time'] = pd.to_datetime(df.status_recoding_time).dt.tz_convert(None)

    reports = []
    report = {}
    workers_id = list(df['userid'].unique())

    for worker in workers_id:
        coming = df.loc[df['userid'] == worker].loc[df['status'] == True].\
            sort_values(by=['status_recoding_time']).head(1).status_recoding_time
        leave = df.loc[df['userid'] == worker].loc[df['status'] == False].\
            sort_values(by=['status_recoding_time'], ascending=False).head(1).status_recoding_time

        time_inside = 0
        time_outside = 0
        video_path = []  # пока не реализовано

        # Устанавливаем стату на "вход" и находим время первого подхода к двери со статусом "вход"
        status_worker = True
        coming_to_door = df.loc[df['userid'] == worker].loc[df['status'] == status_worker]. \
            sort_values(by=['status_recoding_time']).head(1).status_recoding_time

        # Сделал на случай, если мне понадобится исходный датафрейм
        df_for_cycle = df

        # Считаем время внутри и снаружи, изменяя каждый подход к двери status_worker и отсекая
        for open_door in range(1, len(df.loc[df['userid'] == worker])):
            try:
                if status_worker:
                    # ищем время нахождения внтри до первого выхода и записываем в time_inside
                    status_worker = False
                    coming_out = df_for_cycle.loc[df_for_cycle['userid'] == worker]. \
                        loc[df_for_cycle['status'] == status_worker]. \
                        sort_values(by=['status_recoding_time']).head(1).status_recoding_time

                    time_inside_ = coming_out.values[0] - coming_to_door.values[0]
                    time_inside += time_inside_

                    # сокращаем датафрейм и устанавливаем подход к двери на тот который будем минусовать в следуюзий раз
                    df_for_cycle = df_for_cycle. \
                    loc[df_for_cycle['userid'] == worker][df['status_recoding_time'] >= coming_out.values[0]]
                    coming_to_door = df_for_cycle.loc[df_for_cycle['userid'] == worker]. \
                        sort_values(by=['status_recoding_time']).head(1).status_recoding_time
                    # проверяем не последний ли это выход, если последний, то прерываем цикл
                    if coming_out.values[0] == leave.values[0]:
                        print('konec suka')
                        break

                if not status_worker:
                    status_worker = True
                    coming_in = df_for_cycle.loc[df_for_cycle['userid'] == worker]. \
                        loc[df_for_cycle['status'] == status_worker].\
                        sort_values(by=['status_recoding_time']).head(1).status_recoding_time

                    time_outside_ = coming_in.values[0] - coming_to_door.values[0]
                    time_outside += time_outside_
                    df_for_cycle = df_for_cycle.loc[df_for_cycle['userid'] == worker][
                        df['status_recoding_time'] >= coming_in.values[0]]

                    coming_to_door = df_for_cycle.loc[df_for_cycle['userid'] == worker]. \
                        sort_values(by=['status_recoding_time']).head(1).status_recoding_time

            except IndexError:
                print('pohuy pliashem')
                break

        worker_first_name = df.loc[df['userid'] == worker].head(1).first_name.get(0)
        worker_second_name = df.loc[df['userid'] == worker].head(1).second_name.get(0)
        report['date'] = (start_day.strftime("%d-%m-%Y %H:%M:%S"), end_day.strftime("%d-%m-%Y %H:%M:%S"))
        report['name'] = ' '.join((worker_first_name, worker_second_name))
        report['coming'] = str(datetime.utcfromtimestamp(np.datetime64(coming.values[0], 's').astype(int)))
        report['leave'] = str(datetime.utcfromtimestamp(np.datetime64(leave.values[0], 's').astype(int)))
        report['time_inside'] = time_inside.astype('timedelta64[m]')
        report['time_outside'] = time_outside.astype('timedelta64[m]')
        report['video_path'] = video_path
        reports.append(report)
    return reports


def var():
    start_day = pd.to_datetime('2021-04-16 00:00:00')
    end_day = pd.to_datetime('2021-04-16 23:59:59')


