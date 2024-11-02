"""HttpX + beautifulSOUP

Various convenient features related to httpx and BeautifulSoup.

██╗░░██╗██╗░░██╗░██████╗░█████╗░██╗░░░██╗██████╗░
██║░░██║╚██╗██╔╝██╔════╝██╔══██╗██║░░░██║██╔══██╗
███████║░╚███╔╝░╚█████╗░██║░░██║██║░░░██║██████╔╝
██╔══██║░██╔██╗░░╚═══██╗██║░░██║██║░░░██║██╔═══╝░
██║░░██║██╔╝╚██╗██████╔╝╚█████╔╝╚██████╔╝██║░░░░░
╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░░╚════╝░░╚═════╝░╚═╝░░░░░
"""

__title__ = "hxsoup"
__description__ = "Various convenient features related to httpx and BeautifulSoup."
__url__ = "https://github.com/ilotoki0804/WebtoonScraper"
__version__ = "0.6.0"
__author__ = "ilotoki0804"
__author_email__ = "ilotoki0804@gmail.com"
__license__ = "MIT License"

__github_user_name__ = __author__
__github_project_name__ = __title__

from .api import delete, get, head, options, patch, post, put, request, stream
from .broadcast_list import BroadcastList
from .client import DEV_DEFAULT_TIMEOUT_CONFIG, DEV_HEADERS, AsyncClient, Client
from .options import ClientOptions, MutableClientOptions
from .souptools import (
    NotEmptySoupedResponse,
    NotEmptySoupTools,
    Parsers,
    SoupedResponse,
    SoupTools,
)
from .utils import clean_headers, freeze_dict_and_list
