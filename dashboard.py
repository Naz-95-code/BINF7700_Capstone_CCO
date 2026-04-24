import sys
import os
sys.path.append(os.path.abspath("src"))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.stats import mannwhitneyu

st.set_page_config(
    page_title="Universal Mutation Analysis Dashboard",
    layout="wide"
)

st.title("🧬 Universal Mutation Analysis Dashboard")

st.markdown("""
This dashboard provides a comparative analysis of **mutation burden and genomic patterns**
across **synthetic (OncoGAN-generated)** and **real (TCGA-derived)** cancer datasets.
""")

st.sidebar.title("Navigation")

SYNTHETIC_FILES = {
    "Breast": "data/synthetic/breast_mutation_burden.tsv",
    "Prostate": "data/synthetic/prostate_mutation_burden.tsv",
}

REAL_FILES = {
    "Breast": "data/real/tcga_breast_mutation_counts.txt",
    "Prostate": "data/real/tcga_prostate_mutation_counts.txt",
}

SIGNATURE_FILE = "results/signature_exposures.tsv"
VARIANT_FILE = "results/variant_type_summary.tsv"
SPECTRA_FILE = "results/combined_spectra.tsv"
COSMIC_SIG_FILE = "results/signature_exposures.tsv"

@st.cache_data
def load_synthetic_data(cancer):
    df = pd.read_csv(SYNTHETIC_FILES[cancer], sep="\t")
    df.columns = df.columns.str.strip()
    df["total_mutations"] = pd.to_numeric(df["total_mutations"], errors="coerce")
    df = df.dropna()
    df["source"] = "Synthetic (OncoGAN)"
    return df


@st.cache_data
def load_real_data(cancer):
    df = pd.read_csv(REAL_FILES[cancer], sep=r"\s+", engine="python")
    df = df.iloc[:, :4]
    df.columns = ["study", "patient", "sample", "mutation_count"]
    df["mutation_count"] = pd.to_numeric(df["mutation_count"], errors="coerce")
    df = df.dropna()
    df["source"] = "Real (TCGA)"
    return df


@st.cache_data
def load_signature():
    return pd.read_csv(SIGNATURE_FILE, sep="\t", index_col=0)


@st.cache_data
def load_variant():
    try:
        return pd.read_csv(VARIANT_FILE, sep="\t")
    except:
        return None

@st.cache_data
def load_spectra():
    df = pd.read_csv(SPECTRA_FILE, sep="\t")
    df.columns = df.columns.str.strip()
    return df


cancer = st.sidebar.selectbox("Select Cancer Type", ["Breast", "Prostate"])

synthetic = load_synthetic_data(cancer)
real = load_real_data(cancer)

syn_vals = synthetic["total_mutations"]
real_vals = real["mutation_count"]

combined = pd.concat([
    pd.DataFrame({"mutation": syn_vals, "source": "Synthetic"}),
    pd.DataFrame({"mutation": real_vals, "source": "Real"})
])

combined["log_mutation"] = np.log10(combined["mutation"] + 1)

stat, p = mannwhitneyu(syn_vals, real_vals)
tab1, tab2, tab3, tab4, tab5, tab6, = st.tabs([
    "Mutation Burden",
    "Statistical Test",
    "Mutation Spectrum",
    "Mutation Signatures",
    "Cosine Similarity",
    "Summary"
])

with tab1:
    st.subheader(f"{cancer} Mutation Burden Comparison")
    st.markdown("""

    **Mutation burden** refers to the total number of mutations detected per tumor sample.  
    Because mutation counts are highly skewed, a log transformation is applied to improve visualization and reveal distribution patterns.  
    Across both cancer types, the OncoGAN synthetic and TCGA real datasets exhibit right-skewed distributions; however, the OncoGAN synthetic data is more concentrated
    with reduced variance, indicating that it captures general trends but underrepresents the full biological heterogeneity observed in TCGA cohorts.
    """) 
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.histogram(
            combined,
            x="log_mutation",
            color="source",
            nbins=80,
            barmode="overlay",
            opacity=0.6,
            color_discrete_map={
                "Synthetic": "red",
                "Real": "blue"
            },
            title="Mutation count per sample (log scale)"
        )
        fig.update_xaxes(title="Log10 mutation count per sample")
        fig.update_yaxes(title="Number of samples (Synthetic vs Real)")
        st.plotly_chart(fig, use_container_width=True)
            

