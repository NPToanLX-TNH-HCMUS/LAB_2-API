import sys

import requests

BASE_URL = "http://localhost:8080"

TEST_FILES = [
    "tests/test_files/test_1.wav",
    "tests/test_files/test_2.wav",
]
DIVIDER = "-" * 60


def print_section(title: str) -> None:
    print(f"\n{DIVIDER}")
    print(f"  {title}")
    print(DIVIDER)


def print_response(resp: requests.Response) -> None:
    print(f"Status : {resp.status_code}")
    try:
        print(f"Body   : {resp.json()}")
    except ValueError:
        print(f"Body   : {resp.text}")


def test_root() -> None:
    print_section("GET /  (introduction)")
    resp = requests.get(f"{BASE_URL}/")
    print_response(resp)
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    print("✓ PASS")


def test_health() -> None:
    """GET /health – health check."""
    print_section("GET /health  (health check)")
    resp = requests.get(f"{BASE_URL}/health")
    print_response(resp)
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    data = resp.json()
    assert data.get("status") == "ok", f"Unexpected status: {data}"
    assert data.get("pipeline_ready") is True, "Pipeline not ready"
    print("✓ PASS")


def test_predict(audio_path: str) -> None:
    print_section(f"POST /predict  ({audio_path})")
    try:
        with open(audio_path, "rb") as f:
            resp = requests.post(
                f"{BASE_URL}/predict",
                files={"file": (audio_path, f, "audio/wav")},
            )
    except FileNotFoundError:
        print(f"⚠  Skipped – file not found: {audio_path}")
        return

    print_response(resp)
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    data = resp.json()
    assert "transcription" in data, "Missing 'transcription' key in response"
    print("✓ PASS")


def test_predict_no_file() -> None:
    print_section("POST /predict  (no file – expected 422)")
    resp = requests.post(f"{BASE_URL}/predict")
    print_response(resp)
    assert resp.status_code == 422, f"Expected 422, got {resp.status_code}"
    print("✓ PASS")


def main() -> None:
    print(f"\nRunning API tests against: {BASE_URL}\n")

    passed = 0
    failed = 0

    tests = [
        test_root,
        test_health,
        *[lambda p=p: test_predict(p) for p in TEST_FILES],
        test_predict_no_file,
    ]

    for test_fn in tests:
        try:
            test_fn()
            passed += 1
        except AssertionError as exc:
            print(f"✗ FAIL – {exc}")
            failed += 1
        except requests.exceptions.ConnectionError:
            print(f"✗ ERROR – Could not connect to {BASE_URL}. Is the server running?")
            failed += 1

    print(f"\n{DIVIDER}")
    print(f"  Results: {passed} passed, {failed} failed")
    print(DIVIDER)

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
