# G1 Mini-project: Vocabulary Learning App (ver. 1.0; asof 10/22, 2026)

---

## 👥 Group Information

| Item | Details |
|---|---|
| Group | G1 |
| Members | 문채원(Leader), 옥예서, 고나연, 탁서영 |
| README editor | 옥예서 |
| Date & Time | 10/22, 13:00 – 15:35 |
| Location | Room 334 |

---

## 💙 1. What We Learned from the Two Articles

### 1-1. Webb (2007): Vocabulary Learning

- **Main point:** 단어를 반복해서 접할수록 어휘 지식이 향상되지만, 단어의 의미를 알아보는 것과 직접 기억해서 사용하는 능력은 다르다. 어휘 지식에는 철자, 의미, 문법적 특성, 연어 관계 등 다양한 측면이 있으며, 각 지식은 서로 다른 속도로 발달한다.
- **What teachers can learn:** 예비 영어교사는 학생들이 단어의 뜻을 암기하는 데 그치지 않고, 다양한 문맥에서 단어를 반복해서 접하고 실제로 활용할 수 있도록 지도해야 한다. 또한 객관식 문제뿐 아니라 단어 회상, 빈칸 채우기, 문장 만들기 등 다양한 활동을 통해 학생들의 수용적·산출적 어휘 지식을 평가해야 한다.

### 1-2. Nakata et al. (2021)

- **Main point:** 어휘 시험은 학습 결과를 평가하는 도구일 뿐 아니라 학습 자체를 촉진하는 역할을 한다. 최근에 배운 단어와 이전에 배운 단어를 함께 평가하는 누적 평가(Cumulative Testing)는 학습자가 기억에서 단어를 떠올리는 인출 연습(Retrieval Practice)을 촉진하여 장기적인 어휘 기억에 도움을 줄 수 있다.
- **What teachers can learn:** 예비 영어교사는 최근에 학습한 단어뿐 아니라 이전에 배운 단어도 퀴즈에 포함하여 학생들이 지속적으로 복습하도록 해야 한다. 또한 단순히 정답을 다시 보여 주기보다 학생들이 직접 단어를 떠올리고 사용하도록 활동을 설계해야 한다. 다만 누적 평가가 학생들에게 부담이 될 수 있으므로 난이도와 학습 동기도 함께 고려해야 한다.

### 1-3. Our Takeaway for the App

- 두 논문을 바탕으로 우리 앱은 단어를 다양한 문맥에서 반복해서 접하고, 기억에서 직접 떠올려 보는 기회를 제공하도록 설계하고자 한다. 플래시카드, 객관식 퀴즈, 빈칸 채우기, 문장 속 단어 사용 등의 활동을 통해 단어의 의미뿐 아니라 철자와 실제 사용 능력도 연습할 수 있도록 한다. 또한 이전에 학습한 단어를 새로운 단어와 함께 퀴즈에 다시 출제하고, 틀린 단어를 복습할 수 있는 기능을 제공하여 장기적인 어휘 기억을 돕고자 한다.

---

## 💙 2. Our Selected Words from the Basic Vocabulary List

### 2-1. About the List

- 기본 어휘 목록은 알파벳순으로 구성되어 있으며, *와 ** 표시를 통해 어휘의 학교급별 활용 수준을 구분할 수 있다. 대표 단어와 함께 관련 어휘가 괄호 안에 제시되어 있어 Word family와 파생 관계를 확인할 수 있다. color / colour처럼 여러 표기 형태를 함께 제시하여 단어의 다양한 형태에 관한 정보도 제공한다.

### 2-2. Selected Words (10–20)

`[act]`, `[leave]`, `[produce]`, `[subject]`, `[mind]`, `[delight]`, `[confidence]`, `[satisfy]`, `[embarrass]`, `[frustrate]`

### 2-3. Why We Chose These Words

- 선정 기준 1. 다양한 의미와 단어족: 여러 의미와 파생어를 가진 단어
- 선정 기준 2. 문맥에 따른 의미 이해: 상황에 따라 의미와 뉘앙스가 달라지는 단어
- 선정 기준 3. 일상생활과의 관련성: 감정과 경험을 영어로 표현할 수 있는 단어

---

## 💙 3. App Design Draft

### 3-1. Design Concept

- 영어 단어 학습과 판타지 RPG를 결합하여, 퀴즈를 풀며 몬스터를 물리치고 캐릭터를 성장시키는 게임형 어휘 학습 앱

