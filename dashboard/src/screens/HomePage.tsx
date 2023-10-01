import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import BackgroundHeader from '../components/BackgroundHeader';
import axios from 'axios';
import PieChart from '../components/PieChart';
import Card from '../components/Card';
import DotGraph from '../components/DotGraph';
import BarGraph from '../components/BarGraph';
import VerticalBarGraph from '../components/VerticalBarGraph';
import AreaGraph from '../components/AreaGraph';
import SectorGraph from '../components/SectorAreaGraph';
import DetailTable from '../components/DetailTable';

const HomeScreen: React.FC = () => {
  const [displaySidebar, setDisplaySidebar] = useState(true);
  const [visibleModal, setVisibleModal] = useState(false);
  const [url, setUrl] = useState('');
  const [data, setData] = useState<any>(null);
  const [regionInput, setRegionInput] = useState<string>('');
  const [pestleInput, setPestleInput] = useState<string>('');
  const [sectorInput, setSectorInput] = useState<string>('');
  const [topicInput, setTopicInput] = useState<string>('');

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
          '/dashboard/pie_chart_region/',
          '/dashboard/bar_graph_Source/',
          '/dashboard/pie_chart_pestle/',
          '/dashboard/pie_chart_sector/',
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
        data={{ data, setData }}
        regionInput={{ regionInput, setRegionInput }}
        pestleInput={{ pestleInput, setPestleInput }}
        sectorInput={{ sectorInput, setSectorInput }}
        topicInput={{ topicInput, setTopicInput }}
      />

      <div
        className={`transition-all duration-300 ${
          displaySidebar ? 'ml-[230px]' : 'ml-[0px]'
        }`}
        onClick={() => setVisibleModal(false)}
      >
        <BackgroundHeader displaySidebar={displaySidebar} />
        {data?.table_topic_insights_details ? (
          <DetailTable data={data?.table_topic_insights_details} />
        ) : (
          <div>
            <div className="flex flex-row max-sm:flex-col">
              <div className="w-max p-2">
                <Card message={data?.home?.message} />
              </div>
              {/* 
        '/dashboard/home/',✅
        '/dashboard/pie_chart_region/',✅
        '/dashboard/bar_graph_Source/',✅
        '/dashboard/pie_chart_pestle/',✅
        '/dashboard/bar_graph_sector_topic_likelihood/',✅
        '/dashboard/dot_graph_for_insights_published_date/',✅
        '/dashboard/pie_chart_sector/',✅
        */}
              {/* 
          /dashboard/pie_chart_country/ ✅{take country name as formdata } {will be active when click on regional publishes}
          /dashboard/dot_graph_pestle_sector_inetnsity/✅ {take pestle name as formdata } {will be active when click on sectorwise intensity}
          /dashboard/dot_graph_sector_topic_relevance/✅  {take sector name as formdata } {will be active when click on topic relevences}
          /dashboard/table_topic_insights_details/ ✅{take sector and topic name as formdata } {will be active when click on all publishes}
        */}
              <div className="w-full flex flex-row space-x-2 p-2">
                <div className="w-3/5 p-4 rounded border border-gray-300 shadow-md hover:shadow-lg">
                  {data?.pie_chart_country ? (
                    <div>
                      {data?.pie_chart_country.length !== 0 ? (
                        <PieChart
                          data={data?.pie_chart_country}
                          title="Articles Published by each Country"
                        />
                      ) : (
                        <PieChart
                          data={data?.pie_chart_region}
                          title="No Data found for this Region"
                        />
                      )}
                    </div>
                  ) : (
                    <PieChart
                      data={data?.pie_chart_region}
                      title="Articles Published by each Region"
                    />
                  )}
                  {/* <PieChart
                data={data?.pie_chart_country}
                title="Articles Published by each Country"
              /> */}
                </div>
                <div className="w-2/5 p-4 rounded border border-gray-300 shadow-md hover:shadow-lg">
                  <PieChart
                    data={data?.pie_chart_pestle}
                    title="Articles Published for each Pestle"
                  />
                </div>
              </div>
            </div>
            {data?.dot_graph_pestle_sector_inetnsity && (
              <div className="lg:w-full p-2">
                <div className="p-4 rounded border border-gray-300 shadow-md hover:shadow-lg">
                  <AreaGraph
                    data={data?.dot_graph_pestle_sector_inetnsity}
                    title={pestleInput}
                  />
                </div>
              </div>
            )}
            {data?.dot_graph_sector_topic_relevance && (
              <div className="lg:w-full p-2">
                <div className="p-4 rounded border border-gray-300 shadow-md hover:shadow-lg">
                  <SectorGraph
                    data={data?.dot_graph_sector_topic_relevance}
                    title={sectorInput}
                  />
                </div>
              </div>
            )}
            <div className="lg:flex p-2 space-x-2">
              <div className="lg:w-1/2 p-4 rounded border border-gray-300 shadow-md hover:shadow-lg">
                <BarGraph data={data?.bar_graph_sector_topic_likelihood} />
              </div>
              <div className="lg:w-1/2 p-4 rounded border border-gray-300 shadow-md hover:shadow-lg">
                <PieChart
                  data={data?.pie_chart_sector}
                  title="Publish Counts in each Sector"
                />
              </div>
            </div>
            <div className="lg:w-full p-2">
              <div className="p-4 rounded border border-gray-300 shadow-md hover:shadow-lg">
                <DotGraph data={data?.dot_graph_for_insights_published_date} />
              </div>
            </div>
            <div className="lg:w-full p-2">
              <div className="p-4 rounded border border-gray-300 shadow-md hover:shadow-lg">
                <VerticalBarGraph data={data?.bar_graph_Source} />
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default HomeScreen;
