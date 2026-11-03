import api from "./client";

export interface VoiceResponse {
  success: boolean;
  pipeline?: string;

  audio_analysis?: {
    duration_seconds: number;
    sample_rate: number;
    channels: number;
    format: string;
  };

  transcription?: Record<string, unknown>;
  intent_analysis?: Record<string, unknown>;
  ai_response?: Record<string, unknown>;
  speech_output?: Record<string, unknown>;
  resolution_passport?: Record<string, unknown>;

  message?: string;
}

export const processVoice = async (
  file: File,
  language: string
): Promise<VoiceResponse> => {
  const formData = new FormData();

  formData.append("file", file);
  formData.append("language", language);

  const response = await api.post<VoiceResponse>(
    "/api/v1/voice/process",
    formData
  );

  return response.data;
};