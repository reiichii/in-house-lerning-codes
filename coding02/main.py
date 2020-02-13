# import glob
import os
import json


class TargetData:
    def __init__(self, data):
        try:
            self.data = json.loads(data)
            self.appli_id = self.data["appli_id"]
            self.event_name = self.data["event_name"]
        except (json.decoder.JSONDecodeError, KeyError) as error:
            print(f"ファイルに不備があります:{error}")
            raise

    def check_log(self, event):
        print(event["event"]["name"])

        if event["appli_id"] == self.appli_id \
                and event["event"]["name"] == self.event_name:
            return True


class EventLog:
    def __init__(self, log):
        try:
            self.log = json.loads(log)
        except json.decoder.JSONDecodeError as error:
            print(f"データが壊れています: {error}")

    def export_log(self):
        # 対象のログを都度標準出力
        format_log = [d for d in self.log.values()]
        print(*format_log, sep=",")


def main(event_file, request_file):

    with open(event_file, "r") as logs, open(request_file, "r") as targets:
        for t in targets:
            target = TargetData(t)

            for log in logs:
                event = EventLog(log)

                # appli_idの確認
                if not target.check_log(event.log):
                    continue

                event.export_log()


if __name__ == "__main__":
    # event_log_files = os.path.basename("./events.2019-08-04-03.masked.txt")
    event_file = os.path.basename("./events.10.txt")
    request_file = os.path.basename("./request_data.txt")
    main(event_file, request_file)
