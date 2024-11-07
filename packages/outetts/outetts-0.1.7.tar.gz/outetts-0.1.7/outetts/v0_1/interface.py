from .audio_codec import AudioCodec
from .prompt_processor import PromptProcessor
from .model import HFModel, GGUFModel, GenerationConfig
import torch
import sounddevice as sd
from .alignment import CTCForcedAlignment
import torchaudio
import tempfile
from dataclasses import dataclass
import pickle

@dataclass
class ModelOutput:
    audio: torch.Tensor
    sr: int

    def save(self, path: str):
        torchaudio.save(path, self.audio.cpu(), sample_rate=self.sr, encoding='PCM_S', bits_per_sample=16)

    def play(self):
        sd.play(self.audio[0].cpu().numpy(), self.sr)
        sd.wait()

class InterfaceHF:
    def __init__(
        self,
        model_path: str,
        device: str = None,
        dtype: torch.dtype = None,
        additional_model_config: dict = {}
    ) -> None:
        self.device = torch.device(
            device if device is not None
            else "cuda" if torch.cuda.is_available()
            else "cpu"
        )
        self.audio_codec = AudioCodec(self.device)
        self.prompt_processor = PromptProcessor(model_path)
        self.model = HFModel(model_path, self.device, dtype, additional_model_config)

    def prepare_prompt(self, text: str, speaker: dict = None):
        prompt = self.prompt_processor.get_completion_prompt(text, speaker)
        return self.prompt_processor.tokenizer.encode(
            prompt, add_special_tokens=False, return_tensors="pt").to(self.model.device)

    def get_audio(self, tokens):
        output = self.prompt_processor.extract_audio_from_tokens(tokens)
        return self.audio_codec.decode(
            torch.tensor([[output]], dtype=torch.int64).to(self.audio_codec.device)
        )

    def create_speaker(self, audio_path: str, transcript: str):
        ctc = CTCForcedAlignment()
        words = ctc.align(audio_path, transcript)
        ctc.free()

        full_codes = self.audio_codec.encode(
            self.audio_codec.convert_audio_tensor(
                audio=torch.cat([i["audio"] for i in words], dim=1),
                sr=ctc.sample_rate
            ).to(self.audio_codec.device)
        ).tolist()

        data = []
        start = 0
        for i in words:
            end = int(round((i["x1"] / ctc.sample_rate) * 75))
            word_tokens = full_codes[0][0][start:end]
            start = end
            if not word_tokens:
                word_tokens = [1]

            data.append({
                "word": i["word"],
                "duration": round(len(word_tokens) / 75, 2),
                "codes": word_tokens
            })

        return {
            "text": transcript,
            "words": data,
        }

    def save_speaker(self, speaker: dict, path: str):
        with open(path, "wb") as f:
            pickle.dump(speaker, f)

    def load_speaker(self, path: str):
        with open(path, "rb") as f:
            return pickle.load(f)

    def generate(self, text: str, speaker: dict = None, temperature: float = 0.1, repetition_penalty: float = 1.1, max_length: int = 4096) -> ModelOutput:
        input_ids = self.prepare_prompt(text, speaker)
        output = self.model.generate(
            input_ids=input_ids,
            config=GenerationConfig(
                temperature=temperature,
                repetition_penalty=repetition_penalty,
                max_length=max_length
            )
        )
        audio = self.get_audio(output[input_ids.size()[-1]:])
        return ModelOutput(audio, self.audio_codec.sr)

class InterfaceGGUF(InterfaceHF):
    def __init__(
            self,
            model_path: str,
            device: str = None,
            n_gpu_layers: int = 0,
            additional_model_config: dict = {}
    ) -> None:
        self.device = torch.device(
            device if device is not None
            else "cuda" if torch.cuda.is_available()
            else "cpu"
        )
        self.audio_codec = AudioCodec(self.device)
        self.prompt_processor = PromptProcessor("OuteAI/OuteTTS-0.1-350M")
        self.model = GGUFModel(
            model_path=model_path,
            n_gpu_layers=n_gpu_layers,
            additional_model_config=additional_model_config
        )

    def prepare_prompt(self, text: str, speaker: dict = None):
        prompt = self.prompt_processor.get_completion_prompt(text, speaker)
        return self.prompt_processor.tokenizer.encode(
            prompt, add_special_tokens=False)

    def generate(self, text: str, speaker: dict = None, temperature: float = 0.1, repetition_penalty: float = 1.1, max_length: int = 4096) -> ModelOutput:
        output = self.model.generate(
            input_ids=self.prepare_prompt(text, speaker),
            config=GenerationConfig(
                temperature=temperature,
                repetition_penalty=repetition_penalty,
                max_length=max_length
            )
        )
        audio = self.get_audio(output)
        return ModelOutput(audio, self.audio_codec.sr)
