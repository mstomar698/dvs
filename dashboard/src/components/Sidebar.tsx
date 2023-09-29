import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faCalendarCheck,
  faMessage,
  faClock,
  faUserPlus,
  faToggleOn,
} from '@fortawesome/free-solid-svg-icons';
import {
  CModal,
  CModalTitle,
  CModalBody,
  CModalFooter,
  CModalHeader,
  CButton,
} from '@coreui/react';

interface SidebarProps {
  visibilityData: {
    visibleModal: boolean;
    setVisibleModal: (visible: boolean) => void;
  };
  urlData: {
    url: string;
  };
}

const Sidebar: React.FC<SidebarProps> = (props) => {
  library.add(faCalendarCheck, faMessage, faClock, faUserPlus, faToggleOn);

  return (
    <div className="sidebar">
      <p>Dashboard</p>

      <ul>
        <li>
          <FontAwesomeIcon icon="calendar-check" />
          <span>Data</span>
        </li>
      </ul>
    </div>
  );
};

export default Sidebar;
