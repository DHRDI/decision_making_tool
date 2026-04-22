import streamlit as st

# 1. 앱 설정
st.set_page_config(page_title="리더를 위한 의사결정 코치", page_icon="💡", layout="wide")

# 버튼 및 라디오 버튼 색상 커스텀 CSS
st.markdown("""
    <style>
    /* 라디오 버튼 선택 시 강조 색상 변경 */
    div[data-testid="stWidgetSelectionState"] {
        background-color: #e8f0fe !important;
        border-radius: 10px;
    }
    /* 버튼 호버 효과 */
    .stButton>button:hover {
        border-color: #4CAF50;
        color: #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

# 제목 및 안내
st.title("💡 리더를 위한 의사결정 코치")
st.markdown("---")
st.info("이슈별 의사결정 방법을 선택할 때 참고할 수 있는 심플한 진단입니다. 각 문항을 예, 아니오 중 하나에 체크하면 됩니다.")

# 2. 7문항 배치 (기본값을 None으로 설정하여 선택을 유도)
st.subheader("📋 상황 진단 (Decision Tree)")
col1, col2 = st.columns(2)

with col1:
    q1 = st.radio("1. 결정의 질: 의사결정의 질이 중요합니까?", ["예", "아니오"], key="q1", index=None)
    q2 = st.radio("2. 수용의 중요성: 팀원들의 수용(Commitment)이 결정에 중요합니까?", ["예", "아니오"], key="q2", index=None)
    q3 = st.radio("3. 정보 가용성: 리더님께 스스로 결정할 충분한 정보가 있습니까?", ["예", "아니오"], key="q3", index=None)
    q4 = st.radio("4. 문제의 구조: 해결해야 할 문제가 명확합니까?", ["예", "아니오"], key="q4", index=None)

with col2:
    q5 = st.radio("5. 수용 가능성: 리더님이 혼자 결정해도 팀원들이 지지할까요?", ["예", "아니오"], key="q5", index=None)
    q6 = st.radio("6. 목표 공유: 구성원들이 목표를 공유하고 있습니까?", ["예", "아니오"], key="q6", index=None)
    q7 = st.radio("7. 구성원 갈등: 이 결정으로 팀원 간 마찰이 생길 것 같습니까?", ["예", "아니오"], key="q7", index=None)

st.markdown("---")

# 3. 로직 엔진 (동일)
def get_decision(ans):
    if None in ans:
        return "INCOMPLETE"
    v1, v2, v3, v4, v5, v6, v7 = ans
    if v1 == "아니오":
        if v2 == "아니오": return "AI"
        else: return "AI" if v3 == "예" else "GII"
    else: 
        if v2 == "아니오":
            if v3 == "예": return "AI"
            else:
                if v4 == "아니오": return "CII"
                else:
                    if v5 == "예": return "CI" if v6 == "예" else "AII"
                    else: return "AII"
        else:
            if v3 == "예":
                return "AII" if v4 == "예" else ("GII" if v5 == "예" else "CII")
            else:
                if v4 == "아니오":
                    if v5 == "예": return "CII"
                    else: return "GII" if v6 == "예" else "CII"
                else:
                    if v5 == "예":
                        if v6 == "예": return "CI" if v7 == "예" else "AII"
                        else: return "AII"
                    else:
                        if v6 == "예": return "GII" if v7 == "예" else "CII"
                        else: return "CII"

# 4. 결과 출력용 데이터 (동일)
style_map = {"AI": "AI (독단형)", "AII": "AII (정보수집형)", "CI": "CI (개별 협의형)", "CII": "CII (집단 협의형)", "GII": "GII (위임형)"}
content = {
    "AI": {
        "one": "빠르게 혼자 결정하다",
        "feat": "정보가 충분하거나 시간 압박이 클 때 적합함",
        "mind": "결단력과 직관, 신속한 실행 중심",
        "questions": ["내 판단을 뒷받침할 객관적 데이터가 충분한가?", "지금 직접 결정하는 것이 팀의 실행 속도를 높이는가?", "결정의 이유를 팀원들이 납득할 수 있게 설명할 수 있는가?"],
        "books": ["『생각에 관한 생각』 / 대니얼 카너먼", "『리더는 결정으로 말한다』 / 김호준"]
    },
    "AII": {
        "one": "의견은 듣지만 결정은 리더가 한다",
        "feat": "정보 수집이 필요하며 책임은 리더에게 있음",
        "mind": "데이터 기반의 판단과 분석적 사고",
        "questions": ["내가 얻은 정보가 한쪽에 치우친 의견은 아닌가?", "팀원들에게 이 정보가 어디에 쓰일지 명확히 알렸는가?", "수집된 정보를 통합할 나만의 판단 기준은 무엇인가?"],
        "books": ["『팩트풀니스』 / 한스 로슬링", "『OKR』 / 존 도어"]
    },
    "CI": {
        "one": "개별적으로 의견을 듣고 종합한다",
        "feat": "1:1 소통 중심, 구성원의 심리적 안전감 확보가 핵심",
        "mind": "경청을 통해 동기를 부여하는 코칭형 사고",
        "questions": ["1:1 대화에서 팀원이 솔직한 우려를 말할 만큼 편안했는가?", "각기 다른 의견들 사이에서 공통된 접점을 찾았는가?", "내 결정이 팀원의 의견과 다를 때 그를 어떻게 따로 배려할 것인가?"],
        "books": ["『크루셜 컨버세이션』 / 케리 패터슨", "『코칭의 힘』 / 마이클 번게이 스태니어"]
    },
    "CII": {
        "one": "회의를 통해 집단 지성을 활용한다",
        "feat": "팀 토론 중심, 수용성과 갈등 관리가 중요한 경우",
        "mind": "협업과 토론을 촉진하는 퍼실리테이션 사고",
        "questions": ["회의 중 반대 의견이 자유롭게 나올 수 있는 분위기인가?", "팀원들이 리더의 답을 맞히기 위해 눈치를 보고 있진 않은가?", "우리 팀이 합의할 수 있는 최선의 타협점은 어디인가?"],
        "books": ["『팀장의 탄생』 / 줄리 주오", "『회의는 죽었다』 / 패트릭 렌시오니"]
    },
    "GII": {
        "one": "팀이 결정하고 리더는 지원한다",
        "feat": "자율성 극대화, 리더는 촉진자 역할을 수행",
        "mind": "전폭적인 신뢰와 위임을 통한 서번트 리더십",
        "questions": ["팀의 결정을 수용하고 책임질 준비가 되어 있는가?", "팀이 길을 잃지 않도록 최소한의 가이드라인을 주었는가?", "결과보다 '팀이 스스로 결정했다'는 사실에 집중하고 있는가?"],
        "books": ["『턴 더 쉽 어라운드!』 / 데이비드 마퀘트", "『드라이브』 / 다니엘 핑크"]
    }
}

# 5. 실행 및 출력
if st.button("🚀 최적의 의사결정 스타일 확인"):
    ans_list = [q1, q2, q3, q4, q5, q6, q7]
    res_code = get_decision(ans_list)
    
    if res_code == "INCOMPLETE":
        st.warning("⚠️ 모든 문항에 답변해 주세요!")
    else:
        sel = content[res_code]
        st.success(f"### 추천 스타일: {style_map[res_code]}")
        st.info(f"**📣 {sel['one']}**")
        
        c1, c2 = st.columns(2)
        with c1:
            st.write("📌 **주요 특징**")
            st.write(sel['feat'])
        with c2:
            st.write("🧠 **리더의 사고방식**")
            st.write(sel['mind'])
        
        st.markdown("---")
        st.subheader("❓ 이슈 대응력을 높이는 셀프 코칭 질문")
        for q in sel['questions']:
            st.write(f"- {q}")
            
        st.markdown("---")
        st.subheader("📚 역량 강화를 위한 추천 도서")
        for b in sel['books']:
            st.write(f"- {b}")
    
    st.markdown("---")
    st.caption("👨‍🏫 본 모델은 Waterford Institute of Technology 자료를 참고하여 DHRDI에서 제작하였습니다.")