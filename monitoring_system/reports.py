from monitoring_system.models import Journal, User
from datetime import datetime
from sys import argv
import calendar
import pandas as pd
import numpy as np

month = 4


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


def reports(start_date, end_date):
    """ Считает отчет по количеству учтенного времени
    {date: 1, name_1: time_inside: 7:23, time_outside: 0:37, coming: 7:30, leave: 16:00
    timetable: ((7:23, True), (8:53, False), ...), video_path: ((7:30, /static/qweq), (...))"""
    journal = Journal.objects.values_list('status', 'userid', 'userid_id__first_name', 'userid_id__second_name',
                                          'status_recoding_time', 'path_on_video').\
        filter(status_recoding_time__range=(start_date, end_date))
    df = pd.DataFrame(journal, columns= ['status', 'userid', 'first_name', 'second_name',
                                         'status_recoding_time', 'path_on_video'])


    report = {}
    workers_id = list(df['userid'].unique())
    for i in workers_id:
        coming = df.loc[df['userid'] == i].loc[df['status'] == True].\
            sort_values(by=['status_recoding_time']).head(1).status_recoding_time
        leave = df.loc[df['userid'] == i].loc[df['status'] == False].\
            sort_values(by=['status_recoding_time'], ascending=False).head(1).status_recoding_time

        time_inside = []
        time_outside = []
        video_path = []
        timetable = ['?']

        """для каждого сотрудника в дате
        найти первое значение со статусо true (coming)
        найти следующее значение до статуса False
        посчитать это время
        от фолса найти значение до статуса True
        посчитать время отсутствия
        и т.д. до последнего false(leave)"""
        coming_inside = df.loc[df['userid'] == i].loc[df['status'] == True].\
            sort_values(by=['status_recoding_time']).head(1)
        for i in df:
            "Найти следующее время с false, сравнить с leave, если не равно, то" \
            "посчитать дельту, записатьв и insaid" \
            "найти следующую дату true, записать в outside" \
            "else дата с false = leave:" \
            "break " \
            ""
            if not df.sort_values(by=['status_recoding_time'])['status_recoding_time'].min().to_datetime64() \
                   == np.datetime64(coming.values[0]):

                print('jo[a')
            else:
                print('da suka')
            df.loc[df['status_recoding_time'] > coming_inside]
            df.sort_values('status_recoding_time').status_recoding_time == coming_inside.values[0]


        worker_first_name = df.loc[df['userid'] == i].head(1).first_name.get(0)
        worker_second_name = df.loc[df['userid'] == i].head(1).second_name.get(0)
        report['date'] = (start_date.strftime("%d-%m-%Y %H:%M:%S"), end_date.strftime("%d-%m-%Y %H:%M:%S"))
        report['name'] = ' '.join((worker_first_name, worker_second_name))
        report['coming'] = str(datetime.utcfromtimestamp(np.datetime64(coming.values[0], 's').astype(int)))
        report['leave'] = str(datetime.utcfromtimestamp(np.datetime64(leave.values[0], 's').astype(int)))
        report['time_inside'] = time_inside
        report['time_outside'] = time_outside
        report['video_path'] = video_path
        report['timetable'] = timetable
    return report


def var():datetime.utcnow()
    # start_date = datetime(2021, 4, 16, 0, 0, 0)
    # end_date = datetime(2021, 4, 16, 23, 59, 59)

