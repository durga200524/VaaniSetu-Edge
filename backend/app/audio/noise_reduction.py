import io

import numpy as np
import soundfile as sf

from scipy.signal import stft, istft


def reduce_noise(audio_bytes: bytes):

    # Read uploaded WAV audio
    audio, sample_rate = sf.read(
        io.BytesIO(audio_bytes),
        dtype="float32"
    )

    # Convert stereo to mono
    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)

    if len(audio) == 0:
        raise ValueError("Audio file contains no samples.")

    original_length = len(audio)

    # Short-Time Fourier Transform
    frequencies, times, spectrum = stft(
        audio,
        fs=sample_rate,
        nperseg=1024,
        noverlap=768,
        boundary="zeros"
    )

    magnitude = np.abs(spectrum)

    # Estimate background noise from quieter frames
    frame_energy = np.mean(
        magnitude ** 2,
        axis=0
    )

    noise_frame_count = max(
        1,
        int(len(frame_energy) * 0.20)
    )

    quietest_frames = np.argsort(
        frame_energy
    )[:noise_frame_count]

    noise_profile = np.median(
        magnitude[:, quietest_frames],
        axis=1,
        keepdims=True
    )

    # Calculate noise reduction mask
    noise_threshold = 1.5 * noise_profile

    gain = 1.0 - (
        noise_threshold / (magnitude + 1e-8)
    )

    # Preserve a small amount of the original signal
    gain = np.clip(gain, 0.08, 1.0)

    # Apply noise reduction
    cleaned_spectrum = spectrum * gain

    # Convert back to time-domain audio
    _, cleaned_audio = istft(
        cleaned_spectrum,
        fs=sample_rate,
        nperseg=1024,
        noverlap=768,
        input_onesided=True,
        boundary=True
    )

    # Match original audio length
    cleaned_audio = cleaned_audio[:original_length]

    if len(cleaned_audio) < original_length:
        cleaned_audio = np.pad(
            cleaned_audio,
            (0, original_length - len(cleaned_audio))
        )

    # Export processed audio as WAV
    output_buffer = io.BytesIO()

    sf.write(
        output_buffer,
        cleaned_audio,
        sample_rate,
        format="WAV",
        subtype="PCM_16"
    )

    return {
        "processed_audio": output_buffer.getvalue(),
        "sample_rate": sample_rate,
        "duration_seconds": round(
            original_length / sample_rate, 2
        ),
        "message": "Noise reduction completed."
    }