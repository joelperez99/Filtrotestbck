import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import io

st.set_page_config(
    page_title="BitPredict Strategy Backtester",
    page_icon="₿",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

:root {
    --bg:      #080d14;
    --bg2:     #0d1520;
    --bg3:     #111d2e;
    --accent:  #00e5ff;
    --accent2: #ff6b35;
    --green:   #00e676;
    --red:     #ff1744;
    --yellow:  #ffd600;
    --text:    #e8edf5;
    --muted:   #5a7080;
    --border:  #1a2d40;
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

[data-testid="stSidebar"] * { color: var(--text) !important; }

input[type="number"], input[type="text"],
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {
    background-color: var(--bg3) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
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

[data-baseweb="popover"] li, [role="option"] {
    background-color: var(--bg3) !important;
    color: var(--text) !important;
}

[role="option"]:hover { background-color: var(--border) !important; }

[data-baseweb="tag"] {
    background-color: rgba(0,229,255,0.15) !important;
    color: var(--accent) !important;
}

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span { color: var(--text) !important; }

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

/* ── Todos los botones del sidebar ── */
[data-testid="stSidebar"] .stButton > button {
    background: var(--bg3) !important;
    color: var(--muted) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.72rem !important;
    padding: 0.3rem 0.1rem !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    min-height: 2rem !important;
    letter-spacing: 0.02em !important;
    transition: all 0.15s !important;
    box-shadow: none !important;
    width: 100% !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
}

/* ── Botones de hora ACTIVOS (contienen corchetes) ── */
[data-testid="stSidebar"] .stButton > button[data-active="true"] {
    background: rgba(0,229,255,0.15) !important;
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    font-weight: 700 !important;
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
    margin-bottom: 0.8rem;
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

div[data-testid="stVerticalBlock"] > div { background-color: transparent !important; }
</style>
""", unsafe_allow_html=True)


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
            except: return None
        df['HoraMin'] = df['Hora Local'].apply(parse_hora)
    if 'Hora_num' in df.columns and ('HoraMin' not in df.columns or df['HoraMin'].isna().all()):
        df['HoraMin'] = (df['Hora_num'] * 60).astype(int)
    for col in ['Confianza %','Poly UP Ask','Poly UP Bid','Poly DOWN Ask','Poly DOWN Bid','UP %','DOWN %']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    for col in ['Prediccion','Tier','Correcto','Bet Side']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.upper()
    df = df.dropna(subset=['Timestamp CST'])
    return df


def run_strategy(df: pd.DataFrame, params: dict) -> pd.DataFrame:
    data = df.copy()
    if params.get('meses_sel') and 'Fecha' in data.columns:
        data['_mes'] = pd.to_datetime(data['Fecha']).dt.month
        data = data[data['_mes'].isin(params['meses_sel'])].drop(columns=['_mes'])
    if params.get('dias_sel') and 'Fecha' in data.columns:
        data['_dia'] = pd.to_datetime(data['Fecha']).dt.day
        data = data[data['_dia'].isin(params['dias_sel'])].drop(columns=['_dia'])
    if params['tiers']:
        data = data[data['Tier'].isin([t.upper() for t in params['tiers']])]
    horas_sel = params.get('horas_sel', list(range(24)))
    if horas_sel and 'HoraMin' in data.columns:
        data['_h'] = (data['HoraMin'] // 60).astype(int)
        data = data[data['_h'].isin(horas_sel)]
        data = data.drop(columns=['_h'])
    if 'Confianza %' in data.columns:
        data = data[data['Confianza %'] >= params['confianza_min']]
    invertir = params.get('invertir', False)
    def get_bet(row):
        pred = str(row.get('Prediccion', '')).upper()
        direccion = ('DOWN' if pred == 'UP' else 'UP') if invertir else pred
        if direccion == 'UP':
            return pd.Series({'Entry Price': row.get('Poly UP Ask', np.nan), 'Bet Side': 'Up', 'Direccion Bet': 'UP'})
        else:
            return pd.Series({'Entry Price': row.get('Poly DOWN Ask', np.nan), 'Bet Side': 'Down', 'Direccion Bet': 'DOWN'})
    bet_info = data.apply(get_bet, axis=1)
    data['Entry Price']   = bet_info['Entry Price']
    data['Bet Side']      = bet_info['Bet Side']
    data['Direccion Bet'] = bet_info['Direccion Bet']
    data = data[data['Entry Price'].notna()]
    # Rango base de inclusión
    data = data[(data['Entry Price'] >= params['quote_min']) & (data['Entry Price'] <= params['quote_max'])]
    data = data[(data['Entry Price'] > 0) & (data['Entry Price'] < 1)]
    # Aplicar rangos de exclusión
    for exc_min, exc_max in params.get('exclude_ranges', []):
        data = data[~((data['Entry Price'] >= exc_min) & (data['Entry Price'] <= exc_max))]
    data['Stake USD'] = params['target_win'] * data['Entry Price'] / (1 - data['Entry Price'])
    def calc_pnl(row):
        corr    = str(row.get('Correcto', '')).upper()
        ganamos = (corr != 'SI') if invertir else (corr == 'SI')
        return (params['target_win'], 'Gano') if ganamos else (-row['Stake USD'], 'Perdio')
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
        Ganadas     = ('Resultado', lambda x: (x=='Gano').sum()),
        Perdidas    = ('Resultado', lambda x: (x=='Perdio').sum()),
        PnL_Total   = ('PnL Trade', 'sum'),
        Mejor       = ('PnL Trade', 'max'),
        Peor        = ('PnL Trade', 'min'),
        Stake_Total = ('Stake USD', 'sum'),
    ).reset_index()
    g['Win Rate'] = g['Ganadas'] / g['Trades']
    return g


PLOT_TEMPLATE = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(13,21,32,0.8)',
    font=dict(family='Space Mono, monospace', color='#8a9db5', size=11),
    margin=dict(l=10, r=10, t=30, b=10),
)

def plot_equity_curve(trades):
    if trades.empty: return None
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=trades.index, y=trades['PnL Acumulado'], mode='lines',
        line=dict(color='#00e5ff', width=2), fill='tozeroy',
        fillcolor='rgba(0,229,255,0.05)',
        hovertemplate='Trade %{x}<br>$%{y:,.2f}<extra></extra>'
    ))
    fig.add_hline(y=0, line_color='#1a2d40', line_width=1)
    fig.update_layout(**PLOT_TEMPLATE, height=280, showlegend=False,
                      title=dict(text='EQUITY CURVE', font=dict(size=10, color='#00e5ff')))
    fig.update_xaxes(gridcolor='#1a2d40', showline=False, zeroline=False)
    fig.update_yaxes(gridcolor='#1a2d40', showline=False, zeroline=False)
    return fig

def plot_pnl_por_dia(resumen):
    if resumen.empty: return None
    fig = go.Figure(go.Bar(
        x=resumen['Fecha'].astype(str), y=resumen['PnL_Total'],
        marker_color=['#00e676' if v>=0 else '#ff1744' for v in resumen['PnL_Total']],
        hovertemplate='%{x}<br>$%{y:,.2f}<extra></extra>'
    ))
    fig.update_layout(**PLOT_TEMPLATE, height=240,
                      title=dict(text='P&L POR DIA', font=dict(size=10, color='#00e5ff')))
    fig.update_xaxes(gridcolor='#1a2d40', showline=False, zeroline=False)
    fig.update_yaxes(gridcolor='#1a2d40', showline=False, zeroline=False)
    return fig

def plot_winrate_dia(resumen):
    if resumen.empty: return None
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=resumen['Fecha'].astype(str), y=resumen['Win Rate']*100,
        marker_color=['#00e676' if v>=60 else '#ffd600' if v>=50 else '#ff1744'
                      for v in resumen['Win Rate']*100],
        hovertemplate='%{x}<br>%{y:.1f}%<extra></extra>'
    ))
    fig.add_hline(y=50, line_dash='dash', line_color='#5a7080', line_width=1)
    fig.add_hline(y=60, line_dash='dot',  line_color='#00e676', line_width=1)
    fig.update_layout(**PLOT_TEMPLATE, height=240,
                      title=dict(text='WIN RATE POR DIA', font=dict(size=10, color='#00e5ff')))
    fig.update_xaxes(gridcolor='#1a2d40', showline=False, zeroline=False)
    fig.update_yaxes(gridcolor='#1a2d40', showline=False, zeroline=False,
                     range=[0,100], ticksuffix='%')
    return fig

def plot_distribucion_horas(trades):
    if trades.empty or 'HoraMin' not in trades.columns: return None
    t = trades.copy()
    t['Hora'] = (t['HoraMin'] // 60).astype(int)
    grp = t.groupby('Hora').agg(
        Trades  = ('PnL Trade', 'count'),
        Ganadas = ('Resultado', lambda x: (x=='Gano').sum())
    ).reset_index()
    grp['WR'] = grp['Ganadas'] / grp['Trades']
    fig = go.Figure()
    fig.add_trace(go.Bar(x=grp['Hora'].astype(str)+'h', y=grp['Trades'], name='Trades',
                         marker_color='rgba(0,229,255,0.4)',
                         hovertemplate='%{x}<br>Trades: %{y}<extra></extra>'))
    fig.add_trace(go.Scatter(x=grp['Hora'].astype(str)+'h', y=grp['WR']*100,
                             name='Win Rate %', yaxis='y2',
                             line=dict(color='#ffd600', width=2), mode='lines+markers',
                             hovertemplate='%{x}<br>WR: %{y:.1f}%<extra></extra>'))
    fig.update_layout(**PLOT_TEMPLATE, height=260,
                      yaxis2=dict(overlaying='y', side='right', ticksuffix='%', range=[0,110],
                                  gridcolor='rgba(0,0,0,0)', showline=False, zeroline=False,
                                  tickfont=dict(color='#8a9db5')),
                      legend=dict(orientation='h', y=1.05, font=dict(size=9)),
                      title=dict(text='DISTRIBUCION POR HORA', font=dict(size=10, color='#00e5ff')))
    fig.update_xaxes(gridcolor='#1a2d40', showline=False, zeroline=False)
    fig.update_yaxes(gridcolor='#1a2d40', showline=False, zeroline=False)
    return fig


def build_excel_download(trades: pd.DataFrame) -> bytes:
    col_map = {
        'Timestamp CST': 'Timestamp Monterrey',
        'Bet Side':       'Bet Side',
        'Stake USD':      'Stake',
        'Entry Price':    'Entry Price',
        'Correcto':       'Correcto',
        'PnL Trade':      'PL',
    }
    avail = {k: v for k, v in col_map.items() if k in trades.columns}
    df_xl = trades[list(avail.keys())].rename(columns=avail).copy()
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_xl.to_excel(writer, index=False, sheet_name='Trades Filtrados')
        ws = writer.sheets['Trades Filtrados']
        for col_cells in ws.columns:
            max_len = max(len(str(cell.value)) if cell.value else 0 for cell in col_cells)
            ws.column_dimensions[col_cells[0].column_letter].width = max_len + 4
    return output.getvalue()


PRESETS = {
    "TIER D INVERTIDA": {
        "tiers":         ["D"],
        "direccion":     "invertir",
        "horas_sel":     [0, 1, 5, 6, 11, 12, 13, 14, 20, 22, 23],
        "quote_min":     0.35,
        "quote_max":     0.99,
        "confianza_min": 0.0,
    },
    "TIER D SIGUIENDO": {
        "tiers":         ["D"],
        "direccion":     "seguir",
        "horas_sel":     [2, 3, 15, 16, 17, 18, 19],
        "quote_min":     0.50,
        "quote_max":     0.99,
        "confianza_min": 0.0,
    },
}

MESES_NAMES = {
    1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril",
    5:"Mayo",  6:"Junio",   7:"Julio", 8:"Agosto",
    9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre",
}


def metric_card(label, value, color='white', prefix='', suffix=''):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value {color}">{prefix}{value}{suffix}</div>
    </div>
    """, unsafe_allow_html=True)


def main():
    if 'direccion'           not in st.session_state: st.session_state['direccion']           = 'seguir'
    if 'horas_sel'           not in st.session_state: st.session_state['horas_sel']           = list(range(24))
    if 'tiers_widget'        not in st.session_state: st.session_state['tiers_widget']        = ['D']
    if 'confianza_widget'    not in st.session_state: st.session_state['confianza_widget']    = 0.0
    if 'quote_range_widget'  not in st.session_state: st.session_state['quote_range_widget']  = (0.38, 0.99)
    if 'strategy_mode_widget' not in st.session_state: st.session_state['strategy_mode_widget'] = "🎯 Combo Strategy (Filtros activos)"

    _trades_ready = 'trades' in st.session_state and not st.session_state['trades'].empty
    _col_hdr, _col_dl = st.columns([5, 1])
    with _col_hdr:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:1rem;margin-bottom:2rem;
                    padding:1.5rem 2rem;background:linear-gradient(90deg,#0d1520,#111d2e);
                    border:1px solid #1a2d40;border-radius:8px;">
            <div style="font-size:2rem;">₿</div>
            <div>
                <div style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:800;
                            color:#e8edf5;letter-spacing:-0.02em;">BitPredict Strategy Backtester</div>
                <div style="font-family:'Space Mono',monospace;font-size:0.65rem;
                            color:#5a7080;letter-spacing:0.15em;">POLYMARKET · TIER D · BTC BINARY</div>
            </div>
            <div style="margin-left:auto;display:flex;gap:0.5rem;">
                <span class="pill">LIVE DATA</span>
                <span class="pill orange">GOOGLE SHEETS</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with _col_dl:
        st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
        if _trades_ready:
            _excel_bytes = build_excel_download(st.session_state['trades'])
            st.download_button(
                label="⬇ Excel",
                data=_excel_bytes,
                file_name="bitpredict_trades.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                key="dl_excel_header",
            )
        else:
            st.markdown("""
            <div style="background:#0d1520;border:1px solid #1a2d40;border-radius:6px;
                        padding:0.6rem;text-align:center;font-family:'Space Mono',monospace;
                        font-size:0.6rem;color:#5a7080;margin-top:0.3rem;">
                ⬇ Excel<br><span style='font-size:0.5rem;'>ejecuta backtest</span>
            </div>
            """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown('<div class="section-title">⚙ CONFIGURACION</div>', unsafe_allow_html=True)
        sheet_url = st.text_input(
            "Google Sheet URL",
            value="https://docs.google.com/spreadsheets/d/16WpLTAT7GebiuW3XFS7TyyYCSgq5_gyWrmQuqxwG37I/edit?usp=sharing",
        )

        st.markdown("---")
        st.markdown('<div class="section-title">⚡ PRESETS</div>', unsafe_allow_html=True)
        st.markdown(
            '<div style="font-family:Space Mono,monospace;font-size:0.58rem;'
            'color:#5a7080;margin-bottom:0.5rem;">Carga configuración predefinida</div>',
            unsafe_allow_html=True,
        )
        _pc1, _pc2 = st.columns(2)
        with _pc1:
            if st.button("🔄 D INVERTIDA", key="preset_invertida", use_container_width=True):
                _pr = PRESETS["TIER D INVERTIDA"]
                st.session_state['tiers_widget']         = _pr['tiers']
                st.session_state['direccion']            = _pr['direccion']
                st.session_state['horas_sel']            = _pr['horas_sel']
                st.session_state['quote_range_widget']   = (_pr['quote_min'], _pr['quote_max'])
                st.session_state['confianza_widget']     = _pr['confianza_min']
                st.session_state['strategy_mode_widget'] = "🎯 Combo Strategy (Filtros activos)"
                st.rerun()
        with _pc2:
            if st.button("✅ D SIGUIENDO", key="preset_siguiendo", use_container_width=True):
                _pr = PRESETS["TIER D SIGUIENDO"]
                st.session_state['tiers_widget']         = _pr['tiers']
                st.session_state['direccion']            = _pr['direccion']
                st.session_state['horas_sel']            = _pr['horas_sel']
                st.session_state['quote_range_widget']   = (_pr['quote_min'], _pr['quote_max'])
                st.session_state['confianza_widget']     = _pr['confianza_min']
                st.session_state['strategy_mode_widget'] = "🎯 Combo Strategy (Filtros activos)"
                st.rerun()

        st.markdown("---")
        st.markdown('<div class="section-title">📋 ESTRATEGIA</div>', unsafe_allow_html=True)
        strategy_mode = st.selectbox("Modo", [
            "🎯 Combo Strategy (Filtros activos)",
            "📊 Sin estrategia (todos los trades)"
        ], key='strategy_mode_widget')
        use_filters = strategy_mode.startswith("🎯")

        st.markdown("---")
        st.markdown('<div class="section-title">🏷 TIER</div>', unsafe_allow_html=True)
        tiers = st.multiselect("Tiers a incluir", ['S','A','B','C','D'], key='tiers_widget')

        # ── DIRECCION ─────────────────────────────────────────────────────────
        st.markdown("---")
        st.markdown('<div class="section-title">🎲 DIRECCION</div>', unsafe_allow_html=True)
        es_seguir = st.session_state['direccion'] == 'seguir'
        st.markdown(f"""
        <div style="background:rgba({'0,230,118' if es_seguir else '255,23,68'},0.1);
                    border:1px solid {'#00e676' if es_seguir else '#ff1744'};
                    border-radius:6px;padding:0.4rem 0.8rem;
                    font-family:'Space Mono',monospace;font-size:0.6rem;
                    color:{'#00e676' if es_seguir else '#ff1744'};
                    text-align:center;letter-spacing:0.08em;margin-bottom:0.5rem;">
            {'✅ SIGUIENDO PREDICCION' if es_seguir else '🔄 INVIRTIENDO PREDICCION'}
        </div>
        """, unsafe_allow_html=True)
        cs, ci = st.columns(2)
        with cs:
            if st.button("✅ Seguir",   key="btn_seguir",   use_container_width=True):
                st.session_state['direccion'] = 'seguir';   st.rerun()
        with ci:
            if st.button("🔄 Invertir", key="btn_invertir", use_container_width=True):
                st.session_state['direccion'] = 'invertir'; st.rerun()

        # ── HORARIO — GRID 24 BOTONES ─────────────────────────────────────────
        st.markdown("---")
        st.markdown('<div class="section-title">⏰ HORARIO CST</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-family:Space Mono,monospace;font-size:0.58rem;color:#5a7080;margin-bottom:0.5rem;">Toca cada hora para activar / desactivar</div>', unsafe_allow_html=True)

        qa, qb, qc = st.columns(3)
        with qa:
            if st.button("Todas",  key="h_all",   use_container_width=True):
                st.session_state['horas_sel'] = list(range(24)); st.rerun()
        with qb:
            if st.button("Ninguna", key="h_none",  use_container_width=True):
                st.session_state['horas_sel'] = []; st.rerun()
        with qc:
            if st.button("Noche",  key="h_night", use_container_width=True):
                st.session_state['horas_sel'] = [0,1,2,3,4,5,6,7,20,21,22,23]; st.rerun()

        # Grid 4 filas × 6 columnas — label limpio: solo el número
        horas_activas = set(st.session_state['horas_sel'])
        for fila in range(4):
            cols_h = st.columns(6)
            for idx, col in enumerate(cols_h):
                hora = fila * 6 + idx
                activa = hora in horas_activas
                with col:
                    label = f"*{hora}" if activa else str(hora)
                    if st.button(label, key=f"h_{hora}", use_container_width=True):
                        if activa:
                            st.session_state['horas_sel'].remove(hora)
                        else:
                            st.session_state['horas_sel'].append(hora)
                        st.rerun()

        active_hours = sorted(horas_activas)
        st.markdown(f"""
        <script>
        (function() {{
            function colorHourBtns() {{
                const active = {active_hours};
                const sidebar = document.querySelector('[data-testid="stSidebar"]');
                if (!sidebar) return;
                const btns = sidebar.querySelectorAll('button');
                btns.forEach(btn => {{
                    const txt = btn.innerText.trim();
                    const match = txt.match(/^\*(\d+)$/);
                    if (match) {{
                        btn.style.background = 'rgba(0,229,255,0.18)';
                        btn.style.borderColor = '#00e5ff';
                        btn.style.color = '#00e5ff';
                        btn.style.fontWeight = '700';
                        btn.innerText = match[1];
                    }}
                }});
            }}
            setTimeout(colorHourBtns, 300);
            setTimeout(colorHourBtns, 800);
        }})();
        </script>
        """, unsafe_allow_html=True)

        horas_sorted = sorted(st.session_state['horas_sel'])
        if horas_sorted:
            horas_str = '  '.join([f"{h:02d}h" for h in horas_sorted])
            st.markdown(f"""
            <div style="background:rgba(0,229,255,0.05);border:1px solid #1a2d40;
                        border-radius:4px;padding:0.4rem 0.6rem;margin-top:0.3rem;
                        font-family:'Space Mono',monospace;font-size:0.58rem;
                        color:#00e5ff;line-height:1.8;word-break:break-all;">
                {horas_str}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:rgba(255,23,68,0.08);border:1px solid #ff1744;
                        border-radius:4px;padding:0.4rem 0.6rem;margin-top:0.3rem;
                        font-family:'Space Mono',monospace;font-size:0.6rem;color:#ff1744;">
                ⚠ Ninguna hora seleccionada
            </div>
            """, unsafe_allow_html=True)

        # ── CONFIANZA ─────────────────────────────────────────────────────────
        st.markdown("---")
        st.markdown('<div class="section-title">📈 CONFIANZA</div>', unsafe_allow_html=True)
        confianza_min = st.slider("Confianza mínima (%)",
                                   min_value=0.0, max_value=100.0,
                                   step=1.0, disabled=not use_filters,
                                   key='confianza_widget')

        # ── RANGO DE CUOTAS ───────────────────────────────────────────────────
        st.markdown("---")
        st.markdown('<div class="section-title">💹 RANGO DE CUOTAS</div>', unsafe_allow_html=True)

        # Rango base de inclusión
        quote_range = st.slider("Rango base (incluir)",
                                 min_value=0.01, max_value=0.99,
                                 step=0.01, format="%.2f", disabled=not use_filters,
                                 key='quote_range_widget')

        # 4 rangos de exclusión
        st.markdown("""
        <div style="font-family:'Space Mono',monospace;font-size:0.58rem;
                    color:#ff6b35;text-transform:uppercase;letter-spacing:0.12em;
                    margin-top:0.6rem;margin-bottom:0.4rem;">
            ✂ Rangos a excluir
        </div>
        """, unsafe_allow_html=True)

        exclude_ranges = []
        exc_defaults = [(0.01, 0.20), (0.01, 0.20), (0.01, 0.20), (0.01, 0.20)]

        for i in range(1, 5):
            exc_enabled = st.checkbox(
                f"Exclusión {i}",
                key=f"exc_enabled_{i}",
                value=False,
                disabled=not use_filters
            )
            if exc_enabled and use_filters:
                exc_range = st.slider(
                    f"Rango excluido {i}",
                    min_value=0.01, max_value=0.99,
                    value=exc_defaults[i - 1],
                    step=0.01, format="%.2f",
                    key=f"exc_range_{i}",
                )
                exclude_ranges.append(exc_range)
                st.markdown(
                    f'<div style="font-family:Space Mono,monospace;font-size:0.58rem;'
                    f'color:#ff1744;margin-bottom:0.3rem;">'
                    f'✂ excluye [{exc_range[0]:.2f} – {exc_range[1]:.2f}]</div>',
                    unsafe_allow_html=True
                )

        st.markdown("---")
        st.markdown('<div class="section-title">💰 OBJETIVO</div>', unsafe_allow_html=True)
        target_win = st.number_input("Ganancia objetivo ($)",
                                      min_value=100, max_value=100000, value=1000, step=100)

        # ── MES Y DIA ─────────────────────────────────────────────────────────
        st.markdown("---")
        st.markdown('<div class="section-title">📅 MES Y DÍA</div>', unsafe_allow_html=True)
        _mes_opts = [f"{v}" for v in MESES_NAMES.values()]
        _mes_raw  = st.multiselect("Mes", _mes_opts,
                                   placeholder="Todos los meses", key='meses_widget',
                                   default=[])
        meses_sel = [k for k, v in MESES_NAMES.items() if v in _mes_raw]

        dias_sel = st.multiselect("Día del mes", list(range(1, 32)),
                                  placeholder="Todos los días", key='dias_widget',
                                  default=[])

        if meses_sel or dias_sel:
            _tags = []
            if meses_sel:
                _tags.append("📅 " + ", ".join(MESES_NAMES[m] for m in sorted(meses_sel)))
            if dias_sel:
                _tags.append("📆 días: " + ", ".join(str(d) for d in sorted(dias_sel)))
            st.markdown(
                f'<div style="background:rgba(0,229,255,0.05);border:1px solid #1a2d40;'
                f'border-radius:4px;padding:0.4rem 0.6rem;margin-top:0.3rem;'
                f'font-family:Space Mono,monospace;font-size:0.58rem;'
                f'color:#00e5ff;line-height:1.8;">'
                f'{"  ·  ".join(_tags)}</div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")
        run_btn = st.button("▶  EJECUTAR BACKTEST", use_container_width=True, key="run_main")

    invertir = st.session_state['direccion'] == 'invertir'
    params = dict(
        tiers          = tiers if tiers else ['D'],
        horas_sel      = sorted(st.session_state.get('horas_sel', list(range(24)))),
        confianza_min  = float(confianza_min) if use_filters else 0.0,
        quote_min      = float(quote_range[0]) if use_filters else 0.01,
        quote_max      = float(quote_range[1]) if use_filters else 0.99,
        exclude_ranges = exclude_ranges if use_filters else [],
        target_win     = float(target_win),
        invertir       = invertir,
        meses_sel      = meses_sel,
        dias_sel       = list(dias_sel),
    )

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

    if invertir:
        st.markdown("""<div style="background:rgba(255,23,68,0.08);border:1px solid #ff1744;
            border-radius:6px;padding:0.5rem 1.2rem;margin-bottom:1rem;
            font-family:'Space Mono',monospace;font-size:0.7rem;color:#ff1744;">
            🔄 MODO INVERTIR — apostando lo contrario a la predicción</div>""",
            unsafe_allow_html=True)
    else:
        st.markdown("""<div style="background:rgba(0,230,118,0.06);border:1px solid #00e676;
            border-radius:6px;padding:0.5rem 1.2rem;margin-bottom:1rem;
            font-family:'Space Mono',monospace;font-size:0.7rem;color:#00e676;">
            ✅ MODO SEGUIR — apostando según la predicción</div>""",
            unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["  📊  DASHBOARD  ","  📋  DETALLE  ","  📅  RESUMEN POR DIA  "])

    with tab1:
        total    = len(trades)
        ganadas  = (trades['Resultado']=='Gano').sum()
        perdidas = total - ganadas
        wr       = ganadas/total if total>0 else 0
        pl_total = trades['PnL Trade'].sum()
        avg_perd = trades[trades['Resultado']=='Perdio']['PnL Trade'].mean() if perdidas>0 else 0
        best     = trades['PnL Trade'].max()
        worst    = trades['PnL Trade'].min()

        c1,c2,c3,c4,c5 = st.columns(5)
        with c1: metric_card("TOTAL TRADES", f"{total:,}", "cyan")
        with c2:
            wrc = "green" if wr>=0.6 else "yellow" if wr>=0.5 else "red"
            metric_card("WIN RATE", f"{wr*100:.1f}", wrc, suffix="%")
        with c3: metric_card("GANADAS",  f"{ganadas:,}",  "green")
        with c4: metric_card("PERDIDAS", f"{perdidas:,}", "red")
        with c5: metric_card("P&L TOTAL", f"{pl_total:,.0f}", "green" if pl_total>=0 else "red", prefix="$")

        st.markdown("<br>", unsafe_allow_html=True)
        c6,c7,c8,c9 = st.columns(4)
        with c6: metric_card("AVG GANANCIA", f"{target_win:,.0f}", "green", prefix="$")
        with c7: metric_card("AVG PERDIDA",  f"{avg_perd:,.0f}",  "red",   prefix="$")
        with c8: metric_card("MEJOR TRADE",  f"{best:,.0f}",      "green", prefix="$")
        with c9: metric_card("PEOR TRADE",   f"{worst:,.0f}",     "red",   prefix="$")

        st.markdown("<br>", unsafe_allow_html=True)
        ca,cb = st.columns([3,2])
        with ca:
            fig = plot_equity_curve(trades)
            if fig: st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})
        with cb:
            fig = plot_pnl_por_dia(resumen)
            if fig: st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})

        cc,cd = st.columns([2,3])
        with cc:
            fig = plot_winrate_dia(resumen)
            if fig: st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})
        with cd:
            fig = plot_distribucion_horas(trades)
            if fig: st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})

        st.markdown('<div class="section-title" style="margin-top:1rem;">FILTROS APLICADOS</div>', unsafe_allow_html=True)
        p   = st.session_state.get('params', params)
        hs  = sorted(p.get('horas_sel', []))
        hs_s = ', '.join([f"{h}h" for h in hs]) if hs else '—'
        exc  = p.get('exclude_ranges', [])
        exc_s = '  '.join([f"[{mn:.2f}–{mx:.2f}]" for mn, mx in exc]) if exc else '—'

        _ms  = p.get('meses_sel', [])
        _ds  = p.get('dias_sel',  [])
        ms_s = ', '.join(MESES_NAMES[m][:3] for m in sorted(_ms)) if _ms else 'Todos'
        ds_s = ', '.join(str(d) for d in sorted(_ds)) if _ds else 'Todos'

        cols = st.columns(8)
        info = [
            ("Tier",          ', '.join(p['tiers'])),
            ("Horas",         hs_s),
            ("Confianza ≥",   f"{p['confianza_min']:.0f}%"),
            ("Entry Price",   f"{p['quote_min']:.2f}–{p['quote_max']:.2f}"),
            ("Excluidos",     exc_s),
            ("Dirección",     "INVERTIR 🔄" if p.get('invertir') else "SEGUIR ✅"),
            ("Mes",           ms_s),
            ("Día",           ds_s),
        ]
        for col, (lbl, val) in zip(cols, info):
            with col:
                if lbl == "Dirección":
                    color = "#ff1744" if p.get('invertir') else "#00e5ff"
                elif lbl == "Excluidos" and exc:
                    color = "#ff6b35"
                elif lbl in ("Mes", "Día") and val != "Todos":
                    color = "#ffd600"
                else:
                    color = "#00e5ff"
                st.markdown(f"""
                <div style="background:#0d1520;border:1px solid #1a2d40;border-radius:6px;
                            padding:0.7rem 0.8rem;text-align:center;">
                    <div style="font-family:'Space Mono',monospace;font-size:0.55rem;
                                color:#5a7080;text-transform:uppercase;letter-spacing:0.08em;">{lbl}</div>
                    <div style="font-family:'Space Mono',monospace;font-size:0.72rem;
                                color:{color};font-weight:700;margin-top:0.2rem;word-break:break-all;">{val}</div>
                </div>
                """, unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="section-title">DETALLE DE TRADES</div>', unsafe_allow_html=True)
        detail_cols = ['Timestamp CST','Fecha','Prediccion','Bet Side','Entry Price',
                       'Stake USD','Resultado','PnL Trade','PnL Acumulado',
                       'Poly UP Ask','Poly DOWN Ask','Poly UP Bid','Poly DOWN Bid']
        avail   = [c for c in detail_cols if c in trades.columns]
        df_show = trades[avail].copy()
        for c in ['Entry Price','Poly UP Ask','Poly DOWN Ask','Poly UP Bid','Poly DOWN Bid']:
            if c in df_show.columns:
                df_show[c] = df_show[c].map(lambda x: f"{x:.2f}" if pd.notna(x) else '')
        for c in ['Stake USD','PnL Trade','PnL Acumulado']:
            if c in df_show.columns:
                df_show[c] = df_show[c].map(lambda x: f"${x:,.2f}" if pd.notna(x) else '')
        def highlight(row):
            if 'Resultado' in row.index:
                if row['Resultado']=='Gano':   return ['background-color:rgba(0,230,118,0.06)']*len(row)
                if row['Resultado']=='Perdio': return ['background-color:rgba(255,23,68,0.06)']*len(row)
            return ['']*len(row)
        st.dataframe(df_show.style.apply(highlight, axis=1), use_container_width=True, height=520)
        csv = trades[avail].to_csv(index=False).encode('utf-8')
        st.download_button("⬇  Descargar CSV", csv, file_name="bitpredict_detalle.csv", mime="text/csv")

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
            def hl_res(row):
                try:
                    pl = float(str(row['P&L Total']).replace('$','').replace(',',''))
                    if pl>0: return ['background-color:rgba(0,230,118,0.06)']*len(row)
                    if pl<0: return ['background-color:rgba(255,23,68,0.06)']*len(row)
                except: pass
                return ['']*len(row)
            st.dataframe(res_show.style.apply(hl_res, axis=1), use_container_width=True, height=420)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-title">TOTALES ACUMULADOS</div>', unsafe_allow_html=True)
            tt  = resumen['Trades'].sum()
            tw  = resumen['Ganadas'].sum()
            tpl = resumen['PnL_Total'].sum()
            tsk = resumen['Stake_Total'].sum()
            awr = (tw/tt) if tt>0 else 0
            bd  = resumen.loc[resumen['PnL_Total'].idxmax(),'Fecha'] if not resumen.empty else '-'
            wd  = resumen.loc[resumen['PnL_Total'].idxmin(),'Fecha'] if not resumen.empty else '-'
            c1,c2,c3,c4,c5,c6 = st.columns(6)
            with c1: metric_card("TOTAL TRADES",    f"{tt:,}",    "cyan")
            with c2: metric_card("WIN RATE GLOBAL", f"{awr*100:.1f}", "green" if awr>=0.5 else "red", suffix="%")
            with c3: metric_card("P&L ACUMULADO",   f"{tpl:,.0f}", "green" if tpl>=0 else "red", prefix="$")
            with c4: metric_card("STAKE TOTAL",     f"{tsk:,.0f}", "white", prefix="$")
            with c5: metric_card("MEJOR DIA",       str(bd), "green")
            with c6: metric_card("PEOR DIA",        str(wd), "red")
            csv2 = resumen.to_csv(index=False).encode('utf-8')
            st.download_button("⬇  Descargar Resumen CSV", csv2,
                               file_name="bitpredict_resumen.csv", mime="text/csv")
        else:
            st.info("Sin datos para mostrar resumen.")


if __name__ == "__main__":
    main()
