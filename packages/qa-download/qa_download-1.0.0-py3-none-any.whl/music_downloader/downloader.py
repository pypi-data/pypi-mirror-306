import argparse
import os
import re
import shutil
import tempfile
import requests
import yt_dlp
from bs4 import BeautifulSoup
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, USLT, APIC

GENIUS_API_KEY = 'L0BY-i4ZVi0wQ53vlvm2zucqjHTuLbHv--YgjxJoN0spnEIhb5swTr_mWlQ6Ye-F'

def sanitize_filename(filename):
    """Sanitize filename to avoid issues with special characters."""
    return re.sub(r'[\\/:"*?<>|]+', "_", filename)

def search_youtube(song_title):
    """Search for the song on YouTube and return the first video URL."""
    ydl_opts = {'format': 'bestaudio/best'}
    search_url = f"ytsearch:{song_title}"
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(search_url, download=False)
        video_url = result['entries'][0]['webpage_url']
        return video_url

def fetch_genius_metadata(song_title, artist=None):
    """Fetch song metadata, including lyrics and album art, from Genius."""
    headers = {"Authorization": f"Bearer {GENIUS_API_KEY}"}
    params = {"q": f"{song_title} {artist}" if artist else song_title}
    response = requests.get("https://api.genius.com/search", headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data['response']['hits']:
            song_data = data['response']['hits'][0]['result']
            title_with_featured = song_data.get("title_with_featured")
            title = song_data.get("title")
            full_title = song_data.get("full_title")
            
            official_title = title_with_featured or title or full_title
            song_url = song_data['url']
            song_art_url = song_data['song_art_image_url']
            primary_artist = song_data['primary_artist']['name']
            release_date = song_data.get('release_date_for_display')
            lyrics = scrape_lyrics_from_url(song_url)
            
            return {
                "title": official_title,
                "artist": primary_artist,
                "album": "Single",
                "release_date": release_date,
                "song_art_url": song_art_url,
                "lyrics": lyrics
            }
    print("No metadata found for this song on Genius.")
    return None

def scrape_lyrics_from_url(url):
    """Scrape lyrics directly from the Genius song page using the data-lyrics-container attribute."""
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        lyrics_divs = soup.find_all('div', {'data-lyrics-container': 'true'})
        
        # Collect all text within these divs, handling line breaks
        lyrics = "\n".join(div.get_text(separator='\n') for div in lyrics_divs)
        if(lyrics):
            print(lyrics)
        return lyrics if lyrics else None
    return None


def embed_metadata(file_path, metadata):
    """Embed metadata including title, artist, album, artwork, and lyrics into the MP3 file."""
    if metadata is None:
        print("No metadata to embed.")
        return
    
    # Embed title, artist, and album info
    audio = EasyID3(file_path)
    audio['title'] = metadata.get('title', 'Unknown Title')
    audio['artist'] = metadata.get('artist', 'Unknown Artist')
    audio['album'] = metadata.get('album', 'Unknown Album')
    audio.save()

    # Embed lyrics if available
    if metadata.get('lyrics'):
        audio = ID3(file_path)
        audio["USLT::'eng'"] = USLT(encoding=3, lang='eng', desc='', text=metadata['lyrics'])
        audio.save()
        print("Lyrics embedded in the MP3 file.")
    
    # Embed artwork if available
    if metadata.get('song_art_url'):
        try:
            art_response = requests.get(metadata['song_art_url'])
            art_response.raise_for_status()
            audio = ID3(file_path)
            audio["APIC::'Cover'"] = APIC(
                encoding=3,
                mime='image/jpeg',
                type=3,
                desc='Cover',
                data=art_response.content
            )
            audio.save()
            print("Artwork embedded in the MP3 file.")
        except Exception as e:
            print(f"Failed to embed artwork: {e}")
    else:
        print("No artwork found to embed.")


def download_audio(video_url, output_dir, metadata):
    """Download audio from YouTube, convert it to MP3, and embed metadata."""
    official_title = sanitize_filename(metadata['title'])
    with tempfile.TemporaryDirectory() as temp_dir:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(temp_dir, official_title + '.%(ext)s'),
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192'
                }
            ],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(video_url, download=True)
            downloaded_file = os.path.join(temp_dir, f"{official_title}.mp3")
            final_file = os.path.join(output_dir, f"{official_title}.mp3")
            
            embed_metadata(downloaded_file, metadata)
            shutil.move(downloaded_file, final_file)
            print(f"Downloaded and saved '{official_title}' to {output_dir}")

def main(song_name, output_dir):
    """Main function to search, download, and process song metadata."""
    output_dir = os.path.expanduser(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # Fetch Genius metadata
    metadata = fetch_genius_metadata(song_name)
    
    if metadata:
        # Search YouTube using the official title from Genius metadata
        video_url = search_youtube(metadata['title'])
        download_audio(video_url, output_dir, metadata)
        print("All downloads and metadata processing completed.")
    else:
        print("Song metadata not found on Genius; download aborted.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download music and fetch metadata from Genius.")
    parser.add_argument("song_name", help="The name of the song to search and download")
    parser.add_argument("--output_dir", help="Directory to save the downloaded audio", default="~/Music/Music/Media.localized/Automatically Add to Music.localized")
    
    args = parser.parse_args()
    main(args.song_name, args.output_dir)
