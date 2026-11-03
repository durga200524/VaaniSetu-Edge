import { useState, type ChangeEvent } from "react";
import {
  Upload,
  Mic,
  Loader2,
  FileAudio,
  Languages,
  CheckCircle,
  AlertCircle,
  Activity,
  Volume2,
  AudioLines,
  Download,
  GitCompare,
  ShieldCheck,
} from "lucide-react";

import { processVoice, type VoiceResponse } from "../api/voice";
import api from "../api/client";

import "./VoiceAssistant.css";

type AudioAnalysis = {
  duration_seconds?: number;
  sample_rate?: number;
  channels?: number;
  rms_volume?: number;
  volume_dbfs?: number;
  peak_amplitude?: number;
  clipping_percentage?: number;
  silence_percentage?: number;
  audio_quality?: string;
};

type AudioAnalysisResponse = {
  success: boolean;
  message?: string;
  analysis?: AudioAnalysis;
};

type AudioComparisonResponse = {
  success: boolean;
  message?: string;
  duration_seconds?: number;
  comparison?: {
    original_audio?: {
      rms?: number;
      dbfs?: number;
      peak_amplitude?: number;
    };
    processed_audio?: {
      rms?: number;
      dbfs?: number;
      peak_amplitude?: number;
    };
    comparison?: {
      rms_change_percentage?: number;
      residual_rms?: number;
      estimated_snr_db?: number;
      snr_method?: string;
    };
  };
};

type TranscriptionComparisonResponse = {
  success: boolean;
  message?: string;
  duration_seconds?: number;
  noise_reduction?: string;
  transcription_comparison?: {
    success?: boolean;
    model?: string;
    language?: string;
    original_transcription?: {
      transcript?: string;
      request_id?: string;
    };
    processed_transcription?: {
      transcript?: string;
      request_id?: string;
    };
    comparison?: {
      similarity_percentage?: number;
      original_word_count?: number;
      processed_word_count?: number;
      transcripts_match?: boolean;
    };
    evaluation_note?: string;
  };
};

