import streamlit as st
import random
import matplotlib.pyplot as plt

st.set_page_config(page_title="裝備強化模擬器", layout="centered")
st.title("📈 裝備強化模擬器")

# 使用者參數輸入
st.sidebar.header("🔧 模擬參數設定")
simulations = st.sidebar.number_input("模擬次數", 1000, 1_000_000, value=100_000, step=10000)
slots = st.sidebar.selectbox("裝備格數", [10, 7, 5], index=0)
threshold = st.sidebar.number_input("成功能力門檻", 0, 100, value=30)

st.sidebar.markdown("---")
st.sidebar.subheader("📜 各卷軸使用張數")

# 卷軸設定區
scrolls = {
    "10%": {"rate": 0.10, "destroy": False, "value": 5},
    "30%": {"rate": 0.30, "destroy": True, "value": 5},
    "60%": {"rate": 0.60, "destroy": False, "value": 2},
    "70%": {"rate": 0.70, "destroy": True, "value": 2},
    "100%": {"rate": 1.00, "destroy": False, "value": 1},
}

scroll_counts = {}
total_scrolls = 0
for name in scrolls:
    count = st.sidebar.number_input(f"{name} 卷", 0, slots, value=0, step=1)
    scroll_counts[name] = count
    total_scrolls += count

# 驗證
if total_scrolls > slots:
    st.error(f"使用的卷軸總數（{total_scrolls}）超過裝備格數（{slots}）")
    st.stop()

if st.button("🚀 開始模擬"):

    destroyed = 0
    success_counts = [0] * (slots + 1)
    ability_distribution = {}

    for _ in range(simulations):
        total_ability = 0
        destroyed_flag = False
        total_success = 0

        for name, count in scroll_counts.items():
            rate = scrolls[name]["rate"]
            can_destroy = scrolls[name]["destroy"]
            value = scrolls[name]["value"]

            for _ in range(count):
                if random.random() < rate:
                    total_ability += value
                    total_success += 1
                else:
                    if can_destroy and random.random() < 0.5:
                        destroyed += 1
                        destroyed_flag = True
                        break  # 裝備破壞停止強化

            if destroyed_flag:
                break

        if not destroyed_flag:
            if total_success <= slots:
                success_counts[total_success] += 1
            else:
                success_counts[slots] += 1

            ability_distribution[total_ability] = ability_distribution.get(total_ability, 0) + 1

    st.subheader("📊 模擬結果")
    st.write(f"總模擬數：{simulations}")
    st.write(f"裝備被破壞數量：**{destroyed}**（{destroyed / simulations * 100:.2f}%）")

    qualified = sum(count for ability, count in ability_distribution.items() if ability >= threshold)
    st.write(f"達到能力值 **+{threshold}** 的裝備數：**{qualified}**（{qualified / simulations * 100:.2f}%）")

    total_ability_value = sum(ability * count for ability, count in ability_distribution.items())
    avg_ability = total_ability_value / (simulations - destroyed) if simulations - destroyed > 0 else 0
    st.write(f"未被破壞裝備的平均能力值：**{avg_ability:.2f}**")

    st.subheader("✅ 成功格數分佈")
    for i, count in enumerate(success_counts):
        st.write(f"{i} 格成功：{count} 件（{count / simulations * 100:.2f}%）")

    st.subheader("📈 能力值分佈圖")
    sorted_keys = sorted(ability_distribution.keys())
    values = [ability_distribution[k] for k in sorted_keys]

    fig, ax = plt.subplots()
    ax.plot(sorted_keys, values, marker='o')
    ax.set_xlabel("能力值")
    ax.set_ylabel("件數")
    ax.set_title("能力值分佈（模擬結果）")
    st.pyplot(fig)
