import React from 'react';
import ReactDOM from 'react-dom/client';
import { Workbench } from './components/Workbench/Workbench';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Workbench />
  </React.StrictMode>
);