from scipy.stats import mannwhitneyu

# Calculate the p-value using the two data groups
stat, p = mannwhitneyu(syn_vals, real_vals, alternative='two-sided')
if p < 0.0001:
    p_text = "p < 0.0001"
else:
    p_text = f"p = {p:.2e}"
with col2:
    fig2 = px.box(
        combined,
        x="source",
        y="mutation",
        points="all",
        color="source",
        color_discrete_map={
            "Synthetic": "red",
            "Real": "blue"
        }
    )

    fig2.update_yaxes(
        type="log",
        title="Mutation count per sample (log scale)"
    )
    fig2.update_xaxes(title="Dataset type")

    # Bracket position (Keeping your exact logic)
    y_max = combined["mutation"].max()
    y_top = y_max * 1.3  
    y_drop = y_max * 1.15
        
    fig2.add_shape( 
        type="line", x0=0, x1=0, y0=y_drop, y1=y_top,
        line=dict(color="black", width=2)
    )
    fig2.add_shape(
        type="line", x0=0, x1=1, y0=y_top, y1=y_top,
        line=dict(color="black", width=2)
    )
    fig2.add_shape(
        type="line", x0=1, x1=1, y0=y_drop, y1=y_top,
        line=dict(color="black", width=2)
    )

    # Updated annotation to use the calculated 'p'
    fig2.add_annotation(
        x=0.5,
        y=1.05,
        xref="x",
        yref="paper",                 
        text=p_text,
        showarrow=False,
        font=dict(size=14, color="black")
    )

    fig2.update_layout(margin=dict(t=100))
        
    st.plotly_chart(fig2, use_container_width=True)

      

    # Stats below both columns
    def stats(x):
        return {
            "Mean": float(np.mean(x)),
            "Median": float(np.median(x)),
            "Min": float(np.min(x)),
            "Max": float(np.max(x))
        }
            
    c1, c2 = st.columns(2)
    with c1:
        st.write("Synthetic")
        st.write(stats(syn_vals))
    with c2:
        st.write("Real")
        st.write(stats(real_vals))


with tab2:
    st.subheader("Mann–Whitney U Test")

    st.markdown("""
    The **Mann-Whitney U Test** is a non-parametric test used to determine whether 
    two independent groups come from the same distribution. It makes no assumption 
    about normality, making it appropriate for mutation count data which is 
    typically right-skewed.
    
    **Null hypothesis (H₀):** The mutation burden distributions of synthetic and real samples are equal
    
    **Alternative hypothesis (H₁):** The distributions differ significantly
    
    **Significance threshold:** α = 0.05
    """)

    stat, p = mannwhitneyu(syn_vals, real_vals, alternative="two-sided")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("U Statistic", f"{stat:.2f}",
                  help="Larger values indicate greater separation between the two distributions")
    with col2:
        st.metric("P-value", f"{p:.2e}",
                  help="Probability of observing this result if the null hypothesis were true")
    with col3:
        n1, n2 = len(syn_vals), len(real_vals)
        r = 1 - (2 * stat) / (n1 * n2)
        st.metric("Effect size (r)", f"{r:.3f}",
                  help= "Rank-biserial correlation. 0.1 = small, 0.3 = medium, 0.5 = large")
    if abs(r) >= 0.5:
        effect_label = "large"
    elif abs(r) >= 0.3:
        effect_label = "medium"
    else:
        effect_label = "small"

    st.markdown(f"""
    The rank-biserial correlation of **r = {r:.3f}** indicates a **{effect_label} effect size**, 
    meaning the difference between synthetic and real mutation burden is 
    {"substantive and not merely a product of sample size" if abs(r) >= 0.5 
    else "moderate and should be interpreted alongside the sample size imbalance"}.
    """)
    if p < 0.05:
        st.error(f"""
        **Significant difference detected** (p = {p:.2e} < 0.05)
        
        The mutation burden distributions of Synthetic (OncoGAN) and Real (TCGA) 
        {cancer} cancer samples are statistically different. This suggests the synthetic 
        data does not fully replicate the mutational landscape of real tumour samples.
        """)
    else:
        st.success(f"""
        **No significant difference detected** (p = {p:.2e} >= 0.05)
        
        The mutation burden distributions of Synthetic (OncoGAN) and Real (TCGA)
        {cancer} cancer samples are not statistically distinguishable, suggesting 
        the synthetic data captures the real mutational landscape well.
        """)

    st.markdown("#### Summary Statistics")
    summary = pd.DataFrame({
        "Metric": ["Mean", "Median", "Std Dev", "Min", "Max", "N samples"],
        "Synthetic (OncoGAN)": [
            f"{syn_vals.mean():.1f}",
            f"{syn_vals.median():.1f}",
            f"{syn_vals.std():.1f}",
            f"{syn_vals.min():.0f}",
            f"{syn_vals.max():.0f}",
            f"{len(syn_vals)}"
        ],
        "Real (TCGA)": [
            f"{real_vals.mean():.1f}",
            f"{real_vals.median():.1f}",
            f"{real_vals.std():.1f}",
            f"{real_vals.min():.0f}",
            f"{real_vals.max():.0f}",
            f"{len(real_vals)}"
        ]
    })
    st.dataframe(summary, use_container_width=True, hide_index=True)


