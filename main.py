import colorama, httpx, base64, sys, time, os, threading
from pathlib import Path
from colorama import Fore, init, Style, Back
import boostingshit
from boostingshit import thread_boost, boost_server

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def getinviteCode(invite_input):
    if "discord.gg" not in invite_input:
        return invite_input
    if "discord.gg" in invite_input:
        invite = invite_input.split("discord.gg/")[1]
        return invite
    if "https://discord.gg" in invite_input:
        invite = invite_input.split("https://discord.gg/")[1]
        return invite
    
def inputNumber(message):
    while True:
        try:
            userInput = int(input(message))
        except ValueError:
            print(Fore.RED + "This value cannot be a string!" + Fore.WHITE)
            continue
        else:
            return userInput
            break

def mainmenu():
    printwatermark()
    home = (Fore.CYAN + f'''
    1. Boost Server
    2. View Stock
    3. Check Nitro Tokens
    4. Exit
''' + Fore.WHITE)
    for char in home:
        time.sleep(0.00009)
        sys.stdout.write(char)
        sys.stdout.flush()
    choices = input()
    if(input == "1"):
        typeofboost = inputNumber(Fore.CYAN + "Duration of Boost [90 or 30 days]: " + Fore.WHITE)
        while typeofboost != 90 and typeofboost != 30:
            print(Fore.RED + "Duration can either be 30 days or 90 days" + Fore.WHITE)
            typeofboost = inputNumber(Fore.CYAN + "Duration of Boost [90 or 30 days]: " + Fore.WHITE)
        if typeofboost == 90:
            file = "3m_tokens.txt"
        if typeofboost == 30:
            file = "1m_tokens.txt"
        
        if checkEmpty(file) == True:
            print()
            print(Fore.RED + "No Stock" + Fore.WHITE)
            print()
            input("Press Enter To Continue...")
            cls()

            mainmenu()

        
        invite_input = input(Fore.CYAN + "Permanent Invite Link to the server you want to boost [https://discord.gg/[invite_code]]: " + Fore.WHITE)
        while invite_input.isdigit == True:
            print(Fore.RED + "Invite Link cannot be a number" + Fore.WHITE)
            invite_input = input(Fore.CYAN + "Permanent Invite Link to the server you want to boost [https://discord.gg/[invite_code]]: " + Fore.WHITE)

        invite = getinviteCode(invite_input)
        valid_invite = validateInvite(invite)
        while valid_invite == False:
            print(Fore.RED + f"Invalid Invite Code, {invite}")
            invite_input = input(Fore.CYAN + "Permanent Invite Link to the server you want to boost [https://discord.gg/[invite_code]]: " + Fore.WHITE)
            invite = getinviteCode(invite_input)
            valid_invite = validateInvite(invite)


        amount_input = inputNumber(Fore.CYAN + "Amount of Boosts: " + Fore.WHITE)
        while amount_input % 2 != 0:
            print(Fore.RED + "Amount of Boosts must be even." + Fore.WHITE)
            amount_input = inputNumber(Fore.CYAN + "Amount of Boosts: " + Fore.WHITE)
        
        if amount_input/2 > len(open(file , encoding='utf-8').read().splitlines()):
            print()
            print(Fore.RED + "Not Enought Stock" + Fore.WHITE)
            print()
            input("Press Enter To Continue...")
            cls()

            mainmenu()


        amount = amount_input

        EXP = True
        if typeofboost == 90:
            EXP = False

        threads = []
        no_working = False
        r = 0
        numTokens = int(amount/2)
        all_tokens = get_all_tokens(file)
        tokens_to_use = []
        print(Fore.GREEN + "Looking for working tokens" + Fore.WHITE)
        while len(tokens_to_use) != numTokens:
            try:
                token = all_tokens[r]
                if checktoken(token, file) == True:
                    tokens_to_use.append(token)
                r += 1
            except IndexError:
                print(Fore.RED + "Not Enough Working Tokens in Stock" + Fore.WHITE)
                no_working = True
                break
        
        if no_working == True:
            input("Press Enter To Continue...")
            cls()
            
            mainmenu()
        else:
            time.sleep(2)
            cls()
            start = time.time()
            print(Fore.GREEN + "Starting Boosts" + Fore.WHITE)
            tokens_to_use = all_tokens
            for i in range(numTokens):
                token = tokens_to_use[i]
                t = threading.Thread(target=thread_boost, args=(invite, amount, EXP, token))
                t.daemon = True
                threads.append(t)

            for i in range(numTokens):
                threads[i].start()
                
            for i in range(numTokens):
                threads[i].join()
            
            end = time.time()
            time_taken = round(end-start)
            print(Fore.GREEN + f"Successfully boosted discord.gg/{invite}, {amount} times in {time_taken} seconds.")
            

            print()
            input("Press Enter To Continue...")
            cls()
            
            mainmenu()
    elif(input == "2"):
        stock()
    elif(input == "3"):
        nitrochecker()
    elif(input == "4"):
        print(Fore.RED + "Exiting!")
        time.sleep(1500)
        sys.exit()
    else:
        print("invalid option!")
        time.sleep(1750)
        cls()
        mainmenu()
