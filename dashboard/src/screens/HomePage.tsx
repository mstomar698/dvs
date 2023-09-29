import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import BackgroundHeader from '../components/BackgroundHeader';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';

const HomeScreen: React.FC = () => {
  const [displaySidebar, setDisplaySidebar] = useState(true);
  const [visibleModal, setVisibleModal] = useState(false);
  const [url, setUrl] = useState('');
  const [rec_data, setRecData] = useState<any>(null);

  const navigate = useNavigate();

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

  const fetchInfo = async () => {
    try {
      const response = await axios.get(`/dashboard/home/`);
      console.log(response.data);
      setRecData(response);
    } catch (error) {
      navigate('/', { replace: true });
    }
  };

  useEffect(() => {
    fetchInfo();
  }, []);

  return (
    <div className="page-body">
      <Navbar
        displaySidebar={displaySidebar}
        toggleSideBar={() => setDisplaySidebar(!displaySidebar)}
        visibilityData={{ visibleModal, setVisibleModal }}
        urlData={{ url, setUrl }}
      />
      <div
        className={`ml-${
          displaySidebar ? (window.innerWidth >= 991 ? '230' : '0') : '0'
        }`}
      >
        <BackgroundHeader displaySidebar={displaySidebar} />

        <center>{/* {{data}} */}</center>
      </div>
    </div>
  );
};

export default HomeScreen;
