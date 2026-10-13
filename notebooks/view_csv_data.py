import marimo

__generated_with = "0.25.1"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import pandas as pd

    return mo, pd


@app.cell
def _(mo, pd):
    df_base = pd.read_csv("data/incidents_students.csv")
    mo.md(
        f"## CSV viewer - {len(df_base)} rows of base incident reports, with {len(df_base[['asset_type']].dropna())} full lines"
    )
    return (df_base,)


@app.cell
def _(df_base, mo):
    mo.ui.table(df_base, selection=None)
    return


@app.cell
def _(mo, pd):
    df_scanned = pd.read_csv("data/incidents_students_scanned.csv")
    mo.md(
        f"## CSV viewer — {len(df_scanned)} rows of preprocessed scanned pdf incident reports"
    )
    return (df_scanned,)


@app.cell
def _(df_scanned, mo):
    mo.ui.table(df_scanned, selection=None)
    return


@app.cell
def _(mo, pd):
    df_digital = pd.read_csv("data/incidents_students_digital.csv")
    mo.md(
        f"## CSV viewer - {len(df_digital)} rows of preprocessed digital pdf incident reports"
    )
    return (df_digital,)


@app.cell
def _(df_digital, mo):
    mo.ui.table(df_digital, selection=None)
    return


@app.cell
def _(mo, pd):
    df_merged = pd.read_csv("data/incidents_students_merged.csv")
    mo.md(f"## CSV viewer - {len(df_merged)} rows in total")
    return (df_merged,)


@app.cell
def _(df_merged, mo):
    mo.ui.table(df_merged, selection=None)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Visualising costs versus equipment_id
    """)
    return


@app.cell
def _(df_merged, mo, pd):
    import plotly.express as px

    # Group by site and sum the estimated costs (needed to find top site)
    cost_by_site = (
        df_merged.groupby("site")["estimated_cost_eur"].sum().reset_index()
    )
    cost_by_site = cost_by_site.sort_values(
        "estimated_cost_eur", ascending=False
    )

    # Group by site and equipment to get total cost per asset/equipment
    cost_by_site_equipment = (
        df_merged.groupby(["site", "equipment_id"])["estimated_cost_eur"]
        .sum()
        .reset_index()
    )
    cost_by_site_equipment = cost_by_site_equipment.dropna(
        subset=["equipment_id"]
    )

    # Create box plot showing distribution of total cost per equipment, grouped by site
    fig_equipment = px.box(
        cost_by_site_equipment,
        x="site",
        y="estimated_cost_eur",
        title="Distribution of Total Cost per Equipment by Site",
        labels={
            "site": "Site",
            "estimated_cost_eur": "Total Estimated Cost per Equipment (EUR)",
        },
        points="all",
        color="site",
    )

    fig_equipment.update_layout(showlegend=False)
    fig_equipment.update_yaxes(showgrid=True, zeroline=False)

    # Pick the site with the highest total cost
    selected_site = cost_by_site.iloc[0]["site"]

    # Filter df_base for the selected site and ensure date is datetime
    df_site = df_merged[df_merged["site"] == selected_site].copy()
    df_site["date"] = pd.to_datetime(df_site["date"])

    # Get top 3 equipment IDs by total cost within this site
    cost_by_equipment_site = (
        df_site.groupby("equipment_id")["estimated_cost_eur"]
        .sum()
        .reset_index()
    )
    cost_by_equipment_site = cost_by_equipment_site.sort_values(
        "estimated_cost_eur", ascending=False
    )
    top_3_equipment = cost_by_equipment_site.head(3)["equipment_id"].tolist()

    # Create a full date range for the selected site
    min_date = df_site["date"].min()
    max_date = df_site["date"].max()
    full_date_range = pd.date_range(start=min_date, end=max_date, freq="D")

    # Prepare data for plotting: for each equipment, create daily series with 0 for missing dates
    df_plot = pd.DataFrame()

    for equip_id in top_3_equipment:
        # Filter for this equipment
        df_equip = df_site[df_site["equipment_id"] == equip_id].copy()

        # Group by date and sum costs (in case multiple incidents per day)
        df_equip_daily = (
            df_equip.groupby("date")["estimated_cost_eur"].sum().reset_index()
        )

        # Reindex to full date range, filling missing dates with 0
        df_equip_daily = (
            df_equip_daily.set_index("date")
            .reindex(full_date_range, fill_value=0)
            .reset_index()
        )
        df_equip_daily = df_equip_daily.rename(columns={"index": "date"})

        df_equip_daily["equipment_id"] = str(equip_id)
        df_plot = pd.concat([df_plot, df_equip_daily], ignore_index=True)

    # Scatter plot (markers only, no lines) to avoid interpolation between points
    # Dates with no events show value 0
    fig_time = px.line(
        df_plot,
        x="date",
        y="estimated_cost_eur",
        color="equipment_id",
        title=f"Estimated Cost Over Time - Top 3 Equipment at Site: {selected_site}",
        labels={
            "date": "Date",
            "estimated_cost_eur": "Estimated Cost (EUR)",
            "equipment_id": "Equipment ID",
        },
    )

    # Ensure we show markers only (no connecting lines) to avoid interpolation
    fig_time.update_traces(mode="lines", marker=dict(size=8))

    mo.vstack([fig_equipment, fig_time])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
