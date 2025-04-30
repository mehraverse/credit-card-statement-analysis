import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def plot_stacked_bar(csv_path="./data/processed/all_transactions.csv", output_path="./outputs/figures/stacked_bar.png"):
    df = pd.read_csv(csv_path)
    # Ensure Amount is numeric
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    # Convert Month to datetime for formatting
    df["Month_dt"] = pd.to_datetime(df["Month"].astype(str), format="%Y%m")
    # Group by Month and Category, sum Amount
    pivot = df.pivot_table(index="Month_dt", columns="Category", values="Amount", aggfunc="sum", fill_value=0)
    # Sort by Month
    pivot = pivot.sort_index()
    # Custom category order
    category_order = [
        "Utilities/Bills",
        "Groceries",
        "Uber Eats",
        "Dining/Restaurants",
        "Travel (Suica/ETC/Fuel)",
        "Hotels/Airbnb/Flights",
        "Car Rental",
        "Recreational (Snowboarding, Museums, Bars,etc.)",
        "Shopping (Clothing/Electronics)",
        "Others (7-11, Misc.)"
    ]
    # Only keep columns that exist in the data, in the specified order
    cols = [c for c in category_order if c in pivot.columns] + [c for c in pivot.columns if c not in category_order]
    pivot = pivot[cols]
    # Plot
    plt.figure(figsize=(14, 8))
    ax = plt.gca()
    pivot.plot(kind="bar", stacked=True, ax=ax)
    plt.title("Monthly Spending on Credit Card Living in Tokyo")
    plt.xlabel("Month")
    plt.ylabel("Amount (Yen)")
    # Format x-axis as 'Mon YY'
    ax.set_xticklabels([d.strftime("%b %y") for d in pivot.index], rotation=45, ha='right')
    # Set y-axis ticks to 50K increments and format as '50K'
    ax.yaxis.set_major_locator(ticker.MultipleLocator(50000))
    ax.yaxis.set_major_formatter(lambda x, pos: f"{int(x/1000):,}K" if x != 0 else "0")
    plt.legend(loc="upper left", bbox_to_anchor=(1,1))

    # --- Analysis Section ---
    # 1. Percentage of Mercari and Rakuten usage
    total = df["Amount"].sum()
    mercari = df[df["Company"].str.lower() == "mercari"]["Amount"].sum()
    rakuten = df[df["Company"].str.lower() == "rakuten"]["Amount"].sum()
    mercari_pct = mercari / total * 100 if total else 0
    rakuten_pct = rakuten / total * 100 if total else 0

    # 2. Average dining out expense (monthly)
    dining = df[df["Category"] == "Dining/Restaurants"].groupby("Month")["Amount"].sum()
    avg_dining = dining.mean() if not dining.empty else 0

    # 3. Average Uber Eats expense (monthly)
    uber = df[df["Category"] == "Uber Eats"].groupby("Month")["Amount"].sum()
    avg_uber = uber.mean() if not uber.empty else 0

    # 4. Average Travel expense (monthly)
    travel_category = "Travel (Suica/ETC/Fuel)"
    travel = df[df["Category"] == travel_category].groupby("Month")["Amount"].sum()
    avg_travel = travel.mean() if not travel.empty else 0

    # Compose analysis text
    analysis = (
        f"Mercari Usage: {mercari_pct:.1f}%\n"
        f"Rakuten Usage: {rakuten_pct:.1f}%\n"
        f"Avg Dining Out (monthly): ¥{avg_dining:,.0f}\n"
        f"Avg Uber Eats (monthly): ¥{avg_uber:,.0f}\n"
        f"Avg Travel (monthly): ¥{avg_travel:,.0f}"
    )

    # --- Events ---
    # Map: month string -> annotation
    events = {
        "202403": "Parents in Tokyo (Car Rental ↑)",
        "202404": "Parents in Tokyo (Car Rental ↑)",
        "202408": "Bali Trip (Hotels ↑)",
        "202410": "India Trip (Shopping ↑)",
        "202503": "Snowboarding Trips (Recreational ↑)",
        "202504": "Okinawa Trip (Hotels ↑)",
    }
    # Format events for text display
    event_lines = ["\n--- Notable Events ---"]
    for month_str, label in events.items():
        try:
            # Format month for display
            dt = pd.to_datetime(month_str, format="%Y%m")
            month_display = dt.strftime("%b %Y")
            event_lines.append(f"{month_display}: {label}")
        except Exception:
            continue # Skip if month format is invalid

    # Combine analysis and event text
    analysis_and_events = analysis + "\n" + "\n".join(event_lines)

    # Place analysis and events text at bottom right
    ax.text(
        1.02, 0.33, analysis_and_events, # Use combined text
        fontsize=10, # Slightly smaller font to fit more text
        va='top', # Align text block from the top
        ha='left', family='monospace',
        transform=ax.transAxes, wrap=True
    )

    # This line controls the layout, including the bottom margin
    plt.tight_layout(rect=[0, -0.38, 1, 1]) # Adjust right boundary for text
    # The second value (0.04) sets the bottom margin in normalized figure coordinates (0=bottom, 1=top).
    # Increasing this value increases the space below the x-axis labels.
    # Decreasing it reduces the space.

    plt.savefig(output_path)
    plt.close()

if __name__ == "__main__":
    plot_stacked_bar()