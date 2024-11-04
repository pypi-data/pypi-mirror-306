import pandas as pd
import plotext as plx
from auto_scailer.utils import get_log_path
from glob import glob

def usage_plot():
    usage_log_file_list=glob(f"{get_log_path()}/usage/*.log")
    usage_log_file_list.sort()
    usage_log_file=usage_log_file_list[-1]

    df = pd.read_csv(usage_log_file)

    usage = df["cpu_usage(%)"]
    time = [10*i for i in range(len(usage))]

    plx.plot(time, usage)
    plx.xlabel("time (s)")
    plx.ylabel("cpu_usage (%)")

    plx.show()

def status_plot():
    usage_log_file_list=glob(f"{get_log_path()}/usage/*.log")
    usage_log_file_list.sort()
    usage_log_file=usage_log_file_list[-1]

    df = pd.read_csv(usage_log_file)

    plx.bar(pd.DataFrame(df["cpu_use_status"].value_counts()).index, df["cpu_use_status"].value_counts())
    plx.xlabel("status")
    plx.ylabel("times")

    plx.show()

def scale_plot():
    usage_scale_file_list=glob(f"{get_log_path()}/scale/*.log")
    usage_scale_file_list.sort()
    usage_scale_file=usage_scale_file_list[-1]

    df = pd.read_csv(usage_scale_file)

    plx.bar(pd.DataFrame(df["method"].value_counts()).index, df["method"].value_counts())
    plx.xlabel("method")
    plx.ylabel("times")

    plx.show()
