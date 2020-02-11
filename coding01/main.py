# -*- coding: utf-8 -*-
import json


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


def main():
    with open('input/events.2019-08-04-03.300000.last.txt') as f:
        for line in f:
            if not line:
                return

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


if __name__ == '__main__':
    main()
