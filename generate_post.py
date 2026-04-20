#!/usr/bin/env python3
"""Generate blog post assets for RI Governor McKee's CTC analysis."""

import os
import json
from pathlib import Path

from ri_mckee_ctc.charts import (
    create_net_income_change_chart,
    create_avg_benefit_by_decile_chart,
    create_winners_by_decile_chart,
)
from ri_mckee_ctc.statewide import (
    REVENUE_IMPACT_MILLIONS,
    PCT_FAMILIES_BENEFITING,
    POVERTY_IMPACT,
    GINI_IMPACT,
)

# Output directories
OUTPUT_DIR = Path("output")
CHARTS_DIR = OUTPUT_DIR / "charts"

# GitHub Pages base URL
GITHUB_PAGES_BASE = "https://policyengine.github.io/ri-mckee-ctc-calc"

# HTML template for standalone chart files
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title} | PolicyEngine</title>
    <meta name="description" content="{meta_description}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{canonical_url}">

    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:title" content="{title} | PolicyEngine">
    <meta property="og:description" content="{meta_description}">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:site_name" content="PolicyEngine">
    <meta property="og:image" content="https://policyengine.org/assets/logos/policyengine/teal-square.png">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="{title} | PolicyEngine">
    <meta name="twitter:description" content="{meta_description}">
    <meta name="twitter:image" content="https://policyengine.org/assets/logos/policyengine/teal-square.png">
    <meta name="twitter:site" content="@ThePolicyEngine">

    <!-- Structured Data (JSON-LD) -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{title}",
        "description": "{meta_description}",
        "url": "{canonical_url}",
        "author": {{
            "@type": "Organization",
            "name": "PolicyEngine",
            "url": "https://policyengine.org"
        }},
        "publisher": {{
            "@type": "Organization",
            "name": "PolicyEngine",
            "url": "https://policyengine.org",
            "logo": {{
                "@type": "ImageObject",
                "url": "https://policyengine.org/assets/logos/policyengine/teal-square.png"
            }}
        }},
        "mainEntityOfPage": {{
            "@type": "WebPage",
            "@id": "{canonical_url}"
        }}
    }}
    </script>

    <link rel="icon" type="image/png" href="https://policyengine.org/favicon.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
    <script defer src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-2YHG89FY0N"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'G-2YHG89FY0N', {{ tool_name: 'ri-mckee-ctc-calc' }});
    </script>
    <script>
    (function() {{
      var TOOL_NAME = 'ri-mckee-ctc-calc';
      if (typeof window === 'undefined' || !window.gtag) return;

      var scrollFired = {{}};
      window.addEventListener('scroll', function() {{
        var docHeight = document.documentElement.scrollHeight - window.innerHeight;
        if (docHeight <= 0) return;
        var pct = Math.floor((window.scrollY / docHeight) * 100);
        [25, 50, 75, 100].forEach(function(m) {{
          if (pct >= m && !scrollFired[m]) {{
            scrollFired[m] = true;
            window.gtag('event', 'scroll_depth', {{ percent: m, tool_name: TOOL_NAME }});
          }}
        }});
      }}, {{ passive: true }});

      [30, 60, 120, 300].forEach(function(sec) {{
        setTimeout(function() {{
          if (document.visibilityState !== 'hidden') {{
            window.gtag('event', 'time_on_tool', {{ seconds: sec, tool_name: TOOL_NAME }});
          }}
        }}, sec * 1000);
      }});

      document.addEventListener('click', function(e) {{
        var link = e.target && e.target.closest ? e.target.closest('a') : null;
        if (!link || !link.href) return;
        try {{
          var url = new URL(link.href, window.location.origin);
          if (url.hostname && url.hostname !== window.location.hostname) {{
            window.gtag('event', 'outbound_click', {{
              url: link.href,
              target_hostname: url.hostname,
              tool_name: TOOL_NAME
            }});
          }}
        }} catch (err) {{}}
      }});
    }})();
    </script>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            font-family: 'Roboto', sans-serif;
            background: #fff;
        }}
        #chart {{
            width: 100%;
            height: 600px;
        }}
        h1 {{
            font-size: 1.5rem;
            color: #2D3748;
            text-align: center;
            margin-bottom: 0.5rem;
        }}
    </style>
