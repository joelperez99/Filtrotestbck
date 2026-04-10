import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BitPredict Strategy Backtester",
    page_icon="₿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── STYLES ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

:root {
    --bg:        #080d14;
    --bg2:       #0d1520;
    --bg3:       #111d2e;
    --accent:    #00e5ff;
    --accent2:   #ff6b35;
    --green:     #00e676;
    --red:       #ff1744;
    --yellow:    #ffd600;
    --text:      #e8edf5;
    --muted:     #5a7080;
    --border:    #1a2d40;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Syne', sans-serif !important;
}

[data-testid="stSidebar"] {
    background-color: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] * {
    color: var(--text) !important;
}

input[type="number"],
input[type="text"],
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {
    background-color: var(--bg3) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    caret-color: var(--accent) !important;
}

[data-testid="stNumberInput"] button {
    background-color: var(--bg3) !important;
    color: var(--accent) !important;
    border: 1px solid var(--border) !important;
}

[data-testid="stNumberInput"] button:hover {
    background-color: var(--border) !important;
    color: var(--text) !important;
}

[data-testid="stSelectbox"] > div > div,
[data-baseweb="select"] > div {
    background-color: var(--bg3) !important;
    color: var(--text) !important;
    border-color: var(--border) !important;
}

[data-baseweb="select"] span,
[data-baseweb="select"] div {
    color: var(--text) !important;
    background-color: transparent !important;
}

[data-baseweb="popover"] li,
[role="option"] {
    background-color: var(--bg3) !important;
    color: var(--text) !important;
}

[role="option"]:hover {
    background-color: var(--border) !important;
}

[data-baseweb="tag"] {
    background-color: rgba(0,229,255,0.15) !important;
    color: var(--accent) !important;
}

[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
    background-color: var(--accent) !important;
    border-color: var(--accent) !important;
}

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
    color: var(--text) !important;
}

[data-testid="stTextInput"] > div > div {
    background-color: var(--bg3) !important;
    border-color: var(--border) !important;
}

h1, h2, h3, h4 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    color: var(--text) !important;
}

.stSelectbox > div > div,
.stMultiSelect > div > div,
.stSlider > div {
    background-color: var(--bg3) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
}

.stButton > button {
    background: linear-gradient(135deg, var(--accent), #0099bb) !important;
    color: #000 !important;
    font-family: 'Space Mono', monospace !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 0.6rem 2rem !important;
    letter-spacing: 0.05em !important;
    transition: all 0.2s !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(0,229,255,0.3) !important;
}

/* ── Botones Seguir / Invertir ── */
.dir-btn-active-seguir {
    display: block;
    width: 100%;
    padding: 0.55rem 0;
    background: rgba(0,230,118,0.15) !important;
    border: 2px solid #00e676 !important;
    border-radius: 6px;
    color: #00e676 !important;
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    cursor: pointer;
    text-align: center;
    margin-bottom: 0.4rem;
}

.dir-btn-active-invertir {
    display: block;
    width: 100%;
    padding: 0.55rem 0;
    background: rgba(255,23,68,0.15) !important;
    border: 2px solid #ff1744 !important;
    border-radius: 6px;
    color: #ff1744 !important;
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    cursor: pointer;
    text-align: center;
    margin-bottom: 0.4rem;
}

.dir-btn-inactive {
    display: block;
    width: 100%;
    padding: 0.55rem 0;
    background: transparent !important;
    border: 1px solid #1a2d40 !important;
    border-radius: 6px;
    color: #5a7080 !important;
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    font-weight: 400;
    letter-spacing: 0.1em;
    cursor: pointer;
    text-align: center;
    margin-bottom: 0.4rem;
}

/* Override default stButton solo para los direction buttons */
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    color: var(--muted) !important;
    border: 1px solid var(--border) !important;
    box-shadow: none !important;
    font-size: 0.8rem !important;
    padding: 0.45rem 0.5rem !important;
    width: 100% !important;
}

.metric-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.5rem;
}

.metric-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 0.3rem;
}

.metric-value {
    font-family: 'Space Mono', monospace;
    font-size: 1.6rem;
    font-weight: 700;
    line-height: 1;
}

