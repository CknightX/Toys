# coding:utf-8
from aip import AipSpeech
import speech_recognition as sr
import logging,Utils

APP_ID = Utils.get_conf('BAIDU','APP_ID')
API_KEY = Utils.get_conf('BAIDU','API_KEY')
SECRET_KEY = Utils.get_conf('BAIDU','SECRET_KEY')
"""
实时语音识别测试
"""

def recognize(audio,mode):
    res = None
    r = sr.Recognizer()
    if mode == 'google':
        res = r.recognize_google_cloud(audio, language='cmn-Hans-CN', show_all=True)
    elif mode == 'baidu':
        client = AipSpeech(APP_ID,API_KEY,SECRET_KEY)
        res = client.asr(audio.get_raw_data(16000),'pcm',16000,{'lan':'zh'})
    elif mode == 'local':
        res = r.recognize_sphinx(audio,language='zh-cn')
    return res

def listen_once(mode,window):
    r = sr.Recognizer()
    # 麦克风
    mic = sr.Microphone(sample_rate=16000)

    logging.info('录音中')
    while True:
        try:
            with mic as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source,timeout=int(Utils.get_conf('BASE','listen_once_timeout')))
        except sr.WaitTimeoutError:
            logging.info('暂时没有听到任何声音')
            if window.listening is False:
                break
            continue
        else:
            break

    # 提前返回，避免次数浪费
    if window.listening is False:
        return ''

    logging.info('识别中')


    try:
        res = recognize(audio,mode)
        text = res['result'][0]
        logging.debug(text)
    except Exception as e:
        logging.error(e)
        return ''
    else:
        return text