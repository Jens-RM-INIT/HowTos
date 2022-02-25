import asyncio
import time

#%%
async def sleep_print(n):
    print(f"Ich warte {n} Sekunden ...")
    await asyncio.sleep(n)
    print(f"... wieder da (nach {n} Sekunden)!")
    return n
#%%
async def programm1():
    await sleep_print(10)
    await sleep_print(5)
    await sleep_print(2)
    await sleep_print(1)
#%%
asyncio.run(programm1())
#%%
async def programm2():
    task1 = asyncio.create_task(sleep_print(10))
    task2 = asyncio.create_task(sleep_print(5))
    task3 = asyncio.create_task(sleep_print(2))
    task4 = asyncio.create_task(sleep_print(1))
    await task1
    await task2
    await task3
    await task4
#%%
st = time.time()
asyncio.run(programm2())
print(f"{time.time()-st}")
#%%
from pyppeteer import launch
#%%
async def tst():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://example.com')
    await page.screenshot({'path':'example.png'})
    await browser.close()
    print('done')
#%%
import getpass
import os
#%%
PREFIX = 'mckinsey-2'
REGION = 'us10'
DWC_URL = 'https://' + PREFIX + '.' + REGION + '.hcs.cloud.sap/'
DWC_PASSCODE_URL = 'https://' + PREFIX + '.authentication.' + REGION + '.hana.ondemand.com/passcode'
SPACE_NAME = 'PAR_MCK_RL'
USERNAME = input('Username: ')
PASSWORD = getpass.getpass('Password: ')
#%%
print(DWC_URL)
print(DWC_PASSCODE_URL)
print(USERNAME)
print(PASSWORD)
#%%
async def open_dwc():
    browser = await launch()
    page = await browser.newPage()
    await page.goto(DWC_PASSCODE_URL)
    await page.waitForSelector('#logOnForm', {'visible': True, 'timeout': 10000})
    await page.screenshot({'path':'01.png'})
    if await page.querySelector('#logOnForm') is not None:
        await page.screenshot({'path': '01.png'})
        await page.type('#j_username', USERNAME)
        await page.type('#j_password', PASSWORD)
        await page.click('#logOnFormSubmit')
    await page.screenshot({'path':'02.png'})
    await page.waitForSelector('div.island > h1 + h2', {'visible': True, 'timeout': 10000})
    await page.screenshot({'path':'03.png'})
    element = await page.querySelector('h2')
    passcode = await page.evaluate('(element) => element.textContent', element)
    return passcode

#%%
PASSCODE=asyncio.run(open_dwc())


#%%
os.popen(f"dwc spaces read -s {SPACE_NAME} -H {DWC_URL} -p {PASSCODE}").readlines()

#%%
async def exec_dwc_command(i_cmd):
    PASSCODE = await open_dwc()
    cmd = f"dwc {i_cmd} -H {DWC_URL} -p {PASSCODE}"
    res = os.popen(cmd).readlines()
    return res

#%%
# Wie funktioniert das mit den "spaces" ?
# Usage: index spaces [options] [command]
# manage and orchestrate spaces
# Options:
#   -H, --host <host>  specifies the url host where the tenant is hosted
#   -h, --help         display help for command
# Commands:
#   create [options]   create or update space details based on an import file
#   read [options]     fetch space details for a specified space
#   delete [options]   delete an existing space
#   help [command]     display help for command
erg = asyncio.run(exec_dwc_command('spaces -h'))
print(''.join(erg))

#%%
# Wie funktioniert das mit den "spaces read" ?
# Usage: index spaces read [options]
# fetch space details for a specified space
# Options:
#   -o, --output <output>            specifies the file to store the output of
#                                    the command
#   -s, --space <space>              space ID
#   -n, --no-space-definition        read space definition (optional)
#   -d, --definitions [definitions]  read definitions (optional)
#   -V, --verbose                    print detailed log information to console
#                                    (optional)
#   -H, --host <host>                specifies the url host where the tenant is
#                                    hosted
#   -p, --passcode <passcode>        passcode for interactive session
#                                    authentication (optional)
#   -h, --help                       display help for command
erg = asyncio.run(exec_dwc_command('spaces read -h'))
print(''.join(erg))

#%%
# Wie funktioniert das mit den "spaces create" ?
# Usage: index spaces create [options]
# create or update space details based on an import file
# Options:
# -f, --filePath <filePath>  specifies the file to use as input for the command
#     -V, --verbose              print detailed log information to console
# (optional)
# -H, --host <host>          specifies the url host where the tenant is hosted
# -p, --passcode <passcode>  passcode for interactive session authentication
# (optional)
# -h, --help                 display help for command
erg = asyncio.run(exec_dwc_command('spaces create -h'))
print(''.join(erg))

#%%
# Wie funktioniert das mit den "spaces delete" ?
# Usage: index spaces delete [options]
# delete an existing space
# Options:
# -F, --force                force the command execution
# -s, --space <space>        space ID
# -V, --verbose              print detailed log information to console
# (optional)
# -H, --host <host>          specifies the url host where the tenant is hosted
# -p, --passcode <passcode>  passcode for interactive session authentication
# (optional)
# -h, --help                 display help for command
erg = asyncio.run(exec_dwc_command('spaces delete -h'))
print(''.join(erg))

