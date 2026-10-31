# Block 2: 공개 — 점검하고 짝에게 보낸다

> **Phase A 시작 시 그대로 출력한다:**
> ```
> 📖 공식 문서: https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site
> ```

## EXPLAIN

### 1. 정의

| 용어 | 뜻 |
|---|---|
| GitHub Pages | GitHub 저장소의 `index.html`을 웹 주소로 열어 주는 무료 공개 기능. 휴대폰에서도 열린다 |
| 공개 점검 | 공개 전에 회사 자료·개인정보·비밀값이 없는지, 데이터 출처와 "가상" 표기가 있는지 확인하는 일 |

### 2. 왜 공개 전에 점검하는가

| 기준 | 바로 올리기 | 점검 후 올리기 |
|---|---|---|
| 회사 자료 | 섞여 들어가도 모른다 | 공개 저장소에 넣지 않는다 |
| 데이터 표기 | 가상 데이터가 실제처럼 읽힌다 | "실습용 가상 데이터"와 출처를 적는다 |
| 되돌리기 | 공개된 뒤에는 복사·캐시가 남는다 | 올리기 전에 한 번 더 묻는다 |

### 3. 케이스 — 만든 사람의 대시보드

이 강의를 만든 사람의 결과는 https://ypjungg88-netizen.github.io/learn-pdm-lite-hgd/ 에 그래프 한 장으로 공개돼 있다. 내 그래프와 추세 시작 시각이 같은지 비교해 본다.

## EXECUTE

아래 프롬프트를 붙여 넣으라고 안내한다.

```
~/kma-pdm-lite 를 공개하기 전에 점검해 줘.
1. index.html 에 "실습용 가상 데이터"와 데이터 출처
   (keerhee/kma-auto-genai-3-1, Day5_설비센서_50건_가상.csv)가 있는지,
   회사 자료·개인정보·비밀값이 없는지 확인해 표로 보여 줘.
2. https://ypjungg88-netizen.github.io/learn-pdm-lite-hgd/
   를 열어 내 그래프와 추세 시작 시각이 같은지 비교해 줘.
3. 짝에게 보낼 짧은 메시지를 만들어 줘: 대시보드 주소,
   설치 한 줄 npx skills add ypjungg88-netizen/learn-pdm-lite-hgd --agent claude-code --global --yes,
   부르는 이름 /learn-pdm-lite-hgd, 받는 사람이 할 일 세 줄.
4. 내 GitHub에 공개할지는 나에게 먼저 묻고,
   내가 "공개해 줘"라고 할 때만 올린다. 비밀번호는 묻지 않는다.
```

### 확인할 것 (Phase B)

- 공개 점검표에 "가상 데이터 표기 ✓ · 출처 ✓ · 회사 자료 0 · 비밀값 0"이 있다.
- 두 대시보드의 추세 시작이 모두 13:00이다.
- 짝에게 보낼 메시지에 대시보드 주소·설치 한 줄·`/learn-pdm-lite-hgd`가 있다.

막히면 원인을 Claude Code에게 찾게 하는 후속 프롬프트를 준다. 정답은 "정답 보기" 요청이 있을 때만 연다.

```
대시보드 주소가 안 열려. 주소와 Pages 상태를 확인하고 원인을 한 줄로 설명해 줘
```

## QUIZ

없음 (실습판의 퀴즈는 Block 1의 한 문항뿐).

## 과제와 다음

1. 짝의 learn 스킬을 설치해 10분 동안 듣고, 점검표(예/아니오 다섯 줄)를 짝에게 보낸다. 제출물: 점검표 메시지.
2. 다른 Day나 내 업무 주제로 `/course-forge`를 다시 돌려 내 강의를 하나 더 만든다. 제출물: 새 learn 스킬 저장소 주소.