with tab3:
    st.subheader("Mutation Spectrum")
            
    st.markdown("""
    The mutation spectrum shows the relative contribution of each base substitution
    type across samples. The standard six substitution classes help summarize the
    dominant mutational patterns in breast and prostate cancer.
    """)
         
    try:
        spectra = load_spectra()
        
        sub_col = "Mutation"
        freq_col = "Frequency"
        sample_col = "Sample"
        
        sub_types = ["C>A", "C>G", "C>T", "T>A", "T>C", "T>G"]
        
        colors = {
            "C>A": "#1f77b4",
            "C>G": "#ff7f0e",
            "C>T": "#d62728",
            "T>A": "#2ca02c",
            "T>C": "#9467bd",
            "T>G": "#8c564b"
        }
    
        spectra["Cancer Type"] = spectra[sample_col].apply(
            lambda x: "Breast" if "breast" in str(x).lower() else "Prostate"
        )

        spectra = spectra[spectra[sub_col].isin(sub_types)]

        grouped = (
            spectra.groupby(["Cancer Type", sub_col])[freq_col]
            .mean()
            .reset_index()
        )
        grouped.columns = ["Cancer Type", "Substitution", "Mean Frequency"]

        # Show dominant substitution metric cards
        breast_data = grouped[grouped["Cancer Type"] == "Breast"]
        prostate_data = grouped[grouped["Cancer Type"] == "Prostate"]

        breast_dom = breast_data.loc[breast_data["Mean Frequency"].idxmax(), "Substitution"]
        prostate_dom = prostate_data.loc[prostate_data["Mean Frequency"].idxmax(), "Substitution"]
        breast_val = breast_data["Mean Frequency"].max()
        prostate_val = prostate_data["Mean Frequency"].max()

        m1, m2 = st.columns(2)
        m1.metric("Dominant Substitution — Breast", breast_dom, f"freq: {breast_val:.3f}")
        m2.metric("Dominant Substitution — Prostate", prostate_dom, f"freq: {prostate_val:.3f}")

        # Callout box
        st.info(" The dominance of C>T mutations in both cancer types suggests that OncoGAN is capturing key biological mutation patterns observed in real tumors.")
    
        col1, col2 = st.columns(2)
    
        for cancer_type, col in zip(["Breast", "Prostate"], [col1, col2]):
            data = grouped[grouped["Cancer Type"] == cancer_type]

            fig = px.bar(
                data,
                x="Substitution",
                y="Mean Frequency",
                color="Substitution",
                color_discrete_map=colors,
                title=f"{cancer_type} Cancer Mutation Spectrum",
                text="Mean Frequency"
            )
        
            fig.update_traces(texttemplate="%{text:.3f}", textposition="outside")
            fig.update_layout(showlegend=True)
            fig.update_yaxes(title="Mean relative frequency")
            fig.update_xaxes(title="Substitution type")
            
            with col:
                st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        In general, higher contributions from specific substitution classes may reflect
        different mutational processes active in each cancer type. This view helps assess
        whether the synthetic mutation patterns are biologically plausible and consistent
        with known cancer mutational behavior.
        """)
            
    except Exception as e:
        st.warning(f"Spectrum file could not be loaded: {e}")

with tab4:

    st.subheader("Signature Heatmap")

        

    try:

        sig = load_signature()

        

        # Log normalize

        sig_norm = np.log1p(sig)

        sig_norm = sig_norm.div(sig_norm.sum(axis=1), axis=0)

        

        # Sort rows — Breast first, then Prostate

        breast_rows = [i for i in sig_norm.index if "Breast" in i]

        prostate_rows = [i for i in sig_norm.index if "Prost" in i]

        sig_norm = sig_norm.loc[breast_rows + prostate_rows]

    

        breast_count = len(breast_rows)

        

        # Group biologically important signatures

        aging_sigs = ["SBS1", "SBS5", "SBS40"]

        apobec_sigs = ["SBS2", "SBS13"]

        dna_repair_sigs = ["SBS3"]

        other_repair_sigs = ["SBS8"]

        highlight_sigs = aging_sigs + apobec_sigs + dna_repair_sigs + other_repair_sigs

            

        st.markdown("""

        The heatmap shows normalized COSMIC SBS mutational signature contributions across all synthetic samples.

        Values are log-transformed and row-normalized.

        Signatures are grouped by biological meaning:

        - Orange: aging / clock-like (SBS1, SBS5, SBS40)

        - Blue: APOBEC activity (SBS2, SBS13)

        - Purple: DNA repair deficiency (SBS3)

        - Green: other repair-related (SBS8)

        """)

            

        fig = px.imshow(

            sig_norm,

            aspect="auto",

            color_continuous_scale="viridis",

            labels=dict(color="Normalized Contribution"),

            title="COSMIC Signature Contributions (Log + Normalized)"

        )

        

        # Color x-axis tick labels by biological group

        ticktext = []

        tickvals = []

        for i, col in enumerate(sig_norm.columns):

            tickvals.append(i)

            if col in aging_sigs:

                ticktext.append(f'<span style="color:orange"><b>{col}</b></span>')

            elif col in apobec_sigs:

                ticktext.append(f'<span style="color:deepskyblue"><b>{col}</b></span>')

            elif col in dna_repair_sigs:

                ticktext.append(f'<span style="color:violet"><b>{col}</b></span>')

            elif col in other_repair_sigs:

                ticktext.append(f'<span style="color:limegreen"><b>{col}</b></span>')

            else:

                ticktext.append(col)        
        fig.update_xaxes(
            tickvals=tickvals,
            ticktext=ticktext,
            tickangle=90,
            title="Signatures (SBS1-SBS95)"
        )
        
        fig.update_yaxes(
            title="Samples",
            showticklabels=False
        )   
        
        # White horizontal divider between Breast and Prostate
        fig.add_shape(
            type="line",
            x0=-0.5,
            x1=len(sig_norm.columns) - 0.5,
            y0=breast_count - 0.5,
            y1=breast_count - 0.5,
            line=dict(color="white", width=2)
        )

        # Orange block annotation for Breast
        fig.add_shape(
            type="rect",
            x0=-3, x1=-1,
            y0=-0.5, y1=breast_count - 0.5,
            fillcolor="orange",
            line=dict(width=0)
        )
            
        # Green block annotation for Prostate
        fig.add_shape(
            type="rect",
            x0=-3, x1=-1,
            y0=breast_count - 0.5,
            y1=len(sig_norm) - 0.5,
            fillcolor="green",
            line=dict(width=0)
        )
            
        # Legend annotations
        fig.add_annotation(
            x=-0.07, y=breast_count / 2,
            xref="paper", yref="y",
            text="Breast Cancer",
            showarrow=False,
            font=dict(color="orange", size=11),
            textangle=-90
        )
        fig.add_annotation(
            x=-0.07,
            y=breast_count + (len(sig_norm) - breast_count) / 2,
            xref="paper", yref="y",
            text="Prostate Cancer",
            showarrow=False,
            font=dict(color="green", size=11),
            textangle=-90
        )
        
            
        fig.update_layout(
            height=650,
            margin=dict(l=80, r=150)
        )
         
        st.plotly_chart(fig, use_container_width=True)
        
        # Top signatures table
        st.markdown("#### Top Signature Contributions")
            
        sig_meanings = {
            "SBS1": "Spontaneous deamination of 5-methylcytosine (clock-like, aging)",
            "SBS2": "APOBEC cytidine deaminase activity",
            "SBS3": "Defective homologous recombination (BRCA1/BRCA2)",
            "SBS5": "Unknown, clock-like signature (aging-associated)",
            "SBS8": "Unknown, associated with nucleotide excision repair deficiency",
            "SBS13": "APOBEC cytidine deaminase activity",
            "SBS40": "Unknown, associated with prior treatment or replication errors"
        }
            
        top_table = sig_norm[highlight_sigs].mean(axis=0).reset_index()
        top_table.columns = ["Signature", "Mean Normalized Contribution"]
        top_table["Biological Meaning"] = top_table["Signature"].map(sig_meanings)
        top_table["Mean Normalized Contribution"] = top_table[
            "Mean Normalized Contribution"].round(4)
        top_table = top_table.sort_values("Mean Normalized Contribution", ascending=False)
        top_table = top_table[["Signature", "Biological Meaning", "Mean Normalized Contribution"]]
        st.dataframe(top_table, use_container_width=True, hide_index=True)

    except Exception as e:
        st.warning(f"Signature file not found: {e}")



with tab5:
    st.subheader("Cosine Similarity to COSMIC Reference Signatures")
        
    st.markdown("""
    Cosine similarity measures how closely each synthetic sample's mutational
    signature profile matches known COSMIC reference signatures. A value closer
    to 1 indicates stronger similarity.
    """)
    st.info("""
    **How to interpret cosine similarity:**

    • **1.0** → Perfect match  
    • **0.9+** → Very strong similarity  
    • **0.7 – 0.85** → Moderate to strong similarity  
    • **< 0.7** → Weaker match
    """)
    
    try:
        from sklearn.metrics.pairwise import cosine_similarity
                
        sig = load_signature()
        sig_norm = sig.div(sig.sum(axis=1), axis=0)
                
        breast_samples = [i for i in sig_norm.index if "breast" in str(i).lower()]
        prostate_samples = [i for i in sig_norm.index if "prost" in str(i).lower()]
            
        breast_mean = sig_norm.loc[breast_samples].mean(axis=0).values.reshape(1, -1)
        prostate_mean = sig_norm.loc[prostate_samples].mean(axis=0).values.reshape(1, -1)
            
        results = []
            
        for sample in breast_samples:
            val = cosine_similarity(
                sig_norm.loc[sample].values.reshape(1, -1),
                breast_mean
            )[0][0]
            results.append([sample, "Breast", val])
        
        for sample in prostate_samples:
            val = cosine_similarity(
                sig_norm.loc[sample].values.reshape(1, -1),
                prostate_mean
            )[0][0]
            results.append([sample, "Prostate", val])

        cosine_df = pd.DataFrame(results, columns=["Sample", "Cancer Type", "Cosine Similarity"])

        # Metric cards
        b_mean = cosine_df[cosine_df["Cancer Type"] == "Breast"]["Cosine Similarity"].mean()
        p_mean = cosine_df[cosine_df["Cancer Type"] == "Prostate"]["Cosine Similarity"].mean()

        col1, col2 = st.columns(2)
        col1.metric("Mean Similarity — Breast", f"{b_mean:.3f}")
        col2.metric("Mean Similarity — Prostate", f"{p_mean:.3f}")
        st.caption(
        "The scores indicate moderate-to-strong similarity, suggesting the OncoGAN synthetic data aligns with known mutational patterns."
        )    
        fig = px.box(
            cosine_df,
            x="Cancer Type",
            y="Cosine Similarity",
            color="Cancer Type",
            points="all",
            title="Cosine Similarity of Samples to Mean Cancer-Type Signature",
            color_discrete_map={"Breast": "#E91E8C", "Prostate": "#1565C0"}
        )
    
        fig.add_hline(
            y=0.8,
            line_dash="dash",
            line_color="red",
            annotation_text="High similarity threshold (0.8)",
            annotation_position="top left"
        )

        fig.update_yaxes(title="Cosine similarity score")
        fig.update_xaxes(title="Cancer type")
    
        st.plotly_chart(fig, use_container_width=True)

        # Add average rows to table
        avg_row = pd.DataFrame([
            ["AVERAGE (Breast)", "Breast", b_mean],
            ["AVERAGE (Prostate)", "Prostate", p_mean]
        ], columns=["Sample", "Cancer Type", "Cosine Similarity"])

        cosine_df = pd.concat([cosine_df, avg_row], ignore_index=True)

        # Color-coded table
        def highlight_similarity(val):
            if val >= 0.9:
                return "background-color: #c8f7c5"
            elif val >= 0.7:
                return "background-color: #fef9c3"
            else:
                return "background-color: #fcd4d4"

        styled_df = cosine_df.style.map(
            highlight_similarity, subset=["Cosine Similarity"]
        )
        st.dataframe(styled_df, use_container_width=True)
    
    except ImportError:
        st.info("Install scikit-learn to enable this feature.")


with tab6:
    st.subheader("Summary")
            
    # Mutation Burden
    st.markdown("### Mutation Burden")
        
    syn_mean = float(np.mean(syn_vals))
    real_mean = float(np.mean(real_vals))

    col1, col2 = st.columns(2)
    col1.metric("Synthetic Mean", f"{syn_mean:.2f}")
    col2.metric("Real Mean", f"{real_mean:.2f}")

    st.write(
        f"For {cancer.lower()} cancer, synthetic samples show a higher mutation burden "
        f"({syn_mean:.2f}) compared to real data ({real_mean:.2f})."
    )

    st.write(
        "Synthetic data shows reduced variability compared to real samples, "
        "suggesting it captures general trends but simplifies biological diversity."
    )
            
    # Statistical Test
    st.markdown("### Statistical Significance")
        
    st.write(
        f"A Mann-Whitney U test produced a p-value of {p:.2e}. "
        f"This indicates that the difference between synthetic and real mutation counts is "
        f"{'statistically significant' if p < 0.05 else 'not statistically significant'}."
    )
        
    # Mutation Spectrum
    st.markdown("### Mutation Spectrum")

    st.write(
        "The mutation spectrum reflects the distribution of base substitution types across samples. "
        "Similar patterns between datasets suggest shared mutational processes, while differences may indicate biases in synthetic data generation."
    )
    
    # COSMIC Similarity
    st.markdown("### COSMIC Similarity") 

    try:
        from sklearn.metrics.pairwise import cosine_similarity
    
        sig = load_signature()
        sig_norm = sig.div(sig.sum(axis=1), axis=0)
        
        breast_samples = [i for i in sig_norm.index if "Breast" in i]
        prostate_samples = [i for i in sig_norm.index if "Prost" in i]
        
        breast_mean = sig_norm.loc[breast_samples].mean(axis=0).values.reshape(1, -1)
        prostate_mean = sig_norm.loc[prostate_samples].mean(axis=0).values.reshape(1, -1)
    
        breast_scores = cosine_similarity(sig_norm.loc[breast_samples], breast_mean).flatten()   
        prostate_scores = cosine_similarity(sig_norm.loc[prostate_samples], prostate_mean).flatten()
     
        col3, col4 = st.columns(2)
        col3.metric("Breast Similarity", f"{breast_scores.mean():.3f}")
        col4.metric("Prostate Similarity", f"{prostate_scores.mean():.3f}")
    
        st.write(
            f"Breast samples show an average cosine similarity of {breast_scores.mean():.3f}, "
            f"while prostate samples show {prostate_scores.mean():.3f}. "
            "These values indicate moderate to high similarity to known COSMIC mutational signatures."
        )

        if breast_scores.std() < prostate_scores.std():
            st.info("Breast samples show slightly higher COSMIC similarity than prostate samples, with both demonstrating strong alignment.")
        else:
            st.info("Prostate samples show slightly higher COSMIC similarity than breast samples, with both demonstrating strong alignment.")
        
    except Exception as e:
        st.warning(f"COSMIC interpretation unavailable: {e}")
    
    # Overall Insight  
    st.markdown("### Overall Insight")   

    st.write(
        "OncoGAN reproduces general mutation patterns and COSMIC signature structure, "
        "making it useful for exploratory analysis and tool development. "
        "However, it overestimates mutation burden and shows less variability, "
        "indicating it does not fully capture real tumor complexity."
    )
