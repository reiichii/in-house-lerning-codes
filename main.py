# -*- coding: utf-8 -*-
import json
import pathlib
from multiprocessing import Process

def export_file(filename, text):
    dir = 'output'
    file = '{0}/{1}.log'.format(dir, filename)
    with open(file, 'a') as f:
        f.write(text)

def export_error_file(error_msg, line):
    line = '{0}: {1}'.format(error_msg, line)
    export_file('error', line)

def get_appli_id(line):
    error_msg = ''
    appli_id = ''
    try:
        line_json = json.loads(line)
        appli_id = line_json['appli_id']
    except (json.decoder.JSONDecodeError, KeyError) as error_msg:
        return '', error_msg

    return appli_id, ''

def validate_appli_id(appli_id):
    error_msg = ''
    if appli_id == '':
        error_msg = 'No appli_id'
    elif '/' in appli_id:
        error_msg = 'Invalid appli_id'

    return error_msg

def multi_process(idx, num_process, lines):
    for line in lines[idx::num_process]:
        if not line: return

        appli_id, error = get_appli_id(line)
        if error:
            export_error_file(error, line)
            continue

        error_msg = validate_appli_id(appli_id)
        if len(error_msg) > 0:
            export_error_file(error_msg, line)
            continue

        # アプリIDごとにファイルに出力
        export_file(appli_id, line)

def main():
    num_process = 8

    with open('input/events.2019-08-04-03.300000.last.txt') as f:
#    with open('input/test_events_1000.txt') as f:
        lines = f.readlines()
        process_list = []
        for i in range(num_process):
            p = Process(target=multi_process, args=(i, num_process, lines))
            process_list.append(p)

        for p in process_list:
            p.start()
        for p in process_list:
            p.join()

if __name__=='__main__':
    main()
