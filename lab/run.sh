#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-bitwarden-cipher-create-acl}"
export BW_URL="${BW_URL:-http://127.0.0.1:18160}"
chmod +x poc.py

down() {
  echo "== docker compose down -v =="
  docker compose -p "${COMPOSE_PROJECT_NAME}" down -v --remove-orphans || true
}

fail_run() {
  echo "FAIL BITWARDEN-CIPHER-CREATE-ACL $*" | tee poc-last-run.txt
  docker compose -p "${COMPOSE_PROJECT_NAME}" logs --tail=80 bitwarden db || true
  down
  exit 1
}

echo "== docker compose down (clean) =="
down

echo "== docker compose up =="
up_ok=0
for attempt in $(seq 1 12); do
  if docker compose -p "${COMPOSE_PROJECT_NAME}" up -d; then
    up_ok=1
    break
  fi
  echo "IOC compose-up-retry attempt=${attempt}"
  sleep 30
  down
done
if [[ "${up_ok}" != 1 ]]; then
  fail_run "compose up failed"
fi

echo "== wait lite /alive or /api/config + migrated tables =="
ready=0
for i in $(seq 1 180); do
  alive="$(curl -sS -o /tmp/bw-cipher-create-acl-alive.txt -w '%{http_code}' --max-time 8 "${BW_URL}/alive" || true)"
  cfg="$(curl -sS -o /tmp/bw-cipher-create-acl-config.txt -w '%{http_code}' --max-time 8 "${BW_URL}/api/config" || true)"
  tables="$(docker compose -p "${COMPOSE_PROJECT_NAME}" exec -T db mysql -ubitwarden -psuper_strong_password --batch --skip-column-names bitwarden_vault -e 'SHOW TABLES;' 2>/dev/null || true)"
  tcount="$(echo "${tables}" | sed '/^$/d' | wc -l | tr -d ' ')"
  if { [[ "${alive}" == "200" ]] || [[ "${cfg}" == "200" ]]; } && [[ "${tcount}" -ge 60 ]] && echo "${tables}" | grep -qi '^User$'; then
    ready=1
    echo "IOC lite-ready attempt=${i} alive=${alive} config=${cfg}"
    break
  fi
  echo "IOC lite-wait attempt=${i} alive=${alive} config=${cfg} tables=$(echo "${tables}" | wc -l | tr -d ' ')"
  sleep 8
done
if [[ "${ready}" != 1 ]]; then
  fail_run "lite not ready"
fi

echo "== poc.py =="
set +e
python3 ./poc.py | tee poc-last-run.txt
rc=${PIPESTATUS[0]}
set -e
if [[ "${rc}" != 0 ]]; then
  if ! grep -qE 'FAIL BITWARDEN-CIPHER-CREATE-ACL|SUCCESS BITWARDEN-CIPHER-CREATE-ACL' poc-last-run.txt 2>/dev/null; then
    echo "FAIL BITWARDEN-CIPHER-CREATE-ACL poc exit=${rc}" >> poc-last-run.txt
  fi
fi

down
exit "${rc}"
