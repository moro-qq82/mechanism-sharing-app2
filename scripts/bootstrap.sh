#!/usr/bin/env bash
set -euo pipefail

# Determine repository root relative to this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "$REPO_ROOT"

RESET='\033[0m'
BOLD='\033[1m'
BLUE='\033[34m'
GREEN='\033[32m'
YELLOW='\033[33m'

print_section() {
  local title="$1"
  echo -e "\n${BOLD}${BLUE}==> ${title}${RESET}"
}

print_item() {
  local message="$1"
  echo -e "  - ${message}"
}

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

detect_node_manager() {
  if [[ -f "pnpm-lock.yaml" ]]; then
    echo "pnpm"
    return 0
  fi
  if [[ -f "yarn.lock" ]]; then
    echo "yarn"
    return 0
  fi
  if [[ -f "bun.lockb" ]]; then
    echo "bun"
    return 0
  fi
  if [[ -f "package-lock.json" ]]; then
    echo "npm"
    return 0
  fi
  if [[ -f "package.json" ]]; then
    echo "npm"
    return 0
  fi
  return 1
}

detect_python_manager() {
  if [[ -f "poetry.lock" ]] || [[ -f "pyproject.toml" ]]; then
    echo "poetry"
    return 0
  fi
  if [[ -f "Pipfile" ]]; then
    echo "pipenv"
    return 0
  fi
  if [[ -f "requirements.txt" ]]; then
    echo "pip"
    return 0
  fi
  return 1
}

show_env_hint() {
  if [[ -f ".env" ]]; then
    print_item "既存の .env を検出しました。内容を確認し、必要であれば更新してください。"
  elif [[ -f ".env.local" ]]; then
    print_item ".env.local が存在します。複製して環境変数を整備してください。"
  elif [[ -f ".env.example" ]]; then
    print_item "cp .env.example .env で環境変数を用意してください。"
  else
    print_item "環境変数ファイルが見つかりません。README や docs を確認して必要な値を定義してください。"
  fi
}

print_header() {
  local message="$1"
  echo -e "${BOLD}${GREEN}${message}${RESET}"
}

print_warning() {
  local message="$1"
  echo -e "${YELLOW}${message}${RESET}"
}

print_header "Setup helper"
print_item "リポジトリ: ${REPO_ROOT}"

print_section "環境変数の確認"
show_env_hint

node_manager=""
if node_manager=$(detect_node_manager); then
  print_section "Node.js 依存関係"
  case "$node_manager" in
    pnpm)
      if command_exists pnpm; then
        print_item "pnpm install を実行してください。"
      else
        print_warning "pnpm がインストールされていません。npm install -g pnpm などで導入してください。"
      fi
      ;;
    yarn)
      if command_exists yarn; then
        print_item "yarn install を実行してください。"
      else
        print_warning "yarn がインストールされていません。npm install -g yarn などで導入してください。"
      fi
      ;;
    bun)
      if command_exists bun; then
        print_item "bun install を実行してください。"
      else
        print_warning "bun がインストールされていません。公式手順に従って導入してください。"
      fi
      ;;
    npm)
      if command_exists npm; then
        if command_exists npx && [[ -f "package-lock.json" ]]; then
          print_item "npm ci を推奨します。"
        else
          print_item "npm install を実行してください。"
        fi
      else
        print_warning "npm が利用できません。Node.js をインストールしてください。"
      fi
      ;;
  esac
  if [[ -f "package.json" ]]; then
    if command_exists jq && jq -e '.scripts.dev' package.json >/dev/null 2>&1; then
      dev_command=$(jq -r '.scripts.dev' package.json)
      print_item "開発サーバーは npm run dev などで実行できる想定です (実際のコマンド: ${dev_command})。"
    else
      if ! command_exists jq; then
        print_warning "jq が見つかりません。package.json の scripts セクションを手動で確認してください。"
      else
        print_item "package.json の scripts セクションを確認し、利用可能なコマンドを把握してください。"
      fi
    fi
  fi
