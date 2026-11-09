import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="유튜브 영상 의도에 따른 시청자 반응 분석",
    layout="wide"
)

# -------------------------------------------------------------
# 1. 분석 데이터셋 (3개 주제 선정: 라면 논쟁, 한중 관계, 청년 실업)
# -------------------------------------------------------------
DATASET = {
    "주제 1: 신라면 vs 진라면": {
        "description": "식품 비교 영상의 프레이밍(진라면 승리 vs 패배)에 따른 댓글 반응 비교",
        "videos": [
            {
                "title": "진라면은 어떻게 신라면을 이길 수 있었을까",
                "url": "https://www.youtube.com/watch?v=RNiowLb5RSU",
                "intent": "진라면의 경쟁력 및 우세 강조",
                "agree_comments": [
                    "진라면만큼 저렴하고 맛도 무난한 라면이 없음 돈 없는 나같은 자취생들에겐 최고의 라면임ㅋㅋ",
                    "신라면 안먹은지 몇년은 된듯 진라면 매운맛에 계란 하나 풀어먹으면 크~",
                    "진라면은 진리지 그 매운맛의 얼큰함과 탱탱한 면발 정말 라면 그 자체....",
                    "진라면이 최고시다!!!!!",
                    "현재 진라면이 제일 맛남",
                    "진라면 개꿀맛"
                ],
                "disagree_comments": [
                    "아무리 맛 없어졌다 하더라도 신라면은 근본이다",
                    "이긴 적 없는데요 신라면이 부동의 판매 1위임.. 계속.",
                    "진라면은 일단 밀가루냄새가 너무나고 진하지가 않다"
                ]
            },
            {
                "title": "진라면이 신라면을 이길 수 없는 이유",
                "url": "https://www.youtube.com/shorts/mzwQiFPZDgA",
                "intent": "신라면의 우위 및 진라면의 한계 강조",
                "agree_comments": [
                    "이름부터 진라면이니까 지지 이긴라면이면 이긴다.",
                    "맞아 진라면은 달아서 자주 생각 안나더라",
                    "진라면은 마트입구에서부터 할인가로 나와있음ㅋㅋ 거기서부터 이미 모든라면으로부터 진거",
                    "애초에 난 진라면 맛있다는사람이 이해가안감 ㅋㅋㅋㅋㅋ",
                    "진라면 먹는사람은 그냥 싸니까 먹는거지",
                    "신라면 먹는 사람들이 맛잘알임"
                ],
                "disagree_comments": [
                    "신라면도 맛없음 이젠 거기서거기야",
                    "진라면 맛있게 잘 먹고 있는데...",
                    "신라면도 다수가 예전에비해 넘 맛없어졌다고 함 걍 케바케임",
                    "신라면은 최초 출시 때의 맛이 아니면 다시 먹고싶은 생각 없슴"
                ]
            }
        ]
    },
    "주제 2: 한중 청년 인식": {
        "description": "국가 간 혐오/친화 프레이밍에 따른 시청자 감정 동조 현상 분석",
        "videos": [
            {
                "title": "중국 청년들은 한국을 얼마나 싫어할까?",
                "url": "https://www.youtube.com/shorts/DncXZMm73n0",
                "intent": "중국 청년층의 반한 감정 및 반중 정서 자극",
                "agree_comments": [
                    "중국은 전세계가 싫어함",
                    "이게 공산당입니다 여러분.",
                    "원래 지능이 낮으면 세뇌 잘당함",
                    "듣던중 반가운 소리네요. 서로 싫어하는 나라들끼리 서로 방해하지말고 각자 갈길이나 갑시다",
                    "감사하다 한국을 싫어해 줘서 한국도 중국과 얽히고 싶지 않다",
                    "그렇게 싫은데 한국 못와서 난리... 교육이 제대로 되지 않아 한국의 것을 자기들 것이라 우김."
                ],
                "disagree_comments": [
                    "흠... 중국 유학 갔을때 저렇진 않았는데...머지"
                ]
            },
            {
                "title": "한국인을 유독 좋아하는 중국 현지 사람들",
                "url": "https://www.youtube.com/shorts/xITkqKiiEEQ",
                "intent": "중국 현지의 친한 정서 및 온정적 측면 부각",
                "agree_comments": [
                    "중국 어학연수 갔을때 느낌.. 한국인들 엄청 좋아해요",
                    "그냥 나라마다 사람이 케바케지.... 천사만 있는 나라도 없고 악마만 있는 나라도 없다.",
                    "역시 나라 이미지가 어떻든 좋으신 분들은 계시구나...",
                    "여기 중국인들은 착한데 인터넷속의 중국인들 왜 그런거야... 진짜 좋은사람들이네",
                    "저도 중국에 한 달 정도 머문 적이 있어요. 외국인 거의 없는 소도시인데 정말 친절한 분들이 많았네요.",
                    "막상 중국가면 중국사람들 한국인 엄청 좋아함.... 2년살았는데 나중에는 연예인병 살짝 올정도로 대우받음"
                ],
                "disagree_comments": [
                    "음식 식재료가 진짜인지부터 확인을",
                    "중공한테 돈 받음?"
                ]
            }
        ]
    },
    "주제 3: 쉬었음 청년 담론": {
        "description": "청년 구직 단념 현상에 대한 개인 책임론 vs 구조/사회적 책임론 프레이밍",
        "videos": [
            {
                "title": "쉬었음 청년이 많아지면 나라가 위험한 이유",
                "url": "https://www.youtube.com/shorts/9055nPa_lfY",
                "intent": "쉬었음 청년의 도덕적 해이 및 개인적 태도 비판",
                "agree_comments": [
                    "맞아요 힘든일 하기 싫고 깔끔한일 하고 싶어서 노는거지",
                    "맞아요 실업급여받는다고 일쉬면서 놀러다니고 기간 꽉채워서 쉼",
                    "맞습니다. 고르는거죠",
                    "일하기싫어서 집에서 노는애들많아요",
                    "청년 지원금 기초생활수급자 실업급여금 등등 악용하는 이들 한테 자꾸 금액을 증액 시켜 주는데 누가 일 하겠냐고",
                    "너무 인정합니다. 진짜 밥굶을수도 있으니 1시간 반 운전해서라도 돈 벌러 가더군요."
                ],
                "disagree_comments": []
            },
            {
                "title": "욕만먹고있는 쉬었음청년",
                "url": "https://www.youtube.com/shorts/JZOHFS_Dfa0",
                "intent": "가혹한 취업 환경과 구조적 문제 강조 및 청년 위로",
                "agree_comments": [
                    "올해 인턴십 채용에만 경력직이 수십명이 왔었어요. 얼마나 채용경쟁률이 센지 감도 안올정도더군요. 응원합니다..",
                    "원래 청년들한테도 신경쓰지않던 나라가 남의 일에 관심도 많은게 웃김",
                    "20,30,40,50 모두 힘내라...응원한다. 포기하지말고..... 잘 될지어다~~~",
                    "맞아. 사회의 문제를 개인에게 책임전가하는 게 우리나라 사회에 너무 많은 것 같아 문제임!",
                    "다들 너무 나를 몰아넣고 채찍질하지마세요 오늘 하루도 고생하셨습니다",
                    "청년들 기준에서는 마땅한 양질의 일자리가 없고 기업에서는 부품 꼭두각시 노예같이 일할사람을 구하고..."
                ],
                "disagree_comments": [
                    "부모들이 그놈의 대학에 목숨 걸어버리니까 애들이 눈만 높아지지;;",
                    "능력이 안되면 맞춰살던가 연구를해라",
                    "과연 진짜 일자리가 없어서일까...?",
                    "아직 살만한거다 진짜 극한까지 가면 무슨 일 이든 한다",
                    "풍요롭게 자라서 눈깔만높아서 힘든일을 안하려는 게 문제임 요즘애들은 편의점 알바도 하기싫어함",
                    "쉽게 일하는곳, 사무실에서만찾으니 자리가없지 현장으로 나와 힘든일이랑 정신만 차리면 일자리있다"
                ]
            }
        ]
    }
}

