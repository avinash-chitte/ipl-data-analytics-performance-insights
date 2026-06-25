# Changelog

All notable changes to the **IPL Intelligence Hub** project are documented in this file.

---

## [2.0.0] - 2026-06-25

### Added
- **Dynamic Plotly Merging Utility:** Implemented `update_plotly_layout(fig, **kwargs)` in `src/styles.py` to copy and merge layout arguments (e.g., `yaxis`, `legend`, `margin`, `xaxis`) on top of default styles. This completely resolves the `TypeError: got multiple values for keyword argument` conflicts.
- **views/ Structure:** Grouped all modular dashboard components in the `views/` folder, completely bypassing Streamlit's native sidebar multi-page auto-detection which previously caused blank/empty links in the navigation panel:
  - `views/overview.py` (Visual KPIs, season RPO & runs trend, toss impact)
  - `views/team_performance.py` (H2H comparisons, win share ratios, consistency stats)
  - `views/player_explorer.py` (Batter and bowler career profile explorer, overs-phase splits)
  - `views/venue_intelligence.py` (Ground scoring comparison, pitch characteristics, chase favorites)
  - `views/powerplay_death.py` (Phase run rates, boundary distributions, specialist rankings)
  - `views/match_predictor.py` (Win probability gauge, ROC curve, feature coefficients list)
  - `views/key_insights.py` (15 tactical T20 business insights with custom charts)

### Changed
- **Main Router (`app.py`):** Rewritten to integrate the new `views` structure. Imports now load directly from the updated module paths.
- **Styles System (`src/styles.py`):** Integrated Google Fonts (Inter) and custom responsive styles, moving styling controls away from chart parameters to centralized logic.
- **Comprehensive README (`README.md`):** Completely rewritten into a developer-grade portfolio overview featuring system architecture, tech stacks, ML pipeline splits, and recruiter guides.

### Removed
- **Unused Dependencies:** Trimmed `requirements.txt` to only include core Python frameworks (`streamlit`, `pandas`, `numpy`, `plotly`, `scikit-learn`). Removed legacy Node.js/React templates.
- **Legacy Files:** Deleted legacy data preprocessing and Matplotlib-based visualization scripts from `src/`.

### Verified
- **Local Startup:** App starts successfully with `streamlit run app.py` on default port `8501`.
- **Imports Sanity:** Successfully executed import validation for data loaders and machine learning models.
- **Streamlit Cloud Compatibility:** verified system path manipulation and simulated data fallbacks for container setups.
