from auto_scailer.utils import get_limit, get_cpu_use, send_line_noti, get_log_path, get_compose_file_path
import time
import os
from tz_kst import now

log_time=now("%Y%m%d-%H%M%S")
scale_in_value, scale_out_value=map(float,get_limit())


def display_stat(cpu_use=0, scale_cnt=1, status="stable", conti_time=0, time=0):
    print("+"+"-"*87+"+")
    print(f"|\tCPU사용량 (%)\t|\t컨테이너 수\t|\t상태\t|\t지속시간(s)\t|")
    print("-"*89)
    print(f"|\t\t{cpu_use}\t|\t\t{scale_cnt}\t|\t{status}\t|\t\t{conti_time}\t|")
    print("+"+"-"*87+"+")

    print(f"마지막 확인시간 : {time}")

def make_log_file():
    usage_log_path=f"{get_log_path()}/usage"
    scale_log_path=f"{get_log_path()}/scale"

    os.makedirs(usage_log_path, exist_ok=True)
    os.makedirs(scale_log_path, exist_ok=True)

    with open(f"{usage_log_path}/{log_time}.log", "w") as f:
        f.write("cpu_usage(%),time,scale_cnt,cpu_use_status\n")

    with open(f"{scale_log_path}/{log_time}.log", "w") as f:
        f.write("method,time,scale_cnt_before,scale_cnt_after,cpu_usage(%)\n")


def usage_log(cpu_usage, time, scale_cnt, status):
    usage_log_path=f"{get_log_path()}/usage"

    with open(f"{usage_log_path}/{log_time}.log", "a") as f:
        #data = {"cpu_usage(%)":cpu_usage, "time":str(time), "scale_cnt":scale_cnt, "cpu_use_status": status}
        #f.write(str(data))
        f.write(f"{cpu_usage},{time},{scale_cnt},{status}\n")
        #f.write("\n")

def scale_log(method,time,scale_cnt_before,scale_cnt_after,cpu_usage):
    scale_log_path=f"{get_log_path()}/scale"

    with open(f"{scale_log_path}/{log_time}.log", "a") as f:
        #data = {"method":f"scale {method}","scale_cnt_before":scale_cnt_before, "scale_cnt_after":scale_cnt_after, "cpu_usage(%)":cpu_usage }
        #f.write(str(data))
        f.write(f"scale {method},{time},{scale_cnt_before},{scale_cnt_after},{cpu_usage}\n")
        #f.write("\n")

def do_scale(method, scale_cnt):
    print(f"[INFO] container의 수를 {scale_cnt}로 scale {method} 합니다.", end="\n\n")
    os.system(f"docker compose -f {get_compose_file_path()} up -d --scale blog={scale_cnt}")

    code, msg = send_line_noti(f"[INFO] container의 수가 {scale_cnt}로 scale {method} 되었습니다.")


def auto_scailer():
    conti_high=0
    conti_low=0

    cu, scale_cnt =get_cpu_use()

    chk_time=time.time()

    make_log_file()

    while scale_cnt:
        if (chk_time+10)//10==time.time()//10:
            chk_time=time.time()
            cu=float(cu.replace("%",""))
            nowTime=now()

            #### CPU 사용량이 scale_out_value를 넘으면 scale out ####
            if cu >scale_out_value:
                conti_high+=10
            else:
                conti_high=0

            if conti_high==60:
                scale_log("out",nowTime,scale_cnt,scale_cnt+1,cu)
                do_scale("out", scale_cnt+1)
                # print(f"[INFO] container의 수를 {scale_cnt+1}로 scale out 합니다.")
                # os.system(f"docker compose -f {get_compose_file_path()} up -d --scale blog={scale_cnt+1}")

                conti_high=0
            ######################################################
            #### CPU 사용량이 scale_in_value보다 낮으면 scale in ####
            ##### 1개의 컨테이너는 남겨야 함 ########################
            if scale_cnt>1:
                if cu <scale_in_value:
                    conti_low+=10
                else:
                    conti_low=0

                if conti_low==60:
                        scale_log("in",nowTime,scale_cnt,scale_cnt-1,cu)
                        do_scale("in", scale_cnt-1)

                        conti_low=0
            ######################################################
            if conti_high>0:
                status="High"
                conti_time=conti_high
            elif conti_low>0:
                status="Low"
                conti_time=conti_low
            else:
                status="Stable"
                conti_time="-"

            os.system("clear")
            display_stat(cu, scale_cnt, status, conti_time, nowTime)
            usage_log(cu, nowTime, scale_cnt, status)

            cu, scale_cnt =get_cpu_use()
        print(f"잠시 후 통계정보가 갱신됩니다.({(10-time.time()+chk_time)%10:.0f}) ", end="\r", flush=True)