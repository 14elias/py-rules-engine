# Contributing to rules-engine

Thank you for considering contributing to **rules-engine**!
We welcome contributions of all kinds — bug fixes, features, documentation, and improvements.

---

## 🚀 How You Can Contribute

- Report bugs or issues
- Suggest new features
- Add new predicates or rule types
- Improve documentation
- Write or improve tests
- Refactor or optimize code

---

## ⚙️ Development Setup

### 1. Clone the repository

```powershell
git clone https://github.com/14elias/rules-engine.git
cd rules-engine
```

---

### 2. Create and activate environment (using `uv`)

```powershell
uv venv
.\.venv\Scripts\activate
```

---

### 3. Install dependencies

```powershell
uv sync --group dev
```

---

## 🧪 Running Tests

```powershell
uv run pytest
```

With coverage:

```powershell
uv run pytest --cov=rules_engine
```

---

## 🧹 Code Style (Ruff)

We use **ruff** for linting and formatting.

Before committing, run:

```powershell
uv run ruff check . --fix
uv run ruff format .
```

---

## 🌿 Branching

Create a feature branch:

```powershell
git checkout -b feature/your-feature-name
```

---

## ✅ Pull Request Process

1. Make your changes
2. Run linting and tests:

   ```powershell
   uv run ruff check . --fix
   uv run ruff format .
   uv run pytest
   ```

3. Update documentation if needed
4. Submit a Pull Request with a clear description

---

## 🧾 Commit Messages

We follow **Conventional Commits**:

- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation
- `test:` tests
- `refactor:` code changes
- `chore:` maintenance

### Examples

```
feat: add EndsWithRule support
fix: correct typo in Field docstring
docs: improve quick start guide
```

---

## 🤖 Continuous Integration

All pull requests are automatically checked using:

- ✅ Ruff (linting & formatting)
- ✅ Pytest (tests)
- ✅ Coverage reporting

Make sure your code passes all checks before submitting.

---

## 💬 Questions?

Feel free to open an issue if you need help or clarification.

---

Thanks for contributing! 🙌
