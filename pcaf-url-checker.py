#Import
import pandas as pd
from pandas import DataFrame
import urllib.request
from colorama import Fore
from datetime import date


# Check if a file is accessible
def file_accessible(file):
    # Check if a file exists and is accessible.
    try:
        f = open(file, mode = "r")
        f.close()
    except IOError as e:
        return False
    return True

#url checker function
def check(address):
    try:
        req=urllib.request.Request(url=address)
        resp=urllib.request.urlopen(req)
        if resp.status in [400,404,408,409,501,502,503]:
            status = resp.status
            reason = resp.reason
            color = Fore.RED
            redir = "noredirect"
        elif resp.status in [403]:
            status = resp.status
            reason = resp.reason
            color = Fore.YELLOW
            if resp.url != address:
                redir = "redirect"
            else:
                redir = "noredirect"
        else:
            status = resp.status
            reason = resp.reason
            color = Fore.GREEN
            if resp.url != address:
                redir = "redirect"
            else:
                redir = "noredirect"
    except Exception as e:
            #print(Fore.RED + "{}-{}".format(e,address))
            status = "Exception"
            reason = "Exception"
            redir = ""
            color = Fore.RED
            pass
    return status, reason, address, color, redir

# show results of url checker function and export it to a txt file
def check_list(link_list, print_cmd, error_cmd, file_cmd):
    #link_list = list of urls
    #print_cmd = "print"
    #error_cmd = "only error", else
    #file_cmd = "txt", "csv", else
    end = len(link_list)
    if file_cmd == "txt":
        filename = "pcaf_linkcheck" + "_" + str(date.today()) +".txt"
        if not file_accessible(filename):
            output = open(filename, "w")
        else:
            filename = "pcaf_linkcheck" + "_" + str(date.today()) + ".txt"
            counter = 1
            while file_accessible(filename):
                counter += 1
                filename = "pcaf_linkcheck" + "_" + str(date.today()) + "_" + str(counter) + ".txt"
            output = open(filename, "w")
        for i, link in enumerate(link_list, 1):
            status, reason, address, color, redir = check(link)
            percent = (float(i) / float(end)) * float(100)
            if print_cmd == "print" + error_cmd != "only error":
                # Print and save, and full list
                print(f"{i}/{end}, {percent}%, : {color}{status} : {redir} {address}"+ Fore.WHITE)
                output.write(f"{i} {status} : {redir} : {address} \n")
            elif print_cmd == "print" + error_cmd == "only error":
                # Print and save, and only errors
                if status != 200:
                    print(f"{i}/{end}, {percent}%, : {color}{status} : {redir} {address}" + Fore.WHITE)
                    output.write(f"{i} {status} : {redir} : {address} \n")
            elif print_cmd != "print" + error_cmd != "only error":
                # No Print and save, and full list
                output.write(f"{i} {status} : {redir} : {address} \n")
            elif print_cmd != "print" + error_cmd == "only error":
                # No Print, only save, and only errors
                if status != 200:
                    output.write(f"{i}: {address} \n")
            else:
                output.write(f"{i} {status}: {address} \n")
        output.close()
    elif file_cmd == "csv":
        filename = "pcaf_linkcheck" + "_" + str(date.today()) + ".csv"
        if not file_accessible(filename):
            filename = filename
        else:
            filename = "pcaf_linkcheck" + "_" + str(date.today()) + ".csv"
            counter = 1
            while file_accessible(filename):
                counter += 1
                filename = "pcaf_linkcheck" + "_" + str(date.today()) + "_" + str(counter) + ".csv"

        df_temp = DataFrame(columns=["status", "reason", "redirect", "address"])
        for i, link in enumerate(link_list, 1):
            status, reason, address, color, redir = check(link)
            percent = (float(i) / float(end)) * float(100)
            if print_cmd == "print" + error_cmd != "only error":
                # Print and save, and full list
                print(f"{i}/{end}, {percent}%, : {color}{status} : {redir} {address}" + Fore.WHITE)
                new_row = {"status": status, "reason": reason, "redirect": redir, "address": address}
                df_temp.append(new_row, ignore_index=True)
            elif print_cmd == "print" + error_cmd == "only error":
                # Print and save, and only errors
                if status != 200:
                    print(f"{i}/{end}, {percent}%, : {color}{status} : {redir} {address}" + Fore.WHITE)
                    new_row = {"status": status, "reason": reason, "redirect": redir, "address": address}
                    df_temp.append(new_row, ignore_index=True)
            elif print_cmd != "print" + error_cmd != "only error":
                # No Print and save, and full list
                new_row = {"status": status, "reason": reason, "redirect": redir, "address": address}
                df_temp.append(new_row, ignore_index=True)
            elif print_cmd != "print" + error_cmd == "only error":
                if status != 200:
                    new_row = {"status": status, "reason": reason, "redirect": redir, "address": address}
                    df_temp.append(new_row, ignore_index=True)
            else:
                new_row = {"status": status, "reason": reason, "redirect": redir, "address": address}
                df_temp.append(new_row)
        df_temp.to_csv(filename, index=True)
    else:
        print("No file mode spefified, only print active. Results won't be saved!")
        for i, link in enumerate(link_list, 1):
            status, reason, address, color, redir = check(link)
            percent = (float(i) / float(end)) * float(100)
#FÜGE WHILE CMD HINZU
            if error_cmd != "only error":
                print(f"{i}/{end}, {percent}%, : {color}{status} : {redir} {address}" + Fore.WHITE)
            elif error_cmd == "only error":
                if status != 200:
                    print(f"{i}/{end}, {percent}%, : {color}{status} : {redir} {address}" + Fore.WHITE)
            else:
                print("Please specify mode!")
    return

def write_list_to_txt(list):
    output = open("vfu_linkcheck_errorlist" + str(date.today()) + ".txt", "w")
    for i, item in enumerate(list, 1):
        output.write(str(i) + ", " + str(item) + "\n")
    output.close()
    return

def write_list_to_csv(list):
    df_temp = DataFrame(list)
    gfg_csv_data = df.to_csv("vfu_linkcheck_errorlist" + str(date.today()) + ".csv", index=True)
    return

# test the different url checker options
def test_funct():
    print("Test print")
    check_list(links, "print", "", "")
    check_list(links, "print", "only error", "")
    check_list(links, "", "", "")
    check_list(links, "", "only error", "")

    print("Test txt")
    check_list(links, "print", "", "txt")
    check_list(links, "print", "only error", "txt")
    check_list(links, "", "", "txt")
    check_list(links, "", "only error", "txt")

    print("Test csv")
    check_list(links, "print", "", "csv")
    check_list(links, "print", "only error", "csv")
    check_list(links, "", "", "csv")
    check_list(links, "", "only error", "csv")
    return

# load data
df = pd.read_csv("PCAF_emission_factor_database.csv")
full_links_lst = df.iloc[:,-3].to_list()
links = pd.Series(full_links_lst).unique().tolist()

# check urls
    #check_list(links, "print"/"", "only error"/"", "txt"/"csv"/"")

check_list(links, "print", "", "csv")


print("Program finished")
