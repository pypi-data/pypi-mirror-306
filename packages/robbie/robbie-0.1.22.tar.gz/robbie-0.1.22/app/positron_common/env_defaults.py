from typing import Dict
from dataclasses import dataclass
from .build_env import build_env, EnvType
from positron_common.cli.logging_config import logger
from positron_common.cli.console import console

@dataclass
class EnvDefaults():
  name: str
  portal_base: str
  api_base: str
  ws_base: str
  auth0_domain: str
  auth0_audience: str
  auth0_client_id: str

  def dump(self):
    console.print(f"EnvDefaults: {self.name}")
    console.print(f"  portal_base: {self.portal_base}")
    console.print(f"  api_base: {self.api_base}")
    console.print(f"  ws_base: {self.ws_base}")
    console.print(f"  auth0_domain: {self.auth0_domain}")
    console.print(f"  auth0_audience: {self.auth0_audience}")
    console.print(f"  auth0_client_id: {self.auth0_client_id}")
    

env_config: Dict[EnvType, EnvDefaults] = {
  EnvType.LOCAL: EnvDefaults(
    name='local',
    portal_base='http://localhost:3000',
    api_base='http://localhost:3002/api',
    ws_base='ws://localhost:3002',
    auth0_domain='dev-k1t01pbanrr04itm.us.auth0.com',
    auth0_client_id='Mr3GW8Ub4e2bLaEvZ5o0XK5pGfEhtH3d',
    auth0_audience='https://localhost/positron/api',
  ),
  EnvType.DEV: EnvDefaults(
    name='dev',
    portal_base='https://dev.positronsupercompute.com',
    api_base='https://dev.positronsupercompute.com/api',
    ws_base='wss://dev.positronsupercompute.com',
    auth0_domain='dev-k1t01pbanrr04itm.us.auth0.com',
    auth0_client_id='Mr3GW8Ub4e2bLaEvZ5o0XK5pGfEhtH3d',
    auth0_audience='https://localhost/positron/api',
  ),
  EnvType.ALPHA: EnvDefaults(
    name='alpha',
    portal_base='https://alpha.positronsupercompute.com',
    api_base='https://alpha.positronsupercompute.com/api',
    ws_base='wss://alpha.positronsupercompute.com',
    auth0_domain='dev-k1t01pbanrr04itm.us.auth0.com',
    auth0_client_id='Mr3GW8Ub4e2bLaEvZ5o0XK5pGfEhtH3d',
    auth0_audience='https://localhost/positron/api',
  ),
  EnvType.BETA: EnvDefaults(
    name='beta',
    portal_base='https://beta.positronsupercompute.com',
    api_base='https://beta.positronsupercompute.com/api',
    ws_base='wss://beta.positronsupercompute.com',
    auth0_domain='positron-beta.us.auth0.com',
    auth0_client_id='ZW0vio95rYfbHrN7kE3PoUXwmPloBw7e',
    auth0_audience='https://beta/positron/api',
  ),
}



current = env_config[EnvType.DEV]
# current = env_config[EnvType.LOCAL]

# Set current based on build
if build_env:
  current = env_config[build_env]
  logger.debug(f'Using build environment: "{build_env.value}" backend url: "{current.api_base}"')
