import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import random
import time
import math
from datetime import datetime

# 페이지 기본 설정
st.set_page_config(
    page_title="G1 Vocabulary App",
    page_icon="📚",
    layout="centered"
)

WORDS_PER_DAY = 30

# 브라우저 내장 음성 중 영어 원어민(US/UK) 음성을 선택해 재생하는 TTS 함수
def render_tts_button(word: str, key: str, show_word: bool = True):
    safe_word = word.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')
    btn_text = f"🔊 원어민 발음 듣기 ({word})" if show_word else "🔊 원어민 발음 힌트 듣기"

    html_code = f"""
    <div style="display: flex; justify-content: center; margin: 6px 0;">
        <button id="tts_btn_{key}" type="button" onclick="playNativeTTS_{key}('{safe_word}')" style="
            background-color: #f0f4f8;
            border: 1px solid #cbd5e1;
            border-radius: 20px;
            padding: 8px 18px;
            font-size: 14px;
            font-weight: 600;
            color: #1e293b;
            cursor: pointer;
            touch-action: manipulation;
            -webkit-tap-highlight-color: rgba(59, 130, 246, 0.25);
            transition: background-color 0.15s ease, transform 0.1s ease;
        " onpointerdown="this.style.transform='scale(0.97)';"
          onpointerup="this.style.transform='scale(1)';"
          onpointerleave="this.style.transform='scale(1)';"
          onmouseover="this.style.backgroundColor='#e2e8f0'"
          onmouseout="this.style.backgroundColor='#f0f4f8'">
            {btn_text}
        </button>
    </div>

    <script>
    (function() {{
        const preferredNames = [
            'Google US English',
            'Microsoft Aria Online',
            'Microsoft Jenny Online',
            'Microsoft Guy Online',
            'Microsoft Zira',
            'Microsoft David',
            'Samantha',
            'Alex',
            'Daniel',
            'Google UK English Female',
            'Google UK English Male'
        ];

        function pickVoice() {{
            if (typeof window.speechSynthesis === 'undefined') return null;
            const voices = window.speechSynthesis.getVoices() || [];
            if (!voices.length) return null;

            for (const name of preferredNames) {{
                const match = voices.find(v => v.name && v.name.includes(name));
                if (match) return match;
            }}

            const usMatch = voices.find(v => v.lang && (v.lang === 'en-US' || v.lang === 'en_US'));
            if (usMatch) return usMatch;

            return voices.find(v => v.lang && v.lang.toLowerCase().startsWith('en')) || null;
        }}

        if (typeof window.speechSynthesis !== 'undefined') {{
            window.speechSynthesis.getVoices();
            window.speechSynthesis.onvoiceschanged = function() {{
                window.speechSynthesis.getVoices();
            }};
        }}

        window['playNativeTTS_{key}'] = function(text) {{
            if (typeof window.speechSynthesis === 'undefined') return;
            window.speechSynthesis.cancel();
            const utter = new SpeechSynthesisUtterance(text);
            const voice = pickVoice();
            if (voice) {{
                utter.voice = voice;
                utter.lang = voice.lang;
            }} else {{
                utter.lang = 'en-US';
            }}
            utter.rate = 0.92;
            utter.pitch = 1.0;
            window.speechSynthesis.speak(utter);
        }};
    }})();
    </script>
    """
    components.html(html_code, height=48)

# 데이터 로드 함수
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Voca_3000.csv", encoding="utf-8")
        return df
    except Exception as e:
        st.error(f"CSV 파일을 불러오는 중 오류가 발생했습니다: {e}")
        return None

# 랭킹 저장소 (앱 실행 중 모든 사용자 공유)
@st.cache_resource
def get_ranking_store():
    return []

def build_day_options(total_rows: int):
    total_days = math.ceil(total_rows / WORDS_PER_DAY)
    return [
        f"Day {i} ({(i - 1) * WORDS_PER_DAY + 1} ~ {min(i * WORDS_PER_DAY, total_rows)}번)"
        for i in range(1, total_days + 1)
    ]

def get_day_slice(df: pd.DataFrame, day_idx: int) -> pd.DataFrame:
    start_idx = day_idx * WORDS_PER_DAY
    end_idx = min(start_idx + WORDS_PER_DAY, len(df))
    return df.iloc[start_idx:end_idx].reset_index(drop=True)

df = load_data()
ranking_store = get_ranking_store()