.metric-value.green  { color: var(--green); }
.metric-value.red    { color: var(--red); }
.metric-value.cyan   { color: var(--accent); }
.metric-value.yellow { color: var(--yellow); }
.metric-value.white  { color: var(--text); }

.section-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.2em;
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
}

.stDataFrame { background-color: var(--bg2) !important; }

.stTabs [data-baseweb="tab-list"] {
    background-color: var(--bg2) !important;
    border-bottom: 1px solid var(--border) !important;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
    color: var(--muted) !important;
    letter-spacing: 0.1em !important;
}

.stTabs [aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom: 2px solid var(--accent) !important;
}

.pill {
    display: inline-block;
    background: rgba(0,229,255,0.1);
    border: 1px solid rgba(0,229,255,0.3);
    color: var(--accent);
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    letter-spacing: 0.1em;
}

.pill.orange {
    background: rgba(255,107,53,0.1);
    border-color: rgba(255,107,53,0.3);
    color: var(--accent2);
}

div[data-testid="stVerticalBlock"] > div {
    background-color: transparent !important;
}
</style>
""", unsafe_allow_html=True)


# ─── GOOGLE SHEETS LOADER ─────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_from_gsheet(sheet_url: str) -> pd.DataFrame:
    sheet_id = sheet_url.split("/d/")[1].split("/")[0]
    csv_urls = [
        f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Pretester%20Live",
        f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&sheet=Pretester%20Live",
        f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv",
    ]
    df = None
    for url in csv_urls:
        try:
            df = pd.read_csv(url)
            if len(df) > 10:
                break
        except Exception:
            continue
    return df


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.str.strip()

    if 'Timestamp CST' in df.columns:
        df['Timestamp CST'] = pd.to_datetime(df['Timestamp CST'], errors='coerce')
        df['Fecha']    = df['Timestamp CST'].dt.date
        df['Hora_num'] = df['Timestamp CST'].dt.hour + df['Timestamp CST'].dt.minute / 60

    if 'Hora Local' in df.columns:
        def parse_hora(val):
            try:
                if pd.isna(val): return None
                s = str(val).strip()
                if ':' in s:
                    parts = s.split(':')
                    return int(parts[0]) * 60 + int(parts[1])
                fval = float(val)
                fval = fval - int(fval)
                h = int(fval * 24)
                m = int((fval * 24 - h) * 60)
                return h * 60 + m
            except Exception:
                return None
        df['HoraMin'] = df['Hora Local'].apply(parse_hora)

    if 'Hora_num' in df.columns and ('HoraMin' not in df.columns or df['HoraMin'].isna().all()):
        df['HoraMin'] = (df['Hora_num'] * 60).astype(int)

    for col in ['Confianza %', 'Poly UP Ask', 'Poly UP Bid', 'Poly DOWN Ask', 'Poly DOWN Bid', 'UP %', 'DOWN %']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    for col in ['Prediccion', 'Tier', 'Correcto', 'Bet Side']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.upper()

    df = df.dropna(subset=['Timestamp CST'])
    return df


# ─── STRATEGY ENGINE ──────────────────────────────────────────────────────────
def run_strategy(df: pd.DataFrame, params: dict) -> pd.DataFrame:
    data = df.copy()

    if params['tiers']:
        data = data[data['Tier'].isin([t.upper() for t in params['tiers']])]

    h_start = params['hora_start'] * 60 + params['hora_start_min']
    h_end   = params['hora_end']   * 60 + params['hora_end_min']
    if 'HoraMin' in data.columns:
        if h_start <= h_end:
            data = data[(data['HoraMin'] >= h_start) & (data['HoraMin'] <= h_end)]
        else:
            data = data[(data['HoraMin'] >= h_start) | (data['HoraMin'] <= h_end)]

    if 'Confianza %' in data.columns:
        data = data[data['Confianza %'] >= params['confianza_min']]

    invertir = params.get('invertir', False)

    def get_bet(row):
        pred = str(row.get('Prediccion', '')).upper()
        # Si invertir: apostamos lo contrario
        if invertir:
            direccion = 'DOWN' if pred == 'UP' else 'UP'
        else:
            direccion = pred

        if direccion == 'UP':
            ep       = row.get('Poly UP Ask', np.nan)
            bet_side = 'Up'
        else:
            ep       = row.get('Poly DOWN Ask', np.nan)
            bet_side = 'Down'
        return pd.Series({'Entry Price': ep, 'Bet Side': bet_side, 'Direccion Bet': direccion})

    bet_info = data.apply(get_bet, axis=1)
    data['Entry Price']   = bet_info['Entry Price']
    data['Bet Side']      = bet_info['Bet Side']
    data['Direccion Bet'] = bet_info['Direccion Bet']

    data = data[data['Entry Price'].notna()]
    data = data[(data['Entry Price'] >= params['quote_min']) &
                (data['Entry Price'] <= params['quote_max'])]
    data = data[(data['Entry Price'] > 0) & (data['Entry Price'] < 1)]

    data['Stake USD'] = params['target_win'] * data['Entry Price'] / (1 - data['Entry Price'])

    def calc_pnl(row):
        corr      = str(row.get('Correcto', '')).upper()
        dir_real  = str(row.get('Direccion Real', row.get('Direccion Real', ''))).upper()
        dir_bet   = str(row.get('Direccion Bet', '')).upper()

        if invertir:
            # Ganamos si la dirección real es OPUESTA a la predicción
            # es decir, si dir_bet == dir_real
            ganamos = (dir_bet == dir_real) if dir_real else (corr == 'NO')
        else:
            ganamos = (corr == 'SI')

        if ganamos:
            return params['target_win'], 'Gano'
        else:
            return -row['Stake USD'], 'Perdio'

    results = data.apply(calc_pnl, axis=1, result_type='expand')
    data['PnL Trade']     = results[0]
    data['Resultado']     = results[1]
    data['PnL Acumulado'] = data['PnL Trade'].cumsum()

    return data.reset_index(drop=True)


def build_resumen_dia(trades: pd.DataFrame) -> pd.DataFrame:
    if trades.empty or 'Fecha' not in trades.columns:
        return pd.DataFrame()
    g = trades.groupby('Fecha').agg(
        Trades      = ('PnL Trade', 'count'),
        Ganadas     = ('Resultado', lambda x: (x == 'Gano').sum()),
        Perdidas    = ('Resultado', lambda x: (x == 'Perdio').sum()),
        PnL_Total   = ('PnL Trade', 'sum'),
        Mejor       = ('PnL Trade', 'max'),
        Peor        = ('PnL Trade', 'min'),
        Stake_Total = ('Stake USD', 'sum'),
    ).reset_index()
    g['Win Rate'] = g['Ganadas'] / g['Trades']
    return g


# ─── PLOTTING ─────────────────────────────────────────────────────────────────
PLOT_TEMPLATE = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(13,21,32,0.8)',
    font=dict(family='Space Mono, monospace', color='#8a9db5', size=11),
    margin=dict(l=10, r=10, t=30, b=10),
)

def plot_equity_curve(trades: pd.DataFrame):
    if trades.empty: return None
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=trades.index,
        y=trades['PnL Acumulado'],
        mode='lines',
        line=dict(color='#00e5ff', width=2),
        fill='tozeroy',
        fillcolor='rgba(0,229,255,0.05)',
        hovertemplate='Trade %{x}<br>P&L: $%{y:,.2f}<extra></extra>'
    ))
    fig.add_hline(y=0, line_color='#1a2d40', line_width=1)
    fig.update_layout(**PLOT_TEMPLATE, height=280, showlegend=False,
                      title=dict(text='EQUITY CURVE', font=dict(size=10, color='#00e5ff')))
    fig.update_xaxes(gridcolor='#1a2d40', showline=False, zeroline=False)
    fig.update_yaxes(gridcolor='#1a2d40', showline=False, zeroline=False)
    return fig


def plot_pnl_por_dia(resumen: pd.DataFrame):
    if resumen.empty: return None
    colors = ['#00e676' if v >= 0 else '#ff1744' for v in resumen['PnL_Total']]
    fig = go.Figure(go.Bar(
        x=resumen['Fecha'].astype(str),
        y=resumen['PnL_Total'],
        marker_color=colors,
        hovertemplate='%{x}<br>P&L: $%{y:,.2f}<extra></extra>'
    ))
    fig.update_layout(**PLOT_TEMPLATE, height=240,
                      title=dict(text='P&L POR DIA', font=dict(size=10, color='#00e5ff')))
    fig.update_xaxes(gridcolor='#1a2d40', showline=False, zeroline=False)
    fig.update_yaxes(gridcolor='#1a2d40', showline=False, zeroline=False)
    return fig


def plot_winrate_dia(resumen: pd.DataFrame):
    if resumen.empty: return None
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=resumen['Fecha'].astype(str),
        y=resumen['Win Rate'] * 100,
        marker_color=[
            '#00e676' if v >= 60 else '#ffd600' if v >= 50 else '#ff1744'
            for v in resumen['Win Rate'] * 100
        ],
        hovertemplate='%{x}<br>Win Rate: %{y:.1f}%<extra></extra>'
    ))
    fig.add_hline(y=50, line_dash='dash', line_color='#5a7080', line_width=1)
    fig.add_hline(y=60, line_dash='dot',  line_color='#00e676', line_width=1)
    fig.update_layout(**PLOT_TEMPLATE, height=240,
                      title=dict(text='WIN RATE POR DIA', font=dict(size=10, color='#00e5ff')))
    fig.update_xaxes(gridcolor='#1a2d40', showline=False, zeroline=False)
    fig.update_yaxes(gridcolor='#1a2d40', showline=False, zeroline=False,
                     range=[0, 100], ticksuffix='%')
    return fig


def plot_distribucion_horas(trades: pd.DataFrame):
    if trades.empty or 'HoraMin' not in trades.columns: return None
    trades = trades.copy()
    trades['Hora'] = (trades['HoraMin'] // 60).astype(int)
    grp = trades.groupby('Hora').agg(
        Trades  = ('PnL Trade', 'count'),
        Ganadas = ('Resultado', lambda x: (x == 'Gano').sum())
    ).reset_index()
    grp['WR'] = grp['Ganadas'] / grp['Trades']
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=grp['Hora'].astype(str) + 'h',
        y=grp['Trades'],
        name='Trades',
        marker_color='rgba(0,229,255,0.4)',
        hovertemplate='%{x}<br>Trades: %{y}<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=grp['Hora'].astype(str) + 'h',
        y=grp['WR'] * 100,
        name='Win Rate %',
        yaxis='y2',
        line=dict(color='#ffd600', width=2),
        mode='lines+markers',
        hovertemplate='%{x}<br>WR: %{y:.1f}%<extra></extra>'
    ))
    fig.update_layout(
        **PLOT_TEMPLATE, height=260,
        yaxis2=dict(
            overlaying='y', side='right',
            ticksuffix='%', range=[0, 110],
            gridcolor='rgba(0,0,0,0)',
            showline=False, zeroline=False,
            tickfont=dict(color='#8a9db5')
        ),
        legend=dict(orientation='h', y=1.05, font=dict(size=9)),
        title=dict(text='DISTRIBUCION POR HORA', font=dict(size=10, color='#00e5ff'))
    )
    fig.update_xaxes(gridcolor='#1a2d40', showline=False, zeroline=False)
    fig.update_yaxes(gridcolor='#1a2d40', showline=False, zeroline=False)
    return fig


# ─── METRIC CARD ──────────────────────────────────────────────────────────────
def metric_card(label, value, color='white', prefix='', suffix=''):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value {color}">{prefix}{value}{suffix}</div>
    </div>
    """, unsafe_allow_html=True)


# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():

    # Inicializar estado de dirección
    if 'direccion' not in st.session_state:
        st.session_state['direccion'] = 'seguir'

    st.markdown("""
    <div style="display:flex; align-items:center; gap:1rem; margin-bottom:2rem;
                padding:1.5rem 2rem; background:linear-gradient(90deg,#0d1520,#111d2e);
                border:1px solid #1a2d40; border-radius:8px;">
        <div style="font-size:2rem;">₿</div>
        <div>
            <div style="font-family:'Syne',sans-serif; font-size:1.4rem; font-weight:800;
                        color:#e8edf5; letter-spacing:-0.02em;">BitPredict Strategy Backtester</div>
            <div style="font-family:'Space Mono',monospace; font-size:0.65rem;
                        color:#5a7080; letter-spacing:0.15em;">POLYMARKET · TIER D · BTC BINARY</div>
        </div>
        <div style="margin-left:auto; display:flex; gap:0.5rem;">
            <span class="pill">LIVE DATA</span>
            <span class="pill orange">GOOGLE SHEETS</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── SIDEBAR ───────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown('<div class="section-title">⚙ CONFIGURACION</div>', unsafe_allow_html=True)

        sheet_url = st.text_input(
            "Google Sheet URL",
            value="https://docs.google.com/spreadsheets/d/16WpLTAT7GebiuW3XFS7TyyYCSgq5_gyWrmQuqxwG37I/edit?usp=sharing",
        )

        st.markdown("---")
        st.markdown('<div class="section-title">📋 ESTRATEGIA</div>', unsafe_allow_html=True)
        strategy_mode = st.selectbox(
            "Modo",
            ["🎯 Combo Strategy (Filtros activos)", "📊 Sin estrategia (todos los trades)"],
        )
        use_filters = strategy_mode.startswith("🎯")

        st.markdown("---")
        st.markdown('<div class="section-title">🏷 TIER</div>', unsafe_allow_html=True)
        tiers = st.multiselect("Tiers a incluir", ['S', 'A', 'B', 'C', 'D'], default=['D'])

        # ── DIRECCION ─────────────────────────────────────────────────────────
        st.markdown("---")
        st.markdown('<div class="section-title">🎲 DIRECCION DE APUESTA</div>', unsafe_allow_html=True)

        es_seguir   = st.session_state['direccion'] == 'seguir'
        es_invertir = st.session_state['direccion'] == 'invertir'

        # Badge de estado actual
        badge_color = "#00e676" if es_seguir else "#ff1744"
        badge_text  = "✅ SIGUIENDO PREDICCION" if es_seguir else "🔄 INVIRTIENDO PREDICCION"
        st.markdown(f"""
        <div style="background: rgba({'0,230,118' if es_seguir else '255,23,68'},0.1);
                    border: 1px solid {'#00e676' if es_seguir else '#ff1744'};
                    border-radius: 6px; padding: 0.5rem 0.8rem;
                    font-family: 'Space Mono', monospace; font-size: 0.6rem;
                    color: {'#00e676' if es_seguir else '#ff1744'};
                    text-align: center; letter-spacing: 0.08em; margin-bottom: 0.6rem;">
            {badge_text}
        </div>
        """, unsafe_allow_html=True)

        col_s, col_i = st.columns(2)
        with col_s:
            if st.button("✅ Seguir", use_container_width=True, key="btn_seguir"):
                st.session_state['direccion'] = 'seguir'
                st.rerun()
        with col_i:
            if st.button("🔄 Invertir", use_container_width=True, key="btn_invertir"):
                st.session_state['direccion'] = 'invertir'
                st.rerun()

        st.markdown("---")
        st.markdown('<div class="section-title">⏰ HORARIO CST</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            hora_start     = st.number_input("Hora inicio", 0, 23, 15, step=1)
            hora_start_min = st.selectbox("Min inicio", [0,5,10,15,20,25,30,35,40,45,50,55], index=0)
        with col2:
            hora_end     = st.number_input("Hora fin", 0, 23, 19, step=1)
            hora_end_min = st.selectbox("Min fin",   [0,5,10,15,20,25,30,35,40,45,50,55], index=11)

        st.markdown("---")
        st.markdown('<div class="section-title">📈 CONFIANZA</div>', unsafe_allow_html=True)
        confianza_min = st.slider(
            "Confianza mínima (%)",
            min_value=0.0, max_value=100.0,
            value=0.0 if not use_filters else 50.0,
            step=1.0, disabled=not use_filters
        )

        st.markdown("---")
        st.markdown('<div class="section-title">💹 RANGO DE CUOTAS</div>', unsafe_allow_html=True)
        quote_range = st.slider(
            "Entry Price (Ask)",
            min_value=0.01, max_value=0.99,
            value=(0.38, 0.99) if not use_filters else (0.55, 0.99),
            step=0.01, format="%.2f", disabled=not use_filters
        )

        st.markdown("---")
        st.markdown('<div class="section-title">💰 OBJETIVO</div>', unsafe_allow_html=True)
        target_win = st.number_input(
            "Ganancia objetivo por trade ($)",
            min_value=100, max_value=100000, value=1000, step=100
        )

        st.markdown("---")
        run_btn = st.button("▶  EJECUTAR BACKTEST", use_container_width=True)

    invertir = st.session_state['direccion'] == 'invertir'

    # ── PARAMS ────────────────────────────────────────────────────────────────
    params = dict(
        tiers          = tiers if tiers else ['D'],
        hora_start     = int(hora_start),
        hora_start_min = int(hora_start_min),
        hora_end       = int(hora_end),
        hora_end_min   = int(hora_end_min),
        confianza_min  = float(confianza_min) if use_filters else 0.0,
        quote_min      = float(quote_range[0]) if use_filters else 0.01,
        quote_max      = float(quote_range[1]) if use_filters else 0.99,
        target_win     = float(target_win),
        invertir       = invertir,
    )

    # ── LOAD & RUN ────────────────────────────────────────────────────────────
    if run_btn or 'trades' not in st.session_state:
        with st.spinner("Cargando datos desde Google Sheets..."):
            raw = load_from_gsheet(sheet_url)

        if raw is None or raw.empty:
            st.error("❌ No se pudo cargar el Google Sheet. Verifica que sea público.")
            st.stop()

        df = clean_dataframe(raw)

        with st.spinner("Procesando backtest..."):
            trades  = run_strategy(df, params)
            resumen = build_resumen_dia(trades)

        st.session_state['trades']  = trades
        st.session_state['resumen'] = resumen
        st.session_state['params']  = params

    trades  = st.session_state.get('trades',  pd.DataFrame())
    resumen = st.session_state.get('resumen', pd.DataFrame())

    if trades.empty:
        st.warning("⚠️ Sin trades con los filtros aplicados. Ajusta los parámetros.")
        st.stop()

    # ── BANNER MODO ACTIVO ────────────────────────────────────────────────────
    p_saved = st.session_state.get('params', params)
    if p_saved.get('invertir', False):
        st.markdown("""
        <div style="background:rgba(255,23,68,0.08); border:1px solid #ff1744;
                    border-radius:6px; padding:0.6rem 1.2rem; margin-bottom:1rem;
                    font-family:'Space Mono',monospace; font-size:0.7rem;
                    color:#ff1744; letter-spacing:0.08em;">
            🔄 MODO INVERTIR ACTIVO — apostando lo contrario a la predicción
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:rgba(0,230,118,0.06); border:1px solid #00e676;
                    border-radius:6px; padding:0.6rem 1.2rem; margin-bottom:1rem;
                    font-family:'Space Mono',monospace; font-size:0.7rem;
                    color:#00e676; letter-spacing:0.08em;">
            ✅ MODO SEGUIR ACTIVO — apostando según la predicción
        </div>
        """, unsafe_allow_html=True)

    # ─── TABS ─────────────────────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["  📊  DASHBOARD  ", "  📋  DETALLE  ", "  📅  RESUMEN POR DIA  "])

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 1 — DASHBOARD
    # ══════════════════════════════════════════════════════════════════════════
    with tab1:
        total    = len(trades)
        ganadas  = (trades['Resultado'] == 'Gano').sum()
        perdidas = total - ganadas
        wr       = ganadas / total if total > 0 else 0
        pl_total = trades['PnL Trade'].sum()
        avg_perd = trades[trades['Resultado'] == 'Perdio']['PnL Trade'].mean() if perdidas > 0 else 0
        best     = trades['PnL Trade'].max()
        worst    = trades['PnL Trade'].min()

        c1, c2, c3, c4, c5 = st.columns(5)
        with c1: metric_card("TOTAL TRADES", f"{total:,}", "cyan")
        with c2:
            wrc = "green" if wr >= 0.6 else "yellow" if wr >= 0.5 else "red"
            metric_card("WIN RATE", f"{wr*100:.1f}", wrc, suffix="%")
        with c3: metric_card("GANADAS",  f"{ganadas:,}",  "green")
        with c4: metric_card("PERDIDAS", f"{perdidas:,}", "red")
        with c5:
            plc = "green" if pl_total >= 0 else "red"
            metric_card("P&L TOTAL", f"{pl_total:,.0f}", plc, prefix="$")

        st.markdown("<br>", unsafe_allow_html=True)

        c6, c7, c8, c9 = st.columns(4)
        with c6: metric_card("AVG GANANCIA", f"{target_win:,.0f}", "green", prefix="$")
        with c7: metric_card("AVG PERDIDA",  f"{avg_perd:,.0f}",  "red",   prefix="$")
        with c8: metric_card("MEJOR TRADE",  f"{best:,.0f}",      "green", prefix="$")
        with c9: metric_card("PEOR TRADE",   f"{worst:,.0f}",     "red",   prefix="$")

        st.markdown("<br>", unsafe_allow_html=True)

        col_a, col_b = st.columns([3, 2])
        with col_a:
            fig = plot_equity_curve(trades)
            if fig: st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        with col_b:
            fig = plot_pnl_por_dia(resumen)
            if fig: st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        col_c, col_d = st.columns([2, 3])
        with col_c:
            fig = plot_winrate_dia(resumen)
            if fig: st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        with col_d:
            fig = plot_distribucion_horas(trades)
            if fig: st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        st.markdown('<div class="section-title" style="margin-top:1rem;">FILTROS APLICADOS</div>', unsafe_allow_html=True)
        p    = st.session_state.get('params', params)
        cols = st.columns(7)
        info = [
            ("Tier",        ', '.join(p['tiers'])),
            ("Hora inicio", f"{p['hora_start']:02d}:{p['hora_start_min']:02d}"),
            ("Hora fin",    f"{p['hora_end']:02d}:{p['hora_end_min']:02d}"),
            ("Confianza ≥", f"{p['confianza_min']:.0f}%"),
            ("Entry Price", f"{p['quote_min']:.2f} – {p['quote_max']:.2f}"),
            ("Objetivo",    f"${p['target_win']:,.0f}"),
            ("Dirección",   "INVERTIR 🔄" if p.get('invertir') else "SEGUIR ✅"),
        ]
        for col, (lbl, val) in zip(cols, info):
            with col:
                color = "#ff1744" if lbl == "Dirección" and p.get('invertir') else "#00e5ff"
                st.markdown(f"""
                <div style="background:#0d1520; border:1px solid #1a2d40; border-radius:6px;
                            padding:0.7rem 0.8rem; text-align:center;">
                    <div style="font-family:'Space Mono',monospace; font-size:0.55rem;
                                color:#5a7080; text-transform:uppercase; letter-spacing:0.08em;">{lbl}</div>
                    <div style="font-family:'Space Mono',monospace; font-size:0.8rem;
                                color:{color}; font-weight:700; margin-top:0.2rem;">{val}</div>
                </div>
                """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 2 — DETALLE
    # ══════════════════════════════════════════════════════════════════════════
    with tab2:
        st.markdown('<div class="section-title">DETALLE DE TRADES</div>', unsafe_allow_html=True)

        detail_cols = ['Timestamp CST', 'Fecha', 'Prediccion', 'Bet Side', 'Entry Price',
                       'Stake USD', 'Resultado', 'PnL Trade', 'PnL Acumulado',
                       'Poly UP Ask', 'Poly DOWN Ask', 'Poly UP Bid', 'Poly DOWN Bid']
        avail   = [c for c in detail_cols if c in trades.columns]
        df_show = trades[avail].copy()

        for c in ['Entry Price', 'Poly UP Ask', 'Poly DOWN Ask', 'Poly UP Bid', 'Poly DOWN Bid']:
            if c in df_show.columns:
                df_show[c] = df_show[c].map(lambda x: f"{x:.2f}" if pd.notna(x) else '')
        for c in ['Stake USD', 'PnL Trade', 'PnL Acumulado']:
            if c in df_show.columns:
                df_show[c] = df_show[c].map(lambda x: f"${x:,.2f}" if pd.notna(x) else '')

        def highlight(row):
            if 'Resultado' in row.index:
                if row['Resultado'] == 'Gano':
                    return ['background-color: rgba(0,230,118,0.06)'] * len(row)
                elif row['Resultado'] == 'Perdio':
                    return ['background-color: rgba(255,23,68,0.06)'] * len(row)
            return [''] * len(row)

        st.dataframe(
            df_show.style.apply(highlight, axis=1),
            use_container_width=True,
            height=520,
        )

        csv = trades[avail].to_csv(index=False).encode('utf-8')
        st.download_button("⬇  Descargar CSV", csv,
                           file_name="bitpredict_detalle.csv", mime="text/csv")

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 3 — RESUMEN POR DÍA
    # ══════════════════════════════════════════════════════════════════════════
    with tab3:
        st.markdown('<div class="section-title">RESUMEN POR DIA</div>', unsafe_allow_html=True)

        if not resumen.empty:
            res_show = resumen.copy()
            res_show['Win Rate']    = res_show['Win Rate'].map(lambda x: f"{x*100:.1f}%")
            res_show['PnL_Total']   = res_show['PnL_Total'].map(lambda x: f"${x:,.2f}")
            res_show['Mejor']       = res_show['Mejor'].map(lambda x: f"${x:,.2f}")
            res_show['Peor']        = res_show['Peor'].map(lambda x: f"${x:,.2f}")
            res_show['Stake_Total'] = res_show['Stake_Total'].map(lambda x: f"${x:,.2f}")
            res_show.columns = ['Fecha','Trades','Ganadas','Perdidas','Win Rate',
                                'P&L Total','Mejor Trade','Peor Trade','Stake Total']

            def hl_resumen(row):
                try:
                    pl = float(str(row['P&L Total']).replace('$','').replace(',',''))
                    if pl > 0: return ['background-color: rgba(0,230,118,0.06)'] * len(row)
                    if pl < 0: return ['background-color: rgba(255,23,68,0.06)'] * len(row)
                except Exception:
                    pass
                return [''] * len(row)

            st.dataframe(
                res_show.style.apply(hl_resumen, axis=1),
                use_container_width=True,
                height=420,
            )

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-title">TOTALES ACUMULADOS</div>', unsafe_allow_html=True)

            total_trades_r = resumen['Trades'].sum()
            total_won_r    = resumen['Ganadas'].sum()
            total_pl_r     = resumen['PnL_Total'].sum()
            total_stk_r    = resumen['Stake_Total'].sum()
            avg_wr_r       = (total_won_r / total_trades_r) if total_trades_r > 0 else 0
            best_day       = resumen.loc[resumen['PnL_Total'].idxmax(), 'Fecha'] if not resumen.empty else '-'
            worst_day      = resumen.loc[resumen['PnL_Total'].idxmin(), 'Fecha'] if not resumen.empty else '-'

            c1, c2, c3, c4, c5, c6 = st.columns(6)
            with c1: metric_card("TOTAL TRADES",    f"{total_trades_r:,}",  "cyan")
            with c2: metric_card("WIN RATE GLOBAL", f"{avg_wr_r*100:.1f}",  "green" if avg_wr_r >= 0.5 else "red", suffix="%")
            with c3: metric_card("P&L ACUMULADO",   f"{total_pl_r:,.0f}",  "green" if total_pl_r >= 0 else "red", prefix="$")
            with c4: metric_card("STAKE TOTAL",     f"{total_stk_r:,.0f}", "white", prefix="$")
            with c5: metric_card("MEJOR DIA",       str(best_day),         "green")
            with c6: metric_card("PEOR DIA",        str(worst_day),        "red")

            csv2 = resumen.to_csv(index=False).encode('utf-8')
            st.download_button("⬇  Descargar Resumen CSV", csv2,
                               file_name="bitpredict_resumen.csv", mime="text/csv")
        else:
            st.info("Sin datos para mostrar resumen.")


if __name__ == "__main__":
    main()
