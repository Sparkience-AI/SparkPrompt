import json
from pathlib import Path

from scripts.release_evidence import generate


def test_release_evidence_is_bound_to_artifacts_and_commit(tmp_path: Path) -> None:
    dist = tmp_path / "dist"
    output = tmp_path / "evidence"
    dist.mkdir()
    (dist / "sparkprompt.whl").write_bytes(b"wheel")

    generate(dist, output, "abc123")

    assert "sparkprompt.whl" in (output / "SHA256SUMS").read_text(encoding="utf-8")
    sbom = json.loads((output / "sbom.cdx.json").read_text(encoding="utf-8"))
    provenance = json.loads((output / "provenance.json").read_text(encoding="utf-8"))
    assert sbom["bomFormat"] == "CycloneDX"
    assert provenance["source_commit"] == "abc123"
