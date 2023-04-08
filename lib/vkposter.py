import random

import requests
import vk
from settings import Settings
import datetime
from lib.abstract_file_loader import AbstractFileLoader


class VKPoster:

    def __init__(self):
        s = Settings()
        self.access_token = s.get('ACCESS_TOKEN')
        self.group_id = int(s.get('GROUP_ID'))
        self.version_api = s.get('API_VERSION')

        self.time_index = 0
        self.posting_time_list = s.get('POSTING_TIME_LIST').split(',')
        if len(self.posting_time_list) == 0:
            raise Exception('Posting time list must contain 1 or more values')
        skip_days = s.get('SKIP_DAYS')
        self.skip_days = [int(day) for day in skip_days.split(',')] if skip_days != "" else []

        self.skip_days.sort()
        if len(self.skip_days) > 6:
            self.skip_days = self.skip_days[0:6]
        self.random_posting = s.get('RANDOM_POSTING')

        self.posting_time_generator = self.get_posting_time_generator()

        self.session = vk.Session(access_token=self.access_token)
        self.api = vk.API(self.session)
        self.next_posting_date = datetime.datetime.now()
        self.upload_url = ''
        self.postponed_timestamps = []
        self.__init_post_time()
        self.__init_upload_url()

    def __init_post_time(self):
        posting_time = next(self.posting_time_generator).split(':')
        now = datetime.datetime.now()
        self.next_posting_date = datetime.datetime(now.year, now.month, now.day, int(posting_time[0]), int(posting_time[1]))
        if self.next_posting_date < now or self.next_posting_date.weekday() in self.skip_days:
            self.set_next_posting_time()

    def __init_upload_url(self):
        self.upload_url = self.api.photos.getWallUploadServer(v=self.version_api, group_id=self.group_id)['upload_url']

    def set_next_posting_time(self):
        next_posting_time = next(self.posting_time_generator).split(':')
        now = datetime.datetime.now()
        self.next_posting_date = self.next_posting_date.replace(hour=int(next_posting_time[0]), minute=int(next_posting_time[1]))
        if self.next_posting_date < now or self.time_index == len(self.posting_time_list) - 1 and self.next_posting_date.timestamp() in self.postponed_timestamps:
            self.next_posting_date += datetime.timedelta(days=1)

        while self.next_posting_date.weekday() in self.skip_days:
            self.next_posting_date += datetime.timedelta(days=1)

    def get_posting_time_generator(self):
        while True:
            if self.time_index > len(self.posting_time_list) - 1:
                self.time_index = 0
            yield self.posting_time_list[self.time_index]
            self.time_index += 1

    def get_postponed_posts(self):
        postponed_posts = self.api.wall.get(v=self.version_api, owner_id=-self.group_id, filter='postponed', count=100)['items']
        for post in postponed_posts:
            self.postponed_timestamps.append(int(post['date']))
        self.postponed_timestamps.sort()

    def set_available_post_time(self):
        if not self.postponed_timestamps:
            self.get_postponed_posts()
        while self.next_posting_date.timestamp() in self.postponed_timestamps:
            self.set_next_posting_time()

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
            publish_date=int(self.next_posting_date.timestamp()))
        self.postponed_timestamps.append(self.next_posting_date.timestamp())
        self.set_next_posting_time()

        return post_result

    def post_batch(self, file_loader: AbstractFileLoader, file_type='photo'):
        posted_ids = []
        files_to_post = file_loader.get_files()
        if self.random_posting:
            files_to_post_keys = list(files_to_post)
            random.shuffle(files_to_post_keys)
            shuffled_files_to_post = {}
            for key in files_to_post_keys:
                shuffled_files_to_post.update({key: files_to_post[key]})
            files_to_post = shuffled_files_to_post

        for file_name, file_path in files_to_post.items():
            posted_ids.append(self.post(file_path, file_type))
            file_loader.move_to_posted(file_name)
        return posted_ids

