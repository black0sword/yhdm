import requests
import os
import execjs
import urllib3
import json
from urllib import parse
import urllib
import re
import random
from concurrent.futures import ThreadPoolExecutor
import time
import sys





success = False

animation_num = "22269-1-1"
try:
    animation_num = sys.argv[1]
except Exception as e:
    print(e)

dmbh = animation_num.split("-")[0]
jishu = animation_num.split("-")[2]


#路径命名 ./ts/动漫编号/级数/output.mp4
save_m3u8_path = "./ts/" + dmbh + '/' + jishu + "-m3u8/"
folder_path = "./ts/" + dmbh + '/' + jishu + '/'


if not os.path.exists(save_m3u8_path):
    os.makedirs(save_m3u8_path)

if not os.path.exists(folder_path):
    os.makedirs(folder_path)



def check_proxy_isok():
    while True:
        proxies_json = requests.get(url="http://demo.spiderpy.cn/get/").text
        proxies = json.loads(proxies_json)

        proxies = {
            "https": "http://" + proxies['proxy']
        }
        header = {
            'Host': 'www.yhdmp.cc',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 MicroMessenger/7.0.4.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF",
            'Cookie': 'qike123=%u5F26%u97F3%20-%u8054%u7CFB%u7684%u4E00%u7BAD-%20%u7B2C2%u96C6^https%3A//www.yhdmp.cc/vp/23109-1-1.html_$_%u5F26%u97F3%20-%u8054%u7CFB%u7684%u4E00%u7BAD-%20%u7B2C3%u96C6^https%3A//www.yhdmp.cc/vp/23109-1-2.html_$_|; t1=1774060551519; k1=32978960; k2=4101511674152; t2=1774060587302',
            'Referer': 'https://www.yhdmp.cc/vp/22269-1-0.html'
        }

        print(proxies['https'],end='')

        try:
            isok = requests.get(url="https://www.yhdmp.cc/s_all?kw=1&pageindex=1", timeout=3, proxies=proxies,
                                verify=False, headers=header)
            print("  | " + str(isok.status_code))
            is_success = re.findall(r'日本动漫', isok.text)

            if (isok.status_code == 200 and is_success[0] == "日本动漫"):
                print("[+]获取代理ip成功======>" + proxies['https'])
                return proxies
            else:
                continue

        except Exception as e:
            print("[-]" + proxies['https'] + "代理ip无效")
            continue


def download_url(url):

    xuhao = re.findall(r'-(\d{1,}).ts', url)[0]
    print("正在下载=======> " + xuhao + ".ts")
    url = url.replace("%0A", "").replace("\n", "")

    header = {
        "Host": "ccp-bj29-video-preview.oss-enet.aliyuncs.com",
        "User-Agent": "Mozilla / 5.0(Windows NT 6.1;WOW64)"
    }

    # 下载ts文件(可以开多线程)
    r = requests.get(url=url, headers=header, verify=False, timeout=30).content

    # 二进制写入到本地
    with open(folder_path + xuhao + '.ts', "ab+") as file:
        file.write(r)