def stock():
    print(Fore.GREEN + f"3 Months Nitro Tokens Stock: {len(open('3m_tokens.txt', encoding='utf-8').read().splitlines())}")
    print(f"3 Months Boost Stock: {len(open('3m_tokens.txt', encoding='utf-8').read().splitlines())*2}")
    print()
    print(f"1 Month Nitro Tokens Stock: {len(open('1m_tokens.txt', encoding='utf-8').read().splitlines())}")
    print(f"1 Month Boosts Stock: {len(open('1m_tokens.txt', encoding='utf-8').read().splitlines())*2}" + Fore.WHITE)

def validateInvite(invite):
    if '{"message": "Unknown Invite", "code": 10006}' in httpx.get(f"https://discord.com/api/v9/invites/{invite}").text:
        return False
    else:
        return True
def get_all_tokens(filename):
    all_tokens = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            token = line.strip()
            token = find_token(token)
            if token != None:
                all_tokens.append(token)

    return all_tokens

def nitrochecker():

    three_m_working = 0
    one_m_working = 0

    three_m_used = 0
    one_m_used = 0

    three_m_nonitro = 0
    one_m_nonitro = 0

    three_m_invalid = 0
    one_m_invalid = 0

    three_m_locked = 0
    one_m_locked = 0
    three_m_tokens = get_all_tokens("input/3m_tokens.txt")
    one_m_tokens = get_all_tokens("input/1m_tokens.txt")
    print("Checking 3 Months Nitro Tokens")

    if checkEmpty("input/3m_tokens.txt"):
        print(Fore.RED + "No Stock To Check" + Fore.WHITE)
    
    else:

        for token in three_m_tokens:    
            file = "input/3m_tokens.txt"
            s, headers = get_headers(token)
            profile = validate_token(s, headers)

            if profile != False:
                boost_data = s.get(f"https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots", headers={'Authorization': token})

                if boost_data.status_code == 403:
                    print(Fore.RED + f" ✗ {Fore.WHITE}{token} - {profile}{Fore.RED} [LOCKED]" + Fore.WHITE)
                    removeToken(token, file)
                    three_m_locked += 1
                if len(boost_data.json()) != 0 and boost_data.status_code == 200 or boost_data.status_code == 201:
                    if boost_data.json()[0]['cooldown_ends_at'] != None:
                        print(Fore.RED + f" ✗ {Fore.WHITE}{token} - {profile}{Fore.RED} [USED]" + Fore.WHITE)
                        removeToken(token, file)
                        three_m_used += 1
                if len(boost_data.json()) == 0:
                    removeToken(token, file)
                    print(f"{Fore.RED} ✗ {Fore.WHITE}{token} - {profile}{Fore.RED} [NO NITRO]" + Fore.WHITE)
                    three_m_nonitro += 1
                else:
                    if len(boost_data.json()) != 0 and boost_data.status_code == 200 or boost_data.status_code == 201:
                        if boost_data.json()[0]['cooldown_ends_at'] == None:

                            print(f"{Fore.GREEN} ✓ {Fore.WHITE}{token} - {profile}{Fore.GREEN} [WORKING]" + Fore.WHITE)
                            three_m_working += 1
            else:
                print(Fore.RED + f" ✗ {Fore.WHITE}{token}{Fore.RED} [INVALID]" + Fore.WHITE)
                removeToken(token, file)
                three_m_invalid += 1
    print()
    print("Checking 1 Month Nitro Tokens")
    if checkEmpty("input/1m_tokens.txt"):
        print(Fore.RED + "No Stock To Check" + Fore.WHITE)  
    else:
        for token in one_m_tokens:    
            file = "input/1m_tokens.txt"
            s, headers = get_headers(token)
            profile = validate_token(s, headers)
            if profile != False:
                boost_data = s.get(f"https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots", headers={'Authorization': token})

                if boost_data.status_code == 403:
                    print(Fore.RED + f" ✗ {Fore.WHITE}{token} - {profile}{Fore.RED} [LOCKED]" + Fore.WHITE)
                    removeToken(token, file)
                    one_m_locked += 1
                if len(boost_data.json()) != 0 and boost_data.status_code == 200 or boost_data.status_code == 201:
                    if boost_data.json()[0]['cooldown_ends_at'] != None:
                        print(Fore.RED + f" ✗ {Fore.WHITE}{token} - {profile}{Fore.RED} [USED]" + Fore.WHITE)
                        removeToken(token, file)
                        one_m_used += 1
                if len(boost_data.json()) == 0:
                    removeToken(token, file)
                    print(f"{Fore.RED} ✗ {Fore.WHITE}{token} - {profile}{Fore.RED} [NO NITRO]" + Fore.WHITE)
                    one_m_nonitro += 1
                else:
                    if len(boost_data.json()) != 0 and boost_data.status_code == 200 or boost_data.status_code == 201:
                        if boost_data.json()[0]['cooldown_ends_at'] == None:

                            print(f"{Fore.GREEN} ✓ {Fore.WHITE}{token} - {profile}{Fore.GREEN} [WORKING]" + Fore.WHITE)
                            one_m_working += 1
            else:
                print(Fore.RED + f" ✗ {Fore.WHITE}{token}{Fore.RED} [INVALID]" + Fore.WHITE)
                removeToken(token, file)
                one_m_invalid += 1

    print(f"{Fore.GREEN}WORKING (with nitro) : {Fore.WHITE}{three_m_working}  |  {Fore.RED}USED : {Fore.WHITE}{three_m_used}  |  {Fore.RED}NO NITRO : {Fore.WHITE}{three_m_nonitro}  |  {Fore.RED}LOCKED : {Fore.WHITE}{three_m_locked}  |  {Fore.RED}INVALID : {Fore.WHITE}{three_m_invalid}")
    print(f"{Fore.GREEN}WORKING (with nitro) : {Fore.WHITE}{one_m_working}  |  {Fore.RED}USED : {Fore.WHITE}{one_m_used}  |  {Fore.RED}NO NITRO : {Fore.WHITE}{one_m_nonitro}  |  {Fore.RED}LOCKED : {Fore.WHITE}{one_m_locked}  |  {Fore.RED}INVALID : {Fore.WHITE}{one_m_invalid}")

