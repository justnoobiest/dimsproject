import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ============================================================
#                KONFIGURASI UMUM APLIKASI
# ============================================================

st.set_page_config(
    page_title="Global Health, Nutrition & Economics Explorer",
    page_icon="🌍",
    layout="wide",
)

@st.cache_data
def load_data():
    df = pd.read_csv("UnifiedDataset.csv")
    # pastikan Year integer
    if "Year" in df.columns:
        df["Year"] = df["Year"].astype(int)
    return df

df = load_data()

# ------------------------------------------------------------
#                  HELPER & KELOMPOK VARIABEL
# ------------------------------------------------------------

def cols_exist(names):
    """Ambil hanya nama kolom yang benar-benar ada di dataset."""
    return [c for c in names if c in df.columns]

all_countries = sorted(df["Country"].unique())
all_years = sorted(df["Year"].unique())
all_genders = df["Gender"].unique().tolist()
global_min_year, global_max_year = all_years[0], all_years[-1]

# ==== Grup indikator utama ====
health_core = cols_exist([
    "Life Expectancy",
    "Infant Mortality Rate",
    "Low CI Value Infant Mortality Rate",
    "High CI Value Infant Mortality Rate",
    "Under 5 Mortality Rate",
    "Low CI Value Under 5 Mortality Rate",
    "High CI Value Under 5 Mortality Rate",
    "% Death Cardiovascular",
    "Suicides Rate",
    "Alcohol Abuse",
    "Unsafe Wash Mortality Rate",
    "Poisoning Mortality Rate",
    "% Injury Deaths",
    "Death Rate",
    "Birth Rate",
])

air_pollution = cols_exist([
    "Air Pollution Death Rate Stroke",
    "Air Pollution Death Rate Stroke Age Standarized",
    "Air Pollution Death Rate Ischaemic Heart Disease",
    "Air Pollution Death Rate Ischaemic Heart Disease Age Standarized",
    "Air Pollution Death Rate Lower Respiratory Infections",
    "Air Pollution Death Rate Lower Respiratory Infections Age Standarized",
    "Air Pollution Death Rate Chronic Obstructive Pulmonary Disease",
    "Air Pollution Death Rate Chronic Obstructive Pulmonary Disease Age Standarized",
    "Air Pollution Death Rate Total",
    "Air Pollution Death Rate Total Age Standarized",
    "Air Pollution Death Rate Trachea Bronchus Lung Cancers",
    "Air Pollution Death Rate Trachea Bronchus Lung Cancers Age Standarized",
])

demography = cols_exist([
    "% Population Aged 0-14",
    "% Population Aged 15-64",
    "% Population Aged 65+",
    "% Population Aged 65-69",
    "% Population Aged 70-74",
    "% Population Aged 75-79",
    "% Population Aged 80+",
    "Total Population",
])

maternal_child = cols_exist([
    "Maternal Mortality Ratio",
    "Low CI Value Maternal Mortality Ratio",
    "High CI Value Maternal Mortality Ratio",
    "% of Births Attended By Skilled Personal",
    "Neonatal Mortality Rate",
    "Low CI Value Neonatal Mortality Rate",
    "High CI Value Neonatal Mortality Rate",
    "Incidence of Malaria",
    "Incidence of Tuberculosis",
    "Low CI Value Incidence of Tuberculosis",
    "High CI Value Incidence of Tuberculosis",
    "Hepatitis B Surface Antigen",
    "Low CI Value Hepatitis B Surface Antigen",
    "High CI Value Hepatitis B Surface Antigen",
    "Adolescent Birth Rate",
    "Reproductive Age Women",
])

health_system = cols_exist([
    "Universal Heath Care Coverage",
    "Doctors",
    "Nurses and Midwifes",
    "Dentists",
    "Pharmacists",
    "Intervention Against NTDs",
    "Road Traffic Deaths",
])

