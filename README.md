# 📦 InvenAI — Smart Inventory Management System

> An AI-powered inventory management dashboard built for coffee shops, juice bars, and small food & beverage businesses — designed to predict stockouts before they happen, not just report them after.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 🧐 What Problem Does This Solve?

Most small cafes and shops in Pakistan track inventory the same way they did 30 years ago — a notebook, a memory, and a lot of guesswork. This leads to two expensive mistakes that happen in almost every shop, every single week:

1. **Running out of a popular item** at the worst possible time (a busy weekend, a hot day) and losing sales.
2. **Over-ordering perishable stock** that expires before it's sold, turning money into waste.

InvenAI exists to fix both problems with one dashboard. It doesn't just show you *what* you have — it tells you *what's about to run out*, *how much to reorder*, and *who to order it from*, before you even have to ask.

---

## ✨ What It Actually Does

InvenAI is organized into five focused pages, each solving one part of the inventory puzzle.

### 1. 🏠 Main Dashboard
The first thing you see when you open the app — a real-time snapshot of your entire business:
- **Total inventory value** in Pakistani Rupees
- **Critical and low-stock counts**, so problems are visible the second you log in
- **Total revenue** tracked across your sales history
- A **color-coded stock chart** (red = critical, orange = low, green = healthy)
- A **pie chart** showing where your money is tied up across categories (Coffee, Juice, Bakery, Supplies)

### 2. 📋 Inventory Management
A full, searchable table of every item you stock — quantity, minimum/maximum thresholds, unit price, and live status. You can filter by category or status, search for a specific item, and export the filtered results as a CSV whenever you need a report for an accountant or a supplier meeting.

### 3. 🔄 Smart Reorder System
This is where the "AI" in InvenAI earns its name. Instead of you manually checking what's low, the system:
- Calculates exactly **how much of each item to reorder** (based on the gap between current stock and your maximum stock level)
- **Groups everything by supplier**, so you know exactly who to call and what to ask for
- Estimates the **total cost of reordering**, so there are no budget surprises

### 4. 🤝 Supplier Management
A directory of every supplier you work with — contact details, location, lead time (how many days delivery takes), and a reliability rating. It even drafts a sample WhatsApp message you could send to request a delivery, so communication is one less thing to think about.

### 5. 📊 Sales & Analytics
The "why" behind your numbers — daily revenue trends, your top-selling items, revenue broken down by category, and profit margins per item. This is the page that answers questions like *"Is our coffee or our juice actually making more money?"*

---

## 🧠 The "AI" Behind InvenAI

The reorder predictions are designed to be powered by a **Random Forest** model — a machine learning approach that looks at historical sales patterns (day of the week, season, recent sales velocity) rather than a single fixed rule like "reorder when stock hits 10." In plain terms: instead of one simple guess, the model effectively asks the question from a hundred different angles and goes with the majority answer, which makes it far more resistant to one-off mistakes than a basic if/else rule would be.

This matters for a real business because demand isn't constant — a juice shop sells far more mango juice in June than in December, and a model that accounts for that pattern will always outperform a static minimum-stock rule.

---

## 🛠️ Built With

| Technology | Purpose |
|---|---|
| **Python 3.12** | Core language |
| **Streamlit** | Interactive web dashboard, no HTML/CSS required |
| **Pandas** | Data handling and analysis |
| **Plotly** | Interactive charts (bar, pie, line) |
| **scikit-learn** | Random Forest model for reorder prediction |

---

## 📁 Project Structure

```
inventory-management-ai/
│
├── app.py                  # Main Streamlit application (all 5 pages)
├── generate_data.py        # Generates realistic sample data
├── requirements.txt        # Python dependencies
│
└── data/
    ├── inventory.csv        # Items, stock levels, pricing
    ├── suppliers.csv        # Supplier contacts and reliability
    └── sales_history.csv    # Historical sales records
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/Talha102/inventory-management-ai.git
cd inventory-management-ai

# Install dependencies
pip install -r requirements.txt

# Generate sample data
python generate_data.py

# Launch the dashboard
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`.

---

## 📊 Sample Data

The included dataset simulates a real Pakistani coffee & juice shop:

- **15 inventory items** across Coffee, Juice, Bakery, Tea, and Supplies
- **5 local suppliers** (Lahore, Karachi, Islamabad, Faisalabad) with realistic lead times and reliability scores
- **180+ days of sales history** with seasonal patterns built in (e.g., mango and watermelon sales spike in summer)

This means you can explore the entire dashboard immediately — no setup of real data required to see how it works.

---

## 🔮 Roadmap — What's Next

- [ ] Connect to a live POS system instead of static CSVs
- [ ] WhatsApp Business API integration for real (not simulated) supplier alerts
- [ ] Multi-branch support for businesses with more than one location
- [ ] Expiry-date tracking and waste reduction alerts
- [ ] Mobile-responsive layout for on-the-go stock checks

---

## 👤 About the Builder

Built by **Talha Akram** — combining hands-on cafe operations experience (including international experience at Ole & Steen, London) with a growing data science and AI skillset, to build tools that solve problems real small businesses actually face — not just textbook problems.

---

## 📝 License

This project is open for learning and adaptation. Built as part of an ongoing journey into AI-powered business tools for Pakistani small businesses.

---

*Made with ☕, 🧃, and a lot of `streamlit run app.py`*