### 3-2. Learners

- (K7) learners

### 3-3. Goal

- Recognize the meaning & spell the word

### 3-4. Learning Activities

- **Encounters (Webb 2007):** 플래시카드, 객관식 문제, 빈칸 채우기, 예문 보고 뜻 고르기, 뜻 보고 철자 쓰기 등 다섯 가지 활동을 통해 각 단어를 5회 반복 학습
- **Retrieval (Nakata et al. 2021):** 10개 단어를 5개씩 두 세트로 나누어 각 세트 학습 후 테스트를 진행하고, 마지막에는 전체 단어 범위로 게임형 최종 평가 진행

### 3-5. Use of the List Information

| Information | How our app uses it |
|---|---|
| Level (`*`, `**`) | 기호를 활용해 단어의 학교급 관련 정보를 제공하고 학습 순서를 구성 |
| Word family (e.g., *species* ~ *specify*) | 관련 단어를 단어 정보 아래에 작게 제시하여 단어의 형태와 의미 확장 학습 지원 |
| Variation (e.g., *rumor* / *rumour*) | [NA] |

### 3-6. Context Elements (LPGCTXF, Week 03)

| Element | Our decision |
|---|---|
| Learner | 한국 중학교 1학년 학생 |
| Proficiency | 초급~초중급, 기초 어휘와 간단한 문장 이해 가능 |
| Goal | 영어 단어 10개의 뜻, 철자, 기본적인 쓰임 학습 |
| Content | 단어 10개, 한국어 뜻, 쉬운 예문, 단어 카드, 객관식 퀴즈 |
| Time&Task | 회당 약 10분, 단어 학습·퀴즈·오답 복습 |
| Constraints | 학생별 실력 차이, 제한된 학습 시간, 쉬운 설명과 간단한 활동 |
| Feedback | 즉각적인 정답 확인, 정답 제공, 오답 단어 복습 |

---

## 💙 4. App Features

1. **Word Typing Practice**: This feature helps learners memorize English spelling because they type words themselves and practice accurate spelling.
2. **Example Sentences with Highlighted Target Words**: This feature helps learners understand word meanings in context because they can infer meanings from example sentences, which helps them remember words in the long term.
3. **Multiple-Choice Questions**: This feature helps learners understand the meanings of words and distinguish between words with different meanings because they choose the correct answer from multiple options.
4. **Timed Vocabulary Battles**: This feature helps learners recall word meanings quickly because they answer vocabulary questions within a time limit to attack monsters.

---

## 💙 5. Sample Word Data

| Word | Word-family | Variation | Level | Meaning (Korean) | Example sentence |
|---|---|---|---|---|---|
| act | actual, interact | NA | (*) | 행동하다 | They acted quickly to help. |
| leave | NA | NA | (**) | 떠나다 | She left the room quietly. |
| produce | NA | NA | (**) | 생산하다 | The company produces cars. |
| subject | subjective | NA | (**) | 주제 | English is my favorite subject. |
| mind | NA | NA | (*) | 생각 | Keep this idea in mind. |
| delight | NA | NA | (**) | 기쁘게 하다 | The gift delighted her. |
| confide | confident | NA | NA | 털어놓다 | I confide in my friend. |
| satisfy | NA | NA | (**) | 만족시키다 | The food satisfies me. |
| embarrass | NA | NA | (**) | 당황하게 하다 | His joke embarrassed me. |
| frustrate | NA | NA | (**) | 좌절시키다 | The difficult test frustrated me. |

---

## 💙 6. Test and Improve

### 6-1. Checklist

- [ ] All features work (every button was clicked).
- [ ] All words, meanings, and sentences are correct.
- [ ] The app gives clear feedback for right and wrong answers.
- [ ] Learners **retrieve** words and meet each word **more than once**.
- [ ] The app is easy to use on a phone.

### 6-2. Problems Found and How We Fixed Them

| Problem | Fix |
|---|---|
| 아이폰 | 폰 기종 상관없이 정상 작동하도록 수정 |
| 배경음악 | 몰입감을 높일 배경음악 추가 |
| 힌트 | 정답을 바로 제시하지 않고 힌트 제시 |
| 정확도 | 학습 완료 기준이 되는 정답률 수치 조정 |

### 6-3. Saved Versions

- `index_v1.html`: 음악, 힌트, 정확도
- `G1_project_draft.html`: final version

---

## 💙 7. Next Steps

- 마지막 스테이지 한국어 오디오 수정
