import os
import pathlib

import azure.cognitiveservices.speech as speechsdk

import split_book

from pydub import AudioSegment
from datetime import datetime
from pathlib import Path

template = '''
    <speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts"
       xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US">
    <mstts:backgroundaudio src="https://bgm5.b-cdn.net/kongbubgm.mp3" volume="0.2"/>
    <voice name="zh-CN-YunyeNeural">
        <prosody rate="-12%" pitch="0%">{}</prosody>
    </voice>
</speak>
    '''


def maketts(index, p, file_folder):
    print(p)
    text = template.format(p)

    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription='602d8f7790a8439abef08adc079a6926',
                                           region='koreacentral')
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True,
                                                     filename="./{}/{}.wav".format(file_folder, str(index)))

    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name = 'zh-CN-YunyeNeural'

    speech_config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm)

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # Get text from the console and synthesize to the default speaker.

    speech_synthesis_result = speech_synthesizer.speak_ssml(text)

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(p))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")


def merge_mp3(files):
    song = AudioSegment.silent(duration=10)
    for file in sorted(files, reverse=True):
        songclip = AudioSegment.from_wav(file)
        song = songclip + song
    song = AudioSegment.silent(duration=10) + song
    return song


def start(path):
    # split_book.split(path)
    for i, j, k in os.walk(path):
        for chapter in k:
            if not chapter.endswith('txt'):
                continue
            # if "第四十六章" not in chapter:
            #     continue
            file_path = os.path.join(path, chapter)
            file_folder = file_path.strip('.txt')
            if not os.path.exists(file_folder):
                os.makedirs(file_folder)
            else:
                continue
            with open(file_path, 'rb') as f:
                lines = f.readlines()
                # maketts(lines[0])
                # lines.pop(0)
                ttstr = ''
                for index, line in enumerate(lines):
                    if index == len(lines) - 1:
                        if line.decode(encoding='utf-8').strip() != "":
                            ttstr = ttstr + '\n' + "<p>{}</p>".format(line.decode(encoding='utf-8').strip())
                        maketts(index, ttstr, file_folder)
                    elif len(ttstr) > 500:
                        maketts(index, ttstr, file_folder)
                        ttstr = '\n' + "<p>{}</p>".format(line.decode(encoding='utf-8').strip())
                    else:
                        ttstr = ttstr + '\n' + "<p>{}</p>".format(line.decode(encoding='utf-8').strip())

                print("合成结束")
                files = [file for file in Path(file_folder).iterdir() if file.name.endswith(".wav")]
                sound = merge_mp3(files)  # 合并mp3
                [os.remove(file) for file in Path(file_folder).iterdir() if file.name.endswith(".wav")]
                sound.export(f'{os.path.join(file_folder, chapter.strip(".txt"))}.wav',
                             format("wav"))  # 把合并合的mp3进行合成然后重命名。


if __name__ == '__main__':
    start('盗墓笔记2：秦岭神树 作者：南派三叔')
