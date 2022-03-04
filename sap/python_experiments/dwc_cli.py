#%%
import getpass
import os
#import subprocess
from pathlib import Path
import asyncio
import time
from pyppeteer import launch
from dotenv import load_dotenv, find_dotenv
import shlex

#%%
env_file= Path('./sap/python_experiments/.env')
load_dotenv(find_dotenv(env_file))

#%%
class AccessCLI:
    # TODO: Error classes for
    # * wrong command
    # * wrong space name

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
            await page.type('#j_username', self._username)
            await page.type('#j_password', self._password)
            await page.click('#logOnFormSubmit')
        await page.waitForSelector('div.island > h1 + h2', {'visible': True, 'timeout': 10000})
        element = await page.querySelector('h2')
        passcode = await page.evaluate('(element) => element.textContent', element)
        return passcode

    async def exec_raw_dwc_command(self,raw_cmd):
        """
        This executes a raw dwc command

        The command is expanded by the url and passcode
        :param raw_cmd:
        :return:
        """
        print(f'Executing\n$ {raw_cmd!r}\n...')

        passcode = await self._new_passcode()

        cmd = raw_cmd + f' -H {self.dwc_url} -p {passcode}'

        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()

        print(f'...execution finished with {proc.returncode}')
        if stdout:
            print(f'[stdout]\n{stdout.decode()}')
        if stderr:
            print(f'[stderr]\n{stderr}')

        return stdout


#%%