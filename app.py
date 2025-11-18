"""
Highlands Coffee Pricing Dashboard - Interactive Streamlit Application
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data import get_product_data, get_sales_data, get_store_comparison_data

# Page configuration
st.set_page_config(
    page_title="Highlands Coffee Pricing Dashboard",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #D4AF37;
        text-align: center;
        padding: 1rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">☕ Highlands Coffee Pricing Dashboard</p>', unsafe_allow_html=True)
st.markdown("---")

# Load data
@st.cache_data
def load_data():
    product_df = get_product_data()
    sales_df = get_sales_data()
    store_df = get_store_comparison_data()
    return product_df, sales_df, store_df

product_df, sales_df, store_df = load_data()

# Sidebar filters
st.sidebar.header("🎛️ Filters & Options")

# Category filter
selected_categories = st.sidebar.multiselect(
    "Select Categories",
    options=product_df['Category'].unique(),
    default=product_df['Category'].unique()
)

# Price range filter
price_range = st.sidebar.slider(
    "Price Range (VND)",
    min_value=int(product_df['Price (VND)'].min()),
    max_value=int(product_df['Price (VND)'].max()),
    value=(int(product_df['Price (VND)'].min()), int(product_df['Price (VND)'].max())),
    step=1000
)

# Filter data based on selection
filtered_products = product_df[
    (product_df['Category'].isin(selected_categories)) &
    (product_df['Price (VND)'] >= price_range[0]) &
    (product_df['Price (VND)'] <= price_range[1])
]

# Main content tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "💰 Pricing Analysis", "📈 Sales Trends", "🏪 Store Comparison"])

# TAB 1: Overview
with tab1:
    st.header("Business Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_products = len(filtered_products)
        st.metric("Total Products", total_products)
    
    with col2:
        avg_price = filtered_products['Price (VND)'].mean()
        st.metric("Avg Price", f"{avg_price:,.0f} VND")
    
    with col3:
        avg_margin = filtered_products['Margin (%)'].mean()
        st.metric("Avg Margin", f"{avg_margin:.1f}%")
    
    with col4:
        total_profit_potential = filtered_products['Profit (VND)'].sum()
        st.metric("Total Profit Potential", f"{total_profit_potential:,.0f} VND")
    
    st.markdown("---")
    
    # Product table with interactive features
    st.subheader("Product Catalog")
    
    # Sort options
    sort_col = st.selectbox(
        "Sort by:",
        options=['Product', 'Price (VND)', 'Profit (VND)', 'Margin (%)'],
        index=1
    )
    sort_order = st.radio("Order:", ["Ascending", "Descending"], horizontal=True)
    
    sorted_df = filtered_products.sort_values(
        by=sort_col,
        ascending=(sort_order == "Ascending")
    )
    
    # Display dataframe with highlighting
    st.dataframe(
        sorted_df.style.background_gradient(subset=['Margin (%)'], cmap='RdYlGn')
                       .format({
                           'Price (VND)': '{:,.0f}',
                           'Cost (VND)': '{:,.0f}',
                           'Profit (VND)': '{:,.0f}',
                           'Margin (%)': '{:.2f}%'
                       }),
        use_container_width=True,
        height=400
    )

# TAB 2: Pricing Analysis
with tab2:
    st.header("Pricing Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Price distribution by category
        fig_price = px.box(
            filtered_products,
            x='Category',
            y='Price (VND)',
            color='Category',
            title='Price Distribution by Category',
            labels={'Price (VND)': 'Price (VND)'},
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_price.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_price, use_container_width=True)
    
    with col2:
        # Profit margin by category
        fig_margin = px.bar(
            filtered_products.groupby('Category')['Margin (%)'].mean().reset_index(),
            x='Category',
            y='Margin (%)',
            color='Category',
            title='Average Profit Margin by Category',
            color_discrete_sequence=px.colors.qualitative.Pastel,
            text_auto='.2f'
        )
        fig_margin.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_margin, use_container_width=True)
    
    st.markdown("---")
    
    # Interactive scatter plot
    st.subheader("Price vs Profit Analysis")
    
    size_option = st.radio(
        "Bubble size represents:",
        ["Equal", "Margin (%)"],
        horizontal=True
    )
    
    fig_scatter = px.scatter(
        filtered_products,
        x='Price (VND)',
        y='Profit (VND)',
        color='Category',
        size='Margin (%)' if size_option == "Margin (%)" else None,
        hover_name='Product',
        hover_data={
            'Price (VND)': ':,.0f',
            'Profit (VND)': ':,.0f',
            'Margin (%)': ':.2f'
        },
        title='Product Positioning: Price vs Profit',
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig_scatter.update_layout(height=500)
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Price optimization suggestions
    st.subheader("💡 Pricing Insights")
    
    high_margin = filtered_products[filtered_products['Margin (%)'] > 50]
    low_margin = filtered_products[filtered_products['Margin (%)'] < 30]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success(f"**High Margin Products ({len(high_margin)}):**")
        if len(high_margin) > 0:
            for _, product in high_margin.iterrows():
                st.write(f"- {product['Product']}: {product['Margin (%)']:.1f}% margin")
        else:
            st.write("No products with >50% margin in current selection")
    
    with col2:
        st.warning(f"**Low Margin Products ({len(low_margin)}):**")
        if len(low_margin) > 0:
            for _, product in low_margin.iterrows():
                st.write(f"- {product['Product']}: {product['Margin (%)']:.1f}% margin")
        else:
            st.write("No products with <30% margin in current selection")

# TAB 3: Sales Trends
with tab3:
    st.header("Sales Trends Analysis")
    
    # Product selector for trends
    selected_products_trend = st.multiselect(
        "Select products to compare:",
        options=product_df['Product'].unique(),
        default=product_df['Product'].unique()[:3]
    )
    
    if selected_products_trend:
        # Filter sales data
        trend_data = sales_df[sales_df['Product'].isin(selected_products_trend)]
        
        # Aggregate by date
        daily_sales = trend_data.groupby(['Date', 'Product'])['Quantity'].sum().reset_index()
        
        # Line chart for sales trends
        fig_trend = px.line(
            daily_sales,
            x='Date',
            y='Quantity',
            color='Product',
            title='Daily Sales Volume Trends',
            labels={'Quantity': 'Units Sold', 'Date': 'Date'},
            markers=True
        )
        fig_trend.update_layout(height=500, hovermode='x unified')
        st.plotly_chart(fig_trend, use_container_width=True)
        
        st.markdown("---")
        
        # Sales summary statistics
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Sales Summary")
            for product in selected_products_trend:
                product_sales = sales_df[sales_df['Product'] == product]['Quantity']
                total_sales = product_sales.sum()
                avg_sales = product_sales.mean()
                
                with st.expander(f"📦 {product}"):
                    st.metric("Total Units Sold", f"{total_sales:,}")
                    st.metric("Avg Daily Sales", f"{avg_sales:.0f}")
                    st.metric("Peak Day Sales", f"{product_sales.max()}")
        
        with col2:
            # Category performance pie chart
            st.subheader("Sales by Category")
            
            # Merge with product data to get categories
            sales_with_cat = sales_df.merge(product_df[['Product', 'Category']], on='Product')
            category_sales = sales_with_cat.groupby('Category')['Quantity'].sum().reset_index()
            
            fig_pie = px.pie(
                category_sales,
                values='Quantity',
                names='Category',
                title='Sales Distribution by Category',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("Please select at least one product to view trends.")

# TAB 4: Store Comparison
with tab4:
    st.header("Store Performance Comparison")
    
    # Store selection
    selected_stores = st.multiselect(
        "Select stores to compare:",
        options=store_df['Store'].unique(),
        default=store_df['Store'].unique()
    )
    
    if selected_stores:
        filtered_stores = store_df[store_df['Store'].isin(selected_stores)]
        
        # Metrics comparison
        col1, col2 = st.columns(2)
        
        with col1:
            # Revenue comparison
            fig_revenue = px.bar(
                filtered_stores,
                x='Store',
                y='Daily Revenue (VND)',
                title='Daily Revenue by Store',
                color='Store',
                text_auto='.2s',
                color_discrete_sequence=px.colors.qualitative.Vivid
            )
            fig_revenue.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig_revenue, use_container_width=True)
        
        with col2:
            # Customer comparison
            fig_customers = px.bar(
                filtered_stores,
                x='Store',
                y='Daily Customers',
                title='Daily Customer Traffic by Store',
                color='Store',
                text_auto=True,
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            fig_customers.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig_customers, use_container_width=True)
        
        st.markdown("---")
        
        # Detailed store metrics
        st.subheader("Store Metrics Dashboard")
        
        # Create a radar chart for store comparison
        if len(selected_stores) > 1:
            fig_radar = go.Figure()
            
            metrics = ['Daily Revenue (VND)', 'Daily Customers', 'Avg Transaction (VND)', 'Staff']
            
            for _, store_row in filtered_stores.iterrows():
                # Normalize values for radar chart
                values = [
                    store_row['Daily Revenue (VND)'] / 1000000,  # Convert to millions
                    store_row['Daily Customers'],
                    store_row['Avg Transaction (VND)'] / 1000,  # Convert to thousands
                    store_row['Staff'] * 10  # Scale up for visibility
                ]
                
                fig_radar.add_trace(go.Scatterpolar(
                    r=values,
                    theta=['Revenue (M VND)', 'Customers', 'Avg Trans (K VND)', 'Staff (x10)'],
                    fill='toself',
                    name=store_row['Store']
                ))
            
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True)),
                showlegend=True,
                title='Multi-dimensional Store Comparison',
                height=500
            )
            st.plotly_chart(fig_radar, use_container_width=True)
        
        # Store performance table
        st.subheader("Store Performance Details")
        
        # Calculate additional metrics
        filtered_stores_display = filtered_stores.copy()
        filtered_stores_display['Revenue per Customer'] = (
            filtered_stores_display['Daily Revenue (VND)'] / 
            filtered_stores_display['Daily Customers']
        )
        filtered_stores_display['Revenue per Staff'] = (
            filtered_stores_display['Daily Revenue (VND)'] / 
            filtered_stores_display['Staff']
        )
        
        st.dataframe(
            filtered_stores_display.style.format({
                'Daily Revenue (VND)': '{:,.0f}',
                'Daily Customers': '{:,.0f}',
                'Avg Transaction (VND)': '{:,.0f}',
                'Revenue per Customer': '{:,.0f}',
                'Revenue per Staff': '{:,.0f}'
            }).background_gradient(subset=['Daily Revenue (VND)'], cmap='Blues'),
            use_container_width=True
        )
    else:
        st.info("Please select at least one store to view comparison.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p>📊 Highlands Coffee Pricing Dashboard | Built with Streamlit</p>
        <p>🔄 Data updates automatically | Interactive visualizations powered by Plotly</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar info
with st.sidebar:
    st.markdown("---")
    st.info("""
        **How to use:**
        - Use filters to explore different product categories
        - Adjust price range to focus on specific segments
        - Navigate tabs to see different analyses
        - Hover over charts for detailed information
        - Select multiple items for comparison
    """)
    
    with st.expander("📖 About"):
        st.write("""
            This dashboard provides comprehensive pricing and sales analysis 
            for Highlands Coffee products. Use it to:
            - Analyze pricing strategies
            - Compare product profitability
            - Track sales trends
            - Benchmark store performance
        """)
