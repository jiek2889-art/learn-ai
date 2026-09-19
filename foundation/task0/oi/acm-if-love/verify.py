"""对拍脚本: 用题目给出的两组样例验证 solution.py。

    python verify.py
"""

import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).parent


def run_case(infile, expected_file):
    got = subprocess.run(
        [sys.executable, str(HERE / "solution.py")],
        stdin=infile.open(encoding="utf-8"),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if got.returncode != 0:
        return False, f"非零退出码 {got.returncode}\n{got.stderr}"

    want = expected_file.read_text(encoding="utf-8").strip()
    have = got.stdout.strip()
    if have == want:
        return True, have
    return False, f"期望 {want!r}\n实际 {have!r}"


def main():
    ok_all = True
    for i in (1, 2):
        ok, msg = run_case(HERE / f"sample{i}.in", HERE / f"sample{i}.out")
        ok_all &= ok
        print(f"sample{i}: {'PASS' if ok else 'FAIL'}  {msg}")
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()
