# ☕ Highlands Coffee Pricing Dashboard

An interactive Streamlit dashboard for analyzing Highlands Coffee pricing strategies, product profitability, sales trends, and store performance.

## Features

### 📊 Overview Tab
- Key business metrics (total products, average price, average margin, profit potential)
- Interactive product catalog with sorting and filtering
- Color-coded margin visualization

### 💰 Pricing Analysis Tab
- Price distribution by category (box plots)
- Average profit margin comparison
- Interactive price vs profit scatter plot
- Pricing insights and recommendations
- High/low margin product identification

### 📈 Sales Trends Tab
- Daily sales volume trends for selected products
- Sales summary statistics (total, average, peak)
- Category performance pie chart
- Multi-product comparison

### 🏪 Store Comparison Tab
- Revenue and customer traffic comparison
- Multi-dimensional radar chart for store metrics
- Detailed performance metrics table
- Revenue per customer and per staff calculations

## Interactive Features

- **Category Filters**: Select specific product categories to analyze
- **Price Range Slider**: Focus on specific price segments
- **Dynamic Sorting**: Sort products by any metric
- **Multi-select Options**: Compare multiple products or stores
- **Hover Details**: See detailed information on charts
- **Real-time Updates**: All visualizations update based on your selections

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone this repository:
```bash
git clone https://github.com/thunguyen311/Highlands-Pricing.git
cd Highlands-Pricing
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Dashboard

Start the Streamlit application:
```bash
streamlit run app.py
```

The dashboard will open automatically in your default web browser at `http://localhost:8501`

### Using the Dashboard

1. **Sidebar Filters**:
   - Select categories you want to analyze
   - Adjust the price range slider to focus on specific segments

2. **Navigation**:
   - Use the tabs at the top to switch between different analyses
   - Overview: See general metrics and product catalog
   - Pricing Analysis: Analyze pricing strategies and margins
   - Sales Trends: Track sales over time
   - Store Comparison: Compare store performance

3. **Interactions**:
   - Click and drag on charts to zoom
   - Hover over data points for details
   - Use multi-select dropdowns to compare items
   - Sort tables by clicking column headers

## Data

The dashboard currently uses sample data that includes:
- 15 Highlands Coffee products across 5 categories (Coffee, Freeze, Tea, Food, Dessert)
- 30 days of sales data
- 5 store locations with performance metrics

### Customizing Data

To use your own data, modify the functions in `data.py`:
- `get_product_data()`: Update product information, prices, and costs
- `get_sales_data()`: Modify sales history
- `get_store_comparison_data()`: Change store metrics

## Project Structure

```
Highlands-Pricing/
│
├── app.py              # Main Streamlit application
├── data.py             # Data generation and management
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## Technologies Used

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations
- **NumPy**: Numerical computing

## Screenshots

The dashboard features:
- Clean, professional design with coffee-themed colors
- Responsive layout that adapts to screen size
- Interactive charts and graphs
- Real-time filtering and updates

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is open source and available under the MIT License.

## Contact

For questions or suggestions, please open an issue on GitHub.

---

**Built with ❤️ and ☕ using Streamlit**