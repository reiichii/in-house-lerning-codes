import json
import os
import sys


class LogFormatException(Exception):
    """イベントログのフォーマットが崩れていた時のエラー"""
    pass


class TargetFileFormatException(Exception):
    """顧客要望定義ファイルのフォーマットが崩れていた時のエラー"""
    pass


class TargetData:
    """参照しているイベントログが求められているものかをチェックする"""
    def __init__(self, data: dict):
        self.appli_id = data["appli_id"]
        self.event_name = data["event_name"]
        self.keys = data["keys"]

    def check_log(self, appli_id: str, event_name: str) -> bool:
        """参照している行のログが求められているものかを確認する

        Arguments:
            appli_id {str} -- event log appli_id
            event_name {str} -- event log event_name
        """
        if appli_id == self.appli_id \
                and event_name == self.event_name:
            return True
        return False

    def get_target_event(self, event: dict) -> list:
        """参照している行のイベントデータの中の求められているデータを取得する

        Arguments:
            event {dict} -- event data

        Returns:
            list -- Required event value
        """
        event_value = []
        for key in self.keys:
            for e in event:
                if e["key"] == key:
                    event_value.append(e["value"])

        return event_value


class EventLog:
    """イベントログを扱う"""
    def __init__(self, log: dict):
        self.log = log
        self.appli_id = log["appli_id"]
        self.event = log["event"]
        self.event_name = self.event["name"]


class EventData:
    """イベントログの中にあるイベントデータを扱うクラス"""
    def __init__(self, event: dict):
        self.name = event["name"]
        self.timestamp = event["timestamp"]
        self.kvs = event["value"]


class ExportCSV:
    """ログをcsv出力する"""
    def export_csv_header(self, target_keys: list) -> None:
        """csvヘッダーを出力

        Arguments:
            target_keys {list}
        """
        format_header = [
            "appli_id",
            "event.timestamp",
            "device_type",
            "popinfo_id",
            "event.name"
        ]
        format_header.extend(target_keys)
        print(*format_header, sep=",")

    def export_csv_value(self, log: dict, target_key_values: list=[] ) -> None:
        """csvデータを出力

        Arguments:
            log {dict} -- target log

        Keyword Arguments:
            target_key_values {[type]} -- target event value (default: {[]:list})
        """
        format_log = [
            log["appli_id"],
            log["event"]["timestamp"],
            log["device_type"],
            log["popinfo_id"],
            log["event"]["name"]
        ]
        format_log.extend(target_key_values)
        print(*format_log, sep=",")


def validate_target_data(data: str) -> dict:
    """顧客定義ファイルのバリデーション

    Arguments:
        data {str} -- 1 line in target data file

    Returns:
        dict -- target data
    """
    try:
        data_dict = json.loads(data)
    except json.decoder.JSONDecodeError as json_error:
        print("クライアント要望ファイルに不備があります")
        raise TargetFileFormatException

    if len(data_dict["keys"]) > 2:
        print("クライアント要望ファイルにキーが２つ以上指定されています")
        raise TargetFileFormatException

    return data_dict


def validate_event_log(log: str) -> dict:
    """参照している行のイベントログのバリデーション

    Arguments:
        log {str} -- 1 line in event log file

    Returns:
        dict -- event log
    """
    try:
        log_dict = json.loads(log)
    except json.decoder.JSONDecodeError:
        print("ログの形式が不正です")
        raise LogFormatException

    if not log_dict.get("appli_id") or not log_dict.get("event"):
        print("イベントログに必要なキーが存在しません")
        raise LogFormatException

    if not log_dict["event"].get("name"):
        print("イベントログに必要なキーが存在しません")
        raise LogFormatException

    return log_dict


def validate_event_data(event: dict) -> dict:
    """イベントデータのバリデーション

    Arguments:
        event {dict} -- event data

    Returns:
        dict -- event data
    """
    if not event.get("name") \
            or not event.get("timestamp") \
            or not event.get("value"):
        print("イベントデータに必要なキーが存在しません")
        raise LogFormatException
    return event


def export_filtering_event(event_file: str, target_file: str) -> None:
    """対象のイベントログのみ出力する

    Arguments:
        event_file {str} -- event log file
        target_file {str} -- target data file
    """
    with open(event_file, "r") as logs, open(target_file, "r") as targets:
        export_csv = ExportCSV()

        for t in targets:
            try:
                target = TargetData(validate_target_data(t))
            except LogFormatException:
                continue
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
                    target_event_value = target.get_target_event(event_data.kvs)

                export_csv.export_csv_value(event_log.log)


if __name__ == "__main__":
    event_file = os.path.basename("./events.2019-08-04-03.masked.txt")
    target_file = os.path.basename("./target_data.txt")
    export_filtering_event(event_file, target_file)
