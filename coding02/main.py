import json
import os
import sys


class LogFormatException(Exception):
    pass


class TargetData:
    def __init__(self, data):
        try:
            self.data = json.loads(data)
            self.appli_id = self.data["appli_id"]
            self.event_name = self.data["event_name"]
            self.keys = [
                self.data["key1"],
                self.data["key2"],
            ]
        except (json.decoder.JSONDecodeError, KeyError) as error:
            sys.exit(f"クライアント要望ファイルに不備があります:{error}")

    def check_log(self, appli_id, event_name):
        if appli_id == self.appli_id \
                and event_name == self.event_name:
            return True
        return False

    def get_event_key(self, event):
        event_value = []
        for key in self.keys:
            for e in event:
                if e["key"] == key:
                    event_value.append(e["value"])

        return event_value


class EventLog:
    def __init__(self, log):
        self.log = log
        self.appli_id = log["appli_id"]
        self.event = log["event"]
        self.event_name = self.event["name"]


class EventData:
    def __init__(self, event):
        self.name = event["name"]
        self.timestamp = event["timestamp"]
        self.kvs = event["value"]


class ExportCSV:
    def export_csv_header(self, target_keys):
        format_header = [
            "appli_id",
            "event.timestamp",
            "device_type",
            "popinfo_id",
            "event.name"
        ]
        format_header.extend(target_keys)
        print(*format_header, sep=",")

    def export_csv_value(self, log, target_key_values):
        format_log = [
            log["appli_id"],
            log["event"]["timestamp"],
            log["device_type"],
            log["popinfo_id"],
            log["event"]["name"]
        ]
        format_log.extend(target_key_values)
        print(*format_log, sep=",")


def validate_event_log(log):
    try:
        log_dict = json.loads(log)
    except json.decoder.JSONDecodeError as json_error:
        raise LogFormatException("ログの形式が不正です", json_error)

    if not log_dict.get("appli_id") or not log_dict.get("event"):
        raise LogFormatException("イベントログに必要なキーが存在しません")

    if not log_dict["event"].get("name"):
        raise LogFormatException("イベントログに必要なキーが存在しません")

    return log_dict


def validate_event_data(event):
    if not event.get("name") \
            or not event.get("timestamp") \
            or not event.get("value"):
        raise LogFormatException("イベントデータに必要なキーが存在しません")
    return event


def export_filtering_event(event_file, target_file):
    with open(event_file, "r") as logs, open(target_file, "r") as targets:
        export_csv = ExportCSV()

        for t in targets:
            target = TargetData(t)
            export_csv.export_csv_header(target.keys)

            for l in logs:
                try:
                    event_log = EventLog(validate_event_log(l))
                except LogFormatException:
                    continue

                if not target.check_log(event_log.appli_id, event_log.event_name):
                    continue

                if target.keys:
                    event_data = EventData(validate_event_data(
                        event_log.event))
                    target_event_value = target.get_event_key(event_data.kvs)
                else:
                    target_event_value = []

                export_csv.export_csv_value(event_log.log, target_event_value)


if __name__ == "__main__":
    event_file = os.path.basename("./events.2019-08-04-03.masked.txt")
    # event_file = os.path.basename("./events.10.txt")
    target_file = os.path.basename("./target_data.txt")
    export_filtering_event(event_file, target_file)
