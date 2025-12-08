from pathlib import Path

def test_project_structure():
    assert Path("src/app.py").exists()
    assert Path("requirements.txt").exists()
