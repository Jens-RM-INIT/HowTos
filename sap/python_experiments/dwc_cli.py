#%%
import getpass
import os
from pathlib import Path
env_file= Path('./sap/python_experiments/.env')
from dotenv import load_dotenv, find_dotenv
#%%
import asyncio
import time
from pyppeteer import launch
#%%
load_dotenv(find_dotenv(env_file))

#%%
class AccessCLI:

    def __init__(self):
        # For the moment.
        # TODO: Correct this
        if (username:=os.environ.get('DWC_USERNAME')) is None:
            self._username = input('Please enter your DWC-Username')
        else:
            self._username = username
        if (password:=os.environ.get('DWC_PASSWORD')) is None:
            self._password = getpass('Password')
        else:
            self._password = password

    @property
    def dwc_url(self):
        if hasattr(self, '_dwc_url'):
            return self._dwc_url
        else:
            if (prefix := os.environ.get('DWC_PREFIX')) is None:
                prefix = input('Please enter DWC-Prefix (e.g. "mycompany-1")')
            if (region := os.environ.get('DWC_REGION')) is None:
                region = input('Please enter DWC-Region (e.g. "us10")')
            self._dwc_url = 'https://' + prefix + '.' + region + '.hcs.cloud.sap/'
            return self._dwc_url

    @property
    def dwc_passcode_url(self):
        if hasattr(self, '_dwc_passcode_url'):
            return self._dwc_passcode_url
        else:
            if (prefix := os.environ.get('DWC_PREFIX')) is None:
                prefix = input('Please enter DWC-Prefix (e.g. "mycompany-1")')
            if (region := os.environ.get('DWC_REGION')) is None:
                region = input('Please enter DWC-Region (e.g. "us10")')
            self._dwc_passcode_url = 'https://' + prefix + '.authentication.' + region + '.hana.ondemand.com/passcode'
            return self._dwc_passcode_url

    async def _new_passcode(self):
        browser = await launch()
        page = await browser.newPage()
        await page.goto(self.dwc_passcode_url)
        await page.waitForSelector('#logOnForm', {'visible': True, 'timeout': 10000})
        if await page.querySelector('#logOnForm') is not None:
            await page.screenshot({'path': '01.png'})
            await page.type('#j_username', self._username)
            await page.type('#j_password', self._password)
            await page.click('#logOnFormSubmit')
        await page.waitForSelector('div.island > h1 + h2', {'visible': True, 'timeout': 10000})
        element = await page.querySelector('h2')
        passcode = await page.evaluate('(element) => element.textContent', element)
        return passcode

    def exec_raw_dwc_command(self,raw_cmd):
        """
        This executes a raw dwc command

        The command is expanded by the url and passcode
        :param raw_cmd:
        :return:
        """
        print('Start execution')
        passcode = asyncio.run(self._new_passcode())
        cmd = raw_cmd + f' -H {self.dwc_url} -p {passcode}'
        dwc_res = os.popen(cmd)
        print('... execution finished')
        return dwc_res


#%%

#def exec_sys_cmd(cmd):
#    res = os.popen(cmd).readlines()
#    return res
#
#async def exec_dwc_command(i_cmd, outfile=None):
#    loop = asyncio.get_event_loop()
#    PASSCODE = await open_dwc()
#    cmd = f"dwc {i_cmd} -H {DWC_URL} -p {PASSCODE}"
#    if isinstance(outfile,str):
#        cmd = cmd + f" -o {outfile}"
#        await loop.run_in_executor(None, exec_sys_cmd, cmd)
#    else:
#        res = await loop.run_in_executor(None, exec_sys_cmd, cmd)
#        return res
#    return




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
#   -n, --no-space-definition        read space definition (optional) (-n bedeutet, sie wird NICHT gelesen)
#   -d, --definitions [definitions]  read definitions (optional) (-d bedeutet, sie WIRD gelesen)
#   -V, --verbose                    print detailed log information to console
#                                    (optional)
#   -H, --host <host>                specifies the url host where the tenant is
#                                    hosted
#   -p, --passcode <passcode>        passcode for interactive session
#                                    authentication (optional)
#   -h, --help                       display help for command
#
#   ohne -d bekomme ich nur die "Space-Definition:
#           Meta Informationen, Benutzer,...
#
#   mit -n wird die "space-definition" nicht mit heruntergeladen
erg = asyncio.run(exec_dwc_command('spaces read -h'))
print(''.join(erg))

#%%
erg = asyncio.run(exec_dwc_command('spaces read -s PAR_MCK_UL -d'))
#%%
print(''.join(erg))
#%%
with open('testoutput_UL.json','w') as f_out:
    f_out.writelines(erg)
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

#%%
# Auslesen eines spaces
asyncio.run(exec_dwc_command('spaces read -s MCK_UL', 'barespace.json'))

#%%
# Auslesen der Entitäten eines spaces
asyncio.run(exec_dwc_command('spaces read -s PAR_MCK_UL -n -d', 'space_entities.json'))

#%%

#%%
def get_space_def(space_name):
