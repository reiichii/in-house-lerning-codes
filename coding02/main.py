# import glob
import os
import json


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
            print(f"ファイルに不備があります:{error}")
            raise

    def check_log(self, event):

        if event["appli_id"] == self.appli_id \
                and event["event"]["name"] == self.event_name:
            return True


class EventLog:
    def __init__(self, log):
        try:
            self.log = json.loads(log)
        except json.decoder.JSONDecodeError as error:
            print(f"データが壊れています: {error}")

    def export_log(self, target_keys, target_key_values):
        # 対象のログを都度標準出力
        format_header = [
            "appli_id",
            "event.timestamp",
            "device_type",
            "popinfo_id",
            "event.name"
        ]
        format_header.extend(target_keys)
        print(*format_header, sep=",")

        format_log = [
            self.log["appli_id"],
            self.log["event"]["timestamp"],
            self.log["device_type"],
            self.log["popinfo_id"],
            self.log["event"]["name"]
        ]
        format_log.extend(target_key_values)
        print(*format_log, sep=",")


class EventKey:
    def __init__(self, e):
        self.data = e

    def check_key(self, target_keys):
        target_data = []
        for tk in target_keys:
            for j in self.data:
                if j["key"] == tk:
                    target_data.append(j["value"])

        return target_data


def main(event_file, request_file):

    with open(event_file, "r") as logs, open(request_file, "r") as targets:
        for t in targets:
            target = TargetData(t)

            for log in logs:
                event = EventLog(log)

                # appli_idとeventの確認
                if not target.check_log(event.log):
                    continue

                # keyを確認
                if target.keys:
                    event_key = EventKey(event.log["event"]["value"])
                    target_key_value = event_key.check_key(target.keys)
                    if not target_key_value:
                        continue

                event.export_log(target.keys, target_key_value)


if __name__ == "__main__":
    # event_log_files = os.path.basename("./events.2019-08-04-03.masked.txt")
    event_file = os.path.basename("./events.10.txt")
    request_file = os.path.basename("./request_data.txt")
    main(event_file, request_file)
