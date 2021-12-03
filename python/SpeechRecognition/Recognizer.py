# coding:utf-8
from aip import AipSpeech
import speech_recognition as sr
from vosk import Model, KaldiRecognizer,SetLogLevel
import logging,Utils,json
"""
实时语音识别测试
"""

class Recognizer:
    mode = Utils.get_conf('BASE','mode')
    def __init__(self) -> None:
        pass
    def recognize(self,audio):
        pass

class BaiduRr(Recognizer):
    APP_ID = Utils.get_conf('BAIDU','APP_ID')
    API_KEY = Utils.get_conf('BAIDU','API_KEY')
    SECRET_KEY = Utils.get_conf('BAIDU','SECRET_KEY')

    def __init__(self) -> None:
        super().__init__()

    def recognize(self,audio):
        client = AipSpeech(self.APP_ID,self.API_KEY,self.SECRET_KEY)
        res = client.asr(audio.get_raw_data(16000),'pcm',16000,{'lan':'zh'})
        text = ''
        try:
            text = res['result'][0]
            logging.debug(text)
        except Exception as e:
            text = ''
            logging.error(f'baidu Rr error:{e}')
        return text

class VoskRr(Recognizer):
    model = Utils.get_conf('VOSK','model')
    def __init__(self,model_path) -> None:
        super().__init__()
        self.model = Model(f'./model/{model_path}')
        self.rec = KaldiRecognizer(self.model,16000)
        self.rec.SetMaxAlternatives(10)
        self.rec.SetWords(True)
    
    def recognize(self, audio):
        res = ''
        try:
            wave_data = audio.get_wav_data()
            if self.rec.AcceptWaveform(wave_data):
                # res = json.loads(self.rec.Result())
                res = ''
            else:
                res = json.loads(self.rec.PartialResult())
                res = res['partial']
            # print(json.loads(self.rec.FinalResult()))
        except Exception as e:
            logging.error(f'vosk error: {e}')
            res = ''
        # TODO
        return res

def recognize(audio,mode):
    r = sr.Recognizer()

    rec = None

    if mode == 'google':
        res = r.recognize_google_cloud(audio, language='cmn-Hans-CN', show_all=True)
    elif mode == 'baidu':
        rec = BaiduRr()
    elif mode == 'local':
        res = r.recognize_sphinx(audio,language='zh-cn')
    elif mode == 'vosk':
        rec = VoskRr(VoskRr.model)
        pass

    return rec.recognize(audio)

def listen_once(mode,thread):
    r = sr.Recognizer()
    # 麦克风
    mic = sr.Microphone(sample_rate=16000)

    logging.info(f'录音线程启动，id={int(thread.currentThreadId())}')
    while True:
        try:
            with mic as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source,timeout=int(Utils.get_conf('BASE','listen_once_timeout')))
        except sr.WaitTimeoutError:
            if thread.running is False:
                break
            logging.info('暂时没有听到任何声音')
            continue
        else:
            break

    # 提前返回，避免次数浪费
    if thread.running is False:
        return ''

    logging.info('识别中')

    return recognize(audio,Recognizer.mode)
