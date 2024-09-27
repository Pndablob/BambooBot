FILENAME = "downloaded_audio.webm"

YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'outtmpl': FILENAME,
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
    'force-ipv4': True,
    'cachedir': False,
    # 'socket_timeout': 30,
    # 'source_timeout': 30,
    'verbose': True,  # only used for testing
}

FFMPEG_OPTIONS = {
    # 'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', # Can't use when downloading
    'options': '-vn',
}