function VoiceAssistant() {
  const [file, setFile] = useState<File | null>(null);
  const [language, setLanguage] = useState("te-IN");

  const [loading, setLoading] = useState(false);
  const [analysisLoading, setAnalysisLoading] = useState(false);
  const [noiseLoading, setNoiseLoading] = useState(false);
  const [comparisonLoading, setComparisonLoading] = useState(false);

  const [result, setResult] = useState<VoiceResponse | null>(null);

  const [audioAnalysis, setAudioAnalysis] =
    useState<AudioAnalysisResponse | null>(null);

  const [audioComparison, setAudioComparison] =
    useState<AudioComparisonResponse | null>(null);

  const [transcriptionComparison, setTranscriptionComparison] =
    useState<TranscriptionComparisonResponse | null>(null);

  const [cleanedAudioUrl, setCleanedAudioUrl] = useState("");

  const [error, setError] = useState("");
  const [audioToolError, setAudioToolError] = useState("");

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];

    if (!selectedFile) return;

    const allowedTypes = [
      "audio/mpeg",
      "audio/wav",
      "audio/x-wav",
      "audio/mp4",
      "video/mp4",
      "audio/ogg",
      "audio/webm",
    ];

    const validExtension = /\.(mp3|wav|mp4|m4a|ogg|webm)$/i.test(
      selectedFile.name
    );

    if (!validExtension && !allowedTypes.includes(selectedFile.type)) {
      setError("Please select a supported audio file.");
      setFile(null);
      return;
    }

    setFile(selectedFile);

    setResult(null);
    setAudioAnalysis(null);
    setAudioComparison(null);
    setTranscriptionComparison(null);

    if (cleanedAudioUrl) {
      URL.revokeObjectURL(cleanedAudioUrl);
      setCleanedAudioUrl("");
    }

    setError("");
    setAudioToolError("");
  };

  const createAudioFormData = () => {
    const formData = new FormData();
    formData.append("audio", file!);
    return formData;
  };

  // Main voice processing pipeline
  const handleProcessVoice = async () => {
    if (!file) {
      setError("Please upload an audio file first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await processVoice(file, language);
      setResult(response);
    } catch (err) {
      console.error("Voice processing failed:", err);

      setError(
        "Voice processing failed. Please check the backend and try again."
      );
    } finally {
      setLoading(false);
    }
  };

  // Audio quality analysis
  const handleAnalyzeAudio = async () => {
    if (!file) return;

    setAnalysisLoading(true);
    setAudioToolError("");
    setAudioAnalysis(null);

    try {
      const response = await api.post<AudioAnalysisResponse>(
        "/api/v1/audio/analyze",
        createAudioFormData()
      );

      setAudioAnalysis(response.data);
    } catch (err) {
      console.error("Audio analysis failed:", err);
      setAudioToolError(
        "Audio analysis failed. Please check the backend."
      );
    } finally {
      setAnalysisLoading(false);
    }
  };

  // Noise reduction and cleaned audio download
  const handleNoiseReduction = async () => {
    if (!file) return;

    setNoiseLoading(true);
    setAudioToolError("");

    try {
      const response = await api.post(
        "/api/v1/audio/reduce-noise",
        createAudioFormData(),
        {
          responseType: "blob",
        }
      );

      if (cleanedAudioUrl) {
        URL.revokeObjectURL(cleanedAudioUrl);
      }

      const audioBlob = new Blob([response.data], {
        type: "audio/wav",
      });

      const audioUrl = URL.createObjectURL(audioBlob);

      setCleanedAudioUrl(audioUrl);
    } catch (err) {
      console.error("Noise reduction failed:", err);
      setAudioToolError(
        "Noise reduction failed. Please check the backend."
      );
    } finally {
      setNoiseLoading(false);
    }
  };

  // Compare original and noise-reduced audio transcriptions
  const handleCompareTranscriptions = async () => {
    if (!file) return;

    setComparisonLoading(true);
    setAudioToolError("");

    setAudioComparison(null);
    setTranscriptionComparison(null);

    try {
      const audioResponse = await api.post<AudioComparisonResponse>(
        "/api/v1/audio/compare",
        createAudioFormData()
      );

      setAudioComparison(audioResponse.data);

      const formData = createAudioFormData();
      formData.append("language", language);

      const transcriptionResponse =
        await api.post<TranscriptionComparisonResponse>(
          "/api/v1/audio/compare-transcriptions",
          formData
        );

      setTranscriptionComparison(transcriptionResponse.data);
    } catch (err) {
      console.error("Audio comparison failed:", err);

      setAudioToolError(
        "Comparison failed. Please check the backend and try again."
      );
    } finally {
      setComparisonLoading(false);
    }
  };

  const transcription = result?.transcription as
    | Record<string, unknown>
    | undefined;

  const intent = result?.intent_analysis as
    | Record<string, unknown>
    | undefined;

  const answer = result?.ai_response as
    | Record<string, unknown>
    | undefined;

  const speech = result?.speech_output as
    | Record<string, unknown>
    | undefined;

  const passport = result?.resolution_passport as
    | Record<string, unknown>
    | undefined;

  const audioBase64 =
    typeof speech?.audio_base64 === "string"
      ? speech.audio_base64
      : typeof speech?.audio === "string"
        ? speech.audio
        : "";

  const audioSource = audioBase64
    ? `data:audio/wav;base64,${audioBase64}`
    : "";

  const analysis = audioAnalysis?.analysis;

  const noiseMetrics = audioComparison?.comparison?.comparison;

  const transcriptMetrics =
    transcriptionComparison?.transcription_comparison;

  return (
    <div className="voice-assistant-page">

      {/* Page Header */}

      <div className="voice-page-header">
        <div>
          <span className="voice-eyebrow">
            MULTILINGUAL AI PLATFORM
          </span>

          <h1>Voice Assistant</h1>

          <p>
            Upload customer audio and let VaaniSetu Edge
            understand, respond and generate speech.
          </p>
        </div>

        <div className="voice-header-icon">
          <Mic size={32} />
        </div>
      </div>

      {/* Audio Upload */}

      <div className="voice-upload-card">
        <div className="voice-card-heading">
          <Upload size={20} />
          <h2>Upload Customer Audio</h2>
        </div>

        <label className="voice-upload-area">
          <input
            type="file"
            accept=".mp3,.wav,.mp4,.m4a,.ogg,.webm,audio/*,video/mp4"
            onChange={handleFileChange}
          />

          <FileAudio size={38} />

          <strong>
            {file ? file.name : "Choose an audio file"}
          </strong>

          <span>
            {file
              ? `${(file.size / (1024 * 1024)).toFixed(2)} MB`
              : "MP3, WAV, MP4, M4A, OGG or WEBM"}
          </span>

          <span className="upload-button-text">
            Browse Files
          </span>
        </label>

        <div className="voice-language-field">
          <label htmlFor="voice-language">
            <Languages size={17} />
            Select Language
          </label>

          <select
            id="voice-language"
            value={language}
            onChange={(event) => setLanguage(event.target.value)}
          >
            <option value="en-IN">English</option>
            <option value="hi-IN">Hindi</option>
            <option value="te-IN">Telugu</option>
          </select>
        </div>

        {error && (
          <div className="voice-error">
            <AlertCircle size={18} />
            {error}
          </div>
        )}

        <button
          className="process-voice-button"
          onClick={handleProcessVoice}
          disabled={!file || loading}
        >
          {loading ? (
            <>
              <Loader2 className="loading-icon" size={19} />
              Processing Audio...
            </>
          ) : (
            <>
              <Mic size={19} />
              Process Voice
            </>
          )}
        </button>
      </div>

      {/* Noise Resilience Tools */}

      <div className="voice-upload-card noise-tools-card">

        <div className="voice-card-heading">
          <ShieldCheck size={20} />
          <h2>Noise-Resilient Audio Intelligence</h2>
        </div>

        <p>
          Analyze audio quality, reduce background noise and
          evaluate speech recognition before and after processing.
        </p>

        <div className="noise-tool-buttons">

          <button
            className="process-voice-button"
            onClick={handleAnalyzeAudio}
            disabled={!file || analysisLoading}
          >
            {analysisLoading ? (
              <>
                <Loader2 className="loading-icon" size={18} />
                Analyzing...
              </>
            ) : (
              <>
                <Activity size={18} />
                Analyze Audio Quality
              </>
            )}
          </button>

          <button
            className="process-voice-button"
            onClick={handleNoiseReduction}
            disabled={!file || noiseLoading}
          >
            {noiseLoading ? (
              <>
                <Loader2 className="loading-icon" size={18} />
                Reducing Noise...
              </>
            ) : (
              <>
                <Volume2 size={18} />
                Reduce Noise
              </>
            )}
          </button>

          <button
            className="process-voice-button"
            onClick={handleCompareTranscriptions}
            disabled={!file || comparisonLoading}
          >
            {comparisonLoading ? (
              <>
                <Loader2 className="loading-icon" size={18} />
                Comparing...
              </>
            ) : (
              <>
                <GitCompare size={18} />
                Compare Transcriptions
              </>
            )}
          </button>

        </div>

        {audioToolError && (
          <div className="voice-error">
            <AlertCircle size={18} />
            {audioToolError}
          </div>
        )}

      </div>

      {/* Audio Quality Results */}

      {analysis && (
        <div className="voice-result-card">

          <h3>
            <Activity size={18} />
            Audio Quality Analysis
          </h3>

          <div className="noise-metrics-grid">

            <div className="noise-metric">
              <span>Duration</span>
              <strong>
                {analysis.duration_seconds?.toFixed(2) ?? "N/A"} sec
              </strong>
            </div>

            <div className="noise-metric">
              <span>Sample Rate</span>
              <strong>
                {analysis.sample_rate ?? "N/A"} Hz
              </strong>
            </div>

            <div className="noise-metric">
              <span>Channels</span>
              <strong>
                {analysis.channels ?? "N/A"}
              </strong>
            </div>

            <div className="noise-metric">
              <span>RMS Volume</span>
              <strong>
                {analysis.rms_volume?.toFixed(4) ?? "N/A"}
              </strong>
            </div>

            <div className="noise-metric">
              <span>Volume Level</span>
              <strong>
                {analysis.volume_dbfs?.toFixed(2) ?? "N/A"} dBFS
              </strong>
            </div>

            <div className="noise-metric">
              <span>Peak Amplitude</span>
              <strong>
                {analysis.peak_amplitude?.toFixed(4) ?? "N/A"}
              </strong>
            </div>

            <div className="noise-metric">
              <span>Clipping</span>
              <strong>
                {analysis.clipping_percentage?.toFixed(2) ?? "N/A"}%
              </strong>
            </div>

            <div className="noise-metric">
              <span>Silence</span>
              <strong>
                {analysis.silence_percentage?.toFixed(2) ?? "N/A"}%
              </strong>
            </div>

          </div>

          <div className="voice-success">
            <CheckCircle size={18} />
            Audio Quality: {analysis.audio_quality ?? "Analyzed"}
          </div>

        </div>
      )}

      {/* Cleaned Audio */}

      {cleanedAudioUrl && (
        <div className="voice-result-card">

          <h3>
            <AudioLines size={18} />
            Noise-Reduced Audio
          </h3>

          <audio controls src={cleanedAudioUrl}>
            Your browser does not support audio playback.
          </audio>

          <a
            href={cleanedAudioUrl}
            download="vaanisetu_cleaned_audio.wav"
            className="process-voice-button download-audio-button"
          >
            <Download size={18} />
            Download Cleaned Audio
          </a>

        </div>
      )}

      {/* Audio Comparison Results */}

      {noiseMetrics && (
        <div className="voice-result-card">

          <h3>
            <GitCompare size={18} />
            Original vs Noise-Reduced Audio
          </h3>

          <div className="noise-comparison-grid">

            <div className="noise-comparison-column">
              <h4>Original Audio</h4>

              <p>
                RMS:{" "}
                {audioComparison?.comparison?.original_audio?.rms?.toFixed(5) ?? "N/A"}
              </p>

              <p>
                dBFS:{" "}
                {audioComparison?.comparison?.original_audio?.dbfs?.toFixed(2) ?? "N/A"}
              </p>

              <p>
                Peak:{" "}
                {audioComparison?.comparison?.original_audio?.peak_amplitude?.toFixed(5) ?? "N/A"}
              </p>
            </div>

            <div className="noise-comparison-column">
              <h4>Processed Audio</h4>

              <p>
                RMS:{" "}
                {audioComparison?.comparison?.processed_audio?.rms?.toFixed(5) ?? "N/A"}
              </p>

              <p>
                dBFS:{" "}
                {audioComparison?.comparison?.processed_audio?.dbfs?.toFixed(2) ?? "N/A"}
              </p>

              <p>
                Peak:{" "}
                {audioComparison?.comparison?.processed_audio?.peak_amplitude?.toFixed(5) ?? "N/A"}
              </p>
            </div>

          </div>

          <div className="noise-metrics-grid">

            <div className="noise-metric">
              <span>RMS Change</span>
              <strong>
                {noiseMetrics.rms_change_percentage?.toFixed(2) ?? "N/A"}%
              </strong>
            </div>

            <div className="noise-metric">
              <span>Residual RMS</span>
              <strong>
                {noiseMetrics.residual_rms?.toFixed(5) ?? "N/A"}
              </strong>
            </div>

            <div className="noise-metric">
              <span>Estimated SNR</span>
              <strong>
                {noiseMetrics.estimated_snr_db?.toFixed(2) ?? "N/A"} dB
              </strong>
            </div>

          </div>

          <p className="noise-note">
            Method: {noiseMetrics.snr_method ?? "Backend estimation"}.
            Estimated SNR is a signal-to-residual measure, not a
            verified measurement of true environmental SNR improvement.
          </p>

        </div>
      )}

      {/* Transcription Comparison */}

      {transcriptMetrics && (
        <div className="voice-result-card">

          <h3>
            <GitCompare size={18} />
            Speech Recognition Comparison
          </h3>

          <div className="noise-comparison-column">
            <h4>Original Transcription</h4>

            <p>
              {transcriptMetrics.original_transcription?.transcript ??
                "No transcription returned."}
            </p>
          </div>

          <div className="noise-comparison-column">
            <h4>Noise-Reduced Transcription</h4>

            <p>
              {transcriptMetrics.processed_transcription?.transcript ??
                "No transcription returned."}
            </p>
          </div>

          <div className="noise-metrics-grid">

            <div className="noise-metric">
              <span>Transcript Similarity</span>
              <strong>
                {transcriptMetrics.comparison?.similarity_percentage ?? "N/A"}%
              </strong>
            </div>

            <div className="noise-metric">
              <span>Original Word Count</span>
              <strong>
                {transcriptMetrics.comparison?.original_word_count ?? "N/A"}
              </strong>
            </div>

            <div className="noise-metric">
              <span>Processed Word Count</span>
              <strong>
                {transcriptMetrics.comparison?.processed_word_count ?? "N/A"}
              </strong>
            </div>

          </div>

          <div className="voice-success">
            <CheckCircle size={18} />
            Transcripts Match:{" "}
            {transcriptMetrics.comparison?.transcripts_match
              ? "Yes"
              : "No"}
          </div>

          <p className="noise-note">
            Model: {transcriptMetrics.model ?? "Gnani Prisma v2.5"}
          </p>

          {transcriptMetrics.evaluation_note && (
            <p className="noise-note">
              {transcriptMetrics.evaluation_note}
            </p>
          )}

        </div>
      )}

      {/* Main Voice Pipeline Results */}

      {result && (
        <div className="voice-results">

          <div className="voice-success">
            <CheckCircle size={20} />
            Voice processing completed successfully.
          </div>

          <div className="voice-result-card">
            <h3>Speech Transcription</h3>

            <p>
              {String(
                transcription?.text ?? "No transcription returned."
              )}
            </p>

            <span>
              Language: {String(transcription?.language ?? language)}
            </span>
          </div>

          <div className="voice-result-card">
            <h3>Detected Customer Intent</h3>

            <p>
              {String(intent?.intent ?? "Not available")}
            </p>

            <span>
              Confidence: {String(intent?.confidence ?? "N/A")}%
            </span>
          </div>

          <div className="voice-result-card">
            <h3>AI Generated Answer</h3>

            <p>
              {String(answer?.text ?? "No answer returned.")}
            </p>

            <span>
              Model: {String(answer?.model ?? "Not available")}
            </span>
          </div>

          <div className="voice-result-card">
            <h3>Generated Speech</h3>

            {audioSource ? (
              <audio controls src={audioSource}>
                Your browser does not support audio playback.
              </audio>
            ) : (
              <p>
                Audio data was not found in the API response.
              </p>
            )}

            <span>
              Voice: {String(speech?.voice ?? "Not available")}
            </span>
          </div>

          <div className="voice-result-card passport-card">
            <h3>Resolution Passport</h3>

            <p>
              Passport ID:{" "}
              {String(passport?.passport_id ?? "Not available")}
            </p>

            <span>
              Status: {String(passport?.status ?? "Not available")}
            </span>
          </div>

        </div>
      )}

    </div>
  );
}

export default VoiceAssistant;