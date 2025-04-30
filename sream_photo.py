import streamlit as st
from PIL import Image
import numpy as np
import streamlit as st
import requests
from io import BytesIO

print("hello")
st.set_page_config(
    page_title = "포토북",
    page_icon = "./images/책.png"
)
st.title("📚PHOTO BOOK")
st.markdown("사진을 하나씩 등록해보세요!🌞")

def load_and_resize(image_path, target_width, target_height):
    if image_path.startswith("http"):  # URL이면 requests로 불러오기
        response = requests.get(image_path)
        img = Image.open(BytesIO(response.content)).convert("RGB")
    else:
        img = Image.open(image_path).convert("RGB")  # 로컬 이미지
    img = img.resize((target_width, target_height))
    return np.array(img)

type_list =["인물🙋🏻", "풍경⛰️", "여행🧳", "접사🌷", "패션👚", "음식🍰", "거리🛣️", "스포츠⚽️", "연예인💃", "기타✨"]
initial_photo =[
    {
        "name":"케이크",
        "types":["음식🍰"],
        "image_url":"https://i.namu.wiki/i/htTi1XgAj12M-217ZlFTvT2xfXNk4v5FDWstL-C24oiy3ZbZOEGIelCJPHi2hvoEMAHmyCBhsfW__h4hAYj_gLclTg03pcWma1I4-yjtHrHyHmSvLl4akS0I-drR0-W58_A4j7JMGz1Xm0usrrLYWQ.webp",
        "date":"2023"
    },
    {
        "name":"나비",
        "types":["접사🌷"],
        "image_url":"https://image.kr.canon/pds/editor/images/000019/20161114163703522_LO1LUXC1.png",
        "date":"2024"
    },
    {
        "name":"제주도",
        "types":["풍경⛰️"],
        "image_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR45n-koxI6aeoPOFXk7Zv-xxRUH63g3cQy5w&s",
        "date":"2025"
    },
    {
        "name":"축구",
        "types":["스포츠⚽️"],
        "image_url":"https://i.namu.wiki/i/hBDLtpaGIQON5ybKZxVtmd5G57UgL6DaSGMZeG2dpbkk-zVDs5RvcpLw3BzXga9TPCHK6u-JNla30r_gH2LntznpMfMonbGnlRXozNiF9STPGLkacS6oheslk3Js2NMrnBe_ngb538QxlI_tZF8bEA.webp",
        "date":"2021"
    }
]


example_photo = {
    "name": "닝닝",
    "types": ["연예인💃","인물🙋🏻"],
    "date": "2025",
    "image_url": "https://i.ytimg.com/vi/lW2xHXntXho/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLD-7ktAaVzj3dwdPnEYdOHTERDnhQ"
}

if "photo" not in st.session_state:
    st.session_state.photo = initial_photo

auto_complete = st.toggle("예시데이터로 채우기")
print("page_reload, auto_complete",auto_complete)

with st.form(key="form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input(
            label="사진 이름",
            value=example_photo["name"] if auto_complete else ""
        )
        date = st.text_input(
            label = "사진 연도",
            value = example_photo["date"] if auto_complete else ""
        )
    with col2:
        types = st.multiselect(
            label="사진 종류",
            options=type_list,
            max_selections=2,
            default= example_photo['types'] if auto_complete else []
            )
        image_url = st.text_input(
            label="사진 url",
            value= example_photo['image_url'] if auto_complete else ""
            )
    submit =st.form_submit_button(label="Submit")


    if submit:
        if not name:
            st.error("사진의 이름을 입력해주세요")
        elif len(types) ==0:
            st.error("사진의 속성을 적어도 한개 선택해주세요")
        elif not date:
            st.error("사진의 연도를 입력해주세요")
        else:
            st.success("사진을 추가할 수 있습니다")
            st.session_state.photo.append({
                "name":name,
                "types":types,
                "image_url":image_url if image_url else"./images/default.png",
                "date":date
            })


for i in range(0, len(st.session_state.photo), 4):
    row_photo = st.session_state.photo[i:i+4]
    cols = st.columns(4)
    for j in range(len(row_photo)):
        with cols[j]:
            photo = row_photo[j]
            with st.expander(label= f"**{i+j+1}.{photo['name']}**", expanded=True):
                img = load_and_resize(photo["image_url"],300,200)
                st.image(img)
                types = [f"{x}" for x in photo["types"]]
                st.badge(" / ".join(types))
                st.caption(f"연도: {photo['date']}")
                delete_button = st.button(label="삭제", key=i+j, use_container_width=True)
                if delete_button:
                    print("delete button clicked")
                    del st.session_state.photo[i+j]
                    st.rerun()
            st.divider()
