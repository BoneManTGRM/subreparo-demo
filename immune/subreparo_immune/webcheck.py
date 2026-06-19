from __future__ import annotations

from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .models import Finding, FractureType, Severity


@dataclass(frozen=True)
class WebsiteResult:
    url: str
    ok: bool
    status_code: int | None
    message: str


def check_website(url: str, timeout_seconds: int = 10) -> WebsiteResult:
    request = Request(url, headers={"User-Agent": "SubReparo-Immune/0.1"})
    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            status = int(response.status)
            ok = 200 <= status < 400
            return WebsiteResult(url=url, ok=ok, status_code=status, message=f"HTTP {status}")
    except HTTPError as error:
        return WebsiteResult(url=url, ok=False, status_code=int(error.code), message=f"HTTP {error.code}")
    except URLError as error:
        return WebsiteResult(url=url, ok=False, status_code=None, message=str(error.reason))
    except TimeoutError:
        return WebsiteResult(url=url, ok=False, status_code=None, message="request timed out")


def website_finding(result: WebsiteResult) -> Finding | None:
    if result.ok:
        return None
    return Finding(
        fracture_type=FractureType.WEBSITE_HEALTH,
        severity=Severity.MEDIUM,
        path=result.url,
        line=None,
        signal=f"Website check did not return a normal response: {result.message}",
        recommendation="Review hosting, DNS, deployment, and application logs. Re-run the check after repair.",
    )