def checkEmpty(file):
    mypath = Path(file)

    if mypath.stat().st_size == 0:
        return True
    else:
        return False


def get_super_properties():
    properties = '''{"os":"Windows","browser":"Chrome","device":"","system_locale":"en-GB","browser_user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36","browser_version":"95.0.4638.54","os_version":"10","referrer":"","referring_domain":"","referrer_current":"","referring_domain_current":"","release_channel":"stable","client_build_number":102113,"client_event_source":null}'''
    properties = base64.b64encode(properties.encode()).decode()
    return properties

def get_fingerprint(s):
    try:
        fingerprint = s.get(f"https://discord.com/api/v9/experiments", timeout=5).json()["fingerprint"]
        return fingerprint
    except Exception as e:
        return "Error"
    
def find_token(token):
    if ':' in token:
        token_chosen = None
        tokensplit = token.split(":")
        for thing in tokensplit:
            if '@' not in thing and '.' in thing and len(
                    thing) > 30: 
                token_chosen = thing
                break
        if token_chosen == None:
            print(f"Error finding token", Fore.RED)
            return None
        else:
            return token_chosen


    else:
        return token
    
def removeToken(token: str, file:str):
    with open(file, "r") as f:
        fulltokens = f.read().splitlines()
        Tokens = []
        for j in fulltokens:
            p = find_token(j)
            Tokens.append(p)
        for t in Tokens:
            if len(t) < 5 or t == token:
                Tokens.remove(t)
        open(file, "w").write("\n".join(Tokens))

def validate_token(s, headers):
    check = s.get(f"https://discord.com/api/v9/users/@me", headers=headers)
    if check.status_code == 200:
        profile_name = check.json()["username"]
        profile_discrim = check.json()["discriminator"]
        profile_of_user = f"{profile_name}#{profile_discrim}"
        return profile_of_user
    else:
        return False
    
