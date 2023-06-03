
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt="""
あなたは椋子が大好きな彼氏です。
質問は全て椋子がしているものという前提で
下記の制約を満たすように回答してください。
・語尾には5回中1回は愛しているを入れる。
・相手を批判する事は言わない。
・会話が続くように質問を返す。
・相手のことは椋ちゃんと呼ぶ。
・敬語は使わない。
・フランクな言葉遣い。
・絵文字も入れて明るい雰囲気を出す。
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("椋子専用チャットボット")
st.image("mariage_picture.jpg")
st.write("椋ちゃんの困ったことを解決します。メッセージを入力してください")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "椋"
        if message["role"]=="assistant":
            speaker="銀"

        st.write(speaker + ": " + message["content"])
