import { useState } from "react";
import {
  Cpu,
  MemoryStick,
  Wifi,
  WifiOff,
  Activity,
  Play,
  Loader2,
  CheckCircle,
  AlertTriangle,
  RefreshCw,
} from "lucide-react";

import {
  simulateEdge,
  type EdgeSimulationResponse,
} from "../api/edge";

import "./EdgeSimulator.css";

function EdgeSimulator() {
  const [ram, setRam] = useState(512);
  const [cpu, setCpu] = useState(2);
  const [latency, setLatency] = useState(100);
  const [bandwidth, setBandwidth] = useState(10);
  const [internet, setInternet] = useState(true);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] =
    useState<EdgeSimulationResponse | null>(null);

  const handleSimulation = async () => {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await simulateEdge({
        available_ram_mb: ram,
        cpu_cores: cpu,
        network_latency_ms: latency,
        bandwidth_mbps: bandwidth,
        internet_available: internet,
      });

      setResult(response);
    } catch (err) {
      console.error("Edge simulation failed:", err);
      setError("Simulation failed. Please check the backend and try again.");
    } finally {
      setLoading(false);
    }
  };

  const resetSimulation = () => {
    setRam(512);
    setCpu(2);
    setLatency(100);
    setBandwidth(10);
    setInternet(true);
    setResult(null);
    setError("");
  };

  const getStatusClass = (status: string) => {
    if (
      status === "NORMAL OPERATION" ||
      status === "SUFFICIENT" ||
      status === "ONLINE" ||
      status === "NORMAL"
    ) {
      return "edge-status-good";
    }

    if (
      status === "SEVERE CONSTRAINTS" ||
      status === "CRITICAL" ||
      status === "OFFLINE" ||
      status === "UNAVAILABLE"
    ) {
      return "edge-status-critical";
    }

    return "edge-status-warning";
  };

  return (
    <div className="edge-page">
      <div className="edge-header">
        <div>
          <span className="edge-eyebrow">
            SOFTWARE-DEFINED EDGE INTELLIGENCE
          </span>

          <h1>Edge Constraint Simulator</h1>

          <p>
            Simulate VaaniSetu Edge under limited device
            resources and network conditions.
          </p>
        </div>

        <div className="edge-header-icon">
          <Cpu size={30} />
        </div>
      </div>

      <div className="edge-simulation-card">
        <div className="edge-card-heading">
          <Activity size={20} />
          <h2>Configure Device Resources</h2>
        </div>

        <div className="edge-input-grid">

          <div className="edge-field">
            <label>
              <MemoryStick size={17} />
              Available RAM (MB)
            </label>

            <input
              type="number"
              min="1"
              value={ram}
              onChange={(e) => setRam(Number(e.target.value))}
            />
          </div>

          <div className="edge-field">
            <label>
              <Cpu size={17} />
              CPU Cores
            </label>

            <input
              type="number"
              min="0.1"
              step="0.1"
              value={cpu}
              onChange={(e) => setCpu(Number(e.target.value))}
            />
          </div>

          <div className="edge-field">
            <label>
              <Activity size={17} />
              Network Latency (ms)
            </label>

            <input
              type="number"
              min="0"
              value={latency}
              onChange={(e) => setLatency(Number(e.target.value))}
            />
          </div>

          <div className="edge-field">
            <label>
              <Wifi size={17} />
              Bandwidth (Mbps)
            </label>

            <input
              type="number"
              min="0"
              step="0.1"
              value={bandwidth}
              onChange={(e) => setBandwidth(Number(e.target.value))}
            />
          </div>

        </div>

        <div className="edge-connectivity">
          <div>
            <strong>Internet Connectivity</strong>
            <span>
              {internet
                ? "Internet connection available"
                : "Simulating offline conditions"}
            </span>
          </div>

          <button
            type="button"
            className={`edge-toggle ${internet ? "enabled" : ""}`}
            onClick={() => setInternet(!internet)}
            aria-label="Toggle internet connectivity"
            aria-pressed={internet}
          >
            <span />
          </button>
        </div>

        <div className="edge-actions">
          <button
            className="edge-run-button"
            onClick={handleSimulation}
            disabled={loading}
          >
            {loading ? (
              <>
                <Loader2 className="edge-loading-icon" size={18} />
                Simulating...
              </>
            ) : (
              <>
                <Play size={18} />
                Run Simulation
              </>
            )}
          </button>

          <button
            className="edge-reset-button"
            onClick={resetSimulation}
            disabled={loading}
          >
            <RefreshCw size={17} />
            Reset
          </button>
        </div>

        {error && (
          <div className="edge-error">
            <AlertTriangle size={18} />
            {error}
          </div>
        )}
      </div>

      {result && (
        <div className="edge-results">

          <div className="edge-result-banner">
            <div>
              <span>OVERALL SIMULATION STATUS</span>
              <h2>{result.overall_status}</h2>
            </div>

            {result.overall_status === "NORMAL OPERATION" ? (
              <CheckCircle size={32} />
            ) : (
              <AlertTriangle size={32} />
            )}
          </div>

          <div className="edge-assessment-card">
            <h3>Resource Assessment</h3>

            <div className="edge-assessment-grid">
              {Object.entries(result.resource_assessment).map(
                ([name, status]) => (
                  <div className="edge-assessment-item" key={name}>
                    <span>
                      {name.replaceAll("_", " ").toUpperCase()}
                    </span>

                    <strong className={getStatusClass(status)}>
                      {status}
                    </strong>
                  </div>
                )
              )}
            </div>
          </div>

          <div className="edge-assessment-card">
            <h3>
              <AlertTriangle size={19} />
              Identified Limitations
            </h3>

            {result.limitations.length > 0 ? (
              <ul>
                {result.limitations.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            ) : (
              <p>No significant limitations identified.</p>
            )}
          </div>

          <div className="edge-assessment-card">
            <h3>
              <CheckCircle size={19} />
              Recommendations
            </h3>

            {result.recommendations.length > 0 ? (
              <ul>
                {result.recommendations.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            ) : (
              <p>Current resource conditions are sufficient.</p>
            )}
          </div>

          <div className="edge-simulation-note">
            <WifiOff size={18} />
            <p>{result.simulation_note}</p>
          </div>

        </div>
      )}
    </div>
  );
}

export default EdgeSimulator;