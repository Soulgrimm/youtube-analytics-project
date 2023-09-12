import os
import datetime
import isodate
from googleapiclient.discovery import build


class PlayList:

    def __init__(self, playlist_id):
        self.__playlist_id = playlist_id

        playlist = self.get_service().playlistItems().list(playlistId=self.__playlist_id,
                                                           part='contentDetails,snippet',
                                                           maxResults=50,
                                                           ).execute()
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist['items']]
        self.title: str = playlist['items'][0]['snippet']['title'][:-13]
        self.url: str = 'https://www.youtube.com/playlist?list=' + self.__playlist_id

    @property
    def playlist_id(self):
        return self.__playlist_id

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('YT_API_KEY')

        return build('youtube', 'v3', developerKey=api_key)

    def print_info(self):
        print(self.get_service().playlistItems().list(playlistId=self.__playlist_id,
                                                      part='snippet,contentDetails',
                                                      maxResults=50,
                                                      ).execute())

    @property
    def total_duration(self):
        video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                          id=','.join(self.video_ids)
                                                          ).execute()

        duration_videos = datetime.timedelta(0)

        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            duration_videos += duration

        return duration_videos

    def show_best_video(self):
        video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                          id=','.join(self.video_ids)
                                                          ).execute()

        most_like_video_id = ''
        count_likes = 0

        for video in video_response['items']:
            if int(video['statistics']['likeCount']) > count_likes:
                most_like_video_id = video['id']
                count_likes = int(video['statistics']['likeCount'])
            continue

        return f'https://youtu.be/{most_like_video_id}'
