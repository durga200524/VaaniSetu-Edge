import io

import numpy as np
import soundfile as sf


def analyze_audio(audio_bytes: bytes):

    # Read audio from uploaded bytes
    audio, sample_rate = sf.read(
        io.BytesIO(audio_bytes),
        dtype="float32"
    )

    # Convert stereo audio into mono
    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)

    if len(audio) == 0:
        raise ValueError("Audio file contains no samples.")

    # Calculate duration
    duration = len(audio) / sample_rate

    # Calculate RMS volume
    rms = float(
        np.sqrt(np.mean(np.square(audio)))
    )

    # Calculate peak amplitude
    peak = float(
        np.max(np.abs(audio))
    )

    # Calculate clipping percentage
    clipping_percentage = float(
        np.mean(np.abs(audio) >= 0.99) * 100
    )

    # Calculate silence percentage
    silence_threshold = 0.01

    silence_percentage = float(
        np.mean(np.abs(audio) < silence_threshold) * 100
    )

    # Calculate volume in decibels
    volume_dbfs = float(
        20 * np.log10(max(rms, 1e-10))
    )

    # Classify audio quality
    if rms < 0.01:
        quality = "Very Low Volume"

    elif clipping_percentage > 1:
        quality = "Clipping Detected"

    elif silence_percentage > 70:
        quality = "High Silence"

    else:
        quality = "Normal Audio"

    return {
        "duration_seconds": round(duration, 2),
        "sample_rate": int(sample_rate),
        "channels": 1,
        "rms_volume": round(rms, 4),
        "volume_dbfs": round(volume_dbfs, 2),
        "peak_amplitude": round(peak, 4),
        "clipping_percentage": round(clipping_percentage, 2),
        "silence_percentage": round(silence_percentage, 2),
        "audio_quality": quality
    }