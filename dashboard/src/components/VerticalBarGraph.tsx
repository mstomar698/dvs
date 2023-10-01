import React, { FC } from 'react';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';

interface VerticalBarGraphProps {
  data: Record<string, number>;
}

const VerticalBarGraph: FC<VerticalBarGraphProps> = ({ data }) => {
  if (!data) {
    return null;
  }

  const categories = Object.keys(data);
  const counts = categories.map((category) => data[category]);

  const randomColors = counts.map(() => {
    return `#${Math.floor(Math.random() * 16777215).toString(16)}`;
  });

  const options: Highcharts.Options = {
    chart: {
      type: 'column',
      height: 400,
    },
    title: {
      text: 'Article Sources and Published Counts',
    },
    xAxis: {
      categories: categories,
      labels: {
        rotation: -90,
        style: {
          fontSize: '9px',
        },
      },
    },
    yAxis: {
      title: {
        text: 'Articles Published',
      },
    },
    series: [
      {
        showInLegend: false,
        name: 'Count',
        type: 'column',
        data: counts.map((count, index) => ({
          y: count,
          color: randomColors[index],
        })),
        dataLabels: {
          enabled: true,
          format: '{y}',
        },
      },
    ],
  };

  return <HighchartsReact highcharts={Highcharts} options={options} />;
};

export default VerticalBarGraph;
