import asyncio
import io
import aiohttp
from discord import VoiceClient, FFmpegPCMAudio, FFmpegOpusAudio
from discord.ext import commands

from utils.logger import logger
from utils.config import get_config
from utils.path import path


api_url = get_config("server", "gpt_sovits")

async def speech(bot: commands.Bot, text: str):  # TODO: refactor
    if not bot.voice_clients:
        logger.warning("The bot not in voice channel, speech passed")
        return
    vc: VoiceClient = bot.voice_clients[0]
    if not vc.is_connected():
        logger.warning("voice channel disconnected")
        return
    
    data = {
        "text": text,                 # str.(required) text to be synthesized
        "text_lang": "zh",            # str.(required) language of the text to be synthesized
        "ref_audio_path": get_config("voice", "ref_audio_path"),  # str.(required) reference audio path
        "prompt_text": "私人文字頻道加上私人語音頻道",            # str.(optional) prompt text for the reference audio
        "prompt_lang": "zh",            # str.(required) language of the prompt text for the reference audio
        "top_k": 5,                   # int. top k sampling
        "top_p": 1,                   # float. top p sampling
        "temperature": 1,             # float. temperature for sampling
        "text_split_method": "cut5",  # str. text split method, see text_segmentation_method.py for details.
        "batch_size": 1,              # int. batch size for inference
        "batch_threshold": 0.75,      # float. threshold for batch splitting.
        "split_bucket": True,         # bool. whether to split the batch into multiple buckets.
        "speed_factor": 1,            # float. control the speed of the synthesized audio.
        "fragment_interval":0.3,      # float. to control the interval of the audio fragment.
        "seed": -1,                   # int. random seed for reproducibility.
        "media_type": "wav",          # str. media type of the output audio, support "wav", "raw", "ogg", "aac".
        "streaming_mode": False,      # bool. whether to return a streaming response.
        "parallel_infer": True,       # bool.(optional) whether to use parallel inference.
        "repetition_penalty": 1.35    # float.(optional) repetition penalty for T2S model.
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url=api_url, json=data) as resp:
            logger.info(resp)
            if resp.status != 200:
                logger.error("Failed to get audio from GPT-SoVITS API")
                return
            # FFMPEG_OPTIONS = {
            #     'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            #     'options': '-vn'
            # }
            if data["streaming_mode"]:
                # async for chunk in resp.content.iter_chunked(1024):
                #     if chunk:
                #         vc.play(FFmpegPCMAudio(str(chunk)))
                #         while vc.is_playing():
                #             await asyncio.sleep(1)
                pass
            else:
                with open(path("output", "speech.wav"), "wb") as audio:
                    audio.write(await resp.content.read())

                with open(path("output", "speech.wav"), "rb") as audio:
                    vc.play(FFmpegOpusAudio(
                        io.BytesIO(audio.read()),
                        pipe=True,
                        # **FFMPEG_OPTIONS,  # not work
                    ))
                    while vc.is_playing():
                        await asyncio.sleep(1)