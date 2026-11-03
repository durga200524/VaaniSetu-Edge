import io

import numpy as np
import soundfile as sf


def load_audio(audio_bytes: bytes):

    audio, sample_rate = sf.read(
        io.BytesIO(audio_bytes),
        dtype="float32"
    )

    # Convert stereo to mono
    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)

    if len(audio) == 0:
        raise ValueError("Audio contains no samples.")

    return audio, sample_rate


def calculate_rms(audio):

    return float(
        np.sqrt(np.mean(np.square(audio)))
    )


def calculate_dbfs(rms):

    return float(
        20 * np.log10(max(rms, 1e-10))
    )


def compare_audio(
    original_audio_bytes: bytes,
    processed_audio_bytes: bytes
):

    # Load original audio
    original, original_rate = load_audio(
        original_audio_bytes
    )

    # Load processed audio
    processed, processed_rate = load_audio(
        processed_audio_bytes
    )

    if original_rate != processed_rate:
        raise ValueError(
            "Both audio files must have the same sample rate."
        )

    # Match lengths for comparison
    min_length = min(
        len(original),
        len(processed)
    )

    original = original[:min_length]
    processed = processed[:min_length]

    # Calculate RMS
    original_rms = calculate_rms(original)
    processed_rms = calculate_rms(processed)

    # Calculate dBFS
    original_dbfs = calculate_dbfs(original_rms)
    processed_dbfs = calculate_dbfs(processed_rms)

    # Calculate peak amplitude
    original_peak = float(
        np.max(np.abs(original))
    )

    processed_peak = float(
        np.max(np.abs(processed))
    )

    # Estimate residual signal
    residual = original - processed

    residual_rms = calculate_rms(residual)

    # Estimate SNR using the processed signal
    # and the difference between original and processed audio.
    estimated_snr_db = float(
        20 * np.log10(
            max(processed_rms, 1e-10)
            / max(residual_rms, 1e-10)
        )
    )

    # Calculate RMS change
    rms_change_percentage = float(
        (
            (processed_rms - original_rms)
            / max(original_rms, 1e-10)
        ) * 100
    )

    return {
        "original_audio": {
            "rms": round(original_rms, 5),
            "dbfs": round(original_dbfs, 2),
            "peak_amplitude": round(original_peak, 5)
        },

        "processed_audio": {
            "rms": round(processed_rms, 5),
            "dbfs": round(processed_dbfs, 2),
            "peak_amplitude": round(processed_peak, 5)
        },

        "comparison": {
            "rms_change_percentage": round(
                rms_change_percentage, 2
            ),
            "residual_rms": round(
                residual_rms, 5
            ),
            "estimated_snr_db": round(
                estimated_snr_db, 2
            ),
            "snr_method": (
                "Estimated signal-to-residual ratio; "
                "not ground-truth SNR."
            )
        }
    }