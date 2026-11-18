import { useState, useEffect } from 'react';
import { 
  Flame, Shield, Activity, Users, Layers, BookOpen, 
  Search, Target, Award, ExternalLink, Sparkles, TrendingUp,
  ArrowRight, ShieldCheck
} from 'lucide-react';
import { 
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid
} from 'recharts';

export default function App() {
  const [activeTab, setActiveTab] = useState<'overview' | 'shortlist' | 'batters' | 'bowlers' | 'gems' | 'scenarios' | 'pathirana' | 'pool' | 'methodology'>('overview');
  
  // Data state
  const [summary, setSummary] = useState<any>(null);
  const [retainedSquad, setRetainedSquad] = useState<any[]>([]);
  const [shortlist, setShortlist] = useState<any[]>([]);
  const [batters, setBatters] = useState<any[]>([]);
  const [bowlers, setBowlers] = useState<any[]>([]);
  const [hiddenGems, setHiddenGems] = useState<any[]>([]);
  const [scenarios, setScenarios] = useState<any[]>([]);
  const [activePool, setActivePool] = useState<any[]>([]);
  const [pathirana, setPathirana] = useState<any>(null);

  // Filters & Toggles
  const [normType, setNormType] = useState<'pct' | 'minmax'>('pct');
  const [batIndianOnly, setBatIndianOnly] = useState(false);
  const [batSpecOnly, setBatSpecOnly] = useState(false);
  const [bowlIndianOnly, setBowlIndianOnly] = useState(false);
  const [selectedScenario, setSelectedScenario] = useState('B2');
  const [poolSearch, setPoolSearch] = useState('');
  const [poolRoleFilter, setPoolRoleFilter] = useState('All');
  const [poolOverseasFilter, setPoolOverseasFilter] = useState('All');

  // Load verified data
  useEffect(() => {
    fetch('/data/summary.json').then(r => r.json()).then(setSummary).catch(console.error);
    fetch('/data/retained_squad.json').then(r => r.json()).then(setRetainedSquad).catch(console.error);
    fetch('/data/strategic_shortlist.json').then(r => r.json()).then(setShortlist).catch(console.error);
    fetch('/data/top_batters.json').then(r => r.json()).then(setBatters).catch(console.error);
    fetch('/data/top_bowlers.json').then(r => r.json()).then(setBowlers).catch(console.error);
    fetch('/data/hidden_gems.json').then(r => r.json()).then(setHiddenGems).catch(console.error);
    fetch('/data/scenarios.json').then(r => r.json()).then(setScenarios).catch(console.error);
    fetch('/data/active_pool.json').then(r => r.json()).then(setActivePool).catch(console.error);
    fetch('/data/pathirana_audit.json').then(r => r.json()).then(setPathirana).catch(console.error);
  }, []);

  // Filtered Batters
  const filteredBatters = batters.filter(b => {
    if (batIndianOnly && !b.is_indian) return false;
    if (batSpecOnly && !b.is_specialist) return false;
    return true;
  });

  // Filtered Bowlers
  const filteredBowlers = bowlers.filter(b => {
    if (bowlIndianOnly && !b.is_indian) return false;
    return true;
  });

  // Filtered Pool
  const filteredPool = activePool.filter(p => {
    const matchesSearch = p.player.toLowerCase().includes(poolSearch.toLowerCase()) || 
                          p.country.toLowerCase().includes(poolSearch.toLowerCase()) ||
                          p.last_franchise.toLowerCase().includes(poolSearch.toLowerCase());
    const matchesRole = poolRoleFilter === 'All' || p.role.toLowerCase().includes(poolRoleFilter.toLowerCase());
    const matchesOS = poolOverseasFilter === 'All' || 
                      (poolOverseasFilter === 'Indian' && !p.is_overseas) ||
                      (poolOverseasFilter === 'Overseas' && p.is_overseas);
    return matchesSearch && matchesRole && matchesOS;
  });

  // Chart data preparation
  const top10BattersChartData = filteredBatters.slice(0, 10).map(b => ({
    name: b.player.split(' ').pop() || b.player,
    fullName: b.player,
    pressSR: b.press_sr,
    baseSR: b.base_sr,
    clutch: b.delta_sr,
    ppr: b.ppr
  }));

  const top10BowlersChartData = filteredBowlers.slice(0, 10).map(b => ({
    name: b.player.split(' ').pop() || b.player,
    fullName: b.player,
    pressEcon: b.press_econ,
    baseEcon: b.base_econ,
    deltaEcon: b.delta_econ,
    ppr: b.ppr
  }));

  const shortlistChartData = shortlist.slice(0, 8).map(s => ({
    name: s.player.split(' ').pop() || s.player,
    fullName: s.player,
    PPR: s.ppr,
    AOR: s.aor,
    SRR: normType === 'pct' ? s.srr_pct : s.srr_minmax
  }));

  const currentScenario = scenarios.find(s => s.scenario_id.includes(selectedScenario)) || scenarios[0];

  return (
    <div className="min-h-screen bg-[#FFF5F9] text-[#171A35] font-sans">
      {/* 1. CINEMATIC OFFICIAL HERO BANNER */}
      <header className="relative bg-gradient-to-b from-white via-[#FFF0F6] to-[#FFF5F9] border-b border-pink-200/80 overflow-hidden">
        {/* Subtle Architectural Jali & Paisley Motifs */}
        <div className="absolute inset-0 opacity-[0.035] pointer-events-none" style={{
          backgroundImage: `radial-gradient(#E50072 1px, transparent 1px), radial-gradient(#B00055 1px, #FFF5F9 1px)`,
          backgroundSize: '32px 32px',
          backgroundPosition: '0 0, 16px 16px'
        }} />

        {/* Decorative Rajput Arch Silhouette Overlay */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-gradient-to-br from-pink-300/20 via-pink-100/10 to-transparent rounded-full blur-3xl pointer-events-none -mr-20 -mt-20" />
        <div className="absolute bottom-0 left-0 w-80 h-80 bg-gradient-to-tr from-pink-200/20 via-rose-100/10 to-transparent rounded-full blur-2xl pointer-events-none -ml-20 -mb-20" />

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 relative">
          <div className="flex flex-col md:flex-row items-center justify-between gap-8">
            <div className="flex flex-col items-center md:items-start text-center md:text-left space-y-4 max-w-3xl">
              {/* Official Brand Badge */}
              <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-white border border-pink-200 shadow-sm">
                <span className="w-2.5 h-2.5 rounded-full bg-[#E50072] animate-pulse" />
                <span className="text-xs font-bold uppercase tracking-wider text-[#B00055]">Official Strategy Submission</span>
                <span className="text-slate-300">|</span>
                <span className="text-xs font-semibold text-slate-600">IPL 2027 Auction War Room</span>
              </div>

              {/* Main Heading & Subtitles */}
              <div>
                <h1 className="text-3xl sm:text-4xl lg:text-5xl font-black text-[#171A35] tracking-tight leading-tight">
                  SupeRR Selector <span className="text-[#E50072]">— Season 2</span>
                </h1>
                <p className="text-lg sm:text-xl font-bold text-[#B00055] mt-1">
                  Pressure Performance Analytics for IPL 2027
                </p>
                <p className="text-sm sm:text-base text-slate-600 mt-2 font-medium max-w-2xl">
                  Identifying the Top 10 Batters & Top 10 Bowlers Under Pressure to Engineer a Championship-Ready Squad for the Rajasthan Royals.
                </p>
              </div>

              {/* Presenter / Author Credit */}
              <div className="flex flex-wrap items-center justify-center md:justify-start gap-3 pt-2 text-xs text-slate-600">
                <div className="flex items-center gap-2 bg-white px-3 py-1.5 rounded-lg border border-pink-100 shadow-sm">
                  <div className="w-6 h-6 rounded-full bg-pink-100 text-[#E50072] font-bold flex items-center justify-center text-[11px]">
                    AB
                  </div>
                  <div>
                    <span className="font-bold text-[#171A35]">Aman Bapunavar</span>
                    <span className="text-slate-400 mx-1.5">•</span>
                    <span>Data Analysis Enthusiast</span>
                  </div>
                </div>
                <div className="bg-white/80 px-3 py-1.5 rounded-lg border border-pink-100 text-slate-600 font-medium">
                  The National Institute of Engineering, Mysuru
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex items-center gap-3 pt-3">
                <button 
                  onClick={() => {
                    const el = document.getElementById('dashboard-main');
                    if (el) el.scrollIntoView({ behavior: 'smooth' });
                  }}
                  className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-[#E50072] to-[#B00055] text-white font-bold text-sm shadow-md hover:shadow-lg hover:from-[#c80064] hover:to-[#960048] transition-all flex items-center gap-2 cursor-pointer"
                >
                  <span>Explore the Analysis</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
                <a 
                  href="https://github.com/amanbapunavar17/RR" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="px-4 py-2.5 rounded-xl bg-white text-[#171A35] font-semibold text-sm border border-pink-200 hover:bg-pink-50 transition-colors flex items-center gap-2 shadow-sm"
                >
                  <ExternalLink className="w-4 h-4 text-[#E50072]" />
                  <span>GitHub Repository</span>
                </a>
              </div>
            </div>

            {/* Official Rajasthan Royals Crest / Logo Display */}
            <div className="flex flex-col items-center justify-center p-6 bg-white/90 rounded-3xl border border-pink-200 shadow-[0_8px_30px_rgb(229,0,114,0.08)] backdrop-blur-md max-w-xs w-full">
              <div className="p-3 bg-gradient-to-b from-pink-50 to-white rounded-2xl border border-pink-100 mb-3 w-full flex items-center justify-center">
                <img 
                  src="/rr_logo.png" 
                  alt="Rajasthan Royals Official Crest" 
                  className="h-20 w-auto object-contain filter drop-shadow-sm hover:scale-105 transition-transform duration-300"
                />
              </div>
              <div className="text-center">
                <p className="text-xs font-extrabold tracking-widest uppercase text-[#E50072]">Halla Bol</p>
                <p className="text-[11px] font-medium text-slate-500 mt-0.5">Auction Strategy & Squad Architecture</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* 2. STICKY EXECUTIVE NAVIGATION BAR */}
      <nav id="dashboard-main" className="sticky top-0 z-30 bg-white/95 backdrop-blur-md border-b border-pink-200/90 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Small Brand Identity */}
            <div className="flex items-center gap-3">
              <img src="/rr_logo.png" alt="RR" className="h-8 w-auto object-contain" />
              <div className="hidden sm:block">
                <span className="font-extrabold text-[#171A35] text-sm tracking-tight">SupeRR Selector</span>
                <span className="ml-1.5 text-[11px] font-bold text-[#E50072] bg-pink-50 px-2 py-0.5 rounded-full border border-pink-200">2027</span>
              </div>
            </div>

            {/* Desktop Tabs */}
            <div className="flex items-center space-x-1 overflow-x-auto py-2 scrollbar-none">
              {[
                { id: 'overview', label: 'War Room', icon: Shield },
                { id: 'shortlist', label: 'Top 15 Targets', icon: Target },
                { id: 'batters', label: 'Batting Analysis', icon: Flame },
                { id: 'bowlers', label: 'Bowling Analysis', icon: Activity },
                { id: 'gems', label: 'Hidden Gems', icon: Sparkles },
                { id: 'scenarios', label: 'Auction Scenarios', icon: Layers },
                { id: 'pathirana', label: 'Pathirana Audit', icon: ShieldCheck },
                { id: 'pool', label: 'Active Pool (87)', icon: Users },
                { id: 'methodology', label: 'Governance', icon: BookOpen }
              ].map(tab => {
                const Icon = tab.icon;
                const isActive = activeTab === tab.id;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id as any)}
                    className={`flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-bold transition-all whitespace-nowrap cursor-pointer ${
                      isActive 
                        ? 'bg-gradient-to-r from-[#E50072] to-[#B00055] text-white shadow-sm' 
                        : 'text-slate-600 hover:text-[#E50072] hover:bg-pink-50'
                    }`}
                  >
                    <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-white' : 'text-[#E50072]'}`} />
                    <span>{tab.label}</span>
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      </nav>

      {/* 3. MAIN DASHBOARD CONTENT */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* ========================================================================= */}
        {/* TAB 1: WAR ROOM OVERVIEW & SQUAD CONSTRAINTS */}
        {/* ========================================================================= */}
        {activeTab === 'overview' && (
          <div className="space-y-8 animate-fadeIn">
            {/* Top KPI Metric Cards */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-white p-5 rounded-2xl border border-pink-100 shadow-sm relative overflow-hidden">
                <div className="absolute top-0 right-0 w-16 h-16 bg-pink-100/40 rounded-bl-3xl pointer-events-none" />
                <div className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">Retained Squad</div>
                <div className="flex items-baseline gap-2">
                  <span className="text-3xl font-black text-[#171A35]">{summary?.retained_count || 19}</span>
                  <span className="text-xs font-semibold text-[#E50072]">/ 25 Max</span>
                </div>
                <div className="text-[11px] font-medium text-slate-500 mt-2 flex items-center gap-1">
                  <span>14 Indian</span> • <span>5 Overseas</span>
                </div>
              </div>

              <div className="bg-white p-5 rounded-2xl border border-pink-100 shadow-sm relative overflow-hidden">
                <div className="absolute top-0 right-0 w-16 h-16 bg-emerald-100/40 rounded-bl-3xl pointer-events-none" />
                <div className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">Remaining Purse</div>
                <div className="flex items-baseline gap-2">
                  <span className="text-3xl font-black text-emerald-700">₹{summary?.remaining_purse_cr || 27.05}</span>
                  <span className="text-xs font-bold text-emerald-600">Cr</span>
                </div>
                <div className="text-[11px] font-medium text-slate-500 mt-2">
                  Auction War Chest Available
                </div>
              </div>

              <div className="bg-white p-5 rounded-2xl border border-pink-100 shadow-sm relative overflow-hidden">
                <div className="absolute top-0 right-0 w-16 h-16 bg-pink-100/40 rounded-bl-3xl pointer-events-none" />
                <div className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">Available Slots</div>
                <div className="flex items-baseline gap-2">
                  <span className="text-3xl font-black text-[#E50072]">{summary?.available_slots || 6}</span>
                  <span className="text-xs font-semibold text-slate-500">Slots Total</span>
                </div>
                <div className="text-[11px] font-medium text-slate-500 mt-2">
                  Max 3 Overseas Slots
                </div>
              </div>

              <div className="bg-white p-5 rounded-2xl border border-pink-100 shadow-sm relative overflow-hidden">
                <div className="absolute top-0 right-0 w-16 h-16 bg-indigo-100/40 rounded-bl-3xl pointer-events-none" />
                <div className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">Active Released Pool</div>
                <div className="flex items-baseline gap-2">
                  <span className="text-3xl font-black text-[#171A35]">{summary?.active_eligible_candidates || 87}</span>
                  <span className="text-xs font-semibold text-slate-500">Candidates</span>
                </div>
                <div className="text-[11px] font-medium text-slate-500 mt-2 flex items-center gap-1">
                  <span>69 Qualified</span> (39 Bat, 30 Bowl)
                </div>
              </div>
            </div>

            {/* Strategic Roster Requirements & Priority Matrix */}
            <div className="bg-white p-6 rounded-2xl border border-pink-100 shadow-sm space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-3 border-b border-pink-100 gap-2">
                <div>
                  <h2 className="text-lg font-black text-[#171A35] flex items-center gap-2">
                    <Target className="w-5 h-5 text-[#E50072]" />
                    <span>Rajasthan Royals Auction Recruitment Priorities</span>
                  </h2>
                  <p className="text-xs text-slate-500 mt-0.5">Tactical squad gaps identified through pressure-performance simulation</p>
                </div>
                <span className="inline-flex items-center text-xs font-bold text-[#E50072] bg-pink-50 px-3 py-1 rounded-full border border-pink-200">
                  Targeting 6 Precise Acquisitions
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-4 gap-4 pt-2">
                <div className="p-4 rounded-xl bg-gradient-to-b from-pink-50/70 to-white border border-pink-200/80 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-[11px] font-extrabold uppercase tracking-wider text-[#B00055]">Priority 1</span>
                    <span className="w-2 h-2 rounded-full bg-[#E50072]" />
                  </div>
                  <h3 className="font-bold text-sm text-[#171A35]">Indian Death Bowler</h3>
                  <p className="text-xs text-slate-600 leading-relaxed">
                    High-stress death over execution (overs 16–20) alongside Sandeep Sharma.
                  </p>
                  <div className="pt-2 text-[11px] font-semibold text-[#E50072]">
                    Top Target: <span className="underline">Akash Madhwal</span> (SRR 97.12)
                  </div>
                </div>

                <div className="p-4 rounded-xl bg-gradient-to-b from-pink-50/70 to-white border border-pink-200/80 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-[11px] font-extrabold uppercase tracking-wider text-[#B00055]">Priority 2</span>
                    <span className="w-2 h-2 rounded-full bg-[#E50072]" />
                  </div>
                  <h3 className="font-bold text-sm text-[#171A35]">Pedigree Top-Order Bat</h3>
                  <p className="text-xs text-slate-600 leading-relaxed">
                    Stabilizer / anchor at No. 3 allowing Parag & Jurel to play destructive middle-order roles.
                  </p>
                  <div className="pt-2 text-[11px] font-semibold text-[#E50072]">
                    Top Target: <span className="underline">Nitish Rana</span> (SRR 85.06)
                  </div>
                </div>

                <div className="p-4 rounded-xl bg-gradient-to-b from-pink-50/70 to-white border border-pink-200/80 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-[11px] font-extrabold uppercase tracking-wider text-[#B00055]">Priority 3</span>
                    <span className="w-2 h-2 rounded-full bg-[#E50072]" />
                  </div>
                  <h3 className="font-bold text-sm text-[#171A35]">Death Finisher (6/7)</h3>
                  <p className="text-xs text-slate-600 leading-relaxed">
                    High boundary-strike rate in overs 16–20 to maximize par-score acceleration.
                  </p>
                  <div className="pt-2 text-[11px] font-semibold text-[#E50072]">
                    Top Target: <span className="underline">Shahrukh Khan</span> (SRR 88.08)
                  </div>
                </div>

                <div className="p-4 rounded-xl bg-gradient-to-b from-pink-50/70 to-white border border-pink-200/80 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-[11px] font-extrabold uppercase tracking-wider text-[#B00055]">Priority 4</span>
                    <span className="w-2 h-2 rounded-full bg-[#E50072]" />
                  </div>
                  <h3 className="font-bold text-sm text-[#171A35]">Tactical Spin / Pace Depth</h3>
                  <p className="text-xs text-slate-600 leading-relaxed">
                    Defensive spin control and Indian fast bowling reinforcements for squad balance.
                  </p>
                  <div className="pt-2 text-[11px] font-semibold text-[#E50072]">
                    Targets: <span className="underline">Ankolekar / Kuldeep Sen</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Retained 19 Core Squad Roster */}
            <div className="bg-white p-6 rounded-2xl border border-pink-100 shadow-sm space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-pink-100">
                <h2 className="text-lg font-black text-[#171A35] flex items-center gap-2">
                  <Shield className="w-5 h-5 text-[#E50072]" />
                  <span>Rajasthan Royals Retained Core (19 Players Locked)</span>
                </h2>
                <span className="text-xs text-slate-500 font-medium">BCCI Official Retention Announcement</span>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3">
                {retainedSquad.map((player, idx) => (
                  <div key={idx} className="p-3 rounded-xl bg-pink-50/40 border border-pink-100 hover:border-pink-300 transition-colors">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-[10px] font-bold text-slate-400">#{idx + 1}</span>
                      <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${player.is_overseas ? 'bg-indigo-50 text-indigo-700 border border-indigo-200' : 'bg-pink-100 text-[#E50072]'}`}>
                        {player.is_overseas ? 'Overseas' : 'Indian'}
                      </span>
                    </div>
                    <div className="font-bold text-xs text-[#171A35] truncate">{player.player}</div>
                    <div className="text-[11px] text-slate-500 mt-0.5">{player.role}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* ========================================================================= */}
        {/* TAB 2: STRATEGIC SHORTLIST (SRR TOP 15) */}
        {/* ========================================================================= */}
        {activeTab === 'shortlist' && (
          <div className="space-y-6 animate-fadeIn">
            {/* Header with Normalization Toggle */}
            <div className="bg-white p-6 rounded-2xl border border-pink-100 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div>
                <h2 className="text-xl font-black text-[#171A35] flex items-center gap-2">
                  <Target className="w-6 h-6 text-[#E50072]" />
                  <span>Official SupeRR Recommendation Rating (SRR) — Top 15 Targets</span>
                </h2>
                <p className="text-xs text-slate-600 mt-1">
                  Synthesizing on-field pure pressure execution (PPR) with auction feasibility, roster gap fit, and purse agility (AOR).
                </p>
              </div>

              {/* Normalization Mode Toggle */}
              <div className="inline-flex p-1 bg-pink-50 border border-pink-200 rounded-xl">
                <button
                  onClick={() => setNormType('pct')}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                    normType === 'pct' ? 'bg-[#E50072] text-white shadow-sm' : 'text-slate-600 hover:text-[#E50072]'
                  }`}
                >
                  Percentile Rank (SRR_pct)
                </button>
                <button
                  onClick={() => setNormType('minmax')}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                    normType === 'minmax' ? 'bg-[#E50072] text-white shadow-sm' : 'text-slate-600 hover:text-[#E50072]'
                  }`}
                >
                  Min-Max Normalized (SRR_minmax)
                </button>
              </div>
            </div>

            {/* Visual Comparison Chart */}
            <div className="bg-white p-6 rounded-2xl border border-pink-100 shadow-sm">
              <h3 className="text-sm font-bold text-[#171A35] mb-4 flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-[#E50072]" />
                <span>Top 8 Strategic Targets: PPR vs. AOR vs. SRR Balance</span>
              </h3>
              <div className="h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={shortlistChartData} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#FCE7F3" />
                    <XAxis dataKey="name" tick={{ fill: '#171A35', fontSize: 11, fontWeight: 600 }} />
                    <YAxis domain={[40, 100]} tick={{ fill: '#77727A', fontSize: 10 }} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#FFFFFF', borderColor: '#FCE7F3', borderRadius: '12px', boxShadow: '0 4px 20px rgba(0,0,0,0.08)' }} 
                      labelStyle={{ fontWeight: 800, color: '#171A35' }}
                    />
                    <Bar dataKey="PPR" fill="#F472B6" radius={[4, 4, 0, 0]} name="Pure Pressure Rating (PPR)" />
                    <Bar dataKey="AOR" fill="#171A35" radius={[4, 4, 0, 0]} name="Auction Opportunity (AOR)" />
                    <Bar dataKey="SRR" fill="#E50072" radius={[4, 4, 0, 0]} name="Final SupeRR Rating (SRR)" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Shortlist Table */}
            <div className="bg-white rounded-2xl border border-pink-100 shadow-sm overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-pink-50/70 border-b border-pink-100 text-[#171A35] font-extrabold uppercase tracking-wider text-[11px]">
                    <tr>
                      <th className="py-3 px-4">Rank</th>
                      <th className="py-3 px-4">Player</th>
                      <th className="py-3 px-4">Role</th>
                      <th className="py-3 px-4">Target Gap</th>
                      <th className="py-3 px-4 text-center">PPR (Norm)</th>
                      <th className="py-3 px-4 text-center">AOR</th>
                      <th className="py-3 px-4 text-center">Final SRR</th>
                      <th className="py-3 px-4 text-center">Rec. Est. Price</th>
                      <th className="py-3 px-4 text-center">Tier</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-pink-50">
                    {shortlist.map((target, idx) => {
                      const finalSrr = normType === 'pct' ? target.srr_pct : target.srr_minmax;
                      const normPpr = normType === 'pct' ? target.ppr_pct : target.ppr_minmax;
                      const isTopTarget = idx === 0;

                      return (
                        <tr key={target.player_id} className={`hover:bg-pink-50/40 transition-colors ${isTopTarget ? 'bg-pink-50/50 font-semibold' : ''}`}>
                          <td className="py-3 px-4 font-black text-[#171A35]">
                            {isTopTarget ? <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-[#E50072] text-white text-[11px]">1</span> : `#${target.rank}`}
                          </td>
                          <td className="py-3 px-4">
                            <div className="font-bold text-[#171A35] text-sm">{target.player}</div>
                            <div className="text-[10px] text-slate-500">{target.status}</div>
                          </td>
                          <td className="py-3 px-4 text-slate-600">{target.role}</td>
                          <td className="py-3 px-4">
                            <span className="inline-block px-2 py-0.5 rounded-md text-[10px] font-bold bg-pink-100 text-[#B00055]">
                              {target.target_priority}
                            </span>
                          </td>
                          <td className="py-3 px-4 text-center font-mono">
                            <span className="font-bold text-slate-800">{target.ppr.toFixed(1)}</span>
                            <span className="text-[10px] text-slate-400 block">({normPpr.toFixed(1)})</span>
                          </td>
                          <td className="py-3 px-4 text-center font-mono font-bold text-slate-800">
                            {target.aor.toFixed(1)}
                          </td>
                          <td className="py-3 px-4 text-center">
                            <span className="inline-block px-2.5 py-1 rounded-full text-xs font-black bg-gradient-to-r from-[#E50072] to-[#B00055] text-white shadow-xs">
                              {finalSrr.toFixed(2)}
                            </span>
                          </td>
                          <td className="py-3 px-4 text-center font-bold text-emerald-700">
                            ₹{target.est_price_cr.toFixed(2)} Cr
                          </td>
                          <td className="py-3 px-4 text-center">
                            <span className="text-[10px] font-extrabold px-2 py-0.5 rounded border border-pink-200 text-[#E50072] bg-white">
                              {target.tier}
                            </span>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================================= */}
        {/* TAB 3: BATTING ANALYSIS (TOP 10 BATTERS UNDER PRESSURE) */}
        {/* ========================================================================= */}
        {activeTab === 'batters' && (
          <div className="space-y-6 animate-fadeIn">
            {/* Header & Filter Controls */}
            <div className="bg-white p-6 rounded-2xl border border-pink-100 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div>
                <h2 className="text-xl font-black text-[#171A35] flex items-center gap-2">
                  <Flame className="w-6 h-6 text-[#E50072]" />
                  <span>Top Batters Under High Match Pressure (Pure PPR)</span>
                </h2>
                <p className="text-xs text-slate-600 mt-1">
                  Threshold: Match pressure index P_bat &ge; 55.20, minimum sample size N &ge; 25 deliveries.
                </p>
              </div>

              {/* Toggles */}
              <div className="flex items-center gap-3">
                <button
                  onClick={() => setBatIndianOnly(!batIndianOnly)}
                  className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all border cursor-pointer ${
                    batIndianOnly ? 'bg-[#E50072] text-white border-[#E50072]' : 'bg-white text-slate-700 border-pink-200 hover:bg-pink-50'
                  }`}
                >
                  {batIndianOnly ? '✓ Indian Only' : 'Show All Batters'}
                </button>
                <button
                  onClick={() => setBatSpecOnly(!batSpecOnly)}
                  className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all border cursor-pointer ${
                    batSpecOnly ? 'bg-[#171A35] text-white border-[#171A35]' : 'bg-white text-slate-700 border-pink-200 hover:bg-pink-50'
                  }`}
                >
                  {batSpecOnly ? '✓ Specialists Only' : 'Include All-Rounders'}
                </button>
              </div>
            </div>

            {/* Comparison Chart */}
            <div className="bg-white p-6 rounded-2xl border border-pink-100 shadow-sm">
              <h3 className="text-sm font-bold text-[#171A35] mb-4 flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-[#E50072]" />
                <span>Pressure Strike Rate vs. Baseline Strike Rate</span>
              </h3>
              <div className="h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={top10BattersChartData} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#FCE7F3" />
                    <XAxis dataKey="name" tick={{ fill: '#171A35', fontSize: 11, fontWeight: 600 }} />
                    <YAxis domain={[100, 220]} tick={{ fill: '#77727A', fontSize: 10 }} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#FFFFFF', borderColor: '#FCE7F3', borderRadius: '12px', boxShadow: '0 4px 20px rgba(0,0,0,0.08)' }} 
                      labelStyle={{ fontWeight: 800, color: '#171A35' }}
                    />
                    <Bar dataKey="baseSR" fill="#CBD5E1" radius={[4, 4, 0, 0]} name="Baseline Strike Rate" />
                    <Bar dataKey="pressSR" fill="#E50072" radius={[4, 4, 0, 0]} name="Pressure Strike Rate" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Batters Table */}
            <div className="bg-white rounded-2xl border border-pink-100 shadow-sm overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-pink-50/70 border-b border-pink-100 text-[#171A35] font-extrabold uppercase tracking-wider text-[11px]">
                    <tr>
                      <th className="py-3 px-4">Rank</th>
                      <th className="py-3 px-4">Batter</th>
                      <th className="py-3 px-4 text-center">Status</th>
                      <th className="py-3 px-4 text-center">Matches</th>
                      <th className="py-3 px-4 text-center">Pressure Runs (Balls)</th>
                      <th className="py-3 px-4 text-center">Pressure SR</th>
                      <th className="py-3 px-4 text-center">Baseline SR</th>
                      <th className="py-3 px-4 text-center">Clutch Lift (ΔSR)</th>
                      <th className="py-3 px-4 text-center">Pure PPR</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-pink-50">
                    {filteredBatters.slice(0, 10).map((b, idx) => (
                      <tr key={b.player_id} className="hover:bg-pink-50/40 transition-colors">
                        <td className="py-3 px-4 font-black text-[#171A35]">#{idx + 1}</td>
                        <td className="py-3 px-4">
                          <div className="font-bold text-[#171A35] text-sm">{b.player}</div>
                          <div className="text-[10px] text-slate-500">ID: {b.player_id}</div>
                        </td>
                        <td className="py-3 px-4 text-center">
                          <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${b.capped_status === 'Capped' ? 'bg-pink-100 text-[#E50072]' : 'bg-slate-100 text-slate-600'}`}>
                            {b.capped_status}
                          </span>
                        </td>
                        <td className="py-3 px-4 text-center font-medium">{b.matches}</td>
                        <td className="py-3 px-4 text-center font-mono">
                          <span className="font-bold text-[#171A35]">{b.press_runs}</span>
                          <span className="text-slate-400 text-[11px]"> ({b.press_balls}b)</span>
                        </td>
                        <td className="py-3 px-4 text-center font-bold text-[#E50072] font-mono">{b.press_sr.toFixed(2)}</td>
                        <td className="py-3 px-4 text-center font-mono text-slate-600">{b.base_sr.toFixed(2)}</td>
                        <td className="py-3 px-4 text-center font-mono font-bold">
                          <span className={b.delta_sr >= 0 ? 'text-emerald-600' : 'text-rose-600'}>
                            {b.delta_sr >= 0 ? `+${b.delta_sr.toFixed(2)}` : b.delta_sr.toFixed(2)}
                          </span>
                        </td>
                        <td className="py-3 px-4 text-center font-mono">
                          <span className="px-2.5 py-1 rounded-full text-xs font-black bg-pink-100 text-[#B00055] border border-pink-200">
                            {b.ppr.toFixed(2)}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================================= */}
        {/* TAB 4: BOWLING ANALYSIS (TOP 10 BOWLERS UNDER PRESSURE) */}
        {/* ========================================================================= */}
        {activeTab === 'bowlers' && (
          <div className="space-y-6 animate-fadeIn">
            {/* Header & Filter Controls */}
            <div className="bg-white p-6 rounded-2xl border border-pink-100 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div>
                <h2 className="text-xl font-black text-[#171A35] flex items-center gap-2">
                  <Activity className="w-6 h-6 text-[#E50072]" />
                  <span>Top Bowlers Under High Match Pressure (Legal Ball Standard)</span>
                </h2>
                <p className="text-xs text-slate-600 mt-1">
                  Cricket Law: Economy = (Bowler Runs Conceded × 6) / Legal Deliveries Bowled. Denominator excludes wides & no-balls.
                </p>
              </div>

              {/* Indian Toggle */}
              <button
                onClick={() => setBowlIndianOnly(!bowlIndianOnly)}
                className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all border cursor-pointer ${
                  bowlIndianOnly ? 'bg-[#E50072] text-white border-[#E50072]' : 'bg-white text-slate-700 border-pink-200 hover:bg-pink-50'
                }`}
              >
                {bowlIndianOnly ? '✓ Indian Only' : 'Show All Bowlers'}
              </button>
            </div>

            {/* Economy Comparison Chart */}
            <div className="bg-white p-6 rounded-2xl border border-pink-100 shadow-sm">
              <h3 className="text-sm font-bold text-[#171A35] mb-4 flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-[#E50072]" />
                <span>Pressure Economy vs. Baseline Economy (Lower is Better)</span>
              </h3>
              <div className="h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={top10BowlersChartData} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#FCE7F3" />
                    <XAxis dataKey="name" tick={{ fill: '#171A35', fontSize: 11, fontWeight: 600 }} />
                    <YAxis domain={[5, 12]} tick={{ fill: '#77727A', fontSize: 10 }} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#FFFFFF', borderColor: '#FCE7F3', borderRadius: '12px', boxShadow: '0 4px 20px rgba(0,0,0,0.08)' }} 
                      labelStyle={{ fontWeight: 800, color: '#171A35' }}
                    />
                    <Bar dataKey="baseEcon" fill="#CBD5E1" radius={[4, 4, 0, 0]} name="Baseline Economy" />
                    <Bar dataKey="pressEcon" fill="#E50072" radius={[4, 4, 0, 0]} name="Pressure Economy" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Bowlers Table */}
            <div className="bg-white rounded-2xl border border-pink-100 shadow-sm overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-pink-50/70 border-b border-pink-100 text-[#171A35] font-extrabold uppercase tracking-wider text-[11px]">
                    <tr>
                      <th className="py-3 px-4">Rank</th>
                      <th className="py-3 px-4">Bowler</th>
                      <th className="py-3 px-4 text-center">Status</th>
                      <th className="py-3 px-4 text-center">Matches</th>
                      <th className="py-3 px-4 text-center">Pressure Wickets</th>
                      <th className="py-3 px-4 text-center">Pressure Legal Balls</th>
                      <th className="py-3 px-4 text-center">Pressure Economy</th>
                      <th className="py-3 px-4 text-center">Baseline Economy</th>
                      <th className="py-3 px-4 text-center">Economy Difference</th>
                      <th className="py-3 px-4 text-center">Pure PPR</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-pink-50">
                    {filteredBowlers.slice(0, 10).map((b, idx) => (
                      <tr key={b.player_id} className="hover:bg-pink-50/40 transition-colors">
                        <td className="py-3 px-4 font-black text-[#171A35]">#{idx + 1}</td>
                        <td className="py-3 px-4">
                          <div className="font-bold text-[#171A35] text-sm">{b.player}</div>
                          <div className="text-[10px] text-slate-500">ID: {b.player_id}</div>
                        </td>
                        <td className="py-3 px-4 text-center">
                          <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${b.capped_status === 'Capped' ? 'bg-pink-100 text-[#E50072]' : 'bg-slate-100 text-slate-600'}`}>
                            {b.capped_status}
                          </span>
                        </td>
                        <td className="py-3 px-4 text-center font-medium">{b.matches}</td>
                        <td className="py-3 px-4 text-center font-mono font-bold text-[#171A35]">{b.press_wkts}</td>
                        <td className="py-3 px-4 text-center font-mono text-slate-600">{b.press_legal_balls}</td>
                        <td className="py-3 px-4 text-center font-bold text-[#E50072] font-mono">{b.press_econ.toFixed(2)}</td>
                        <td className="py-3 px-4 text-center font-mono text-slate-600">{b.base_econ.toFixed(2)}</td>
                        <td className="py-3 px-4 text-center font-mono font-bold">
                          <span className={b.delta_econ <= 0 ? 'text-emerald-600' : 'text-slate-600'}>
                            {b.delta_econ >= 0 ? `+${b.delta_econ.toFixed(2)}` : b.delta_econ.toFixed(2)}
                          </span>
                        </td>
                        <td className="py-3 px-4 text-center font-mono">
                          <span className="px-2.5 py-1 rounded-full text-xs font-black bg-pink-100 text-[#B00055] border border-pink-200">
                            {b.ppr.toFixed(2)}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================================= */}
        {/* TAB 5: 5 AUDITED HIDDEN GEMS */}
        {/* ========================================================================= */}
        {activeTab === 'gems' && (
          <div className="space-y-6 animate-fadeIn">
            <div className="bg-white p-6 rounded-2xl border border-pink-100 shadow-sm">
              <h2 className="text-xl font-black text-[#171A35] flex items-center gap-2">
                <Sparkles className="w-6 h-6 text-[#E50072]" />
                <span>Audited Hidden Gems: High-Leverage Strategic Targets</span>
              </h2>
              <p className="text-xs text-slate-600 mt-1">
                Players whose market availability and price efficiency deliver exceptional value under Rajasthan Royals' purse constraints.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {hiddenGems.map((gem) => (
                <div key={gem.id} className="bg-white rounded-2xl border border-pink-100 p-5 shadow-sm hover:border-pink-300 transition-all flex flex-col justify-between space-y-4">
                  <div>
                    {/* Header with Avatar & Status */}
                    <div className="flex items-start justify-between">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#E50072] to-[#B00055] text-white font-extrabold flex items-center justify-center text-sm shadow-sm">
                          {gem.name.split(' ').map((n: string) => n[0]).join('')}
                        </div>
                        <div>
                          <h3 className="font-black text-base text-[#171A35]">{gem.name}</h3>
                          <span className="text-[11px] text-slate-500 font-medium">{gem.role}</span>
                        </div>
                      </div>
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${gem.capped === 'Capped' ? 'bg-pink-100 text-[#E50072]' : 'bg-slate-100 text-slate-600'}`}>
                        {gem.capped}
                      </span>
                    </div>

                    {/* Key Metrics Grid */}
                    <div className="grid grid-cols-3 gap-2 mt-4 p-3 bg-pink-50/50 rounded-xl border border-pink-100 text-center">
                      <div>
                        <div className="text-[10px] text-slate-500 uppercase font-semibold">PPR</div>
                        <div className="text-sm font-black text-[#171A35]">{gem.ppr.toFixed(1)}</div>
                      </div>
                      <div>
                        <div className="text-[10px] text-slate-500 uppercase font-semibold">AOR</div>
                        <div className="text-sm font-black text-[#171A35]">{gem.aor.toFixed(1)}</div>
                      </div>
                      <div>
                        <div className="text-[10px] text-slate-500 uppercase font-semibold">SRR (Pct)</div>
                        <div className="text-sm font-black text-[#E50072]">{gem.srr_pct.toFixed(1)}</div>
                      </div>
                    </div>

                    {/* Undervalued Reason & Tactical Fit */}
                    <div className="mt-4 space-y-2 text-xs">
                      <div>
                        <span className="font-bold text-[#B00055]">Why Undervalued: </span>
                        <span className="text-slate-600">{gem.why_undervalued}</span>
                      </div>
                      <div>
                        <span className="font-bold text-[#171A35]">Tactical Fit: </span>
                        <span className="text-slate-600">{gem.tactical_fit}</span>
                      </div>
                    </div>
                  </div>

                  {/* Estimated Price Footer */}
                  <div className="pt-3 border-t border-pink-100 flex items-center justify-between">
                    <span className="text-[11px] font-semibold text-slate-500">Rec. Acquisition Range</span>
                    <span className="text-sm font-black text-emerald-700">₹{gem.rec_price_cr.toFixed(2)} Cr</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ========================================================================= */}
        {/* TAB 6: FOUR 6-PLAYER AUCTION SCENARIOS */}
        {/* ========================================================================= */}
        {activeTab === 'scenarios' && (
          <div className="space-y-6 animate-fadeIn">
            <div className="bg-white p-6 rounded-2xl border border-pink-100 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div>
                <h2 className="text-xl font-black text-[#171A35] flex items-center gap-2">
                  <Layers className="w-6 h-6 text-[#E50072]" />
                  <span>Four 6-Player Auction Scenarios (Full 25-Man Roster)</span>
                </h2>
                <p className="text-xs text-slate-600 mt-1">
                  Budget: ₹27.05 Cr | 6 Open Slots | Max 3 Overseas Acquisitions
                </p>
              </div>

              {/* Scenario Selector Pills */}
              <div className="flex flex-wrap items-center gap-2">
                {[
                  { id: 'A', label: 'Scenario A (Pathirana Anchor)' },
                  { id: 'B1', label: 'Scenario B1 (Indian Death Core)' },
                  { id: 'B2', label: 'Scenario B2 (RECOMMENDED)' },
                  { id: 'C', label: 'Scenario C (Hybrid 20-Over Definite)' }
                ].map(sc => (
                  <button
                    key={sc.id}
                    onClick={() => setSelectedScenario(sc.id)}
                    className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                      selectedScenario === sc.id 
                        ? 'bg-gradient-to-r from-[#E50072] to-[#B00055] text-white shadow-sm' 
                        : 'bg-white text-slate-700 border border-pink-200 hover:bg-pink-50'
                    }`}
                  >
                    {sc.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Selected Scenario Detail Card */}
            {currentScenario && (
              <div className="bg-white rounded-2xl border border-pink-100 shadow-sm p-6 space-y-6">
                {/* Header */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-pink-100 gap-3">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="px-2.5 py-0.5 rounded-full text-xs font-black bg-pink-100 text-[#B00055] border border-pink-200">
                        {currentScenario.scenario_id}
                      </span>
                      {currentScenario.rec_status.includes('RECOMMENDED') && (
                        <span className="px-2.5 py-0.5 rounded-full text-xs font-black bg-emerald-100 text-emerald-800 border border-emerald-300">
                          RECOMMENDED STRATEGY
                        </span>
                      )}
                    </div>
                    <h3 className="text-lg font-black text-[#171A35] mt-1.5">{currentScenario.scenario_name}</h3>
                  </div>

                  <div className="flex items-center gap-4 bg-pink-50/60 px-4 py-2 rounded-xl border border-pink-100">
                    <div>
                      <span className="text-[10px] text-slate-500 uppercase font-semibold block">Total Outlay</span>
                      <span className="text-base font-black text-rose-700">₹{currentScenario.total_spend_cr.toFixed(2)} Cr</span>
                    </div>
                    <div className="w-px h-8 bg-pink-200" />
                    <div>
                      <span className="text-[10px] text-slate-500 uppercase font-semibold block">Safety Buffer</span>
                      <span className="text-base font-black text-emerald-700">₹{currentScenario.remaining_buffer_cr.toFixed(2)} Cr</span>
                    </div>
                  </div>
                </div>

                {/* 6 Target Acquisitions */}
                <div>
                  <h4 className="text-xs font-extrabold uppercase tracking-wider text-slate-500 mb-3">
                    6 Target Acquisitions (Completes 25-Player Squad)
                  </h4>
                  <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-3">
                    {currentScenario.key_signings.map((signing: string, idx: number) => (
                      <div key={idx} className="p-3 rounded-xl bg-pink-50/30 border border-pink-100 text-center">
                        <div className="text-[10px] font-bold text-[#E50072] mb-1">Pick #{idx + 1}</div>
                        <div className="font-bold text-xs text-[#171A35]">{signing}</div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Playing XI & 20-Over Plan */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
                  {/* First Choice XI */}
                  <div className="space-y-3">
                    <h4 className="text-xs font-extrabold uppercase tracking-wider text-slate-500">
                      First-Choice Playing XI & Impact Player
                    </h4>
                    <div className="p-4 bg-pink-50/40 rounded-xl border border-pink-100 space-y-2 text-xs">
                      <div className="leading-relaxed font-medium text-slate-700">
                        {currentScenario.playing_xi}
                      </div>
                      <div className="pt-2 border-t border-pink-200/80 text-[11px] text-[#B00055] font-semibold">
                        Impact Player Sub: <span className="text-[#171A35]">{currentScenario.impact_sub}</span>
                      </div>
                    </div>
                  </div>

                  {/* 20-Over Bowling Plan */}
                  <div className="space-y-3">
                    <h4 className="text-xs font-extrabold uppercase tracking-wider text-slate-500">
                      Certified 20-Over Phase Allocation
                    </h4>
                    <div className="p-4 bg-pink-50/40 rounded-xl border border-pink-100 space-y-2 text-xs">
                      <div className="leading-relaxed font-mono text-[11px] text-slate-800">
                        {currentScenario.death_overs_plan}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Strategic Evaluation */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2 text-xs">
                  <div className="p-3 rounded-xl bg-emerald-50/60 border border-emerald-200 space-y-1">
                    <span className="font-bold text-emerald-800">Key Strengths: </span>
                    <span className="text-slate-700">{currentScenario.strengths}</span>
                  </div>
                  <div className="p-3 rounded-xl bg-rose-50/60 border border-rose-200 space-y-1">
                    <span className="font-bold text-rose-800">Execution Risks: </span>
                    <span className="text-slate-700">{currentScenario.risks}</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* ========================================================================= */}
        {/* TAB 7: MATHEESHA PATHIRANA FORENSIC AUDIT */}
        {/* ========================================================================= */}
        {activeTab === 'pathirana' && (
          <div className="space-y-6 animate-fadeIn">
            <div className="bg-white p-6 rounded-2xl border border-pink-100 shadow-sm">
              <h2 className="text-xl font-black text-[#171A35] flex items-center gap-2">
                <ShieldCheck className="w-6 h-6 text-[#E50072]" />
                <span>Matheesha Pathirana Forensic Delivery Audit</span>
              </h2>
              <p className="text-xs text-slate-600 mt-1">
                Cricket Law Denominator Verification: Bowler runs divided by legal deliveries bowled (excluding 28 wides & 5 no-balls).
              </p>
            </div>

            {/* Delivery Accounting Metrics */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-white p-5 rounded-2xl border border-pink-100 shadow-sm text-center">
                <div className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">Total Deliveries</div>
                <div className="text-3xl font-black text-[#171A35]">{pathirana?.total_deliveries || 281}</div>
                <div className="text-[11px] text-slate-400 mt-1">Raw Ball Events</div>
              </div>

              <div className="bg-white p-5 rounded-2xl border border-pink-100 shadow-sm text-center">
                <div className="text-xs font-bold uppercase tracking-wider text-[#E50072] mb-1">Legal Deliveries</div>
                <div className="text-3xl font-black text-[#E50072]">{pathirana?.legal_deliveries || 248}</div>
                <div className="text-[11px] text-slate-400 mt-1">28 Wides, 5 No-Balls Excluded</div>
              </div>

              <div className="bg-white p-5 rounded-2xl border border-pink-100 shadow-sm text-center">
                <div className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">Runs Conceded</div>
                <div className="text-3xl font-black text-rose-700">{pathirana?.runs_conceded || 415}</div>
                <div className="text-[11px] text-slate-400 mt-1">Bowler Runs Charged</div>
              </div>

              <div className="bg-white p-5 rounded-2xl border border-pink-100 shadow-sm text-center">
                <div className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">Wickets Taken</div>
                <div className="text-3xl font-black text-emerald-700">{pathirana?.wickets || 20}</div>
                <div className="text-[11px] text-slate-400 mt-1">High-Stress Wickets</div>
              </div>
            </div>

            {/* Forensic Economy Comparison */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white p-6 rounded-2xl border border-pink-100 shadow-sm space-y-4">
                <h3 className="font-bold text-base text-[#171A35] pb-2 border-b border-pink-100">
                  Overall Match Pressure Phase (N_legal = 248)
                </h3>
                <div className="space-y-3 text-xs">
                  <div className="flex justify-between items-center py-1 border-b border-pink-50">
                    <span className="text-slate-600">Certified Pressure Economy:</span>
                    <span className="font-mono font-bold text-sm text-[#E50072]">{pathirana?.overall_pressure_econ || 10.04} rpo</span>
                  </div>
                  <div className="flex justify-between items-center py-1 border-b border-pink-50">
                    <span className="text-slate-600">Tournament Baseline Economy:</span>
                    <span className="font-mono font-bold text-sm text-slate-700">{pathirana?.baseline_econ || 8.49} rpo</span>
                  </div>
                  <div className="flex justify-between items-center py-1">
                    <span className="text-slate-600">Delta Economy (Overheating):</span>
                    <span className="font-mono font-bold text-sm text-rose-600">+{pathirana?.delta_econ || 1.55} rpo</span>
                  </div>
                </div>
              </div>

              <div className="bg-white p-6 rounded-2xl border border-pink-100 shadow-sm space-y-4">
                <h3 className="font-bold text-base text-[#171A35] pb-2 border-b border-pink-100">
                  Death Phase Performance (Overs 16–20)
                </h3>
                <div className="space-y-3 text-xs">
                  <div className="flex justify-between items-center py-1 border-b border-pink-50">
                    <span className="text-slate-600">Death Legal Deliveries:</span>
                    <span className="font-mono font-bold text-sm text-[#171A35]">{pathirana?.death_legal_balls || 168} legal balls</span>
                  </div>
                  <div className="flex justify-between items-center py-1 border-b border-pink-50">
                    <span className="text-slate-600">Death Phase Economy:</span>
                    <span className="font-mono font-bold text-sm text-emerald-700">{pathirana?.death_pressure_econ || 10.75} rpo</span>
                  </div>
                  <div className="flex justify-between items-center py-1">
                    <span className="text-slate-600">Tournament Death Benchmark:</span>
                    <span className="font-mono font-bold text-sm text-slate-700">{pathirana?.death_benchmark_econ || 11.15} rpo</span>
                  </div>
                </div>
                <div className="p-3 bg-emerald-50 rounded-xl border border-emerald-200 text-[11px] text-emerald-800 font-semibold">
                  ✓ Pathirana outperforms the tournament death-over economy benchmark by -0.40 rpo while taking 15 wickets.
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================================= */}
        {/* TAB 8: ACTIVE RELEASED CANDIDATE POOL (87 PLAYERS) */}
        {/* ========================================================================= */}
        {activeTab === 'pool' && (
          <div className="space-y-6 animate-fadeIn">
            <div className="bg-white p-6 rounded-2xl border border-pink-100 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div>
                <h2 className="text-xl font-black text-[#171A35] flex items-center gap-2">
                  <Users className="w-6 h-6 text-[#E50072]" />
                  <span>Active Released Player Pool (87 Candidates)</span>
                </h2>
                <p className="text-xs text-slate-600 mt-1">
                  89 official releases reconciled: 87 active eligible cricketers, 2 ineligible/retired (MS Dhoni, Ajinkya Rahane).
                </p>
              </div>

              {/* Search and Filters */}
              <div className="flex flex-wrap items-center gap-2">
                <div className="relative">
                  <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
                  <input
                    type="text"
                    placeholder="Search player, team, country..."
                    value={poolSearch}
                    onChange={(e) => setPoolSearch(e.target.value)}
                    className="pl-9 pr-3 py-1.5 rounded-xl border border-pink-200 bg-white text-xs text-[#171A35] focus:outline-none focus:border-[#E50072]"
                  />
                </div>
                <select
                  value={poolRoleFilter}
                  onChange={(e) => setPoolRoleFilter(e.target.value)}
                  className="px-3 py-1.5 rounded-xl border border-pink-200 bg-white text-xs text-slate-700 focus:outline-none"
                >
                  <option value="All">All Roles</option>
                  <option value="Batter">Batter</option>
                  <option value="Bowler">Bowler</option>
                  <option value="All-Rounder">All-Rounder</option>
                  <option value="Wicket-Keeper">Wicket-Keeper</option>
                </select>
                <select
                  value={poolOverseasFilter}
                  onChange={(e) => setPoolOverseasFilter(e.target.value)}
                  className="px-3 py-1.5 rounded-xl border border-pink-200 bg-white text-xs text-slate-700 focus:outline-none"
                >
                  <option value="All">All Nationalities</option>
                  <option value="Indian">Indian Only</option>
                  <option value="Overseas">Overseas Only</option>
                </select>
              </div>
            </div>

            {/* Candidate Pool Table */}
            <div className="bg-white rounded-2xl border border-pink-100 shadow-sm overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-pink-50/70 border-b border-pink-100 text-[#171A35] font-extrabold uppercase tracking-wider text-[11px]">
                    <tr>
                      <th className="py-3 px-4">Player</th>
                      <th className="py-3 px-4">Country</th>
                      <th className="py-3 px-4">Last Franchise</th>
                      <th className="py-3 px-4 text-center">Status</th>
                      <th className="py-3 px-4">Playing Role</th>
                      <th className="py-3 px-4 text-center">AOR Score</th>
                      <th className="py-3 px-4 text-center">Tactical Fit</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-pink-50">
                    {filteredPool.slice(0, 30).map((player) => (
                      <tr key={player.player_id} className="hover:bg-pink-50/40 transition-colors">
                        <td className="py-3 px-4">
                          <div className="font-bold text-[#171A35] text-sm">{player.player}</div>
                          <div className="text-[10px] text-slate-400">ID: {player.player_id}</div>
                        </td>
                        <td className="py-3 px-4 text-slate-600">{player.country}</td>
                        <td className="py-3 px-4 font-semibold text-slate-800">{player.last_franchise}</td>
                        <td className="py-3 px-4 text-center">
                          <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${player.capped_status === 'Capped' ? 'bg-pink-100 text-[#E50072]' : 'bg-slate-100 text-slate-600'}`}>
                            {player.capped_status}
                          </span>
                        </td>
                        <td className="py-3 px-4 text-slate-600">{player.role}</td>
                        <td className="py-3 px-4 text-center font-mono font-bold text-slate-800">
                          {player.aor_score ? player.aor_score.toFixed(1) : '—'}
                        </td>
                        <td className="py-3 px-4 text-center">
                          <span className="text-[10px] font-bold text-[#B00055]">
                            {player.priority_alignment || 'Depth'}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <div className="p-3 bg-pink-50/30 border-t border-pink-100 text-center text-xs text-slate-500">
                Showing top 30 of {filteredPool.length} candidates matching active filters
              </div>
            </div>
          </div>
        )}

        {/* ========================================================================= */}
        {/* TAB 9: METHODOLOGY & GOVERNANCE ARCHITECTURE */}
        {/* ========================================================================= */}
        {activeTab === 'methodology' && (
          <div className="space-y-6 animate-fadeIn">
            <div className="bg-white p-6 rounded-2xl border border-pink-100 shadow-sm">
              <h2 className="text-xl font-black text-[#171A35] flex items-center gap-2">
                <BookOpen className="w-6 h-6 text-[#E50072]" />
                <span>Analytical Governance & Mathematical Formulations</span>
              </h2>
              <p className="text-xs text-slate-600 mt-1">
                Audited mathematical models, Empirical Bayes Shrinkage, and Cricket Law bowling metrics.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs">
              {/* PPR Formula */}
              <div className="bg-white p-5 rounded-2xl border border-pink-100 shadow-sm space-y-3">
                <h3 className="font-black text-sm text-[#E50072] flex items-center gap-2">
                  <Flame className="w-4 h-4" />
                  <span>1. Pure Pressure Performance Rating (PPR)</span>
                </h3>
                <p className="text-slate-600 leading-relaxed">
                  Evaluates on-field execution under high match pressure (P_bat &ge; 55.20, P_bowl &ge; 68.90).
                </p>
                <div className="bg-pink-50/60 p-3 rounded-xl border border-pink-100 font-mono text-[11px] text-slate-800 space-y-1">
                  <div>comp_bat = 0.40*z_sr + 0.25*z_delta + 0.20*z_avg + 0.15*z_cons</div>
                  <div>comp_bowl = 0.35*z_econ + 0.25*z_delta + 0.25*z_wkt + 0.15*z_cons</div>
                  <div>PPR = Clip(50.0 + 18.0 * comp, 25.0, 95.0)</div>
                </div>
                <p className="text-slate-500 text-[11px]">
                  Empirical Bayes Shrinkage (K = 40) regulates small-sample variance. Zero demographic or auction points.
                </p>
              </div>

              {/* AOR Formula */}
              <div className="bg-white p-5 rounded-2xl border border-pink-100 shadow-sm space-y-3">
                <h3 className="font-black text-sm text-[#171A35] flex items-center gap-2">
                  <Target className="w-4 h-4 text-[#E50072]" />
                  <span>2. Auction Opportunity Rating (AOR)</span>
                </h3>
                <p className="text-slate-600 leading-relaxed">
                  Evaluates market availability, tactical roster fit, and purse efficiency.
                </p>
                <div className="bg-pink-50/60 p-3 rounded-xl border border-pink-100 font-mono text-[11px] text-slate-800 space-y-1">
                  <div>AOS = 100.0 * (0.35*I_avail + 0.30*I_fit + 0.25*I_slot + 0.10*I_sample)</div>
                  <div>• I_avail: 0.0 (Retired), 0.90 (RR Released), 1.0 (Other)</div>
                  <div>• I_fit: Priority 1-4 gap alignment (0.60 - 0.95)</div>
                  <div>• I_slot: Indian Uncapped (1.0), Capped (0.55-0.80), OS (0.40-0.70)</div>
                </div>
              </div>

              {/* Normalization Audit */}
              <div className="bg-white p-5 rounded-2xl border border-pink-100 shadow-sm space-y-3">
                <h3 className="font-black text-sm text-[#B00055] flex items-center gap-2">
                  <Award className="w-4 h-4" />
                  <span>3. Score Synthesis: SRR_pct vs SRR_minmax</span>
                </h3>
                <p className="text-slate-600 leading-relaxed">
                  To eliminate scale mismatch between PPR (25–95) and AOR (0–100), two mathematically sound methods are certified:
                </p>
                <div className="bg-pink-50/60 p-3 rounded-xl border border-pink-100 font-mono text-[11px] text-slate-800 space-y-1">
                  <div>Percentile: SRR_pct = 0.50 * Percentile(PPR) + 0.50 * AOR</div>
                  <div>Min-Max: SRR_minmax = 0.50 * MinMax(PPR) + 0.50 * AOR</div>
                </div>
                <p className="text-slate-500 text-[11px]">
                  Akash Madhwal ranks #1 under both normalizations (SRR_pct: 97.12, SRR_minmax: 87.05).
                </p>
              </div>

              {/* Cricket Law Bowling Economy */}
              <div className="bg-white p-5 rounded-2xl border border-pink-100 shadow-sm space-y-3">
                <h3 className="font-black text-sm text-emerald-800 flex items-center gap-2">
                  <ShieldCheck className="w-4 h-4 text-emerald-600" />
                  <span>4. Cricket Law Bowling Economy Standard</span>
                </h3>
                <p className="text-slate-600 leading-relaxed">
                  Compliance with official Marylebone Cricket Club (MCC) & BCCI Laws:
                </p>
                <div className="bg-pink-50/60 p-3 rounded-xl border border-pink-100 font-mono text-[11px] text-slate-800 space-y-1">
                  <div>Economy = (Bowler Runs Conceded × 6) / Legal Deliveries Bowled</div>
                  <div>• Denominator EXCLUDES wides and no-balls</div>
                  <div>• Numerator INCLUDES wide & no-ball penalties charged to bowler</div>
                  <div>• Numerator EXCLUDES byes and leg-byes</div>
                </div>
              </div>
            </div>
          </div>
        )}

      </main>

      {/* 4. FOOTER */}
      <footer className="bg-white border-t border-pink-200/80 py-8 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between gap-4 text-xs text-slate-500">
          <div className="flex items-center gap-3">
            <img src="/rr_logo.png" alt="RR Logo" className="h-7 w-auto object-contain" />
            <div>
              <span className="font-bold text-[#171A35]">Rajasthan Royals SupeRR Selector Season 2</span>
              <span className="block text-[11px] text-slate-400">Official IPL 2027 Auction Strategy Portal</span>
            </div>
          </div>
          <div className="text-center md:text-right">
            <div>Engineered by <span className="font-bold text-[#171A35]">Aman Bapunavar</span></div>
            <div className="text-[11px] text-slate-400">The National Institute of Engineering, Mysuru</div>
          </div>
        </div>
      </footer>
    </div>
  );
}
