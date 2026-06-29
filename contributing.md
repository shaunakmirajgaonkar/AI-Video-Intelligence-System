# Contributing to AI Video Intelligence System

Thank you for your interest in contributing! 🎉

---

## 🚀 Getting Started

1. **Fork** the repository
2. **Clone** your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-video-intelligence.git
   cd ai-video-intelligence
   ```
3. **Create a branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

---

## 📁 Project Structure

- `core/` — Detection, tracking, activity, summarisation logic
- `utils/` — Drawing and reporting helpers
- `config.py` — All constants live here (no hardcoding elsewhere)
- `main.py` — Pipeline entry point only (keep it thin)

---

## ✅ Contribution Guidelines

- Follow existing code style (PEP 8)
- All new settings go in `config.py`
- Keep `main.py` clean — business logic belongs in `core/`
- Test with both webcam and a video file before submitting
- Update `CHANGELOG.md` under `[Unreleased]`

---

## 🐛 Reporting Bugs

Open a GitHub Issue with:
- OS and Python version
- Full error traceback
- Steps to reproduce

---

## 💡 Feature Requests

Open a GitHub Issue with the `enhancement` label and describe:
- What problem it solves
- Proposed implementation approach

---

## 📬 Pull Request Checklist

- [ ] Code runs without errors on webcam source
- [ ] No hardcoded values (use `config.py`)
- [ ] `CHANGELOG.md` updated
- [ ] Descriptive commit message
