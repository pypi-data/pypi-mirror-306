import logging
from urllib.parse import urlparse

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from libman.mixins.account import AccountMixin
from libman.mixins.album import DownloadAlbumMixin, UploadAlbumMixin
from libman.mixins.auth import LoginMixin
from libman.mixins.bloks import BloksMixin
from libman.mixins.challenge import ChallengeResolveMixin
from libman.mixins.clip import DownloadClipMixin, UploadClipMixin
from libman.mixins.collection import CollectionMixin
from libman.mixins.comment import CommentMixin
from libman.mixins.direct import DirectMixin
from libman.mixins.explore import ExploreMixin
from libman.mixins.fbsearch import FbSearchMixin
from libman.mixins.fundraiser import FundraiserMixin
from libman.mixins.hashtag import HashtagMixin
from libman.mixins.highlight import HighlightMixin
from libman.mixins.igtv import DownloadIGTVMixin, UploadIGTVMixin
from libman.mixins.insights import InsightsMixin
from libman.mixins.location import LocationMixin
from libman.mixins.media import MediaMixin
from libman.mixins.multiple_accounts import MultipleAccountsMixin
from libman.mixins.note import NoteMixin
from libman.mixins.notification import NotificationMixin
from libman.mixins.password import PasswordMixin
from libman.mixins.photo import DownloadPhotoMixin, UploadPhotoMixin
from libman.mixins.private import PrivateRequestMixin
from libman.mixins.public import (
    ProfilePublicMixin,
    PublicRequestMixin,
    TopSearchesPublicMixin,
)
from libman.mixins.share import ShareMixin
from libman.mixins.signup import SignUpMixin
from libman.mixins.story import StoryMixin
from libman.mixins.timeline import ReelsMixin
from libman.mixins.totp import TOTPMixin
from libman.mixins.track import TrackMixin
from libman.mixins.user import UserMixin
from libman.mixins.video import DownloadVideoMixin, UploadVideoMixin

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Used as fallback logger if another is not provided.
DEFAULT_LOGGER = logging.getLogger("libman")


class Client(
    PublicRequestMixin,
    ChallengeResolveMixin,
    PrivateRequestMixin,
    TopSearchesPublicMixin,
    ProfilePublicMixin,
    LoginMixin,
    ShareMixin,
    TrackMixin,
    FbSearchMixin,
    HighlightMixin,
    DownloadPhotoMixin,
    UploadPhotoMixin,
    DownloadVideoMixin,
    UploadVideoMixin,
    DownloadAlbumMixin,
    NotificationMixin,
    UploadAlbumMixin,
    DownloadIGTVMixin,
    UploadIGTVMixin,
    MediaMixin,
    UserMixin,
    InsightsMixin,
    CollectionMixin,
    AccountMixin,
    DirectMixin,
    LocationMixin,
    HashtagMixin,
    CommentMixin,
    StoryMixin,
    PasswordMixin,
    SignUpMixin,
    DownloadClipMixin,
    UploadClipMixin,
    ReelsMixin,
    ExploreMixin,
    BloksMixin,
    TOTPMixin,
    MultipleAccountsMixin,
    NoteMixin,
    FundraiserMixin,
):
    proxy = None

    def __init__(
        self,
        settings: dict = {},
        proxy: str = None,
        delay_range: list = None,
        logger=DEFAULT_LOGGER,
        **kwargs,
    ):

        super().__init__(**kwargs)

        self.settings = settings
        self.logger = logger
        self.delay_range = delay_range

        self.set_proxy(proxy)

        self.init()

    def set_proxy(self, dsn: str):
        if dsn:
            assert isinstance(
                dsn, str
            ), f'Proxy must been string (URL), but now "{dsn}" ({type(dsn)})'
            self.proxy = dsn
            proxy_href = "{scheme}{href}".format(
                scheme="http://" if not urlparse(self.proxy).scheme else "",
                href=self.proxy,
            )
            self.public.proxies = self.private.proxies = {
                "http": proxy_href,
                "https": proxy_href,
            }
            return True
        self.public.proxies = self.private.proxies = {}
        return False
