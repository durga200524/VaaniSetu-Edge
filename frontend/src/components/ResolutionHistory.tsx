import { useEffect, useState } from "react";
import {
  History,
  RefreshCw,
  FileText,
  CheckCircle,
  Clock,
  AlertCircle,
} from "lucide-react";

import {
  getAllPassports,
  type ResolutionPassport,
} from "../api/resolution";

import "./ResolutionHistory.css";

function ResolutionHistory() {
  const [passports, setPassports] = useState<ResolutionPassport[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchPassports = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await getAllPassports();
      setPassports(response.passports ?? []);
    } catch (err) {
      console.error("Failed to fetch resolution history:", err);
      setError("Unable to load Resolution History. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPassports();
  }, []);

  const formatDate = (timestamp: string) => {
    if (!timestamp) return "Date unavailable";

    const date = new Date(timestamp);

    if (Number.isNaN(date.getTime())) return timestamp;

    return date.toLocaleString();
  };

  return (
    <div className="resolution-page">
      <div className="resolution-header">
        <div>
          <span className="resolution-eyebrow">
            CUSTOMER INTERACTION RECORDS
          </span>

          <h1>Resolution History</h1>

          <p>
            View customer conversations and their completed AI resolutions.
          </p>
        </div>

        <button
          className="resolution-refresh-button"
          onClick={fetchPassports}
          disabled={loading}
        >
          <RefreshCw size={17} />
          Refresh
        </button>
      </div>

      <div className="resolution-summary">
        <div className="resolution-summary-icon">
          <History size={23} />
        </div>

        <div>
          <span>Total Resolution Passports</span>
          <h2>{passports.length}</h2>
        </div>
      </div>

      {loading && (
        <div className="resolution-message">
          <RefreshCw size={20} className="resolution-loading-icon" />
          Loading resolution records...
        </div>
      )}

      {error && (
        <div className="resolution-error">
          <AlertCircle size={19} />
          {error}
        </div>
      )}

      {!loading && !error && passports.length === 0 && (
        <div className="resolution-empty">
          <FileText size={42} />

          <h3>No Resolution Passports Found</h3>

          <p>
            Process a customer voice message to create your first
            Resolution Passport.
          </p>
        </div>
      )}

      {!loading && !error && passports.length > 0 && (
        <div className="resolution-records">
          {passports.map((passport) => (
            <div
              className="resolution-record-card"
              key={passport.passport_id}
            >
              <div className="resolution-record-top">
                <div className="resolution-record-icon">
                  <FileText size={21} />
                </div>

                <div className="resolution-record-info">
                  <h3>
                    {passport.intent_analysis?.intent ?? "Customer Interaction"}
                  </h3>

                  <span>
                    ID: {passport.passport_id}
                  </span>
                </div>

                <div className="resolution-status">
                  <CheckCircle size={15} />
                  {passport.processing?.status ?? "UNKNOWN"}
                </div>
              </div>

              <div className="resolution-record-details">
                <div>
                  <span>Customer Transcript</span>
                  <p>
                    {passport.customer_interaction?.transcript ??
                      "Transcript unavailable"}
                  </p>
                </div>

                <div>
                  <span>AI Generated Response</span>
                  <p>
                    {passport.ai_resolution?.response ??
                      "AI response unavailable"}
                  </p>
                </div>
              </div>

              <div className="resolution-record-footer">
                <span>
                  <Clock size={15} />
                  {formatDate(passport.timestamp)}
                </span>

                <span>
                  Language:{" "}
                  {passport.customer_interaction?.language ?? "N/A"}
                </span>

                <span>
                  Model: {passport.ai_resolution?.model ?? "N/A"}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default ResolutionHistory;