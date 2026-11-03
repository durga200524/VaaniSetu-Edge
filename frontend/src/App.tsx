import { useEffect, useState } from "react";

import {
  LayoutDashboard,
  Mic,
  History,
  Cpu,
  Settings,
  Bell,
  Search,
  ArrowUpRight,
  Activity,
  Languages,
  AudioWaveform,
  ShieldCheck,
  Zap,
  CircleCheck,
  Clock,
  MessageSquare,
  Headphones,
  ChevronRight,
} from "lucide-react";

import { checkBackendHealth } from "./api/health";
import { getAllPassports, type ResolutionPassport } from "./api/resolution";
import VoiceAssistant from "./components/VoiceAssistant";
import ResolutionHistory from "./components/ResolutionHistory";
import EdgeSimulator from "./components/EdgeSimulator";

import "./App.css";

type Page = "dashboard" | "voice" | "history" | "edge";

function App() {
  const [backendOnline, setBackendOnline] = useState(false);
  const [activePage, setActivePage] = useState<Page>("dashboard");
  const [passports, setPassports] = useState<ResolutionPassport[]>([]);
  const [dashboardLoading, setDashboardLoading] = useState(true);

  // Load real dashboard statistics from Resolution Passport records
  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        const result = await getAllPassports();
        setPassports(result.passports || []);
      } catch (error) {
        console.error("Dashboard statistics could not be loaded:", error);
      } finally {
        setDashboardLoading(false);
      }
    };

    loadDashboardData();
    const interval = setInterval(loadDashboardData, 10000);
    return () => clearInterval(interval);
  }, []);

  const completedResolutions = passports.filter(
    (passport) => passport.processing?.status?.toLowerCase() === "completed"
  ).length;

  const latestPassport = [...passports].sort(
    (a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
  )[0];

  // Backend health check
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const result = await checkBackendHealth();
        setBackendOnline(result.status === "healthy");
      } catch (error) {
        console.error("Backend health check failed:", error);
        setBackendOnline(false);
      }
    };

    checkHealth();

    const interval = setInterval(checkHealth, 10000);

    return () => clearInterval(interval);
  }, []);

  const navigationItems = [
    {
      id: "dashboard" as Page,
      label: "Dashboard",
      icon: LayoutDashboard,
    },
    {
      id: "voice" as Page,
      label: "Voice Assistant",
      icon: Mic,
    },
    {
      id: "history" as Page,
      label: "Resolution History",
      icon: History,
    },
    {
      id: "edge" as Page,
      label: "Edge Simulator",
      icon: Cpu,
    },
  ];

  const pageTitles: Record<Page, string> = {
    dashboard: "Dashboard",
    voice: "Voice Assistant",
    history: "Resolution History",
    edge: "Edge Simulator",
  };

  return (
    <div className="app-container">

      {/* SIDEBAR */}
      <aside className="sidebar">

        <div className="brand">
          <div className="brand-icon">
            <AudioWaveform size={25} />
          </div>

          <div>
            <h2>VaaniSetu</h2>
            <span>EDGE INTELLIGENCE</span>
          </div>
        </div>

        <div className="workspace-label">
          WORKSPACE
        </div>

        <nav className="sidebar-nav">

          {navigationItems.map((item) => {
            const Icon = item.icon;

            return (
              <button
                key={item.id}
                className={`nav-item ${
                  activePage === item.id ? "active" : ""
                }`}
                onClick={() => setActivePage(item.id)}
                style={{
                  width: "100%",
                  border: "none",
                  background:
                    activePage === item.id
                      ? undefined
                      : "transparent",
                  textAlign: "left",
                  cursor: "pointer",
                }}
              >
                <Icon size={19} />
                <span>{item.label}</span>
              </button>
            );
          })}

        </nav>

        <div className="sidebar-bottom">

          {/* BACKEND STATUS */}
          <div className="sidebar-status">

            <div
              className="status-indicator"
              style={{
                background: backendOnline
                  ? "#22c98a"
                  : "#ef4444",
              }}
            />

            <div>
              <strong>
                System {backendOnline ? "Online" : "Offline"}
              </strong>

              <span>
                {backendOnline
                  ? "Backend connected"
                  : "Backend disconnected"}
              </span>
            </div>

          </div>

          <button
            className="nav-item"
            onClick={() => setActivePage("dashboard")}
            style={{
              width: "100%",
              border: "none",
              background: "transparent",
              textAlign: "left",
              cursor: "pointer",
            }}
          >
            <Settings size={19} />
            <span>Settings</span>
          </button>

          <div className="profile-card">

            <div className="profile-avatar">
              VS
            </div>

            <div>
              <strong>VaaniSetu Admin</strong>
              <span>Workspace Owner</span>
            </div>

          </div>

        </div>

      </aside>


      {/* MAIN CONTENT */}
      <main className="main-content">

        {/* TOPBAR */}
        <header className="topbar">

          <div>
            <div className="breadcrumb">
              Workspace <ChevronRight size={14} />
              {pageTitles[activePage]}
            </div>

            <h1>{pageTitles[activePage]}</h1>
          </div>

          <div className="topbar-actions">

            <div className="search-box">
              <Search size={17} />

              <input
                type="text"
                placeholder="Search anything..."
              />
            </div>

            <button className="notification-button">
              <Bell size={19} />
              <span></span>
            </button>

            <div className="top-avatar">
              VS
            </div>

          </div>

        </header>


        {/* PAGE CONTENT */}
        {activePage === "voice" ? (

          <VoiceAssistant />

        ) : activePage === "history" ? (

          <ResolutionHistory />

        ) : activePage === "edge" ? (

          <EdgeSimulator />

        ) : activePage === "dashboard" ? (

          <div className="dashboard-content">

            {/* WELCOME */}
            <section className="welcome-section">

              <div>

                <div className="welcome-tag">
                  <Zap size={14} />
                  MULTILINGUAL AI PLATFORM
                </div>

                <h2>
                  Welcome to <span>VaaniSetu Edge</span>
                </h2>

                <p>
                  Intelligent voice interactions for India's
                  multilingual business ecosystem.
                </p>

              </div>

              <div className="welcome-visual">
                <AudioWaveform size={65} strokeWidth={1.3} />
              </div>

            </section>


            {/* STATISTICS */}
            <section className="stats-grid">

              <div className="stat-card">

                <div className="stat-top">

                  <div className="stat-icon purple">
                    <MessageSquare size={20} />
                  </div>

                  <span className="stat-label">
                    TOTAL INTERACTIONS
                  </span>

                </div>

                <h2>{dashboardLoading ? "..." : passports.length}</h2>

                <p>Customer voice interactions</p>

              </div>


              <div className="stat-card">

                <div className="stat-top">

                  <div className="stat-icon blue">
                    <Languages size={20} />
                  </div>

                  <span className="stat-label">
                    LANGUAGES
                  </span>

                </div>

                <h2>3</h2>

                <p>English, Hindi and Telugu</p>

              </div>


              <div className="stat-card">

                <div className="stat-top">

                  <div className="stat-icon green">
                    <ShieldCheck size={20} />
                  </div>

                  <span className="stat-label">
                    RESOLUTIONS
                  </span>

                </div>

                <h2>{dashboardLoading ? "..." : completedResolutions}</h2>

                <p>Completed AI resolutions</p>

              </div>


              <div className="stat-card">

                <div className="stat-top">

                  <div className="stat-icon orange">
                    <Activity size={20} />
                  </div>

                  <span className="stat-label">
                    SYSTEM STATUS
                  </span>

                </div>

                <h2
                  className={
                    backendOnline
                      ? "online-text"
                      : "offline-text"
                  }
                >
                  {backendOnline ? "Online" : "Offline"}
                </h2>

                <p>
                  {backendOnline
                    ? "Backend services available"
                    : "Backend connection unavailable"}
                </p>

              </div>

            </section>


            {/* MAIN GRID */}
            <section className="dashboard-grid">

              {/* VOICE INTELLIGENCE */}
              <div className="panel voice-panel">

                <div className="panel-header">

                  <div>
                    <h3>Voice Intelligence</h3>

                    <p>
                      Process multilingual customer queries
                    </p>
                  </div>

                  <div className="panel-icon">
                    <Mic size={20} />
                  </div>

                </div>


                <div className="voice-box">

                  <div className="voice-circle">
                    <Headphones size={34} />
                  </div>

                  <h3>Start a Voice Interaction</h3>

                  <p>
                    Upload a customer audio recording to begin
                    intelligent voice processing.
                  </p>

                  <button
                    className="primary-button"
                    onClick={() => setActivePage("voice")}
                  >
                    <Mic size={17} />

                    Open Voice Assistant

                    <ArrowUpRight size={16} />
                  </button>

                </div>


                <div className="supported-languages">

                  <span>SUPPORTED LANGUAGES</span>

                  <div className="language-list">
                    <div>English</div>
                    <div>हिन्दी</div>
                    <div>తెలుగు</div>
                  </div>

                </div>

              </div>


              {/* AI PIPELINE */}
              <div className="panel pipeline-panel">

                <div className="panel-header">

                  <div>
                    <h3>AI Processing Pipeline</h3>

                    <p>
                      VaaniSetu intelligent workflow
                    </p>
                  </div>

                  <div className="panel-icon blue-bg">
                    <Activity size={20} />
                  </div>

                </div>


                <div className="pipeline-list">

                  <div className="pipeline-item">

                    <div className="pipeline-icon">
                      <Mic size={17} />
                    </div>

                    <div>
                      <strong>Audio Input</strong>
                      <span>Customer voice recording</span>
                    </div>

                    <CircleCheck className="check-icon" size={19} />

                  </div>

                  <div className="pipeline-connector"></div>

                  <div className="pipeline-item">

                    <div className="pipeline-icon">
                      <Languages size={17} />
                    </div>

                    <div>
                      <strong>Speech Recognition</strong>
                      <span>Gnani Prisma v2.5 STT</span>
                    </div>

                    <CircleCheck className="check-icon" size={19} />

                  </div>

                  <div className="pipeline-connector"></div>

                  <div className="pipeline-item">

                    <div className="pipeline-icon">
                      <MessageSquare size={17} />
                    </div>

                    <div>
                      <strong>Intent & Knowledge</strong>
                      <span>Intent detection and RAG</span>
                    </div>

                    <CircleCheck className="check-icon" size={19} />

                  </div>

                  <div className="pipeline-connector"></div>

                  <div className="pipeline-item">

                    <div className="pipeline-icon">
                      <Zap size={17} />
                    </div>

                    <div>
                      <strong>AI Answer Generation</strong>
                      <span>Qwen2.5 local LLM</span>
                    </div>

                    <CircleCheck className="check-icon" size={19} />

                  </div>

                  <div className="pipeline-connector"></div>

                  <div className="pipeline-item">

                    <div className="pipeline-icon">
                      <Headphones size={17} />
                    </div>

                    <div>
                      <strong>Speech Output</strong>
                      <span>Gnani Timbre v2.5 TTS</span>
                    </div>

                    <CircleCheck className="check-icon" size={19} />

                  </div>

                </div>

              </div>

            </section>


            {/* BOTTOM GRID */}
            <section className="bottom-grid">

              {/* RECENT ACTIVITY */}
              <div className="panel activity-panel">

                <div className="panel-header">

                  <div>
                    <h3>Recent Activity</h3>
                    <p>Latest platform activities</p>
                  </div>

                  <button
                    className="text-button"
                    onClick={() => setActivePage("history")}
                  >
                    View history
                    <ArrowUpRight size={15} />
                  </button>

                </div>


                {passports.length > 0 ? (
                  [...passports]
                    .sort(
                      (a, b) =>
                        new Date(b.timestamp).getTime() -
                        new Date(a.timestamp).getTime()
                    )
                    .slice(0, 5)
                    .map((passport) => (
                      <div
                        className="pipeline-item"
                        style={{ marginTop: "18px" }}
                        key={passport.passport_id}
                      >
                        <div className="pipeline-icon">
                          <MessageSquare size={17} />
                        </div>

                        <div style={{ minWidth: 0 }}>
                          <strong>
                            {passport.intent_analysis?.intent || "Voice interaction"}
                          </strong>

                          <span>
                            {passport.customer_interaction?.transcript ||
                              "Transcript unavailable"}
                          </span>

                          <span>
                            {passport.timestamp
                              ? new Date(passport.timestamp).toLocaleString()
                              : "Timestamp unavailable"}
                          </span>
                        </div>

                        <CircleCheck className="check-icon" size={19} />
                      </div>
                    ))
                ) : (
                  <div className="empty-state">
                    <Clock size={28} />
                    <strong>
                      {dashboardLoading
                        ? "Loading recent activity..."
                        : "No recent activity displayed"}
                    </strong>
                    <span>
                      {dashboardLoading
                        ? "Fetching Resolution Passport records."
                        : "Process a voice interaction to get started."}
                    </span>
                  </div>
                )}

              </div>


              {/* SYSTEM OVERVIEW */}
              <div className="panel system-panel">

                <div className="panel-header">

                  <div>
                    <h3>System Overview</h3>
                    <p>Platform service availability</p>
                  </div>

                  <div className="panel-icon green-bg">
                    <ShieldCheck size={20} />
                  </div>

                </div>


                <div className="system-row">
                  <span>FastAPI Backend</span>

                  <strong>
                    <span
                      className="green-dot"
                      style={{
                        background: backendOnline
                          ? "#20ad7d"
                          : "#ef4444",
                      }}
                    />

                    {backendOnline ? "Available" : "Unavailable"}
                  </strong>

                </div>


                <div className="system-row">
                  <span>Gnani Prisma STT</span>

                  <strong>
                    <span className="green-dot"></span>
                    Configured
                  </strong>
                </div>


                <div className="system-row">
                  <span>Gnani Timbre TTS</span>

                  <strong>
                    <span className="green-dot"></span>
                    Configured
                  </strong>
                </div>


                <div className="system-row">
                  <span>Local LLM</span>

                  <strong>
                    <span className="green-dot"></span>
                    Configured
                  </strong>
                </div>


                <div className="system-row">
                  <span>ChromaDB</span>

                  <strong>
                    <span className="green-dot"></span>
                    Configured
                  </strong>
                </div>

              </div>

            </section>


            {/* FOOTER */}
            <footer className="footer">

              <span>
                © 2026 VaaniSetu Edge
              </span>

              <span>
                Multilingual Voice Intelligence Platform
              </span>

            </footer>

          </div>

        ) : (

          <div className="dashboard-content">
            <div className="panel">
              <h3>{pageTitles[activePage]}</h3>

              <p style={{ marginTop: "12px", color: "#929bad" }}>
                This section will be implemented in the next development
                phase.
              </p>
            </div>
          </div>

        )}

      </main>

    </div>
  );
}

export default App;