#!/usr/bin/env python3
import csv
import argparse
from collections import defaultdict
import os
import json
from jamo import h2j, j2hcj

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(SCRIPT_DIR, 'dictionary.json')
MAX_MATCH_SHOWN = 5


def get_brokenword(word):  # 자음모음 쪼갠 스트링 리턴하는 함수
    return j2hcj(h2j(word))


def get_longest_matches(data, broken_search_word):
    longest_matches = []
    max_prefix_length = 0
    for w in data:
        # 단어별로 가장 길게 일치하는 길이를 찾고
        prefix_length = 0
        for i in range(min(len(broken_search_word), len(w))):
            if broken_search_word[i] == w[i]:
                prefix_length += 1
            else:
                break

        # 일치 목록 갱신
        if prefix_length > 0:
            # 이전 보다 긴 경우 새로 리스트
            if prefix_length > max_prefix_length:
                max_prefix_length = prefix_length
                longest_matches = [w]

            # 이전과 길이 같은 경우 그냥 목록 추가
            elif prefix_length == max_prefix_length:
                longest_matches.append(w)

    # 짧은 단어를 우선적으로 보여주도록 정렬함
    longest_matches.sort(key=lambda x: len(x))
    return longest_matches


def search_word(word):
    broken_search_word = get_brokenword(word)

    # JSON 파일에서 단어와 의미를 로드
    with open(FILE_PATH, 'r', encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)

    # 일치하는거 있으면 일치하는거 보여줌
    if broken_search_word in data:
        print(
            f"[ {data[broken_search_word]['word']} ]: {data[broken_search_word]['meaning']}")

    # 일치하는게 없는 경우
    # 가장 길게 일치하는 단어를 찾아서 보여줌
    else:
        longest_matches = get_longest_matches(data, broken_search_word)

        if longest_matches:
            print(
                f"'{word}' 해당 단어를 찾을 수 없습니다. 이 단어를 찾으셨나요?")
            # 최대 5개만 보여줌
            for i in range(min(MAX_MATCH_SHOWN, len(longest_matches))):
                print(
                    f" - {data[longest_matches[i]]['word']}: {data[longest_matches[i]]['meaning']}")
        else:
            print(f"'{word}' 해당 단어를 찾을 수 없습니다.")


def main():
    parser = argparse.ArgumentParser(
        description="tool that provides English synonyms for Korean words")
    parser.add_argument("word", help="Enter korean word to search")
    args = parser.parse_args()
    search_word(args.word)


if __name__ == "__main__":
    main()
