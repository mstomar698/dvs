import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import BackgroundHeader from '../components/BackgroundHeader';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

const HomeScreen: React.FC = () => {
  const [displaySidebar, setDisplaySidebar] = useState(true);
  const [visibleModal, setVisibleModal] = useState(false);
  const [url, setUrl] = useState('');
  const [data, setData] = useState<any>(null);

  // const navigate = useNavigate();

  // Handle Sidebar and its props using screen-width.
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

  // Fetch data from API and store it in state.
  useEffect(() => {
    const fetchData = async () => {
      try {
        const urls = [
          // All GET Urls data for better performance
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
      <div className={displaySidebar ? 'ml-[230px]' : 'ml-[0px]'}>
        <BackgroundHeader displaySidebar={displaySidebar} />
        {/* 
        '/dashboard/home/',
        '/dashboard/pie_chart_country/',
        '/dashboard/bar_graph_Source/',
        '/dashboard/pie_chart_pestle/',
        '/dashboard/bar_graph_sector_topic_likelihood/',
        '/dashboard/dot_graph_for_insights_published_date/',
        */}
        <div className="flex flex-row ">
          <div className="w-2/5 p-4  border-2 border-blue-500">
            Home Message Here {data?.home?.message}
          </div>
          <div className="w-1/3 p-4 border-2 border-green-500">
            Countries published the articles
            <div>Pie Chart for country pie_chart_country</div>
          </div>
          <div className="w-1/3 p-4 0 border-2 border-yellow-500">
            Pestle related to articles
            <div>Pie Chart for Pestles pie_chart_pestle</div>
          </div>
        </div>
        <div className="lg:w-full">
          <div className="h-[300px]  p-4 border-2 border-gray-500">
            all insights in the data in date order
            <div>dot_graph_for_insights_published_date</div>
          </div>
        </div>
        <div className="lg:flex">
          <div className="h-[300px] lg:w-1/2 p-4  border-2 border-purple-500">
            all likelihood in the data in date order
            <div>bar_graph_sector_topic_likelihood</div>
          </div>
          <div className="h-[300px] lg:w-1/2 p-4  border-2 border-red-500">
            all source in the data in date order
            <div>bar_graph_Source</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomeScreen;
