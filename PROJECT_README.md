# AI Native Journey - Three Component Project

This project contains three main components as requested:

1. **Email Validation Function** (`email_validator.py`)
2. **Data Analysis and Visualization** (`data_analysis.py`)
3. **Web Form with Validation** (`web_form.html`)

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Modern web browser (for the web form)

### Installation
1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## 📧 Component 1: Email Validation Function

**File:** `email_validator.py`

A comprehensive email validation function that performs multiple validation checks:

### Features:
- ✅ Format validation using regex
- ✅ Domain format validation
- ✅ Length validation (RFC 5321 compliant)
- ✅ Special character validation
- ✅ Optional DNS lookup validation
- ✅ Detailed error reporting

### Usage:
```python
from email_validator import validate_email

# Basic validation
is_valid, details = validate_email("user@example.com")
print(f"Valid: {is_valid}")
print(f"Details: {details}")

# Advanced DNS validation
from email_validator import validate_email_dns
dns_valid = validate_email_dns("user@example.com")
```

### Example Output:
```
Email Validation Results:
==================================================
user@example.com                              ✓ VALID

invalid-email                                 ✗ INVALID
  └─ Invalid email format

user@domain                                   ✗ INVALID
  └─ Invalid domain format
```

## 📊 Component 2: Data Analysis and Visualization

**File:** `data_analysis.py`

A comprehensive data analysis and visualization system with sample dataset generation.

### Features:
- 📈 **Sample Dataset Generation**: Creates realistic sales data
- 📊 **Statistical Analysis**: Mean, median, std, correlations
- 🎨 **Multiple Visualizations**: 9 different chart types
- 📋 **Automated Report Generation**: Comprehensive analysis report
- 💾 **Plot Saving**: Automatically saves visualizations

### Visualizations Included:
1. Sales Amount Distribution (Histogram)
2. Sales by Product Category (Pie Chart)
3. Daily Sales Trend (Line Chart)
4. Correlation Heatmap
5. Sales by Category (Box Plot)
6. Customer Age Distribution (Histogram)
7. Satisfaction vs Sales (Scatter Plot)
8. Regional Sales (Bar Chart)
9. Quantity vs Sales (Scatter Plot)

### Usage:
```python
from data_analysis import DataAnalyzer

# Create analyzer and generate sample data
analyzer = DataAnalyzer()
data = analyzer.create_sample_data()

# Generate comprehensive report
report = analyzer.generate_report()
print(report)

# Create visualizations
analyzer.create_visualizations(save_plots=True)
```

### Sample Report Output:
```
============================================================
DATA ANALYSIS REPORT
============================================================
Dataset Shape: (1000, 7)
Total Records: 1000
Total Columns: 7

DATA TYPES:
--------------------
date: datetime64[ns]
product_category: object
sales_amount: float64
quantity_sold: int64
customer_age: float64
customer_satisfaction: float64
region: object

BASIC STATISTICS:
--------------------
SALES_AMOUNT:
  mean: 149.85
  median: 149.12
  std: 49.98
  min: 0.00
  max: 299.99
  count: 1000
  missing: 0
```

## 🌐 Component 3: Web Form with Validation

**File:** `web_form.html`

A modern, responsive web form with comprehensive client-side validation.

### Features:
- 🎨 **Modern UI Design**: Gradient background, smooth animations
- ✅ **Real-time Validation**: Instant feedback as users type
- 🔒 **Password Strength Indicator**: Visual password strength meter
- 📱 **Responsive Design**: Works on all device sizes
- 🎯 **Comprehensive Validation**: Email, phone, ZIP code, names, etc.
- ✨ **Success Animation**: Beautiful success state with auto-reset

### Validation Rules:
- **Names**: Letters and spaces only (2-50 characters)
- **Email**: Standard email format validation
- **Phone**: International phone number format
- **Password**: Minimum 8 characters, uppercase, lowercase, number
- **ZIP Code**: US ZIP code format (12345 or 12345-6789)
- **Date of Birth**: Must be 13+ years old, not in future
- **Required Fields**: Marked with asterisk (*)

### Usage:
1. Open `web_form.html` in any modern web browser
2. Fill out the form fields
3. Watch real-time validation feedback
4. Submit to see success animation

### Form Fields:
- First Name & Last Name
- Email Address
- Phone Number
- Password & Confirm Password
- Date of Birth
- Gender Selection
- Address Information
- Interests (Multiple selection)
- Newsletter subscription
- Terms agreement

## 🛠️ Running the Components

### Email Validator:
```bash
python email_validator.py
```

### Data Analysis:
```bash
python data_analysis.py
```

### Web Form:
```bash
# Simply open the HTML file in your browser
# Or use Python's built-in server:
python -m http.server 8000
# Then visit: http://localhost:8000/web_form.html
```

## 📁 Project Structure
```
AI_Native_Journey/
├── email_validator.py      # Email validation component
├── data_analysis.py        # Data analysis & visualization
├── web_form.html          # Web form with validation
├── requirements.txt       # Python dependencies
├── PROJECT_README.md      # This file
└── data_analysis_plots.png # Generated plots (after running analysis)
```

## 🔧 Dependencies

### Python Packages:
- `pandas`: Data manipulation and analysis
- `matplotlib`: Plotting and visualization
- `seaborn`: Statistical data visualization
- `numpy`: Numerical computing
- `dnspython`: DNS toolkit (for email validation)

### Browser Requirements:
- Modern web browser with ES6+ support
- No additional dependencies required

## 🎯 Key Features Summary

| Component | Key Features | Output |
|-----------|-------------|---------|
| Email Validator | Multi-level validation, DNS lookup, detailed errors | Validation results with error details |
| Data Analysis | 9 chart types, statistical analysis, automated reports | PNG plots + text report |
| Web Form | Real-time validation, password strength, responsive design | Interactive web form |

## 🚀 Next Steps

1. **Customize the email validation** for your specific needs
2. **Replace sample data** with your actual dataset in the analysis component
3. **Modify form fields** and validation rules in the web form
4. **Add server-side validation** to the web form
5. **Integrate components** into a larger application

## 📝 Notes

- The email validator includes optional DNS lookup (requires internet connection)
- The data analysis generates a sample dataset automatically
- The web form is purely client-side (no backend required)
- All components are self-contained and can be used independently

---

**Created for AI Native Journey Project** 🚀 