wash = cols_exist([
    "Basic Drinking Water Services",
    "Basic Sanization Services Total",
    "Basic Sanization Services Urban",
    "Basic Sanization Services Rural",
    "Safely Sanitation Total",
    "Safely Sanitation Urban",
    "Safely Sanitation Rural",
    "Basic Hand Washing Total",
    "Basic Hand Washing Urban",
    "Basic Hand Washing Rural",
    "Clean Fuel and Technology",
])

economics = cols_exist([
    "GDP per Capita",
    "Income per Capita",
    "GNI per Capita",
    "Government Expenditure Education",
    "Government Expenditure Military",
    "Government Expenditure Health",
])

poverty = cols_exist([
    "% Population $1.90 a day",
    "% Population $3.20 a day",
    "% Population $5.50 a day",
])

sdg_pop = cols_exist([
    "Population 10 Percentage SDG Total",
    "Population 10 Percentage SDG Urban",
    "Population 10 Percentage SDG Rural",
    "Population 25 Percentage SDG Total",
    "Population 25 Percentage SDG Urban",
    "Population 25 Percentage SDG Rural",
])

conflict = cols_exist([
    "Conflict and Terrorism Deaths",
    "Homicide Rate",
    "Battle Related Deaths",
])

diet_composition = cols_exist([
    "Diet Composition Alcoholic Beverages",
    "Diet Composition Other",
    "Diet Composition Sugar",
    "Diet Composition Oils And Fats",
    "Diet Composition Meat",
    "Diet Composition Dairy And Eggs",
    "Diet Composition Fruit And Vegetables",
    "Diet Composition Starchy Roots",
    "Diet Composition Pulses",
    "Diet Composition Cereals And Grains",
])

diet_fruit = cols_exist([
    "Fruit Consumption Plantains",
    "Fruit Consumption Other",
    "Fruit Consumption Bananas",
    "Fruit Consumption Dates",
    "Fruit Consumption Other Citrus",
    "Fruit Consumption Oranges And Mandarines",
    "Fruit Consumption Apples",
    "Fruit Consumption Lemons And Limes",
    "Fruit Consumption Grapes",
    "Fruit Consumption Grapefruit",
    "Fruit Consumption Pineapples",
])

diet_veg_cereal = cols_exist([
    "Vegetable Consumption",
    "Cereal Consumption Oats",
    "Cereal Consumption Rye",
    "Cereal Consumption Barley",
    "Cereal Consumption Sorghum",
    "Cereal Consumption Maize",
    "Cereal Consumption Wheat",
    "Cereal Consumption Rice",
])

diet_macros = cols_exist([
    "Diet Calories Animal Protein",
    "Diet Calories Plant Protein",
    "Diet Calories Fat",
    "Diet Calories Carbohydrates",
])

numeric_cols = df.select_dtypes(include="number").columns.tolist()

# ---- Tahun khusus untuk subset data (supaya tidak pernah kosong) ----
def years_with_any(cols):
    ys = []
    for y in all_years:
        sub = df[df["Year"] == y]
        if any(sub[c].notna().any() for c in cols if c in sub.columns):
            ys.append(y)
    return ys

years_diet = years_with_any(diet_composition + diet_fruit + diet_veg_cereal)
diet_min_year, diet_max_year = years_diet[0], years_diet[-1]  # 1990–2017

years_wash = years_with_any(wash)
wash_min_year, wash_max_year = years_wash[0], years_wash[-1]  # 2000–2018

# Indikator yang bisa dipetakan di Global Map
map_metrics = cols_exist(
    health_core
    + economics
    + ["Life Expectancy", "Death Rate", "Birth Rate"]
)

# ============================================================
#                       SIDEBAR NAVIGASI
# ============================================================

st.sidebar.title("📊 Navigation")

