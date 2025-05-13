import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Drug Release Calculator", layout="centered")

st.title("Pharmaceutical Drug Release Calculator")
st.markdown("بررسی تأثیر پارامترها بر فرمول دارورسانی")

st.sidebar.header("Input Parameters")

# ورودی‌ها
De = st.sidebar.number_input("Effective Diffusion Coefficient (De) [cm²/s]", min_value=1e-8, max_value=1e-3, value=1e-6, step=1e-7, format="%.1e")
tau = st.sidebar.slider("Tortuosity (τ)", min_value=0.5, max_value=5.0, value=2.0, step=0.1)
A = st.sidebar.slider("Surface Area (A) [cm²]", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
eps = st.sidebar.slider("Porosity (ε)", min_value=0.1, max_value=0.9, value=0.4, step=0.05)
Cs = st.sidebar.number_input("Solubility (Cs) [g/cm³]", min_value=0.001, max_value=0.1, value=0.01, step=0.001)
t = st.sidebar.number_input("Time (t) [s]", min_value=1, max_value=86400, value=3600, step=60)

# محاسبه Q
def calculate_Q(De, tau, A, eps, Cs, t):
    term = (2 * A - eps * Cs)
    if term <= 0:
        return None
    Q = ((De / tau) * term * Cs * t) ** 0.5
    return Q

Q = calculate_Q(De, tau, A, eps, Cs, t)

st.subheader("Calculated Drug Release (Q):")
if Q is not None:
    st.success(f"Q = {Q:.5f} (units based on input)")
else:
    st.error("Invalid parameters: ensure that (2A - εCs) > 0")

# رسم نمودار بر حسب زمان
st.subheader("1. Drug Release over Time")
plot_time = st.checkbox("نمایش نمودار Q بر حسب زمان")

if plot_time:
    time_range = np.linspace(1, 7200, 200)
    Q_values = [calculate_Q(De, tau, A, eps, Cs, ti) for ti in time_range]
    plt.figure(figsize=(8, 4))
    plt.plot(time_range / 60, Q_values, color='purple')
    plt.xlabel("Time (minutes)")
    plt.ylabel("Q (drug released)")
    plt.title("Q vs. Time")
    plt.grid(True)
    st.pyplot(plt)

# نمودار تغییر Q با یکی از پارامترها
st.subheader("2. Effect of a Parameter on Q")

param_to_vary = st.selectbox("Select parameter to vary:", ["De", "τ", "A", "ε", "Cs"])

param_ranges = {
    "De": np.linspace(1e-8, 1e-3, 200),
    "τ": np.linspace(0.5, 5.0, 200),
    "A": np.linspace(0.1, 5.0, 200),
    "ε": np.linspace(0.1, 0.9, 200),
    "Cs": np.linspace(0.001, 0.1, 200)
}

Q_vals = []
x_vals = param_ranges[param_to_vary]

for val in x_vals:
    args = {
        "De": De,
        "tau": tau,
        "A": A,
        "eps": eps,
        "Cs": Cs,
        "t": t
    }
    args[param_to_vary if param_to_vary != "τ" else "tau"] = val
    q = calculate_Q(**args)
    Q_vals.append(q if q is not None else np.nan)

plt.figure(figsize=(8, 4))
plt.plot(x_vals, Q_vals, label=f"Q vs {param_to_vary}", color='darkgreen')
plt.xlabel(param_to_vary)
plt.ylabel("Q (drug released)")
plt.title(f"Q vs. {param_to_vary}")
plt.grid(True)
st.pyplot(plt)

st.markdown("---")
st.caption("Developed by Zahra – Pharmaceutical Science Project")