else
  print_section "Node.js 依存関係"
  print_item "package.json が見つかりません。Node.js ベースのアプリではない可能性があります。"
fi

if python_manager=$(detect_python_manager); then
  print_section "Python 依存関係"
  case "$python_manager" in
    poetry)
      if command_exists poetry; then
        print_item "poetry install を実行してください。"
      else
        print_warning "poetry がインストールされていません。pipx install poetry などで導入してください。"
      fi
      ;;
    pipenv)
      if command_exists pipenv; then
        print_item "pipenv install を実行してください。"
      else
        print_warning "pipenv がインストールされていません。pip install --user pipenv などで導入してください。"
      fi
      ;;
    pip)
      if command_exists python3 && command_exists pip; then
        print_item "python3 -m venv .venv && source .venv/bin/activate を実行した後、pip install -r requirements.txt を実行してください。"
      else
        print_warning "python3 または pip が見つかりません。Python をインストールしてください。"
      fi
      ;;
  esac
else
  print_section "Python 依存関係"
  print_item "pyproject.toml や requirements.txt が見つかりません。Python の構成は不要かもしれません。"
fi

if [[ -f "docker-compose.yml" || -f "compose.yaml" ]]; then
  print_section "Docker コンテナ"
  if command_exists docker && docker compose version >/dev/null 2>&1; then
    print_item "docker compose up --build を実行してサービスを立ち上げられます。"
  elif command_exists docker-compose; then
    print_item "docker-compose up --build を実行してサービスを立ち上げられます。"
  else
    print_warning "Docker が見つかりません。Docker Desktop などをインストールしてください。"
  fi
fi

if [[ -d "prisma" && -f "prisma/schema.prisma" ]]; then
  print_section "Prisma マイグレーション"
  if command_exists pnpm; then
    print_item "pnpm prisma migrate deploy でデータベースを最新化できます。"
  elif command_exists npx; then
    print_item "npx prisma migrate deploy を実行してください。"
  else
    print_warning "Prisma を実行するための Node.js ツールチェーンが見つかりません。"
  fi
fi

if [[ -d "migrations" ]]; then
  print_section "マイグレーション"
  print_item "migrations ディレクトリが見つかりました。採用フレームワークの手順に従って適用してください。"
fi

if [[ -f "Makefile" ]]; then
  print_section "Makefile"
  print_item "make help または Makefile を確認して便利なタスクを把握してください。"
fi

print_section "テスト"
if [[ -f "package.json" ]]; then
  if command_exists jq && jq -e '.scripts.test' package.json >/dev/null 2>&1; then
    case "$node_manager" in
      pnpm)
        if command_exists pnpm; then
          print_item "pnpm test を実行してテストを回してください。"
        else
          print_warning "pnpm が見つかりません。インストール後にテストを実行してください。"
        fi
        ;;
      yarn)
        if command_exists yarn; then
          print_item "yarn test もしくは yarn run test を試してください。"
        else
          print_warning "yarn が見つかりません。"
        fi
        ;;
      bun)
        if command_exists bun; then
          print_item "bun test など、scripts.test の内容に従ってください。"
        else
          print_warning "bun が見つかりません。"
        fi
        ;;
      *)
        if command_exists npm; then
          print_item "npm test を実行してテストを回してください。"
        else
          print_warning "npm が利用できません。Node.js をインストールしてください。"
        fi
        ;;
    esac
  else
    if ! command_exists jq; then
      print_warning "jq が見つかりません。package.json の test スクリプトを手動で確認してください。"
    else
      print_item "package.json 内の test スクリプトを確認してください。"
    fi
  fi
elif [[ -f "pytest.ini" || -d "tests" ]]; then
  if command_exists pytest; then
    print_item "pytest を実行してテストを回してください。"
  else
    print_warning "pytest が見つかりません。pip install pytest などで導入してください。"
  fi
else
  print_item "テスト関連ファイルが見つかりません。プロジェクトのテスト方法を確認してください。"
fi

print_header "完了"
print_item "上記の推奨コマンドを順に実行すれば環境構築の見通しが立つはずです。"