</head>
<body>
    <main>
        <h1>{title}</h1>
        <div id="chart" role="img" aria-label="{title}"></div>
        <noscript>
            <p>This interactive chart requires JavaScript to display. Please enable JavaScript in your browser to view the {title} visualization.</p>
        </noscript>
    </main>
    <script>
        function renderChart() {{
            var figure = {figure_json};
            Plotly.newPlot('chart', figure.data, figure.layout, {{responsive: true}});
        }}
        if (typeof Plotly !== 'undefined') {{
            renderChart();
        }} else {{
            document.addEventListener('DOMContentLoaded', function() {{
                var check = setInterval(function() {{
                    if (typeof Plotly !== 'undefined') {{
                        clearInterval(check);
                        renderChart();
                    }}
                }}, 100);
            }});
        }}
    </script>
</body>
</html>
"""


# SEO metadata for each chart page
CHART_META = {
    "net-income-change.html": {
        "meta_description": (
            "Interactive chart showing how Rhode Island Governor McKee's proposed "
            "$325 child tax credit changes net income for families at different "
            "earnings levels. Analysis by PolicyEngine."
        ),
    },
    "winners-by-decile.html": {
        "meta_description": (
            "Interactive chart showing winners and losers of Rhode Island Governor "
            "McKee's proposed child tax credit by income decile. Analysis by PolicyEngine."
        ),
    },
    "avg-benefit-by-decile.html": {
        "meta_description": (
            "Interactive chart showing the average household benefit of Rhode Island "
            "Governor McKee's proposed child tax credit by income decile. Analysis by PolicyEngine."
        ),
    },
}


def save_chart_html(fig, filename: str, title: str) -> None:
    """Save a Plotly figure as a standalone HTML file."""
    figure_json = fig.to_json()
    canonical_url = f"{GITHUB_PAGES_BASE}/{filename}"
    meta = CHART_META.get(filename, {})
    meta_description = meta.get(
        "meta_description",
        f"{title} - Analysis of Rhode Island Governor McKee's proposed child tax credit by PolicyEngine.",
    )
    html_content = HTML_TEMPLATE.format(
        title=title,
        figure_json=figure_json,
        canonical_url=canonical_url,
        meta_description=meta_description,
    )

    filepath = CHARTS_DIR / filename
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"  Created: {filepath}")


def generate_charts() -> None:
    """Generate all chart HTML files."""
    print("Generating charts...")

    # Net income change chart
    fig = create_net_income_change_chart(num_children=2)
    save_chart_html(fig, "net-income-change.html", "Net Income Change - RI CTC")

    # Winners by decile chart
    fig = create_winners_by_decile_chart()
    save_chart_html(fig, "winners-by-decile.html", "Winners by Decile - RI CTC")

    # Average benefit by decile chart
    fig = create_avg_benefit_by_decile_chart()
    save_chart_html(fig, "avg-benefit-by-decile.html", "Average Benefit by Decile - RI CTC")


def generate_markdown() -> str:
    """Generate the blog post markdown content."""
    return f"""Rhode Island Governor Dan McKee has proposed a state child tax credit as part of his fiscal year 2026 budget. The proposal would provide a $325 fully refundable credit per child under 19 years old, while eliminating the state's personal exemption for dependent children.

We at PolicyEngine have analyzed the effects of this proposed change on Rhode Island and its residents.

Key results for 2026:

* Costs the state ${abs(REVENUE_IMPACT_MILLIONS):.1f} million (net)
* Benefits {PCT_FAMILIES_BENEFITING}% of Rhode Island families
* Reduces child poverty by {abs(POVERTY_IMPACT):.1f}%
* Lowers the Gini index of inequality by {abs(GINI_IMPACT):.2f}%

