from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas
import csv

# Define API key and YouTube channel ID
API_KEY = "#####################################"
CHANNEL_ID = "UC-CSyyi47VX1lD9zyeABW3w"  # Dhruv Rathee's channel ID


def get_video_details():
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    try:
        # Retrieve the playlist ID of the uploaded videos for the channel
        channels_response = youtube.channels().list(
            part='contentDetails',
            id=CHANNEL_ID
        ).execute()

        playlist_id = channels_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        # Retrieve the list of uploaded videos for the channel
        playlist_items = []
        next_page_token = None

        while True:
            playlist_response = youtube.playlistItems().list(
                part='contentDetails',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            playlist_items.extend(playlist_response['items'])
            next_page_token = playlist_response.get('nextPageToken')

            if not next_page_token:
                break

        video_details = []

        # Retrieve details for each video in the playlist
        for item in playlist_items:
            video_id = item['contentDetails']['videoId']
            video_response = youtube.videos().list(
                part='snippet,statistics',
                id=video_id
            ).execute()

            video_snippet = video_response['items'][0]['snippet']
            video_title = video_snippet['title']
            video_tags = video_snippet.get('tags', [])
            video_published_at = video_snippet['publishedAt']

            video_statistics = video_response['items'][0]['statistics']
            video_like_count = video_statistics.get('likeCount', 0)

            # Retrieve comments for the video
            try:
                comments_response = youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    maxResults=100  # Adjust as needed
                ).execute()

                video_comments = []
                for comment in comments_response['items']:
                    comment_snippet = comment['snippet']['topLevelComment']['snippet']
                    comment_text = comment_snippet['textDisplay']
                    comment_like_count = comment_snippet.get('likeCount', 0)
                    video_comments.append({
                        'text': comment_text,
                        'like_count': comment_like_count
                    })

                video_details.append({
                    'title': video_title,
                    'tags': ', '.join(video_tags),
                    'like_count': video_like_count,
                    'total_comment_count': len(video_comments),
                    'published_on': video_published_at,
                    'comments': video_comments
                })
            except HttpError as e:
                error_reason = e._get_reason()
                if 'commentsDisabled' in error_reason:
                    print(f"Comments are disabled for video: {video_id}. Skipping...")
                    continue  # Skip processing this video and move to the next one
                else:
                    print(f"An HTTP error occurred for video {video_id}: {error_reason}")

        return video_details

    except HttpError as e:
        print("An HTTP error occurred:", e)

def write_to_csv(video_details):
    with open('youtube_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['video_title', 'video_tags', 'video_like_count', 'total_comment_count', 'published_on', 'comment_text', 'comment_like_count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for video in video_details:
            for comment in video['comments']:
                writer.writerow({
                    'video_title': video['title'],
                    'video_tags': video['tags'],
                    'video_like_count': video['like_count'],
                    'total_comment_count': video['total_comment_count'],
                    'published_on': video['published_on'],
                    'comment_text': comment['text'],
                    'comment_like_count': comment['like_count']
                })

if __name__ == "__main__":
    videos = get_video_details()
    write_to_csv(videos)
