# NameHint

**NameHint**는 한글 단어의 영어 동의어를 제공하여 영어 변수나 함수 이름을 짓는 데 도움을 주는 CLI 도구입니다.  
"아, 그거 영어로 뭐였지?" 라는 생각이 들 때 유용하게 사용할 수 있습니다.

이 도구는 [한국어기초사전](https://krdict.korean.go.kr/kor/mainAction)의 데이터를 사용하고 있습니다.  
관련 자세한 내용은 [블로그 링크](https://gongboo.github.io/project/namehint/)에서 확인할 수 있습니다.

## pip 으로 설치

```bash
pip install namehint
```

## 사용법

```bash
namehint [ 단어 ]
```

## 예시

### 단어 찾기

```bash
namehint 공부
```

다음과 같이 출력

> \[ 공부 \]: study

### 단어가 없는 경우 : 비슷한 단어

```bash
namehint 학교가자
```

다음과 같이 출력

> '학교가자' 해당 단어를 찾을 수 없습니다. 이 단어를 찾으셨나요?
>
> - 학교: school
> - 학교장: principal
> - 학교 교육: school education; schooling
> - 학교생활: school life; student life

### 단어가 없는 경우 : 비슷한 단어

```bash
namehint school
```

다음과 같이 출력

> 'school' 해당 단어를 찾을 수 없습니다.
