from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import pprint
import requests

API_KEY = "AIzaSyCVRrhke_FTaC7gtTJdpj-UL4HJPRuRU5g"

# It creates a service object for the YouTube API version 3 with the specified API key.
youtube = build('youtube', 'v3', developerKey=API_KEY)


"""Iterates through the items in the response and extracts relevant information about each channel,
 including the channel ID, title, description, and the latest videos"""
def search_channels(query, max_results=50):
    request = youtube.search().list(
        part="snippet",
        type="channel",
        q=query,
        maxResults=max_results
    )
    response = request.execute()
    channels = []
    i = 0
    for item in response.get('items', []):
        if i > 5:
            break
        i += 1
        channel_id = item['snippet']['channelId']
        channels.append({
            'channelId': channel_id,
            'channelTitle': item['snippet']['channelTitle'],
            'description': item['snippet']['description'],
            'latestVideos': get_latest_videos(channel_id), 
        })
    return channels




# Function to get the latest videos from a channel id given 
def get_latest_videos(channel_id, max_results=2):
    # Get the uploads playlist ID
    channel_response = youtube.channels().list(
        part='contentDetails',
        id=channel_id
    ).execute()
    uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    # Fetch videos from the playlist
    playlist_request = youtube.playlistItems().list(
        part="snippet",
        playlistId=uploads_playlist_id,
        maxResults=max_results
    )
    try:
        playlist_response = playlist_request.execute()
        videos = []
        for item in playlist_response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            videos.append({
                'videoId': video_id,
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'publishedAt': item['snippet']['publishedAt'],
                'transcript': video_transcript(video_id)
            })
        return videos
    except:
        return []



def video_transcript(video_id): 
    video_id = 'video_id'
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        for transcript in transcript_list:
            return transcript['text']
    except Exception as e:
        return f"retrieve transcript for this video is impossible"


def video_transcript_v2(lang, video_id):

    url = f"http://video.google.com/timedtext?lang={lang}&v={video_id}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(response.content)
            return response.text
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Transcript Error: {e}")
        return None


def filter_channels_by_keyword(channels, keyword):
    return [channel for channel in channels if re.search(keyword, channel['description'], re.IGNORECASE)]

def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

def main():
    user_query = input("Enter your query (e.g., 'Attack on Titan latest season'): ")

    # Step 1: Search for channels based on the user's query
    channels = search_channels(user_query)
    
    if not channels:
        print("No channels found. Exiting.")
        return

    # Step 2: Filter channels based on a keyword (e.g., 'anime')
    filtered_channels = filter_channels_by_keyword(channels, 'anime')

    if not filtered_channels:
        print("No anime-related channels found. Exiting.")
        return

    # Step 3: Fetch the latest videos from the filtered channels
    for channel in filtered_channels:
        print(f"\nChannel: {channel['channelTitle']}")
        latest_videos = get_latest_videos(channel['channelId'])

        # Step 4: Display video information and sentiment analysis
        for video in latest_videos:
            print("\nVideo:")
            print(f"Title: {video['title']}")
            print(f"Description: {video['description']}")
            sentiment_score = analyze_sentiment(video['description'])
            print(f"Sentiment Score: {sentiment_score}")

if __name__ == "__main__":
    #main()
    print(video_transcript('W_ba-3tRjSA'))
    #print(video_transcript_v2('en', 'W_ba-3tRjSA'))

"""channels = search_channels('history')
pprint.pprint(channels)"""



