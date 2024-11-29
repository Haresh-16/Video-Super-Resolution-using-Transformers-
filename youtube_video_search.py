# Combined code to search YouTube and download videos
from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL
import os
import ssl
import urllib.request

# Fix SSL issues
ssl._create_default_https_context = ssl._create_unverified_context

def search_youtube(query, max_results=5):
    results = YoutubeSearch(query, max_results=max_results).to_dict()
    return results

def download_video(video_url):
    opts = {
        #'format': 'bestvideo+bestaudio/best',  # Download video in the best available resolution
        'outtmpl': r'D:\UW_courses\EE P 596 CV\Project\youtube_video_dataset\%(title)s_%(height)sp.%(ext)s'  # Append resolution value in the video file name
    }
    with YoutubeDL(opts) as yt:
        yt.download([video_url])
    print(f"Downloaded video: {video_url}")

if __name__ == "__main__":
    search_query = "old tamil movie songs black and white" #input("Enter search string for YouTube: ")
    num_videos = 5 #int(input("Enter number of videos to download: "))
    
    results = search_youtube(search_query, max_results=num_videos * 2)  # Increase results to filter by duration
    
    if len(results) == 0:
        print("No results found.")
    else:
        downloaded_count = 0
        for idx, video in enumerate(results):
            if downloaded_count >= num_videos:
                break
            
            video_duration = video['duration']
            duration_parts = list(map(int, video_duration.split(':')))
            if len(duration_parts) == 3:
                hours, minutes, seconds = duration_parts
                total_seconds = hours * 3600 + minutes * 60 + seconds
            elif len(duration_parts) == 2:
                minutes, seconds = duration_parts
                total_seconds = minutes * 60 + seconds
            else:
                total_seconds = int(duration_parts[0])
            
            if total_seconds <= 300:
                video_url = f"https://www.youtube.com{video['url_suffix']}"
                print(f"Downloading video [{downloaded_count+1}/{num_videos}]: {video['title']}")
                download_video(video_url)
                downloaded_count += 1
        
        print(f"Total number of suitable videos downloaded: {downloaded_count}")
