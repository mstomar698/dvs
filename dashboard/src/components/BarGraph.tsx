import React, { FC } from 'react';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';

interface BarGraphProps {
  data: Record<string, any>;
}

const BarGraph: FC<BarGraphProps> = ({ data }) => {
  if (!data) {
    return null;
  }

  const categories = Object.keys(data);
  const seriesData = categories.flatMap((category) => {
    const topics = data[category];
    return topics.map((item: any) => {
      return {
        name: item.topic,
        stack: category,
        y: item.avg_likelihood,
      };
    });
  });

  // Generate random colors for each data point
  const randomColors = seriesData.map(() => {
    return `#${Math.floor(Math.random() * 16777215).toString(16)}`;
  });

  const options: Highcharts.Options = {
    chart: {
      type: 'bar',
    },
    title: {
      text: 'Average Likelihood by Category and Topic',
    },
    xAxis: {
      categories: seriesData.map((item) => item.name),
      reversed: true,
      labels: {
        rotation: -45,
      },
      scrollbar: {
        enabled: true,
      },
    },
    yAxis: {
      title: {
        text: 'Average Likelihood',
      },
      max: 4,
    },
    series: [
      {
        type: 'bar',
        data: seriesData.map((item, index) => ({
          ...item,
          color: randomColors[index], // Assign random color to each bar
        })),
        cursor: 'pointer',
        events: {
          click: function (event) {
            const topic = event.point.name;
            const category = event.point.series.name;
            console.log(`Topic: ${topic}, Sector: ${category}`);
          },
        },
      },
    ],
    plotOptions: {
      series: {
        stacking: 'normal',
      },
    },
    tooltip: {
      pointFormat:
        '<b>{point.name}</b><br>Sector: {point.stack}<br>Average Likelihood: {point.y}',
    },
  };

  return <HighchartsReact highcharts={Highcharts} options={options} />;
};

export default BarGraph;
