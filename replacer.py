import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_style = """  <style>
    /* ─── DESIGN TOKENS ─── */
    :root {
      --h: 240; --accent-h: 46;
      --bg: hsl(var(--h), 12%, 6%);
      --surface: hsl(var(--h), 12%, 10%);
      --surface-2: hsl(var(--h), 12%, 14%);
      --border: hsl(var(--h), 10%, 20%);
      --border-light: hsl(var(--h), 10%, 28%);
      --accent: hsl(var(--accent-h), 92%, 61%);
      --accent-glow: hsla(var(--accent-h), 92%, 61%, 0.15);
      --accent-2: hsl(var(--accent-h), 100%, 48%);
      --text: hsl(var(--h), 10%, 95%);
      --text-2: hsl(var(--h), 10%, 70%);
      --text-3: hsl(var(--h), 10%, 45%);
      --danger: hsl(0, 91%, 64%);
      --success: hsl(142, 69%, 58%);
      --glass-bg: hsla(var(--h), 12%, 12%, 0.7);
      --glass-border: hsla(0, 0%, 100%, 0.1);
      --radius: 16px; --radius-sm: 8px; --radius-lg: 24px;
      --shadow: 0 12px 40px rgba(0, 0, 0, 0.5);
      --ease: cubic-bezier(0.23, 1, 0.32, 1);
    }

    /* ─── RESET & BASE ─── */
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Outfit', 'Inter', sans-serif;
      background: var(--bg); color: var(--text);
      min-height: 100vh; overflow-x: hidden; -webkit-font-smoothing: antialiased;
    }
    .crystal {
      background: var(--glass-bg); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
      border: 1px solid var(--glass-border); box-shadow: var(--shadow);
    }

    /* ─── HEADER ─── */
    header {
      display: flex; align-items: center; justify-content: space-between;
      padding: 16px 32px; border-bottom: 1px solid var(--border);
      background: hsla(var(--h), 12%, 6%, 0.8); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
      position: sticky; top: 0; z-index: 100;
      transition: all 0.3s var(--ease);
    }
    .logo { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 24px; letter-spacing: -1px; }
    .logo span { background: linear-gradient(135deg, var(--accent), var(--accent-2)); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; }
    .header-actions { display: flex; gap: 12px; align-items: center; }
    .header-btn-group { display: flex; gap: 8px; }

    /* ─── LAYOUT ─── */
    .app-layout { display: grid; grid-template-columns: 440px 1fr; height: calc(100vh - 65px); transition: all 0.5s var(--ease); }
    .app-layout.focus-mode { grid-template-columns: 0px 1fr; }
    .sidebar { background: var(--surface); border-right: 1px solid var(--border); overflow-y: auto; padding: 24px; display: flex; flex-direction: column; gap: 24px; z-index: 50; }
    .sidebar::-webkit-scrollbar { width: 5px; }
    .sidebar::-webkit-scrollbar-thumb { background: var(--border); border-radius: 10px; }
    
    .divider { border: none; border-top: 1px solid var(--border); }
    .hint { font-size: 11.5px; color: var(--text-3); line-height: 1.5; }
    .required { color: var(--accent); }

    /* ─── TABS ─── */
    .tabs { display: flex; gap: 4px; background: var(--surface-2); padding: 4px; border-radius: 12px; margin-bottom: 8px; }
    .tab { flex: 1; padding: 10px; text-align: center; font-size: 13px; font-weight: 600; color: var(--text-3); cursor: pointer; border-radius: 8px; transition: all 0.2s; }
    .tab.active { background: var(--surface); color: var(--accent); box-shadow: 0 4px 12px rgba(0,0,0,0.2); }

    /* ─── SECTIONS ─── */
    .section { display: flex; flex-direction: column; gap: 16px; }
    .section-header { display: flex; align-items: center; justify-content: space-between; padding: 2px 0; cursor: pointer; user-select: none; }
    .section-title { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 11px; text-transform: uppercase; letter-spacing: 1.8px; color: var(--text-3); display: flex; align-items: center; gap: 10px; }
    .section-toggle { color: var(--text-3); font-size: 12px; transition: 0.3s; }
    .section-toggle.open { transform: rotate(180deg); color: var(--accent); }
    .section-body { display: flex; flex-direction: column; gap: 16px; overflow: hidden; }
    .section-body.collapsed { display: none; }

    /* ─── FORMS ─── */
    .form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
    .form-group { display: flex; flex-direction: column; gap: 6px; }
    label { font-size: 12px; font-weight: 600; color: var(--text-2); letter-spacing: 0.3px; }
    input, textarea, select {
      background: var(--surface-2); border: 1px solid var(--border); color: var(--text);
      font-family: 'Outfit', sans-serif; font-size: 13.5px; padding: 10px 14px;
      border-radius: var(--radius-sm); outline: none; width: 100%; transition: all 0.2s;
    }
    input:focus, textarea:focus, select:focus {
      border-color: var(--accent); background: hsla(var(--h), 12%, 16%, 0.8);
      box-shadow: 0 0 0 3px hsla(var(--accent-h), 92%, 61%, 0.1);
    }
    textarea { resize: vertical; min-height: 80px; line-height: 1.6; }

    /* ─── LINE ITEMS ─── */
    .line-items { display: flex; flex-direction: column; gap: 10px; }
    .line-item {
      background: var(--surface-2); border: 1px solid var(--border); border-radius: var(--radius-sm);
      padding: 16px; display: flex; flex-direction: column; gap: 10px; transition: all 0.25s var(--ease);
    }
    .line-item:hover { transform: translateX(4px); border-color: var(--border-light); background: hsla(var(--h), 10%, 16%, 0.8); }
    .line-item-row { display: grid; grid-template-columns: 1fr 64px 90px 96px 36px; gap: 10px; align-items: center; }
    .line-item-total { font-family: 'DM Mono', monospace; font-size: 13px; color: var(--accent); font-weight: 600; text-align: right; }
    .delete-item { background: transparent; border: none; color: var(--text-3); cursor: pointer; font-size: 14px; padding: 8px; border-radius: 8px; transition: all 0.2s; }
    .delete-item:hover { color: var(--danger); background: hsla(0, 91%, 64%, 0.1); }

    /* Totals Card */
    .totals-card { background: hsla(var(--h), 12%, 14%, 0.5); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 20px; box-shadow: inset 0 0 20px rgba(0,0,0,0.2); }
    .total-row { display: flex; justify-content: space-between; align-items: center; padding: 6px 0; font-size: 14px; }
    .total-row.divider { border-top: 1px solid var(--border); margin-top: 12px; padding-top: 16px; }
    .total-row.grand { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 18px; color: var(--accent); }
    .total-label { color: var(--text-2); font-weight: 500; }
    .total-value { font-family: 'DM Mono', monospace; font-weight: 600; }

    /* ─── BUTTONS ─── */
    .btn {
      font-family: 'Outfit', sans-serif; font-size: 14px; font-weight: 600; padding: 10px 20px;
      border-radius: var(--radius-sm); border: 1px solid transparent; cursor: pointer;
      transition: all 0.25s var(--ease); display: inline-flex; align-items: center; gap: 8px; white-space: nowrap;
    }
    .btn-primary { background: var(--accent); color: hsl(var(--h), 20%, 5%); box-shadow: var(--shadow-accent); }
    .btn-primary:hover { background: var(--accent-2); transform: translateY(-2px); box-shadow: 0 6px 20px hsla(var(--accent-h), 90%, 60%, 0.3); }
    .btn-ghost { background: transparent; color: var(--text-2); border-color: var(--border); }
    .btn-ghost:hover { border-color: var(--border-light); color: var(--text); background: var(--surface-2); }
    .btn-icon { padding: 10px; background: var(--surface-2); color: var(--text-2); border: 1px solid var(--border); border-radius: var(--radius-sm); cursor: pointer; transition: all 0.2s; font-size: 16px; display: inline-flex; align-items: center; justify-content: center; }
    .btn-icon:hover { color: var(--text); border-color: var(--accent); background: hsla(var(--accent-h), 92%, 61%, 0.05); }

    /* ─── LOGO UPLOAD ─── */
    .logo-upload-zone { border: 2px dashed var(--border); border-radius: var(--radius-sm); padding: 16px; text-align: center; cursor: pointer; transition: all 0.2s; position: relative; overflow: hidden; background: var(--surface-2); }
    .logo-upload-zone:hover { border-color: var(--accent); background: hsla(var(--accent-h), 92%, 61%, 0.04); }
    .logo-upload-zone.has-logo { border-style: solid; border-color: var(--accent); padding: 10px; }
    .logo-upload-zone input[type="file"] { position: absolute; inset: 0; opacity: 0; cursor: pointer; width: 100%; height: 100%; }
    .logo-preview-img { max-width: 100%; max-height: 72px; object-fit: contain; display: block; margin: 0 auto 6px; }

    /* ─── PREVIEW & CANVAS ─── */
    .preview-area { background: #08080a; display: flex; flex-direction: column; align-items: center; padding: 40px; gap: 32px; overflow-y: auto; position: relative; scrollbar-width: thin; scrollbar-color: var(--border) transparent; }
    .preview-toolbar { display: flex; align-items: center; gap: 12px; width: 100%; max-width: 840px; justify-content: space-between; background: hsla(var(--h), 12%, 12%, 0.6); padding: 8px 16px; border-radius: 40px; border: 1px solid var(--glass-border); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); position: sticky; top: 0; z-index: 10; }
    .preview-label { font-size: 11px; color: var(--text-3); font-family: 'Syne', sans-serif; text-transform: uppercase; letter-spacing: 2px; font-weight: 700; }
    .preview-controls { display: flex; gap: 8px; align-items: center; }
    .zoom-display { font-family: 'DM Mono', monospace; font-size: 12px; color: var(--text-accent); font-weight: 600; padding: 6px 12px; background: hsla(var(--h), 12%, 18%, 0.5); border-radius: 20px; }

    .invoice-wrap { transform-origin: top center; box-shadow: 0 30px 60px -12px rgba(0,0,0,0.5), 0 18px 36px -18px rgba(0,0,0,0.5); border-radius: 2px; }
    .invoice { width: 760px; min-height: 1000px; background: white; border-radius: 2px; position: relative; overflow: hidden; }

    /* ─── PROGRESS BAR ─── */
    .progress-wrap { margin-top: 2px; }
    .progress-bar { height: 3px; background: var(--surface-2); border-radius: 2px; overflow: hidden; }
    .progress-fill { height: 100%; background: var(--accent); border-radius: 2px; transition: width 0.3s; }
    .progress-label { font-size: 11px; color: var(--text-3); margin-top: 4px; display: flex; justify-content: space-between; }

    /* ─── STATUS BADGES ─── */
    .status-badge { display: inline-flex; align-items: center; gap: 5px; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; border: 1px solid transparent; }
    .status-unpaid { background: hsla(0, 91%, 64%, 0.1); color: var(--danger); border-color: hsla(0, 91%, 64%, 0.3); }
    .status-paid { background: hsla(142, 69%, 58%, 0.1); color: var(--success); border-color: hsla(142, 69%, 58%, 0.3); }
    .status-draft { background: var(--surface-2); color: var(--text-2); border-color: var(--border); }

    /* ─── THEME PICKER ─── */
    .theme-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; }
    .theme-swatch { aspect-ratio: 4/5; border-radius: var(--radius-sm); cursor: pointer; border: 1px solid var(--border); overflow: hidden; position: relative; transition: all 0.2s var(--ease); display: flex; flex-direction: column; background: var(--surface-2); }
    .theme-swatch:hover { transform: translateY(-4px); border-color: var(--border-light); box-shadow: var(--shadow); }
    .theme-swatch.active { border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent-glow); }
    .theme-swatch-header { height: 35%; }
    .theme-swatch-body { flex: 1; padding: 6px; display: flex; flex-direction: column; gap: 4px; justify-content: center; }
    .theme-swatch-line { height: 2px; border-radius: 1px; opacity: 0.3; }
    .theme-name { font-size: 11px; text-align: center; color: var(--text-2); margin-top: 6px; font-weight: 600; }

    /* Currency Select */
    .currency-select { display: flex; gap: 6px; flex-wrap: wrap; }
    .currency-btn { padding: 6px 12px; border-radius: 8px; font-size: 12px; font-weight: 600; background: var(--surface-2); border: 1px solid var(--border); color: var(--text-2); cursor: pointer; transition: all 0.2s; font-family: 'DM Mono', monospace; }
    .currency-btn.active { background: var(--accent); color: #000; border-color: var(--accent); }

    /* Notifications */
    .toast { position: fixed; bottom: 24px; right: 24px; background: var(--surface-2); border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 14px 18px; display: flex; align-items: center; gap: 10px; font-size: 13.5px; font-weight: 500; z-index: 1000; opacity: 0; pointer-events: none; max-width: 320px; box-shadow: var(--shadow); }

    /* Modals */
    .modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.8); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); z-index: 200; display: flex; align-items: center; justify-content: center; opacity: 0; pointer-events: none; }
    .modal { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 28px; width: 380px; max-width: calc(100vw - 48px); box-shadow: var(--shadow); }
    .export-option { display: flex; align-items: center; gap: 14px; padding: 14px 16px; background: var(--surface-2); border: 1px solid var(--border); border-radius: var(--radius-sm); cursor: pointer; transition: all 0.15s; margin-bottom: 10px; }
    .export-option:hover { border-color: var(--accent); background: hsla(var(--accent-h), 92%, 61%, 0.05); }
    
    /* Print adjustments */
    @media print { body * { visibility: hidden; } .invoice, .invoice * { visibility: visible; } .invoice { position: absolute; left: 0; top: 0; width: 100%; border-radius: 0; } }

    /* ─── INVOICE THEMES ─── */
    .inv-logo-img { max-width: 160px; max-height: 64px; object-fit: contain; display: block; margin-bottom: 8px; }
    .inv-logo-placeholder { width: 64px; height: 64px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-family: 'Syne', sans-serif; font-weight: 800; font-size: 22px; margin-bottom: 8px; }

    /* Noir 2.0 (Premium Dark) */
    .theme-noir { background: #000000; color: #ffffff; padding: 80px 70px; font-family: 'Inter', sans-serif; }
    .theme-noir .inv-accent { color: #f5c842; }
    .theme-noir .inv-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 80px; }
    .theme-noir .inv-brand { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 32px; letter-spacing: -1.2px; line-height: 1; }
    .theme-noir .inv-title { font-family: 'Syne', sans-serif; font-size: 56px; font-weight: 800; text-transform: uppercase; letter-spacing: -2px; color: #f5c842; text-align: right; line-height: 0.9; }
    .theme-noir .inv-number { font-family: 'DM Mono', monospace; font-size: 14px; color: #555; margin-top: 8px; text-align: right; letter-spacing: 2px; }
    .theme-noir .inv-parties { display: grid; grid-template-columns: 1.2fr 1fr; gap: 60px; margin-bottom: 60px; }
    .theme-noir .inv-party-label { font-size: 11px; text-transform: uppercase; letter-spacing: 3px; color: #444; margin-bottom: 12px; font-family: 'Syne', sans-serif; font-weight: 700; }
    .theme-noir .inv-party-name { font-weight: 700; font-size: 18px; margin-bottom: 6px; letter-spacing: -0.2px; }
    .theme-noir .inv-party-detail { font-size: 14px; color: #888; line-height: 1.6; white-space: pre-wrap; }
    .theme-noir .inv-meta { display: flex; justify-content: space-between; margin-bottom: 60px; padding: 24px 32px; background: #0a0a0a; border: 1px solid #1a1a1a; }
    .theme-noir .inv-meta-label { font-size: 10px; text-transform: uppercase; letter-spacing: 2px; color: #444; }
    .theme-noir .inv-meta-value { font-family: 'DM Mono', monospace; font-size: 15px; color: #fff; }
    .theme-noir .inv-table { width: 100%; border-collapse: collapse; margin-bottom: 60px; }
    .theme-noir .inv-table th { font-size: 11px; text-transform: uppercase; letter-spacing: 2px; color: #444; padding: 0 0 16px; text-align: left; font-weight: 700; font-family: 'Syne', sans-serif; border-bottom: 2px solid #1a1a1a; }
    .theme-noir .inv-table td { padding: 20px 0; border-bottom: 1px solid #0d0d0d; font-size: 15px; vertical-align: top; }
    .theme-noir .inv-table td.desc { font-weight: 600; width: 45%; }
    .theme-noir .inv-table th:last-child, .theme-noir .inv-table td:last-child { text-align: right; }
    .theme-noir .inv-table td.amount { font-family: 'DM Mono', monospace; color: #f5c842; font-weight: 700; font-size: 16px; }
    .theme-noir .inv-table td.num { font-family: 'DM Mono', monospace; color: #555; }
    .theme-noir .inv-totals { display: flex; justify-content: flex-end; margin-bottom: 80px; }
    .theme-noir .inv-totals-inner { width: 320px; }
    .theme-noir .inv-total-row { display: flex; justify-content: space-between; padding: 10px 0; font-size: 15px; }
    .theme-noir .inv-total-row.grand { border-top: 2px solid #f5c842; margin-top: 10px; padding-top: 20px; font-family: 'Syne', sans-serif; font-weight: 800; font-size: 24px; color: #f5c842; }
    .theme-noir .inv-total-label { color: #555; text-transform: uppercase; letter-spacing: 1px; font-size: 12px; }
    .theme-noir .inv-total-val { font-family: 'DM Mono', monospace; }
    .theme-noir .inv-footer { border-top: 1px solid #1a1a1a; padding-top: 40px; display: flex; justify-content: space-between; }
    .theme-noir .inv-footer-note { font-size: 14px; color: #666; max-width: 360px; line-height: 1.7; font-style: italic; white-space: pre-wrap; }
    .theme-noir .inv-footer-thank { font-family: 'Syne', sans-serif; font-size: 14px; color: #f5c842; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; white-space: pre-wrap; }
    .theme-noir .inv-desc-small { font-size: 13px; color: #444; margin-top: 6px; font-weight: 400; font-style: normal; }
    .theme-noir .inv-decoration { position: absolute; top: 0; right: 0; width: 300px; height: 300px; background: radial-gradient(circle at 100% 0%, rgba(245,200,66,0.08) 0%, transparent 75%); pointer-events: none; }

    /* Arctic 2.0 (Crisp Light) */
    .theme-arctic { background: #ffffff; color: #000000; padding: 80px 70px; font-family: 'Inter', sans-serif; }
    .theme-arctic .inv-accent { color: #0066ff; }
    .theme-arctic .inv-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 60px; }
    .theme-arctic .inv-brand { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 28px; color: #000; letter-spacing: -1px; border-left: 6px solid #0066ff; padding-left: 16px; }
    .theme-arctic .inv-title { font-family: 'Syne', sans-serif; font-size: 52px; font-weight: 800; text-transform: uppercase; letter-spacing: -2px; color: #0066ff; text-align: right; line-height: 0.9; }
    .theme-arctic .inv-number { font-family: 'DM Mono', monospace; font-size: 14px; color: #ddd; margin-top: 8px; text-align: right; letter-spacing: 1px; }
    .theme-arctic .inv-parties { display: grid; grid-template-columns: 1fr 1fr; gap: 60px; margin-bottom: 60px; }
    .theme-arctic .inv-party-label { font-size: 11px; text-transform: uppercase; letter-spacing: 3px; color: #bbb; margin-bottom: 12px; font-family: 'Syne', sans-serif; font-weight: 700; }
    .theme-arctic .inv-party-name { font-weight: 700; font-size: 18px; margin-bottom: 6px; letter-spacing: -0.2px; }
    .theme-arctic .inv-party-detail { font-size: 14px; color: #666; line-height: 1.6; white-space: pre-wrap; }
    .theme-arctic .inv-meta { display: flex; justify-content: space-between; margin-bottom: 60px; padding: 24px 0; border-top: 2px solid #f0f0f0; border-bottom: 2px solid #f0f0f0; }
    .theme-arctic .inv-meta-label { font-size: 10px; text-transform: uppercase; letter-spacing: 2px; color: #999; }
    .theme-arctic .inv-meta-value { font-family: 'DM Mono', monospace; font-size: 15px; font-weight: 600; color: #000; }
    .theme-arctic .inv-table { width: 100%; border-collapse: collapse; margin-bottom: 40px; }
    .theme-arctic .inv-table thead tr { background: #000000; }
    .theme-arctic .inv-table th { font-size: 11px; text-transform: uppercase; letter-spacing: 2px; color: #fff; padding: 14px 20px; font-family: 'Syne', sans-serif; text-align: left; }
    .theme-arctic .inv-table tr:nth-child(even) { background: #f9f9f9; }
    .theme-arctic .inv-table td { padding: 18px 20px; border-bottom: 1px solid #f0f0f0; font-size: 15px; }
    .theme-arctic .inv-table th:last-child, .theme-arctic .inv-table td:last-child { text-align: right; }
    .theme-arctic .inv-table td.amount { font-family: 'DM Mono', monospace; color: #0066ff; font-weight: 700; }
    .theme-arctic .inv-table td.desc { font-weight: 600; }
    .theme-arctic .inv-totals { display: flex; justify-content: flex-end; margin-bottom: 60px; }
    .theme-arctic .inv-totals-inner { width: 300px; }
    .theme-arctic .inv-total-row { display: flex; justify-content: space-between; padding: 10px 0; font-size: 15px; }
    .theme-arctic .inv-total-row.grand { border-top: 4px solid #000000; margin-top: 10px; padding-top: 20px; font-family: 'Syne', sans-serif; font-weight: 800; font-size: 24px; color: #000; }
    .theme-arctic .inv-total-label { color: #999; text-transform: uppercase; letter-spacing: 1px; font-size: 12px; }
    .theme-arctic .inv-footer { border-top: 1px solid #f0f0f0; padding-top: 40px; display: flex; justify-content: space-between; align-items: flex-end; }
    .theme-arctic .inv-footer-note { font-size: 14px; color: #888; max-width: 360px; line-height: 1.7; white-space: pre-wrap; }
    .theme-arctic .inv-footer-thank { font-family: 'Syne', sans-serif; font-size: 14px; color: #0066ff; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; white-space: pre-wrap; }
    .theme-arctic .inv-decoration { position: absolute; bottom: 0; left: 0; width: 100%; height: 8px; background: linear-gradient(to right, #0066ff, #000000); }

    /* Velvet (Luxury Purple) */
    .theme-velvet { background: #0f0a1a; color: #e9e5f5; padding: 80px 70px; font-family: 'Outfit', sans-serif; }
    .theme-velvet .inv-accent { color: #b59dfa; }
    .theme-velvet .inv-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 60px; }
    .theme-velvet .inv-brand { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 32px; background: linear-gradient(135deg, #b59dfa, #ebdfff); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; }
    .theme-velvet .inv-title { font-family: 'Syne', sans-serif; font-size: 56px; font-weight: 800; text-transform: uppercase; letter-spacing: -2px; color: #b59dfa; text-align: right; line-height: 0.9; }
    .theme-velvet .inv-number { font-family: 'DM Mono', monospace; font-size: 14px; color: #5a4b86; margin-top: 8px; text-align: right; letter-spacing: 1px; }
    .theme-velvet .inv-parties { display: grid; grid-template-columns: 1fr 1fr; gap: 60px; margin-bottom: 40px; }
    .theme-velvet .inv-party-label { font-size: 11px; text-transform: uppercase; letter-spacing: 3px; color: #5a4b86; margin-bottom: 12px; font-weight: 600; }
    .theme-velvet .inv-party-name { font-weight: 600; font-size: 18px; margin-bottom: 6px; letter-spacing: -0.2px; }
    .theme-velvet .inv-party-detail { font-size: 14px; color: #aaa1c5; line-height: 1.6; white-space: pre-wrap; }
    .theme-velvet .inv-meta { display: flex; justify-content: space-between; margin-bottom: 40px; padding: 24px; background: rgba(181, 157, 250, 0.05); border-radius: 12px; }
    .theme-velvet .inv-meta-label { font-size: 10px; text-transform: uppercase; letter-spacing: 2px; color: #5a4b86; font-weight: 600; }
    .theme-velvet .inv-meta-value { font-family: 'DM Mono', monospace; font-size: 15px; color: #fff; }
    .theme-velvet .inv-table { width: 100%; border-collapse: collapse; margin-bottom: 40px; }
    .theme-velvet .inv-table th { border-bottom: 1px solid #33215c; color: #b59dfa; padding: 16px 0; text-align: left; text-transform: uppercase; font-size: 12px; font-weight: 700; letter-spacing: 1px; }
    .theme-velvet .inv-table td { border-bottom: 1px solid #1a1130; padding: 16px 0; font-size: 15px; }
    .theme-velvet .inv-table td.desc { font-weight: 500; }
    .theme-velvet .inv-table td.amount { font-family: 'DM Mono', monospace; color: #fff; font-weight: 600; }
    .theme-velvet .inv-table th:last-child, .theme-velvet .inv-table td:last-child { text-align: right; }
    .theme-velvet .inv-totals { display: flex; justify-content: flex-end; margin-bottom: 40px; }
    .theme-velvet .inv-totals-inner { width: 320px; }
    .theme-velvet .inv-total-row { display: flex; justify-content: space-between; padding: 10px 0; font-size: 15px; }
    .theme-velvet .inv-total-row.grand { border-top: 2px solid #b59dfa; color: #b59dfa; font-family: 'Syne', sans-serif; font-weight: 800; font-size: 24px; padding-top: 16px; margin-top: 16px; }
    .theme-velvet .inv-total-label { color: #8c7dba; }
    .theme-velvet .inv-footer { border-top: 1px solid #33215c; padding-top: 30px; display: flex; justify-content: space-between; }
    .theme-velvet .inv-footer-note { font-size: 14px; color: #aaa1c5; max-width: 360px; line-height: 1.7; white-space: pre-wrap; }
    .theme-velvet .inv-footer-thank { font-family: 'Syne', sans-serif; font-size: 14px; color: #b59dfa; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; white-space: pre-wrap; }
    .theme-velvet .inv-desc-small { font-size: 13px; color: #8c7dba; margin-top: 6px; }

    /* Crystal (Full Glass) */
    .theme-crystal { background: url('https://images.unsplash.com/photo-1557683316-973673baf926?q=80&w=2629&auto=format&fit=crop') center/cover; position: relative; color: #fff; padding: 80px 70px; font-family: 'Outfit', sans-serif; }
    .theme-crystal::before { content: ''; position: absolute; inset: 0; background: rgba(20,20,30,0.6); backdrop-filter: blur(40px); -webkit-backdrop-filter: blur(40px); z-index: 0; }
    .theme-crystal > * { position: relative; z-index: 1; }
    .theme-crystal .inv-brand { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 32px; }
    .theme-crystal .inv-title { font-family: 'Syne', sans-serif; font-size: 56px; font-weight: 800; text-transform: uppercase; text-shadow: 0 4px 20px rgba(255,255,255,0.4); text-align: right; line-height: 0.9; color: #fff; }
    .theme-crystal .inv-number { font-family: 'DM Mono', monospace; font-size: 14px; color: rgba(255,255,255,0.6); margin-top: 8px; text-align: right; }
    .theme-crystal .inv-header { margin-bottom: 60px; display: flex; justify-content: space-between; align-items: flex-start; }
    .theme-crystal .inv-parties { display: grid; grid-template-columns: 1fr 1fr; gap: 60px; margin-bottom: 40px; }
    .theme-crystal .inv-party-label { font-size: 11px; text-transform: uppercase; letter-spacing: 3px; color: rgba(255,255,255,0.5); margin-bottom: 12px; font-weight: 600; }
    .theme-crystal .inv-party-name { font-weight: 600; font-size: 18px; margin-bottom: 6px; }
    .theme-crystal .inv-party-detail { font-size: 14px; color: rgba(255,255,255,0.8); line-height: 1.6; white-space: pre-wrap; }
    .theme-crystal .inv-meta { display: flex; justify-content: space-between; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 16px; padding: 24px 32px; margin-bottom: 60px; box-shadow: 0 8px 32px rgba(0,0,0,0.2); }
    .theme-crystal .inv-meta-label { font-size: 10px; text-transform: uppercase; letter-spacing: 2px; color: rgba(255,255,255,0.6); }
    .theme-crystal .inv-meta-value { font-family: 'DM Mono', monospace; font-size: 15px; color: #fff; text-shadow: 0 2px 4px rgba(0,0,0,0.3); }
    .theme-crystal .inv-table { width: 100%; border-collapse: collapse; margin-bottom: 40px; }
    .theme-crystal .inv-table td { border-bottom: 1px solid rgba(255,255,255,0.1); padding: 16px 0; font-size: 15px; }
    .theme-crystal .inv-table th { border-bottom: 1px solid rgba(255,255,255,0.3); color: rgba(255,255,255,0.7); padding: 16px 0; text-align: left; text-transform: uppercase; font-size: 11px; letter-spacing: 2px; }
    .theme-crystal .inv-table td.desc { font-weight: 500; }
    .theme-crystal .inv-table td.amount { font-family: 'DM Mono', monospace; font-weight: 600; }
    .theme-crystal .inv-table th:last-child, .theme-crystal .inv-table td:last-child { text-align: right; }
    .theme-crystal .inv-totals { display: flex; justify-content: flex-end; margin-bottom: 40px; }
    .theme-crystal .inv-totals-inner { width: 320px; }
    .theme-crystal .inv-total-row { display: flex; justify-content: space-between; padding: 10px 0; font-size: 15px; }
    .theme-crystal .inv-total-row.grand { border-top: 2px solid rgba(255,255,255,0.4); font-family: 'Syne', sans-serif; font-weight: 800; font-size: 24px; margin-top: 16px; padding-top: 16px; text-shadow: 0 2px 10px rgba(0,0,0,0.5); }
    .theme-crystal .inv-total-label { color: rgba(255,255,255,0.7); }
    .theme-crystal .inv-footer { border-top: 1px solid rgba(255,255,255,0.2); padding-top: 30px; display: flex; justify-content: space-between; }
    .theme-crystal .inv-footer-note { font-size: 14px; color: rgba(255,255,255,0.8); max-width: 360px; line-height: 1.7; white-space: pre-wrap; }
    .theme-crystal .inv-footer-thank { font-family: 'Syne', sans-serif; font-size: 14px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; text-shadow: 0 2px 4px rgba(0,0,0,0.3); white-space: pre-wrap; }
    .theme-crystal .inv-desc-small { font-size: 13px; color: rgba(255,255,255,0.6); margin-top: 6px; }

  </style>"""

content = re.sub(r'<style>[\s\S]*?</style>', new_style, content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('CSS rewritten successfully!')
