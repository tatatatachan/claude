#!/bin/sh
# 回帰テスト: 悪い例が FAIL になり、良い例(../../mockups)が FAIL にならないこと。
cd "$(dirname "$0")/.."
node validate.js tests/bad_thumbnail.html >/tmp/bad.out; code=$?
cat /tmp/bad.out
[ $code -eq 1 ] && echo "OK: 悪い例はFAILになった" || { echo "NG: 悪い例がFAILにならない"; exit 1; }
