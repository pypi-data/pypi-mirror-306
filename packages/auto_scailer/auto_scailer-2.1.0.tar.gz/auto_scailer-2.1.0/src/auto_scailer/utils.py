import subprocess
import json
import os
import requests as reqs

line_status={
    200: "Success",
    400: "Bad request",
    401: "Invalid access token",
    500: "Failure due to server error"
}

def get_cpu_use():
    snapshot = subprocess.run(["docker", "stats", "--no-stream", "--format", "json"], capture_output=True)
    p_rst = snapshot.stdout.decode("utf-8").strip()

    if p_rst=="":
        print("[INFO] 실행중인 container가 없습니다.")
        return None,None
    else:
        containers=dict()

        for container in list(map(json.loads,snapshot.stdout.decode("utf-8").strip().split("\n"))):
            containers[container["Name"]]=container["CPUPerc"]

        cnts = len(list(filter(lambda x:"samdul-blog" in x,containers.keys())))

        if cnts==0:
            print("[INFO] 실행중인 container가 없습니다.")

            return None,None

        cpu_use = containers["samdul-blog-1"]

        return cpu_use, cnts

def get_config():
    from configparser import ConfigParser

    cfp = ConfigParser()

    cfp.read(f"{get_file_path()}/config/config.ini")

    return cfp

def get_limit():

    limit_cfg = get_config()["limit"]

    return limit_cfg["scale_in_value"],limit_cfg["scale_out_value"]

def send_line_noti(message):
    # curl -X POST -H "Authorization: Bearer $LINE_TOKEN" -F "message=1"
    LINE_TOKEN=os.getenv("LINE_TOKEN")
    if LINE_TOKEN==None:
        print("[WARN] LINE_TOKEN이 존재하지 않습니다.")
    else:
        headers={
            "Authorization" : f"Bearer {LINE_TOKEN}"
        }
        msg={
            "message" : message
        }

        status=reqs.post("https://notify-api.line.me/api/notify", data=msg, headers=headers).status_code

        return (status,line_status[status]) if status in line_status else (status,"Processed over time or stopped")

def get_file_path():
    return os.path.dirname(os.path.abspath(__file__))

def get_log_path():
    return f"{get_file_path()}/logs"

def get_compose_file_path():
    rst=subprocess.run(["docker","compose","ls","--format","json"], capture_output=True).stdout.decode("utf-8").strip()
    rst=eval(rst)

    return rst[-1]["ConfigFiles"] if len(rst)!=0 else None