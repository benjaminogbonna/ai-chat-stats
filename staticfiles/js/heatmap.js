document.addEventListener("DOMContentLoaded", function () {
    const container = document.getElementById("heatmap");
    const boxSize = 15;
    const padding = 1;
    const margin = { top: 20, right: 20, bottom: 10, left: 30 };
    const colors = ['#ebedf0', '#9be9a8', '#40c463', '#30a14e', '#216e39'];
    const svgWidth = 900;
    const svgHeight = 150 + margin.top + margin.bottom;

    const svg = d3
        .select(container)
        .append("svg")
        .attr("width", "100%")
        .attr("height", svgHeight)
        .attr("viewBox", `0 0 ${svgWidth} ${svgHeight}`)
        .attr("preserveAspectRatio", "xMidYMid meet");

    function drawHeatmap(data) {
        svg.selectAll("*").remove(); // Clear existing heatmap
        const xScale = d3.scaleLinear().domain([0, 52]).range([0, svgWidth - margin.left - margin.right]);
        const yScale = d3.scaleLinear().domain([0, 7]).range([0, svgHeight - margin.top - margin.bottom]);
        const dayLabels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
        const monthLabels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

        // Add labels
        svg.selectAll(".day-label")
            .data(dayLabels)
            .enter()
            .append("text")
            .attr("x", margin.left - 10)
            .attr("y", (d, i) => margin.top + yScale(i) + boxSize / 2)
            .attr("text-anchor", "end")
            .text(d => d)
            .style("font-size", "10px");

        svg.selectAll(".month-label")
            .data(monthLabels)
            .enter()
            .append("text")
            .attr("x", (d, i) => margin.left + xScale((i * 52) / 12) + boxSize / 2)
            .attr("y", margin.top - 5)
            .text(d => d)
            .style("font-size", "10px");

        // Draw heatmap boxes
        data.forEach(([week, weekday, count]) => {
            const color = count === 0
                ? colors[0]
                : count < 5
                    ? colors[1]
                    : count < 10
                        ? colors[2]
                        : count < 20
                            ? colors[3]
                            : colors[4];

            svg.append("rect")
                .attr("x", margin.left + xScale(week))
                .attr("y", margin.top + yScale(weekday))
                .attr("width", boxSize)
                .attr("height", boxSize)
                .attr("fill", color)
                .attr("rx", 2) // Add slight rounding to the edges
                .attr("ry", 2)
                .attr("stroke", "#ccc");
        });
    }

    // Draw the initial heatmap
    drawHeatmap(heatmapData);

    // Handle year link clicks
    document.querySelectorAll(".year-link").forEach(link => {
        link.addEventListener("click", function (e) {
            // e.preventDefault();
            const year = this.getAttribute("data-year");

            // Fetch new heatmap data for the selected year
            fetch(`/${slug}/${year}/`, {
                method: "GET",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
                .then(response => response.json())
                .then(data => {
                    drawHeatmap(data);
                })
                .catch(err => {
                    console.error("Error fetching heatmap data:", err);
                });
        });
    });
});
