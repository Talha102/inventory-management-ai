import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="InvenAI — Smart Inventory",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS — Dark Professional Theme
# ============================================
st.markdown("""
<style>
    .main { background-color: #0a0a0f; }
    .stApp { background-color: #0a0a0f; }
    
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #7c6af7;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin: 5px;
    }
    .metric-title {
        color: #a0a0c0;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .metric-value {
        color: #ffffff;
        font-size: 28px;
        font-weight: 800;
        margin: 8px 0;
    }
    .critical { border-color: #ff4444; }
    .warning { border-color: #ffaa00; }
    .good { border-color: #00cc66; }
    
    .alert-critical {
        background: rgba(255,68,68,0.1);
        border: 1px solid #ff4444;
        border-radius: 8px;
        padding: 10px 15px;
        margin: 5px 0;
        color: #ff6666;
    }
    .alert-warning {
        background: rgba(255,170,0,0.1);
        border: 1px solid #ffaa00;
        border-radius: 8px;
        padding: 10px 15px;
        margin: 5px 0;
        color: #ffcc44;
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0d1a 0%, #1a1a2e 100%);
        border-right: 1px solid #7c6af7;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# LOAD DATA
# ============================================
@st.cache_data
def load_data():
    inventory = pd.read_csv('data/inventory.csv')
    suppliers = pd.read_csv('data/suppliers.csv')
    sales = pd.read_csv('data/sales_history.csv')
    sales['date'] = pd.to_datetime(sales['date'])
    return inventory, suppliers, sales

inventory, suppliers, sales = load_data()

# ============================================
# SIDEBAR NAVIGATION
# ============================================
st.sidebar.markdown("## 📦 InvenAI")
st.sidebar.markdown("*Smart Inventory Management*")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Dashboard", "📋 Inventory", "🔄 Reorder System", "🤝 Suppliers", "📊 Analytics"]
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Last Updated:** {datetime.now().strftime('%d %b %Y, %H:%M')}")

# ============================================
# HELPER FUNCTIONS
# ============================================
def get_stock_status(row):
    if row['current_stock'] <= row['min_stock'] * 0.5:
        return 'Critical'
    elif row['current_stock'] <= row['min_stock']:
        return 'Low'
    else:
        return 'Good'

inventory['status'] = inventory.apply(get_stock_status, axis=1)
inventory['stock_value_pkr'] = inventory['current_stock'] * inventory['unit_price']
inventory['profit_margin'] = ((inventory['unit_price'] - inventory['cost_price']) / inventory['unit_price'] * 100).round(1)

# ============================================
# PAGE 1 — MAIN DASHBOARD
# ============================================
if page == "🏠 Dashboard":
    st.title("🏠 InvenAI Dashboard")
    st.markdown("*Real-time inventory intelligence for your coffee & juice shop*")
    st.markdown("---")

    # KPI CARDS
    total_value = inventory['stock_value_pkr'].sum()
    critical_items = len(inventory[inventory['status'] == 'Critical'])
    low_items = len(inventory[inventory['status'] == 'Low'])
    good_items = len(inventory[inventory['status'] == 'Good'])
    total_revenue = sales['revenue'].sum()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Inventory Value</div>
            <div class="metric-value">PKR {total_value:,.0f}</div>
            <div style="color:#7c6af7">📦 {len(inventory)} Items</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card critical">
            <div class="metric-title">Critical Stock</div>
            <div class="metric-value" style="color:#ff4444">{critical_items}</div>
            <div style="color:#ff6666">⚠️ Order Immediately!</div>
        </div>""", unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card warning">
            <div class="metric-title">Low Stock</div>
            <div class="metric-value" style="color:#ffaa00">{low_items}</div>
            <div style="color:#ffcc44">⚡ Order Soon</div>
        </div>""", unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card good">
            <div class="metric-title">Total Revenue</div>
            <div class="metric-value" style="color:#00cc66">PKR {total_revenue:,.0f}</div>
            <div style="color:#44ee88">📈 All Time</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ALERTS
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🚨 Critical Alerts")
        critical = inventory[inventory['status'] == 'Critical']
        if len(critical) > 0:
            for _, row in critical.iterrows():
                st.markdown(f"""
                <div class="alert-critical">
                    ⛔ <b>{row['item_name']}</b> — Only {row['current_stock']} {row['unit']} left!
                    (Min: {row['min_stock']} {row['unit']})
                </div>""", unsafe_allow_html=True)
        else:
            st.success("✅ No critical alerts!")

    with col2:
        st.markdown("### ⚠️ Low Stock Warnings")
        low = inventory[inventory['status'] == 'Low']
        if len(low) > 0:
            for _, row in low.iterrows():
                st.markdown(f"""
                <div class="alert-warning">
                    ⚡ <b>{row['item_name']}</b> — {row['current_stock']} {row['unit']} remaining
                    (Min: {row['min_stock']} {row['unit']})
                </div>""", unsafe_allow_html=True)
        else:
            st.success("✅ All stock levels good!")

    st.markdown("---")

    # CHARTS
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 Stock Levels by Item")
        colors = {'Critical': '#ff4444', 'Low': '#ffaa00', 'Good': '#00cc66'}
        fig = px.bar(
            inventory.sort_values('current_stock'),
            x='current_stock', y='item_name',
            color='status',
            color_discrete_map=colors,
            orientation='h',
            template='plotly_dark'
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 🥧 Stock Value by Category")
        cat_value = inventory.groupby('category')['stock_value_pkr'].sum().reset_index()
        fig2 = px.pie(
            cat_value, values='stock_value_pkr', names='category',
            template='plotly_dark',
            color_discrete_sequence=['#7c6af7','#00d4ff','#ff6b6b','#ffd93d','#6bcb77']
        )
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        st.plotly_chart(fig2, use_container_width=True)

# ============================================
# PAGE 2 — INVENTORY
# ============================================
elif page == "📋 Inventory":
    st.title("📋 Inventory Management")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        category_filter = st.multiselect("Category", inventory['category'].unique(), default=inventory['category'].unique())
    with col2:
        status_filter = st.multiselect("Status", ['Critical', 'Low', 'Good'], default=['Critical', 'Low', 'Good'])
    with col3:
        search = st.text_input("Search Item", "")

    filtered = inventory[
        (inventory['category'].isin(category_filter)) &
        (inventory['status'].isin(status_filter))
    ]
    if search:
        filtered = filtered[filtered['item_name'].str.contains(search, case=False)]

    st.markdown(f"**Showing {len(filtered)} items**")

    def color_status(val):
        if val == 'Critical':
            return 'background-color: rgba(255,68,68,0.2); color: #ff4444'
        elif val == 'Low':
            return 'background-color: rgba(255,170,0,0.2); color: #ffaa00'
        return 'background-color: rgba(0,204,102,0.2); color: #00cc66'

    display_cols = ['item_name', 'category', 'current_stock', 'min_stock', 'max_stock', 'unit', 'unit_price', 'status']
    styled = filtered[display_cols].style.map(color_status, subset=['status'])
    st.dataframe(styled, use_container_width=True, height=400)

    csv = filtered.to_csv(index=False)
    st.download_button("📥 Download Filtered Data", csv, "inventory_filtered.csv", "text/csv")

# ============================================
# PAGE 3 — REORDER SYSTEM
# ============================================
elif page == "🔄 Reorder System":
    st.title("🔄 Smart Reorder System")
    st.markdown("*AI-powered reorder suggestions*")
    st.markdown("---")

    reorder_items = inventory[inventory['status'].isin(['Critical', 'Low'])].copy()
    reorder_items['reorder_qty'] = reorder_items['max_stock'] - reorder_items['current_stock']
    reorder_items['reorder_cost'] = reorder_items['reorder_qty'] * reorder_items['cost_price']
    reorder_items['days_left'] = (reorder_items['current_stock'] / reorder_items['min_stock'] * 3).round(1)

    reorder_with_supplier = reorder_items.merge(suppliers, on='supplier_id', how='left')

    st.markdown(f"### 🛒 {len(reorder_items)} Items Need Reordering")
    st.markdown(f"**Total Reorder Cost: PKR {reorder_items['reorder_cost'].sum():,.0f}**")
    st.markdown("---")

    for supplier_name, group in reorder_with_supplier.groupby('supplier_name'):
        with st.expander(f"🏪 {supplier_name} — {len(group)} items"):
            supplier_info = group.iloc[0]
            col1, col2, col3 = st.columns(3)
            col1.metric("Contact", supplier_info['contact_person'])
            col2.metric("Phone", supplier_info['phone'])
            col3.metric("Lead Time", f"{supplier_info['lead_time_days']} days")

            for _, item in group.iterrows():
                status_color = "🔴" if item['status'] == 'Critical' else "🟡"
                st.markdown(f"""
                {status_color} **{item['item_name']}** — Order: **{item['reorder_qty']} {item['unit']}** 
                | Cost: PKR {item['reorder_cost']:,.0f} | Days left: ~{item['days_left']}
                """)

# ============================================
# PAGE 4 — SUPPLIERS
# ============================================
elif page == "🤝 Suppliers":
    st.title("🤝 Supplier Management")
    st.markdown("---")

    for _, supplier in suppliers.iterrows():
        with st.expander(f"🏪 {supplier['supplier_name']} — ⭐ {supplier['reliability_score']}"):
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Contact", supplier['contact_person'])
            col2.metric("City", supplier['city'])
            col3.metric("Phone", supplier['phone'])
            col4.metric("Lead Time", f"{supplier['lead_time_days']} days")

            st.markdown(f"""
            <div class="alert-warning">
                📱 WhatsApp Alert Preview: "Dear {supplier['contact_person']}, 
                please arrange delivery for our pending order. 
                Lead time expected: {supplier['lead_time_days']} day(s). — InvenAI System"
            </div>
            """, unsafe_allow_html=True)

# ============================================
# PAGE 5 — ANALYTICS
# ============================================
elif page == "📊 Analytics":
    st.title("📊 Sales & Analytics")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📈 Daily Revenue Trend")
        daily_sales = sales.groupby('date')['revenue'].sum().reset_index()
        fig = px.line(daily_sales, x='date', y='revenue', template='plotly_dark',
                      color_discrete_sequence=['#7c6af7'])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 🏆 Top Selling Items")
        top_items = sales.groupby('item_name')['quantity_sold'].sum().nlargest(10).reset_index()
        fig2 = px.bar(top_items, x='quantity_sold', y='item_name', orientation='h',
                      template='plotly_dark', color_discrete_sequence=['#00d4ff'])
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### 💰 Revenue by Category")
        sales_with_cat = sales.merge(inventory[['item_name','category']], on='item_name', how='left')
        cat_revenue = sales_with_cat.groupby('category')['revenue'].sum().reset_index()
        fig3 = px.pie(cat_revenue, values='revenue', names='category', template='plotly_dark',
                      color_discrete_sequence=['#7c6af7','#00d4ff','#ff6b6b','#ffd93d','#6bcb77'])
        fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown("### 📊 Profit Margin by Item")
        fig4 = px.bar(inventory.sort_values('profit_margin', ascending=False),
                      x='item_name', y='profit_margin', template='plotly_dark',
                      color='profit_margin', color_continuous_scale='viridis')
        fig4.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig4, use_container_width=True)