*[Use PolicyEngine](https://www.policyengine.org/us) to view the full results or calculate the effect on your household.*

## Background

Rhode Island currently provides a personal exemption for dependent children that reduces taxable income. However, this exemption primarily benefits higher-income families who have sufficient tax liability to utilize it. Lower-income families often cannot fully benefit from the exemption.

Governor McKee's proposal would replace this exemption with a $325 fully refundable child tax credit. Key features include:

- **Credit amount:** $325 per qualifying child
- **Age eligibility:** Children under 19 years old
- **Refundability:** Fully refundable, meaning families can receive the credit even with no tax liability
- **Phase-out:** Begins at $261,000 for all filing statuses
- **Exemption integration:** Eliminates the personal exemption for dependent children under 19

The net fiscal cost is approximately ${abs(REVENUE_IMPACT_MILLIONS):.1f} million, as the elimination of the dependent exemption offsets a significant portion of the credit's cost.

## Household impacts

The reform primarily benefits lower-income families with children. A married couple with two children would see their net income change as shown in Figure 1.

<iframe src="{GITHUB_PAGES_BASE}/net-income-change.html" width="100%" height="650" frameborder="0" title="Net income change chart for a married couple with two children under RI CTC proposal" loading="lazy"></iframe>

Lower-income households gain the most because the $325 credit is fully refundable, while the eliminated personal exemption provided less value to families with lower tax liability. Higher-income households near the phase-out threshold may see smaller gains or even small losses if they previously benefited more from the personal exemption.

## Statewide impacts

For tax year 2026, the proposal would reduce state revenues by ${abs(REVENUE_IMPACT_MILLIONS):.1f} million (net), according to PolicyEngine's static modeling. The standalone credit would cost approximately $60 million, but eliminating the dependent personal exemption saves roughly $25 million.

The reform would raise the net income of {PCT_FAMILIES_BENEFITING}% of Rhode Island families, with beneficiaries concentrated in lower income deciles. Figure 2 shows the share of residents in each income decile that would gain or lose from the reform.

<iframe src="{GITHUB_PAGES_BASE}/winners-by-decile.html" width="100%" height="650" frameborder="0" title="Winners and losers by income decile under RI CTC proposal" loading="lazy"></iframe>

Average benefits are largest for lower-income households due to the credit's refundability.

<iframe src="{GITHUB_PAGES_BASE}/avg-benefit-by-decile.html" width="100%" height="650" frameborder="0" title="Average benefit by income decile under RI CTC proposal" loading="lazy"></iframe>

We project that the proposal would reduce child poverty by {abs(POVERTY_IMPACT):.1f}% as measured by the Supplemental Poverty Measure. The Gini index of income inequality would decrease by {abs(GINI_IMPACT):.2f}%.

## Conclusion

Governor McKee's proposed child tax credit would shift Rhode Island's approach to supporting families with children from an income exemption to a refundable credit. This change would direct more benefits to lower-income families while reducing support for higher-income households.

If enacted, Rhode Island would become the 12th state to adopt a refundable child tax credit, following the "New England model" approach used by Massachusetts and Maine.

As policymakers evaluate reforms such as these, analytical tools like PolicyEngine offer critical insights into the impacts on diverse household compositions and the broader economy.

---

**Explore our [Rhode Island CTC Calculator](https://www.policyengine.org/us/rhode-island-ctc-calculator)**, developed in partnership with the Niskanen Center, to model how different child tax credit designs would affect your household and the state. You can input your household details and create custom CTC reforms to see their personalized impact.

We invite you to explore our [additional analyses](https://www.policyengine.org/us/research) and use [PolicyEngine](https://www.policyengine.org/us) to calculate your own tax benefits or design custom policy reforms.
"""


def generate_robots_txt() -> None:
    """Generate robots.txt for the GitHub Pages site."""
    print("Generating robots.txt...")
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        f"\nSitemap: {GITHUB_PAGES_BASE}/sitemap.xml\n"
    )
    filepath = CHARTS_DIR / "robots.txt"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Created: {filepath}")


def generate_sitemap() -> None:
    """Generate sitemap.xml for the GitHub Pages site."""
    print("Generating sitemap.xml...")
    chart_files = ["net-income-change.html", "winners-by-decile.html", "avg-benefit-by-decile.html"]
    urls = "\n".join(
        f"  <url>\n    <loc>{GITHUB_PAGES_BASE}/{f}</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>"
        for f in chart_files
    )
    content = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n"
        "</urlset>\n"
    )
    filepath = CHARTS_DIR / "sitemap.xml"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Created: {filepath}")


def main():
    """Generate all blog post assets."""
    # Create output directories
    OUTPUT_DIR.mkdir(exist_ok=True)
    CHARTS_DIR.mkdir(exist_ok=True)

    # Generate charts
    generate_charts()

    # Generate SEO files
    generate_robots_txt()
    generate_sitemap()

    # Generate markdown
    print("\nGenerating markdown...")
    markdown_content = generate_markdown()
    markdown_path = OUTPUT_DIR / "ri-mckee-ctc.md"
    with open(markdown_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    print(f"  Created: {markdown_path}")

    print("\n✓ All assets generated successfully!")
    print(f"\nTo deploy charts to GitHub Pages:")
    print(f"  1. Push to main branch")
    print(f"  2. Charts will be available at: {GITHUB_PAGES_BASE}/")


if __name__ == "__main__":
    main()
