import React, { useEffect, useRef } from 'react';
import Chart, { ChartConfiguration } from 'chart.js/auto';

interface PieChartProps {
  data: Record<string, number>;
  title: string;
}

const PieChart: React.FC<PieChartProps> = ({ data, title }) => {
  const chartRef = useRef<HTMLCanvasElement | null>(null);
  const chartInstance = useRef<Chart<'pie', number[], unknown> | null>(null);

  useEffect(() => {
    if (chartInstance.current) {
      chartInstance.current.destroy();
    }
    if (!data) return;

    if (chartRef.current) {
      const labels = Object.keys(data);
      const values = Object.values(data);

      const backgroundColors = labels.map(() => getRandomColor());

      const chartConfig: ChartConfiguration<'pie'> = {
        type: 'pie',
        data: {
          labels: labels,
          datasets: [
            {
              data: values,
              backgroundColor: backgroundColors,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          onClick: (event, elements) => {
            if (elements.length > 0) {
              const clickedIndex = elements[0].index;
              const clickedLabel = labels[clickedIndex];
              const clickedValue = values[clickedIndex];
              console.log(`Clicked Label: ${clickedLabel}`);
              console.log(`Clicked Value: ${clickedValue}`);
            }
          },
          elements: {
            arc: {
              spacing: 0,
            },
          },
          plugins: {
            legend: {
              position: 'right',
              labels: {
                font: {
                  size: 10,
                },
              },
            },
          },
        },
      };

      chartInstance.current = new Chart(chartRef.current, chartConfig);
    }
  }, [data]);

  const getRandomColor = () => {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  };

  return (
    <div>
      <p className='text-xl font-weight-900 font-semibold'>{title}</p>      
      <div className="w-full h-auto">
        <canvas ref={chartRef} />
      </div>
    </div>
  );
};

export default PieChart;