# 세션 상태 초기화 (로그인)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# 로그인 화면
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.title("📚 G1 English Vocabulary App")
    st.subheader("중학교 1학년 필수 영단어 마스터 프로그램")
    st.write("학습 기록과 타임어택 랭킹 등록을 위해 이름을 입력하고 로그인해 주세요.")

    with st.form("login_form"):
        name_input = st.text_input("학습자 이름 (또는 닉네임)", placeholder="예: 1학년 3반 홍길동")
        submit_login = st.form_submit_button("🚀 학습 시작하기 (로그인)", use_container_width=True)

        if submit_login:
            if name_input.strip():
                st.session_state.logged_in = True
                st.session_state.username = name_input.strip()
                st.rerun()
            else:
                st.warning("이름을 입력해 주세요!")

# 로그인 완료 후 메인 화면
else:
    if df is not None:
        word_col = df.columns[1]     # 2번째 열 (영단어)
        meaning_col = df.columns[3]  # 4번째 열 (뜻)
        day_options = build_day_options(len(df))

        # 사이드바 구성
        st.sidebar.title("📚 G1 Vocabulary App")
        st.sidebar.success(f"👤 **{st.session_state.username}** 님 학습 중")
        if st.sidebar.button("로그아웃", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()

        st.sidebar.markdown("---")

        # 검색/수정이 불가능한 라디오 버튼 메뉴
        menu = st.sidebar.radio(
            "학습 메뉴 선택",
            [
                "🏠 홈 소개",
                "🃏 플래시카드 학습",
                "❓ 객관식 퀴즈",
                "✍️ 서술형 스펠링 테스트",
                "⏱️ 타임어택 랭킹전"
            ]
        )

        # ---------------------------------------------------------
        # 1) 홈 소개
        # ---------------------------------------------------------
        if menu == "🏠 홈 소개":
            st.title("🌟 G1 English Vocabulary App")
            st.write(f"**{st.session_state.username}**님 환영합니다! 중학교 1학년 수준의 3,000개 어휘를 Day별 플래시카드와 퀴즈로 마스터해보세요.")
            st.info("👈 왼쪽 사이드바에서 원하는 학습 단계를 선택하세요!")

            st.subheader("📊 데이터 현황 및 전체 단어 보기")
            st.write(f"현재 연동된 전체 학습 단어 수: **{len(df)}개** (총 {len(day_options)}일 완성 코스, Day당 {WORDS_PER_DAY}단어)")

            if st.checkbox("📖 전체 단어장 목록 펼쳐보기 (3,000 단어)"):
                st.markdown("### 📋 전체 단어 리스트")
                st.dataframe(
                    df[[word_col, meaning_col]].rename(columns={word_col: "영단어 (Word)", meaning_col: "뜻 (Meaning)"}),
                    use_container_width=True
                )

        # ---------------------------------------------------------
        # 2) 플래시카드 학습 (Day별 분할 + 카드 직접 터치 뒤집기 + 원어민 TTS)
        # ---------------------------------------------------------
        elif menu == "🃏 플래시카드 학습":
            st.header("🃏 플래시카드 단어 암기")
            st.write("학습할 **Day 세트**를 선택하고, **카드를 직접 터치/클릭**하여 앞/뒷면을 뒤집어 보세요!")

            selected_day_label = st.selectbox("📅 학습할 Day 세트 선택", day_options, key="fc_day_select")
            selected_day_idx = day_options.index(selected_day_label)
            day_df = get_day_slice(df, selected_day_idx)

            if st.session_state.get("fc_current_day") != selected_day_idx:
                st.session_state.fc_current_day = selected_day_idx
                st.session_state.fc_index = 0
                st.session_state.fc_flipped = False

            idx = st.session_state.fc_index
            current_row = day_df.iloc[idx]
            word = str(current_row[word_col]).strip()
            meaning = str(current_row[meaning_col]).strip()

            st.progress((idx + 1) / len(day_df), text=f"진행률: {idx + 1} / {len(day_df)} 단어")

            st.markdown("""
            <style>
            div[data-testid="stButton"] > button[kind="secondary"] {
                min-height: 200px;
                border-radius: 16px;
                border: 2px solid #cbd5e1;
                background-color: #ffffff;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
                font-size: 26px;
                font-weight: 700;
                touch-action: manipulation;
                transition: transform 0.12s ease, box-shadow 0.12s ease;
            }
            div[data-testid="stButton"] > button[kind="secondary"]:active,
            div[data-testid="stButton"] > button[kind="secondary"]:hover {
                border-color: #3b82f6;
                box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
            }
            </style>
            """, unsafe_allow_html=True)

            if not st.session_state.fc_flipped:
                card_label = f"🔤 {word}\n\n(카드를 터치하면 뜻이 보입니다)"
            else:
                card_label = f"💡 {meaning}\n\n[ {word} ]"

            def toggle_flashcard():
                st.session_state.fc_flipped = not st.session_state.fc_flipped

            st.button(
                card_label,
                key=f"flip_card_{selected_day_idx}_{idx}",
                use_container_width=True,
                type="secondary",
                on_click=toggle_flashcard
            )

            render_tts_button(word, key=f"fc_{selected_day_idx}_{idx}", show_word=True)

            col_prev, col_shuffle, col_next = st.columns([1, 1, 1])

            def go_prev_card():
                if st.session_state.fc_index > 0:
                    st.session_state.fc_index -= 1
                    st.session_state.fc_flipped = False

            def go_random_card():
                st.session_state.fc_index = random.randint(0, len(day_df) - 1)
                st.session_state.fc_flipped = False

            def go_next_card():
                if st.session_state.fc_index < len(day_df) - 1:
                    st.session_state.fc_index += 1
                    st.session_state.fc_flipped = False

            with col_prev:
                st.button("⬅️ 이전 단어", use_container_width=True, type="primary", disabled=(idx == 0), on_click=go_prev_card)
            with col_shuffle:
                st.button("🔀 랜덤 뽑기", use_container_width=True, type="primary", on_click=go_random_card)
            with col_next:
                st.button("다음 단어 ➡️", use_container_width=True, type="primary", disabled=(idx == len(day_df) - 1), on_click=go_next_card)

            st.markdown("---")
            if st.checkbox(f"📖 Day {selected_day_idx + 1} 단어 목록 보기"):
                st.dataframe(
                    day_df[[word_col, meaning_col]].rename(columns={word_col: "영단어", meaning_col: "뜻"}),
                    use_container_width=True
                )

        # ---------------------------------------------------------
        # 3) 객관식 퀴즈 (플래시카드 Day 세트 연동 + 원어민 TTS)
        # ---------------------------------------------------------
        elif menu == "❓ 객관식 퀴즈":
            st.header("❓ 객관식 퀴즈 (영단어 ➔ 뜻)")
            st.write("선택한 **Day 세트**의 단어들로 출제됩니다. 발음을 듣고 알맞은 뜻을 고르세요.")

            selected_day_label = st.selectbox("📅 퀴즈 Day 세트 선택", day_options, key="quiz_day_select")
            selected_day_idx = day_options.index(selected_day_label)
            day_df = get_day_slice(df, selected_day_idx)

            def pick_mc_question(pool_df: pd.DataFrame, full_df: pd.DataFrame):
                correct_row = pool_df.sample(1).iloc[0]
                q_word = str(correct_row[word_col]).strip()
                q_correct = str(correct_row[meaning_col]).strip()

                wrong_pool = pool_df[pool_df[word_col].astype(str).str.strip() != q_word]
                if len(wrong_pool) >= 3:
                    wrong_rows = wrong_pool.sample(3)
                else:
                    fallback_pool = full_df[full_df[word_col].astype(str).str.strip() != q_word]
                    wrong_rows = fallback_pool.sample(3)

                options = [str(m).strip() for m in wrong_rows[meaning_col].values] + [q_correct]
                random.shuffle(options)
                st.session_state.q_word = q_word
                st.session_state.q_correct = q_correct
                st.session_state.q_options = options
                st.session_state.q_retry = False
                st.session_state.q_solved = False
                st.session_state.q_feedback = None
                st.session_state.q_id = st.session_state.get("q_id", 0) + 1

            if st.session_state.get("q_current_day") != selected_day_idx or "q_word" not in st.session_state:
                st.session_state.q_current_day = selected_day_idx
                st.session_state.q_total = 0
                st.session_state.q_correct_cnt = 0
                pick_mc_question(day_df, df)

            st.markdown(f"📊 **진행도: 맞춘 문제 {st.session_state.q_correct_cnt}개 / 총 푼 문제 {st.session_state.q_total}개**")
            st.markdown("---")

            st.markdown(f"### Q. 다음 영단어의 뜻은 무엇일까요?\n# **{st.session_state.q_word}**")
            render_tts_button(st.session_state.q_word, key=f"quiz_{selected_day_idx}_{st.session_state.q_id}", show_word=True)

            choice = st.radio(
                "보기를 선택하세요:",
                st.session_state.q_options,
                key=f"quiz_radio_{selected_day_idx}_{st.session_state.q_id}",
                disabled=st.session_state.q_solved
            )

            if st.session_state.q_feedback:
                ftype, fmsg = st.session_state.q_feedback
                if ftype == "success":
                    st.success(fmsg)
                elif ftype == "warning":
                    st.warning(fmsg)
                elif ftype == "error":
                    st.error(fmsg)

            if not st.session_state.q_solved:
                if st.button("정답 제출하기", type="primary", key=f"quiz_submit_{st.session_state.q_id}"):
                    if choice == st.session_state.q_correct:
                        st.session_state.q_total += 1
                        st.session_state.q_correct_cnt += 1
                        st.session_state.q_solved = True
                        st.session_state.q_feedback = ("success", f"🎉 정답입니다! 훌륭해요 👏 (**{st.session_state.q_word}** = {st.session_state.q_correct})")
                        st.rerun()
                    else:
                        if not st.session_state.q_retry:
                            st.session_state.q_retry = True
                            st.session_state.q_feedback = ("warning", "⚠️ 틀렸습니다! 다시 한 번 잘 생각해보세요. (기회 1번 더!)")
                            st.rerun()
                        else:
                            st.session_state.q_total += 1
                            st.session_state.q_solved = True
                            st.session_state.q_feedback = ("error", f"❌ 아쉽습니다. 정답은 **{st.session_state.q_correct}** 입니다.")
                            st.rerun()
            else:
                if st.button("➡️ 다음 문제 풀기", type="primary", key=f"quiz_next_{st.session_state.q_id}"):
                    pick_mc_question(day_df, df)
                    st.rerun()

        # ---------------------------------------------------------
        # 4) 서술형 스펠링 테스트 (플래시카드 Day 세트 연동 + 단어 숨김 발음 힌트)
        # ---------------------------------------------------------
        elif menu == "✍️ 서술형 스펠링 테스트":
            st.header("✍️ 서술형 스펠링 테스트 (뜻 ➔ 영단어)")
            st.write("선택한 **Day 세트**의 단어들로 출제됩니다. 한국어 뜻과 발음 힌트를 듣고 영단어 철자를 입력하세요.")

            selected_day_label = st.selectbox("📅 스펠링 테스트 Day 세트 선택", day_options, key="subj_day_select")
            selected_day_idx = day_options.index(selected_day_label)
            day_df = get_day_slice(df, selected_day_idx)

            def pick_subj_question(pool_df: pd.DataFrame):
                rand_row = pool_df.sample(1).iloc[0]
                w = str(rand_row[word_col]).strip()
                m = str(rand_row[meaning_col]).strip()
                st.session_state.subj_word = w
                st.session_state.subj_meaning = m
                st.session_state.subj_hint = w[0] + " _ " * (len(w) - 1)
                st.session_state.subj_retry = False
                st.session_state.subj_solved = False
                st.session_state.subj_feedback = None
                st.session_state.subj_q_id = st.session_state.get("subj_q_id", 0) + 1

            if st.session_state.get("subj_current_day") != selected_day_idx or "subj_word" not in st.session_state:
                st.session_state.subj_current_day = selected_day_idx
                st.session_state.subj_total = 0
                st.session_state.subj_correct_cnt = 0
                pick_subj_question(day_df)

            target_word = st.session_state.subj_word
            target_meaning = st.session_state.subj_meaning

            st.markdown(f"📊 **진행도: 맞춘 문제 {st.session_state.subj_correct_cnt}개 / 총 푼 문제 {st.session_state.subj_total}개**")
            st.markdown("---")

            st.markdown(f"### 뜻: **{target_meaning}**")

            col_h1, col_h2 = st.columns(2)
            with col_h1:
                if st.checkbox("💡 첫 글자 힌트 보기", key=f"subj_first_hint_{st.session_state.subj_q_id}"):
                    st.info(f"힌트: {st.session_state.subj_hint}")
            with col_h2:
                if st.checkbox("🔊 발음 힌트 듣기", key=f"subj_audio_hint_{st.session_state.subj_q_id}"):
                    # 1번 요청 반영: 발음 힌트 버튼 옆에 영단어 철자 미표시
                    render_tts_button(target_word, key=f"subj_hint_{st.session_state.subj_q_id}", show_word=False)

            user_input = st.text_input(
                "영단어 철자를 소문자로 입력하세요:",
                key=f"user_subj_input_{selected_day_idx}_{st.session_state.subj_q_id}",
                disabled=st.session_state.subj_solved
            )

            if st.session_state.subj_feedback:
                ftype, fmsg = st.session_state.subj_feedback
                if ftype == "success":
                    st.success(fmsg)
                elif ftype == "warning":
                    st.warning(fmsg)
                elif ftype == "error":
                    st.error(fmsg)

            if not st.session_state.subj_solved:
                if st.button("정답 확인하기", type="primary", key=f"subj_submit_{st.session_state.subj_q_id}"):
                    if user_input.strip().lower() == target_word.lower():
                        st.session_state.subj_total += 1
                        st.session_state.subj_correct_cnt += 1
                        st.session_state.subj_solved = True
                        st.session_state.subj_feedback = ("success", f"🎉 정답입니다! 단어: **{target_word}** ({target_meaning})")
                        st.rerun()
                    else:
                        if not st.session_state.subj_retry:
                            st.session_state.subj_retry = True
                            st.session_state.subj_feedback = ("warning", "⚠️ 틀렸습니다! 다시 한 번 철자를 꼼꼼히 생각해보세요. (기회 1번 더!)")
                            st.rerun()
                        else:
                            st.session_state.subj_total += 1
                            st.session_state.subj_solved = True
                            st.session_state.subj_feedback = ("error", f"❌ 아쉽습니다. 정답은 **{target_word}** 입니다.")
                            st.rerun()
            else:
                render_tts_button(target_word, key=f"subj_ans_{st.session_state.subj_q_id}", show_word=True)
                if st.button("➡️ 다음 문제 풀기", type="primary", key=f"subj_next_{st.session_state.subj_q_id}"):
                    pick_subj_question(day_df)
                    st.rerun()

        # ---------------------------------------------------------
        # 5) 타임어택 랭킹전 (Day 세트 선택 + 랜덤 출제 + 랭킹 기록)
        # ---------------------------------------------------------
        elif menu == "⏱️ 타임어택 랭킹전":
            st.header("⏱️ 타임어택 스피드 랭킹전")
            st.write("원하는 **Day 세트**를 선택해 제한 시간 **10초** 안에 랜덤 출제 문제를 맞히세요! 최종 기록은 **명예의 전당**에 저장됩니다.")

            if "battle_started" not in st.session_state:
                st.session_state.battle_started = False
            if "battle_score" not in st.session_state:
                st.session_state.battle_score = 0
            if "battle_total" not in st.session_state:
                st.session_state.battle_total = 0
            if "b_q_id" not in st.session_state:
                st.session_state.b_q_id = 0
            if "battle_game_over" not in st.session_state:
                st.session_state.battle_game_over = False
            if "battle_fail_reason" not in st.session_state:
                st.session_state.battle_fail_reason = ""
            if "battle_record_saved" not in st.session_state:
                st.session_state.battle_record_saved = False
            if "battle_day_idx" not in st.session_state:
                st.session_state.battle_day_idx = 0

            def reset_battle_question(pool_df: pd.DataFrame, full_df: pd.DataFrame):
                # 선택한 Day 세트 내에서 랜덤 단어 선택
                row = pool_df.sample(1).iloc[0]
                b_word = str(row[word_col]).strip()
                b_correct = str(row[meaning_col]).strip()

                wrong_pool = pool_df[pool_df[word_col].astype(str).str.strip() != b_word]
                if len(wrong_pool) >= 3:
                    w_rows = wrong_pool.sample(3)
                else:
                    fallback_pool = full_df[full_df[word_col].astype(str).str.strip() != b_word]
                    w_rows = fallback_pool.sample(3)

                opts = [str(m).strip() for m in w_rows[meaning_col].values] + [b_correct]
                random.shuffle(opts)

                st.session_state.b_word = b_word
                st.session_state.b_correct = b_correct
                st.session_state.b_opts = opts
                st.session_state.b_q_id += 1
                st.session_state.battle_start_time = time.time()

            def save_battle_record():
                if not st.session_state.battle_record_saved:
                    total_elapsed = round(time.time() - st.session_state.battle_session_start, 1)
                    day_short = f"Day {st.session_state.battle_day_idx + 1}"
                    ranking_store.append({
                        "학습자": st.session_state.username,
                        "세트": day_short,
                        "점수(개)": st.session_state.battle_score,
                        "총 생존시간(초)": total_elapsed,
                        "도전 일시": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.session_state.battle_record_saved = True

            if not st.session_state.battle_started:
                selected_battle_label = st.selectbox("📅 도전할 Day 세트 선택", day_options, key="battle_day_select")
                selected_battle_idx = day_options.index(selected_battle_label)
                battle_day_df = get_day_slice(df, selected_battle_idx)

                st.markdown("---")
                if st.button("🚀 타임어택 랭킹전 시작하기", use_container_width=True, type="primary"):
                    st.session_state.battle_day_idx = selected_battle_idx
                    st.session_state.battle_started = True
                    st.session_state.battle_score = 0
                    st.session_state.battle_total = 0
                    st.session_state.battle_game_over = False
                    st.session_state.battle_fail_reason = ""
                    st.session_state.battle_record_saved = False
                    st.session_state.battle_session_start = time.time()
                    reset_battle_question(battle_day_df, df)
                    st.rerun()

                st.markdown("---")
                st.subheader("🏆 명예의 전당 (TOP 10 랭킹)")
                if len(ranking_store) > 0:
                    rank_df = pd.DataFrame(ranking_store)
                    rank_df = rank_df.sort_values(by=["점수(개)", "총 생존시간(초)"], ascending=[False, True]).head(10).reset_index(drop=True)
                    rank_df.index = rank_df.index + 1
                    rank_df.index.name = "순위"
                    st.dataframe(rank_df, use_container_width=True)
                else:
                    st.info("아직 등록된 랭킹 기록이 없습니다. 첫 번째 1위의 주인공이 되어보세요!")

            else:
                active_battle_df = get_day_slice(df, st.session_state.battle_day_idx)

                if st.session_state.battle_game_over:
                    save_battle_record()
                    if st.session_state.battle_fail_reason == "timeout":
                        st.error("⏰ 10초 시간 초과! 게임이 종료되었습니다.")
                    else:
                        st.error(f"❌ 오답입니다! 게임이 즉시 종료되었습니다. (정답은 '{st.session_state.b_correct}' 였습니다)")

                    st.subheader(
                        f"최종 결과: **{st.session_state.username}** 님 (Day {st.session_state.battle_day_idx + 1}) — "
                        f"맞춘 문제 **{st.session_state.battle_score}개**"
                    )
                    st.success("✅ 랭킹 보드에 기록이 등록되었습니다!")

                    if st.button("🔄 다시 도전하기 / 랭킹 확인", type="primary", key="battle_retry_btn"):
                        st.session_state.battle_started = False
                        st.session_state.battle_game_over = False
                        st.rerun()
                else:
                    elapsed = time.time() - st.session_state.battle_start_time
                    remaining = 10 - int(elapsed)

                    if remaining > 0:
                        st.caption(f"출제 범위: Day {st.session_state.battle_day_idx + 1} (랜덤 출제)")
                        col1, col2 = st.columns(2)
                        col1.metric(label="⏳ 남은 시간", value=f"{remaining}초")
                        col2.metric(label="🏆 현재 점수", value=f"{st.session_state.battle_score}점")

                        st.markdown(f"### 단어: **{st.session_state.b_word}**")
                        ans = st.radio(
                            "뜻을 고르세요:",
                            st.session_state.b_opts,
                            key=f"battle_radio_{st.session_state.b_q_id}"
                        )

                        if st.button("정답 제출", key=f"battle_submit_{st.session_state.b_q_id}", type="primary"):
                            st.session_state.battle_total += 1
                            if ans == st.session_state.b_correct:
                                st.session_state.battle_score += 1
                                reset_battle_question(active_battle_df, df)
                                st.rerun()
                            else:
                                st.session_state.battle_game_over = True
                                st.session_state.battle_fail_reason = "wrong"
                                st.rerun()

                        time.sleep(1)
                        st.rerun()
                    else:
                        st.session_state.battle_game_over = True
                        st.session_state.battle_fail_reason = "timeout"
                        st.rerun()
    else:
        st.warning("데이터를 로드할 수 없습니다.")
