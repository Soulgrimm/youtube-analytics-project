import os

from googleapiclient.discovery import build


class Video:
    def __init__(self, video_id):
        try:
            self.__video_id = video_id

            video = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                     id=self.__video_id
                                                     ).execute()

            # self.id_video: str = video['items'][0]['id']
            self.title: str = video['items'][0]['snippet']['title']
            self.url = 'https://www.youtube.com/watch/' + self.__video_id
            self.view_count: int = int(video['items'][0]['statistics']['viewCount'])
            self.like_count: int = int(video['items'][0]['statistics']['likeCount'])

        except IndexError:
            print('Передан некорректный ID')

            self.title = None
            self.like_count = None
            self.url = None
            self.view_count = None

    @property
    def video_id(self):
        return self.__video_id

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('YT_API_KEY')

        return build('youtube', 'v3', developerKey=api_key)

    def __str__(self):
        return f'{self.title}'

    def print_info(self):
        print(self.get_service().videos().list(id=self.video_id, part='snippet,statistics').execute())


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.__playlist_id = playlist_id

        playlist_videos = self.get_service().playlistItems().list(playlistId=self.__playlist_id,
                                                                  part='contentDetails',
                                                                  maxResults=50,
                                                                  ).execute()
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