def checktoken(token, file):
    s, headers = get_headers(token)
    profile = validate_token(s, headers)

    if profile != False:

        boost_data = s.get(f"https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots", headers={'Authorization': token})


        if boost_data.status_code == 403:
            print(Fore.RED + f" ✗ {Fore.WHITE}{token} - {profile}{Fore.RED} [LOCKED]" + Fore.WHITE)
            removeToken(token, file)
            return False

        if len(boost_data.json()) != 0 and boost_data.status_code == 200 or boost_data.status_code == 201:
            if boost_data.json()[0]['cooldown_ends_at'] != None:
                print(Fore.RED + f" ✗ {Fore.WHITE}{token} - {profile}{Fore.RED} [USED]" + Fore.WHITE)
                removeToken(token, file)
                return False

        if len(boost_data.json()) == 0 and boost_data.status_code == 200 or boost_data.status_code == 201:
            print(f"{Fore.RED} ✗ {Fore.WHITE}{token} - {profile}{Fore.RED} [NO NITRO]" + Fore.WHITE)
            removeToken(token, file)
            return False

        else:
            if len(boost_data.json()) != 0 and boost_data.status_code == 200 or boost_data.status_code == 201:
                if boost_data.json()[0]['cooldown_ends_at'] == None:
                    print(f"{Fore.GREEN} ✓ {Fore.WHITE}{token} - {profile}{Fore.GREEN} [WORKING]" + Fore.WHITE)
                    return True

    else:
        print(Fore.RED + f" ✗ {Fore.WHITE}{token}{Fore.RED} [INVALID]" + Fore.WHITE)
        removeToken(token, file)
        return False
    
def get_headers(token):
    while True:
        s = httpx.Client()
        dcf, sdc = get_cookies(s, "https://discord.com/")
        fingerprint = get_fingerprint(s)
        if fingerprint != "Error":
            break
    super_properties = get_super_properties()
    headers = {
        'authority': 'discord.com',
        'method': 'POST',
        'path': '/api/v9/users/@me/channels',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'en-US',
        'authorization': token,
        'cookie': f'__dcfduid={dcf}; __sdcfduid={sdc}',
        'origin': 'https://discord.com',
        'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
        'x-debug-options': 'bugReporterEnabled',
        'x-fingerprint': fingerprint,
        'x-super-properties': super_properties,
    }
    return s, headers

def get_cookies(s, url):
    try:
        cookieinfo = s.get(url, timeout=5).cookies
        dcf = str(cookieinfo).split('__dcfduid=')[1].split(' ')[0]
        sdc = str(cookieinfo).split('__sdcfduid=')[1].split(' ')[0]
        return dcf, sdc
    except:
        return "", ""
    
def printwatermark():
        print(Fore.MAGENTA + f'''

 █████╗ ██╗   ██╗██╗    ██╗██╗███████╗   ''' + Fore.LIGHTMAGENTA_EX + ''' ██████╗  ██████╗  ██████╗ ███████╗████████╗    ████████╗ ██████╗  ██████╗ ██╗     ██╗
██╔══██╗██║   ██║██║    ██║██║██╔════╝    ██╔══██╗██╔═══██╗██╔═══██╗██╔════╝╚══██╔══╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██║
███████║██║   ██║██║ █╗ ██║██║███████╗    ██████╔╝██║   ██║██║   ██║███████╗''' + Fore.MAGENTA +'''    ██║          ██║   ██║   ██║██║   ██║██║     ██║
██╔══██║██║   ██║██║███╗██║██║╚════██║    ''' + Fore.LIGHTMAGENTA_EX + ''' ██╔══██╗██║   ██║██║   ██║╚════██║   ██║          ██║   ██║   ██║██║   ██║██║     ╚═╝
██║  ██║╚██████╔╝╚███╔███╔╝██║███████║    ██████╔╝╚██████╔╝╚██████╔╝███████║   ██║          ██║   ╚██████╔╝╚██████╔╝███████╗██╗
╚═╝  ╚═╝ ╚═════╝  ╚══╝╚══╝ ╚═╝╚══════╝    ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝ ''' + Fore.MAGENTA + '''  ╚═╝          ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚═╝
    discord.gg/omari
    https://github.com/auwii
    made by conspiracy#0002/conspiracy#0001                                                                                                           
    ''')
        

if __name__ == '__main__':
    
    cls()
    cls()
    colorama.init()
    
    mainmenu()
