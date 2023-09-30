import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import BackgroundHeader from '../components/BackgroundHeader';
import axios from 'axios';
import PieChart from '../components/PieChart';
import Card from '../components/Card';
import DotGraph from '../components/DotGraph';
import BarGraph from '../components/BarGraph';
import VerticalBarGraph from '../components/VerticalBarGraph';

const HomeScreen: React.FC = () => {
  const [displaySidebar, setDisplaySidebar] = useState(true);
  const [visibleModal, setVisibleModal] = useState(false);
  const [url, setUrl] = useState('');
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    const handleResize = () => {
      setDisplaySidebar(window.innerWidth >= 991);
    };

    handleResize();

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const urls = [
          '/dashboard/home/',
          '/dashboard/pie_chart_country/',
          '/dashboard/bar_graph_Source/',
          '/dashboard/pie_chart_pestle/',
          '/dashboard/bar_graph_sector_topic_likelihood/',
          '/dashboard/dot_graph_for_insights_published_date/',
        ];

        const requests = urls.map(async (url) => {
          const response = await axios.get(url);
          const trimmedUrl = url.replace('/dashboard/', '');
          const cleanedUrl = trimmedUrl.replace(/\/+/g, '');
          return { [cleanedUrl]: response.data };
        });

        const responseData = await Promise.all(requests);

        const combinedData = Object.assign({}, ...responseData);
        setData(combinedData);
        console.log(combinedData);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  useEffect(() => {
    console.log('Fetched data:', data);
  }, [data]);

  return (
    <div>
      <Navbar
        displaySidebar={displaySidebar}
        toggleSideBar={() => setDisplaySidebar(!displaySidebar)}
        visibilityData={{ visibleModal, setVisibleModal }}
        urlData={{ url, setUrl }}
      />
      <div
        className={`transition-all duration-300 ${
          displaySidebar ? 'ml-[230px]' : 'ml-[0px]'
        }`}
      >
        <BackgroundHeader displaySidebar={displaySidebar} />
        <div className="flex flex-row max-sm:flex-col">
          <div className="w-1/5 p-4 rounded border border-gray-300 shadow-md hover:shadow-lg">
            <Card message={data?.home?.message} />
          </div>
          {/* 
        '/dashboard/home/',✅
        '/dashboard/pie_chart_country/',✅
        '/dashboard/bar_graph_Source/',✅
        '/dashboard/pie_chart_pestle/',✅
        '/dashboard/bar_graph_sector_topic_likelihood/',✅
        '/dashboard/dot_graph_for_insights_published_date/',✅
        */}
          {/* 
        
        */}
          <div className="w-4/5 flex flex-row p-4">
            <div className="w-3/5 p-4 rounded border border-gray-300 shadow-md hover:shadow-lg">
              <PieChart
                data={data?.pie_chart_country}
                title="Articles Published by each Country"
              />
            </div>
            <div className="w-2/5 p-4 rounded border border-gray-300 shadow-md hover:shadow-lg">
              <PieChart
                data={data?.pie_chart_pestle}
                title="Articles Published for each Pestle"
              />
            </div>
          </div>
        </div>
        <div className="lg:w-full">
          <div className="p-4 rounded border border-gray-300 shadow-md hover:shadow-lg">
            <DotGraph data={data?.dot_graph_for_insights_published_date} />
          </div>
        </div>
        <div className="lg:flex">
          <div className="lg:w-1/2 p-4 rounded border border-gray-300 shadow-md hover:shadow-lg">
            <BarGraph data={data?.bar_graph_sector_topic_likelihood} />
          </div>
          <div className="lg:w-1/2 p-4 rounded border border-gray-300 shadow-md hover:shadow-lg">
            <VerticalBarGraph data={data?.bar_graph_Source} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomeScreen;
