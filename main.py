import numpy_financial as npf
import streamlit as st


def tax_paid_cal(net_income):
    if net_income >= 4530001:
        r = net_income * 0.4 - 829600
        return r, 0.4

    elif 2420001 <= net_income <= 4530000:
        r = net_income * 0.3 - 376600
        return r, 0.3

    elif 1210001 <= net_income <= 2420000:
        r = net_income * 0.2 - 134600
        return r, 0.2

    elif 540001 <= net_income <= 1210000:
        r = net_income * 0.12 - 37800
        return r, 0.12

    elif net_income <= 540000:
        r = net_income * 0.05
        return r, 0.05

    else:
        pass


st.title('勞退自提報酬率試算')
st.write('兩個變數可以經由網站搜尋取得，已便更精確的評估是否應該自提')
st.info('1. 谷歌搜尋:公告勞工退休金條例退休基金最近月份收益率')
st.write('已便取得退休基金平均收益率；也可根據您的直覺輸入預期勞退收益率')
st.info('2. 谷歌搜尋:勞工退休金個人專戶查詢')
st.write('已便取得勞工退休金個人專戶資料；也可輸入0')


st.subheader('試算應納稅額')
net_income = st.sidebar.number_input('輸入淨所得', value=600000)
original_paid = tax_paid_cal(net_income)
st.write('沒自提應付稅額:', int(original_paid[0]), '元')

st.subheader('以下試算退休後勞退收益報酬率')

withdraw_percent = st.sidebar.number_input('請輸入自提成數 %', min_value=1, max_value=6, value=6, step=1)
st.write('自提%數:', withdraw_percent, '%')

labor_fund_profit = st.sidebar.number_input('請輸入平均勞退收益率 %', value=3.59, step=0.01)
st.write('勞退收益率:', round(labor_fund_profit, 2), '%')

age_now = st.sidebar.number_input('請輸入目前年齡', value=30, step=1)
year_left = 65 - age_now
st.write('距離退休時間還有:', year_left, '年')

# FV:計算一項投資在未來的價值
# @rate:各期的利率
# @Nper:總付款期數
# @Pmt:各期給付的金額
# @Pv:未來付款的現值或目前總額,default 0

monthly_salary = st.sidebar.number_input('請輸入大約月薪:', value=50000, step=10000)
year_draw_money = monthly_salary * withdraw_percent/100 * 12
st.write('年自提金額:', int(year_draw_money), '元')
account_worth_now = st.sidebar.number_input('請輸入目前勞工退休金個人專戶總金額:', value=60000, step=10000)
fv_ = npf.fv(labor_fund_profit/100, year_left, -year_draw_money, account_worth_now)
fv = int(round(fv_, 0))
st.write('退休預計可取得勞退退休金:', fv, '元')

# RATE:回傳年金每期的利率
# @rate:各期的利率
# @Pmt:各期給付的金額
# @Pv:未來付款的現值或目前總額,default 0
# @Fv:最後一次付款完成後，所能獲得的未來值或現金餘額

after_tax_self_withdraw = year_draw_money * (1-original_paid[1])
st.write('扣稅後自提金額:', int(after_tax_self_withdraw), '元')
rate_ = npf.rate(year_left, -after_tax_self_withdraw, account_worth_now, fv)
rate = round(float(rate_ * 100), 2)
st.write('預期報酬率:', rate, '%')