# -------------------------------------------------------------
# 2. UI 렌더링
# -------------------------------------------------------------
st.title("📊 유튜브 영상 의도에 따른 시청자 반응 분석 대시보드")
st.caption("영상의 프레이밍과 연출 의도가 시청자 댓글의 긍정/부정적 동조에 미치는 영향을 비교 분석합니다.")

# 10개 중 1차 구현된 3개 주제 탭 생성
tab_names = list(DATASET.keys())
tabs = st.tabs(tab_names)

for tab, topic_name in zip(tabs, tab_names):
    with tab:
        topic_info = DATASET[topic_name]
        st.info(f"📌 **주제 설명**: {topic_info['description']}")

        # 내부 페이지 전환 (요청에 따라 1, 2페이지 우선 구현)
        page = st.radio(
            "페이지 선택",
            ["Page 1: 댓글 긍정/부정 비율 분석 (원 그래프)", "Page 2: 영상별 대표 댓글 분석"],
            key=f"page_selector_{topic_name}",
            horizontal=True
        )
        st.divider()

        # =========================================================
        # PAGE 1: 원 그래프 (Donut Chart)
        # =========================================================
        if page.startswith("Page 1"):
            st.subheader("📈 영상 의도에 대한 댓글 동조/비동조 비율")
            col1, col2 = st.columns(2)

            for idx, col in enumerate([col1, col2]):
                video = topic_info["videos"][idx]
                agree_count = len(video["agree_comments"])
                disagree_count = len(video["disagree_comments"])
                total = agree_count + disagree_count

                with col:
                    st.markdown(f"#### 영상 {idx + 1}: [{video['title']}]({video['url']})")
                    st.markdown(f"**기획 의도:** `{video['intent']}`")

                    if total > 0:
                        fig = go.Figure(
                            data=[go.Pie(
                                labels=["영상 의도에 긍정(동조)", "영상 의도에 부정(반박)"],
                                values=[agree_count, disagree_count],
                                hole=0.45,
                                marker_colors=["#2b5c8f", "#d9534f"],
                                textinfo="percent+value",
                                textfont_size=13
                            )]
                        )
                        fig.update_layout(
                            showlegend=True,
                            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                            margin=dict(t=20, b=30, l=10, r=10),
                            height=330
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("분석 가능한 댓글 데이터가 없습니다.")

        # =========================================================
        # PAGE 2: 대표 댓글 목록
        # =========================================================
        elif page.startswith("Page 2"):
            st.subheader("💬 영상별 대표 댓글 모음")

            for idx, video in enumerate(topic_info["videos"]):
                st.markdown(f"### 영상 {idx + 1}. {video['title']}")
                st.markdown(f"🔗 [유튜브 바로가기]({video['url']}) | **기획 의도**: {video['intent']}")

                c_agree, c_disagree = st.columns(2)

                with c_agree:
                    st.success(f"👍 **영상 의도에 긍정 / 동조 ({len(video['agree_comments'])}개)**")
                    if video['agree_comments']:
                        for c in video['agree_comments'][:6]:  # 대표 댓글 6개
                            st.markdown(f"- {c}")
                    else:
                        st.write("*(해당 반응 댓글 없음)*")

                with c_disagree:
                    st.error(f"👎 **영상 의도에 부정 / 반박 ({len(video['disagree_comments'])}개)**")
                    if video['disagree_comments']:
                        for c in video['disagree_comments'][:6]:  # 대표 댓글 6개
                            st.markdown(f"- {c}")
                    else:
                        st.write("*(해당 반응 댓글 없음)*")

                st.markdown("---")