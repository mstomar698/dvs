import React, { FC } from 'react';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';

interface AreaGraphProps {
  data: Record<string, Array<{ sector: string; intensity_sum: number }>>;
  title: string;
}

const AreaGraph: FC<AreaGraphProps> = ({ data, title }) => {
  // we have two title types i.e. pestleInput and sectorInput
  // the code right now is for pestleInput, update it to handle sectorInput too without removing anything for pestleInput graph.
  if (!data) {
    return null;
  }

  const dates = Object.keys(data);
  const sectors = dates.flatMap((date) =>
    data[date].map((item) => item.sector)
  );

  const uniqueSectors = Array.from(new Set(sectors));

  const seriesData = uniqueSectors.map((sector) => {
    const dataPoints = dates.map((date) => {
      const sectorData = data[date].find((item) => item.sector === sector);
      return sectorData ? sectorData.intensity_sum : 0;
    });

    return {
      name: sector,
      data: dataPoints,
    };
  });

  const options: Highcharts.Options = {
    chart: {
      type: 'area',
    },
    title: {
      text: `Intensity of Publishments in ${title} by sectors`,
    },
    xAxis: {
      categories: dates,
    },
    yAxis: {
      title: {
        text: 'Intensity Average',
      },
    },
    plotOptions: {
      area: {
        stacking: 'normal',
        cursor: 'pointer', // Add cursor pointer to the area series
        events: {
          // Handle click event on area series
          click: function (event) {
            const clickedSector = event.point.series.name;
            console.log('Clicked Sector:', clickedSector);
          },
        },
      },
    },
    series: seriesData.map((series, index) => ({
      type: 'area',
      name: series.name,
      data: series.data,
      marker: {
        symbol: 'circle',
        radius: 6,
      },
    })),
    tooltip: {
      shared: true,
      pointFormat:
        '<span style="color:{point.color}">\u25CF</span> {series.name}: <b>{point.y}</b><br/>',
    },
  };

  return <HighchartsReact highcharts={Highcharts} options={options} />;
};

export default AreaGraph;
