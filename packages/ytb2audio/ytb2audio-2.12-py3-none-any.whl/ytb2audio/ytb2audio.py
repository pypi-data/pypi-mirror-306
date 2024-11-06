import argparse
import asyncio
import pathlib
import ssl
import subprocess
from urllib.parse import urlparse
import requests
from pytube import YouTube
from pytube.extract import video_id

YT_DLP_OPTIONS_DEFAULT = ('--extract-audio --audio-format m4a --audio-quality 48k'
                          ' --embed-thumbnail --console-title --embed-metadata'
                          ' --newline --progress-delta 2 --break-on-existing')


def get_youtube_move_id(url: str):
    try:
        movie_id = video_id(url)
    except Exception as e:
        return None
    return movie_id


async def run_command(cmd):
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    return stdout.decode(), stderr.decode(), process.returncode


async def download_audio(
        movie_id: str,
        data_dir,
        ytdlprewriteoptions: str = YT_DLP_OPTIONS_DEFAULT
):
    data_dir = pathlib.Path(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)

    m4a_file = data_dir.joinpath(f'{movie_id}.m4a')
    if m4a_file.exists():
        print(f'💚 Audio file yet exists: {m4a_file}')
        return m4a_file

    url = f'https://www.youtube.com/watch?v={movie_id}'

    command = f'yt-dlp {ytdlprewriteoptions} --output {m4a_file.as_posix()} {url}'
    print('💙️ The audio download is starting...')
    print('[bash command yt-dlp] ', command)

    stdout, stderr, returncode = await run_command(command)

    for line in stdout:
        print(line, end='')

    for line in stderr:
        print(line, end='')

    return m4a_file


async def download_audio_by_audio_path(
        audio_path: pathlib.Path,
        movie_id: str = '',
        ytdlprewriteoptions: str = YT_DLP_OPTIONS_DEFAULT
):

    m4a_file = pathlib.Path(audio_path)
    if m4a_file.exists():
        print(f'💚 Audio file yet exists: {m4a_file}')
        return m4a_file

    url = f'https://www.youtube.com/watch?v={movie_id}'

    command = f'yt-dlp {ytdlprewriteoptions} --output {m4a_file.as_posix()} {url}'
    print('💙️ The audio download is starting...')
    print('[bash command yt-dlp] ', command)

    stdout, stderr, returncode = await run_command(command)

    for line in stdout:
        print(line, end='')

    for line in stderr:
        print(line, end='')

    return m4a_file


async def download_audio_by_movie_meta(movie_meta: dict):
    print('🍍 Starting downloading audio ... ')
    audio = await download_audio(
        movie_id=movie_meta['id'],
        data_dir=movie_meta['store'],
        ytdlprewriteoptions=movie_meta['ytdlprewriteoptions']
    )
    return pathlib.Path(audio)


async def download_thumbnail(
        movie_id: str,
        data_dir
):
    data_dir = pathlib.Path(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)
    thumbnail = data_dir.joinpath(f'{movie_id}.jpg')

    if thumbnail.exists():
        print(f'💚 Thumbnail file yet exists: {thumbnail}')
        return thumbnail.as_posix()

    # Special SSL setting to make valid HTTP request to Youtube server.
    ssl._create_default_https_context = ssl._create_stdlib_context

    yt = None
    try:
        yt = YouTube.from_id(movie_id)
        print('💙️ The thumbnail download is starting... \n', yt.thumbnail_url)
    except Exception as e:
        print(f"🟥 Error downloading thumbnail [YouTube.from_id(movie_id)]:\n {str(e)}")
        return

    try:
        response = requests.get(yt.thumbnail_url)
        if response.status_code == 200:
            with thumbnail.open('wb') as f:
                f.write(response.content)
        else:
            print(f"🟥 Failed to download image [response = requests.get(yt.thumbnail_url)].")
            print(f"Status code: {response.status_code}")
            return
    except Exception as e:
        print(f"🟥 Failed to download image [response = requests.get(yt.thumbnail_url)]:\n {str(e)}")
        return

    return thumbnail


async def download_thumbnail_by_movie_meta(movie_meta: dict):
    print('🥑 Starting downloading thumbnail ... ')

    data_dir = pathlib.Path(movie_meta['store'])

    data_dir.mkdir(parents=True, exist_ok=True)
    if not movie_meta['id']:
        _err = f'🟠 Thumbnail. No ID in movie meta.'
        print(_err)
        return 'Error'

    thumbnail = data_dir.joinpath(movie_meta['id'] + '.jpg')

    if thumbnail.exists():
        print(f'💚 Thumbnail file yet exists: {thumbnail}')
        return thumbnail

    # Special SSL setting to make valid HTTP request to Youtube server.
    ssl._create_default_https_context = ssl._create_stdlib_context

    try:
        response = requests.get(movie_meta['thumbnail_url'])
        if response.status_code == 200:
            with thumbnail.open('wb') as f:
                f.write(response.content)
        else:
            _err = f'🟠 Thumbnail. Not a 200 valid code. Response code: {response.status_code}.'
            print(_err)
            return 'Error'
    except Exception as e:
        _err = f'🟠 Thumbnail. Failed to download. Exception: {e}.'
        print(_err)
        return 'Error'

    return thumbnail


async def full_download(url, folder, ytdlprewriteoptions):
    context = dict()
    if not urlparse(url).netloc:
        print('⛔️ No URL in your request.')
        return context

    if not (movie_id := get_youtube_move_id(url)):
        print('⛔️ Its not a youtube URL. Check it again.')
        return context

    audio = await download_audio(movie_id, folder, ytdlprewriteoptions)

    if not audio.exists():
        print(f'🟥 Unexpected error. After Check m4a_file.exists.')
        return context

    context['audio'] = audio

    thumbnail = await download_thumbnail(movie_id, folder)
    if thumbnail.exists():
        print(f'🟥 Unexpected error. After Check thumbnail.exists().')
        return context

    context['thumbnail'] = thumbnail

    return context


async def main():
    parser = argparse.ArgumentParser(description='Downloading Youtube audio and its thumbnail')
    parser.add_argument('url', type=str, help='Youtube URL with movie_id.')
    parser.add_argument('--folder', type=str,
                        help='Path to folder to save outputs. '
                             'Default is \".\"', default='.')
    parser.add_argument('--ytdlprewriteoptions', type=str,
                        help=f'Set no a default YT_DPL options in quotes. '
                             f'Default value is \"{YT_DLP_OPTIONS_DEFAULT}\". '
                             f'See full options https://github.com/yt-dlp/yt-dlp.',
                        default=f'{YT_DLP_OPTIONS_DEFAULT}')
    args = parser.parse_args()

    results = await full_download(args.url, args.folder, args.ytdlprewriteoptions)
    if audio := results.get('audio'):
        print(audio)
    if thumbnail := results.get('thumbnail'):
        print(thumbnail)


if __name__ == "__main__":
    asyncio.run(main())