if __name__ == '__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    #github某项目代理池
    # proxies = check_proxy_isok()
    # V2ray调试
    proxies = {
        "https":"http://127.0.0.1:10809"
    }
    baseurl = "https://www.yhdmp.cc/"

    #查看时候存在MP4
    if os.path.exists(folder_path + "output.mp4"):
        print("The file exists--" + folder_path + "output.mp4")
        exit(1)

    #查看时候存在m3u8
    if os.path.exists(save_m3u8_path + "index.m3u8"):
        print("The m3u8 exists !")
        success = True
        with open(save_m3u8_path + "index.m3u8",'r',encoding='utf-8') as f:
            ts_arr = re.findall(r"(https://ccp-.+&x-oss-signature=.+%3D)\n", f.read())
            print(ts_arr)
            print("ts文件的总长度--> " + str(len(ts_arr)))
            # 开线程池
            with ThreadPoolExecutor(max_workers=len(ts_arr)) as executor:
                executor.map(download_url, ts_arr)
                executor.shutdown()
                # 等待所有线程执行完毕


        filelist_path = folder_path + "/file_list.txt"
        video_file = folder_path + "/output.mp4"

        if (os.path.exists(video_file)):
            print("Video has been Exist !")
            exit(1)

        if os.path.exists(filelist_path):
            os.remove(filelist_path)
            #print("File has been removed.")

        file_list = os.listdir(folder_path)

        #print(file_list)
        file_list.sort(key=lambda x: int(x[:-3]))

        with open(filelist_path, "w+") as f:
            for file in file_list:
                # print(file)
                f.write("file '{}'\n".format(file))

        #os.system("chcp 65001")
        time.sleep(0.1)
        os.system("cd " + folder_path + " & ffmpeg.exe -f concat -i file_list.txt -c copy output.mp4 ")
        time.sleep(0.1)
        #os.system("cd " + folder_path + " &del *.ts")
        exit(1)

    radom_num = str(random.randint(10,99))

    #cookie与qike123 t1 t2 k1 k2 有关
    header = {
        'Host': 'www.yhdmp.cc',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 MicroMessenger/7.0.4.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF",
        'Cookie': 'qike123=%u5F26%u97F3%20-%u8054%u7CFB%u7684%u4E00%u7BAD-%20%u7B2C2%u96C6^https%3A//www.yhdmp.cc/vp/23109-1-1.html_$_%u5F26%u97F3%20-%u8054%u7CFB%u7684%u4E00%u7BAD-%20%u7B2C3%u96C6^https%3A//www.yhdmp.cc/vp/23109-1-2.html_$_|; t1=1774060551519; k1=32978960; k2=4101511674152; t2=1774060587302',
        'Referer':'https://www.yhdmp.cc/vp/22269-1-0.html'
    }


    with open(r"./yhdm.js", 'r',encoding='utf-8') as f:
        # 读取js文件的全部内容到content变量中
        content = f.read()

    ctx = execjs.compile(content)# 获取代码编译完成后的对象
    # res = ctx.call("__yh_cb_getplay_url", 6, 2) # 调用js函数add，并传入它的参数
    print("初始化开始 ! ! !  ")
    url1 = ctx.call("__yh_cb_getplay_url",animation_num) # 调用js函数add，并传入它的参数

    #https://www.yhdmp.cc/_getplay?aid=22350&playindex=1&epindex=0&r=0.8063252426589729
    print(url1)




    # jsonData = requests.get(url=url1,headers=header,verify=False,proxies=proxies).text
    i = 0
    while(True):

        i = i + 1
        if(i > 1):
            break
        print("请求vurl中 ! ! !")



        jsonData = requests.get(url=url1,headers=header,verify=False,timeout=12,proxies=proxies).text
        print(jsonData)

        _vurl = ''
        # 字符串转化为字典
        try:
            parse_json = json.loads(jsonData)
            _vurl = parse_json['vurl']
        except Exception as e:
            print(e)



        if (_vurl != ''):
            print("正在获取m3u8地址 ! ! !")

            with open(r"./yhdm-step2.js", 'r', encoding='utf-8') as f:
                # 读取js文件的全部内容到content变量中
                content1 = f.read()
            ctx = execjs.compile(content1)

            # 获取代码编译完成后的对象
            # res = ctx.call("__yh_cb_getplay_url", 6, 2) # 调用js函数add，并传入它的参数
            _m3u8_url = ctx.call("__getplay_rev_data", _vurl)  # 调用js函数add，并传入它的参数
            print(_m3u8_url)
            if('xmfans' in _m3u8_url):
                print("!!!!!获取地址成功!!!!!!")

                m3u8_url = urllib.parse.unquote(_m3u8_url)
                print(m3u8_url)

                #获得m3u8内容
                res = requests.get(url=m3u8_url,headers=header,verify=False,timeout=13,proxies=proxies).text
                # print(res)
                with open(save_m3u8_path + "index.m3u8",'w',encoding="utf-8") as f1:
                    f1.write(res)


                ts_arr = re.findall(r"(https://ccp-.+&x-oss-signature=.+%3D)\n", res)
                print(res)
                print("ts文件的总长度--> "+str(len(ts_arr)))

                success = True
                # 开线程池
                with ThreadPoolExecutor(max_workers=len(ts_arr)) as executor:
                    executor.map(download_url, ts_arr)
                    # 等待所有线程执行完毕
                    executor.shutdown()

                break
            else:
                continue


        else:
            continue
        # except Exception as e:
        #     print(e)


    #如果成功就进入合并ts文件(这里会调用到ffmpeg.exe)
    if(success):
        filelist_path = folder_path + "/file_list.txt"
        video_file = folder_path + "/output.mp4"

        if (os.path.exists(video_file)):
            print("Video has been Exist !")
            exit(1)

        if os.path.exists(filelist_path):
            os.remove(filelist_path)
            #print("File has been removed.")

        file_list = os.listdir(folder_path)

        #print(file_list)
        file_list.sort(key=lambda x: int(x[:-3]))

        with open(filelist_path, "w+") as f:
            for file in file_list:
                # print(file)
                f.write("file '{}'\n".format(file))

        # os.system("chcp 65001")
        os.system("cd " + folder_path + " & ffmpeg.exe -f concat -i file_list.txt -c copy output.mp4")
        #os.system("cd " + folder_path + " &del *.ts")