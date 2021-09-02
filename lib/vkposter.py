import requests
import vk
from settings import Settings
import datetime
from lib.abstract_file_loader import AbstractFileLoader


class VKPoster:

    def __init__(self):
        s = Settings()
        self.access_token = s.get('ACCESS_TOKEN')
        self.posting_time = s.get('POSTING_TIME')
        self.group_id = int(s.get('GROUP_ID'))
        self.version_api = s.get('API_VERSION')
        self.session = vk.Session(access_token=self.access_token)
        self.api = vk.API(self.session)
        self.next_post_time = datetime.datetime.now()
        self.upload_url = ''
        self.postponed_timestamps = []
        self.__init_post_time()
        self.__init_upload_url()

    def __init_post_time(self):
        posting_time = self.posting_time.split(':')
        now = datetime.datetime.now()
        self.next_post_time = datetime.datetime(now.year, now.month, now.day, int(posting_time[0]), int(posting_time[1]))
        if self.next_post_time < now:
            self.set_next_day_post()

    def __init_upload_url(self):
        self.upload_url = self.api.photos.getWallUploadServer(v=self.version_api, group_id=self.group_id)['upload_url']

    def set_next_day_post(self):
        self.next_post_time += datetime.timedelta(days=1)
        if self.next_post_time.weekday() is 6:
            self.next_post_time += datetime.timedelta(days=1)

    def get_postponed_posts(self):
        postponed_posts = self.api.wall.get(v=self.version_api, owner_id=-self.group_id, filter='postponed', count=100)['items']
        for post in postponed_posts:
            self.postponed_timestamps.append(int(post['date']))
        self.postponed_timestamps.sort()

    def set_available_post_time(self):
        if not self.postponed_timestamps:
            self.get_postponed_posts()
        while self.next_post_time.timestamp() in self.postponed_timestamps:
            self.set_next_day_post()

    def post(self, file_path, file_type='photo', message=''):
        self.set_available_post_time()
        files = {'photo': open(file_path, 'rb')}
        upload_result = requests.post(self.upload_url, files=files).json()
        uploaded_photo = self.api.photos.saveWallPhoto(
            v=self.version_api,
            hash=upload_result['hash'],
            group_id=self.group_id,
            server=upload_result['server'],
            photo=upload_result[file_type])
        attachment = '{}{}_{}'.format(file_type, uploaded_photo[0]['owner_id'], uploaded_photo[0]['id'])
        post_result = self.api.wall.post(
            v=self.version_api,
            owner_id=-self.group_id,
            message=message,
            from_group=1,
            attachments=attachment,
            publish_date=int(self.next_post_time.timestamp()))
        self.postponed_timestamps.append(self.next_post_time.timestamp())
        self.set_next_day_post()

        return post_result

    def post_batch(self, file_loader: AbstractFileLoader, file_type='photo'):
        posted_ids = []
        files_to_post = file_loader.get_files()
        for file_name, file_path in files_to_post.items():
            posted_ids.append(self.post(file_path, file_type))
            file_loader.move_to_posted(file_name)
        return posted_ids