page = st.sidebar.radio(
    "Pilih halaman:",
    (
        "🏠 Home",
        "🌍 Global Map",
        "📋 Country Profile",
        "📈 Compare Countries",
        "🥦 Nutrition & Diet",
        "🚰 Demography & WASH",
        "💰 Economics & Poverty",
        "📊 Correlation Explorer",
        "📑 Data & Download",
    ),
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Dataset:** Global Health, Nutrition, Mortality & Economic Data")
st.sidebar.markdown("Sumber: Kaggle – Miguel Roca")
st.sidebar.markdown("**Author**  \nMuhammad Dimas Sudirman  \nNIM: 021002404001")

# ============================================================
#                           HOME
# ============================================================

if page == "🏠 Home":
    st.markdown(
        """
        <h1 style="text-align:center;">🌍 Global Health, Nutrition & Economics Explorer</h1>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown("### 👤 Identitas")
        st.markdown(
            """
            **Nama:** Muhammad Dimas Sudirman  
            **NIM:** 021002404001  
            """
        )

    with c2:
        st.markdown("### 🎯 Tujuan Aplikasi")
        st.markdown(
            """
            Aplikasi ini digunakan untuk mengeksplorasi keterkaitan antara:
            - **Kesehatan & mortalitas** (life expectancy, infant mortality, air pollution, NCD)
            - **Sistem kesehatan, WASH & demografi**
            - **Ekonomi, kemiskinan & SDGs**
            - **Pola gizi & konsumsi makanan**  

            Semua komponen dibuat **interaktif** dan otomatis menyesuaikan kombinasi data yang tersedia.
            """
        )

    st.markdown("---")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Jumlah Negara", f"{df['Country'].nunique():,}")
    with c2:
        st.metric("Rentang Tahun", f"{global_min_year} - {global_max_year}")
    with c3:
        st.metric("Total Observasi", f"{len(df):,}")
    with c4:
        latest_year = df["Year"].max()
        mask_latest = (df["Year"] == latest_year) & (df["Gender"] == "Both sexes")
        if "Life Expectancy" in df.columns and mask_latest.any():
            mean_le = df.loc[mask_latest, "Life Expectancy"].mean()
            st.metric(f"Rata-rata Life Expectancy ({latest_year})", f"{mean_le:.1f} tahun")

    st.markdown("### 🔍 Contoh Data")
    st.dataframe(df.head(20))


# ============================================================
#                        GLOBAL MAP
# ============================================================

elif page == "🌍 Global Map":
    st.header("🌍 Global Map")
    st.write("Visualisasi indikator pada peta dunia untuk tahun dan gender tertentu.")

    col1, col2 = st.columns(2)
    with col1:
        year = st.slider("Pilih Tahun", global_min_year, global_max_year, global_max_year)
    with col2:
        gender = st.selectbox("Pilih Gender", options=all_genders)

    base = df[(df["Year"] == year) & (df["Gender"] == gender)]

    # pilih hanya indikator yang punya data di kombinasi ini
    available_metrics = [
        m for m in map_metrics
        if m in base.columns and base[m].notna().any()
    ]

    if not available_metrics:
        st.info("Silakan pilih tahun/gender lain, karena angka untuk kombinasi ini tidak disediakan di dataset.")
    else:
        metric = st.selectbox("Pilih indikator:", options=available_metrics)

        plot_df = base.dropna(subset=[metric])

        fig = px.choropleth(
            plot_df,
            locations="Country",
            locationmode="country names",
            color=metric,
            hover_name="Country",
            color_continuous_scale="Viridis",
            projection="natural earth",
            title=f"{metric} ({gender}, {year})",
        )
        fig.update_layout(margin=dict(l=0, r=0, t=50, b=0))
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("📈 Distribusi indikator (histogram)"):
            fig_hist = px.histogram(
                plot_df,
                x=metric,
                nbins=30,
                marginal="box",
                hover_data=["Country"],
            )
            st.plotly_chart(fig_hist, use_container_width=True)


# ============================================================
#                      COUNTRY PROFILE
# ============================================================

elif page == "📋 Country Profile":
    st.header("📋 Country Profile")
    st.write("Profil lengkap satu negara: tren kesehatan, polusi udara, demografi, ekonomi, dan gizi.")

    col1, col2 = st.columns(2)
    with col1:
        country = st.selectbox(
            "Pilih negara:",
            options=all_countries,
            index=all_countries.index("Indonesia") if "Indonesia" in all_countries else 0,
        )

    # gender yang benar-benar ada untuk negara ini
    available_gender = sorted(df[df["Country"] == country]["Gender"].unique().tolist())
    default_gender = "Both sexes" if "Both sexes" in available_gender else available_gender[0]

    with col2:
        gender = st.selectbox(
            "Pilih Gender:",
            options=available_gender,
            index=available_gender.index(default_gender),
        )

    country_df = df[(df["Country"] == country) & (df["Gender"] == gender)]
    years_c = sorted(country_df["Year"].unique().tolist())
    y_min, y_max = years_c[0], years_c[-1]

    year_range = st.slider(
        "Rentang tahun:",
        y_min,
        y_max,
        (y_min, y_max),
    )

    country_df = country_df[country_df["Year"].between(year_range[0], year_range[1])]

    tab_health, tab_pollution, tab_demo, tab_econ, tab_diet = st.tabs(
        ["🩺 Health", "💨 Air Pollution", "👨‍👩‍👧 Demography & Maternal", "💰 Economics", "🍽 Nutrition"]
    )

    # ---- health ----
    with tab_health:
        st.subheader("Health & Mortality")
        metrics_to_plot = cols_exist(["Life Expectancy", "Infant Mortality Rate", "Under 5 Mortality Rate", "Death Rate"])
        for m in metrics_to_plot:
            fig = px.line(country_df, x="Year", y=m, markers=True, title=m)
            st.plotly_chart(fig, use_container_width=True)

    # ---- pollution ----
    with tab_pollution:
        st.subheader("Air Pollution (age-standardised)")
        metrics_to_plot = cols_exist([
            "Air Pollution Death Rate Total Age Standarized",
            "Air Pollution Death Rate Stroke Age Standarized",
            "Air Pollution Death Rate Ischaemic Heart Disease Age Standarized",
            "Air Pollution Death Rate Lower Respiratory Infections Age Standarized",
            "Air Pollution Death Rate Chronic Obstructive Pulmonary Disease Age Standarized",
            "Air Pollution Death Rate Trachea Bronchus Lung Cancers Age Standarized",
        ])
        if metrics_to_plot:
            long_df = country_df.melt(
                id_vars="Year",
                value_vars=metrics_to_plot,
                var_name="Cause",
                value_name="Rate",
            )
            fig = px.line(long_df, x="Year", y="Rate", color="Cause", markers=True)
            st.plotly_chart(fig, use_container_width=True)

    # ---- demography & maternal ----
    with tab_demo:
        st.subheader("Demography & Maternal / Child Health")

        c1, c2 = st.columns(2)
        with c1:
            if demography:
                demo_df = country_df[["Year"] + demography].set_index("Year")
                long_demo = demo_df.reset_index().melt(
                    id_vars="Year",
                    value_vars=demography,
                    var_name="Age Group",
                    value_name="Percent",
                )
                fig = px.area(long_demo, x="Year", y="Percent", color="Age Group")
                fig.update_layout(title="Struktur usia penduduk (%)")
                st.plotly_chart(fig, use_container_width=True)

        with c2:
            mcols = cols_exist(["Maternal Mortality Ratio", "Neonatal Mortality Rate", "% of Births Attended By Skilled Personal"])
            for m in mcols:
                fig = px.line(country_df, x="Year", y=m, markers=True, title=m)
                st.plotly_chart(fig, use_container_width=True)

    # ---- economics ----
    with tab_econ:
        st.subheader("Economics & Poverty")
        econ_cols = cols_exist(["GDP per Capita", "Income per Capita", "GNI per Capita"])
        pov_cols = poverty

        c1, c2 = st.columns(2)
        with c1:
            for m in econ_cols:
                fig = px.line(country_df, x="Year", y=m, markers=True, title=m)
                st.plotly_chart(fig, use_container_width=True)
        with c2:
            if pov_cols:
                long_pov = country_df.melt(
                    id_vars="Year",
                    value_vars=pov_cols,
                    var_name="Line",
                    value_name="Percent",
                )
                fig = px.line(long_pov, x="Year", y="Percent", color="Line", markers=True)
                fig.update_layout(title="Persentase penduduk di bawah garis kemiskinan")
                st.plotly_chart(fig, use_container_width=True)

    # ---- diet ----
    with tab_diet:
        st.subheader("Diet Composition & Macros")

        # Gabungan semua kolom diet yang mungkin ada
        diet_cols_all = [
            c for c in (diet_composition + diet_macros)
            if c in country_df.columns
        ]

        # Cari tahun terakhir yang PUNYA data diet (tidak semua NaN)
        diet_years = []
        for y in sorted(country_df["Year"].unique()):
            sub_y = country_df[country_df["Year"] == y]
            if sub_y[diet_cols_all].notna().any().any():
                diet_years.append(y)

        if not diet_years:
            st.info("Tidak ada data diet untuk negara & gender ini di dataset.")
        else:
            last_diet_year = diet_years[-1]
            latest = country_df[country_df["Year"] == last_diet_year]

            st.markdown(
                f"Ditampilkan untuk tahun terakhir yang memiliki data diet: "
                f"**{last_diet_year}**"
            )

            c1, c2 = st.columns(2)

            # --- Grafik komposisi diet ---
            with c1:
                comp_cols = [
                    c for c in diet_composition
                    if c in latest.columns and latest[c].notna().any()
                ]
                if comp_cols:
                    long = latest.melt(
                        id_vars=["Country", "Year"],
                        value_vars=comp_cols,
                        var_name="Component",
                        value_name="Share",
                    )
                    fig = px.bar(
                        long,
                        x="Component",
                        y="Share",
                        title="Diet composition (proporsi kalori)",
                    )
                    fig.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Tidak ada data komposisi diet untuk tahun ini.")

            # --- Grafik makro kalori ---
            with c2:
                macro_cols = [
                    c for c in diet_macros
                    if c in latest.columns and latest[c].notna().any()
                ]
                if macro_cols:
                    long = latest.melt(
                        id_vars=["Country", "Year"],
                        value_vars=macro_cols,
                        var_name="Macro",
                        value_name="Calories",
                    )
                    fig = px.bar(
                        long,
                        x="Macro",
                        y="Calories",
                        title="Kalori dari protein, lemak, dan karbohidrat",
                    )
                    fig.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Tidak ada data kalori makro untuk tahun ini.")


# ============================================================
#                      COMPARE COUNTRIES
# ============================================================

elif page == "📈 Compare Countries":
    st.header("📈 Compare Countries")
    st.write("Bandingkan beberapa negara untuk indikator tertentu.")

    default_countries = [c for c in ["Indonesia", "Malaysia", "Thailand"] if c in all_countries]
    if not default_countries:
        default_countries = [all_countries[0]]

    countries = st.multiselect(
        "Pilih negara:",
        options=all_countries,
        default=default_countries,
    )

    if not countries:
        st.info("Pilih minimal satu negara.")
    else:
        gender = st.selectbox("Pilih Gender:", options=all_genders)

        sub = df[(df["Country"].isin(countries)) & (df["Gender"] == gender)]
        years_sub = sorted(sub["Year"].unique().tolist())
        y_min, y_max = years_sub[0], years_sub[-1]

        year_range = st.slider(
            "Rentang tahun:",
            y_min,
            y_max,
            (y_min, y_max),
        )

        sub = sub[sub["Year"].between(year_range[0], year_range[1])]

        candidate_metrics = cols_exist(health_core + economics)
        metric_options = [m for m in candidate_metrics if sub[m].notna().any()]
        metric = st.selectbox("Indikator:", options=metric_options)

        c1, c2 = st.columns(2)
        with c1:
            fig = px.line(
                sub,
                x="Year",
                y=metric,
                color="Country",
                markers=True,
            )
            fig.update_layout(hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            year_bar = st.slider(
                "Tahun untuk bar chart:",
                year_range[0],
                year_range[1],
                year_range[1],
            )
            bar_df = sub[sub["Year"] == year_bar].dropna(subset=[metric])
            fig2 = px.bar(bar_df, x="Country", y=metric, color="Country", title=f"{metric} pada {year_bar}")
            st.plotly_chart(fig2, use_container_width=True)


# ============================================================
#                     NUTRITION & DIET
# ============================================================

elif page == "🥦 Nutrition & Diet":
    st.header("🥦 Nutrition & Diet")
    st.write("Eksplorasi pola konsumsi makanan dan hubungannya dengan kesehatan / ekonomi.")

    col1, col2 = st.columns(2)
    with col1:
        # tahun dibatasi hanya periode yang memang punya data diet
        year = st.slider("Tahun:", diet_min_year, diet_max_year, diet_max_year)
    with col2:
        gender = st.selectbox("Gender:", options=all_genders)

    selected_countries = st.multiselect(
        "Filter negara (opsional):",
        all_countries,
        ["Indonesia"] if "Indonesia" in all_countries else [],
    )

    base = df[(df["Year"] == year) & (df["Gender"] == gender)]
    if selected_countries:
        base = base[base["Country"].isin(selected_countries)]

    # Indikator diet dan health yang benar-benar punya data di filter ini
    diet_candidates = cols_exist(diet_composition + diet_fruit + diet_veg_cereal)
    health_candidates = cols_exist(health_core + economics)

    available_x = [c for c in diet_candidates if base[c].notna().any()]
    available_y = [c for c in health_candidates if base[c].notna().any()]

    if not available_x or not available_y:
        st.info("Untuk kombinasi tahun/gender ini, indikator diet belum tersedia. Coba pilih tahun lain.")
    else:
        x_axis = st.selectbox("X axis (indikator diet):", options=available_x)
        y_axis = st.selectbox("Y axis (indikator health/economic):", options=available_y)

        plot_df = base.dropna(subset=[x_axis, y_axis])

        # buang outlier ekstrim supaya grafik lebih enak dilihat
        for col in [x_axis, y_axis]:
            q1 = plot_df[col].quantile(0.01)
            q99 = plot_df[col].quantile(0.99)
            plot_df = plot_df[(plot_df[col] >= q1) & (plot_df[col] <= q99)]

        fig = px.scatter(
            plot_df,
            x=x_axis,
            y=y_axis,
            size="GDP per Capita" if "GDP per Capita" in plot_df.columns else None,
            color="Country",
            hover_name="Country",
        )
        fig.update_layout(title=f"{y_axis} vs {x_axis} ({gender}, {year})")
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("📋 Tabel ringkas"):
            cols_show = ["Country", x_axis, y_axis] + cols_exist(["GDP per Capita"])
            st.dataframe(plot_df[cols_show].sort_values(y_axis, ascending=False))


# ============================================================
#                    DEMOGRAPHY & WASH
# ============================================================

elif page == "🚰 Demography & WASH":
    st.header("🚰 Demography & WASH")
    st.write("Kondisi demografi, akses air minum, sanitasi, dan energi bersih.")

    col1, col2 = st.columns(2)
    with col1:
        country = st.selectbox(
            "Negara:",
            options=all_countries,
            index=all_countries.index("Indonesia") if "Indonesia" in all_countries else 0,
        )
    with col2:
        gender = st.selectbox("Gender:", options=all_genders)

    base = df[(df["Country"] == country) & (df["Gender"] == gender)]

    # Tahun dibatasi ke periode di mana data WASH ada
    years_country_wash = sorted(
        y for y in years_wash if y in base["Year"].unique()
    )
    y_min, y_max = years_country_wash[0], years_country_wash[-1]

    year_range = st.slider(
        "Rentang tahun:",
        y_min,
        y_max,
        (y_min, y_max),
    )

    base = base[base["Year"].between(year_range[0], year_range[1])]

    t1, t2 = st.tabs(["👨‍👩‍👧 Demografi & SDGs", "🚿 WASH & Clean Fuel"])

    with t1:
        st.subheader("Struktur Penduduk & SDGs")
        if demography:
            demo_df = base[["Year"] + demography].set_index("Year")
            long_demo = demo_df.reset_index().melt(
                id_vars="Year",
                value_vars=demography,
                var_name="Age Group",
                value_name="Percent",
            )
            fig = px.area(long_demo, x="Year", y="Percent", color="Age Group")
            fig.update_layout(title="Struktur penduduk menurut kelompok umur")
            st.plotly_chart(fig, use_container_width=True)

        if sdg_pop:
            long_sdg = base[["Year"] + sdg_pop].melt(
                id_vars="Year",
                value_vars=sdg_pop,
                var_name="Indicator",
                value_name="Percent",
            )
            fig = px.line(long_sdg, x="Year", y="Percent", color="Indicator", markers=True)
            fig.update_layout(title="Indikator SDGs populasi")
            st.plotly_chart(fig, use_container_width=True)

    with t2:
        st.subheader("Akses WASH & Energi Bersih (tahun terakhir)")
        last_year = base["Year"].max()
        latest = base[base["Year"] == last_year]

        st.markdown(f"Ditampilkan untuk tahun terakhir: **{last_year}**")

        if wash:
            long_wash = latest.melt(
                id_vars=["Country", "Year"],
                value_vars=wash,
                var_name="Service",
                value_name="Percent",
            )
            fig = px.bar(long_wash, x="Service", y="Percent", title="Cakupan layanan WASH & clean fuel")
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)


# ============================================================
#                   ECONOMICS & POVERTY
# ============================================================

elif page == "💰 Economics & Poverty":
    st.header("💰 Economics & Poverty")
    st.write("Ikhtisar indikator ekonomi makro, kemiskinan, dan belanja pemerintah.")

    col1, col2 = st.columns(2)
    with col1:
        country = st.selectbox(
            "Negara:",
            options=all_countries,
            index=all_countries.index("Indonesia") if "Indonesia" in all_countries else 0,
        )
    with col2:
        gender = st.selectbox("Gender:", options=all_genders)

    base = df[(df["Country"] == country) & (df["Gender"] == gender)]
    years_ct = sorted(base["Year"].unique().tolist())
    y_min, y_max = years_ct[0], years_ct[-1]

    year_range = st.slider(
        "Rentang tahun:",
        y_min,
        y_max,
        (y_min, y_max),
    )

    base = base[base["Year"].between(year_range[0], year_range[1])]

    c1, c2 = st.columns(2)
    with c1:
        econ_cols = [c for c in economics if base[c].notna().any()]
        for m in econ_cols:
            fig = px.line(base, x="Year", y=m, markers=True, title=m)
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        if poverty:
            long_pov = base.melt(
                id_vars="Year",
                value_vars=[c for c in poverty if base[c].notna().any()],
                var_name="Line",
                value_name="Percent",
            )
            fig = px.line(long_pov, x="Year", y="Percent", color="Line", markers=True)
            fig.update_layout(title="Persentase penduduk di bawah garis kemiskinan")
            st.plotly_chart(fig, use_container_width=True)

        if conflict:
            for m in [c for c in conflict if base[c].notna().any()]:
                fig = px.line(base, x="Year", y=m, markers=True, title=m)
                st.plotly_chart(fig, use_container_width=True)


# ============================================================
#                    CORRELATION EXPLORER
# ============================================================

elif page == "📊 Correlation Explorer":
    st.header("📊 Correlation Explorer")
    st.write("Pilih subset indikator untuk melihat hubungan antar variabel.")

    col1, col2, col3 = st.columns(3)
    with col1:
        year = st.slider("Tahun:", global_min_year, global_max_year, global_max_year)
    with col2:
        gender = st.selectbox("Gender:", options=all_genders)
    with col3:
        country_filter = st.multiselect("Filter negara (opsional):", all_countries, [])

    base = df[(df["Year"] == year) & (df["Gender"] == gender)]
    if country_filter:
        base = base[base["Country"].isin(country_filter)]

    # pilih kolom numerik yang punya cukup data
    candidate = [c for c in numeric_cols if c not in ["Year"]]
    avail_vars = [c for c in candidate if base[c].notna().sum() >= 20]

    default_vars = cols_exist([
        "Life Expectancy",
        "Infant Mortality Rate",
        "Under 5 Mortality Rate",
        "Death Rate",
        "GDP per Capita",
        "Government Expenditure Health",
        "Diet Calories Fat",
        "Diet Calories Carbohydrates",
    ])
    default_vars = [c for c in default_vars if c in avail_vars]

    selected = st.multiselect(
        "Pilih indikator:",
        options=avail_vars,
        default=default_vars,
    )

    if len(selected) >= 2:
        num = base[selected].dropna()
        corr = num.corr()

        st.subheader("Matriks korelasi")
        fig = px.imshow(
            corr,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="RdBu_r",
            zmin=-1,
            zmax=1,
        )
        st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            x_var = st.selectbox("X axis:", selected, index=0, key="corr_x")
        with c2:
            y_var = st.selectbox("Y axis:", selected, index=1 if len(selected) > 1 else 0, key="corr_y")

        fig_scatter = px.scatter(
            base.dropna(subset=[x_var, y_var]),
            x=x_var,
            y=y_var,
            color="Country",
            hover_name="Country",
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.info("Pilih minimal dua indikator untuk melihat korelasi.")


# ============================================================
#                     DATA & DOWNLOAD
# ============================================================

elif page == "📑 Data & Download":
    st.header("📑 Data & Download")
    st.write("Filter dan unduh subset data untuk analisis lanjutan di Jupyter / Excel / Stata, dll.")

    col1, col2, col3 = st.columns(3)
    with col1:
        year_range = st.slider(
            "Rentang tahun:",
            global_min_year,
            global_max_year,
            (global_min_year, global_max_year),
        )
    with col2:
        gender_opt = ["All"] + all_genders
        gender_sel = st.selectbox("Gender:", gender_opt)
    with col3:
        countries = st.multiselect("Negara:", all_countries, [])

    filtered = df[df["Year"].between(year_range[0], year_range[1])]
    if gender_sel != "All":
        filtered = filtered[filtered["Gender"] == gender_sel]
    if countries:
        filtered = filtered[filtered["Country"].isin(countries)]

    default_cols = cols_exist([
        "Country",
        "Year",
        "Gender",
        "Life Expectancy",
        "Infant Mortality Rate",
        "Under 5 Mortality Rate",
        "Maternal Mortality Ratio",
        "GDP per Capita",
        "Total Population",
    ])

    selected_cols = st.multiselect(
        "Pilih kolom yang ditampilkan:",
        options=list(df.columns),
        default=default_cols,
    )

    if selected_cols:
        filtered = filtered[selected_cols]

    st.markdown("### Hasil filter")
    st.dataframe(filtered)

    csv_data = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        "💾 Download CSV",
        data=csv_data,
        file_name="global_health_filtered.csv",
        mime="text/csv",
    )
